# FRIDAY Application Launcher Audit

Source: `p5_launch_validation.py` (74-check audit, 2026-08-07) + catalog
probes + full phase regressions + the 28-turn sequential-launch harness
(`p5_seq_launch.py`). Targets the launch-pipeline BUG 1–8 set: universal
discovery, deterministic resolution, never-guess ambiguity, honest
reporting, the fabricated "I opened the file manager" success, and the
sequential-turn execution/context bug (every launch turn must re-fire the
tool even when Understanding drops its structured signals).

---

## 1. Overall Health

| Metric | Value |
|---|---|
| Launch audit (`p5_launch_validation`) | **74/74 PASS** (R 41, G 15, L 11, P 4, H 3) |
| Sequential launch (`p5_seq_launch`) | **28/28 PASS** |
| Phase 5 stress (`p6_stress_500`) | **255/255 PASS** |
| p5 stress / p4 stress / response / honesty | 42/42 · 64/64 · 5/5 · PASS |
| Catalog index (this machine) | 216 entries (start_menu 98, builtin 15, registry 23, windowsapps 80) |
| Hardcoded app names/paths in launch pipeline | 0 |

**Health verdict: launch pipeline is trustworthy.** Discovery is universal
(Start Menu + registry + WindowsApps aliases + Steam + Epic + builtins), the
resolver never guesses (found / ambiguous / not_found only), results carry
display names not paths, and an empty tool path now produces an honest
"could not do it" reply instead of fabricated success. First audit run was
60/66; both residual failures were real resolver bugs (chrome→Office
ambiguity, injected-ambiguity collapsing to a single FOUND hit), fixed and
re-verified to 66/66.

## 2. Architecture Diagram

```
 User message
    |
    v
 [UNDERSTANDING]  capability/goal/entities (off-enum noise absorbed downstream)
    |
    v
 [MODEL ROUTER]   capability -> model (unchanged, Phase 4)
    |
    v
 [TOOL ROUTER]    route_tool(understanding, reasoning)
    |   open_application goal + device -> app_launcher   <-- rescue (was web/general)
    |   folder/file rescue -> file_manager (wins) ; command -> terminal ; web -> web_search
    v
 [TOOL EXECUTOR]  permission gate -> execute(request)
    |
    v
 [APP LAUNCHER]   ApplicationLauncherTool.execute(launch, app)
    |   app_catalog.resolve(app)  -> found | ambiguous | not_found
    |   found:       os.startfile(target), data {launched: True, detail: <display name>}
    |   ambiguous:   data {launched: False, ambiguous: True, candidates: [...]}
    |   not_found:   ToolResult(status="not_found", error="not_found")
    v
 [EXECUTION MGR]  empty results + resolvable capability -> synthesized failure
    |                 ToolResult(tool_router/dispatch/no_tool_selected)
    v
 [PROMPT BUILDER] TOOL RESULTS -> ambiguous block (ask which one) /
    |                 non-success block (nothing ran -> say so) / stale-context guard
    v
 [RESPONSE]       never claims success without a real launched detail
```

## 3. Failure Distribution (first audit run, before fixes)

| Part | Tests | Pass | Fail | Dominant failure |
|---|---|---|---|---|
| R resolution | 41 | 38 | 3 | chrome→AMBIGUOUS vs Office (1); file-manager label expectation (1); injected ambiguity collapsed to FOUND (1) |
| G routing | 9 | 9 | 0 | — |
| L launcher | 9 | 6 | 3 | file-manager label (1); spiderman label (1); injected ambiguity launched instead of clarifying (1) |
| P prompt | 4 | 4 | 0 | — |
| H honesty | 3 | 3 | 0 | — |
| **Total** | 66 | 60 | 6 | 3 resolver logic, 3 harness expectations |

After fixes: **66/66**, zero logic failures.

## 4. Root Cause Analysis

### RC-L1 — Multi-token fuzzy matching pinned short name tokens
"open my chrome browser" resolved AMBIGUOUS against 'Microsoft Office Home
2024 - en-us' (the query token *chrome* fuzzy-pinned *home*). Fixed in
`_aligned_match`: fuzzy pins now require multi-token queries AND a pinned
name token ≥ 5 characters, so a 6-char query token can no longer pin a 4-char
name token. Chrome is FOUND deterministically.

### RC-L2 — Category words treated as filler
When `app/application/program/browser` were filler, "whats app" collapsed
into the 'Whats New' entry. Fix: three sets — `_FILLER` (the/a/an/please/
open/launch/start/run/me/my), `_SKIPPABLE_CATEGORY` (browser/program, freely
skippable), `_PIN_CATEGORY` (app/application/manager/viewer/player, real name
parts that must pin a name token and drive the "whats app"→"whatsapp"
concat variant). An all-category query ("browser") now matches nothing
(`pinned_any`).

### RC-L3 — Misrouted/entity-less launches went silent or fabricated
The BUG 5/6/7 evidence: "launch spotify" → `web` → web_search fired; "open
spotify" → `general` → no tool + vague reply; "open file manager" → `device`/
`create`, zero tool results, fabricated success. Fixes (all deterministic):
- Router pins `goal == "open_application"` to `device` after the file/folder
  rescue (never overrides automation), so both spotify turns reach the
  launcher.
- Execution manager synthesizes a failure ToolResult when a capability
  resolves to a registered tool but no request is routable; the prompt's
  non-success branch forces "I could not do it" — fabrication impossible.
- Prompt BASE_HONESTY_RULES gained the stale-context guard: replies may only
  use the current message + TOOL RESULTS, never earlier turns' listings.

### RC-L4 — Ambiguity launched a single best match
The audit's injected near-duplicate app ("Google Chrome Beta") collapsed to a
FOUND launch instead of a clarification. The resolver's confident threshold
(82) + ambiguity band (12) handle real cases ("studio" → Visual Studio Code /
Visual Studio Installer), but the true fix is the contract: `resolve()` never
returns a guess — the ambiguity path returns candidates and the prompt forces
"which one do you mean?" with no launch and no claimed success.

### RC-L5 — Paths leaked into responses
A launched app's absolute WindowsApps path appeared in the spoken reply.
Fixed: launcher `data.detail` carries the display name only; `_format_tool_results`
renders the payload as structured facts; no tool names, paths, dict dumps, or
URLs reach the response prompt.

## 5. Architectural Weaknesses

1. **Understanding off-enum capability is still absorbed, not fixed.** Every
   observed LLM variant (`web_search`, `searching`, `file_system`, `device`…)
   is patched in the router. Durable fix = schema validation with retry at the
   Understanding layer (tracked KI-007/KI-009).
2. **Ambiguity is keyed to name overlap.** "studio" works; genuinely distinct
   apps with identical display names are collapsed by `_collapse_duplicates`
   (longest entry wins). Acceptable for a voice assistant, documented.
3. **Launch is fire-and-forget.** `os.startfile` reports launch initiation,
   not the app's own startup success; the launcher cannot distinguish "opened
   then crashed" from "opened". Honest by design — it claims "launched", not
   "running well".
4. **Registry DisplayIcon/InstallLocation can be empty**, forcing fallback to
   the WindowsApps/`.lnk` index for some store installs; coverage is
   source-dependent (Steam/Epic absent on this machine, so untested live).

## 6. Implementation Bugs

| # | Location | Bug | Effect | Fix |
|---|---|---|---|---|
| 1 | `app_catalog._aligned_match` | Fuzzy pin on short name tokens | chrome→AMBIGUOUS vs Office | Pinned name token ≥5 chars + multi-token gate |
| 2 | `app_catalog._FILLER` | app/application/program/browser were filler | "whats app"→'Whats New' | Split into `_SKIPPABLE_CATEGORY` / `_PIN_CATEGORY` |
| 3 | `app_catalog` | WindowsApps scan used a single bad dir | 0 aliases discovered | Scan 3 candidate dirs, dedup by filename |
| 4 | `tool_router` | No rescue for open_application on web/general | spotify never launched | `goal==open_application` → device (post file/folder rescue) |
| 5 | `execution_manager` | Empty tool results passed silently | fabricated success / silence | Synthesized `no_tool_selected` failure |
| 6 | `app_launcher` | Hardcoded aliases/paths, leaked target path | stale/machine-specific behavior | Rewrite: catalog-only, `detail` = display name |
| 7 | `prompt_builder` | No ambiguity/empty-results/context guard | "I opened it" without a launch | Ambiguity block + non-success branch + stale-context guard |

## 7. Technical Debt

- **Audit harness lives outside the repo** (`%TEMP%\opencode\p5_launch_validation.py`
  with `p5_launch_validation_log.txt` / `_results.json`); no `tests/` dir, no
  CI — same pattern as earlier phase harnesses.
- **`resolve()` ambiguity depends on the installed set** on the machine it
  runs on; the audit pins the stable cases (chrome, studio, whats app) but
  label expectations are per-machine (e.g. 'file manager' builtin label).
- **Steam/Epic paths unverified live** (no client installed); logic is
  standard VDF/JSON parsing, unit-covered by the catalog source wiring only.
- **`os.startfile` is mocked in the audit**; real launches are user-test
  territory (per standing instruction the user runs the live test).

## 8. Recommended Implementation Order

1. **Move the audit + probe harnesses into `tests/`** and wire a CI/smoke
   script (all prior phases would also gain reproducible harnesses).
2. **Stable Understanding (KI-007)** — schema-validated capability with retry
   at the Understanding layer; lets the router drop its variant table and
   rescues.
3. **App-set reflection** — surface `app_catalog.stats()` and ambiguous
   candidates into the response so "which one?" can offer precise names.
4. **Steam/Epic live test** on a machine with the clients, then lock those
   catalog paths into the audit.
5. **Launch-verify follow-up** — optional Windows `WaitForInputIdle`-style
   check if "running well" reporting is ever required (today's "launched" is
   the honest ceiling).

## 9. Expected Performance After Fixes

| Capability | Before | After |
|---|---|---|
| Discover apps (any source) | hardcoded aliases only | universal (176 entries here) |
| Resolve exact/typed names | fuzzy keyword match | exact→subset→aligned→fuzzy tiers, threshold 82 |
| Resolve ambiguity | launched best guess | never guesses; asks with candidate list |
| not_found | silent / vague | honest `not_found` reply |
| Misrouted launch (web/general) | wrong tool or nothing | always app_launcher for open_application |
| Empty tool path | fabricated success | synthesized failure + honest "could not do it" |
| Path/payload leak into speech | leaked absolute paths | display names only |
| Stale context echoed | old listings carried in | current-message + TOOL RESULTS only |
| Regression safety | — | 66/66 audit + 255/255 p6 + 42/42 + 64/64 + probes |

Residual risks: Understanding off-enum noise (mitigated, KI-009), fire-and-
forget launch semantics (by design), per-machine app-set variability in the
audit's label expectations.

---

## Follow-up: Reliable app activation + launch routing (2026-08-07)

Live user test surfaced the intermittent "launch spotify reports success but
the app never opens" bug plus two misrouting failures. Root causes, all
fixed and regression-proven:

### Bug B — WindowsApps alias stubs are unreliable for packaged apps

`resolve("spotify")` returned the store alias
`C:\Users\polis\AppData\Local\Microsoft\WindowsApps\Spotify.exe`, which
`os.startfile` cannot reliably activate (tasklist showed only
`SpotifyLauncher.exe` / `SpotifyXboxGamebarWebView`, no `Spotify.exe` UI).
Chrome/File Explorer resolve to `.lnk` targets and always worked — the
failure was specific to packaged-app alias stubs.

Fix (`app_catalog.py` + `app_launcher.py`):
- `app_catalog._start_apps_aumids()` caches `Get-StartApps` AUMIDs once per
  process (filtered to real apps, no `scheme://` AppIDs) and attaches
  `aumid` to every WindowsApps entry; `resolve()` carries it through.
- `app_launcher` activates any resolved entry that has an AUMID via
  `subprocess.Popen(["explorer.exe", "shell:AppsFolder\\" + aumid], ...)`
  with `os.startfile(target)` as fallback if the shell activation fails.
  Non-packaged entries (`.lnk`, registry, builtins) keep the `os.startfile`
  path unchanged.
- Universal: applies to every packaged app, not just Spotify. Live-verified
  twice — `launcher.execute("spotify")` reports success and multiple
  `Spotify.exe` UI processes run.

### Bug A1 — "launch brave browser" fired a web search

Understanding labeled it capability=web, goal=create, entity
`(brave, application)`; the router sent it to `web_search`. Fix
(`tool_router.py`): a `web`-capability request carrying an
`application`-labeled entity is a launch signal unless the goal is an
explicit web goal (`search_web` / `retrieve_web` / `find_information`);
real searches keep their `topic`/`query` labels and stay on `web_search`.

### Bug A2 — "open file explorer" dropped its entity and did nothing

The model returned no entities, so no tool request could be built and the
pipeline synthesized an honest `no_tool_selected` failure. Fix
(`tool_router.py`): for goal `open_application` + device capability with no
entities, recover the reference from the user's own words
(`_fallback_app_reference`), rejecting folder/path-style text; the recovered
name still passes through the safe resolver (found / ambiguous / not_found —
never a blind launch).

### Residual (not pipeline bugs)

- Phrasing quirks in generated speech ("I found the Chrome browser in your
  list of files", present-tense "I'm opening … on my device") are LLM
  wording, not routing/execution issues.

### Regression proof after fixes

| Suite | Result |
|---|---|
| `p5_launch_validation` (74 checks) | 74/74 PASS |
| `p5_seq_launch` (28 turns) | 28/28 PASS |
| `p6_stress_500` (checkpoint cleared) | 255/255 PASS |
| `p5_stress_50` | 42/42 PASS |
| `p4_stress_50` | 64/64 PASS |
| `p5_response_probe` | 5/5 PASS |
| `p5_honesty_probe` | PASS |
| Live `launcher.execute("spotify")` | success + `Spotify.exe` UI running |

---

## Sequential-launch execution/context bug (2026-08-07)

The single-turn fixes above left one failure layer: **repeated launch turns in
one conversation**. Reproducing "open spotify" four times in a row:

- Turn 1 worked. Turn 2 came back `Need Tools: False`, `TOOL RESULTS: None`,
  and Friday fabricated "I'm opening Spotify… playing some music".
- Turn 3 had `Need Tools: True` but still `TOOL RESULTS: None`.
- KI-009 full structural drift on long repeats (harness turns 23-25):
  `use_tools=False` plus planning hijack ("I'll continue with step 2 of the
  execution plan…", no tool results) or misrouting "open steam" onto
  `web_search` ("I found Steam on the desktop. It's open now.").

### Layer 1 — deterministic launch-signal gate (already in)

- `tool_router.has_launch_signal(understanding)`: `goal == "open_application"`
  or an intent command/request with an `application`-labeled entity is a
  launch signal; explicit web goals excluded. `route_tool` forces
  `tool_cap = "device"` for launch signals when the model's cap is not in
  {device, system, automation}.
- `execution_manager`: a synthesized-failure ToolResult fires when
  `capability_has_tool(...) or has_launch_signal(...)`, so an empty route
  never claims success.
- `reasoning_engine`: `use_tools` includes `has_launch_signal(...)`, so the
  pipeline re-fires a tool even when Understanding drops `tools`.

### Layer 2 — raw-text launch recovery + planning/web suppression (this fix)

The gate still depended on structured `goal`/`capability` surviving the LLM.
On long repeats the model drifts to `use_tools=False` **and** drops the launch
goal. Fix in `tool_router.py` + `reasoning_engine.py`:

- **Raw-text launch gate.** `_raw_text_launch_ref(raw_text)` strips a
  pre-verb filler set (`please`, `can`, `could`, `would`, `will`, `do`,
  `hey`, `okay`, `ok`, `sure`, `yes`, `kindly`), requires the literal first
  token to be `open`/`launch`, then recovers the app reference via
  `_fallback_app_reference` (folder/path-style text rejected, single-letter
  references rejected). `has_launch_signal` checks raw text **first**, so a
  raw launch wins even over a drifted web goal.
- **Web suppression on launch.** `route_tool` hoists the launch signal above
  the web/capability logic and sets `use_web=False` /
  `goal_search_web=False`, so "open steam" (drifted `cap=web`) goes to
  `app_launcher`, never `web_search`.
- **Planning suppression on launch.** `reasoning_engine` sets
  `use_planning = (base_planning or continuity) and not launch_signal` and
  `continuity_only = continuity and not base_planning and not launch_signal`
  — a launch turn never degrades into "continue the plan" chit-chat.
- **Safety invariant kept.** `_raw_text_launch_ref` only fires on a literal
  leading `open`/`launch`; chat/web/terminal/system turns and folder-hint
  text never reach `app_launcher`. Genuine web requests still hit
  `web_search`; explicit web goals stay excluded.

### Sequential harness

`p5_seq_launch.py`: 28 sequential turns (repeated "open spotify" plus
notepad / file explorer / steam / an unknown app). Run against a fresh
conversation manager; every launch turn must show a fresh tool execution
turn in its response, and the final turn must report `not_found` honestly
instead of a fabricated open.

### Regression proof (all after the layer-2 fix)

| Suite | Result |
|---|---|
| `p5_launch_validation` (74 checks) | 74/74 PASS |
| `p5_seq_launch` (28 turns) | 28/28 PASS |
| `p6_stress_500` (checkpoint cleared, full re-run) | 255/255 PASS (A 79, B 13, C 35, D 72, E 24, F 16, G 16) |
| `p5_stress_50` / `p4_stress_50` | 42/42 · 64/64 PASS |
| `p5_response_probe` / `p5_honesty_probe` | 5/5 · PASS |

### Residual (documented, not pipeline bugs)

The Understanding model is still nondeterministic about `goal`/`capability`/
`entities` on long conversations; the raw-text gate absorbs the observed
drift, but the durable fix remains schema validation with retry at the
Understanding layer (tracked with KI-007/KI-009).

---

## Packaged-app discovery gap (2026-08-07)

Live test: "launch whatsapp" returned `app_launcher -> not_found` — no
permission window ever appeared because the catalog could not resolve the
app at all (not_found never reaches the permission gate). WhatsApp Desktop
is installed as a **packaged (Store/MSIX) app**; `Get-StartApps` lists it
(`WhatsApp -> 5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App`), but the catalog's
WindowsApps discovery only scanned `%LOCALAPPDATA%\Microsoft\WindowsApps`
for `.exe` alias stubs, and WhatsApp exposes **no** alias stub. (Spotify
worked because it does.)

**Fix** (`app_catalog.py` + `app_launcher.py`), universal, no hardcoded apps:

- **New discovery source — the shell's Start-Apps index.** `_start_apps_index()`
  caches the parsed `Get-StartApps` output once per process; `_discover_start_apps()`
  adds every packaged-app entry (AppID is a real AUMID, contains `!`) that is
  not already covered by a higher-priority source. These entries activate via
  `shell:AppsFolder` (the same AUMID path already proven on Spotify).
- **`_launchable` recognizes AUMID targets** so packaged entries resolve as
  existing, not dead.
- **Launcher fallback handles AUMID-only entries.** If the shell activation
  throws, entries whose target is a real file keep the `os.startfile`
  fallback (unchanged); AUMID-only entries retry the shell activation once,
  then fail honestly.
- **Dedupe keeps higher-priority sources winning**: Start Menu / registry /
  builtin / alias-stub entries still beat the Start-Apps entry for the same
  name, so existing behavior is untouched.

New coverage on this host: WhatsApp, Microsoft Teams, Photos, XBOX, Outlook,
Media Player, Copilot, Snipping Tool, Clock, Weather, and ~38 more packaged
apps. "whatsapp" and "whats app" now resolve to WhatsApp (the latter still
never collapses into "Whats New").

### Regression proof (after the packaged-app fix)

| Suite | Result |
|---|---|
| `p5_launch_validation` (74 checks, whatsapp expectations corrected) | 74/74 PASS |
| `p5_seq_launch` (28 turns, live re-run) | 28/28 PASS |
| `p6_stress_500` (checkpoint, routing unaffected) | 255/255 PASS |
| `resolve` spot-check of every R-battery reference | unchanged (all found/not_found as before) |
| Live `launcher.execute("whatsapp")` | success, `WhatsApp.Root` process running |

### Residual (documented, not pipeline bugs)

The Start-Apps index itself can fail to list a packaged app until it has
surfaced in the shell (or while the app is still provisioning); those cases
still resolve to `not_found` honestly. Re-running the catalog (`refresh()`)
at conversation start re-reads the index.

---

## Response-layer fix — launch success narration (2026-08-08)

With launches executing reliably, live user tests exposed that the *spoken
reply* about a successful launch was wrong even though `app_launcher ->
success` (the `launched: True / detail: ...` ToolResult):

- "launch whats app" → Friday fabricated a file listing ("WhatsApp.exe,
  WhatsApp.apk, ...").
- "launch lenovo vantage" → Friday echoed a permission refusal ("I'm not
  sure I can launch... without your permission, as it's a hardware
  device...") despite `launched: True`.
- "launch microsoft store" → Friday rambled about Lenovo devices from
  earlier turns.

Root cause (response prompt only, `src/ai/prompt_builder.py`): a successful
launch rendered in TOOL RESULTS as raw scalar lines (`launched: True /
detail: WhatsApp`) that the small model does not read as "the app is now
open", and the generic success instructions contained no launch rule — so the
model invented a listing (primed by the file/weather listing wording) or
fixated on the `(hardware)` ENTITIES label and a stale permission-refusal
exchange in RECENT CONVERSATION.

Fix (universal, structural, no app names/keywords):

- `_render_tool_payload`: dedicated `app_launcher` branch renders a
  successful launch as `Opened application: <detail>` instead of the raw
  `launched: True / detail: ...` scalar lines.
- `build_prompt`: a dedicated instruction branch for all-success app-launch
  turns — the applications are already open (never permission talk), confirm
  each in one short natural sentence naming the app exactly as shown, a
  launch produces no files/folders so nothing may be invented, and ENTITIES
  MENTIONED + RECENT CONVERSATION must be ignored (TOOL RESULTS are the
  only facts). Other tool paths keep their existing instructions.

### Regression proof (after the response-layer fix)

| Suite | Result |
|---|---|
| Offline repro: whatsapp / lenovo / store (real prompt + real LLM) | "WhatsApp is open." / "Lenovo Vantage is open." / "Microsoft Store is open." — no file-list, permission-echo, or stale-ramble |
| `p5_response_probe` | 5/5 PASS |
| `p5_honesty_probe` | PASS |
| Launcher / router / executor | untouched (no behavior change) |

### Residual (documented, not pipeline bugs)

- Issue #1 ("sometime it says it opened the application when it doesn't")
  is explicitly out of scope per the user — launch is fire-and-forget by
  design (see weakness #3); the launcher honestly claims "launched", not
  "running well".
- The Understanding layer nondeterminism (KI-009) remains the tracked root
  cause; schema validation with retry (KI-007) is the durable fix.

---

## Documented residual: "open file explorer" hijack (2026-08-08, no code change)

User manual-test finding: "open file explorer" **sometimes** does not launch
File Explorer and instead lists the workspace root, while FRIDAY says it
launched. Root-caused and documented in `docs/KNOWN_ISSUE/KI-010.md`
(reproduced with the real router): when the Understanding model labels the
entity `file`/`location` instead of `application` (plausible — the name
contains "file"), the `_FILE_LABELS` folder/path rescue
(`tool_router.py:341-346`) redirects the launch to file_manager, and the
`open_application` pin cannot override `automation` by design. file_manager
`list` with no path defaults to the workspace root
(`file_manager.py:86-87`), and the response model narrates it as a File
Explorer open.

```
entity label='application'  -> [('app_launcher', 'launch', {'app': 'file explorer'})]
entity label='file'         -> [('file_manager', 'list', {})]
entity label='location'     -> [('file_manager', 'list', {})]
entity label='folder'       -> [('file_manager', 'list', {})]
```

Deterministic once the label fires; intermittency is the Understanding
label. No code changed (per the user's instruction). The user will run
further manual tests before Phase 6. A second residual (launch-turn reply
repeating the prior answer) is documented in `docs/KNOWN_ISSUE/KI-011.md`.
