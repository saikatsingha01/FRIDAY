# FRIDAY — Updated Master Roadmap
## Including Self-Evolution Framework Placement

---

# The Governing Rule

Every phase exists because the previous one enables it.
Self-evolution is the most extreme example of this rule.
It requires every other cognitive system to exist first.
Building it before those systems exist would be dangerous, not impressive.

---

# Phase 1 — Foundation ✅ COMPLETE

Project structure, LLM interface, speech pipeline, prompt builder,
contracts, basic memory storage, modular skills, configuration.

**Outcome:** A stable skeleton. FRIDAY became a modular software project
instead of a single Python script.

---

# Phase 2 — Cognitive Core (Current)

The most important phase. Everything after depends on it.

## Phase 2.1 — Understanding Layer ✅
Single LLM call → structured LanguageUnderstanding contract.

## Phase 2.2 — Reasoning Engine ✅
Reasoning decides what systems are needed. Never executes them.

## Phase 2.3 — Execution Layer ✅
ExecutionManager coordinates systems through `if reasoning.use_X` branches.
New capabilities in every future phase are added as new branches here.
Never as a bypass around this layer.

## Phase 2.4 — Prompt Architecture ✅
LLM receives structured context, not raw application state.

## Phase 2.5 — Memory Foundation ⚠ Partial
Semantic, episodic, context stores exist.
Conflict resolver, history, evaluator all implemented.
Storage and retrieval both partially working.

## Phase 2.6 — Memory Stabilization 🚧 ACTIVE NOW

**The fix (5 files, ~60 lines):**

1. `understanding/understanding_prompt.py`
   — Add `memory_operation` and `canonical_fact` to the JSON schema
   — Add definitions: extraction rules, examples, null conditions

2. `memory/memory_fact.py` — NEW (only justified new file in current phase)
   — MemoryFact dataclass: `operation`, `canonical_fact`
   — Owned by Memory layer. Keeps LanguageUnderstanding clean.

3. `understanding/understanding_orchestrator.py`
   — Build MemoryFact from raw_understanding after LLM call
   — Return `(understanding, memory_fact)` tuple instead of single object

4. `core/brain.py`
   — Unpack tuple from analyze()
   — Pass `memory_fact` to `process_memory()` instead of `user_message`
   — Memory status ("stored") → LLM generates natural confirmation response

5. `memory/memory_decision.py`
   — Accept MemoryFact, never raw text
   — Return status string ("stored") not English dialogue
   — MemoryDecision decides what happened. LLM decides how to phrase it.

**Zero changes to:**
memory_manager, memory_conflict_resolver, memory_evaluator,
memory_validator, episode_manager, memory_history, language_understanding.py

**Exit criteria (from Handoff doc — all five must pass):**
- Test A: "Remember my favorite game is Sekiro" → stored cleanly
- Test B: "My favorite game is Ghost of Tsushima now" → updated, Sekiro archived
- Test C: "What is my favorite game?" → Ghost of Tsushima
- Test D: "What was my favorite game before?" → Sekiro
- Test E: "What GPU does my laptop have?" → RTX 4050, no unrelated memories

Do not leave this phase until all five pass.

## Phase 2.7 — Retrieval-Side Leak Fix

**What:** Replace `retrieve_relevant_memories(user_message)` with structured query objects.

**Where:** `memory/memory_query_builder.py` (already exists as empty stub — fill it).
`execution/execution_manager.py` → pass `MemoryQuery` built from
`understanding.semantic` + `understanding.memory` instead of raw string.

**New file needed:** None. `memory_query_builder.py` already exists.
Build `MemoryQuery` dataclass inside it. Symmetric to `MemoryFact`.

**What unlocks:** Intent-aware retrieval, category-aware retrieval,
entity-aware retrieval, "before" questions answered from episodes,
context-aware ranked memory in prompts.

## Phase 2.8 — Semantic Triage (Fast Path)

**What:** Cheap embedding check at the top of Understanding to skip the full
LLM call for trivial messages (greetings, farewells, small talk).

**Where:** New small file `understanding/triage.py`.
Called as first line of `understanding_orchestrator.analyze()`.
If triage returns a category → build lightweight LanguageUnderstanding, return early.
Full LLM call only runs for real requests.

**Technology:** `ollama.embeddings(model="nomic-embed-text", prompt=text)`
Single forward pass. Not generative. Fast.
Semantic similarity against a small set of exemplar phrases per category.
Threshold deliberately high (0.82+) — false negative is cheap, false positive loses a real request.

**New file:** `understanding/triage.py` — justified because triage is a
distinct responsibility from Understanding. It gates Understanding.
It should never live inside the orchestrator body.

**What unlocks:** FRIDAY stops calling the large model for "hello".
Foundation for model routing (Phase 4) — triage already classifies social vs real.

**Why before Phase 3:** Planner depends on Understanding quality.
Triage must be stable and not interfering with real requests
before Planning trusts Understanding's output.

---

# Phase 3 — Planning Engine ✅ COMPLETE

**What:** FRIDAY stops reacting turn-by-turn and starts accomplishing goals.
Complex tasks get decomposed into steps. Execution becomes a graph, not a line.

**Depends on:** Reliable memory (2.6, 2.7) — plans need to recall project history.
Clean Understanding (2.8) — triage must not intercept planning requests.

**Where in existing architecture:**
- `contracts/planner.py` already exists as empty stub — fill it with
  `PlannerInput` and `ExecutionPlan` dataclasses.
- `execution/execution_manager.py` gains a planning branch:
  `if reasoning.use_planning: result.plan = planner.plan(understanding, reasoning)`
- `core/brain.py` gains a planning path alongside the conversation path.
  This is the one structural change to brain.py that must happen here:
  brain.py evolves from a linear sequence into a dispatcher.
  Conversation path (current) stays untouched.
  Planning path routes through Planner → multi-step Execution loop.

**New files needed:** `core/planner.py` — justified because Planning is
a genuinely new cognitive responsibility that doesn't exist anywhere yet.

**What unlocks:** Multi-step task execution, project continuity,
"continue where we left off", decomposing large user goals into steps.
Also unlocks Reflection (Phase 5) which needs plans to evaluate against.

---

# Phase 4 — Model Router ✅ COMPLETE

**What:** FRIDAY selects which local model to use based on task type.
User never selects manually. Architecture decides.

**Depends on:** Stable Understanding (so `category` output is consistent,
not noisy). Multiple meaningful task types in the pipeline.
Triage (2.8) already classified social messages — router builds on that.

**Where in existing architecture:**
- New file `ai/model_router.py` — justified because routing is a distinct
  infrastructure responsibility belonging to the AI layer, not core or memory.
- Called from `core/brain.py` between Prompt (step 6) and LLM (step 7).
- `ai/llm_interface.py` already accepts model parameter — no change needed there.

**Design:** Deterministic lookup table. No LLM call. No keyword matching.
`understanding.semantic.category` → model name.
Python dict. Fast. Testable. Replaceable.

```
social          → llama3.2:1b   (fast, trivial)
general         → llama3.2:3b   (default)
preference      → llama3.2:3b
hardware        → llama3.2:3b
science         → llama3.1:8b
planning        → llama3.1:8b
programming     → qwen2.5-coder:7b
```

**Important:** `category` field in the Understanding prompt must be a
closed enum before this phase — not free text. The LLM must output
one of a defined list, not invent new category names, or routing silently
falls back to default every time.

**What unlocks:** Efficient resource use. Coding model for code.
Fast model for conversation. Large model only when actually needed.
Foundation for learning-based routing in Phase 7 (which model actually
produced better results for which category).

---

# Phase 5 — Tool Intelligence

**What:** FRIDAY selects and executes tools based on structured reasoning.
Not keyword matching.

**Depends on:** Stable Reasoning output (so `use_tools: True` is reliable).
Model Router (Phase 4) — tools and model selection are often co-decisions.

**Where in existing architecture:**
- `core/tool_router.py` already exists — replace `route_tool(user_message)`
  with `route_tool(understanding, reasoning)` in brain.py.
- `execution/execution_manager.py` `if reasoning.use_tools` branch — currently `pass`.
  Fill it with actual tool dispatch.
- `skills/skill_registry.py` and `skills/skill_loader.py` already exist.
  New tools register here. No new architecture needed.

**New tools to add here (not new architecture, just new skill files):**
- Web search
- File manager (file_manager/ already exists and is scaffolded)
- Terminal (permission-gated)
- Application launcher

**What unlocks:** FRIDAY can actually do things, not just answer questions.
Also unlocks Reflection being useful — Reflection can now evaluate
"was that the right tool?" not just "was that a good answer?"

---

# Phase 6 — Reflection Engine

**What:** After significant responses, FRIDAY evaluates her own work.
Not self-awareness. Quality control.

**Depends on:** Planning (Phase 3) — Reflection evaluates plans against outcomes.
Tool Intelligence (Phase 5) — Reflection evaluates tool choices.
Without these, Reflection only evaluates simple Q&A (low value).

**Where in existing architecture:**
- `contracts/reflection.py` already exists as empty stub — fill it.
  `ReflectionInput`: understanding + execution + response + outcome signals.
  `ReflectionResult`: quality score, what worked, what failed, suggested adjustments.
- New execution branch in `execution_manager.py`:
  `if reasoning.use_reflection: result.reflection = reflection_engine.reflect(...)`
- Reflection results feed into `episode_manager.add_episode()` —
  significant reflection events become episodic memories.
  No new files needed for this connection.

**New file:** `core/reflection_engine.py` — justified, genuinely new cognitive
responsibility. Does not exist anywhere in current codebase.

**What unlocks:** FRIDAY starts accumulating engineering experience about herself.
Feeds directly into Learning (Phase 7) and Self-Evolution (Phase 9).
Without Reflection, Learning has nothing to learn from.
Without Reflection, Self-Evolution has no evidence to act on.

---

# Phase 7 — Learning Engine

**What:** FRIDAY improves decisions based on patterns from Reflection history.
Not model retraining. Improving architectural decisions.

**Depends on:** Reflection (Phase 6) — Learning reads from Reflection history.
Enough runtime data — Learning needs hundreds of Reflection episodes to find
real patterns, not noise. This phase should not start too early.

**Where in existing architecture:**
- `memory/memory_consolidator.py` already exists (currently stub) —
  consolidation logic belongs here. Expand it.
- New background worker concept introduced here but kept minimal:
  A function called periodically (not a daemon thread yet) that reads
  Reflection episodes and proposes memory weight adjustments.
  Lives in `memory/memory_consolidator.py` to avoid new files.
- Model routing table (Phase 4) gets its first data-driven update here:
  Which model actually produced better Reflection scores for which category?
  Routing table adjusts.

**What unlocks:** Retrieval gets better over time without code changes.
Model routing gets better over time without code changes.
Foundation for Self-Evolution (Phase 9) — Learning produces the
"accumulated engineering experience" that Self-Evolution reasons over.

---

# Phase 8 — Knowledge Graph

**What:** Facts become connected nodes with relationships instead of
isolated JSON entries. "My laptop has RTX 4050" connects to
"FRIDAY project" connects to "Python" connects to "Saikat".

**Depends on:** Stable semantic memory with clean canonical facts (2.6).
Learning (Phase 7) — the graph should be informed by which connections
proved useful, not just which ones exist.
Memory Consolidator already started (Phase 7 expanded it).

**Where in existing architecture:**
- `memory/memory_consolidator.py` becomes the bridge between flat JSON
  memory and the future graph. It already groups by category.
  Extend it to extract relationships using a small LLM call.
- Storage backend evolves. The rest of the architecture
  (MemoryFact, MemoryQuery, conflict resolver) stays unchanged.
  Only what's behind memory_manager.py changes.
- No new public-facing files. The graph is an implementation detail
  of the memory layer, hidden behind the existing interface.

**What unlocks:** Reasoning over relationships instead of keyword matching.
"What projects use my laptop?" becomes answerable.
Foundation for the Self-Evolution system (Phase 9) which needs to
reason about relationships between its own modules and their interactions.

### Dependencies & Core Libraries

These libraries belong only in Phase 8. Do not install them earlier.

**chromadb** (or FAISS as alternative)
Purpose: Vector database. Replaces or augments flat JSON memory storage.
Enables semantic retrieval by embedding proximity rather than keyword overlap.
Required for Memory V2 — embedding-based search over thousands of memories.

**Embedding models** (via `ollama` — already integrated)
Purpose: Semantic search. Meaning-based retrieval.
The existing `nomic-embed-text` model already handles triage embeddings.
In Phase 8 it is extended to embed every stored memory fact for vector
similarity search. No new dependency if using Ollama. New dependency only
if switching to a separate embedding service.

**Rerankers** (e.g. `sentence-transformers` with cross-encoder models)
Purpose: Improve retrieval accuracy after initial vector search.
First-pass retrieval returns candidates. Reranker re-scores them by
relevance to the specific query. Install only when retrieval quality
requires this level of precision.

These libraries belong only in Memory V2 / Phase 8 and must not be
introduced in earlier phases. Phases 2.6 and 2.7 use keyword + category
scoring which is sufficient for their scope.

---

# Phase 9 — Autonomous Self-Evolution Framework

**Placed here because it requires everything above:**
- Reliable memory (2.6, 2.7) — evidence must be stored and retrieved correctly
- Planning (3) — evolution proposals are multi-step plans
- Model Router (4) — the right model must handle code generation vs reasoning
- Tool Intelligence (5) — sandboxed execution requires tool-level file/terminal access
- Reflection (6) — evidence collection is Reflection output accumulated over time
- Learning (7) — "engineering experience" is what Learning accumulated
- Knowledge Graph (8) — reasoning about module relationships requires graph structure

**Without all of these in place, Self-Evolution would be:**
- Operating on corrupted evidence (no reliable memory)
- Generating unfalsifiable proposals (no planning to structure them)
- Using the wrong model for code generation (no routing)
- Unable to execute in isolation (no tool access)
- With nothing meaningful to evaluate against (no reflection history)
- With no accumulated experience to reason from (no learning)
- Unable to understand module dependencies (no knowledge graph)

**This is why it is Phase 9, not Phase 4.**

---

## What Self-Evolution Needs — Mapped to Existing Architecture

The entire Self-Evolution capability is built inside existing layers.
No new top-level package. No new architectural tier.
It is a set of capabilities added to layers that already exist.

---

### Evidence Collection — Lives in Reflection (Phase 6, extended)

`core/reflection_engine.py` already evaluates individual responses.
Extend it to aggregate patterns over time:

```
Single reflection: "Memory retrieval failed this turn."
              ↓
Aggregated pattern: "Memory retrieval has failed 17 times
                    under similar conditions."
```

Aggregated patterns are stored as a special category in episodic memory
via `episode_manager.add_episode()` — no new storage system needed.
Pattern detection lives in `memory/memory_consolidator.py`
(already exists, already groups by category — extend it to group by failure type).

---

### Root Cause Investigation — Lives in Reasoning (Phase 3, extended)

When a pattern crosses a configurable evidence threshold,
`core/reasoning_engine.py` activates an investigation mode.
This is a new `ReasoningResult` field: `use_self_evolution: bool`.

The investigation produces a structured problem report using the
LLM (routed to the largest available model via Phase 4 routing).
The report is stored as an episodic memory.

No new file. New reasoning mode in existing `reasoning_engine.py`.

---

### Engineering Proposal Generation — Lives in Planning (Phase 3, extended)

`core/planner.py` (created in Phase 3) gains a new plan type:
`EvolutionPlan` alongside regular `ExecutionPlan`.

An EvolutionPlan contains:
- Problem description
- Evidence summary
- Root cause
- Alternative solutions considered
- Chosen solution
- Files to be modified
- Expected improvement metrics
- Estimated risks
- Rollback strategy
- Confidence score

This lives inside `contracts/planner.py` as a new dataclass.
No new files. The Planner already produces structured plans —
this is a new plan shape, not a new planner.

---

### Sandboxed Code Generation — Lives in Tool Intelligence (Phase 5, extended)

The sandbox is a tool. FRIDAY's tool system (Phase 5) handles:
- File system access (cloned repo directory)
- Terminal execution (isolated environment)
- Test runner invocation

The sandbox itself is not a new cognitive layer.
It is a permission-gated tool set that the Evolution plan executes through.

Sandbox isolation is enforced by the permission system (Design Doc 4):
the sandbox tools have write access only to the cloned directory,
never to the production source tree.

No new cognitive files. New tool registrations in `skills/`.

---

### Automated Verification Pipeline — Lives in Tool Intelligence (Phase 5, extended)

Verification stages (syntax, linting, static analysis, imports) are
sequential tool calls inside the EvolutionPlan's execution graph.
Each stage is a skill registered in `skills/skill_registry.py`.

If any verification stage returns failure → plan execution halts.
This is plan-level flow control, already supported by the Planner.

---

### Behavioral Comparison — Lives in Reflection (Phase 6, extended)

Comparing old vs new behavior is a Reflection task.
`core/reflection_engine.py` already has the shape for evaluating
a response against expected outcomes.
Extend it with a comparison mode: given two execution results
(old system, new system) produce a `ComparisonResult`.

Stored in episodic memory as evidence for the post-deployment review.

---

### Human Approval Layer — Lives in brain.py response path

When an EvolutionPlan is complete and verified, it does not execute.
It surfaces to the user via the normal response pipeline.

brain.py gets one new branch (parallel to the existing memory_result branch):

```python
if evolution_result is not None:
    return {
        "understanding": understanding,
        "reasoning": reasoning,
        "response": format_evolution_report(evolution_result),
    }
```

`format_evolution_report()` lives in `core/response_generator.py`
(already exists, already has formatting branches).

The user reads the report in normal conversation.
Replies "yes" → EvolutionPlan executes through the tool system.
Replies "no" → plan archived as rejected proposal in episodic memory.

---

### Safe Deployment — Lives in Tool Intelligence (Phase 5, extended)

Deployment is a sequence of tool calls in the approved EvolutionPlan:
1. `backup_tool` → snapshot production files
2. `file_write_tool` → apply changes to production
3. `restart_tool` → reload affected modules
4. `health_check_tool` → verify startup

Automatic rollback is the failure branch of this tool sequence.
If `health_check_tool` fails → `restore_tool` runs the snapshot.

These are all skills. No new architecture.

---

### Post-Deployment Reflection — Lives in Reflection (Phase 6, extended)

Same Reflection engine, new trigger: post-deployment monitoring.
Runs for N conversations after deployment.
Compares expected improvement metrics against actual metrics.
Stores outcome (success or failure) in episodic memory.
This outcome feeds into Learning (Phase 7) for future proposal quality.

---

## Summary: New Files Added for Self-Evolution

**Zero new top-level files.**

All Self-Evolution capability lives in extensions to:

| Existing file | Extended with |
|---|---|
| `core/reflection_engine.py` | Pattern aggregation, behavioral comparison, post-deployment monitoring |
| `core/reasoning_engine.py` | Investigation mode, `use_self_evolution` flag |
| `core/planner.py` | EvolutionPlan dataclass alongside ExecutionPlan |
| `contracts/planner.py` | EvolutionPlan contract |
| `core/brain.py` | evolution_result branch in response path |
| `core/response_generator.py` | `format_evolution_report()` function |
| `memory/memory_consolidator.py` | Pattern detection, failure aggregation |
| `skills/` | Sandbox tools, verification tools, deployment tools registered here |

The cognitive pipeline does not change shape.
Self-Evolution uses the same pipeline that handles user requests,
because FRIDAY treats her own code with the same engineering discipline
as any other problem.

---

# Phase 10 — Vision and Perception System

**Purpose:**
Vision becomes a complete perception layer that fuses with Memory,
Planning, and the Agent Architecture. FRIDAY sees and understands
her environment.

## Desktop Vision
- Read windows, recognize application states, identify UI elements,
  icons, buttons, loading states, errors, progress bars
- UI Automation API preferred over image matching wherever available
- OCR for any on-screen text

## Camera Vision
- Object recognition, room understanding, furniture, books, devices
- Handwritten text recognition
- Gesture recognition
- Facial expression recognition (permission-gated)
- Scene understanding — relationships between objects, movement tracking

## Visual Memory
- Remember previously seen environments
- Associate locations with stored memories
- Track recurring objects and scenes

## Fusion with Memory and Planning
Visual observations feed into semantic memory ("my desk setup has changed"),
episodic memory ("on August 2 the user was working in a dark room"),
and planning ("the compile failed — I can see the error in the terminal").

## Architecture
- `skills/vision/` — new skills package: desktop_vision, camera_vision, ocr
- Vision Agent (Phase 9a) handles all vision processing
- Vision results enter the PromptBuilder's context section

### Dependencies & Core Libraries

Install these only when the specific perception capability is being
implemented. Do not install the full list at phase start.

**opencv-python**
Purpose: Computer vision foundation. Image processing. Object detection.
Frame analysis for desktop and camera vision.
Install when desktop vision or camera vision implementation begins.

**pillow**
Purpose: Image manipulation. Image loading and conversion. Drawing overlays.
Processing screen capture assets.
Install alongside opencv-python.

**mss**
Purpose: Fast cross-platform screen capture. Minimal CPU overhead.
Screen understanding foundation.
Install when desktop vision implementation begins.

**easyocr** (preferred) or **pytesseract** (alternative)
Purpose: OCR — reading text from screen captures, documents, whiteboards,
handwritten notes.
Install when OCR capability is implemented.
Choose one based on accuracy vs speed requirements at that time.

**pdfplumber**
Purpose: PDF text extraction. Reading documents FRIDAY is asked to analyze.
Install when document understanding is implemented.

**pymupdf**
Purpose: Advanced PDF parsing. Handles complex layouts, embedded images,
forms. Install when pdfplumber proves insufficient.

**python-docx**
Purpose: Word document understanding. Reading .docx files the user is
working on. Install when document understanding is implemented.

**openpyxl**
Purpose: Spreadsheet understanding. Reading .xlsx files.
Install when spreadsheet awareness is implemented.

Additional perception models (depth estimation, gesture recognition,
facial expression) should be installed only when that specific capability
is being built. Do not install speculatively.

---

# Phase 11 — Complete Device Control Framework

**Purpose:**
FRIDAY gains full Operating System Interaction capability.
Not simple macro playback. Structured workflow execution with awareness
of application state.

## Windows Control
Launch, close, switch, resize, rearrange applications.
Multi-monitor awareness. Virtual desktop management.
Taskbar and system tray interaction. Notification management.
Clipboard management. File explorer navigation including selection,
context menus, drag and drop. Keyboard shortcuts, mouse automation, hotkeys.
Windows Accessibility APIs for reliable UI element targeting.

## System Control
Shutdown, restart, sleep, lock. Brightness, volume, audio device switching.
WiFi, Bluetooth, network settings. Battery awareness.
Performance mode and power profile management.

## Application Awareness
FRIDAY does not blindly click. She knows which application is open,
which window is active, which UI elements exist, and whether an action
succeeded or failed. UI Automation API is the primary interface —
image matching is a fallback only.

## Workflow Execution
FRIDAY executes complete workflows, not individual commands.

Example:
Open VS Code → open project → compile → run tests → read terminal →
fix error → commit → push → open browser → research → return →
continue coding.

This is expressed as an ExecutionPlan (Phase 3), executed by the
Desktop Agent, supervised by the Reflection Agent.

## Architecture
- `skills/desktop/` — new skills package: window_manager, system_control,
  app_launcher, keyboard_mouse, file_explorer, accessibility_api
- Desktop Agent handles coordination
- All actions are permission-gated and logged

### Dependencies & Core Libraries

**pywin32**
Purpose: Windows API access. Notifications. COM automation.
Windows Services integration. OS-level integration for the
Trusted Device Agent. Window management via Windows accessibility APIs.
Install when Windows Control implementation begins.
Required for reliable UI Automation over image matching.

**watchdog**
Purpose: File system monitoring. Folder watching. Background event detection.
Automatic workflow triggers when files change.
Required for the "watch this folder" and "monitor my downloads" capabilities.
Install when background file monitoring is implemented.

Additional automation libraries should only be added when a specific
automation capability genuinely requires them and no existing dependency
already provides that functionality.

---

# Phase 12 — Browser Intelligence

**Purpose:**
Complete browser reasoning. Not just opening URLs.
Understanding page structure, extracting information, performing
multi-step research tasks, continuing interrupted browsing sessions.

## Capabilities
Navigate websites. Understand page structure semantically.
Fill forms. Read tables and extract data. Download and upload files.
Switch tabs, bookmark pages. Continue interrupted sessions.
Perform research and comparison tasks. Read documentation and
summarize results.

## Architecture
- `skills/browser/` — new skills package
- Browser Agent handles execution
- Page content enters the retrieval pipeline alongside memory
- Research results stored as episodic memory for future reference

---

# Phase 13 — Game Interaction System

**Purpose:**
FRIDAY interacts with local, offline, single-player games.
Not competitive or online gaming. Autonomous interaction with software
that happens to be a game. Uses the same perception-planning-control
architecture as all other device control.

## Scope
Keyboard input, mouse movement, camera control, inventory interaction,
menu navigation, map navigation, quest progress tracking.

## Examples
Minecraft (automated building, resource gathering),
Sekiro (training scenario automation),
Ghost of Tsushima (exploration, objective tracking),
offline RPGs and sandbox games.

## Architecture
- `skills/game/` — new skills package
- Uses Desktop Vision (Phase 10) for perception
- Uses Desktop Control (Phase 11) for input
- Game state stored in episodic memory

---

# Phase 14 — Mobile Device Integration

**Purpose:**
FRIDAY extends to Android devices. Controls phone remotely via ADB or
wireless. Mirrors phone state. Reads notifications. Manages communication.

## Capabilities
Read and reply to notifications and messages. Launch apps. Control media.
Mirror phone state. Transfer files. Answer and reject calls.
Read SMS. Remote control.

## Architecture
- `skills/mobile/` — new skills package using ADB integration
- Mobile Agent handles coordination
- Phone state enters ContextUnderstanding

---

# Phase 15 — Multimodal Reasoning

**Purpose:**
FRIDAY reasons jointly across all modalities simultaneously rather than
each operating independently.

Voice + Vision + Memory + Desktop state + Browser state + Device state
+ Location + Context all fuse into one unified understanding before
reasoning begins.

## Architecture
- `understanding/understanding_orchestrator.py` evolves to collect signals
  from all active modalities before calling the Understanding LLM
- A unified perceptual context object replaces the current text-only input
- The Understanding LLM receives this fused context as structured input

## What it unlocks
FRIDAY understanding "the user just opened the file they mentioned
yesterday and looks frustrated" without being told explicitly.
Proactive assistance based on observed state rather than explicit requests.

---

# Phase 16 — Proactive Intelligence

**Purpose:**
FRIDAY notices patterns and acts without being asked.
Not intrusive. Proactive only when confidence is high and the action
is clearly beneficial.

## Capabilities
- Detect repeated tasks and suggest automation
- Surface forgotten reminders based on context
- Notice project deadlines from episodic memory
- Identify coding patterns and suggest improvements
- Recognize when the user is struggling before they ask for help
- Suggest study plans when exam proximity is detected in memory

## Architecture
- Proactive triggers stored in `memory/memory_consolidator.py` as
  pattern-based rules built from Learning history
- Proactive Agent monitors continuously at lowest priority
- All proactive suggestions surface through the normal Conversation Agent
  — never as interruptions

---

# Phase 17 — Always-On Wake Word System

**Purpose:**
Ultra-low-power always-on listening. Hands-free activation.
FRIDAY is available without requiring manual launch.

## Requirements
Separate lightweight wake model (not the main LLM).
Custom wake words configurable by user.
Conversation activation on detection. Conversation timeout.
Interrupt handling — new wake word during active conversation suspends
current task, addresses new request, resumes.
False activation protection. Sleep mode. Independent from the main
cognitive pipeline.

## Architecture
- `speech/wake_detector.py` — NEW. Runs in a separate low-priority thread.
- `speech/voice_detector.py` — existing, extended with wake integration.
- Wake model independent of Whisper and the main LLM.

---

# Phase 18 — Complete Ecosystem

**Purpose:**
One FRIDAY. One identity. One memory. Multiple devices.
Seamless continuity across all environments.

## Components

**Desktop Companion** — Primary interface. Full capability. All phases available.

**Phone Companion** — Android app. Shares memory. Shares identity.
Voice-first. Handles mobile-specific tasks. Continues desktop tasks when
user leaves.

**Browser Extension** — Lightweight browser presence. Research integration.
Form assistance. Page summarization. Connects to desktop FRIDAY via local API.

**Smart Home Integration** — Light control, temperature, media, security,
routines. FRIDAY as the home operating system.

**Smart Displays** — Dashboard companion. Visual summaries. Project status.
Reminders. Calendar.

**Watch Integration** — Ambient notifications. Quick queries. Health awareness.

**Vehicle Integration** — Navigation assistance. Communication management.
Context-aware mode switching.

## Cross-Device Continuity
User starts coding on desktop. Leaves. Continues on phone. Returns.
FRIDAY resumes seamlessly.

This requires:
- Shared memory server (all devices read/write to one store)
- Shared identity (same personality, same knowledge, same voice)
- Cross-device planning (ExecutionPlans survive device switches)
- Context synchronization (recent conversation migrates between devices)
- Task migration (in-progress agent tasks transfer to the active device)

## Architecture
- Memory server evolves from local JSON to a shared persistence layer
  accessible by all devices
- Identity layer remains constant — personality, tone, behavioral memory
  are device-agnostic
- Each device runs a FRIDAY instance that connects to the shared brain

### Dependencies & Core Libraries

Generation capabilities will be selected when the relevant Ecosystem
component is implemented. The ecosystem changes rapidly — locking specific
frameworks now would require updates before the phase begins.
Install from these categories only when building that specific component:

**Image generation**
Model selection deferred to implementation time. Landscape changes rapidly.

**Video generation**
Model selection deferred to implementation time.

**Voice generation**
Already partially handled by the existing TTS pipeline.
Upgrade path depends on quality requirements at that time.

**Avatar generation**
Model and rendering library selection deferred to implementation time.

**Multimedia processing**
`ffmpeg` (via `ffmpeg-python`) is the most stable cross-version choice
for audio/video manipulation. Can be tentatively listed as a known
dependency for this category.

Do not install any generation library before Phase 18 begins.
The current TTS pipeline (Phase 1) is sufficient through Phase 17.

---

# Non-Negotiable Sequencing Rules

1. Never start Phase N+1 until Phase N exit criteria pass.

2. Every new capability enters the pipeline through ExecutionManager's
   existing branch pattern. Never bypass ExecutionManager.

3. Every new data object is a contract dataclass. Never pass raw dicts
   between layers.

4. Raw user text dies at the Understanding boundary. Nothing downstream
   receives user_message ever again after Phase 2.6 is complete.

5. Self-Evolution follows the same cognitive pipeline as user requests.
   FRIDAY's own code receives no special treatment.

6. New files only when the responsibility genuinely does not exist yet.
   The current file count is already sufficient for Phases 2-8.
   Phase 9 adds only tool registrations in skills/.

7. When a feature request arrives, ask: which existing layer owns this
   responsibility? Add it there. If no layer owns it yet, which phase
   introduces the right layer? Schedule it there.

8. Dependencies are installed only when the capability that requires them
   is actively being implemented. Never install speculatively.

FRIDAY is not a collection of features.
She is a cognitive architecture that grows in one direction.
Every phase makes the next one possible.
That is the only way an ecosystem gets built.

---

# Feature Placement Quick Reference

When a new feature request comes in, place it here:

| Feature | Phase | Reason |
|---|---|---|
| No keywords anywhere | 2.8, 4, 5 | Triage replaces social keywords; routing replaces tool keywords |
| Small LLM for greetings | 2.8 | Triage fast path, before model router exists |
| Model routing (coding/physics/chat) | 4 | Needs stable category output from Understanding |
| Automatic model selection | 4 (table), 7 (learned) | Start deterministic, evolve data-driven |
| Tool usage (calculator, web, files) | 5 | Needs reliable reasoning to select correctly |
| Multi-step task execution | 3 | Planner |
| "Continue where we left off" | 3 | Planner + reliable memory (2.6) |
| FRIDAY challenges bad decisions | 3/6 | Planner reasoning + Reflection quality control |
| Proactive suggestions | 6 | Reflection detects patterns, surfaces insights |
| Behavioral patterns about user | 7 | Learning from Reflection history |
| "What projects use my laptop?" | 8 | Knowledge Graph relationships |
| Vector/semantic memory search | 8 | chromadb / FAISS — Memory V2 |
| Background monitoring | 9 | Requires full tool access + safe execution |
| Self-improvement proposals | 9 | Requires all prior phases |
| User approves code changes | 9 | Human approval layer in brain.py |
| Autonomous deployment | 9 | Tool-based sandbox deployment |
| Screen reading / OCR | 10 | Vision System — easyocr / pytesseract |
| Desktop vision / UI reading | 10 | Vision System — opencv-python, mss |
| Document understanding | 10 | pdfplumber, pymupdf, python-docx |
| Window management | 11 | Device Control — pywin32 |
| System control (volume, sleep) | 11 | Device Control — pywin32 |
| Folder / file monitoring | 11 | Device Control — watchdog |
| Complete workflow automation | 11 | Device Control |
| Browser automation | 12 | Browser Intelligence |
| Game interaction | 13 | Game System — needs Vision + Device Control |
| Android control | 14 | Mobile Integration |
| Unified perception | 15 | Multimodal Reasoning |
| Wake word | 17 | Always-On System |
| Cross-device continuity | 18 | Ecosystem |
| Shared memory across devices | 18 | Ecosystem |
| Image / video / avatar generation | 18 | Ecosystem — deferred to implementation time |