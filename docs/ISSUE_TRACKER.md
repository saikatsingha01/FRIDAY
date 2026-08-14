# FRIDAY Issue Tracker

Single source of truth for known issues in FRIDAY. Updated after every major
validation run. Latest data source: `docs/RANDOM_STRESS_TEST.md` (5000-test
randomized stress run, seed 20260804, 2026-08-05).

---

## Executive Summary

### Overall stability
- **5000/5000 tests completed: PASS 4277 (85.5%), FAIL 717 (14.3%), ERROR 6 (0.1%)**.
- Solid subsystems: **no-write decisioning (D 99.7%)**, **history tracking
  (H 100%)**, **episodic retrieval when explicitly routed (R-epi 100%)**.
- The biggest single loss is **clarification over-triggering** (~466 tests):
  FRIDAY asks "which do you mean?" instead of storing / updating / forgetting
  plain, unambiguous statements.
- One **silent data-corruption bug** found: context-aware updates can store the
  OLD value from the recent-conversation block as if it were the new fact.

### Major weak subsystems
| Subsystem | Evidence | Status |
|---|---|---|
| Forget decisioning | C 41.2% (235/400 `needs_clarification`) | Weak — clarification gate blocks forgets |
| Context tracking / updates | F 64.6% + 5 errors (119 fails) | Weak — old-value leak + clarification |
| Episodic recall routing | E 62.3% (113/300 not routed) | Weak — generic "chat about X" missed |
| Semantic / profile / history retrieval | R-sem 68.3%, R-pro 73.3%, R-hist 36.7% | Weak-to-ok |
| Casual store decisioning | A 92.8% | Ok, with 70 clarification over-triggers |

### Recently fixed issues
- Stress-harness spec generator hang (could not build 5000 specs; LOOP_CAP).
- Tokenizer quote-split bug (`'fried rice'` → `'fried` / `rice'`).
- Spec id-range overlap (D 13000 / E 14000 silently overwrote 300 specs).
- Pool exhaustion (DRINK 56→86 entries; category-prefix headroom).
- Historic phase fixes tracked in `docs/KNOWN_ISSUE/` (e.g. KI-004 education
  category/query mapping).

### Highest priority engineering tasks
1. **Fix context value leak (FRIDAY-004)** — only Critical issue; silently
   stores wrong data.
2. **Record write outcome in R-sem/R-pro harness (FRIDAY-014)** — separates
   store-decision failures from retrieval failures; unlocks accurate RC-04.
3. **Tune clarification gate (RC-01)** — biggest volume (~466 tests).
4. **Route generic chat-recall queries to episodes (FRIDAY-008)**.

---

# Issue Categories

| Category | Open issues | Notes |
|---|---|---|
| Memory Storage | FRIDAY-001, 012, 013 | Clarification over-trigger; session-end false writes; no-write leak |
| Memory Retrieval | FRIDAY-009, 010, 011 | Semantic/profile/history low recall |
| Forget Decisioning | FRIDAY-003 | Clarification gate blocks forgets (235) |
| Conflict Resolution | — | No dedicated coverage; exercised indirectly via B updates |
| Context Tracking | FRIDAY-004, 005, 006, 007 | Old-value leak; clarification; ignored; analyze failure |
| Conversation Flow | FRIDAY-013 | No-write leak on conversational messages |
| Intent Detection | FRIDAY-008 | Chat-recall intent not routed to episodes |
| Personality | — | No coverage |
| Voice Pipeline | — | No coverage (see KI-02 STT accuracy) |
| Planning | — | No coverage |
| Reasoning | FRIDAY-008 (routing) | Only boolean use_memory/use_episodes covered |
| Response Generation | FRIDAY-015 (KI-013) | Grounding guard rejects valid temp claims due to quote-degree symbols |
| Performance | — | Serial LLM write phase is the test-run bottleneck |
| Testing Infrastructure | FRIDAY-014 | Harness lives in %TEMP%; no write-outcome logging in R tests |
| Other | — | Repo has large uncommitted working tree |

---

# Root Cause Analysis

Root causes are grouped by shared mechanism, not by category. Each is followed
by the individual issues it explains.

## Root Cause 1 — Clarification over-triggering

**Title:** The understanding LLM requests clarification on unambiguous casual
statements instead of acting.

**Description:** For plain statements like "my favorite drink is birch beer",
value-change followups like "my favorite breakfast is burrito", and forget
requests, FRIDAY responds `op=needs_clarification` even though no ambiguity
exists. The model is a 3B-parameter LLM (llama3.2:3b) and the understanding
prompt's clarification path fires too readily.

**Why it happens:** Likely over-emphasis on clarification in the understanding
prompt combined with a low-confidence model that cannot reliably distinguish a
complete statement from a genuinely ambiguous one. The same prompt block that
should classify these as store/update/forget instead selects the clarification
escape hatch.

**Subsystems affected:** Memory storage (store), update, forget decisioning;
understanding orchestration.

**Severity:** High (volume; degrades UX but does not corrupt data).

**Estimated affected tests:** ~466 (A 72, B 107, C 235, F 52).

**Affected issues:** FRIDAY-001, FRIDAY-002, FRIDAY-003, FRIDAY-005.

**Suggested solution:** Rework the understanding prompt to reserve
`needs_clarification` for genuinely ambiguous inputs (missing value, multiple
interpretations) and add a confidence/pattern fallback so the canonical
`"my favorite X is Y"` / `"now my favorite X is Y"` / `"forget my favorite X"`
shapes are classified deterministically without an LLM clarification decision.

**Implementation complexity:** Medium.

**Regression risk:** Medium — tightening clarification could cause false
"stored" on genuinely ambiguous messages; needs the D (no-write) class as a
guard.

**Current status:** Open.

## Root Cause 2 — Context value leak in follow-up updates

**Title:** Context-aware updates store the prior value from the recent
conversation instead of the new value in the user message.

**Description:** With ctx `"my favorite coffee is root beer"` + followup
`"now my favorite coffee is mocha"`, FRIDAY returns
`op=update canonical_fact="My favorite coffee is root beer"` — it updates the
fact *to the old value*, silently corrupting memory. Verified across 4 examples
(#3952–#3955); 3 further followups were `ignored`, and 5 produced no analysis.

**Why it happens:** The recent-conversation block is explicitly framed as
"context only — never as new facts" (`understanding_prompt.py:919-923`), but
the model extracts the attribute value from that block rather than from the
user message. Because the op is `update`, the wrong value is committed with no
signal that anything is wrong — the most dangerous failure in the suite.

**Subsystems affected:** Context-aware update, memory storage, memory history.

**Severity:** Critical (silent data corruption; compounds over time).

**Estimated affected tests:** ~72 (F: 64 stored-old + 3 ignored + 5 errors).

**Affected issues:** FRIDAY-004, FRIDAY-006, FRIDAY-007.

**Suggested solution:** Strengthen the prompt instruction and post-process in
the analyzer: extract candidate values from the **user message** only, and if
the produced fact's value matches a recent-context value but not any token in
the user message, re-route to the clarification path instead of storing.

**Implementation complexity:** Low–medium (prompt + analyzer guard).

**Regression risk:** Low — the guard only rejects facts whose value never
appears in the current message, which is the safe direction.

**Current status:** Open.

## Root Cause 3 — Generic chat-recall queries not routed to episodes

**Title:** "anything from our chat about X" / "remind me what we planned for X"
queries are not flagged for episodic recall.

**Description:** 113/300 episodic-category tests produced `use_episodes=False`.
Explicitly episodic phrasing passes (R-epi 100%), so the routing logic
(reasoning gate) recognizes only a narrow set of phrasings and misses common
variants like "anything from our chat about job interview".

**Why it happens:** The reasoning gate uses keyword/pattern matching that
covers a fixed set of episodic expressions; "anything from our chat about…"
and "remind me what we planned for…" fall through to the semantic path.

**Subsystems affected:** Reasoning gate, episode retrieval routing.

**Severity:** High (feature under-utilization; memory feels empty).

**Estimated affected tests:** ~113.

**Affected issues:** FRIDAY-008.

**Suggested solution:** Extend the gate with the observed phrasings and add a
semantic fallback (recall intent via LLM) when a query is recall-like but no
keyword matched.

**Implementation complexity:** Low–medium.

**Regression risk:** Low.

**Current status:** Open.

## Root Cause 4 — Low-recall retrieval for attribute/profile/history queries

**Title:** Stored facts are not retrieved for queries about the same attribute.

**Description:** After storing "my favorite salad is korean bbq" in an isolated
store, a query about the favorite salad returns 0 results; identity facts
("my name is sunny") and history before-questions also return nothing.
R-hist is the weakest class at 36.7%.

**Why it happens:** Undetermined with current data — R-sem/R-pro failures may
share RC-01 (the store never persisted because of clarification) or be genuine
retrieval low-recall (query builder drops the attribute term, embedding
threshold too strict). The harness does not record the write outcome, so the
split is unknown (see FRIDAY-014).

**Subsystems affected:** Memory retrieval, query builder, history retriever.

**Severity:** Medium–high (core feature: stored facts are useless if not
retrievable).

**Estimated affected tests:** ~46 (R-sem 19, R-pro 8, R-hist 19), some
overlapping RC-01.

**Affected issues:** FRIDAY-009, FRIDAY-010, FRIDAY-011.

**Suggested solution:** First fix FRIDAY-014 to split store vs retrieve
failures, then tune query building / retrieval threshold for attribute and
identity facts.

**Implementation complexity:** Medium.

**Regression risk:** Medium.

**Current status:** Open (partially unclassified).

## Root Cause 5 — Over-eager writes on non-factual statements

**Title:** Conversational and session-end/dismissal messages are stored as
facts.

**Description:** 19 session-end/dismissal messages produced `op=store` and 1
produced `op=update` (G); 5 conversational no-write messages produced
`op=store` (D). The no-write decision boundary is otherwise very good
(D 99.7%), so these are edge leaks at the boundary rather than a systemic
problem.

**Why it happens:** The no-write classifier is tuned to be permissive (prefer
to store), and certain dismissals ("nevermind", "forget it", wrapping-up
statements) contain enough fact-like phrasing to pass.

**Subsystems affected:** Memory decisioning (no-write), end-session analyzer.

**Severity:** Medium (memory pollution risk; not corruption).

**Estimated affected tests:** ~25.

**Affected issues:** FRIDAY-012, FRIDAY-013.

**Suggested solution:** Extend the end-session/dismissal classifier with the
observed phrasings; tighten the store branch to require a concrete value.

**Implementation complexity:** Low.

**Regression risk:** Low–medium (must not break the 99.7% no-write class).

**Current status:** Open.

## Root Cause 6 (testing infra, FIXED) — Harness could not build a valid spec set

**Title:** Spec generation hung / produced broken or overlapping specs.

**Description:** The original generator failed at ~94% utilization
("could not generate B specs (262)" after 30000 attempts), silently lost 300
specs to an id-range overlap, and mangled quoted pool values.

**Why it happened:** (a) partial-consume uniqueness leak — a value consumed by
a failed retry stayed consumed; (b) `.split(" ")` tokenizer split `'fried rice'`
into `'fried` and `rice'`; (c) fixed id ranges overlapped; (d) pools sized with
insufficient headroom for 2-unique-strings-per-test.

**Subsystems affected:** Testing infrastructure only.

**Severity:** N/A (fixed).

**Estimated affected tests:** 0 now (was the entire suite).

**Affected issues:** none open.

**Suggested solution (applied):** no-replacement `sample()` with strict
`commit()` duplicate detection, re-tokenizer `_T()`, non-overlapping id ranges,
larger pools, per-5-test checkpointing.

**Implementation complexity:** Medium (done).

**Regression risk:** Low.

**Current status:** **FIXED 2026-08-05**, verified 5000/6800 unique, 0 dups.

---

# Detailed Issue List

| ID | Title | Root cause | Sev | Pri | Subsystem | Files | Repro (stress id) | Expected | Actual | Suggested fix | Fix risk | Status | Discovered |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FRIDAY-001 | Plain casual fact flagged needs_clarification | RC-01 | High | 2 | Memory Storage | `understanding_prompt.py`, `memory_decision.py` | A: "my favorite drink is birch beer" | op=store present | op=store `needs_clarification`, not persisted (70 + 2 confirmation) | Prompt rework; deterministic store for `my favorite X is Y` | Medium | Open | 2026-08-05 |
| FRIDAY-002 | Value-change followup asks clarification | RC-01 | High | 2 | Memory Storage (update) | `understanding_prompt.py`, `memory_decision.py` | B: "my favorite breakfast is burrito" (after seed) | op=update, old replaced | op=update `needs_clarification` (107) | Same as FRIDAY-001 for `now/actually my favorite X is Y` | Medium | Open | 2026-08-05 |
| FRIDAY-003 | Forget requests gated by clarification | RC-01 | High | 2 | Forget Decisioning | `memory_decision.py` | C: forget "my favorite X" | forget applied | `needs_clarification` (235) | Deterministic forget for explicit "forget my favorite X"; distinguish from real ambiguity | Medium | Open | 2026-08-05 |
| FRIDAY-004 | Context update stores OLD value from recent conversation | RC-02 | **Critical** | 1 | Context Tracking / Storage | `understanding_prompt.py`, `understanding_orchestrator.py`, `memory_analyzer.py` | F: ctx "coffee is root beer", msg "now… mocha" | update to mocha | `op=update` fact="…root beer" (64) | Prompt: value must come from user message; analyzer guard: reject fact whose value not in message | Low | Open | 2026-08-05 |
| FRIDAY-005 | Context followup asks clarification instead of updating | RC-01 | High | 2 | Context Tracking | `understanding_prompt.py` | F: "no wait, i prefer watermelon juice…" | op=update | `needs_clarification` (52) | Same as FRIDAY-002 with ctx | Medium | Open | 2026-08-05 |
| FRIDAY-006 | Context followup ignored (no write) | RC-02 | Medium | 3 | Context Tracking | `understanding_prompt.py` | F: "no wait, i prefer…" | op=update | op=ignored (3) | Analyzer guard / prompt emphasis | Low | Open | 2026-08-05 |
| FRIDAY-007 | Context followup produces no analysis (ERROR) | RC-02 | Medium | 3 | Context Tracking | `understanding_orchestrator.py` | F: "no wait, i prefer cider…" | op=update | analyze returned None (5 ERROR) | Hardening; retry / fallback to clarification | Low | Open | 2026-08-05 |
| FRIDAY-008 | Generic chat-recall query not routed to episodes | RC-03 | High | 3 | Intent Detection / Reasoning | `reasoning_engine.py` | E: "anything from our chat about job interview" | use_episodes=True | use_episodes=False (113) | Extend gate with observed phrasings + semantic fallback | Low | Open | 2026-08-05 |
| FRIDAY-009 | Stored semantic fact not retrieved | RC-04 | Medium | 3 | Memory Retrieval | `memory_retriever.py`, `memory_query_builder.py` | R-sem: salad="korean bbq" then query | results contain value | results=0 (19) | Split store-vs-retrieve first (FRIDAY-014); tune query/threshold | Medium | Open | 2026-08-05 |
| FRIDAY-010 | Identity/profile fact not retrieved | RC-04 | Medium | 3 | Memory Retrieval | `memory_retriever.py`, `memory_classifier.py` | R-pro: "my name is sunny" | query returns fact | results=0 (8) | Same as FRIDAY-009 | Medium | Open | 2026-08-05 |
| FRIDAY-011 | History before-question returns no entry | RC-04 | Medium | 3 | Memory Retrieval | history retriever, `memory_router.py` | R-hist: seasoning="pho" | history contains old | hist=0 (19) | Same as FRIDAY-009 | Medium | Open | 2026-08-05 |
| FRIDAY-012 | Session-end/dismissal message stored as fact | RC-05 | Medium | 3 | Memory Storage | end-session analyzer, `memory_decision.py` | G: dismissal/session-end | no write | op=store (19) / op=update (1) | Extend dismissal classifier with observed phrasings | Low–med | Open | 2026-08-05 |
| FRIDAY-013 | Conversational no-write message occasionally stored | RC-05 | Medium | 3 | Conversation Flow | `memory_decision.py` | D: conversational msg | no write | op=store (5) | Tighten store branch: require concrete value | Low–med | Open | 2026-08-05 |
| FRIDAY-014 | R-sem/R-pro harness does not log write outcome | — | High | 2 | Testing Infrastructure | `random_stress.py` (exec_R block) | any R-sem/R-pro | write result recorded | results=0 only | Record mf1 op/present in `actual`; re-run R (60+30) | Low | Open | 2026-08-05 |
| FRIDAY-015 | Grounding guard rejects valid temp claims (quote-degree symbols) | KI-013 | Medium | 3 | Response Generation | `response_generator.py` | "weather in siliguri" | Correct weather answer | "no verified weather info" | Expand `_TEMP_RE` to accept quote-degree symbols | Low | Fixed 2026-08-15 | 2026-08-15 |

*Severity: Critical > High > Medium > Low > Cosmetic. Priority: 1 = next, 2 = soon, 3 = later.*

---

# Priority Roadmap

## Critical
- **FRIDAY-004** — Context update stores old value (silent data corruption). Must fix before next milestone.

## High
- **FRIDAY-001 / FRIDAY-002 / FRIDAY-003** — Clarification over-triggering across store/update/forget (~466 tests).
- **FRIDAY-014** — R-sem/R-pro write-outcome logging (unblocks accurate RC-04).
- **FRIDAY-005** — Context followup clarification.
- **FRIDAY-008** — Generic chat-recall not routed to episodes.

## Medium
- **FRIDAY-009 / FRIDAY-010 / FRIDAY-011** — Retrieval low-recall.
- **FRIDAY-012 / FRIDAY-013** — Over-eager writes.
- **FRIDAY-015** — Grounding guard rejects valid temp claims (quote-degree symbols) — **Fixed 2026-08-15**.

## Low
- **FRIDAY-006** — Context followup ignored.
- **FRIDAY-007** — Context followup analyze failure (rare; keep under FRIDAY-004 fix umbrella).

## Cosmetic
- None filed. (Candidate: report/tracker maintenance automation once harness is in-repo.)

---

# Regression Watchlist

| Bug | Date fixed | Tests protecting against regression | Regression status |
|---|---|---|---|
| Harness spec-generation hang (LOOP_CAP) | 2026-08-05 | Generator self-check: 5000 specs, 6800 unique strings, 0 dups, 0 v1==v2 (0.03s) | Guarded |
| Tokenizer quote-split (`'fried rice'` → `'fried`/`rice'`) | 2026-08-05 | `_T()` re-tokenizer applied to all string pools; verified 6800 unique | Guarded |
| Spec id-range overlap (D 13000 / E 14000) | 2026-08-05 | Non-overlapping ranges A=10000…R=16300; total 5000 confirmed | Guarded |
| Pool exhaustion under 2-unique-strings load | 2026-08-05 | Pool headroom + DRINK expanded to 86; generation completes 0.03s | Guarded |
| Education fact categorized as `device`; query fell back to `preference` (KI-004) | 2026-08-03 | KI-004 verification suite (lasagna store→forget round trip; general-to-food update) | Guarded (in SESSION_LOG) |
| Grounding guard rejects valid temp claims — quote-degree symbols (KI-013) | 2026-08-15 | Weather query test; `_TEMP_RE` matches quote-degree symbols | Guarded |

---

# Test Coverage

| Subsystem | Coverage | Evidence |
|---|---|---|
| No-write decisioning | **Excellent** | D 1850 tests, 99.7% |
| History tracking (write/update entries) | **Excellent** | H 250 tests, 100% |
| Episodic retrieval (explicit phrasing) | **Excellent** | R-epi 30 tests, 100% |
| Casual store decisioning | **Good** | A 1000 tests, 92.8% |
| Update decisioning (no context) | Good | B 400 tests, 73.2% |
| Semantic retrieval | Limited | R-sem 60 tests, 68.3% (partly unclassified) |
| Context tracking / follow-up updates | Limited | F 350 tests, 64.6% (fails dominate) |
| Forget decisioning | Limited | C 400 tests, 41.2% (covered but failing) |
| Episodic recall routing (generic phrasings) | Limited | E 300 tests, 62.3% |
| Profile / identity retrieval | Limited | R-pro 30 tests, 73.3% |
| History retrieval | Limited | R-hist 30 tests, 36.7% |
| Conflict resolution | Indirect only | Exercised via B updates; no dedicated category |
| Personality | **No coverage** | — |
| Voice pipeline | **No coverage** | — |
| Planning | **No coverage** | — |
| Response generation | **No coverage** | — |
| Intent detection | Limited | Only via E/F recall & followup classes |
| Reasoning quality | Limited | Only boolean use_memory/use_episodes asserted |

---

# Risk Assessment

- **Silent data corruption (RC-02):** The highest-risk item. Facts are
  overwritten with the wrong value while reporting `status=updated`, so there
  is no error signal. Compounds across turns; poisons retrieval and history.
- **Memory pollution:** Forget failures (RC-01/C) leave stale facts; over-eager
  writes (RC-05) add noise; RC-02 corrupts values. Together these degrade the
  store over time.
- **Classifier ambiguity:** Episodic ("chat about X") vs semantic recall
  (E routing); identity/profile category for R-pro. Boundary is phrasing-based
  and narrow.
- **Rule conflicts:** The prompt explicitly forbids storing RECENT CONVERSATION
  as new facts, yet RC-02 does exactly that — instruction vs model behavior
  conflict, not a missing instruction.
- **Overfitting to tests:** All messages use canned templates
  ("my favorite X is Y", "no wait, i prefer Y", "now my favorite X is Y").
  85.5% is an upper bound for this template distribution; real-world phrasing
  varies and may fare worse (or better, with more context). The F ctx pattern
  also made context-update quality *easier* to test in isolation than in real
  mixed conversation.
- **Hidden regressions:** R-sem/R-pro failures are unclassified (store vs
  retrieve), so retrieval health is currently unknowable (FRIDAY-014).
- **Performance bottleneck:** The harness write phase is serial and LLM-bound
  (~50s/spec for E; F/H slower), making large runs many-hours. Runtime impact
  on FRIDAY itself is not measured (no end-to-end latency coverage).
- **Technical debt / repo hygiene:** Harness lives in `%TEMP%\opencode` (not in
  the repo) — not reproducible by others and at risk of loss. Working tree has
  large uncommitted changes (30+ files, incl. deletions of legacy modules).
  Recommend moving the harness into the repo under a `tests/` or `tools/` dir.

---

# Recommended Next Work

Prioritized by impact, risk, complexity, and measured test impact. Only items
supported by the 2026-08-05 run.

1. **Fix FRIDAY-004 (context value leak).** Impact: removes silent data
   corruption (~72 F tests). Risk: Low (analyzer guard only rejects facts whose
   value never appears in the user message). Complexity: Low–medium. Expected
   improvement: F pass rate toward B's 73%+, and a safe invariant for the whole
   update path.
2. **Add FRIDAY-014 write-outcome logging and re-run R-sem/R-pro.** Impact:
   reclassifies ~27 R failures into store-decision vs retrieval, making RC-04
   actionable. Risk: None (harness-only). Complexity: Trivial (~2 lines).
   Expected improvement: accurate retrieval metrics.
3. **Tune the clarification gate (RC-01).** Impact: ~466 tests, the largest
   single loss. Risk: Medium (must not break D no-write / 99.7%). Complexity:
   Medium (prompt + deterministic pattern fallback for canonical templates).
   Expected improvement: A/B/C/F pass rates rise together; run a focused
   clarify-vs-act classifier eval first.
4. **Extend episodic routing (FRIDAY-008).** Impact: 113 E tests, recall
   feature under-utilization. Risk: Low. Complexity: Low–medium.
   Expected improvement: E toward R-epi-level routing.
5. **Move harness into the repo + add C/H/R-epi-style regression suites.**
   Impact: reproducibility and regression protection for everything above.
   Risk: None. Complexity: Low. Do alongside item 2.

**Not recommended yet:** semantic retrieval threshold tuning (blocked by
FRIDAY-014), response/personality work (no coverage), and planning changes
(no coverage). Do not tune blind.
