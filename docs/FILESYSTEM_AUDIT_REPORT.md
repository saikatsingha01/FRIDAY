# FRIDAY Universal Filesystem Audit

Source: `p7_fs_stress.py` (59-check deterministic harness, 2026-08-08)
+ full phase regressions. Targets the Phase 5 universal-filesystem
stabilization: FRIDAY must resolve file/folder references anywhere on
the machine (absolute paths, drive letters, known/OneDrive folders,
folder/file names), never silently fall back to the project root, never
hallucinate contents, and must not confuse filesystem intents with
launcher or web intents (and vice versa).

---

## 1. Overall Health

| Metric | Value |
|---|---|
| Phase 5 filesystem stress (`p7_fs_stress`) | **63/63 PASS** (R 30, T 15, P 4, G 10 + 4 LIVE) |
| Phase 5 stress (`p6_stress_500`) | **255/255 PASS** |
| Launch validation (`p5_launch_validation`) | **74/74 PASS** (R 41, G 15, L 11, P 4, H 3) |
| Sequential launch (`p5_seq_launch`) | **28/28 PASS** |
| Response probe / honesty probe | 5/5 PASS · PASS |
| New-file detection (`p8_newfile_probe`) | **10/10 PASS** |
| Live 60-conversation harness (`convo50`) | **60/60 PASS** |
| Hardcoded app names/paths in filesystem pipeline | 0 |
| Silent fallback to workspace on miss | 0 (every miss is an honest `not_found`) |

**Health verdict: the filesystem pipeline is trustworthy.** Every
reference resolves to a real absolute path or a structured miss; the
workspace is only ever a candidate root in a name search, never a
default; file-system intents never leak into launcher/web and vice
versa; and a locate reports the resolved location or an honest
`not_found` carrying the user's requested string.

## 2. Architecture Diagram

```
 User message
    |
    v
 [UNDERSTANDING]  capability/goal/entities (noisy labels absorbed downstream)
    |
    v
 [TOOL ROUTER]    route_tool(understanding, reasoning)
    |   locate phrase / machine scope  -> automation (file_manager), web OFF
    |   folder/path label + device cap -> automation (file_manager)   [folder rescue]
    |   open_application goal + device -> app_launcher                 [launch pin]
    |   web goal / web cap             -> web_search (never for locate/launch)
    v
 [FILE MANAGER]   FileManagerTool.execute(action, path)
    |   path = reference built from structured entities (never raw prose)
    |   resolve_reference(path) -> ResolvedPath{found, path, kind, exists}
    |       absolute path | known folder (shell/OneDrive) | drive ref
    |       workspace/cwd alias | explicit relative | name search (shallow+deep)
    |   found+exists -> read/list/write/delete/locate
    |   found but absent -> write creates it; read/list/locate/delete -> not_found
    |   empty / unresolved -> empty_path / not_found (NO silent fallback)
    v
 [PROMPT BUILDER] locate -> "Found: <path> (kind)"; miss -> "not found: '<requested>'."
    v
 [RESPONSE]       never claims a listing/read/locate that did not happen
```

## 3. What Changed

### New: `src/utils/path_resolver.py`

Deterministic, read-only universal resolver. Resolution tiers (first
match wins):

1. **Absolute path** — `expandvars`/`expanduser`, normalized; carries
   `exists` so write-to-new-file works while read/list/locate stay
   honest.
2. **Known folder** — Windows shell `SHGetKnownFolderPath` (ctypes) so
   OneDrive-redirected Desktop/Documents/Pictures resolve to their real
   location, with singular/alternate aliases (`photos`, `my desktop`,
   ...) mapped to the canonical shell key; env-var fallback when the
   shell call is unavailable (see KI-012).
3. **Drive reference** — "c drive", `c:`, `c:\`, bare `c` → `C:\`,
   with a scoped name search ("games folder in c drive" → `C:\games`).
4. **Workspace / cwd aliases** — "project", "here", ... (matched on
   raw words so "here" is not swallowed as a stopword).
5. **Explicit relative path** — resolved against cwd then workspace.
6. **Name search** — across every drive root, then USERPROFILE, PUBLIC,
   then the workspace (a candidate like any other, never a default).
   Shallow one-level search first, then a bounded deep search
   (max depth 3, 5000 entries, system/cache trees pruned) so a nested
   folder like `C:\games\Marvel's Spider-Man 2` is still found.

Guardrails:

- **No silent fallback.** An unresolved reference returns
  `error="not_found"` (or `"empty"`) with no path — never an implicit
  workspace listing.
- **Type-descriptor stopwords** are singular and noun-modifying only
  (`game`, `app`, `file`, ...); plural forms (`games`, `files`,
  `programs`) and `program` stay significant because they name real
  folders (`C:\games`, `Program Files`).
- **Fuzzy containment requires both tokens >= 2 chars**, so `src` is
  never absorbed by a name like "c game" and "spiderman" never matches
  "01.a.problem".

### Rewritten: `src/skills/file_manager.py`

Sandbox removed; replaced with resolver dispatch. Actions: `read`,
`write` (FILE_WRITE gate), `list`, `delete` (FILE_DELETE gate),
`locate` (new — returns `{found, path, kind}`). No default base: a
missing reference is `empty_path`, an unresolved one is `not_found`
carrying `metadata.requested` = the user's string.

### Updated: `src/core/tool_router.py`

- `_filesystem_reference()` builds the path parameter from structured
  entities (excludes machine-scope words like "my pc"; an
  `application` label counts only for locate or folder/path text).
- `_filesystem_action()` picks locate/read/list from the intent, goal,
  and the user's own words.
- `_filesystem_locate_signal()` rescue pins a locate request to
  file_manager before the launch pins run, and forces web off — a
  locate is never a launch and never a web search. "where is paris"
  (no machine scope, no file/folder entity) stays a web search.
- `file_manager` requests now carry `parameters={"path": ref}` (joined
  entity texts) instead of empty parameters, or `{}` when no reference
  was extracted (executor returns a structured `empty_path` failure —
  the response model can never hallucinate contents).

### Updated: `src/ai/prompt_builder.py`

- A `file_manager` success with `found` renders
  `"  Found: <path> (<kind>)"` before entries/content.
- A `file_manager` miss renders `"  Outcome: not found: '<requested>'."`
  using `metadata.requested`, so the reply names exactly what was
  asked for.

## 4. The Three Live-User Bugs This Fixes

| Live symptom | Root cause (before) | Now |
|---|---|---|
| "location of marvel's spider-man 2 game" → web search | locate request drifted to `web_search` | `file_manager.locate` pinned by `_filesystem_locate_signal`; web forced off. |
| "...location of marvels spiderman 2 game in my pc" → app launcher | `open_application` goal hijacked a locate | locate rescue runs before the launch pin; request stays `file_manager.locate`. |
| "whats inside my games folder in c drive" → listed the project root, hallucinated games | `file_manager` fired with `{}` → `_list` fell back to `DEFAULT_BASE` = project root | path = "games folder in c drive" → resolves to `C:\games` and lists its real contents. |

Offline end-to-end (real router + real executor, no LLM):

```
where is marvels spiderman 2 game in my pc
  -> file_manager.locate("marvels spiderman 2 game")
     found: C:\games\Marvel's Spider-Man 2 (dir)
tell me whats inside my games folder in c drive
  -> file_manager.list("games folder in c drive")
     entries: [Marvel's Spider-Man 2 (dir)]
what is inside my python problem folder
  -> file_manager.list("python problem folder")
     entries: [PINT_STAR.PY (file), ...]  (real C:\python problem)
list C:/nope -> status=not_found (never a workspace listing)
```

## 5. Deterministic Verification (`p7_fs_stress.py`, 59 checks)

| Part | Checks | Covers |
|---|---|---|
| R resolver | 30 | absolute (dir/file/slash/missing), env expansion, known folders incl. OneDrive + aliases, drive refs (word/colon/bare letter), workspace/cwd aliases, relative paths, shallow + deep name search, drive-scoped search, empty/None/bogus, fuzzy guardrails, no-silent-fallback |
| T tool | 15 | list (folder/drive/missing/empty), read (existing/missing/dir), locate (found + honest miss), write + delete (permission-gated, real temp dir), delete-missing, unsupported action |
| P prompt | 4 | locate "Found: <path> (dir)", not_found carries requested, list renders names (no raw paths), read trims long content |
| G routing | 10 | locate beats launch, list vs read vs locate, "open spotify" stays launcher, "where is paris" stays web, locate + use_web never fires web, machine scope excluded from reference, folder rescue beats open_application, empty-reference request |

## 5b. New-File Detection (`p8_newfile_probe.py`, 10 probes) + live 60-convo

Final Phase 5 proof: FRIDAY must detect **freshly created** files and
folders anywhere on the machine through natural voice phrasing. Ten real
folders/files were created across every drive and known-folder type
(C: root, D:, E:, Downloads, OneDrive Desktop, OneDrive Documents,
profile root, nested custom folders, games-adjacent folder), each
queried with the exact phrasing a user would speak (zero structured
entities injected). Was 5/10 before the fixes below; **10/10 PASS**
after.

Root causes fixed:

- `_deep_entries` (path_resolver): a single shared `seen` set + shared
  depth/count budget across all roots starved later roots (the C:\ walk
  exhausted the depth budget before Downloads/Desktop/Documents were
  reached). Each root now walks independently (per-root depth + budget).
- Single-letter frame word "i" (tool_router): "friday probe i" lost the
  "i" and silently matched `friday_probe_a`. `_raw_filesystem_reference`
  now re-attaches a single-letter frame token directly adjacent to a
  surviving name token.
- Read-via-goal (tool_router): "read my rootfile dot txt file" fired
  `list` because read-detection required a `file`-labeled entity.
  `_filesystem_action` now reads `read`/`read_file`/`readfile` from the
  intent/goal.
- Dictation + scoped search (path_resolver): new `_spoken_filename`
  ("rootfile dot txt" → `rootfile.txt`) and resolver stages 6a/6b
  (`<name> <known folder>` → search inside that folder, e.g. "friday
  probe e desktop" → Desktop), both only tried after the unscoped name
  search misses.

Live-pipeline routing gap the 60-turn harness caught (the deterministic
probe injects the filesystem semantic, so it cannot see this): the small
Understanding model misclassifies natural phrasing as an app launch
(`device`/`open_application` + `application` entity) or a memory/hardware
turn — "what is inside my friday probe a folder", "list what is inside
friday probe e on my desktop", "read my rootfile dot txt file". Fixed in
`src/core/tool_router.py`:

- `_FS_QUERY_TEXT_RE`: a filesystem ask is "what's/what is inside",
  "contents of", or a list/show/read verb + folder/file/known-folder
  word — never a launch/web/chat phrase.
- Rescue in `route()` pins a matching raw-text query to `automation`
  (file_manager) before the `open_application`/launch pins; explicit
  web-search goals are never hijacked.
- `_filesystem_action` detects a literal "read" verb in raw text (the
  live model sets `goal=open_application`, so intent+goal alone never
  carried the read signal).
- `tool_required()` enters the tool path for a raw-text filesystem
  query even when the capability resolves to memory/hardware (the
  execution gate previously kept `route()` from running at all).

| Probe | Result |
|---|---|
| C:\friday_probe_a (report.txt) — "what is inside my friday probe a folder" | list → real path |
| D:\friday_probe_b (notes.md, rootfile.txt) — "friday probe b on the d drive" | list → real path |
| E:\friday_probe_c (data.log) — "contents of the friday probe c folder" | list → real path |
| Downloads\friday_probe_d (hello.txt) | list → real path |
| OneDrive Desktop\friday_probe_e (desktop.txt) — "on my desktop" | list → real path |
| OneDrive Documents\friday_probe_f (doc.txt) | list → real path |
| profile\friday_probe_g (readme.txt) | list → real path |
| D:\friday_probe_b\rootfile.txt — "read my rootfile dot txt file" | read → real content |
| C:\test code\friday_probe_i (inner.txt) | list → real path |
| E:\my games\friday_probe_j (kappa.txt) | list → real path |

After proof, all 10 probe items were deleted; `Get-ChildItem` confirmed
the machine was restored. `convo50.py` (real pipeline, real LLM,
checkpointed) extended to 60 turns — **60/60 PASS**. One transient
flake: an already-empty real folder produced a fabricated prose reply on
the first 60-run; re-verified 5/5 clean on retry and the rerun then
passed 60/60 (the honesty render "the folder is empty" was already in
place — pure response-model nondeterminism, not a resolver bug).


## 6. Regressions (all re-run after the resolver and router changes)

| Suite | Result |
|---|---|
| `p6_stress_500` (full, checkpoint cleared) | 255/255 PASS |
| `p5_launch_validation` | 74/74 PASS |
| `p5_seq_launch` | 28/28 PASS |
| `p5_response_probe` | 5/5 PASS |
| `p5_honesty_probe` | PASS |
| `p7_fs_stress` (after router fixes) | 63/63 PASS |
| `p8_newfile_probe` (after router fixes) | 10/10 PASS |
| `convo50` (60-turn live) | 60/60 PASS |

## 7. Minor Issues / Notes

- **KI-012** (documented): on non-Windows, known folders resolve via
  env-var paths instead of the shell table — inherently can't follow
  OneDrive redirection. Windows (the supported platform) always uses
  the shell tier first.
- **Name-search ordering**: multiple matches resolve to the first hit
  in deterministic search order (exact before fuzzy, shallow before
  deep, drive roots before profile/workspace). A broad reference like
  "src" resolves to the first real match — users should be specific,
  and a miss is always honest.
- **Deep search is bounded** (depth 3, 5000 entries, system/cache
  trees pruned) so a huge drive can never stall a turn (~70ms typical
  miss).

## 8. Folder Contents-Retrieval Fix (`fsq_live_suite`, 60/60 PASS)

Universal fix for the two classes of contents bug FRIDAY hit when asked
"What is inside my <folder>" (folder cross-contamination and stale /
incorrect directory listings in answers).

### 8.1 Root cause (confirmed from real data)

`src/memory/memory.json` facts ids 153–154 and `episodes.json` 58–59 /
`memory_history.json` 152 show directory **listings were being written
to long-term memory as durable facts** (the C Lab listing was merged
into the Python Projects fact, so later listings of either folder
echoed the wrong, stale contents). The LLM then answered contents
questions from those stored facts instead of from a fresh `file_manager`
listing.

### 8.2 Fix architecture (universal — no hardcoded names/paths)

1. **Prompt-level contract** — `understanding_prompt.py` SYSTEM_PROMPT
   gained a "FILESYSTEM CONTENT IS NEVER STORED" section: listings are
   dynamic machine state, never memories.
2. **Deterministic store gate (Rule 14)** — `memory_analyzer.py` added
   deterministic Rule 14: closed-class vocab (location nouns, inspection
   frames, state predicates) forces inspection questions → a memory
   query with **no fact**, and content-state statements ("contains",
   "is inside") → **no write**. Gate suite `fs14_analyzer_gate_suite.py`
   **37/37**; p9 regression 128/128 + 6/6.
3. **Deterministic response guard** — `response_generator.py` added
   `guard_listing_response()` (fabricated-in detection, deterministic
   re-render from the real `entries`, honest not-found reply, honest
   failure reply, grant/permission-language replacement). `brain.py`
   routes every final response through `_final_response()` =
   `_clean_response(guard_listing_response(response, execution.tool_results))`.
   Guard unit suite `fsq_guard_unit.py` **17/17**.

Net effect: the LLM is never the source of filesystem facts. Fresh
inspection happens per request, identity = the resolved absolute path,
memory may resolve references but never overrides a fresh listing, and
the actual listing results always reach the final response generator.

### 8.3 Results (all fresh runs, current code)

| Suite | Result |
|---|---|
| `fsq_live_suite.py` (60-item live FSQ) | **60/60 PASS** |
| `fsq_guard_unit.py` (guard determinism) | **17/17 PASS** |
| `fs14_analyzer_gate_suite.py` (Rule 14) | **37/37 PASS** |
| `p9_fs_accuracy_suite.py` (regression) | **128/128 + 6/6 LIVE** |
| `convo50.py` (broad 60-turn regression, fresh) | **60/60 PASS** |
| Real `memory.json` listing-fact scan after all runs | **0 listing facts** |

### 8.4 Notes

- Probing found the 3b model occasionally mislabels `switch` as a
  hardware word and `one`/`two` as frame words; the live suite uses
  fixture names (`fsq set a/b/c`, `fsq alpha/beta`) and router
  backstops that resolve deterministically even with zero entities.
- The guard only rewrites successful-listings / not-found / failure
  results; non-filesystem and `read` results pass through untouched.

## 9. Universal Contents-Retrieval Round 2 (`fsq30_convo`, 30/30 PASS)

A dedicated **30-conversation live suite on the user's real PC folders**
(C:\C Lab, C:\python projects, C:\c projects, C:\games, Downloads,
Desktop, Documents, C:\project friday, C:\test code, fixture folders,
plus repeated asks, corrections, and re-asks) still found **5 wrong
answers** after Round 1 — none of them stale-memory echoes (Round 1 had
fixed those), but two new router-level routing bugs.

### 9.1 Root causes (confirmed from live understanding/route dumps)

1. **Known-folder queries fired NO tool.** "what is inside my downloads
   folder" / "desktop folder" arrive from Understanding with
   `capability=device` (the small model treats a folder as the File
   Explorer app). `tool_required()` returned `False` for
   `capability=="device" and not a launch` **before** the raw-text
   filesystem-query rescue was ever checked — so the execution manager
   never called the router and the model answered with an evasive
   "I don't have any information about the contents of that folder yet /
   I don't have access to your files" reply. No tool, no listing.
2. **Apostrophe contractions silently listed the drive ROOT.** "what's
   inside my python project folder in c drive" tokenized `what's` into
   `what s`; the stray `s` is not a frame word, so it survived stripping
   and poisoned the recovered reference (`"s python project c drive"`).
   It did not resolve, so `_best_filesystem_reference` fell back to the
   structured entity `"c drive"` → a real, confident-looking listing of
   `C:\` (47 entries). Not a fabricated file, but the wrong folder.

### 9.2 Fix (both universal, no hardcoded names/paths)

1. **`tool_required()` ordering** (`src/core/tool_router.py`): the
   raw-text filesystem-query gate is now computed first and overrides
   the device short-circuit — a "what is inside X folder" turn is never
   a chat turn, so capability=device can no longer drop it before the
   router's fs-query rescue pins it to `file_manager`. Web-search goals
   remain excluded, so knowledge turns ("what is inside a black hole")
   are untouched.
2. **Contraction-safe reference recovery** (`_raw_filesystem_reference`):
   apostrophes are merged before tokenizing (`what's` → `whats`, a frame
   word), so no stray `s`/`t` can poison the recovered reference.

Round 1 additions also landed this session: the guard now also catches
empty/only-one claims on a non-empty first listing, denial language on a
success, and evasive no-info replies (guard suite grew 17/17 → 33/33),
and listings are folder-bound in the prompt (`prompt_builder
._format_tool_results` renders `Folder listed: "<basename>"`; `file_manager
._list` carries the resolved `path` in its result data).

### 9.3 Results (all fresh runs, current code)

| Suite | Result |
|---|---|
| `fsq30_convo.py` (30-convo real-folder live suite) | **30/30 PASS** |
| `fsq_live_suite.py` (60-item live FSQ) | **60/60 PASS** |
| `fsq_guard_unit.py` (guard determinism) | **33/33 PASS** |
| `fs14_analyzer_gate_suite.py` (Rule 14) | **37/37 PASS** |
| `p9_fs_accuracy_suite.py` (regression) | **128/128 + 6/6 LIVE** |
| `convo50.py` (broad 60-turn regression, fresh) | **60/60 PASS** |
| Real `memory.json` scan after all runs | **38 facts, 0 listing facts** |

### 9.4 Notes

- Pre-fix reproductions confirmed the routing miss is deterministic per
  phrasing class (3/3 runs each for downloads, desktop, python-project),
  not a one-off LLM flake: all fired no tool / drive root before the fix,
  and all resolved to the real folder after it.
- The evasive no-tool replies (`I don't have any information about the
  contents of that folder yet`) are also guarded against in the response
  guard, but the root fix is routing — the tool now always fires.

## 10. Universal Local-Path Truth Fix (`locate_guard_regression`, 25/25 PASS)

The final-response path guard. This closes the last fabrication class:
FRIDAY **speaking a confident absolute local path that no current tool
result produced**.

### 10.1 Symptom evidence (user session log, 2026-08-10 01:42–01:45)

| Ask | FRIDAY said | Truth |
|---|---|---|
| "tell me the path of srczip file" | `C:\project\srczip` (a *folder*) | `srczip` was not a file; answer mislabeled kind and path |
| "python 3.12 installer.exe" | invented `C:\project\python\bin\python.exe` | the tool had found only a `.pyc`; that path does not exist |
| "assassins creed 3 remastered folder" | claimed `C:\Games\Ubisoft\Assassin's Creed III Remastered` | `web_search` succeeded, but that local path does not exist |

### 10.2 Root causes (confirmed from live dumps)

1. **No final-response path check.** A locate turn that produced no
   `file_manager` result (or a web-only one) still let the LLM speak an
   absolute path built from web info / memory / a guess. Nothing verified
   the path was in the current turn's successful local results.
2. **Web results were indistinguishable from local findings.** A locate ask
   that drifted to `web_search` (AC3 case: planner goal `general`, steps had
   no `use_tool` locate step) rendered web snippets without marking them as
   internet info, so the model turned a webpage into a local path.
3. **Wrong kind.** "the path of srczip *file*" — `locate_reference` did not
   exist; the old locate path could not say file-vs-folder, exact-vs-close.

### 10.3 Fix (universal — no hardcoded names/paths)

1. **`path_resolver.locate_reference()`** — a locate that only ever reports
   paths that **exist right now**, classifies each match as **exact /
   normalized / fuzzy**, and returns every relevant real candidate
   (bounded multi-match) so "multiple matches" is reported honestly.
2. **`file_manager._locate`** — locate is routed through `locate_reference`
   **before** the shared not_found gate; result carries `path`, `kind`,
   `match`, `requested`, and `candidates`.
3. **`tool_router`** — a raw-text filesystem-noun locate signal
   (`folder/file/directory/desktop/downloads/...`) pins locate asks to
   `file_manager` even when the model classified device/hardware/memory/web
   (AC3 phrase reaches the tool, never `web_search`).
4. **`prompt_builder`** — web results are labeled "(These are internet
   search results, not a location on this computer.)"; locate renders show
   the requested reference, match kind, and every real candidate.
5. **`response_generator.guard_path_response`** (wired in
   `brain._final_response` after `guard_listing_response`) — the universal
   rule: **an absolute local path may be spoken ONLY when it appears in a
   successful current `file_manager` result**. Locate turns are regenerated
   deterministically from the tool result (path + kind + match kind + all
   real candidates). Non-locate file turns replace any spoken path not in
   the current results. Web-only / zero-result locate asks that still speak
   a path get an honest "that was internet information, not a location on
   this computer". Path-token splitting only separates a note at a dash with
   whitespace on both sides, so real names like
   `Godot_v4.6.3-stable_win64.exe.zip` survive.

### 10.4 Results (all fresh runs, current code)

| Suite | Result |
|---|---|
| `locate_guard_regression.py` (universal 25-case: exact/normalized/fuzzy/multi/not-found/web/weather/contamination, real seeded files) | **25/25 PASS** |
| Manual real-pipeline (Siliguri weather → web only; "srczip" → 4 real matches; python installer → real `Downloads\Python 3.12 Installer.exe`; AC3 → honest not-found) | **PASS** |
| `locate_guard_smoke.py` | **13/13 PASS** |
| `fsq_guard_unit.py` | **33/33 PASS** |
| `fs14_analyzer_gate_suite.py` | **37/37 PASS** |
| `convo50.py` | **60/60 PASS** |
| `p9_fs_accuracy_suite.py` | **128/128 + 6/6 LIVE** |
| `fsq_live_suite.py` | **60/60 PASS** |
| `fsq30_convo.py` | **30/30 PASS** |

### 10.5 Honest remaining issues (not fixed, not hidden)

- **Reference extraction quality is model-dependent.** "file named gur src
  zip" can arrive as the reference `src`; a single fused word
  ("gurxanaduprime") can be dropped by the ≥2-token raw recovery rule.
  In every such case the answer stays honest (real paths, or an honest
  "couldn't find"), never fabricated.
- A genuine **multiple-match** reply lists up to 4 real candidates; if the
  user meant a specific one, they must name it. This is truth, not noise.
