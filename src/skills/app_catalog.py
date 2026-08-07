# ==========================================================
# UNIVERSAL APPLICATION CATALOG
#
# Phase 5 — data-driven discovery + semantic resolution of
# installed applications on the host.
#
# The launcher never hardcodes application names or aliases.
# Instead it builds an internal catalog of installed apps from
# standard Windows sources, then resolves a user's natural
# reference against that catalog with generic matching rules
# (spacing / punctuation / capitalization / partial names /
# small typos / common abbreviations). When several apps match
# with similar confidence it returns an ambiguity instead of
# guessing.
#
# Sources (all data-driven, none require manual lists):
#   - Start Menu shortcuts            (%APPDATA%, %ProgramData%)
#   - Desktop shortcuts               (user + public)
#   - Installed applications          (registry Uninstall keys)
#   - Windows Apps                    (%LOCALAPPDATA%\\WindowsApps)
#   - Start-Apps index                (Get-StartApps packaged apps —
#     WhatsApp, Teams, Photos, ... have no alias stub, so the shell
#     index is the source that discovers them; they activate by AUMID)
#   - Steam installed games           (steamapps library manifests)
#   - Epic Games installed games      (Epic manifests)
#   - A tiny set of fixed Windows OS
#     utilities (File Explorer, Notepad, Calculator, ...) —
#     universal binaries present on every install, not
#     user-installed applications.
# ==========================================================

import json
import os
import re
import shutil
from difflib import SequenceMatcher

try:
    import winreg
except ImportError:  # pragma: no cover - Windows-only module
    winreg = None

# ----------------------------------------------------------
# WINDOWS OS UTILITIES
# Universal, fixed shell utilities — every Windows install has
# these. Not user-installed applications, so listing them here
# is universal rather than application-specific. wt.exe is
# included conditionally (only when present on PATH).
# ----------------------------------------------------------

_BUILTINS = [
    {"name": "File Explorer", "target": "explorer.exe", "source": "builtin"},
    {"name": "Notepad", "target": "notepad.exe", "source": "builtin"},
    {"name": "Calculator", "target": "calc.exe", "source": "builtin"},
    {"name": "Command Prompt", "target": "cmd.exe", "source": "builtin"},
    {"name": "Windows PowerShell", "target": "powershell.exe", "source": "builtin"},
    {"name": "Settings", "target": "ms-settings:", "source": "builtin"},
    {"name": "Control Panel", "target": "control.exe", "source": "builtin"},
    {"name": "Windows Terminal", "target": "wt.exe", "source": "builtin"},
]

# Universal English/Windows-generic nouns that name an OS
# utility without naming the app (never brand names). Kept
# deliberately small.
_BUILTIN_SYNONYMS = {
    "file explorer": "File Explorer",
    "file manager": "File Explorer",
    "files": "File Explorer",
    "explorer": "File Explorer",
    "my computer": "File Explorer",
    "this pc": "File Explorer",
    "computer": "File Explorer",
    "cmd": "Command Prompt",
    "command prompt": "Command Prompt",
    "terminal": "Windows Terminal",
    "powershell": "Windows PowerShell",
    "power shell": "Windows PowerShell",
    "settings app": "Settings",
    "settings": "Settings",
    "control panel": "Control Panel",
}

# Filler words never part of an application's identity and safe
# to drop from any reference.
_FILLER = {
    "the", "a", "an", "please", "open", "launch", "start", "run",
    "me", "my",
}

# Category words that only ever qualify a name ("chrome browser",
# "steam program"). They may be skipped by the aligned matcher.
_SKIPPABLE_CATEGORY = {"browser", "program"}

# Category words that are frequently genuine name parts ("WhatsApp",
# "File Manager", "Media Player") and therefore must always pin a
# real name token. References like "whats app" resolve through the
# concatenation rule ("whatsapp") rather than by dropping the word.
_PIN_CATEGORY = {"app", "application", "manager", "viewer", "player"}

_STEAM_DEFAULTS = [
    r"C:\Program Files (x86)\Steam",
    r"C:\Program Files\Steam",
]

_EPIC_MANIFEST_DIR = r"C:\ProgramData\Epic\EpicGamesLauncher\Data\Manifests"


def _norm(value):
    text = re.sub(r"[^a-z0-9 ]", " ", str(value or "").lower())
    return re.sub(r"\s+", " ", text).strip()


def _tokens(value):
    return set(_norm(value).split())


def _launchable(target):
    """True when os.startfile can plausibly run this target."""
    if not target:
        return False
    if re.match(r"^[a-zA-Z]+://", target):
        return True
    if target.endswith(":"):
        return True
    if "!" in target and "/" not in target and "\\" not in target:
        # Packaged-app AUMID ("PublisherPrefix.Package_...!App"),
        # activated through shell:AppsFolder by the launcher.
        return True
    if os.path.isfile(target):
        return True
    if shutil.which(target):
        return True
    return False


def _resolve_lnk(_path):
    # A .lnk file is itself launchable via os.startfile — we do
    # not need to parse the shortcut target.
    return _path


class AppCatalog:

    def __init__(self):
        self._entries = []
        self._built = False
        self._start_apps_cache = None

    # ======================================================
    # DISCOVERY
    # ======================================================

    def build(self):
        entries = [dict(e) for e in _BUILTINS]

        # Universal synonyms resolve to their canonical builtin only
        # when that utility is actually launchable on this host.
        for synonym, canonical in _BUILTIN_SYNONYMS.items():
            match = next(
                (e for e in entries if e["name"] == canonical), None
            )
            if match and _launchable(match["target"]):
                entries.append({
                    "name": synonym,
                    "target": match["target"],
                    "source": "builtin",
                })

        entries += self._discover_shortcuts()
        entries += self._discover_registry()
        entries += self._discover_windows_apps()
        entries += self._discover_steam()
        entries += self._discover_epic()
        entries += self._discover_start_apps(
            {_norm(e["name"]) for e in entries})

        self._entries = self._dedupe(entries)
        self._built = True
        return self

    def refresh(self):
        self._built = False
        return self.build()

    def _discover_shortcuts(self):
        found = []
        roots = []

        appdata = os.environ.get("APPDATA")
        if appdata:
            roots.append(os.path.join(
                appdata, r"Microsoft\Windows\Start Menu\Programs"))
        programdata = os.environ.get("ProgramData")
        if programdata:
            roots.append(os.path.join(
                programdata, r"Microsoft\Windows\Start Menu\Programs"))
        user_profile = os.environ.get("USERPROFILE")
        if user_profile:
            roots.append(os.path.join(user_profile, "Desktop"))
        public = os.environ.get("PUBLIC")
        if public:
            roots.append(os.path.join(public, "Desktop"))

        seen = set()
        for root in roots:
            if not os.path.isdir(root):
                continue
            for dirpath, _dirs, files in os.walk(root):
                for fname in files:
                    if not fname.lower().endswith(".lnk"):
                        continue
                    path = os.path.join(dirpath, fname)
                    key = os.path.normcase(path)
                    if key in seen:
                        continue
                    seen.add(key)
                    name = os.path.splitext(fname)[0]
                    found.append({
                        "name": name,
                        "target": _resolve_lnk(path),
                        "source": "start_menu",
                    })
        return found

    def _discover_registry(self):
        if winreg is None:
            return []
        found = []
        roots = [
            (winreg.HKEY_LOCAL_MACHINE,
             r"Software\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE,
             r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER,
             r"Software\Microsoft\Windows\CurrentVersion\Uninstall"),
        ]

        for hive, subkey in roots:
            try:
                key = winreg.OpenKey(hive, subkey)
            except OSError:
                continue
            index = 0
            while True:
                try:
                    app_key_name = winreg.EnumKey(key, index)
                except OSError:
                    break
                index += 1
                try:
                    app_key = winreg.OpenKey(key, app_key_name)
                except OSError:
                    continue
                entry = self._registry_entry(app_key)
                if entry is not None:
                    found.append(entry)

        return found

    def _registry_entry(self, app_key):
        def read(name):
            try:
                value, _type = winreg.QueryValueEx(app_key, name)
                return value
            except OSError:
                return None

        display_name = read("DisplayName")
        if not display_name:
            return None

        icon = read("DisplayIcon") or ""
        icon = icon.strip("\"'")
        icon = re.sub(r",\d+$", "", icon)  # strip icon resource index

        install = read("InstallLocation") or ""
        if not icon and install and os.path.isdir(install):
            icon = install

        target = None
        if icon and os.path.isfile(icon) and icon.lower().endswith(".exe"):
            target = icon
        elif install and os.path.isdir(install):
            # Best-effort: an .exe directly under InstallLocation.
            candidates = [
                os.path.join(install, fname)
                for fname in os.listdir(install)
                if fname.lower().endswith(".exe")
                and os.path.isfile(os.path.join(install, fname))
            ]
            if candidates:
                target = sorted(candidates)[0]

        if not target:
            return None

        return {
            "name": str(display_name).strip(),
            "target": target,
            "source": "registry",
        }

    def _start_apps_index(self):
        """
        The shell's Start-Apps index (display name -> AppID), read
        once per process. Source for both the AUMID map used by the
        WindowsApps alias scanner and the standalone packaged-app
        discovery source (_discover_start_apps).
        """
        if self._start_apps_cache is not None:
            return self._start_apps_cache
        items = []
        try:
            import subprocess
            proc = subprocess.run(
                [
                    "powershell", "-NoProfile", "-NonInteractive",
                    "-Command",
                    "$OutputEncoding=[Console]::OutputEncoding="
                    "[System.Text.Encoding]::UTF8; "
                    "Get-StartApps | ConvertTo-Json",
                ],
                capture_output=True,
                timeout=45,
                creationflags=0x08000000,  # CREATE_NO_WINDOW
            )
            text = proc.stdout.decode("utf-8", errors="replace")
            data = json.loads((text or "").strip() or "[]")
            if isinstance(data, dict):
                data = [data]
            for item in data:
                name = (item.get("Name") or "").strip()
                aid = (item.get("AppID") or "").strip()
                if name and aid and not re.match(
                        r"^[a-zA-Z]+://", aid):
                    items.append({"name": name, "aumid": aid})
        except Exception:
            pass
        self._start_apps_cache = items
        return items

    def _start_apps_aumids(self):
        """Display name (lowercased) -> AUMID from the Start-Apps index."""
        return {
            item["name"].lower(): item["aumid"]
            for item in self._start_apps_index()
        }

    def _discover_windows_apps(self):
        found = []
        candidates = []
        local = os.environ.get("LOCALAPPDATA")
        if local:
            candidates.append(os.path.join(
                local, r"Microsoft\WindowsApps"))
            candidates.append(os.path.join(
                local, r"Microsoft\Windows\Apps"))
        program_files = os.environ.get("ProgramFiles")
        if program_files:
            candidates.append(os.path.join(
                program_files, "WindowsApps"))

        aumids = self._start_apps_aumids()

        seen = set()
        for apps in candidates:
            if not os.path.isdir(apps):
                continue
            for fname in sorted(os.listdir(apps)):
                if not fname.lower().endswith(".exe"):
                    continue
                if fname in seen:
                    continue
                seen.add(fname)
                name = os.path.splitext(fname)[0]
                # WindowsApps alias files are tiny shims; keep them
                # only as a fallback source (lowest priority). The
                # AUMID enables reliable packaged-app activation.
                found.append({
                    "name": name,
                    "target": os.path.join(apps, fname),
                    "source": "windowsapps",
                    "aumid": aumids.get(name.lower(), None),
                })
        return found

    def _discover_start_apps(self, existing):
        """
        Packaged (Store / MSIX) apps from the shell's Start-Apps
        index. Many packaged apps — WhatsApp Desktop, Microsoft Teams,
        Photos, Copilot, ... — expose no WindowsApps alias .exe stub,
        so the stub scanner alone never discovers them. Every Start-app
        has an AppID; packaged apps are the ones whose AppID is a real
        AUMID (contains '!'), and they are activated reliably through
        shell:AppsFolder by the launcher. Entries already covered by a
        higher-priority source (Start Menu / registry / builtin / stub)
        are skipped so the catalog stays lean.
        """
        found = []
        for item in self._start_apps_index():
            aumid = item["aumid"]
            if "!" not in aumid:
                continue
            key = _norm(item["name"])
            if not key or key in existing:
                continue
            found.append({
                "name": item["name"],
                "target": aumid,
                "source": "windowsapps",
                "aumid": aumid,
            })
        return found

    def _discover_steam(self):
        import configparser
        found = []
        steam_dir = self._find_steam()
        if not steam_dir:
            return found

        library_paths = self._steam_library_paths(steam_dir)

        for library in library_paths:
            manifests = os.path.join(library, "steamapps")
            if not os.path.isdir(manifests):
                continue
            for fname in os.listdir(manifests):
                if not (fname.startswith("appmanifest_")
                        and fname.endswith(".acf")):
                    continue
                path = os.path.join(manifests, fname)
                try:
                    parser = configparser.ConfigParser()
                    parser.optionxform = str
                    parser.read(path, encoding="utf-8-sig")
                    app_state = parser["AppState"]
                    name = app_state.get("name", "").strip()
                    appid = app_state.get("appid", "").strip()
                except Exception:
                    continue
                if not name or not appid:
                    continue
                found.append({
                    "name": name,
                    "target": f"steam://rungameid/{appid}",
                    "source": "steam",
                })
        return found

    def _find_steam(self):
        for path in _STEAM_DEFAULTS:
            if os.path.isfile(os.path.join(path, "steam.exe")):
                return path

        # Fall back to the registry InstallLocation (data-driven).
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Valve\Steam",
            )
            value, _type = winreg.QueryValueEx(key, "SteamPath")
            if value and os.path.isfile(os.path.join(value, "steam.exe")):
                return value
        except OSError:
            pass

        return None

    def _steam_library_paths(self, steam_dir):
        paths = []
        vdf = os.path.join(steam_dir, "steamapps", "libraryfolders.vdf")
        if os.path.isfile(vdf):
            for match in re.finditer(
                r'"path"\s+"((?:[^"\\]|\\.)+)"',
                open(vdf, "r", encoding="utf-8", errors="replace").read(),
            ):
                raw = match.group(1)
                raw = raw.replace("\\\\", "\\")
                if os.path.isdir(raw):
                    paths.append(raw)

        # The default library always counts.
        default = os.path.join(steam_dir, "steamapps")
        if os.path.isdir(default) and default not in paths:
            paths.append(steam_dir)
        return paths

    def _discover_epic(self):
        found = []
        if not os.path.isdir(_EPIC_MANIFEST_DIR):
            return found
        for fname in os.listdir(_EPIC_MANIFEST_DIR):
            if not fname.lower().endswith(".item"):
                continue
            path = os.path.join(_EPIC_MANIFEST_DIR, fname)
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    manifest = json.load(f)
            except Exception:
                continue
            name = (manifest.get("DisplayName") or "").strip()
            location = (manifest.get("InstallLocation") or "").strip()
            executable = (manifest.get("LaunchExecutable") or "").strip()
            if not name or not executable:
                continue
            target = executable
            if location and not os.path.isabs(executable):
                target = os.path.join(location, executable)
            if not os.path.isfile(target):
                continue
            found.append({
                "name": name,
                "target": target,
                "source": "epic",
            })
        return found

    def _dedupe(self, entries):
        # One entry per normalized name, keeping the highest-priority
        # launchable (start-menu shortcuts are the most reliable).
        priority = {
            "start_menu": 0, "registry": 1, "builtin": 2,
            "steam": 3, "epic": 4, "windowsapps": 5,
        }
        keep = {}
        for entry in entries:
            name_key = _norm(entry["name"])
            if not name_key:
                continue
            existing = keep.get(name_key)
            if existing is None:
                keep[name_key] = entry
                continue
            if priority.get(entry["source"], 9) < priority.get(
                    existing["source"], 9):
                keep[name_key] = entry
        return list(keep.values())

    # ======================================================
    # RESOLUTION
    # ======================================================

    def resolve(self, query):
        """
        Resolve a user's natural application reference against the
        catalog.

        Returns a dict:
          {"status": "found",     "target": str, "label": str}
          {"status": "ambiguous", "label": str, "candidates": [str]}
          {"status": "not_found", "label": str}

        Never guesses: close ties return an ambiguity.
        """
        if not self._built:
            self.build()

        raw = str(query or "").strip()

        if not raw:
            return {"status": "not_found", "label": "", "candidates": []}

        # A literal path / URI is used directly — the user pointed
        # at a concrete launchable.
        if self._looks_like_path(raw):
            return {"status": "found", "target": raw,
                    "label": os.path.basename(raw)}

        scored = self._score(raw)

        if not scored:
            return {"status": "not_found", "label": raw, "candidates": []}

        scored = self._collapse_duplicates(scored)

        best = scored[0]
        second = scored[1] if len(scored) > 1 else None

        if best["score"] < 82:
            return {"status": "not_found", "label": raw, "candidates": []}

        if second is not None and (best["score"] - second["score"]) < 12:
            candidates = [
                e["label"] for e in scored
                if best["score"] - e["score"] < 12
            ]
            return {
                "status": "ambiguous",
                "label": raw,
                "candidates": candidates,
            }

        return {
            "status": "found",
            "target": best["target"],
            "label": best["label"],
            "aumid": best.get("aumid") or None,
        }

    def _looks_like_path(self, raw):
        if os.path.exists(raw):
            return True
        if re.match(r"^[a-zA-Z]:[\\/]", raw):
            return True
        if "/" in raw or "\\" in raw:
            return True
        if raw.lower().endswith((".exe", ".lnk", ".url", ".bat",
                                 ".cmd", ".msi")):
            return True
        if re.match(r"^[a-zA-Z]+://", raw):
            return True
        return False

    def _score(self, query):
        query_norm = _norm(query)
        query_clean = _norm(" ".join(
            token for token in _norm(query).split()
            if token not in _FILLER))
        query_order = query_clean.split() or query_norm.split()
        query_tokens = set(query_order)
        multi_token = len(query_tokens) > 1

        scored = []

        for entry in self._entries:
            name_norm = _norm(entry["name"])
            name_tokens = _tokens(entry["name"])
            name_order = name_norm.split()

            if not name_tokens:
                continue

            score = self._match(query_clean, query_norm, query_tokens,
                                query_order, name_norm, name_tokens,
                                name_order, multi_token)

            if score > 0:
                scored.append({
                    "score": score,
                    "label": entry["name"],
                    "target": entry["target"],
                    "aumid": entry.get("aumid") or None,
                    "exists": _launchable(entry["target"]),
                    "tokens": len(name_tokens),
                })

        # Prefer the canonical shorter name and an existing launchable
        # when scores tie.
        scored.sort(key=lambda e: (-e["score"], e["tokens"], -int(e["exists"])))
        return scored

    def _collapse_duplicates(self, scored):
        """
        Vendor/parenthetical duplicates (\"Visual Studio Code\" vs
        \"Microsoft Visual Studio Code (User)\", \"Microsoft Edge\"
        vs \"Microsoft Edge WebView2 Runtime\") are the same app
        surfacing through several install sources. When two near-tied
        candidates (within the ambiguity band) are token-subset
        duplicates and both matched strongly, keep only the canonical
        shorter one instead of asking the user to pick between
        copies of one app.
        """
        kept = []
        for entry in scored:
            dropped = False
            for other in scored:
                if other is entry:
                    continue
                mine = _tokens(entry["label"])
                theirs = _tokens(other["label"])
                if (
                    mine and theirs
                    and len(mine) - len(theirs) <= 2
                    and theirs.issubset(mine)
                    and abs(entry["score"] - other["score"]) < 12
                ):
                    # This entry is the longer duplicate of a canonical
                    # shorter name that is already in the running list.
                    dropped = True
                    break
            if not dropped:
                kept.append(entry)
        return kept or scored

    def _match(self, query_clean, query_norm, query_tokens, query_order,
               name_norm, name_tokens, name_order, multi_token=False):
        best = 0

        # 1. Exact.
        if query_clean == name_norm or query_norm == name_norm:
            best = max(best, 100)

        # 2. Query tokens all present in the name tokens.
        if query_tokens and query_tokens.issubset(name_tokens):
            best = max(best, 90 if len(query_tokens) == len(name_tokens)
                       else 85)

        # 3. Aligned abbreviation / partial-name match ("vs code" ->
        #    "visual studio code", "spiderman 2" -> "spider man 2",
        #    "chrome browser" -> "google chrome"). Each query token
        #    must pin a distinct name token in order. Short-form
        #    tokens ("vs") and fuzzy pins are only accepted for
        #    multi-token queries (or substring pins for a long single
        #    token like "vscode"), so a lone "vs" or a word like
        #    "chrome" never hijacks an unrelated app.
        if query_order and self._aligned_match(
                query_order, name_order, multi_token):
            best = max(best, 86)

        # 4. Prefix / substring.
        if name_norm.startswith(query_clean):
            best = max(best, 82)
        if query_clean in name_norm:
            best = max(best, 78)
        if name_norm in query_clean:
            best = max(best, 74)

        # 5. Compound concatenation in natural token order
        #    ("spiderman2" -> "spider man 2"). A trailing category
        #    word may be appended compactly instead ("whats app" ->
        #    "whatsapp"), so WhatsApp resolves when installed while
        #    "whats app" can never collapse into a shorter unrelated
        #    name. Deliberately capped below the confident-found
        #    threshold.
        name_concat = "".join(name_norm.split())
        concat_variants = {query_clean}
        for token in query_order:
            if token in _PIN_CATEGORY and token == query_order[-1]:
                concat_variants.add("".join(
                    t for t in query_order if t != token) + token)
        for variant in concat_variants:
            if variant == name_concat:
                best = max(best, 84)
            elif len(variant) >= 5 and name_concat.startswith(variant):
                best = max(best, 76)

        # 6. Token-level fuzzy (small typos): every query token
        #    fuzzy-matches a distinct name token. Multi-token queries
        #    are reliable (each token pins a name token). A lone fuzzy
        #    token is capped low so a short word never hijacks an
        #    unrelated app ("chrome" must not match "home"); a single
        #    near-identical long token (typo like "chorme" or
        #    "calclator") pinning a name token of at least 5 chars is
        #    accepted as a confident hit.
        if not multi_token:
            token = next(iter(query_tokens))
            if len(token) >= 2:
                pin_ratio, pin_len = self._single_pin(token, name_tokens)
                if pin_ratio >= 0.78:
                    if pin_ratio >= 0.8 and pin_len >= 5:
                        best = max(best, 84)
                    else:
                        best = max(best, 72)
        else:
            fuzzy_ratio = self._token_fuzzy(query_tokens, name_tokens)
            if fuzzy_ratio:
                best = max(best, 80)

        # 7. Whole-string fuzzy (capped below the confident threshold).
        ratio = SequenceMatcher(None, query_clean, name_norm).ratio()
        if ratio >= 0.62:
            best = max(best, min(70, int(ratio * 70)))

        return best

    def _aligned_match(self, query_order, name_order, multi_token):
        """
        Ordered pinning: each query token must match a distinct name
        token, in name order. Accepted token forms (strict ->
        relaxed):
          exact, prefix,
          fuzzy (>=0.78) — multi-token queries only (and the pinned
            name token must be at least 5 chars so a common word like
            "chrome" can never pin a short token like "home"), or for
            a long (>=6 chars) single token that pins a name token
            fully contained in it ("vscode" -> "code");
          short form ("vs" -> "visual") — multi-token queries only.
        Skipping name tokens is allowed so "spiderman 2" can pin
        "spider" in "Marvel's Spider-Man 2". Category words
        ("browser", "program") are skipped freely, but at least one
        real query token must pin a name token — a query made up
        entirely of category words ("browser") matches nothing.
        """
        cursor = 0
        pinned_any = False
        for token in query_order:
            if token in _SKIPPABLE_CATEGORY:
                continue
            if len(token) < 2 and not token.isdigit():
                return False
            matched = False
            for index in range(cursor, len(name_order)):
                name_token = name_order[index]
                fuzzy = SequenceMatcher(None, token, name_token).ratio()
                substring_pin = (
                    not multi_token
                    and len(token) >= 6
                    and (name_token in token or token in name_token)
                )
                if (
                    token == name_token
                    or (name_token.startswith(token))
                    or (substring_pin and fuzzy >= 0.78)
                    or (
                        multi_token
                        and fuzzy >= 0.78
                        and len(name_token) >= 5
                    )
                    or (
                        multi_token
                        and len(token) <= 2
                        and len(name_token) >= 4
                        and name_token.startswith(token[0])
                    )
                ):
                    cursor = index + 1
                    matched = True
                    pinned_any = True
                    break
            if not matched:
                return False
        return pinned_any

    def _single_pin(self, token, name_tokens):
        """Best (ratio, length) over all name tokens for one token."""
        best = (0.0, 0)
        for name_token in name_tokens:
            ratio = SequenceMatcher(None, token, name_token).ratio()
            if ratio > best[0]:
                best = (ratio, len(name_token))
        return best

    def _token_fuzzy(self, query_tokens, name_tokens):
        """Best overall ratio when every query token fuzzy-matches a
        distinct name token; 0.0 when no full pin exists."""
        available = list(name_tokens)
        ratios = []
        for token in query_tokens:
            if len(token) < 2:
                if any(name_token == token for name_token in available):
                    available.remove(token)
                    continue
                return 0.0
            best_ratio = 0.0
            picked = None
            for name_token in available:
                ratio = SequenceMatcher(None, token, name_token).ratio()
                if ratio > best_ratio:
                    best_ratio = ratio
                    picked = name_token
            if picked is None or best_ratio < 0.78:
                return 0.0
            ratios.append(best_ratio)
            available.remove(picked)
        return min(ratios) if ratios else 0.0

    def _synonym_lookup(self, query):
        canonical = _BUILTIN_SYNONYMS.get(_norm(query))
        if canonical is None:
            return None
        for entry in self._entries:
            if entry["name"] == canonical:
                return entry
        return None

    # ======================================================
    # ACCESS
    # ======================================================

    def entries(self):
        if not self._built:
            self.build()
        return list(self._entries)

    def stats(self):
        if not self._built:
            self.build()
        counts = {}
        for entry in self._entries:
            counts[entry["source"]] = counts.get(entry["source"], 0) + 1
        return counts


app_catalog = AppCatalog()
