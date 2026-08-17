# FRIDAY — Engineering Master Handoff

This document is the permanent, detailed engineering handoff for the FRIDAY
project. Its purpose is to let any future AI agent (or engineer) continue
development without rewriting or breaking the architecture. Everything here
was reconstructed from actual repository inspection on 2026-08-09 and
refreshed on 2026-08-10 and 2026-08-18; nothing is invented. Where the repo
is silent, that is stated explicitly.

Canonical sources (never contradict them silently):
`docs/ROADMAP.md`, `docs/PROJECT_BIBLE.md`, `docs/ARCHITECTURE.md`,
`docs/SESSION_LOG.md`, `docs/CHANGELOG.md`, `docs/ISSUE_TRACKER.md`,
`docs/FILESYSTEM_AUDIT_REPORT.md`, `docs/LAUNCHER_AUDIT_REPORT.md`,
`docs/engineering_report.md`, and `docs/KNOWN_ISSUE/*`.

**Before doing anything, read section 0 (Current Situation).** FRIDAY is a
real, working V1 system; the worst possible outcome is a future agent that
rebuilds or reimagines it. Extend within the existing architecture.

---

## 0. Current Situation — READ THIS FIRST

The rest of this document is the full handoff; this section is the snapshot a
new agent needs before touching anything.

### What FRIDAY is (one paragraph)
FRIDAY is a fully-local **Windows voice-first AI Operating System** (Ollama
LLMs + Whisper STT on a CUDA GPU + pyttsx3 TTS), not a chatbot. It
understands, reasons, plans, stores/recalls long-term memory, and acts on the
machine through permission-gated tools. V1 (Phases 1-5) is implemented,
stable, and honest by construction: every machine claim is produced or
verified by a deterministic layer, never by the small LLM's narration alone.

### The filesystem-truth fix cycles — ALL COMPLETE (the current edge)
1. **2026-08-09 — KI-013**: directory listings were stored as durable memory
   facts and the LLM answered contents questions from stale/contaminated
   data. Fixed: `memory_analyzer` Rule-14 store gate + "FILESYSTEM CONTENT IS
   NEVER STORED" prompt contract + deterministic `guard_listing_response`
   wired into `brain._final_response`. (FILESYSTEM_AUDIT_REPORT §8)
2. **2026-08-10 — Round 2**: a 30-convo live suite (`fsq30_convo`) exposed
   two router gaps — `tool_required()` dropped device-capability filesystem
   asks before the raw-text rescue ran, and `what's`→`what s` apostrophe
   poisoning corrupted the recovered reference. Fixed: fs-query gate overrides
   the device short-circuit; apostrophes merged; answer guard extended
   17/17→33/33. (§9)
3. **2026-08-10 — KI-014 / locate guard**: FRIDAY spoke confident absolute
   local paths no tool result produced (web results and memory became local
   paths; a found path was "improved" into a non-existent one). User evidence:
   `srczip`→wrong-kind path, python installer→invented
   `...\python\bin\python.exe`, AC3→invented `C:\Games\...` from a web
   result. Fixed universally, no hardcoded names: `locate_reference()`
   (real-existing-only locate, match kinds exact/normalized/fuzzy, bounded
   multi-candidates), `file_manager._locate` routed through it, router
   locate-ask pass-through, and `guard_path_response` (a local absolute path
   is spoken ONLY when a successful current `file_manager` result produced
   it), chained in `_final_response` after the listing guard. (§10)
4. **2026-08-16/17 — deep-navigation hierarchy fix**: after deeper
   navigation ("python revision" → "chapter 1" → "examples"), follow-up asks
   ("tell me whats inside the examples folder") failed — the old Section 5b
   relative resolution was broken (deterministic first-hit global fuzzy hits
   picked stale leftover folders). Fixed: bounded session **discovery
   registry** + **context chain** + `last_listed_scope`/`active_folder_context`
   in `path_resolver.py` (new `_hierarchy_lookup` tiers, global search only
   as fall-through), and `file_manager._list`/`_read`/`_locate` register
   every verified object into the registry. (§11)
5. **2026-08-17 — empty_path + spoken-number fix**: "tell me whats inside
   the examples" and "chapter one folder" → `parameters={}` `empty_path`
   failures. Root causes proven: (1) `_raw_filesystem_reference` had a
   `len(keep) < 2` rule that killed single-word folder names ("examples",
   "exam") whenever the small Understanding model dropped entities;
   (2) "one" was a `_FS_FRAME_WORDS` member, stripping "chapter one" to
   nothing. Fixed: single-token recovery; compound spoken-number parser
   ("chapter twenty one"→21, "two hundred five"→205); same-parent
   canonical ambiguity ("chapter one" never picks chapter 10). (§12)
6. **2026-08-18 — routing-drift fix (KI-015)**: a REAL production log
   (2026-08-17, 08:28–08:32) showed every folder-content query
   ("tell me whats inside the exam folder", "the lab 3 folder", "its inside
   the c lab folder…") firing `web_search` and the response model
   hallucinating contents (exam1/exam2, "test.py"). Root cause: the
   Understanding model classified the turns `category=search` and the
   variant table maps `"search"→"web"` → capability=web; the fs-query
   rescue was blocked by `goal not in _NON_FILE_GOALS` and
   `tool_cap != "web"`. Fixed: decisive raw-text fs gate `_fs_decisive()`
   (inside phrase + fs noun; list/show/read + fs noun; or a session-verified
   object via new `context_knows()`), pins to file_manager and forces web
   off; genuine web questions ("whats inside a black hole", "whats in the
   news") are never hijacked. (§13)

### Verified test state (latest re-run 2026-08-18, all PASS)
| Suite | Result |
|---|---|
| `locate_guard_regression.py` | 25/25 (incl. contamination A→B→A, failure→success, web→locate) |
| `locate_guard_smoke.py` | 13/13 |
| `fsq_guard_unit.py` | 33/33 |
| `fsq_live_suite.py` | 60/60 |
| `fsq30_convo.py` (+ `fsq30_fixtures.py`) | 30/30 |
| `convo50.py` | 60/60 |
| `p9_fs_accuracy_suite.py` | 128/128 + 6/6 LIVE |
| `fs14_analyzer_gate_suite.py` | 37/37 |
| `manual_weather_real.py` | PASS (Siliguri → web only; srczip → 4 real matches; AC3 → honest not-found) |
| `test_navigation_flow.py` (repo root, 18 tests) | 18/18 — the 9 navigation scenarios + 5 routing-drift regressions (folder asks with the worst-case fabricated web classification + `use_web=True` always land on `file_manager`; genuine web asks always stay on `web_search`) |
| `test_hierarchy_resolution.py` (repo root, 13 tests) | 13/13 — session hierarchy/registry/context-chain resolution |
| `test_universal_fix.py` (repo root, 6 tests) | 6/6 |
| `test_scenario_b.py` / `test_c_lab_exam.py` / `test_fix.py` / `test_verify_fix.py` (repo root) | PASS — legacy live navigation on real `C:\c lab`/`C:\python revision` trees |
Real `memory.json`: **40 facts, 0 listing facts** (additions are the user's
real conversational facts, not contamination).

### The single most important instruction
**Do not rebuild FRIDAY. Do not redesign broad areas. Do not install new
libraries.** V1 (Phases 1-5) is implemented, tested, and wired; extend within
the existing architecture and invariants (sections 13-14). Remaining work:
(a) live-voice validation (5 phrases) pending user recordings; (b) the
RC-01..05 memory fix batch (section 11 / engineering_report §10); (c) V2 /
Phase-8 vector memory — deferred until ROADMAP allows.

### State to be aware of
- The whole working tree is uncommitted (section 15). **Do NOT commit without
  explicit user approval.**
- `guard_listing_response` + `guard_path_response` run on every final reply
  (in that order, then TTS cleanup). They are deterministic and must never be
  bypassed or loosened.
- No `tests/` directory, no CI; the newer filesystem suites live in the
  REPO ROOT (`test_navigation_flow.py`, `test_hierarchy_resolution.py`,
  `test_universal_fix.py`, `test_scenario_b.py`, `test_c_lab_exam.py`,
  `test_fix.py`, `test_verify_fix.py`); the older suites live in
  `C:\Users\polis\AppData\Local\Temp\opencode\`; fixture roots
  `C:\Users\polis\friday_fs_suite` (persistent) and
  `C:\Users\polis\friday_locguard_suite` (created/deleted by suite teardown).
  Do not run suites without user approval.
- Leftover machine artifacts from earlier sessions (cause deterministic
  first-hit global fuzzy hits in tests): `C:\Users\polis\other_exam_final`,
  `C:\Users\polis\other_chapter_1_final`, `C:\test_friday_bug\python
  revision\chapter 1`. Do not delete without user approval.
- Residual, documented, no code change made: KI-010 (open-file-explorer
  mis-launch), KI-011 (launch-turn reply echo), KI-012 (non-Windows
  known-folder OneDrive limitation). Live-voice validation still pending.

---

## 1. Purpose and Vision

FRIDAY is **not a chatbot**. FRIDAY is an **AI Operating System** — a
trustworthy AI companion capable of understanding, reasoning, planning,
remembering, executing, learning, and evolving, always remaining under the
user's authority. (Source: `docs/PROJECT_BIBLE.md`.)

Architecture comes before features. Long-term maintainability is valued over
short-term speed. The whole system is designed so it grows in one direction:
every phase exists because the previous one enables it.

Current product reality (2026-08-10): a **Windows voice-first desktop
assistant** running fully locally (Ollama LLMs + Whisper STT on a CUDA GPU +
pyttsx3 TTS) that can hold a conversation, store/recall long-term memories,
run multi-step plans, route requests to the right local model, and act on the
machine through permission-gated tools (filesystem, application launcher,
terminal, web search, calculator).

Why FRIDAY exists: everything runs on the user's own hardware — no cloud, no
data leaves the machine — and the user stays in authority (permission gates,
honest failures, no fabricated success). Trust is engineered, not promised:
the deterministic layer (resolver → router → executor → prompt → response
guards) is what makes the small local models safe to act on the machine.

---

## 2. What Is Implemented vs Planned vs Deferred

This section is the single most important reality check. Never assume a
feature from the roadmap exists in code.

### IMPLEMENTED (verified in code, working)
- Speech pipeline: WebRTC VAD → capture → Whisper (CUDA, `small` model) → text.
- Text processing/normalization + input validation.
- Understanding layer: one LLM call → structured `LanguageUnderstanding`
  contract (semantic, conversation, emotion, memory, context, entities).
- Semantic triage fast path (`understanding/triage.py`) — skips the full LLM
  for trivial messages (greeting/farewell/gratitude/affirmation/small_talk)
  via embedding similarity to exemplars (threshold 0.85).
- Reasoning engine (`core/reasoning_engine.py`) — decides which systems are
  needed (`use_memory`, `use_episodes`, `use_context`, `use_tools`,
  `use_web`, `use_vision`, `use_planning`, `continuity_only`,
  `continue_conversation`).
- Execution layer (`execution/execution_manager.py`) — coordinates memory,
  tools, web, planning, vision through `if reasoning.use_X` branches.
- Long-term memory: write jury (canonicalizer → validator → classifier →
  conflict resolver → store), importance scoring, categories, history,
  episodes, retrieval (keyword + category + semantic embedding).
- Memory routing via structured query objects (`MemoryQuery`/`EpisodeQuery`
  from understanding, never raw text).
- Context manager: rolling 15-turn buffer, 600s inactivity timeout,
  session-scoped active plan (never persisted).
- Prompt architecture: LLM receives structured context, not raw app state.
- Response generator: sentence-case + trivial templates + markdown-stripping
  for TTS.
- Model Router (Phase 4): capability → model dictionary.
- Planning engine (Phase 3): `core/planner.py`, action space
  {retrieve_memory, search_web, use_tool, generate_response,
  ask_clarification, analyze}, default action generate_response.
- Tool Intelligence (Phase 5): tool_router, tool_executor, skill_registry /
  skill_loader, permission gate, and tools — file_manager, app_launcher +
  app_catalog, terminal, web_search, calculator.
- Brain layer (`core/brain.py`) as dispatcher + conversation path.
- Deterministic command/skill routing + greeting handling.
- Filesystem-content fix (2026-08-09): store gate (memory_analyzer Rule 14
  + "FILESYSTEM CONTENT IS NEVER STORED" prompt contract) and deterministic
  response guard (`response_generator.guard_listing_response`, wired as
  `brain._final_response`). The LLM is never the source of filesystem facts;
  listings are fresh, per-request machine state. Round 2 (2026-08-10):
  device-capability filesystem asks no longer short-circuit in
  `tool_required()`, apostrophe merge fixes `what's` reference poisoning,
  guard extended to denial/evasive/empty claims (17/17 → 33/33).
- Local-path truth fix (2026-08-10, KI-014): `path_resolver.locate_reference`
  (real-existing-only locate; exact/normalized/fuzzy match kinds; bounded
  multi-candidates), `file_manager._locate` routed through it, router
  locate-ask pass-through, and `response_generator.guard_path_response` (a
  local absolute path is spoken only when a successful current `file_manager`
  result produced it) chained in `brain._final_response` after the listing
  guard. Closes fabricated local paths (srczip/python-installer/AC3 evidence
  in FILESYSTEM_AUDIT_REPORT §10; `locate_guard_regression` 25/25).
- Session hierarchy fix (2026-08-16/17): `path_resolver.py` — bounded
  discovery registry + context chain + `last_listed_scope`/
  `active_folder_context`, `_hierarchy_lookup` replaces the broken Section
  5b relative resolution, spoken compound numbers ("chapter twenty one"→21),
  same-parent canonical ambiguity; `file_manager._list`/`_read`/`_locate`
  register every verified object. (§11; `test_hierarchy_resolution` 13/13)
- Router reference fix (2026-08-17): `_raw_filesystem_reference` accepts a
  single surviving token ("examples", "exam") — the old `len(keep) < 2`
  rule + "one" as a frame word killed single-word folder and "chapter one"
  asks whenever the Understanding model dropped entities; compound number
  parser applied through `_canonical_tokens`/`_parse_number_run` and
  `_exact_children` ambiguity. (§12; `test_navigation_flow` 13/13 then)
- Routing-drift fix (2026-08-18, KI-015): folder-content queries routed to
  `web_search` (Understanding classified them `category=search` →
  `_CAPABILITY_VARIANTS["search"]="web"`). Fixed by the decisive raw-text
  gate `_fs_decisive()` (+ `_FS_INSIDE_TEXT_RE`/`_FS_OBJECT_NOUN_RE`/
  `_FS_BARE_VERB_RE` in `tool_router.py` and `context_knows()` in
  `path_resolver.py`): inside phrase + fs noun, list/show/read + fs noun, or
  a session-verified object — pinned to file_manager, web forced off; genuine
  web questions never hijacked. (§13; `test_navigation_flow` 18/18)

### PLANNED (in roadmap, NOT implemented)
- Reflection Engine (Phase 6), Learning Engine (Phase 7), Knowledge Graph
  (Phase 8), Self-Evolution (Phase 9), Vision (Phase 10), Device Control
  (Phase 11), Browser Intelligence (Phase 12), Game Interaction (Phase 13),
  Mobile Integration (Phase 14), Multimodal Reasoning (Phase 15), Proactive
  Intelligence (Phase 16), Wake Word (Phase 17), Ecosystem (Phase 18).
- `core/reflection_engine.py` does **not** exist in the tree (checked).
- `memory/memory_consolidator.py` exists as a stub.
- Vision/web-history/multi-modal features do not exist in code.

### DEFERRED (documented, intentionally postponed)
- `docs/DEFFERED_IMPROVEMENT/DI-001..005`: AI intent detection, text
  normalization, NLU upgrades. Engineering decision: avoid building features
  that will be fully replaced by AI; build clean interfaces instead.
- `docs/IDEAS.md`: wake word, noise suppression, speaker recognition,
  emotion-aware responses, neural TTS (Piper/Coqui/XTTS/ElevenLabs/OpenVoice),
  custom voice.
- Legacy `KNOWN_ISSUE` KI-01..03: keyword intent limits, STT accuracy,
  heuristic memory — historically resolved-by-architecture or accepted.

---

## 3. Repository Layout (verified 2026-08-09, refreshed 2026-08-10)

```
C:\project friday\
  MASTER.md                    (this document)
  main.py                      entry point: load_settings -> start() ->
                               save_message -> start_assistant
  voice_assistant.py           VoiceAssistant loop: listen->transcribe->
                               validate->process->speak; SHUTDOWN_WORDS;
                               grants app_launch permission at startup
  generate_random_test_data.py
  tts_test.py / whisper_test.py / speech_test.py / voice_test.py
  temp.wav                     (recorded test audio, ~1.9 s)
  config\settings.json         assistant_name=Friday, language=en,
                               voice_enabled=true, debug_mode=true
  data\  logs\  output\
  docs\                        (see section 4)
  venv\  venv_cuda\            Python envs (venv_cuda = CUDA/Whisper env)
  src\
    ai\        llm_interface.py (providers dict, register/set/get provider),
               model_router.py (ROLE_MODEL_MAP), prompt_builder.py,
               providers\ base_provider, dummy_provider, ollama_provider
    contracts\ capability.py (CapabilityCategory, 23 constants),
               execution.py, language_understanding.py, planner.py,
               reflection.py, tool.py
    core\      assistant.py, brain.py, context_manager.py,
               context_reasoner.py, conversation_manager.py,
               input_validator.py, memory_router.py, planner.py,
               process.py, reasoning_engine.py, response_generator.py,
               response_manager.py, skill_manager.py, tool_router.py
    execution\ execution_manager.py, memory_executor.py, tool_executor.py
    file_manager\ manager.py (save_message; legacy helper)
    input\     text_input.py
    memory\    memory_decision.py, memory_manager.py, memory_retriever.py,
               memory_query_builder.py, memory_evaluator.py,
               memory_canonicalizer.py, memory_classifier.py,
               memory_conflict_resolver.py, memory_validator.py,
               memory_fact.py, memory_history.py, episode_manager.py,
               episode_retriever.py, episode_summarizer.py,
               knowledge_normalizer.py, memory_consolidator.py (stub),
               memory_service.py, memory_updater.py,
               episodes.json, memory.json, memory_history.json (DATA)
    skills\    app_catalog.py, app_launcher.py, calculator.py,
               file_manager.py, permissions.py, skill_loader.py,
               skill_registry.py, terminal.py, tool_base.py, web_search.py
    speech\    speech_recognizer.py, speech_speaker.py, voice_detector.py
    understanding\ understanding_orchestrator.py, understanding_parser.py,
               understanding_merger.py, understanding_prompt.py,
               llm_understanding.py, triage.py, semantic_analyzer.py,
               conversation_analyzer.py, emotion_analyzer.py,
               memory_analyzer.py, context_analyzer.py,
               end_session_analyzer.py, entity_extractor.py, time_parser.py,
               prompts\ (semantic/conversation/emotion/memory/context prompts)
    utils\     path_resolver.py, config.py, logger.py, tool_logger.py
  README.md / requirements.txt   (both 0 bytes — empty, do not trust)
```

Note: root `README.md` and `requirements.txt` are **empty** (0 bytes). Do not
infer dependencies from them. Dependencies are documented in
`docs/TOOLS/T-01.md` / `T-02.md` (Python 3.12.10, PyTorch 2.11.0 + CUDA 12.8,
Whisper, sounddevice, scipy, soundfile, webrtcvad-wheels, pyttsx3, numpy,
numba, tqdm, requests, tiktoken, pywin32, comtypes).

---

## 4. Docs Inventory

| File | Status | Content |
|---|---|---|
| `docs/ROADMAP.md` | ACTIVE | Master roadmap Phases 1-18 + 2.1-2.8 + sequencing rules. Do NOT modify. |
| `docs/PROJECT_BIBLE.md` | ACTIVE v2.0 | Vision, principles, engineering rules, folder responsibilities. Source of truth for architecture. |
| `docs/ARCHITECTURE.md` | ACTIVE | Pipeline diagrams, per-module purpose/status. Some "Future" items now exist. |
| `docs/CHANGELOG.md` | ACTIVE | 2026-07-28: Brain architecture foundation. |
| `docs/SESSION_LOG.md` | ACTIVE (1417 lines) | Per-session detail through 2026-08-08. |
| `docs/ISSUE_TRACKER.md` | ACTIVE | FRIDAY-001..014 ↔ root causes RC-01..06. |
| `docs/engineering_report.md` | ACTIVE | 5000-test review + implementation prompt for memory fixes. |
| `docs/FILESYSTEM_AUDIT_REPORT.md` | ACTIVE | Phase 5 universal filesystem audit (2026-08-08) + the truth-fix rounds: §8 KI-013 store gate, §9 round-2 router fixes, §10 KI-014 local-path truth fix, §11 session hierarchy fix, §12 empty_path + spoken-number fix, §13 routing-drift fix (KI-015). |
| `docs/LAUNCHER_AUDIT_REPORT.md` | ACTIVE | Phase 5 launcher audit + follow-ups (2026-08-07/08). |
| `docs/RANDOM_STRESS_TEST.md` | DATA | 5000 tests, seed 20260804. |
| `docs/RANDOM_STRESS_1000_TEST.md` | DATA | 1000 tests, seed 20260805. |
| `docs/PHASE3_STRESS_100_TEST.md` | DATA | 100 convo stress (Phase 3). |
| `docs/IDEAS.md` | IDEA | Deferred voice/feature ideas. |
| `docs/KNOWN_ISSUE/KI-01..03, KI-004..012` | ACTIVE | Known issues (see section 11). Naming is inconsistent (KI-01/02/03 vs KI-004..012). KI-013/014 have no files — they are documented inside FILESYSTEM_AUDIT_REPORT §8/§10. |
| `docs/DEFFERED_IMPROVEMENT/DI-001..005` | ACTIVE | Deferred improvements (note the typo "DEFFERED" in the folder name — keep it). |
| `docs/TOOLS/T-01.md, T-02.md` | ACTIVE | Installed tools/libraries; `T-02` lists the CUDA env stack. |
| `docs/RESEARCH/01-MEMORY_GATE.md` | **EMPTY (0 bytes)** | Placeholder; do not treat as authoritative. |

---

## 5. Pipeline Architecture

### 5.1 End-to-end pipeline (verified in code)

```
Microphone
  -> WebRTC VAD (voice_detector)            -> detects start/end of speech
  -> Whisper STT (speech_recognizer, CUDA)  -> text (temperature 0, beam 5, en)
  -> process.py clean_text                  -> lowercase, strip punct/collapse spaces
  -> input_validator                        -> reject empty/invalid
  -> TRIAGE (understanding/triage.py)       -> trivial? skip LLM (social template)
  -> Understanding orchestrator (analyze)   -> ONE LLM call -> LanguageUnderstanding
       (+ semantic/conversation/emotion/memory/context analyzers + entities)
  -> Reasoning engine (reason)              -> ReasoningResult (which systems)
  -> ExecutionManager (execute)             -> branches: memory / context /
                                                tools / web / planning / vision
  -> Prompt builder                         -> structured context + TOOL RESULTS
  -> Model Router (capability -> model)     -> pick model
  -> LLM (ollama)                           -> response text
  -> Response generator (sentence_case)     -> clean spoken reply
  -> TTS (speech_speaker, pyttsx3)          -> speak
```

No layer skips another (PROJECT_BIBLE pipeline: Understanding → Reasoning →
Execution → Prompt → LLM → Response → Reflection(future) → Memory update).

### 5.2 Key contracts (`src/contracts/`)
- `LanguageUnderstanding` (language_understanding.py): goal, intent, category,
  capability, memory_scope/operation, canonical_fact, uncertain_terms,
  confidence breakdown, entities.
- `ReasoningResult` (core/reasoning_engine.py): the use_* flags; also
  `continuity_only`, `continue_conversation`.
- `MemoryFact` (memory/memory_fact.py): operation + canonical_fact; owned by
  Memory layer; per-stage confidence with `gate_confidence()` (currently
  under-used — see engineering report RC-01).
- `MemoryQuery` (memory/memory_query_builder.py): built from understanding,
  never raw text; category-aware; `query_text` field for embedding-only.
- `EpisodeQuery`, `ExecutionPlan`/`PlannerInput` (contracts/planner.py),
  `ReflectionInput`/`ReflectionResult` (contracts/reflection.py — stub,
  Phase 6 not built), `ToolResult`/`ToolRequest` (contracts/tool.py),
  `CapabilityCategory` (capability.py).

### 5.3 Brain layer
`core/brain.py` is the dispatcher. It calls `conversation_manager.process()`
which runs: understanding → reasoning → execution → prompt → LLM. It has a
`DETOUR_GOALS = {"retrieve_information", "amusement"}` set (a goal in that set
detours around the planner) and `_clean_response()` which strips markdown
(bold, bullets, blank lines) for TTS. Every final response now flows through
`_final_response(response, execution, understanding=None)` =
`_clean_response(guard_path_response(guard_listing_response(response,
execution.tool_results), execution.tool_results, raw_text))`: the
deterministic **listing guard runs first**, then the **local-path truth
guard**, then TTS cleanup — on every spoken reply (10 call sites pass
`understanding`). Shutdown
words (`assistant.py`, `voice_assistant.py`) end the session; `assistant.py`
does a forced rollover(force=True) on shutdown (Issue 10 in the launcher
audit lineage).

### 5.4 Memory system (deep dive)
Write path:
1. Understanding emits `memory_operation` + `canonical_fact` (+
   `uncertain_terms`, `confidence_breakdown`).
2. `memory_analyzer.py` applies 14 deterministic Rules (suppress no-write
   forms, route recall, force query on recalls, imperative forget).
   **Rule 14 (2026-08-09)**: filesystem-inspection frames and
   content-state statements — closed-class vocab (location nouns,
   inspection frames, state predicates) — force an inspection question
   to a memory query with **no fact**, and a content-state statement
   ("contains", "is inside") to **no write**. Directory listings are
   never durable memory facts (see 5.7 guard + `understanding_prompt.py`
   "FILESYSTEM CONTENT IS NEVER STORED").
3. `memory_decision.py` `process()`: `is_uncertain()` gate →
   `needs_clarification`; then Canonicalizer → Validator → Classifier →
   Evaluator (importance) → Conflict Resolver → Store. Statuses: `stored`,
   `updated`, `needs_clarification`, `needs_confirmation`, `ignored`, `None`;
   tracks `last_event`. Forget path `_process_delete()` skips the evaluator
   and matches by subject.
4. Storage: `memory_manager.py` (store_fact/delete_fact), `memory.json`,
   `memory_history.json`, `episodes.json` (real data — OFF-LIMITS to tests;
   harnesses redirect to temp stores).

Read path:
1. `reasoning_engine.reason()` sets `use_memory/use_episodes/use_context`.
2. `memory_router.py` builds `MemoryQuery`/`EpisodeQuery` from understanding
   (never raw text); history scope uses `retrieve_history()`.
3. Retrievers: `memory_retriever.py` (keyword + category + embedding semantic
   scoring with 0.5 floor / 0.7 full-weight ramp; high-value boost only ranks
   already-matched memories), `episode_retriever.py` (episodes),
   `memory_query_builder.py` (`CATEGORY_MAP` incl. `education`, profile /
   history / specific builders).

Phase 2.7 education fix (KI-004) is in place: `education` category detected
before `device` in `detect_category` with importance 9; `education` in
`CATEGORY_MAP`/keywords/profile list; embedding semantic scoring; study/
education patterns in `memory_evaluator.py`.

### 5.5 Planning engine (Phase 3)
- `core/planner.py` + `contracts/planner.py`.
- `VALID_ACTIONS = {retrieve_memory, search_web, use_tool, generate_response,
  ask_clarification, analyze}`; `DEFAULT_ACTION = generate_response`.
- Builds prompts with recent context; produces `ExecutionPlan`.
- Context manager holds a **session-scoped `_active_plan`** (continuity).
  It is derived per-session and never persisted across sessions.
- Brain detour: goals in `DETOUR_GOALS` bypass planner (see 5.3).
- Phase 3 stress (PHASE3_STRESS_100_TEST, 2026-08-06): 99/100 exercised,
  97 pass (98.0%), 2 extreme failures (convo 71 "madrid pivot" expected
  pivot got continue; convo 75 expected pivot got continue), memory regression
  8/8, goal pool 176/180.

### 5.6 Model Router (Phase 4)
- `src/ai/model_router.py`. `ModelRole` roles: FAST_CHAT, DEFAULT_CHAT,
  REASONING, CODING.
- `ROLE_MODEL_MAP` is the **only** place physical model names live:
  - FAST_CHAT → `llama3.2:1b`
  - DEFAULT_CHAT → `llama3.2:3b`
  - REASONING → `llama3.1:8b`
  - CODING → `qwen2.5-coder:7b`
- Routing is a pure dictionary lookup from `semantic.category` →
  role → model. Unknown category → `general`/DEFAULT_CHAT fallback (safe).
- `llm_interface.py`: providers dict, `register_provider` /
  `set_provider` / `get_provider`, ollama is the default provider.

### 5.7 Tool Intelligence (Phase 5) — MOST DETAILED
This is the largest, most-fixed area. Full lineage in
`docs/FILESYSTEM_AUDIT_REPORT.md` and `docs/LAUNCHER_AUDIT_REPORT.md`.

Architecture:
```
 User message
   -> [UNDERSTANDING] capability/goal/entities (noisy labels absorbed downstream)
   -> [TOOL ROUTER] route_tool(understanding, reasoning)
        locate phrase / machine scope  -> automation (file_manager), web OFF
        folder/path label + device cap -> automation (file_manager)   [folder rescue]
        open_application goal + device -> app_launcher                 [launch pin]
        web goal / web cap             -> web_search (never for locate/launch)
   -> [TOOL EXECUTOR] permission gate -> execute(request)
   -> [FILE MANAGER] FileManagerTool.execute(action, path)
        path = reference built from structured entities (never raw prose)
        resolve_reference(path) -> ResolvedPath{found, path, kind, exists}
   -> [PROMPT BUILDER] TOOL RESULTS (structured facts, no raw paths)
   -> [RESPONSE] guard_listing_response + guard_path_response deterministically
        rewrite any narration that invents files/folders or local paths
```

`src/utils/path_resolver.py` — deterministic read-only universal resolver.
Tiers (first match wins):
1. Absolute path (`expandvars`/`expanduser`, normalized; carries `exists`).
2. Known folder — Windows `SHGetKnownFolderPath` (ctypes) so OneDrive-
   redirected Desktop/Documents/Pictures resolve to real locations;
   singular/alternate aliases mapped to canonical shell key; env-var
   fallback when shell unavailable (KI-012).
3. Drive reference — "c drive", `c:`, `c:\`, bare `c` → `C:\`; drive-scoped
   name search.
4. Workspace/cwd aliases — "project", "here" (matched on raw words).
5. Explicit relative path — against cwd then workspace.
6. Name search — every drive root, then USERPROFILE, PUBLIC, then workspace
   (a candidate like any other, never a default). Shallow first, then bounded
   deep (max depth 3, 5000 entries, system/cache pruned, per-root
   independent depth/budget). Dictated-name handling `_spoken_filename`
   ("rootfile dot txt" → `rootfile.txt`) and `<name> <known folder>` scoping
   ("friday probe e desktop") as stages 6a/6b. Conversation-scoped follow-up
   search `_scoped_followup_search` (tolerant majority-token match inside the
   just-listed directory; ties = ambiguous miss, never a guess; only after all
   normal paths miss).
7. No silent fallback: unresolved → `error="not_found"`/`"empty"`, no path.

Companion API **`locate_reference(reference)`** (path_resolver.py:715) is the
same deterministic machinery powering `file_manager._locate`: real-existing
matches only, match kinds `exact`/`normalized`/`fuzzy`, bounded multi-match
candidates (≤ 4, all real), `error="empty"`/`"not_found"` on no hit. A "found"
path is always a real file/folder on disk — a web result or a memory is never
a path. `LocateResult`/`LocateCandidate` are the contract dataclasses.

Guardrails: type-descriptor stopwords are singular + noun-modifying only
(`game`, `app`, `file`; plural `games`/`files`/`program` stay significant —
`C:\games`, `Program Files`); fuzzy containment requires both tokens ≥ 2
chars; `%TEMP%` is NOT in search roots (removed this cycle).

`src/skills/file_manager.py` — actions: `read` (SAFE), `write`
(FILE_WRITE gate), `list`, `delete` (FILE_DELETE gate), `locate` (runs
`locate_reference` **before** the not-found gate; returns
`{found, path, kind, match, requested, candidates}`); no default base
(missing reference = `empty_path`, unresolved = `not_found` carrying
`metadata.requested` = user's string); sets `last_listed_scope` after a
successful directory list.

`src/core/tool_router.py` — the routing brain:
- `_filesystem_reference()`: builds path param from structured entities
  (excludes machine-scope words like "my pc"; `application` label counts only
  for locate or folder/path text).
- `_filesystem_action()`: picks locate/read/list from intent, goal, user words
  (reads `read`/`read_file`/`readfile` from intent/goal).
- `_filesystem_locate_signal()`: rescue pins locate → file_manager before
  launch pins; forces web off. "where is paris" (no machine scope, no
  file/folder entity) stays web.
- `_FS_NOUN_RE`: raw-text filesystem-noun locate signal ("where is the gur src
  zip", "location of the assassins creed 3 remastered folder") — pins locate
  to `file_manager` so AC3-style asks reach the resolver, never web search.
- `tool_required()` locate pass-through: a locate/file-noun ask reaches the
  tool path even when capability resolves to web/hardware (AC3 came in labeled
  as web info; the pass-through is what routes it to `file_manager` instead).
- `_FS_QUERY_TEXT_RE`: raw-text filesystem ask detection
  ("what's/what is inside", "contents of", list/show/read verb + folder/file
  word) — pinned to automation before `open_application`/launch pins;
  explicit web goals never hijacked.
- Session hierarchy (2026-08-16/17): `path_resolver.py` holds a bounded
  discovery registry (`_DiscoveryRecord`, 512, oldest-evicted) fed by
  `register_discovered()` (read/locate) and `set_last_listed_scope(path,
  entries)` (successful lists); `active_folder_context`/
  `clear_active_folder_context` manage the session context chain;
  `_hierarchy_lookup` (exact children of the last-listed folder → context
  chain → single verified record → relative path against chain bases, global
  search only as fall-through) replaced the broken Section 5b. `context_knows()`
  (registry/chain only, never a global disk search) is the public hook the
  router uses to keep a bare "whats inside X"/"read X" ask on file_manager
  once the object was verified this session.
- Spoken numbers (2026-08-17): `_NUMBER_WORDS` values + `_canonical_tokens`/
  `_parse_number_run` collapse compound runs ("chapter twenty one"→21, "two
  hundred five"→205) applied in `_tokens_match`/`_norm_key`; `_exact_children`
  + same-parent canonical ambiguity in tier 2 ("chapter 1"+"chapter one" in
  the same parent = ambiguous; with chapter 10/11 present, "chapter one" →
  deterministically chapter 1).
- Routing drift decisive gate (KI-015, 2026-08-18): `_CAPABILITY_VARIANTS`
  maps `"search"→"web"`, so a fabricated `category=search` made folder asks
  fire web_search. New `_fs_decisive(raw_text)` + `_FS_INSIDE_TEXT_RE`
  (whats/what is inside, whats in, its inside, contents of) +
  `_FS_OBJECT_NOUN_RE` (folder/directory/dir/drive/desktop/downloads/
  documents/file) + `_FS_BARE_VERB_RE` (list/show/read): decisive = inside
  phrase + fs noun, list/show/read + fs noun, or verb/inside phrase with a
  session-verified object. `route()` then pins `tool_cap="automation"` and
  forces `use_web=False; goal_search_web=False` (same pattern as the
  launch/locate rescues); `tool_required()` enters the tool path. Genuine
  web asks ("whats inside a black hole", "whats in the news", "read me a
  story", "show me pictures") never match and stay on web_search.
- `has_launch_signal()`: `goal == "open_application"` or intent
  command/request with `application`-labeled entity; **now requires a raw
  launch verb** (`_raw_text_is_launch`: open/launch/start/run after
  politeness filler; raw text is the only signal the Understanding model
  cannot hallucinate).
- `_raw_text_launch_ref()`: strips pre-verb filler, requires literal first
  token open/launch, recovers app reference via `_fallback_app_reference`
  (folder/path-style text rejected, single-letter references rejected).
- Launch suppression: `use_web=False`/`goal_search_web=False` on launch;
  `use_planning = (base_planning or continuity) and not launch_signal`;
  `continuity_only = continuity and not base_planning and not launch_signal`.
- `tool_required()`: enters tool path for raw-text filesystem query even when
  capability resolves to memory/hardware; returns False for a device
  capability without a launch verb (when tools flag off) — fabricated
  launches never enter the tool path; when model DID set the flag, H1
  honest-failure contract preserved.
- file_manager requests carry `parameters={"path": ref}` (or `{}` → executor
  returns structured `empty_path` failure).

`src/execution/tool_executor.py` — executes ToolRequests, enforces the
permission gate here, never crashes Brain, logs tool events.

`src/skills/permissions.py` — `PermissionGate`,
`ToolPermission.DEFAULT_ALLOWED`; `FRIDAY_TOOL_PERMS` env var;
`grant()`/`revoke()`. Default allow for safe tools (e.g. read/list/calculator/
web search); write/delete/launch gated. `app_launch` is denied by default and
granted at startup by `voice_assistant.py`.

`src/skills/app_catalog.py` — universal application catalog:
- Sources: Start Menu `.lnk`, Desktop, registry `Uninstall`, WindowsApps
  alias stubs, **`Get-StartApps` index (AUMIDs)** for packaged/MSIX apps
  (WhatsApp, Teams, Photos, XBOX, Outlook, Media Player, Copilot, Snipping
  Tool, Clock, Weather, ~38 more on this host), Steam manifests, Epic
  manifests, fixed Windows utilities (builtins). 216 entries on this machine
  (start_menu 98, builtin 15, registry 23, windowsapps 80).
- `resolve(app)` → `found | ambiguous | not_found` (never a guess). Exact →
  subset → aligned → fuzzy tiers, confidence threshold 82; multi-token query
  required for fuzzy pins; pinned name token ≥ 5 chars; `_FILLER` /
  `_SKIPPABLE_CATEGORY` (browser/program) / `_PIN_CATEGORY`
  (app/application/manager/viewer/player; "whats app"→"whatsapp");
  `_collapse_duplicates` longest-wins; `_launchable` recognizes AUMID targets.
- AUMID entries activate via `explorer.exe shell:AppsFolder\<aumid>`
  (`subprocess.Popen`), `os.startfile(target)` fallback for real files.

`src/skills/app_launcher.py` — `ApplicationLauncherTool`, APP_LAUNCH
permission, Windows `os.startfile`, `data.detail` = display name only
(never paths).

Prompt/response layer for tools (`src/ai/prompt_builder.py`):
- `_format_memories_grouped` with CATEGORY_LABELS (preference, device,
  identity, project, emotional, general); `_format_context` from session
  buffer.
- `_render_tool_payload`: dedicated `app_launcher` branch renders a success
  as `Opened application: <detail>`; file_manager success renders
  `Found: <path> (<kind>)`; miss renders
  `Outcome: not found: '<requested>'.` (uses `metadata.requested`).
  **Locate render (2026-08-10)**: shows the match kind
  (exact/normalized/fuzzy) and every real candidate path, so the response
  layer can rebuild an honest multi-match answer.
- **Internet-info marker (2026-08-10)**: web search results are explicitly
  labeled "internet info" in the prompt, and the path-truth instruction says a
  web page or a memory is never a local path — this is what stops AC3-style
  `C:\Games\...` inventions at the prompt layer.
- Ambiguity block (candidates, "which one do you mean?"), non-success branch
  ("I could not do it" — fabrication impossible), stale-context guard
  ("TOOL RESULTS are the only facts; ignore ENTITIES MENTIONED and RECENT
  CONVERSATION"), BASE_HONESTY_RULES.
- **Deterministic filesystem answer guards (2026-08-09/10)**
  (`response_generator.py`): two guards run in `brain._final_response` (5.3).
  `guard_listing_response(response, tool_results)` makes the LLM's narration
  of file operations honest no matter what the 3b model writes. It inspects
  the real `file_manager` results:
  - a **successful listing** reply containing fabricated names (regex
    `_FAB_TOK_RE`, ext-bearing tokens; spaced names via multi-word
    containment) or fabricated counts, or grant/permission language, is
    replaced with a deterministic listing built from the real `entries`;
  - a **not_found** result whose reply asks permission or fails to admit the
    miss → deterministic honest not-found reply;
  - a **failure** result (e.g. `empty_path`) whose reply asks permission or
    names files → deterministic failure reply ("I couldn't look that up…");
  - **extended (round 2)**: also catches empty/only-one-content claims, denial
    language, and evasive no-information replies;
  - `read`/launch/non-filesystem/no-result replies pass through untouched.
  `guard_path_response(response, tool_results, raw_text)` closes the
  **local-path truth** class (KI-014): an absolute local path may be spoken
  ONLY when a successful current `file_manager` result produced it
  (`_allowed_paths()` collects the real paths; `_spoken_paths()` is a
  dash-safe tokenizer — paths with a bare hyphen like
  `Godot_v4.6.3-stable_win64.exe.zip` are not truncated). Locate replies are
  regenerated deterministically (`_deterministic_locate`) from the real
  candidates with their match kind; a locate ask whose only result was web
  information gets an honest "not on this computer". `_deterministic_listing`/
  `_deterministic_not_found`/`_deterministic_failure`/`_deterministic_locate`/
  `_deterministic_no_local_path`/`_deterministic_not_found_named` are the only
  fallback texts; wiring is `brain._final_response` (see 5.3). Unit suites:
  `fsq_guard_unit.py` 33/33, `locate_guard_smoke.py` 13/13,
  `locate_guard_regression.py` 25/25.

Execution manager (`execution/execution_manager.py`):
- Maps natural-language `end_session` intent to runtime shutdown.
- Synthesizes a failure ToolResult when a capability resolves to a registered
  tool but no request is routable (empty tool path → honest failure, no
  fabricated success).

### 5.8 Understanding details
- `understanding/triage.py`: embedding cosine similarity to exemplars;
  skip full LLM when trivial.
- `_float_confidence` coerces null → 0.0 (crash fix in orchestrator).
- `end_session_analyzer.py`: end-session / topic-dismissal YES/NO classifier.
- `entity_extractor.py`, `time_parser.py`, `understanding_parser.py` /
  `understanding_merger.py`, per-aspect analyzer files.
- Known fragility: the small model emits off-enum `capability` (KI-007),
  spurious `memory_operation: store` on math (KI-008), and structural drift
  on long conversations (KI-009). Mitigations are router-side, not
  Understanding-side (durable fix = schema validation + retry, KI-007).

---

## 6. Model/Provider Configuration

- Default provider: Ollama (local). `LLMInterface` supports pluggable
  providers (base/dummy/ollama).
- Embedding model: `nomic-embed-text` (triage, semantic retrieval).
- Physical model names ONLY in `ROLE_MODEL_MAP` (model_router.py).
- Whisper: `small` model, CUDA GPU, `temperature=0, beam_size=5, language=en`
  (per live-voice validation scripts). GPU = RTX 4050.
- TTS: pyttsx3 (robotic, known; neural TTS deferred to IDEAS.md).
- Config: `config/settings.json`.

---

## 7. Current Machine Capabilities (this host, 2026-08-10)

Verified tool capabilities (all permission-gated and regression-proven):
- **Filesystem**: read, list, write (gated), delete (gated), locate anywhere
  on the machine — absolute paths, drive letters (`c drive`), known folders
  (OneDrive-redirected Desktop/Documents/Pictures via shell table), workspace
  aliases, name search (shallow + bounded deep), dictated filenames, folder-
  scoped dictation, just-listed-directory follow-ups, honest misses. Locate
  (2026-08-10) returns only real-existing matches with a match kind
  (exact/normalized/fuzzy) and bounded multi-candidates; a spoken absolute
  path is guaranteed to be a real current tool result (`guard_path_response`).
- **Application launcher**: universal discovery (Start Menu/Desktop/registry/
  WindowsApps/Get-StartApps AUMIDs/Steam/Epic/builtins), resolve found/
  ambiguous/not_found, fire-and-forget launch (honest "launched" ceiling),
  packaged-app activation via shell:AppsFolder.
- **Terminal**: permission-gated tool (present in skills/).
- **Web search**: `web_search` skill (never for locate/launch).
- **Calculator**: `calculator` skill.
- Ground-truth paths used in tests: `C:\games\Marvel's Spider-Man 2`,
  `C:\python projects`, `C:\c projects`,
  `C:\Users\polis\friday_fs_suite` (suite fixture root),
  `C:\Users\polis\OneDrive\Desktop\friday_probe_e`.
  Manual real-file locate evidence (2026-08-10): "srczip" → 4 real matches
  including `C:\project friday\src`; python installer → real
  `C:\Users\polis\Downloads\Python 3.12 Installer.exe`; AC3 folder → honest
  not-found (no `C:\Games\...` fabrication).

---

## 8. Known Phase 5 Problems (historical, fixed or documented)

Fixed this cycle (all regression-proven, see FILESYSTEM_AUDIT_REPORT):
- **Folder-content queries firing web_search (KI-015, 2026-08-18)**: a REAL
  production log showed "tell me whats inside the exam folder" / "the lab 3
  folder" / "its inside the c lab folder…" answering from `web_search` with
  hallucinated contents (exam1/exam2, "test.py"). Root cause: Understanding
  classified the turns `category=search` → `_CAPABILITY_VARIANTS["search"]`
  = "web" → capability=web; the fs-query rescue was blocked by `goal not in
  _NON_FILE_GOALS` and `tool_cap != "web"`. Fixed with the decisive raw-text
  gate `_fs_decisive()` (+ `context_knows()`): folder asks are pinned to
  file_manager and web is forced off; genuine web questions are never
  hijacked. (§13; `test_navigation_flow` 18/18)
- **`empty_path` on single-word folder / "chapter one" asks (2026-08-17)**:
  `_raw_filesystem_reference` had `len(keep) < 2` (killed "examples",
  "exam") and "one" was a frame word (stripped "chapter one"). Fixed:
  single-token recovery + compound spoken-number parser +
  `_exact_children` ambiguity. (§12; `test_navigation_flow` 13/13)
- **Deep-navigation hierarchy resolution (2026-08-16/17)**: follow-up asks
  after multi-level navigation hit the wrong folder (deterministic first-hit
  global fuzzy matches, e.g. "examples" → stale leftover `other_exam_final`).
  Fixed: session discovery registry + context chain + `last_listed_scope`
  (`_hierarchy_lookup` replacing Section 5b, global search as fall-through
  only). (§11; `test_hierarchy_resolution` 13/13)
- Spider-Man 2 locate → web search. Fixed by `_filesystem_locate_signal`
  (pins locate, web off). Verified offline: `file_manager.locate` → `C:\games\Marvel's Spider-Man 2`.
- "…in my pc" locate → app launcher. Fixed: locate rescue runs before launch pin.
- "whats inside my games folder in c drive" → listed project root / hallucinated
  games. Fixed: path built from entities → `C:\games`, real contents.
- RPS false extra files / wrong-directory repeats / Python-vs-C projects folder
  confusion: fixed via coverage-based token containment matching,
  `_LOCATE_STRONG_RE`, `_filesystem_locate_signal` machine-scope check.
- New-file detection (p8): 10/10 after per-root deep-search budgets, single-
  letter frame-word re-attach ("probe i"), read-via-goal, dictated names +
  folder scoping.
- Live-pipeline routing (60-turn convo): `_FS_QUERY_TEXT_RE` rescue,
  raw-text read verb, `tool_required` bypass.
- **Fabricated local paths (KI-014, 2026-08-10)**: web info or memory spoken
  as a local path (srczip → wrong-kind path, python installer → invented
  `...\python\bin\python.exe`, AC3 → invented `C:\Games\...` from a web
  result). Fixed universally with `locate_reference` (real-existing-only) +
  `guard_path_response` (absolute paths spoken only from successful current
  `file_manager` results) — FILESYSTEM_AUDIT_REPORT §10; `locate_guard_regression`
  25/25 + manual real-file locates PASS.
- Launcher BUG 1-8, Bug A1/A2, Bug B (WindowsApps alias stubs), packaged-app
  discovery gap, sequential-launch context bug, launch-success narration
  response-layer fix — all documented in LAUNCHER_AUDIT_REPORT (74/74,
  28/28, 255/255, etc.).

Still documented as residual (no code change made by user request):
- **KI-010**: "open file explorer" sometimes lists project root and claims
  launch. Root cause: Understanding labels entity `file`/`location` →
  `_FILE_LABELS` folder rescue wins over launch pin by design; file_manager
  list with no path defaults to workspace root. Deterministic once the label
  fires.
- **KI-011**: launch-turn reply occasionally re-states the prior answer
  (RECENT CONVERSATION bleed into 1b model's reply). Launch itself correct.
- **KI-012**: non-Windows known-folder fallback can't follow OneDrive
  redirection (Windows-first by design).

---

## 9. STT vs Intent vs Resolution vs Tool-vs-Response Failure Distinction

When a live failure is reported, classify it before changing code:

1. **STT failure** — Whisper produced the wrong text (e.g. "rock paper
   caesar" for `rock_paper_seizor`). Evidence: transcript in log differs from
   user intent. Fix domain: speech/ (prompting Whisper, temperature/beam,
   or accepting minor mismatch via tolerant scoped follow-up).
2. **Intent failure** — text is correct but Understanding mislabeled
   capability/goal/entities (off-enum capability, spurious store op,
   fabricated launch goal). Evidence: structured output in the trace.
   Fix domain: understanding/ (worked examples, schema validation) — NOT
   the router. Router rescues are band-aids (documented KI-007/008/009).
3. **Resolution failure** — the tool got the right intent but the wrong
   target (path/app). Evidence: tool request params wrong. Fix domain:
   path_resolver.py / app_catalog.py.
4. **Tool-vs-response failure** — the tool did the right thing but the LLM
   narrated it wrongly (fabricated listing, permission echo, stale echo).
   Evidence: ToolResult correct in trace, spoken reply wrong. Fix domain:
   prompt_builder.py rendering + honesty rules, possibly a stronger
   response-tier model for tool turns. **Path fabrication (web/memory spoken
   as a local path) is this class** and is closed deterministically by
   `guard_path_response` (see 5.7 / KI-014).

The standing rule: the deterministic layer (resolver/router/executor/prompt/
response guards) must make fabricated success impossible; the small response
model is the last narration step and its wording quirks are not pipeline
bugs.

---

## 10. Testing History and Philosophy

Threshold: **85% overall pass ≈ V1-acceptable**; the deterministic layer must
never silently fail. Every change re-runs affected suites + `python -m
py_compile` on touched modules.

| Suite | What | Latest result |
|---|---|---|
| `random_stress.py` (5000, seed 20260804) | memory write/read randomized | 85.5% (4277P/717F/6E) |
| `p7_fs_stress.py` | filesystem resolver/tool/prompt/routing (59→63 checks) | 63/63 |
| `p5_launch_validation.py` | launcher audit (74 checks) | 74/74 |
| `p5_seq_launch.py` | 28 sequential launches | 28/28 |
| `p5_response_probe.py` / `p5_honesty_probe.py` | response/honesty | 5/5, PASS |
| `p8_newfile_probe.py` | fresh-file detection (10 probes) | 10/10 |
| `convo50.py` | live 60-turn conversation | 60/60 |
| `fsq_live_suite.py` | folder contents-retrieval (60 items, live) | 60/60 |
| `fsq_guard_unit.py` | filesystem answer guards (deterministic, incl. round-2 denial/evasive classes) | 33/33 |
| `fsq30_convo.py` (+ `fsq30_fixtures.py`) | 30-convo live suite on real user folders | 30/30 |
| `locate_guard_smoke.py` | locate guard (deterministic) | 13/13 |
| `locate_guard_regression.py` | locate path-truth regression (incl. contamination A→B→A, failure→success, web→locate) | 25/25 |
| `manual_weather_real.py` | real pipeline: Siliguri→web only; srczip→4 real matches; python installer→real path; AC3→honest not-found | PASS |
| `fs14_analyzer_gate_suite.py` | memory_analyzer Rule 14 gate | 37/37 |
| `p9_fs_accuracy_suite.py` | fs accuracy regression | 128/128 + 6/6 LIVE |
| `p6_stress_500.py` | Phase 5 stress | 255/255 |
| `p5_stress_50` / `p4_stress_50` | phase stresses | 42/42, 64/64 |
| `resolver_fix_probe.py` / `fix_probe.py` | targeted fixes | 18/18, 17/17 |
| `chat_regression.py` | pure chat: zero launches/web | 10/10 |
| `random_stress_1000` (seed 20260805) | memory stress | 98.3% |
| PHASE3 stress 100 | planning/convo stress | 98.0% |
| `test_navigation_flow.py` (repo root) | 9 navigation scenarios + 5 routing-drift regressions, drives the REAL `FileManagerTool` with unique uuid fixture roots (avoids real-folder shadowing) | 18/18 |
| `test_hierarchy_resolution.py` (repo root) | session hierarchy/registry/context-chain/spoken-number unit suite | 13/13 |
| `test_universal_fix.py` (repo root) | universal reference + number regression | 6/6 |
| `test_scenario_b.py` / `test_c_lab_exam.py` / `test_fix.py` / `test_verify_fix.py` (repo root) | legacy live navigation on real `C:\c lab` / `C:\python revision` trees | PASS |

Harness location: the NEW filesystem suites live in the REPO ROOT
(`test_*.py`); the OLDER suites live in
`C:\Users\polis\AppData\Local\Temp\opencode\` (outside the repo; no
`tests/` directory, no CI — known technical debt). Suite fixture roots:
`C:\Users\polis\friday_fs_suite` (persistent) and
`C:\Users\polis\friday_locguard_suite` (created/deleted by suite teardown);
`test_navigation_flow.py` builds its own uuid fixture root
`C:\friday_nav_flow_<uuid>` and deletes it in teardown. Probes delete
their machine fixtures after proof; machine state must be restored after every
run. The table above was re-verified 2026-08-18 after the KI-015 fix.

Stress-test philosophy (engineering_report): failure mass concentrates in
LLM-driven predicates and extraction leaks, NOT hardware/pipeline faults;
fix at the prompt/gate layer with deterministic guards; always guard with a
no-write regression class.

---

## 11. Known Issues and Deferred Improvements Index

### KNOWN_ISSUE (note inconsistent numbering: KI-01/02/03 vs KI-004..012)
- KI-01: keyword intent can't handle spelling mistakes (superseded by LLM
  understanding).
- KI-02: Whisper STT accuracy on unclear speech.
- KI-03: heuristic memory/context/intent/response limitations (era doc).
- KI-004: education category missing from memory category mapping (FIXED —
  Phase 2.7 memory fixes, see 5.4).
- KI-005: compound "dismiss + recall" ends the session (deferred to Layer 3
  response pipeline; safe failure).
- KI-006: politeness message mid-plan derails into active plan (deferred to
  Layer 3; safe failure). Root causes: triage false negative, off-taxonomy
  intent "acknowledgment", continuity gate passes, planner goal-bias, brain
  `plan_detour` backstop misses `remember_information`.
- KI-007: Understanding emits off-enum `capability` variants; router falls
  back gracefully (deferred; durable fix = schema validation + retry + worked
  examples).
- KI-008: spurious `memory_operation: store` on a math question derails the
  answer into a clarification (deferred; worked examples + gate memory op on
  goal).
- KI-009: structural drift on long conversations (raw-text gates absorb it;
  durable fix = KI-007).
- KI-010: "open file explorer" mis-launch (documented, no code change).
- KI-011: launch-turn reply echoes prior answer (documented, no code change).
- KI-012: known-folder env fallback can't follow OneDrive redirection on
  non-Windows (documented limitation).
- KI-013: **FIXED 2026-08-09** — directory listings were stored as durable
  memory facts (cross-contamination: C Lab merged into Python Projects) and
  the LLM answered contents questions from stored, stale facts. Fixed by the
  Rule-14 store gate + "FILESYSTEM CONTENT IS NEVER STORED" prompt contract +
  the deterministic filesystem answer guard (see 5.4 / 5.7 / FILESYSTEM_AUDIT
  section 8). Verified: `fsq_live_suite` 60/60, real `memory.json` has 0
  listing facts after all runs.
- KI-014: **FIXED 2026-08-10** — FRIDAY spoke confident absolute local paths
  no tool result produced (web results or memory became local paths; a found
  path was "improved" into a non-existent one). Fixed: `locate_reference`
  (real-existing-only locate) + `guard_path_response` (absolute paths spoken
  only from successful current `file_manager` results), wired in
  `brain._final_response` after the listing guard (FILESYSTEM_AUDIT section
  10; no KI file — same convention as KI-013). Verified: `locate_guard_regression`
  25/25, manual real-file locates, all prior suites green.
- KI-015: **FIXED 2026-08-18** — folder-content queries ("tell me whats
  inside the exam folder", "the lab 3 folder", "its inside the c lab folder
  in my c drive") routed to `web_search` and the response model hallucinated
  contents (exam1/exam2, "test.py"); real production log 2026-08-17
  08:28–08:32 (Need Tools/Web both False, web still fired via the resolved
  web capability). Root cause: Understanding classified the turns
  `category=search / goal=search_web / capability=search` and
  `_CAPABILITY_VARIANTS["search"]="web"`; the fs-query rescue was blocked by
  `goal not in _NON_FILE_GOALS` and `tool_cap != "web"`. Fixed by the
  decisive raw-text gate `_fs_decisive()` in `tool_router.py` (+
  `context_knows()` in `path_resolver.py`), which pins unmistakable
  filesystem-contents asks to `file_manager` and forces web off; genuine web
  questions ("whats inside a black hole", "whats in the news", "read me a
  story") are never hijacked (FILESYSTEM_AUDIT section 13; no KI file — same
  convention as KI-013/014). Verified: `test_navigation_flow` 18/18 incl.
  the 5 routing regressions; live simulation with the exact log flags routes
  `['file_manager']`; all prior suites re-passed. The 2026-08-16/17 hierarchy
  and empty_path/numbers cycles (§11/§12) are likewise documented inside
  FILESYSTEM_AUDIT_REPORT, no KI files.

### DEFFERED_IMPROVEMENT
- DI-001: AI intent detection (replace keyword `detect_intent()` with LLM;
  architecture already supports it).
- DI-002: text normalization (likely unnecessary once AI intent exists).
- DI-003: NLU for free-form phrasing (priority High, deferred).
- DI-004: STT output correction layer.
- DI-005: brain/memory/context/response/speech/vision/intelligence/learning/
  security deferred list.
- Engineering decision (in DI docs): don't build features AI will replace;
  build clean interfaces, replace implementations later.

### TOOLS
- T-01: audio & speech stack (SpeechRecognition, sounddevice, SciPy, NumPy,
  Whisper, PyTorch) + current audio pipeline.
- T-02: full tool/version list (Python 3.12.10, PyTorch 2.11.0 + CUDA 12.8,
  Whisper, webrtcvad-wheels, pyttsx3, pywin32, etc.).

### ISSUE_TRACKER (FRIDAY-001..014, all open unless noted)
- FRIDAY-001/002/003/005: clarification over-trigger (RC-01, ~466 tests).
- FRIDAY-004: context value leak (RC-02, CRITICAL — silent wrong-store).
- FRIDAY-006/007: context clarification/ignored/analyze failures.
- FRIDAY-008: chat-recall routing to episodes (RC-03).
- FRIDAY-009/010/011: semantic/profile/history retrieval recall (RC-04).
- FRIDAY-012/013: session-end/no-write leak (RC-05).
- FRIDAY-014: harness write-outcome logging (RC-04 unblocker, trivial).
- RC-06 was the harness-spec bug — FIXED 2026-08-05.
None of RC-01..05 has been implemented as of 2026-08-10 (verified: code still
gates before the operation split; no value-origin guard in
`memory_analyzer.py`). This is the prime next-engineering target.

---

## 12. V1 vs V2

- **V1 = current state.** Phase 1-5 architecture with keyword+deterministic
  layers + small local LLMs (3b default), 85% memory stress acceptance,
  honest tool behavior. Stable and trustworthy for filesystem/launcher within
  documented bounds.
- **V2 = Memory V2 / Phase 8** — chromadb/FAISS vector memory, semantic
  retrieval at scale, knowledge graph relationships. Libraries (chromadb,
  embedding models, rerankers) belong ONLY to Phase 8 — do not install
  earlier (ROADMAP rule 8).
- Deferred AI-replacement list: intent detection (DI-001), text
  normalization (DI-002), NLU (DI-003) — the architecture intentionally keeps
  interfaces so these swap in without restructuring.

---

## 13. ARCHITECTURAL INVARIANTS (never violate)

1. **Every phase exists because the previous one enables it.** Never start
   Phase N+1 until N's exit criteria pass.
2. **No layer may skip another layer.** Pipeline order is fixed:
   Understanding → Reasoning → Execution → Prompt → LLM → Response →
   Reflection(future) → Memory update.
3. **Every new capability enters through ExecutionManager's existing branch
   pattern** (`if reasoning.use_X`). Never bypass ExecutionManager.
4. **Every new data object is a contract dataclass.** Never pass raw dicts
   between layers.
5. **Raw user text dies at the Understanding boundary.** Nothing downstream
   receives the raw user message after Phase 2.6 (retrievers take structured
   queries; tool params are built from entities). The ONLY exceptions are the
   deterministic router rescue signals that inspect raw text
   (launch/file/web gates) — keep them as rescue-only, never primary.
6. **Brain orchestrates; Brain does not think.** Understanding never
   executes; Execution never understands language; Memory never decides;
   Reasoning never parses English.
7. **LLMs are replaceable.** Never hardcode a model name outside
   `ROLE_MODEL_MAP`. Provider abstraction must hold (ollama/OpenAI/etc.
   interchangeable).
8. **Every module owns one responsibility.** New files only when the
   responsibility genuinely doesn't exist yet.
9. **Universality rule: no keyword/hardcoded-name hacks.** The launch and
   filesystem pipelines must contain ZERO hardcoded app names or paths (this
   is verified — currently 0). App discovery is universal (catalog), path
   resolution is universal (resolver). Phase 5 fixes were deliberately
   universal (coverage-based matching, `_PIN_CATEGORY` sets, rescue signals)
   rather than app-specific.
10. **No silent fallback / no fabricated success.** A missed reference is an
    honest `not_found` carrying the user's requested string. An empty tool
    path is a synthesized failure. A launch claims "launched", never "running
    well". A list/read/locate result must reflect a real executed action.
11. **Real memory data is OFF-LIMITS to tests.** Harnesses redirect to temp
    stores; never modify `src/memory/*.json`.
12. **Permission-gating is mandatory.** Sensitive tools (write, delete,
    launch, terminal) go through PermissionGate; powerful capabilities never
    run silently.
13. **PROJECT_BIBLE.md is the source of truth.** Architecture changes update
    it FIRST, then code — never the other way around.
14. **ROADMAP.md is read-only for the agent** — it is the plan, not an
    implementation target by itself.
15. **FILESYSTEM CONTENT IS NEVER STORED.** Directory listings are dynamic
    machine state, not memories. The deterministic layer (Rule-14 store gate
    + `guard_listing_response`) is the only source of filesystem facts; the
    LLM's narration is rewritten from the real tool results whenever it
    fabricates. Memory may resolve references but never overrides a fresh
    listing, and every inspection is a fresh, independent lookup resolved to
    the real absolute path.
16. **LOCAL-PATH TRUTH.** An absolute local path may be spoken ONLY when a
    successful current `file_manager` result produced it. `guard_path_response`
    enforces this on every final reply: a web page is internet info (never a
    local path), memory is never a path source, and a "found" locate path is
    always a real-existing file/folder (`locate_reference` guarantees it).
    Never bypass or loosen this guard.

---

## 14. Rules for Future Agents (operating constraints)

1. Read section 0 (Current Situation) first. Only `python -m py_compile` for
   verification unless the user explicitly approves running a suite (newer
   filesystem suites live in the REPO ROOT — `test_navigation_flow.py`,
   `test_hierarchy_resolution.py`, `test_universal_fix.py`; older suites
   live outside the repo in `%TEMP%\opencode\` or
   `C:\Users\polis\friday_fs_suite`).
2. Do not commit without explicit user approval. Stage only intended files;
   never commit secrets.
3. Preserve Phase 1-5 behavior. Do not redesign broadly; make minimal,
   verifiable changes. Guard every loosening with the no-write regression
   class.
4. Filesystem = truth. Report only actual tool results; never summarize
   actions as done.
5. After ANY change to a touched module, run `python -m py_compile`; re-run
   the relevant suites; delete any machine fixtures created; verify machine
   state restored; update MASTER.md's change log + relevant docs.
6. Do not edit `src/memory/*.json` (real data). Do not modify ROADMAP.md.
7. When a live bug is reported, classify it (STT / intent / resolution /
   tool-vs-response — section 9) before touching code.
8. When in doubt about a phase's intent, read ROADMAP.md + PROJECT_BIBLE.md;
   when in doubt about a feature's existence, read the code, not the docs.
9. Keep the universality rule: no hardcoded app names or paths in the tool
   pipeline.
10. The next engineering target is the RC-01..RC-05 memory fix batch
    (engineering_report.md section 10 has a self-contained implementation
    prompt): FRIDAY-014 harness logging → RC-02 value-origin guard → RC-01
    operation-aware gate → RC-03 episodic routing → RC-05 session-end
    suppression.
11. **Never weaken or bypass the two deterministic guards**
    (`guard_listing_response`, `guard_path_response`) that run on every final
    reply; they are the only filesystem fact sources (invariants 15-16).
12. If a user reports a fabricated local path, that is the KI-014 class —
    already fixed (section 0, §10). Classify it (section 9) before touching
    code, and re-run `locate_guard_regression.py` (25/25) after any change.
13. If a user reports a folder-content query answered from the web, or an
    invented folder listing, that is the KI-015 class — already fixed
    (section 0, §13). Classify it (section 9) before touching code, and
    re-run `test_navigation_flow.py` (18/18) after any change. A `parameters={}`
    empty_path failure is the §12 class; a wrong-folder hit after deep
    navigation is the §11 class (both fixed; see sections 0, 8, 16).

---

## 15. Git History and Working-Tree State

Commits (newest → oldest):
- `d3d77bf5` 2026-08-08 Phase 5: stabilize application launcher and universal
  filesystem foundation
- `e5aef5cf` 2026-08-07 Complete Phase 4: Model Router architecture
- `01a5dd79` 2026-08-05 FRIDAY Memory V1 Stabilized
- `31b3fec4` 2026-08-01 Phase 2.6: Memory stabilization with cross-session
  semantic recall
- `672a2b7e` 2026-07-29 FRIDAY V1 before architecture rewrite
- `811e4550` 2026-07-28 Added brain layer with memory and context reasoning
- `93a2e733` 2026-07-26 Voice recording stabilized and debug removed
- `f42a8294` 2026-07-26 Friday Voice v1 - STT and TTS integration complete

Uncommitted working tree (2026-08-09, still uncommitted 2026-08-18):
- Modified: `docs/KNOWN_ISSUE/KI-009.md`, `docs/LAUNCHER_AUDIT_REPORT.md`,
  `docs/SESSION_LOG.md`, `src/ai/model_router.py`, `src/ai/prompt_builder.py`,
  `src/core/tool_router.py`, `src/core/brain.py` (`_final_response`),
  `src/core/response_generator.py` (`guard_listing_response` +
  `guard_path_response`),
  `src/memory/memory.json`, `src/memory/episodes.json`,
  `src/memory/memory_history.json` (runtime data),
  `src/memory/memory_fact.py`, `src/skills/file_manager.py`,
  `src/understanding/memory_analyzer.py` (Rule 14),
  `src/understanding/understanding_orchestrator.py`,
  `src/understanding/understanding_prompt.py` (filesystem-never-stored
  section)
- Untracked: `MASTER.md` (this doc), `docs/FILESYSTEM_AUDIT_REPORT.md`
  (sections 8/9/10/11/12/13), `docs/KNOWN_ISSUE/KI-012.md`,
  `src/utils/path_resolver.py`,
  plus runtime backups `src/memory/memory.json.bak-20260809-225311`,
  `src/memory/memory_history.json.bak-20260809-225311`.

Uncommitted working tree additions (2026-08-10, location-truth fix):
- `src/core/response_generator.py` (`guard_path_response`, `_spoken_paths`
  dash-safe path tokenizer, deterministic locate render),
  `src/utils/path_resolver.py` (`locate_reference` + match kinds),
  `src/skills/file_manager.py` (locate via `locate_reference`),
  `src/core/tool_router.py` (locate-ask pass-through, filesystem-noun
  signal), `src/ai/prompt_builder.py` (internet-info marker + locate render),
  `src/core/brain.py` (path guard chained in `_final_response`),
  `docs/FILESYSTEM_AUDIT_REPORT.md` (section 10), `MASTER.md` (this entry).

Uncommitted working tree additions (2026-08-16/17/18, hierarchy +
numbers + routing-drift fixes):
- `src/utils/path_resolver.py` (discovery registry, `_hierarchy_lookup`,
  `register_discovered`, `set_last_listed_scope`, `active_folder_context`,
  `context_knows`, compound spoken-number parser, `_exact_children`),
  `src/core/tool_router.py` (`_raw_filesystem_reference` single-token
  recovery, `"one"` removed from frame words, `_fs_decisive` +
  `_FS_INSIDE_TEXT_RE`/`_FS_OBJECT_NOUN_RE`/`_FS_BARE_VERB_RE` decisive
  gate, `tool_required`/`route` wiring),
  `src/skills/file_manager.py` (listing entries registered into the
  discovery registry),
  `docs/FILESYSTEM_AUDIT_REPORT.md` (sections 11/12/13),
  `test_navigation_flow.py` (18 tests), `test_hierarchy_resolution.py`
  (13 tests), `test_universal_fix.py` (6 tests), `test_scenario_b.py`,
  `test_c_lab_exam.py`, `test_fix.py`, `test_verify_fix.py` (legacy live
  navigation scripts), `MASTER.md` (this entry).

The uncommitted set is the Phase 5 stabilization work plus the 2026-08-09
filesystem contents-retrieval fix (KI-013), the 2026-08-10 round-2 router
fixes, and the 2026-08-10 local-path truth fix (KI-014). Do not commit it
without user approval.

---

## 16. Change Log

- **2026-08-18** — **Routing-drift fix (KI-015)**. A REAL production log
  (2026-08-17, 08:28–08:32) showed every folder-content query answering
  from `web_search`: "tell me whats inside the exam folder" →
  `Need Tools: False` + `web_search -> success` → hallucinated "The 'exam'
  folder contains one entry: test.py" (real contents: ch1_function,
  ch2_string, ch3_array, ch4_structure, exam_notes.txt, test.txt); "the
  lab 3 folder" → web rate-limit failure; "its inside the c lab folder in
  my c drive please check" → invented "exam1 (file), exam2 (file)".
  Root cause (proven, not guessed): Understanding classified the turns
  `category=search / goal=search_web / capability=search`, and
  `_CAPABILITY_VARIANTS["search"]="web"` canonically resolved them to the
  web capability — `tool_required()`'s `fs_query` gate was blocked by
  `goal not in _NON_FILE_GOALS`, the `route()` fs rescue by `tool_cap !=
  "web"`, and the web branch fired on `is_web_cap` with no tool flags set.
  Fix (universal, no hardcoded names): new decisive raw-text gate
  `_fs_decisive()` in `tool_router.py` — (1) inside/contents phrase +
  filesystem noun ("whats inside the exam folder", "its inside the c lab
  folder in my c drive"), (2) list/show/read + filesystem noun ("list my
  downloads", "read the first.py file"), (3) verb/inside phrase with a
  SESSION-VERIFIED object via new `context_knows()` in `path_resolver.py`
  (registry/context chain only, never a global disk search — "read
  first.py", "whats inside the examples" after being shown). `route()`
  pins `tool_cap="automation"` and forces `use_web=False;
  goal_search_web=False` (same pattern as the launch/locate rescues);
  `tool_required()` enters the tool path. Genuine web asks are never
  hijacked: "whats inside a black hole", "whats in the news", "show me
  pictures", "read me a story", "list my books", weather, "search the web
  for X" all stay on `web_search`; "open spotify" → app_launcher unchanged.
  Results: `test_navigation_flow` 18/18 (5 new routing regressions, no new
  files), `test_hierarchy_resolution` 13/13, `test_universal_fix` 6/6,
  legacy live scripts PASS; live simulation with the exact log flags
  (`Need Tools: False`, `Need Web: False`, `category=search`) →
  `tool_required=True`, routes `['file_manager']`. Docs:
  FILESYSTEM_AUDIT_REPORT section 13.
- **2026-08-17** — **empty_path + spoken-number fix (router reference
  recovery)**. "tell me whats inside the examples"/"chapter one folder"
  failed with `parameters={}` `empty_path` even though parent-context
  propagation was proven intact. Root causes: (1) `_raw_filesystem_reference`
  dropped any reference with fewer than 2 surviving tokens (`len(keep) < 2`)
  — single-word folder names ("examples", "exam") died whenever the small
  Understanding model emitted `parameters={}`; (2) "one" was a
  `_FS_FRAME_WORDS` member, so "chapter one" stripped to nothing. Fix:
  single surviving token is now a valid recovery (junk words still
  degrade to an honest not_found naming the word); "one" removed from the
  frame words; compound spoken numbers parsed (`_canonical_tokens` +
  conservative `_parse_number_run`: "chapter twenty one"→21, "one hundred
  twenty two"→122, "two hundred five"→205, "one thousand two hundred"→1200;
  "twenty twenty"/"three zero" stay literal) applied in `_tokens_match`
  and `_norm_key`; `_exact_child` → `_exact_children` with same-parent
  canonical ambiguity in `_hierarchy_lookup` tier 2 ("chapter 1" +
  "chapter one" in one parent = ambiguous; with chapter 10/11 present,
  "chapter one" deterministically → chapter 1). Results:
  `test_navigation_flow` 13/13 (unique uuid fixture roots so real folders
  can never shadow them), `test_hierarchy_resolution` 13/13,
  `test_universal_fix` 6/6, legacy scripts PASS; live repro on the real
  `C:\python revision` tree PASS. Docs: FILESYSTEM_AUDIT_REPORT section 12.
- **2026-08-16/17** — **Session hierarchy fix (deep-navigation resolution)**.
  Follow-up asks after multi-level navigation ("python revision" →
  "chapter 1" → "whats inside the examples") hit the wrong folder: the old
  Section 5b relative resolution was broken and the deterministic first-hit
  global fuzzy search picked stale leftover folders (`C:\Users\polis\
  other_exam_final` answered "examples"). Fix: `path_resolver.py` gains a
  bounded session discovery registry (`_DiscoveryRecord`, 512, oldest
  evicted) fed by `register_discovered()` (read/locate) and
  `set_last_listed_scope(path, entries)` (successful lists); session context
  chain via `active_folder_context`/`clear_active_folder_context` (clearing
  also empties the registry); `_hierarchy_lookup` (exact children of the
  last-listed folder → context chain → single verified record → relative
  path against chain bases, global search only as fall-through) replaces the
  broken Section 5b in both `resolve_reference` and `locate_reference`;
  `file_manager._list`/`_read`/`_locate` register every verified object.
  Results: `test_hierarchy_resolution` 13/13, `test_navigation_flow` 13/13,
  `test_universal_fix` 6/6, legacy scripts PASS. Docs: FILESYSTEM_AUDIT_REPORT
  section 11.
- **2026-08-10** — **Universal local-path truth fix (KI-014 / locate guard)**.
  Closes the last fabrication class: FRIDAY speaking a confident absolute
  local path no current tool result produced (web info or memory became
  local paths; a found path was "improved" into a non-existent one). User
  session log evidence: `srczip` → wrong-kind `C:\project\srczip`, python
  installer → invented `C:\project\python\bin\python.exe`, AC3 → invented
  `C:\Games\Ubisoft\...` from a web result. Universal fix, no hardcoded
  names: `locate_reference()` (real-existing-only locate with exact/
  normalized/fuzzy match kinds + bounded multi-candidates),
  `file_manager._locate` (locate before the not_found gate, richer data),
  `tool_router` (raw-text filesystem-noun locate signal + `tool_required`
  locate-ask pass-through so AC3-style asks reach `file_manager`, never
  web), `prompt_builder` (web results labeled internet info; locate render
  shows match kind + every real candidate; path-truth instruction),
  `response_generator.guard_path_response` (universal: an absolute local
  path may be spoken ONLY when a successful current `file_manager` result
  produced it; locate replies regenerated deterministically; web-only locate
  asks get an honest "not on this computer"), wired in `brain._final_response`
  after `guard_listing_response`. Results: `locate_guard_regression` 25/25,
  manual weather (Siliguri→web only) + real-file locate (srczip→4 real
  matches, python installer→real `Downloads\Python 3.12 Installer.exe`,
  AC3→honest not-found) PASS; all prior suites re-passed (smoke 13/13,
  guard 33/33, fs14 37/37, convo50 60/60, p9 128/128+6/6, fsq_live 60/60,
  fsq30 30/30). Docs: FILESYSTEM_AUDIT_REPORT section 10.
- **2026-08-10** — **Universal contents-retrieval fix round 2 (FSQ follow-up)**.
  A 30-convo live suite on real user folders (`fsq30_convo`) found 5 wrong
  answers that Round 1 (stale-memory echoes) had not fixed, in two new
  router-level classes: (1) "what is inside my downloads/desktop folder"
  arrives `capability=device` and `tool_required()` dropped it before the
  raw-text FS rescue ran → no tool fired, evasive "no information" reply;
  (2) `what's` tokenized to `what s` and the stray `s` poisoned the
  recovered reference ("s python project c drive"), silently falling back
  to the structured `"c drive"` → listed the drive ROOT. Fix: fs-query gate
  now overrides the device short-circuit in `tool_required()`; apostrophes
  are merged in `_raw_filesystem_reference`. Also this session: response
  guard extended to empty/only-one claims, denial language, and evasive
  no-info replies (17/17 → 33/33), and listings are folder-bound in the
  prompt. Results: `fsq30_convo` 30/30, `fsq_live_suite` 60/60, guard
  33/33, Rule-14 37/37, p9 128/128 + 6/6, convo50 60/60; real memory 38
  facts / 0 listing facts. Docs: FILESYSTEM_AUDIT_REPORT section 9.
- **2026-08-09** — **Filesystem contents-retrieval fix (KI-013)**. Root
  cause: directory listings were written to long-term memory as durable
  facts (folder cross-contamination + stale answers). Fix: Rule 14 store
  gate in `memory_analyzer.py`, "FILESYSTEM CONTENT IS NEVER STORED" prompt
  contract in `understanding_prompt.py`, and the deterministic filesystem
  answer guard `guard_listing_response()` in `response_generator.py` wired
  as `brain._final_response`. Results: `fsq_live_suite` 60/60, guard unit
  17/17, Rule-14 gate 37/37, p9 128/128 + 6/6, convo50 60/60; real
  `memory.json` shows 0 listing facts. Docs: FILESYSTEM_AUDIT_REPORT section
  8.
- **2026-08-09** — MASTER.md created from full repository inspection
  (reconstructed pipeline, invariants, issues, test history, Phase 5
  details; documented empty README/requirements and RESEARCH placeholder).
  Live-voice validation (5 phrases) still pending user recordings.
- **2026-08-08** — Phase 5 stabilization (resolver + router + filesystem
  fixes; see FILESYSTEM_AUDIT_REPORT); KI-010/011/012 documented.
- **2026-08-07** — Phase 5 launcher stabilization (LAUNCHER_AUDIT_REPORT);
  Phase 4 committed.
- **2026-08-05** — Memory V1 stabilized; 5000-test stress run (85.5%);
  engineering report + issue tracker written.
- **2026-08-01** — Phase 2.6 memory stabilization committed.
- **2026-07-29** — "FRIDAY V1 before architecture rewrite" checkpoint.
- **2026-07-28** — Brain layer architecture foundation (CHANGELOG/SESSION_LOG).
- **2026-07-26** — Friday Voice v1 (STT + TTS integration).
