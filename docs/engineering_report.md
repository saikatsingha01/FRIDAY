# FRIDAY Engineering Review

Source: 5000-test randomized stress run (seed 20260804, 2026-08-05) +
code inspection. Companion doc: `docs/ISSUE_TRACKER.md` (issue database),
`docs/RANDOM_STRESS_TEST.md` (per-test data).

---

## 1. Overall Health

| Metric | Value |
|---|---|
| Tests completed | 5000/5000 |
| Pass | 4277 (85.5%) |
| Fail | 717 (14.3%) |
| Error | 6 (0.1%) |
| Silent data corruption (wrong value stored as "updated") | Confirmed, ~64 tests |
| Model | llama3.2:3b + nomic-embed-text |

**Health verdict: functional but not trustworthy for memory-write decisions.**
The deterministic layer works (no-write D 99.7%, history H 100%, seeded
episodic retrieval R-epi 100%). The failure mass concentrates in **one
LLM-driven predicate** (`is_uncertain()` → `needs_clarification`) and **one
extraction leak** (context value stored as new fact). Neither is a hardware
pipeline fault; both are fixable at the prompt/gate layer with low risk.

Biggest risks in order:
1. **Context value leak (RC-02)** — silently stores the *wrong* fact while
   reporting success. Critical.
2. **Clarification over-triggering (RC-01)** — ~466 tests; makes store/update/
   forget unusable for ordinary casual statements.
3. **Retrieval conflation (RC-04)** — R-sem/R-pro/R-hist failures may be
   mostly *inherited* store failures; metrics are currently unreadable.

---

## 2. Architecture Diagram

```
 Voice/Text
    |
    v
 [TRIAGE]  classify_trivial (triage.py)          -> greeting/farewell/gratitude/affirmation/small_talk (skip LLM)
    | (not trivial)
    v
 [UNDERSTANDING ORCHESTRATOR]  analyze()  (understanding_orchestrator.py)
    |  build_understanding_prompt() (understanding_prompt.py: 936-line SYSTEM_PROMPT
    |      + optional RECENT CONVERSATION block, lines 918-923)
    v
 [UNDERSTANDING LLM]  returns structured JSON  (goal/intent/category/memory_scope/
    |   memory_operation/canonical_fact/uncertain_terms/confidence_breakdown/entities)
    v
 [MEMORY ANALYZER]  analyze_memory()  (memory_analyzer.py: 13 deterministic Rules)
    |   Rules 1-6 wiring; Rule 7 structured recall; Rule 8 centroid recall;
    |   Rules 9-12 no-write suppression; Rule 13 imperative forget
    v
 [MEMORY DECISION]  process()  (memory_decision.py)
    |   is_uncertain() gate -> needs_clarification  <---- RC-01 (over-blocks)
    |   canonicalizer -> validator -> classifier -> evaluator -> conflict resolver
    |   forget path: _process_delete() (skips evaluator)
    v
 [MEMORY STORE]  store_fact/delete_fact  (memory_manager.py) + memory_history.json

 WRITE PATH above / READ PATH below:

 [READ]  reasoning_engine.reason()  (reasoning_engine.py)
    |   use_memory / use_episodes / use_context flags   <---- RC-03 (episodes miss)
    v
 [MEMORY ROUTER]  retrieve()  (memory_router.py)
    |   build_memory_query()  (memory_query_builder.py: profile/history/specific, CATEGORY_MAP)
    v
 [RETRIEVERS]  memory_retriever.py: retrieve_with_query() (keyword+category+semantic)
    |   retrieve_history() (changed-fact trail)   episode_retriever.py (episodes)
    v
 [RESPONSE GENERATOR]  (uncovered by stress suite)
```

---

## 3. Failure Distribution

| Category | Tests | Pass | Fail | Error | Pass rate | Dominant failure |
|---|---|---|---|---|---|---|
| A store | 1000 | 928 | 72 | 0 | 92.8% | `needs_clarification` (70) |
| B update (no ctx) | 400 | 293 | 107 | 0 | 73.2% | `needs_clarification` on update (107) |
| C forget | 400 | 165 | 235 | 0 | 41.2% | `needs_clarification` on forget (235) |
| D no-write | 1850 | 1845 | 5 | 0 | 99.7% | false `store` (5) |
| E episodic | 300 | 187 | 113 | 0 | 62.3% | `use_episodes=False` (113) |
| F context followup | 350 | 226 | 119 | 5 | 64.6% | stored OLD value (64), clarify (52), ignored (3), analyze fail (5) |
| G session-end | 300 | 279 | 20 | 1 | 93.0% | false `store` (19) |
| H history | 250 | 250 | 0 | 0 | 100.0% | — |
| R-sem | 60 | 41 | 19 | 0 | 68.3% | value not retrieved (19, cause split unknown) |
| R-pro | 30 | 22 | 8 | 0 | 73.3% | fact not returned (8) |
| R-epi | 30 | 30 | 0 | 0 | 100.0% | — |
| R-hist | 30 | 11 | 19 | 0 | 36.7% | history empty (19) |

Total by status: **PASS 4277 (85.5%) · FAIL 717 (14.3%) · ERROR 6 (0.1%)**

By failure mechanism (re-grouped, not by category):
- `needs_clarification` gate: **466** (A 72 + B 107 + C 235 + F 52)
- Context-value leak / ignored / analyze-fail: **72** (F)
- Episodic not routed: **113** (E)
- Retrieval misses (conflated, see RC-04): **46** (R-sem 19 + R-pro 8 + R-hist 19)
- Over-eager writes: **25** (G 20 + D 5)

---

## 4. Root Cause Analysis

### Root Cause #1 — The `is_uncertain()` gate over-blocks writes

**Evidence**
`needs_clarification` is returned for plain, complete statements:
- A: "my favorite drink is birch beer" → clarify (should store)
- B: "my favorite breakfast is burrito" → clarify (should update)
- C: "forget my favorite X" → clarify (should delete)
- F: "no wait, i prefer watermelon juice" → clarify (should update)

**Code responsible**
- `src/memory/memory_fact.py:94-104` — `is_uncertain()`: any entry in
  `uncertain_terms`, **or** `confidence < 0.5`, blocks the write.
- `src/memory/memory_decision.py:65-66` — the gate runs *before* the
  operation split, so it blocks `forget` even though the delete path
  (`_process_delete`, line 159) deliberately skips the durability evaluator
  and matches by subject machinery.
- `src/understanding/understanding_prompt.py:286-312` — the prompt already
  says "do NOT flag" for recognized-but-unusual terms; the 3B model still
  flags exactly the uncommon values the tests use (korean bbq, pho, tamale,
  birch beer, gyoza).

**Impact**
~466 tests (9.3% of the whole suite). Store/update/forget all become
unreliable for the most ordinary memory interactions. This is the single
largest loss.

**Recommended redesign**
Make the gate **operation-aware** and **confidence-component-aware**:
1. `forget`: do not require value confidence — only require that the delete
   target is a valid fact subject (validator already checks this). A misheard
   target is already protected by exact-subject matching, not by value
   confidence.
2. `store`/`update`: replace the raw `confidence < 0.5` check with the
   existing `gate_confidence()` (`memory_fact.py:136`) so only the stage that
   actually failed (e.g. STT) can block, instead of a single flattened number.
3. Distinguish "genuinely unparseable" (a real mishearing/typo) from
   "uncommon but recognized": a recognized value that round-trips through the
   canonicalizer (B.Tech → b tech normalization) should not block; only
   values the canonicalizer cannot recognize at all should.
4. Treat `uncertain_terms` as a **soft** signal for casual facts: lower
   confidence instead of hard-blocking, unless STT confidence is also low.

**Estimated improvement**
- C forget: 41.2% → ~90% (235 → ~40 residual).
- A store: 92.8% → ~97%. B update: 73.2% → ~90%. F clarify subset: −52 fails.
- Overall: roughly **+350–450 tests** (85.5% → ~93–95%).

**Regression risk**
Medium. Loosening the gate can admit misheard values. Mitigation: keep a hard
block when `stt_confidence < 0.5`; require canonicalizer recognition; add a
D-class regression suite (no-write must not fall below 99%).

---

### Root Cause #2 — Context value leak: follow-up updates store the OLD value

**Evidence** (verified, not a harness artifact)
- ctx "my favorite coffee is root beer" + "now my favorite coffee is mocha"
  → `op=update fact="My favorite coffee is root beer"` (#3952).
- ctx "…cafe au lait" + "…now flat white" → stored "cafe au lait" (#3953).
- ctx "…yerba mate" + "no wait, i prefer sangria" → stored "yerba mate" (#3954).
- 3 further followups → `ignored`; 5 → analyze returned nothing.

**Code responsible**
- `src/understanding/understanding_prompt.py:918-923` — the RECENT
  CONVERSATION block is correct ("never as new facts"), but it is a
  **non-enforced instruction**. The model extracts the attribute value from
  this block, not from the user message.
- `src/understanding/memory_analyzer.py:128-132` — `canonical_fact` from the
  LLM JSON is passed straight through. **Nothing ever verifies that the
  fact's value appears in the current user message.**
- `src/memory/memory_decision.py:65, 86, 138` — the fact is confident
  (`is_uncertain()` false), so it is committed as `updated`. No error signal.

**Impact**
~67 tests directly; more importantly this is the only failure that **corrupts
memory silently**. It compounds across turns and poisons future retrieval and
history.

**Recommended redesign**
Add a deterministic **value-origin guard** in the analyzer (rules layer, not
the LLM):
1. Tokenize the user message (reuse `_T()`-style tokenizer or
   `knowledge_normalizer`).
2. Extract the value from the proposed `canonical_fact` (the object of
   "is/now is").
3. If the value **does not occur in the user message** but **does occur in a
   recent-context turn**, downgrade the operation to `query`/`needs_confirmation`
   — never `update`.
4. Mirror this in the prompt: "The canonical_fact value MUST come from the
   User message section. If the value appears only in RECENT CONVERSATION,
   set memory_operation to null."

**Estimated improvement**
- F corruption 64 → ~0; ignored/analyze-fail subset largely resolved.
- F pass: 64.6% → ~82% (remaining fails stay in the RC-01 clarification class).

**Regression risk**
Low. The guard only rejects facts whose value never appears in the current
message — the safe direction. No legitimate update is affected.

---

### Root Cause #3 — Generic chat-recall queries are not routed to episodes

**Evidence**
- E: "anything from our chat about job interview", "remind me what we planned
  for research internship" → `use_episodes=False` (113/300).
- R-epi: "recap what we discussed about X" → `use_episodes=True` 30/30. The
  difference is phrasing.

**Code responsible**
- `src/understanding/memory_analyzer.py:342-368` (Rule 8) — centroid recall
  detection. A **non-question statement** requires `sim >= 0.70` plus a user
  pronoun. "anything from our chat about X" and "remind me what we planned
  for X" do not start with an interrogative and carry no "?", so they fall in
  the strictest bucket; their similarity to the recap centroids
  (`memory_analyzer.py:1-7`) is below 0.70.
- `src/core/reasoning_engine.py:101-105` — `use_episodes` reads
  `systems.episodes | category=="conversation" | goal in (summarize, recall)`;
  the LLM structured output missed these phrasings too.

**Impact**
113 tests. The recall feature (Phase 2.6/2.7 investment) is under-used for
the most natural phrasings; users get no past-session context.

**Recommended redesign**
1. Add dedicated centroids for the observed phrasings ("remind me what we
   planned for X", "anything from our chat about X", "did we talk about X
   before") and lower the statement threshold only for a *matched topic
   entity* (the phrasing + a concrete entity ≈ unambiguous recall intent).
2. Add a narrow structural backstop, consistent with existing rules:
   message starting with "remind"/"anything from our chat"/"what did we
   plan" + user pronoun → episodic, and (Rule 9 already) force operation to
   query with `canonical_fact=None`.
3. Keep the generic 0.70 statement threshold for unrelated statements to
   avoid misrouting.

**Estimated improvement**
- E: 62.3% → ~95% (recovering ~100 tests).

**Regression risk**
Low. The structural fallback requires a topic entity + user pronoun, and Rule 9
already prevents a recall turn from becoming a write.

---

### Root Cause #4 — Retrieval failures are conflated with store failures

**Evidence**
- R-sem: "my favorite salad is korean bbq" → query "what is my favorite salad"
  → `results=0`. The query builder maps category food → preference family
  (matches), keyword "favorite" matches, score ≥ 60 ≫ threshold 15
  (`memory_retriever.py:198-236`). **A stored fact should always surface.**
- R-hist: "my favorite seasoning is pho" → "…now curry" → "what was …
  before curry" → `hist=0`. History retrieval needs the update entry; if the
  update was rejected, history is empty by design.
- The failing values (korean bbq, butter chicken, tamale, pho, curry) are
  exactly the values RC-01's uncertainty gate rejects.

**Code responsible**
- `memory_retriever.py:113-249` / `memory_query_builder.py:167-353` — retrieval
  logic is not the obvious culprit; it self-checks above threshold.
- **Harness gap:** `random_stress.py:1049-1100` (`exec_R`) records only the
  query outcome (`results=0`), **not** whether the seed write persisted. The
  R categories therefore cannot distinguish "nothing stored" (RC-01) from
  "stored but not retrieved".

**Impact**
46 tests unclassified. This hides whether retrieval is healthy at all — the
single biggest blind spot in the current metrics.

**Recommended redesign**
1. Harness fix (FRIDAY-014): record `mf1.operation/status/present` alongside
   `results=`. Two lines, zero risk.
2. Re-run R-sem (60), R-pro (30), R-hist (30).
3. Only if pure-retrieval failures remain: lower the semantic floor
   (`memory_retriever.py:218`, currently sim > 0.5 / full weight at 0.7) or
   widen `CATEGORY_KEYWORDS` for the failing attributes.

**Estimated improvement**
Metrics become accurate (expected reclassification: most of the 46 → store-side
RC-01). No behavioural change yet.

**Regression risk**
None (harness-only).

---

### Root Cause #5 — Over-eager writes on session-end / conversational turns

**Evidence**
- G: session-end/dismissal messages produced `op=store` (19) and `op=update`
  (1); D: 5 conversational messages produced `op=store`. No-write class is
  otherwise 99.7%, so this is a narrow boundary leak.

**Code responsible**
- `src/understanding/memory_analyzer.py` Rules 8-12 suppress many no-write
  forms (declination, "you remember", history questions), but session-end /
  topic-dismissal messages that carry a canonical_fact and a confident
  classification are not universally suppressed; `memory_decision.process`
  then commits them.
- `src/understanding/end_session_analyzer.py` — the end-session signal is not
  plumbed back into the write gate.

**Impact**
~25 tests; memory pollution (stale/irrelevant facts) over time. Low severity,
real drift risk.

**Recommended redesign**
Mirror the existing suppression style: when `intent == end_session` or the
dismissal classifier fires, force `memory_operation = None` and drop the
canonical_fact (same pattern as Rules 9-12). Add the observed phrasings to the
dismissal detector.

**Estimated improvement**
- G: 93.0% → ~99%; D: 99.7% → ~99.9%.

**Regression risk**
Low–medium. The suppression must not capture genuine stores that merely end
with "okay, thanks" — the dismissal detector already gates this.

---

### Root Cause #6 (testing infra, FIXED) — Harness could not build/run a valid suite

Fixed 2026-08-05: no-replacement `sample()` + strict `commit()` dedup, `_T()`
re-tokenizer (quote-split), non-overlapping id ranges, larger pools,
per-5-test checkpointing. Verified 5000 specs / 6800 unique strings / 0 dups.
See `ISSUE_TRACKER.md` regression watchlist.

---

## 5. Architectural Weaknesses

1. **Trust in a small model's structured JSON.** The whole memory decision
   hinges on llama3.2:3b emitting correct `canonical_fact`/`uncertain_terms`/
   `confidence`. The deterministic layer only patches known misshapes
   (Rules 1-13); it has no *invariant* check that the emitted fact corresponds
   to the user's actual words. RC-02 is a direct symptom.
2. **Conflated confidence.** `MemoryFact` already carries per-stage
   confidence and `gate_confidence()` (`memory_fact.py:106-146`), but
   `is_uncertain()` ignores both and uses the flattened `confidence` +
   `uncertain_terms`. Rich signal exists and is unused.
3. **Compensating layers.** 936-line prompt + 580-line analyzer rulebook grow
   together; each LLM miss adds another deterministic patch. Maintainability
   and prompt-drift risk are high.
4. **Read/write coupling in the test design.** R categories test write+read
   as one unit, making retrieval health unmeasurable (RC-04).
5. **Magic thresholds everywhere.** 0.70 recall-statement, 0.55 recall-
   question, 0.5 semantic floor, 0.85 triage, `UNCERTAINTY_THRESHOLD = 0.5`.
   None are measured against data; several directly cause the failures above.
6. **No assertion on the response layer.** The suite validates memory
   operations but never what FRIDAY *says* — clarification dialogue,
   confirmation wording, and contradiction handling are uncovered.
7. **Conflict resolver is untested in isolation.** B updates exercise it
   indirectly (293 pass suggests it works), but no dedicated stress class.

## 6. Implementation Bugs

| # | Location | Bug | Effect | Fix |
|---|---|---|---|---|
| 1 | `memory_fact.py:94-104` | `is_uncertain()` gates `forget` | Legitimate deletes blocked (C 235) | Operation-aware gate (RC-01) |
| 2 | `memory_fact.py:104` | Uses flattened `confidence`, not `gate_confidence()` | Stage confidence can't be trusted; single low number blocks writes | Use per-stage breakdown |
| 3 | `memory_analyzer.py:131` | `canonical_fact` passed through unverified | Context value stored as new fact (RC-02) | Value-origin guard |
| 4 | `memory_analyzer.py:342-368` | Rule 8 statement threshold 0.70 too strict | Chat-recall statements missed (E 113) | Centroid/structural fallback (RC-03) |
| 5 | `memory_decision.py:65-66` | Gate runs before operation split | Forget/update both blocked by same predicate | Reorder: operation-aware gates |
| 6 | `understanding_prompt.py:901-913` | `[-4:]` context slice + non-enforced instruction | Model lifts value from context block | Slice to 2 user turns; enforce via guard |
| 7 | `random_stress.py:1049-1100` | R results omit write outcome | 46 retrieval fails unclassifiable (RC-04) | Log write status (FRIDAY-014) |

## 7. Technical Debt

- **Harness not in the repo.** Lives in `%TEMP%\opencode\`; no `tests/`
  directory exists in the repo, no CI. The 5000-test suite is not
  reproducible by anyone else and can be lost with the temp dir.
- **Mid-rewrite working tree.** 30+ uncommitted changes, deletions of legacy
  modules (`intent_detector.py`, `query_understanding.py`,
  `contracts/reasoning.py`, understanding_models/validator). Last commit:
  Phase 2.6. The Phase 2.7 rewrite is uncommitted.
- **Compensating layers** (see §5.3): prompt + rules grow together.
- **Dead/legacy code**: `retrieve_relevant_memories` (`memory_retriever.py:365`)
  kept "for compatibility", no callers in the stress path.
- **Unused capability**: `CONFIDENCE_SOURCES`/`gate_confidence`/per-stage
  breakdown wired into `MemoryFact` but not into the decision gate.
- **Overfit test templates**: "my favorite X is Y" templates test a narrow
  register; generalization to real conversational phrasing is unproven (see
  §Risks below).
- **Monolithic prompt file**: `understanding_prompt.py` (936 lines) mixes
  instructions, field definitions, and 25+ examples; hard to diff/tune.

## 8. Recommended Implementation Order

Ordered by (impact / risk / dependency):

1. **FRIDAY-014 — harness write-outcome logging** (RC-04 unblocker).
   Trivial, zero risk. Re-run R-sem/R-pro/R-hist → accurate retrieval metrics.
   *Do this before any retrieval tuning.*
2. **RC-02 — value-origin guard** (Critical). Analyzer-side invariant +
   prompt mirror. Low risk. Removes silent corruption.
3. **RC-01 — operation-aware uncertainty gate** (biggest volume).
   Start with the forget path (C, 235) — lowest risk and largest single
   category. Then store/update with per-stage confidence + canonicalizer
   recognition. Guard with the existing D no-write regression.
4. **RC-03 — episodic routing** (E, 113). New centroids + narrow structural
   fallback. Low risk.
5. **RC-05 — session-end suppression** (G/D, 25). Mirror Rules 9-12.
6. **Repo integration** — move harness into `tests/`, commit Phase 2.7,
   add focused regression suites for the D no-write and H history classes.

Each step is independently verifiable against the existing checkpoint format;
run the full 5000 after steps 2+3 to re-measure.

## 9. Expected Performance After Fixes

Projected from measured failure counts (not speculation):

| Category | Now | After 1-3 | After all |
|---|---|---|---|
| A store | 92.8% | ~97% | ~97% |
| B update | 73.2% | ~90% | ~90% |
| C forget | 41.2% | ~90% | ~90% |
| D no-write | 99.7% | 99.7% | ~99.9% |
| E episodic | 62.3% | 62.3% | ~95% |
| F context followup | 64.6% | ~82% | ~82% |
| G session-end | 93.0% | 93.0% | ~99% |
| H history | 100% | 100% | 100% |
| R-sem / R-pro / R-hist | 68/73/37% | *reclassified* | accurate; residual = real retrieval gaps |
| **TOTAL** | **85.5%** | **~93-95%** | **~95-97%** |

Corruption cases (RC-02): 64 → 0. Silent-write risk: eliminated by the origin
guard. No new latency: all fixes are deterministic rules or prompt text; the
value-origin guard is a tokenizer + `in` check.

Residual risks after fixes:
- Remaining fails concentrate in genuinely ambiguous inputs (correct
  clarification behavior).
- Real-conversation generalization is unproven; only the template register is
  measured. Recommend a follow-up pass with untemplated/natural phrasing.

---

## 10. Claude Implementation Prompt

> Paste the block below into a coding agent to implement the fixes in order.
> It is self-contained: files, invariants, verification, acceptance criteria.

```text
ROLE
You are fixing an AI assistant ("FRIDAY") memory pipeline based on a measured
stress test. DO NOT redesign broadly. Make minimal, verifiable changes in the
order below. The working directory is a Windows PowerShell project root.

CONTEXT (from a 5000-test run, seed 20260804)
- Overall 85.5% pass. Dominant failure: `needs_clarification` blocking
  store/update/forget (~466 tests). Critical: context-aware follow-up updates
  store the OLD value from recent context (~64 tests). Retrieval metric
  conflation in the test harness hides ~46 failures.
- Key files:
    src/memory/memory_fact.py            MemoryFact.is_uncertain() / gate_confidence()
    src/memory/memory_decision.py        process() gate order, _process_delete()
    src/understanding/understanding_prompt.py   SYSTEM_PROMPT + _format_recent_context()
    src/understanding/memory_analyzer.py Rules 1-13 (esp. Rule 8 recall, canonical_fact passthrough)
    src/understanding/understanding_orchestrator.py  analyze() entry point
    src/memory/memory_retriever.py       retrieve_with_query() / retrieve_history()
    src/memory/memory_query_builder.py   MemoryQuery / CATEGORY_MAP
    src/core/reasoning_engine.py         use_episodes gate
    src/understanding/end_session_analyzer.py
  The 5000-test harness is at %TEMP%\opencode\random_stress.py (checkpoint
  random_stress_ckpt.json, status helper ckpt_status.py). Run it with:
    python random_stress.py --max N   (resumes; safe to interrupt)
  Real data in src/memory/*.json is OFF-LIMITS. Never modify it. Run the
  harness; it redirects to a temp store.

TASK 1 — Harness write-outcome logging (do first; unblocks metrics)
In random_stress.py exec_R (R-sem/R-pro/R-hist branches), record the seed
write outcome in the result `actual` string: include mf1.operation, the
process_memory status, and whether the canonical text is present after write,
in addition to `results=...`. Re-run R-sem/R-pro/R-hist. Report the split of
failures into (a) seed write rejected vs (b) write ok but retrieval empty.
Acceptance: the re-run log lets you state the real retrieval failure count.

TASK 2 — Value-origin guard (Critical: silent corruption)
In memory_analyzer.analyze_memory, after canonical_fact is resolved and
BEFORE it is returned, verify the fact's value appears in the current user
message. Implementation notes:
  - Extract the value = the tail noun phrase after the last copula
    ("is"/"was") in canonical_fact.
  - Compare against tokens of the user message using the project's existing
    tokenizer/normalizer (knowledge_normalizer.normalize_fact is fine).
  - If the value does not occur in the user message: set memory_operation to
    None (or "query") and canonical_fact to None, so no write happens.
  - Add the same rule to SYSTEM_PROMPT text near the RECENT CONVERSATION
    block: "The canonical_fact value MUST come from the User message section.
    If it appears only in RECENT CONVERSATION, set memory_operation to null."
Acceptance: for ctx "my favorite coffee is root beer" + "now my favorite
coffee is mocha", FRIDAY must NOT produce canonical_fact "root beer"; it must
store mocha (or produce no write). Run F category and confirm 0
stored-old-value cases.

TASK 3 — Operation-aware uncertainty gate
Change MemoryDecision.process so the uncertainty check is operation-aware:
  - forget: do NOT block on value confidence/uncertain_terms. Keep only the
    canonicalizer + validator structural checks (a bad subject is rejected
    there). Rationale: delete matching uses exact subject machinery; value
    confidence is irrelevant to removing a fact.
  - store/update: replace `confidence < UNCERTAINTY_THRESHOLD` with
    gate_confidence() (per-stage), and treat uncertain_terms as a soft signal
    (lower confidence) unless stt_confidence < 0.5, in which case keep a hard
    block. A recognized value that round-trips through memory_canonicalizer
    (e.g. btech -> b tech) must never block.
Acceptance: C category forgets drop from 41% fails to <15%; A/B pass rates
rise; D no-write stays >=99%.

TASK 4 — Episodic recall routing for natural phrasings
In memory_analyzer Rule 8 and reasoning_engine.reason():
  - Add centroids for "remind me what we planned for X", "anything from our
    chat about X", "did we talk about X before".
  - Add a narrow structural fallback: user pronoun present AND message begins
    with "remind"/"anything from our chat"/"what did we plan" AND a concrete
    entity/topic token exists -> set memory_scope episodic (Rule 9 already
    forces operation to query and drops canonical_fact).
  - Keep the generic 0.70 statement threshold unchanged.
Acceptance: E category use_episodes=True rate rises toward 90%+ without
misrouting ordinary statements (verify no new store failures in A).

TASK 5 — Session-end/dismissal write suppression
In memory_analyzer, when intent == end_session OR the dismissal classifier in
end_session_analyzer.py fires, force memory_operation=None and drop
canonical_fact (mirror the existing declination rule). Add the observed
phrasings from the G category failures to the dismissal detector.
Acceptance: G false stores drop to <5; D no-write stays >=99%.

VERIFY
After Tasks 2+3, run the full 5000 (or resume):
    python random_stress.py --max 5000
Confirm the checkpoint summary improves as projected (overall >=93%) and that
the docs report regenerates. Do NOT edit src/memory/*.json or the report docs.
Return: per-task diff summary, before/after pass counts per category, and any
new regression introduced.

CONSTRAINTS
- No broad refactors. Change only what a task requires.
- Keep the existing code style: docstrings, module-level singleton pattern,
  no comments explaining "what" (explain "why").
- All message parsing must stay in the deterministic rule layer, not new
  keyword logic in the LLM prompt — except where a task explicitly says
  "add to SYSTEM_PROMPT".
```

---

## Appendix — Data provenance
- Stress data: `docs/RANDOM_STRESS_TEST.md`, checkpoint
  `%TEMP%\opencode\random_stress_ckpt.json`, seed 20260804.
- Issue registry: `docs/ISSUE_TRACKER.md` (FRIDAY-001…014 ↔ root causes
  RC-01…RC-06 above).
- Historic known issues: `docs/KNOWN_ISSUE/`, `docs/DEFFERED_IMPROVEMENT/`.
