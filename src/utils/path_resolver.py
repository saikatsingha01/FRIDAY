# ==========================================================
# UNIVERSAL FILESYSTEM REFERENCE RESOLVER
#
# Phase 5 stabilization — resolves a user-facing filesystem
# reference (absolute path, drive letter, known folder, or
# folder/file name) to an absolute path on the machine, or to
# a structured miss.
#
# No project-specific names, no keyword hacks, and NO silent
# fallback: when a reference cannot be resolved it is an
# explicit not_found, never an implicit listing of the
# workspace. The workspace is only one candidate root in the
# name search, and only when the user's reference actually
# names it.
#
# Deterministic and read-only: never executes anything.
# ==========================================================

import os
import re
import string
import uuid
from collections import deque
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ResolvedPath:
    found: bool
    path: Optional[str] = None
    kind: Optional[str] = None      # "dir" | "file"
    reason: Optional[str] = None    # how the reference was resolved
    error: Optional[str] = None     # "empty" | "not_found" | None
    # For absolute/known-folder refs the target may not exist yet
    # (e.g. write creates it). `path` still carries the resolved
    # target, and `exists` records whether it is already on disk so
    # read/list/locate can stay honest while write/delete proceed.
    exists: bool = False


@dataclass
class LocateCandidate:
    """
    One real filesystem entry a locate reference could point at.
    `match` classifies how well the requested reference maps to it:
      - "exact"     whole-name equality
      - "normalized" only spelling/format differs ("srczip" -> "src.zip",
                     "rootfile dot txt" -> "rootfile.txt")
      - "fuzzy"     a partial/token containment match
    """
    path: str
    kind: Optional[str] = None
    match: str = "fuzzy"


@dataclass
class LocateResult:
    """
    Result of a LOCATE resolution. Every path it carries is a real
    filesystem entry that exists RIGHT NOW. `candidates` holds every
    relevant match (exact/normalized first, fuzzy only when no better
    one exists) so the caller can honestly report "multiple matches".
    """
    found: bool
    path: Optional[str] = None
    kind: Optional[str] = None
    match: Optional[str] = None
    candidates: List[LocateCandidate] = field(default_factory=list)
    requested: Optional[str] = None
    error: Optional[str] = None      # "empty" | "not_found" | None


# The assistant's own workspace, used only as (a) the meaning of
# "project / workspace" references and (b) a candidate root in the
# name search. Never a silent default.
_WORKSPACE_BASE = os.path.normpath(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    )
)

# Words that carry no identifying meaning in a folder/file name.
_STOPWORDS = {
    "the", "a", "an", "my", "your", "our", "its", "this", "that",
    "folder", "folders", "directory", "directories", "dir", "drive",
    "in", "on", "of", "at", "for", "from", "to", "under", "into",
    "inside", "within", "here", "please", "tell", "show", "me",
    "all", "are", "is", "what", "which", "with", "pc", "computer",
    "laptop", "system", "machine", "hard", "disk", "device",
    # Grammar connectors and question words a full spoken sentence
    # can carry ("and", "whats", "how"). The tool_router strips these
    # as frame words too, so a direct resolver call on the raw
    # sentence must behave the same. Single letters ("i", "a") are
    # deliberately NOT here — they can be a folder's name letter
    # ("friday probe i folder"). "or" is also NOT here: it is a real
    # token of names like "or_with_else", and dictating that file
    # ("or underscore with underscore else") must still resolve it.
    "and", "but", "not", "whats", "whose", "why", "how",
    "when", "who", "installed",
    # Action verbs and frame words a full spoken sentence can carry.
    # Mirrors the tool_router's frame-word stripping, so a direct
    # resolver call on the raw sentence behaves like the routed one
    # ("find the location of my c projects folder" names the folder,
    # not a file called "find"). Deliberately not "drive" (the "c
    # drive" unit must survive) and not "or" (it is a real token of
    # names like "or_with_else").
    "find", "locate", "search", "look", "read", "open", "list",
    "give", "check", "see", "display", "view", "print", "scan",
    "go", "come", "get", "access", "take", "bring", "grab", "pull",
    "pass", "turn", "say", "stop", "start", "contents", "content",
    # Type descriptors that carry no identifying meaning ("the
    # spiderman 2 game" names a folder "Marvel's Spider-Man 2").
    # Deliberately singular and noun-modifying only: plural forms
    # ("games", "files", "programs") are kept significant because
    # they name real folders ("C:\games", "Program Files"), and
    # "program" is kept so the "Program Files" signature survives.
    "game", "app", "application", "installer", "setup", "exe",
    "executable", "launcher", "tool", "file",
    # Location-frame words: "the location and path of the spiderman 2
    # game" names the game, not a folder called "location" or "path".
    # The tool_router strips these as frame words too, so a direct
    # resolver call on the full sentence must behave the same.
    "location", "path", "where",
}

# Bare references that mean the workspace itself.
_WORKSPACE_ALIASES = {
    "project", "workspace", "current project", "project folder",
    "my project", "my project folder", "this project",
}

# Bare references that mean the process working directory.
_CWD_ALIASES = {
    "here", "current directory", "current folder",
    "current working directory", "working directory", "work folder",
}

# Known user/system folders, mapped to (env_var, subfolder). The
# special shell-known-folder set (desktop/documents/downloads/music/
# pictures/videos) is resolved through the Windows shell so redirected
# folders (OneDrive) resolve to their real location.
_KNOWN_FOLDER_KEYS = {
    "downloads": ("USERPROFILE", "Downloads"),
    "download": ("USERPROFILE", "Downloads"),
    "desktop": ("USERPROFILE", "Desktop"),
    "documents": ("USERPROFILE", "Documents"),
    "document": ("USERPROFILE", "Documents"),
    "music": ("USERPROFILE", "Music"),
    "pictures": ("USERPROFILE", "Pictures"),
    "photos": ("USERPROFILE", "Pictures"),
    "videos": ("USERPROFILE", "Videos"),
    "video": ("USERPROFILE", "Videos"),
    "home": ("USERPROFILE", ""),
    "user": ("USERPROFILE", ""),
    "userprofile": ("USERPROFILE", ""),
    "profile": ("USERPROFILE", ""),
    "public": ("PUBLIC", ""),
    "temp": ("TEMP", ""),
    "tmp": ("TEMP", ""),
    "appdata": ("APPDATA", ""),
    "local appdata": ("LOCALAPPDATA", ""),
    "program files": ("PROGRAMFILES", ""),
    "program files x86": ("PROGRAMFILES(X86)", ""),
    "windows": ("WINDIR", ""),
    "system32": ("WINDIR", "System32"),
    "system": ("WINDIR", "System32"),
}

# FOLDERID -> the Windows shell known-folder GUID, resolved through
# SHGetKnownFolderPath so OneDrive-redirected folders resolve to their
# real location.
_SHELL_FOLDER_IDS = {
    "desktop": "B4BFCC3A-DB2C-424C-B029-7FE99A87C641",
    "documents": "FDD39AD0-238F-46AF-ADB4-6C85480369C7",
    "downloads": "374DE290-123F-4565-9164-39C4925E467B",
    "music": "4BD8D571-6D19-48D3-BE97-422220080E43",
    "pictures": "33E28130-4E1E-4676-835A-98395C3BC3BB",
    "videos": "18989B1D-99B5-455B-841C-AB7C74E4DDFC",
}

# Singular / alternate spellings of a shell known folder map to the
# canonical key above, so "photos" resolves through the shell just
# like "pictures" (the env-var fallback alone is wrong when the
# folder is OneDrive-redirected and C:\Users\<user>\Pictures does not
# exist).
_SHELL_KEY_ALIASES = {
    "photo": "pictures",
    "photos": "pictures",
    "picture": "pictures",
    "doc": "documents",
    "document": "documents",
    "download": "downloads",
    "video": "videos",
    "my documents": "documents",
    "my desktop": "desktop",
    "my downloads": "downloads",
    "my pictures": "pictures",
    "my photos": "pictures",
    "my videos": "videos",
    "my music": "music",
}


def _shell_known_folder(key):
    """
    Real location of a shell known folder via SHGetKnownFolderPath,
    so OneDrive-redirected folders resolve to their real location.
    Returns None on any failure (non-Windows, missing folder, ...).
    """
    try:
        import ctypes

        guid_str = _SHELL_FOLDER_IDS.get(key)
        if guid_str is None:
            return None

        u = uuid.UUID(guid_str).int

        class _GUID(ctypes.Structure):
            _fields_ = [
                ("Data1", ctypes.c_ulong),
                ("Data2", ctypes.c_ushort),
                ("Data3", ctypes.c_ushort),
                ("Data4", ctypes.c_ubyte * 8),
            ]

        g = _GUID()
        g.Data1 = (u >> 96) & 0xFFFFFFFF
        g.Data2 = (u >> 80) & 0xFFFF
        g.Data3 = (u >> 64) & 0xFFFF
        tail = u & 0xFFFFFFFFFFFFFFFF
        data4 = (ctypes.c_ubyte * 8)()
        for i in range(8):
            data4[i] = (tail >> (8 * (7 - i))) & 0xFF
        g.Data4 = data4

        shell32 = ctypes.windll.shell32
        shell32.SHGetKnownFolderPath.argtypes = [
            ctypes.POINTER(_GUID), ctypes.c_ulong, ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_wchar_p),
        ]
        shell32.SHGetKnownFolderPath.restype = ctypes.c_long

        ppsz = ctypes.c_wchar_p()
        hr = shell32.SHGetKnownFolderPath(
            ctypes.byref(g), 0, None, ctypes.byref(ppsz)
        )
        if hr != 0 or not ppsz.value:
            return None
        path = ppsz.value
        ctypes.windll.ole32.CoTaskMemFree(ppsz)
        return path
    except Exception:
        return None


def _known_folder(text):
    sig = _signature(text)

    shell = _shell_known_folder(_SHELL_KEY_ALIASES.get(sig, sig))
    if shell and os.path.isdir(shell):
        return os.path.normpath(shell)

    spec = _KNOWN_FOLDER_KEYS.get(sig)
    if spec is None:
        return None
    base = os.environ.get(spec[0])
    if not base:
        return None
    return os.path.normpath(os.path.join(base, spec[1])) if spec[1] else os.path.normpath(base)

# "c drive", "c:", "c:\" — a single-letter drive reference.
_DRIVE_WORD_RE = re.compile(
    r"\b([a-zA-Z]):(?=[\\/]|\s|$)|(?<![a-zA-Z])([a-zA-Z])\s+drive\b",
    re.IGNORECASE,
)

_ABSOLUTE_RE = re.compile(r"^[a-zA-Z]:[\\/]")

_PATH_SEPARATORS = re.compile(r"[\\/]")


def _tokens(text):
    return re.findall(r"[a-z0-9]+", str(text).lower())


def _significant_tokens(text):
    return [t for t in _tokens(text) if t not in _STOPWORDS]


def _signature(text):
    return " ".join(_significant_tokens(text))


def _kind(path):
    try:
        return "dir" if os.path.isdir(path) else "file"
    except OSError:
        return "file"


def _extract_drive(text):
    """
    Pulls a drive reference out of the text: "c drive", "c:", "c:\".
    Returns (drive_root or None, remaining_text).
    """
    match = _DRIVE_WORD_RE.search(text)
    if not match:
        return None, text
    letter = (match.group(1) or match.group(2)).upper()
    rest = text[:match.start()] + " " + text[match.end():]
    return f"{letter}:\\", rest


def _drive_roots():
    roots = []
    for letter in string.ascii_uppercase:
        root = f"{letter}:\\"
        if os.path.isdir(root):
            roots.append(root)
    return roots


def _search_roots(drive=None):
    """
    Candidate roots for a name search, most specific first.
    A drive-scoped search checks only that drive; otherwise every
    available drive root, then the user profile, then PUBLIC, then
    the workspace. The workspace is a candidate like any other —
    it is never a default when nothing matches.
    """
    roots = []
    if drive:
        if os.path.isdir(drive):
            roots.append(drive)
        return roots
    roots.extend(_drive_roots())
    for var in ("USERPROFILE", "PUBLIC"):
        path = os.environ.get(var)
        if path and os.path.isdir(path):
            roots.append(os.path.normpath(path))
    if os.path.isdir(_WORKSPACE_BASE):
        base = os.path.normpath(_WORKSPACE_BASE)
        if base not in roots:
            roots.append(base)
    return roots


# Dictated separator words ("underscore", "dot", "hyphen") map to the
# symbols they spell. The Understanding layer / whisper often writes a
# folder name the user dictated aloud ("rock underscore paper underscore
# caesar" for a folder literally named "rock_paper_caesar"). Universal —
# any spoken separator, any folder name.
_SPOKEN_SYMBOLS = {
    "dot": ".", "underscore": "_", "hyphen": "-", "dash": "-",
    "slash": "/", "backslash": "\\",
}


def _spoken_filename(tokens):
    """
    "rootfile dot txt" -> "rootfile.txt"; "rock underscore paper
    underscore caesar" -> "rock_paper_caesar". When every spoken
    separator word sits between two alphanumeric tokens, returns the
    translated string with each separator symbol in its place. A
    separator REPLACES the space it was dictated in ("zsq code dot c"
    -> "zsq code.c": the space between "zsq" and "code" survives, the
    dot takes the place of the space before "c"). Returns None
    otherwise (no separators, or one dangling at an edge).
    """
    if len(tokens) < 3:
        return None
    indexes = [i for i, tok in enumerate(tokens) if tok in _SPOKEN_SYMBOLS]
    if not indexes:
        return None
    for idx in indexes:
        if idx == 0 or idx == len(tokens) - 1:
            return None
        if not tokens[idx - 1].isalnum() or not tokens[idx + 1].isalnum():
            return None
    out = []
    prev_sep = False
    for tok in tokens:
        if tok in _SPOKEN_SYMBOLS:
            out.append(_SPOKEN_SYMBOLS[tok])
            prev_sep = True
        else:
            if out and not prev_sep:
                out.append(" ")
            out.append(tok)
            prev_sep = False
    return "".join(out)


def normalize_spoken_reference(text):
    """
    Public dictation normalization: "rock underscore paper underscore
    caesar" -> "rock_paper_caesar". Returns the text unchanged when no
    spoken separator is present.
    """
    translated = _spoken_filename(_tokens(str(text)))
    return translated if translated else str(text)


def _token_hit(token, name):
    """
    True when one significant token of a spoken reference matches a name
    token of a directory entry — by equality, or by containment when both
    are substantial enough (>=3 chars) to carry meaning. Used by the
    tolerant follow-up match: a single whisper/STT drift in one token
    ("caesar" for "seizor") must not hide a directory the user just saw.
    """
    name_tokens = _tokens(name)
    return any(
        token == nt
        or (len(token) >= 3 and len(nt) >= 3 and (token in nt or nt in token))
        for nt in name_tokens
    )


def _tokens_match(name, tokens, exact=False):
    name_tokens = _tokens(name)
    if not name_tokens:
        return False
    if exact:
        return name_tokens == tokens
    # A requested token matches a name token by equality, or by
    # containment when BOTH tokens are substantial enough (>=3 chars)
    # to carry meaning. A one- or two-character token never matches by
    # containment, so "or" can never be absorbed by a name like
    # "or_with_else.py" (a dictated "rockpaperscissors" produced that
    # false hit), and "src" never matches a name like "c game".
    # A short token still matches by exact equality, so a folder
    # genuinely named "or" resolves when asked for by that name.
    #
    # A fused dictation ("cprojects" for "c projects", "rockpaperscissors"
    # for "rock paper scissors") matches because the query token carries
    # enough of the folder's name tokens inside it — the covered length
    # must be at least half the query token. A garbage word like
    # "flibberwibble" can never absorb a 3-letter folder name like "lib",
    # because a single 3-character fragment covers far less than half of
    # it. The reverse direction (a query token that is a prefix/slice of
    # a longer name token) is accepted only when the query token is at
    # least half the name token, so a drifted short token still finds its
    # folder without letting fragments match unrelated words.
    for tok in tokens:
        hit = False
        for nt in name_tokens:
            if tok == nt:
                hit = True
                break
            if len(tok) >= 3 and len(nt) >= 3:
                if nt in tok:
                    covered = sum(
                        len(o) for o in name_tokens
                        if len(o) >= 3 and o in tok
                    )
                    if covered >= len(tok) / 2:
                        hit = True
                        break
                elif tok in nt and len(tok) >= len(nt) / 2:
                    hit = True
                    break
        if not hit:
            return False
    return True


# ==========================================================
# CONVERSATION SCOPE
#
# Session state recording the most recently listed directory
# (set by the file_manager tool after a successful directory
# listing). A follow-up that refers to an entry the user just
# saw listed — "whats inside that rock underscore paper
# underscore caesar directory" right after a listing of python
# projects — falls back to a tolerant, bounded match inside
# this directory when every normal resolution missed. Universal:
# any parent, any entry name. It is never consulted while a real
# name, known folder, drive, or absolute path resolves, so it can
# never shadow a genuine match.
# ==========================================================

_last_listed_scope = None


def set_last_listed_scope(path):
    """Records the directory most recently listed. Directories only."""
    global _last_listed_scope
    if path is None:
        _last_listed_scope = None
        return
    if path and os.path.isdir(path):
        _last_listed_scope = os.path.normpath(path)


def last_listed_scope():
    """The most recently listed directory, or None."""
    return _last_listed_scope


def _scoped_followup_search(scope, tokens):
    """
    Tolerant, bounded match for a follow-up that refers to an entry
    the user just saw listed inside `scope` ("whats inside that rock
    underscore paper underscore caesar directory" right after the
    parent was listed). A single token of whisper/STT drift ("caesar"
    for "seizor") must not hide that entry: the reference needs a
    strict majority of its significant tokens to hit ONE entry, and
    two entries tying for the top hit count is an ambiguous miss,
    never a guess. Returns the matching path or None.
    """
    if not scope or not tokens or not os.path.isdir(scope):
        return None
    try:
        names = os.listdir(scope)
    except OSError:
        return None
    scored = []
    for name in names:
        hits = sum(1 for tok in tokens if _token_hit(tok, name))
        if hits > 0:
            scored.append((hits, os.path.join(scope, name)))
    if not scored:
        return None
    scored.sort(key=lambda item: (item[0], len(item[1])), reverse=True)
    best_hits = scored[0][0]
    required = max(2, len(tokens) // 2 + 1)
    if best_hits < required:
        return None
    tied = [path for hits, path in scored if hits == best_hits]
    if len(tied) > 1:
        return None
    return tied[0]


# Directories never descended during a deep name search: system,
# cache, or package-manager trees that are huge and almost never the
# home of a user-named folder. Case-insensitive comparisons.
_SKIP_DIRS = {
    ".git", ".svn", ".hg", "node_modules", "venv", ".venv", ".tox",
    "$recycle.bin", "system volume information", "appdata",
    "windows", "winsxs", "msocache", "recovery", "perflogs",
    "config.msi", "windows.old", "$windows.~bt", "programdata",
    "boot", "efi",
}

_DEEP_MAX_DEPTH = 6
_DEEP_MAX_ENTRIES = 5000


def _deep_entries(root):
    """
    Bounded breadth-first walk over ONE root yielding
    (path, name, is_dir) for every entry up to _DEEP_MAX_DEPTH,
    skipping _SKIP_DIRS, and never visiting more than
    _DEEP_MAX_ENTRIES entries (safety cap so a huge drive cannot
    stall a name search). Depth and budget are per root, so a deep
    nested folder that sits at the depth limit from a drive root is
    still reachable from a more specific root (the profile), and a
    huge drive cannot starve the other roots' searches.

    The walk is LEVEL-ORDER (breadth-first), so the entry budget is
    spent across the breadth of a root first: a huge subtree can
    never consume the whole budget before a sibling subtree's folder
    is seen ("C:\\python prog\\or_with_else.py" is a child of a
    top-level dir and is always found before the walk runs out in
    Program Files). A depth-first walk let one huge subtree starve
    every other candidate.
    """
    seen = set()
    count = 0
    queue = deque([(root, 0)])
    while queue and count < _DEEP_MAX_ENTRIES:
        dirpath, depth = queue.popleft()
        if depth >= _DEEP_MAX_DEPTH:
            continue
        try:
            with os.scandir(dirpath) as it:
                entries = list(it)
        except OSError:
            continue
        for entry in entries:
            count += 1
            try:
                is_dir = entry.is_dir(follow_symlinks=False)
            except OSError:
                is_dir = False
            yield entry.path, entry.name, is_dir
            if is_dir and entry.name.lower() not in _SKIP_DIRS:
                if entry.path not in seen:
                    seen.add(entry.path)
                    queue.append((entry.path, depth + 1))


def _name_search(roots, tokens):
    """
    Exact name match first (whole name equals the reference), then
    normalized match (case/separator-insensitive key equality), then
    a fuzzy token match (every significant token appears in the name).
    Shallow (one level) search first, then a bounded deep search so a
    nested folder like C:\\games\\Marvel's Spider-Man 2 is still found.
    Each root is walked independently (own depth + budget), so a folder
    nested under the profile is found even when the drive-root walk
    never reaches it. Returns the first match, or None.
    """
    shallow = []
    for root in roots:
        try:
            names = os.listdir(root)
        except OSError:
            continue
        for name in names:
            shallow.append((os.path.join(root, name), name))
    # Tier 1: exact token match
    for path, name in shallow:
        if _tokens_match(name, tokens, exact=True):
            return path
    # Tier 2: normalized key match (case/separator-insensitive)
    needle = " ".join(tokens)
    needle_norm = _norm_key(needle)
    for path, name in shallow:
        if _norm_key(name) == needle_norm:
            return path
    # Tier 3: fuzzy token match
    for path, name in shallow:
        if _tokens_match(name, tokens, exact=False):
            return path
    # Deep search: same tier order
    for exact in (True, False):
        for root in roots:
            for path, name, _is_dir in _deep_entries(root):
                if _tokens_match(name, tokens, exact=exact):
                    return path
    # Deep normalized
    for root in roots:
        for path, name, _is_dir in _deep_entries(root):
            if _norm_key(name) == needle_norm:
                return path
    return None


def _norm_key(text):
    """Case/separator-insensitive key: 'src.zip' == 'srczip'."""
    return re.sub(r"[^a-z0-9]", "", str(text).lower())


def _levenshtein_ratio(a: str, b: str) -> float:
    """
    Normalized Levenshtein similarity ratio (0.0 to 1.0).
    Used for phonetic/approximate matching when normalized keys are close.
    """
    if not a or not b:
        return 0.0
    # Ensure a is the shorter string
    if len(a) > len(b):
        a, b = b, a
    # Quick length-based early exit
    if len(b) - len(a) > len(b) * 0.4:
        return 0.0
    previous_row = list(range(len(b) + 1))
    for i, ca in enumerate(a):
        current_row = [i + 1]
        for j, cb in enumerate(b):
            insert_cost = current_row[j] + 1
            delete_cost = previous_row[j + 1] + 1
            replace_cost = previous_row[j] + (ca != cb)
            current_row.append(min(insert_cost, delete_cost, replace_cost))
        previous_row = current_row
    distance = previous_row[-1]
    max_len = max(len(a), len(b))
    return 1.0 - (distance / max_len)


def _match_kind(name, reference, tokens):
    """
    Classifies how a located name relates to the requested reference:
    "exact" (whole-name equality), "normalized" (only spelling/format
    differs, e.g. "srczip" vs "src.zip"), else "fuzzy" (a token
    containment/partial match).
    """
    if _tokens_match(name, tokens, exact=True):
        return "exact"
    if _norm_key(name) == _norm_key(reference):
        return "normalized"
    return "fuzzy"


def _match_confidence(name, reference, tokens, match_kind):
    """
    Returns a confidence score (0.0 to 1.0) for a match.
    Used to distinguish high-confidence fuzzy matches from low-confidence ones.
    """
    if match_kind == "exact":
        return 1.0
    if match_kind == "normalized":
        return 0.95
    # Fuzzy: use Levenshtein on normalized keys + token overlap
    name_norm = _norm_key(name)
    ref_norm = _norm_key(reference)
    lev_ratio = _levenshtein_ratio(name_norm, ref_norm)
    # Token overlap bonus
    name_tokens = set(_tokens(name))
    ref_tokens = set(tokens)
    if name_tokens and ref_tokens:
        overlap = len(name_tokens & ref_tokens) / len(name_tokens | ref_tokens)
    else:
        overlap = 0.0
    # Weighted combination
    return min(0.85, 0.6 * lev_ratio + 0.4 * overlap)


def _collect_name_matches(roots, tokens, reference, limit=4, norm=False):
    """
    All relevant real entries matching a reference, in a deterministic
    order (shallow before deep, then alphabetical). Match tiers:
    1. Exact (whole-name token equality)
    2. Normalized (case/separator-insensitive key equality)
    3. Fuzzy (token containment, both tokens >=3 chars)
    Exact/normalized candidates win; fuzzy matches are returned ONLY
    when no exact or normalized candidate exists, so an ambiguous
    fuzzy pool never crowds out a genuine same-name hit. Bounded by `limit`.
    """
    if norm:
        needle = _norm_key(reference)
    else:
        needle = None
    exact_paths = []
    norm_paths = []
    fuzzy_paths = []
    seen = set()

    def _consider(name, path):
        if path in seen:
            return
        seen.add(path)
        if norm:
            if _norm_key(name) == needle:
                norm_paths.append(path)
            return
        if _tokens_match(name, tokens, exact=True):
            exact_paths.append(path)
        elif _norm_key(name) == _norm_key(reference):
            norm_paths.append(path)
        elif _tokens_match(name, tokens, exact=False):
            fuzzy_paths.append(path)

    shallow = []
    for root in roots:
        try:
            names = os.listdir(root)
        except OSError:
            continue
        for name in names:
            shallow.append((os.path.join(root, name), name))
    for path, name in shallow:
        _consider(name, path)
    for root in roots:
        for path, name, _is_dir in _deep_entries(root):
            _consider(name, path)

    # Priority: exact > normalized > fuzzy
    pool = exact_paths or norm_paths or fuzzy_paths
    pool.sort(key=lambda p: (len(os.path.dirname(p)), p.lower()))
    return pool[:limit]


def _locate_result(paths, tokens, requested, match=None):
    """
    Builds a LocateResult from real candidate paths. The primary path
    is the first (most specific) candidate; `match` classifies it.
    Low-confidence fuzzy matches are filtered out.
    """
    candidates = []
    for path in paths:
        kind = _kind(path)
        m = match or _match_kind(os.path.basename(path), requested, tokens)
        conf = _match_confidence(os.path.basename(path), requested, tokens, m)
        # Only include fuzzy matches with reasonable confidence (>= 0.6)
        if m == "fuzzy" and conf < 0.6:
            continue
        candidates.append(LocateCandidate(path=path, kind=kind, match=m))
    if not candidates:
        return LocateResult(False, requested=requested, error="not_found")
    primary = candidates[0]
    return LocateResult(
        found=True,
        path=primary.path,
        kind=primary.kind,
        match=primary.match,
        candidates=candidates,
        requested=requested,
    )


def locate_reference(reference, scope=None) -> LocateResult:
    """
    LOCATE resolution: returns the real filesystem entry (or every
    relevant entry) the reference maps to. Unlike resolve_reference it
    only ever reports paths that EXIST on disk right now, distinguishes
    exact / normalized / fuzzy matches, and collects multiple matches
    so a duplicate-name file can be reported honestly instead of
    silently picking the first one. Never raises.
    """
    if scope is None:
        scope = _last_listed_scope

    if reference is None:
        return LocateResult(False, requested=None, error="empty")

    text = str(reference).strip()

    if not text:
        return LocateResult(False, requested=text, error="empty")

    # ---- 1. absolute path ---- exists right now, or an honest miss
    if _is_absolute_path(text):
        expanded = os.path.expandvars(os.path.expanduser(text))
        path = os.path.normpath(os.path.abspath(expanded))
        if not os.path.exists(path):
            return LocateResult(False, requested=text, error="not_found")
        return LocateResult(
            True, path, _kind(path), "exact", requested=text,
        )

    # ---- 2. known folder ----
    known = _known_folder(text)
    if known is not None:
        if not os.path.isdir(known):
            return LocateResult(False, requested=text, error="not_found")
        return LocateResult(
            True, known, "dir", "exact", requested=text,
        )

    # ---- 3. drive reference ("c drive", "c:", "c:\") ----
    drive, rest = _extract_drive(text)
    if drive:
        if not os.path.isdir(drive):
            return LocateResult(False, requested=text, error="not_found")
        tokens = _significant_tokens(rest)
        if not tokens:
            return LocateResult(
                True, drive, "dir", "exact", requested=text,
            )
        paths = _collect_name_matches([drive], tokens, rest)
        if paths:
            return _locate_result(paths, tokens, text)
        return LocateResult(False, requested=text, error="not_found")

    # A bare single letter is a drive ("c" -> C:\).
    if len(text) == 1 and text.lower() in string.ascii_lowercase:
        root = f"{text.upper()}:\\"
        if os.path.isdir(root):
            return LocateResult(True, root, "dir", "exact", requested=text)
        return LocateResult(False, requested=text, error="not_found")

    tokens = _significant_tokens(text)
    sig = " ".join(tokens)

    # ---- 4. workspace / cwd aliases ----
    if text.lower() in _WORKSPACE_ALIASES or sig in _WORKSPACE_ALIASES:
        if os.path.isdir(_WORKSPACE_BASE):
            return LocateResult(
                True, _WORKSPACE_BASE, "dir", "exact", requested=text,
            )
        return LocateResult(False, requested=text, error="not_found")
    if text.lower() in _CWD_ALIASES or sig in _CWD_ALIASES:
        cwd = os.getcwd()
        if os.path.isdir(cwd):
            return LocateResult(
                True, os.path.normpath(cwd), "dir", "exact", requested=text,
            )
        return LocateResult(False, requested=text, error="not_found")

    # ---- 5. explicit relative path ----
    if _PATH_SEPARATORS.search(text) or text in (".", "..", "~"):
        expanded = os.path.expandvars(os.path.expanduser(text))
        if text == "~":
            expanded = os.path.expanduser("~")
        bases = []
        for candidate in (os.getcwd(), _WORKSPACE_BASE):
            candidate = os.path.normpath(candidate)
            if candidate not in bases:
                bases.append(candidate)
        for base in bases:
            path = os.path.normpath(os.path.join(base, expanded))
            if os.path.exists(path):
                return LocateResult(
                    True, path, _kind(path), "exact", requested=text,
                )
        return LocateResult(False, requested=text, error="not_found")

    # ---- 6. name search (multi-match) ----
    if not tokens:
        return LocateResult(False, requested=text, error="not_found")

    paths = _collect_name_matches(_search_roots(), tokens, text)
    if paths:
        return _locate_result(paths, tokens, text)

    # ---- 6a. spoken "name dot ext" -> "name.ext" ----
    spoken = _spoken_filename(_tokens(text))
    if spoken:
        spoken_paths = _collect_name_matches(
            _search_roots(), _significant_tokens(spoken), spoken,
            norm=True,
        )
        if spoken_paths:
            return _locate_result(
                spoken_paths, _significant_tokens(spoken), text,
                match="normalized",
            )
        tokens = _significant_tokens(spoken)

    # ---- 6b. "<name> <known folder>" scoped search ----
    if len(tokens) >= 2:
        known = _known_folder(tokens[-1])
        if known and os.path.isdir(known):
            scoped = _collect_name_matches(
                [known], tokens[:-1], " ".join(tokens[:-1]),
            )
            if scoped:
                return _locate_result(scoped, tokens[:-1], text)

    # ---- 6c. conversation-scoped follow-up ----
    # A follow-up that refers to an entry the user just saw listed
    # ("whats inside that <name> directory" right after the parent was
    # listed). A single token of whisper/STT drift ("caesar" for
    # "seizor") must not hide that entry: the reference needs a strict
    # majority of its significant tokens to hit ONE entry, and two
    # entries tying for the top hit count is an ambiguous miss, never
    # a guess. ONLY triggered when the user explicitly references the
    # previous listing with deictic words ("that", "this", "those",
    # "these", "it", "there"). NOT a general fallback for failed
    # directory queries.
    _DEICTIC_RE_LOC = re.compile(r"\b(that|this|those|these|it|there)\b", re.IGNORECASE)
    if scope and _DEICTIC_RE_LOC.search(text):
        scoped = _scoped_followup_search(scope, tokens)
        if scoped:
            return LocateResult(
                True, scoped, _kind(scoped), "exact", requested=text,
            )

    return LocateResult(False, requested=text, error="not_found")


def _is_absolute_path(text):
    if _ABSOLUTE_RE.match(text):
        return True
    return text.startswith("\\\\") or text.startswith("/")


def resolve_reference(reference, scope=None) -> ResolvedPath:
    """
    Resolve a user-facing filesystem reference to an absolute path
    or a structured miss. Never raises.

    `scope` (optional) is the directory to consult for a tolerant
    follow-up match when every normal resolution misses — the
    directory the user most recently had listed. When None, the
    resolver uses the session's most recently listed directory.
    """
    if scope is None:
        scope = _last_listed_scope

    if reference is None:
        return ResolvedPath(False, error="empty")

    text = str(reference).strip()

    if not text:
        return ResolvedPath(False, error="empty")

    # ---- 1. absolute path ("C:\...", "C:/...", "\\server\...") ----
    if _is_absolute_path(text):
        expanded = os.path.expandvars(os.path.expanduser(text))
        path = os.path.normpath(os.path.abspath(expanded))
        exists = os.path.exists(path)
        return ResolvedPath(
            True, path, _kind(path) if exists else None,
            "absolute", exists=exists,
        )

    # ---- 2. known folder ("downloads", "my desktop", "temp") ----
    known = _known_folder(text)
    if known is not None and os.path.isdir(known):
        return ResolvedPath(True, known, "dir", "known_folder", exists=True)

    # ---- 3. drive reference ("c drive", "c:", "c:\") ----
    drive, rest = _extract_drive(text)
    if drive:
        if not os.path.isdir(drive):
            return ResolvedPath(False, error="not_found")
        tokens = _significant_tokens(rest)
        if not tokens:
            return ResolvedPath(True, drive, "dir", "drive", exists=True)
        match = _name_search([drive], tokens)
        if match:
            return ResolvedPath(
                True, match, _kind(match), "name_search", exists=True,
            )
        return ResolvedPath(False, error="not_found")

    # A bare single letter is a drive ("c" -> C:\).
    if len(text) == 1 and text.lower() in string.ascii_lowercase:
        root = f"{text.upper()}:\\"
        if os.path.isdir(root):
            return ResolvedPath(True, root, "dir", "drive", exists=True)
        return ResolvedPath(False, error="not_found")

    tokens = _significant_tokens(text)
    sig = " ".join(tokens)

    # ---- 4. workspace / cwd aliases (matched on the raw words, so
    # "here" is not swallowed as a stopword) ----
    if text.lower() in _WORKSPACE_ALIASES or sig in _WORKSPACE_ALIASES:
        if os.path.isdir(_WORKSPACE_BASE):
            return ResolvedPath(
                True, _WORKSPACE_BASE, "dir", "workspace", exists=True,
            )
        return ResolvedPath(False, error="not_found")
    if text.lower() in _CWD_ALIASES or sig in _CWD_ALIASES:
        cwd = os.getcwd()
        if os.path.isdir(cwd):
            return ResolvedPath(
                True, os.path.normpath(cwd), "dir", "cwd", exists=True,
            )
        return ResolvedPath(False, error="not_found")

    # ---- 5. explicit relative path ("logs\file.txt", "src") ----
    if _PATH_SEPARATORS.search(text) or text in (".", "..", "~"):
        expanded = os.path.expandvars(os.path.expanduser(text))
        if text == "~":
            expanded = os.path.expanduser("~")
        bases = []
        for candidate in (os.getcwd(), _WORKSPACE_BASE):
            candidate = os.path.normpath(candidate)
            if candidate not in bases:
                bases.append(candidate)
        for base in bases:
            path = os.path.normpath(os.path.join(base, expanded))
            exists = os.path.exists(path)
            return ResolvedPath(
                True, path, _kind(path) if exists else None,
                "relative", exists=exists,
            )
        return ResolvedPath(False, error="not_found")

    # ---- 6. name search across drive roots, profile, workspace ----
    if not tokens:
        return ResolvedPath(False, error="not_found")

    match = _name_search(_search_roots(), tokens)
    if match:
        return ResolvedPath(
            True, match, _kind(match), "name_search", exists=True,
        )

    # ---- 6a. spoken "name dot ext" -> "name.ext" ----
    # "rootfile dot txt" is how a user dictates "rootfile.txt". Only
    # tried when the plain name search missed, and only when the
    # translated form actually exists, so a folder genuinely named
    # "dot" is never shadowed by this rule. The scope is passed
    # through so a dictated follow-up ("rock underscore paper
    # underscore caesar") can still be matched tolerantly inside the
    # directory the user just listed. The FULL tokens are translated
    # (not the stopword-stripped ones), so a stopword that is part of
    # a dictated name survives: "or underscore with underscore else"
    # must translate to "or_with_else", never "or__else".
    spoken = _spoken_filename(_tokens(text))
    if spoken:
        spoken_path = resolve_reference(spoken, scope=scope)
        if spoken_path.found:
            return spoken_path
        tokens = _significant_tokens(spoken)

    # ---- 6b. "<name> <known folder>" scoped search ----
    # "friday probe e desktop" means "friday probe e, located in my
    # desktop" — the trailing known-folder word scopes the search to
    # that folder instead of being a name token. Only tried when the
    # unscoped search missed, so a folder literally named "documents"
    # is still found by its own name first.
    if len(tokens) >= 2:
        known = _known_folder(tokens[-1])
        if known and os.path.isdir(known):
            scoped = _name_search([known], tokens[:-1])
            if scoped:
                return ResolvedPath(
                    True, scoped, _kind(scoped), "name_search", exists=True,
                )

    # ---- 6c. conversation-scoped follow-up ----
    # A follow-up that refers to an entry the user just saw listed
    # ("whats inside that <name> directory" right after a listing)
    # runs a tolerant, bounded match inside the most recently listed
    # directory. ONLY when the user explicitly references the previous
    # listing with deictic words ("that", "this", "those", "these",
    # "it", "there"). NOT a general fallback for failed directory queries.
    _DEICTIC_RE_RES = re.compile(r"\b(that|this|those|these|it|there)\b", re.IGNORECASE)
    if scope and _DEICTIC_RE_RES.search(text):
        scoped = _scoped_followup_search(scope, tokens)
        if scoped:
            return ResolvedPath(
                True, scoped, _kind(scoped), "name_search", exists=True,
            )

    return ResolvedPath(False, error="not_found")


# ==========================================================
# PUBLIC DEBUG VIEW
# ==========================================================

def describe(reference) -> str:
    """Compact, structured description of a resolution for logs."""
    resolved = resolve_reference(reference)
    if resolved.error == "empty":
        return "requested: <none>  resolved: <none>  reason: empty_path"
    if not resolved.found:
        return (
            f"requested: {reference}  resolved: <none>  "
            f"reason: not_found"
        )
    return (
        f"requested: {reference}  resolved: {resolved.path}  "
        f"reason: {resolved.reason}"
    )
