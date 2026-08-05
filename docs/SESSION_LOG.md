# Session Log

## Session: Brain Architecture Foundation

Date:
2026-07-28

---

## Major Achievements

### Speech System

- Verified CUDA acceleration on RTX 4050
- Confirmed Whisper Small running on GPU
- Confirmed WebRTC Voice Activity Detection pipeline
- Improved overall speech responsiveness

---

### Memory System

- Improved automatic memory evaluation
- Improved preference detection
- Added importance-based memory storage
- Verified long-term memory persistence
- Verified memory recall through voice
- Fixed automatic memory storage issues

---

### Context System

- Implemented short-term conversation memory
- Created Context Manager
- Created Context Reasoner
- Added keyword-based conversation lookup
- Connected context with the Brain layer

---

### Brain Layer

This session introduced Friday's first true Brain layer.

The Brain now:

- Receives every processed user message
- Retrieves recent conversation context
- Searches long-term memories
- Decides whether memory or command handling should answer
- Routes responses through a dedicated response generator

This separates reasoning from command execution and prepares Friday for future LLM integration.

---

### Response Generation

Implemented the first version of a response generator.

Current abilities:

- Converts memory objects into readable English
- Prevents raw JSON from being spoken
- Produces cleaner voice responses

Example:

Before

Friday:
[
{"text":"my favorite game is sekiro"}
]

After

Friday:
"You told me: my favorite game is sekiro."

---

## Observations

Compared to previous sessions:

- Friday is no longer just a command-response assistant.
- Memory, context, and commands now work through a centralized Brain.
- The overall architecture is significantly more modular.
- Future intelligence can now be added without rewriting the entire assistant.

---

## Known Issues (Deferred)

The following issues were intentionally deferred to later phases because they do not block LLM integration:

### Response Formatting

- Responses are still somewhat robotic.
- Greeting responses sometimes fail because punctuation affects intent detection.
- Formatting is functional but not conversational.

### Context Reasoning

- Uses keyword matching only.
- Cannot understand semantic similarity.
- Cannot merge multiple memories into one answer.

### Memory

- Importance scoring is rule-based.
- Automatic remembering still uses simple heuristics.

### Speech

- Whisper occasionally mishears words.
- Neural TTS has not yet been integrated.

---

## Next Session

Planned order:

1. Improve response formatting.
2. Finalize Brain output structure.
3. Begin LLM integration.
4. Replace deterministic reasoning with AI-assisted reasoning.

No additional features will be introduced before LLM integration unless they directly support this roadmap.

---

## Milestone Reached

This session marks the transition from:

Command-Based Voice Assistant

↓

Brain-Centered AI Architecture

This is one of the most significant milestones completed so far in Project Friday.

---

## Session: History Recall & END_SESSION

Date:
2026-08-04

---

## Major Achievements

### History "Before" Answers

- Fixed "what was my favorite food before X" recall. Answers are now
  deterministic and model-free: the literal value after "before" is
  extracted from the raw message, matched against the OLD side of the
  change entries in memory history, and the found value is injected
  into the prompt as a FINAL NOTE. Verified 2/2 across chicken curry
  (rice), lasagna (honest no-record), Sekiro (Ghost of Tsushima), and
  the ramen/Priya compound question.
- History entries are deduplicated and scored so the most recent
  change wins even when a reverse change entry exists.

### Canonical END_SESSION

- Sleep/shutdown is now a conversation-intent problem, not a keyword
  list. The Understanding Layer runs a focused micro-classifier that
  labels natural-language session ends ("you can sleep now", "i am
  done for today", ...) into a canonical metadata flag. The
  ExecutionManager maps that flag to the runtime: the voice loop
  rolls the working buffer into an episode and stops listening.
- The flag is conservative by construction — only an exact
  'end_session' label is accepted, so ordinary messages can never
  randomly stop the session. Verified: all session-end phrases set
  the flag; "dismiss this topic", "see you later", jokes and time
  questions do not.
- Response honesty: the response LLM is told when a session is ending
  so it gives a natural farewell, and a base rule forbids claiming to
  shut down, sleep, or recharge unless the runtime is actually doing
  so. The legacy "shut down"/"exit" commands still work.

---

## Observations

- The small model (llama3.2:3b) cannot follow an intent taxonomy
  embedded in the large understanding prompt; a dedicated ~0.55s
  micro-prompt is reliable where the full prompt fails.
- History before-answers are best resolved deterministically in the
  prompt builder rather than by asking the model to reason across
  history entries.

---

## Verification

- Smoke pipeline: 23/24 — the only residual failure is the known
  `forget` store/delete mislabel by the LLM (no keyword fallback by
  design).
- Delete pipeline: 15/15 PASS.

---

## Session addendum: write-protection rules (stress test fixes)

- Rule 11 — "you remember/know/recall X" is a question to FRIDAY,
  never a store. Second-person address + knowledge-state verb forces
  a query and drops the canonical fact ("you remember my favorite
  food is sushi" no longer overwrites the stored lasagna value).
  The fact-drop form "did you know X" still stores.
- Rule 12 — declining an offer is never a memory write. "you don't
  have to write it again" / "no need to X" forces the operation off
  and drops the fact (the LLM was emitting garbage canonical facts
  like "I don't need to write it again"). First-person subjects
  ("I don't have to work tomorrow") stay stores.
- Profile classifier — "tell me about" / "what do you know" /
  "everything about" only mean a profile question when their object
  is the user ("tell me about yourself"); "can you tell me about
  it" (a GPU question) no longer triggers the profile dump.

---

## Session addendum: pipeline hardening (final stress pass)

- END_SESSION classifier was rewritten as a YES/NO boolean
  micro-classifier with terse-standalone-shutdown framing. Only an
  exact "yes" label is accepted (`detect_end_session` returns
  `label == "yes"`), so false negatives are safe and false positives
  are impossible by construction. All 20 END_SESSION phrasings are
  caught; every memory command ("forget my favorite food", "delete
  the ramen memory", ...), topic follow-ups, and auto-store phrases
  return False.
- Recall-store fix: `is_question_turn` now flags trailing tag
  questions (`raw_text.rstrip().endswith((" right", " right?"))`),
  so "we were working on the c program, right" is treated as a
  recall turn and never stored.
- Delete-matching fix: the category gate in
  `memory_conflict_resolver.check_conflict` was asymmetric — it
  exempted only a "general" NEW fact, so an exact-text delete target
  that the LLM re-classified specifically (e.g. store side None ->
  "general", delete side "food" -> "preference") was skipped and
  `delete_fact` returned `not_found`. The gate now skips only when
  BOTH sides carry specific, different categories; a "general"
  stored record can no longer block an exact-text match. Applied to
  the whole matching loop (stores/updates/deletes alike), verified
  with the lasagna store -> forget round trip and a general-to-food
  update.
- Universal-only: no command names, keywords, or per-case rules were
  introduced.

## Verification (final)

- Stress suite (temp-store harness, truthy `no_write()`):
  END_SESSION 20/20, TOPIC_DISMISSAL 20/20, REMOVAL 15/15,
  QUERY/RECALL/HISTORY 18/18, DECLINE 7/7, YOU_REMEMBER 5/5,
  PROFILE 4/4, WORLD 5/5, STORE 20/20, DEVICE FIDELITY 8/8,
  FULL WRITE PATH clean, CASUAL AUTO-STORE 5/6, MULTI-TURN CONTEXT
  clean — TOTAL CHECKS 5, FAILURES 0.
- Smoke pipeline: 24/24 PASS.
- Delete pipeline: 15/15 PASS.
- Real data files verified untouched by the test runs (all suites
  write to temp dirs; smoke reads only).