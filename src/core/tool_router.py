# ==========================================================
# TOOL ROUTER
#
# Phase 5 — Tool Intelligence.
#
# The ToolRouter SELECTS tools. It never decides whether tools
# are needed (that is Reasoning's job via reasoning.use_tools /
# reasoning.use_web) and it never executes anything (that is the
# ExecutionManager's job).
#
# Deterministic and universal:
#   - reads structured Understanding fields (capability, goal, intent,
#     entities) and structured Reasoning flags;
#   - normalizes the Understanding layer's off-enum capability
#     variants (KI-007 pattern) onto canonical capabilities;
#   - selects tools through their registered metadata
#     (capability -> tool), so adding a tool is a metadata
#     declaration, never a router edit;
#   - the ONLY raw-text touch is a narrow launch gate (KI-009): when
#     the Understanding model has dropped every structured signal on
#     a repeat launch, a literal "open/launch X" prefix keeps the
#     device path alive. The recovered reference still runs through
#     the safe resolver, so a bad extraction degrades to an honest
#     miss — never a wrong launch. No keywords, no hardcoded apps.
#
# Returns a list of ToolRequest objects (possibly empty).
# ==========================================================

import re

from src.skills import skill_registry
from src.skills.skill_loader import ensure_loaded
from src.contracts.tool import ToolRequest
from src.utils.path_resolver import resolve_reference


# ==========================================================
# CAPABILITY NORMALIZATION
#
# The Understanding layer emits free-form capability labels
# (KI-007). Map the observed variants onto canonical capabilities
# so routing can match tool metadata. Canonical values pass
# through unchanged.
# ==========================================================

_CAPABILITY_VARIANTS = {
    "searching":          "web",
    "information":        "web",
    "web_search":         "web",
    "search":             "web",
    "weather":            "web",
    "news":               "web",
    "current_events":     "web",
    "prices":             "web",
    "stock":              "web",
    "stocks":             "web",
    "forecast":           "web",
    "finance":            "web",
    "information retrieval": "web",
    "information_retrieval": "web",
    "cooking":            "web",
    "file_system":        "automation",
    "filesystem":         "automation",
    "file management":    "automation",
    "file_system_ops":    "automation",
    "file_manager":       "automation",
    "file operations":    "automation",
    "exploration":        "automation",
    "file exploration":   "automation",
    "device_control":     "device",
    "system_control":     "system",
    "terminal":           "system",
    "app_launcher":       "device",
    "app_launch":         "device",
    "automation":         "automation",
    "tool_use":           "tool_use",
}

# Canonical capability -> tool routing. Tools register via
# metadata.capabilities; this table is the deterministic order
# of preference when several tools could serve one capability.
# Tools not listed here are never auto-selected.
_CAPABILITY_TO_TOOL = {
    "web":        "web_search",
    "device":     "app_launcher",
    "system":     "terminal",
    "automation": "file_manager",
    "tool_use":   "file_manager",
}


def _norm(value):
    if value is None:
        return ""
    return str(value).strip().lower()


def _canonical_capability(capability):
    raw = _norm(capability)
    if raw in _CAPABILITY_VARIANTS:
        return _CAPABILITY_VARIANTS[raw]
    return raw


def _entity_texts(understanding):
    entities = []
    for entity in (understanding.semantic.entities or []):
        if isinstance(entity, dict):
            text = entity.get("text")
        else:
            text = getattr(entity, "text", None)
        if text:
            entities.append(str(text).strip())
    return [e for e in entities if e]


def _entity_items(understanding):
    """
    Entities as (text, label) pairs. Labels let the router rescue
    structured misclassifications deterministically (e.g. a command
    entity mislabeled device, or a search query mislabeled as an app
    launch) without ever reading raw text.
    """
    items = []
    for entity in (understanding.semantic.entities or []):
        if isinstance(entity, dict):
            text = entity.get("text")
            label = entity.get("label")
        else:
            text = getattr(entity, "text", None)
            label = getattr(entity, "label", None)
        if text and str(text).strip():
            items.append((str(text).strip(), (label or "").strip().lower()))
    return items


# Entity labels that prove a "device" turn is actually a command
# the user wants run (misclassified terminal intent). Routed to the
# terminal tool instead of the app launcher.
_COMMAND_LABELS = {"command", "command_line", "shell", "cli"}

# Entity labels that prove a "device" turn is actually a file-system
# operation (misclassified app launch): the user pointed at a folder
# or path, not an application. Routed to file_manager instead.
_FILE_LABELS = {"location", "file", "folder", "directory", "path"}

# Entity TEXT that proves the same thing even when the Understanding
# model labeled the entity "application" (it conflates "photos folder"
# with the File Explorer app). Matches structured entity text — a
# folder/path token never names a real app, so this is safe.
_FOLDER_TEXT_HINT = re.compile(r"(folder|directory|(?:^|[\\/])[^\\/]*[\\/])", re.IGNORECASE)

# Raw-text phrasing that is an unambiguous filesystem query — the user
# asks WHAT'S INSIDE / CONTENTS OF / LIST / READ a folder or file. The
# small Understanding model drifts these turns to device (open_application
# with an "application" entity), memory, or hardware; the user's own
# words are the only reliable signal (same narrow raw-text gate
# philosophy as the launch gate, KI-009). A verb + a folder/file word
# together are required, so a launch ("open notepad"), a web question
# ("what is the weather like"), or chat ("read me a story") never match.
_FS_QUERY_TEXT_RE = re.compile(
    r"\bwhat'?s\s+inside\b"
    r"|\bwhat\s+is\s+inside\b"
    r"|\bcontents?\s+of\b"
    r"|\b(?:list|show|read)\b[^.]*\b(folder|directory|file|"
    r"desktop|downloads?|documents?)\b",
    re.IGNORECASE,
)

# Entity labels that name a filesystem object the user wants listed,
# read, or located. The Understanding prompt maps folder/file names to
# "location"; observed drift emits "folder"/"directory"/"file"/"path".
# Used to build the file_manager path parameter — it is NOT a routing
# signal by itself ("location" also labels world places like "paris").
_FS_PATH_LABELS = {
    "location", "file", "folder", "directory", "dir", "path",
    "drive", "filesystem", "media",
}

# Labels that are unambiguous filesystem-object references for the
# locate rescue (world places are labeled "location" and excluded).
_FS_ENTITY_LABELS = {
    "file", "folder", "directory", "dir", "path", "drive",
    "filesystem", "media",
}

# Location entities that are the machine itself ("my pc", "on my
# computer", "my device") — scope, never the thing being located.
_SCOPE_LOCATION_RE = re.compile(
    r"\b(my\s+)?(pc|computer|laptop|system|machine|device)\b",
    re.IGNORECASE,
)

# Phrases that mean the user wants a filesystem LOCATION — never a
# launch and never a web answer. The small Understanding model drifts
# these turns to goal=open_application / label=application ("tell me
# the location of spiderman 2 in my pc" fired the launcher), so the
# user's own words are the only reliable signal. This is the same
# narrow raw-text gate pattern as the launch gate (KI-009).
_LOCATE_PHRASE = re.compile(
    r"(where\s+(is|are)|where'?s|location\s+of|locate\b|"
    r"find\s+(out\s+)?where|find\s+the\s+(location|path)|"
    r"what'?s\s+the\s+(location|path)|"
    r"tell\s+me\s+(the\s+)?(location|where|path)|"
    r"search\s+(my\s+)?(files|folders|hard\s+drive|drives))",
    re.IGNORECASE,
)

# The strong subset of locate phrasing: an explicit "find the
# location of X" / "locate X" / "search my files" ask. These are
# unambiguous filesystem-locate commands that no genuine world-
# knowledge or web question ever uses — "where is paris" never says
# "find the location of". When present, the turn is pinned to the
# filesystem even if the Understanding model classified it as a web
# search or an app launch (the same narrow raw-text gate philosophy
# as the launch gate, KI-009). The weak forms ("where is X") still
# require a local signal so world-knowledge questions stay web.
_LOCATE_STRONG_RE = re.compile(
    r"(?:find|tell\s+me|what'?s|what\s+is)\s+the\s+"
    r"(?:location|path)(?:\s+and\s+(?:location|path))?\s+of\b"
    r"|\blocate\b"
    r"|\bsearch\s+(?:my\s+)?(?:files|folders|hard\s+drive|drives)\b",
    re.IGNORECASE,
)

# "on my pc" / "in my computer" / "in my device" — an unambiguous
# machine-filesystem scope that never appears in a launch or a
# world-knowledge question.
_MACHINE_SCOPE = re.compile(
    r"\b(on|in)\s+my\s+(pc|computer|laptop|system|machine|device)\b"
    r"|\b(on|in)\s+this\s+(pc|computer|laptop|system|machine|device)\b",
    re.IGNORECASE,
)

# A filesystem-object noun in the user's OWN words ("folder", "file",
# "directory", "desktop", "downloads", "documents", "drive"). A
# world-knowledge question ("where is paris", "where is the eiffel
# tower") never names one, so a locate phrase + a filesystem noun is
# a local-location ask even when the small Understanding model dropped
# every structured label (the "help me the location of assassins creed
# 3 remastered folder" bug: capability=general, no entity labels, and
# the turn fired a web search instead of a local locate).
_FS_NOUN_RE = re.compile(
    r"\b(folders?|director(?:y|ies)|desktop|downloads?|documents?|"
    r"drive|subfolder|subdirectory)\b"
    r"|\bfile\b|\bfiles\b",
    re.IGNORECASE,
)

# Intent/goal words that mean the user wants a file's CONTENT read
# (only when the entity is labeled a file — folders stay listable).
_READ_WORDS = {
    "read", "view", "inspect", "open", "show", "display",
    "contents", "content", "whats", "what's", "what",
}

# Goals where a "location" entity is a place, not a path — the file
# rescue must not hijack a weather/web/knowledge turn that merely
# happened to misclassify as "device".
_NON_FILE_GOALS = {
    "search_web", "search", "weather", "get_weather", "forecast",
    "lookup", "query", "retrieve_web", "find_information",
}

# Entity labels that prove a "device" turn is NOT an app launch —
# a search/system/location intent misclassified as device. No app
# exists to launch; the router must not fire app_launcher.
_NON_APP_LABELS = {
    "query", "system", "location", "place", "city", "country",
    "weather", "topic", "concept", "question", "thing",
}

# The Understanding model's goal for "launch/open <app>" turns.
# When the goal is this exact value, the turn IS an application
# launch no matter what the (noisy) capability label says — a
# local action wins over a web/general misclassification.
_OPEN_APPLICATION_GOAL = "open_application"

# Goals that are unmistakably web searches. When one is present,
# an "application"-labeled entity must NOT be treated as a launch —
# the user explicitly asked to search, not to open.
_EXPLICIT_WEB_GOALS = {"search_web", "retrieve_web", "find_information"}

# Leading words that prefix a spoken app reference ("open chrome",
# "can you launch spotify", "open the file explorer"). Used only by
# the bounded entity-less fallback below — the reference then runs
# through the same safe resolver (found / ambiguous / not_found),
# never against names. "the"/"a" are stripped so article-leading
# references resolve ("open the file explorer" -> "file explorer").
_OPEN_VERBS = {
    "open", "launch", "start", "run", "please", "can", "you",
    "would", "could", "do", "the", "a",
}

# Politeness/attention filler that may precede the launch verb itself
# ("please open spotify", "can you open spotify", "hey open chrome").
# Consumed before the verb check so the raw-text launch gate is
# anchored to a real verb, never to politeness.
_PRE_VERB_FILLER = {
    "please", "can", "could", "would", "will", "do", "hey",
    "okay", "ok", "sure", "yes", "kindly", "you",
}

# The explicit launch verbs that make a turn a launch in the user's
# own words. The pre-launch gate below relies on this: raw text is
# the only signal the Understanding model cannot fabricate.
_LAUNCH_VERBS = {"open", "launch", "start", "run"}

_FALLBACK_TRAILING = {"please", "now", "thanks", "thank", "me", "you"}


def _raw_text_is_launch(raw_text):
    """
    True when the user's own words are an explicit launch command —
    the launch verb is the first meaningful word after optional
    politeness filler ("open spotify", "can you start steam"). This
    is the pre-launch gate that keeps a FABRICATED open_application
    struct on a pure chat turn from ever reaching the launcher: the
    small Understanding model occasionally invents goal="open_application"
    plus an "application" entity ("chrome browser") out of a bare
    conversation turn, and the user's own words are the only signal
    that cannot be hallucinated. No launch verb, no launch.
    """
    if not raw_text:
        return None
    text = re.sub(r"[^a-z0-9 ]", " ", str(raw_text).lower())
    tokens = text.split()
    while tokens and tokens[0] in _PRE_VERB_FILLER:
        tokens.pop(0)
    return bool(tokens and tokens[0] in _LAUNCH_VERBS)


def _fallback_app_reference(raw_text):
    """
    Recovers the app reference from the user's own words when the
    Understanding model dropped the entity for a launch command
    ("open file explorer"). Strips leading verbs / trailing politeness
    and hands the remainder to the resolver, which still returns
    found / ambiguous / not_found — a bad extraction can never launch
    the wrong thing, it degrades to an honest miss.
    """
    if not raw_text:
        return None
    text = re.sub(r"[^a-z0-9 ]", " ", str(raw_text).lower())
    tokens = text.split()
    while tokens and tokens[0] in _OPEN_VERBS:
        tokens.pop(0)
    while tokens and tokens[-1] in _FALLBACK_TRAILING:
        tokens.pop()
    ref = " ".join(tokens).strip()
    if len(ref) >= 2 and any(ch.isalnum() for ch in ref):
        return ref
    return None


def _raw_text_launch_ref(raw_text):
    """
    Recovers an app reference from the raw user text when it is an
    unambiguous launch command ("open spotify", "can you launch
    chrome"). Used ONLY to keep the deterministic launch path alive
    when the Understanding model lost the structured signals on a
    long repeat (KI-009). Two hard gates keep this universal and safe:

      - the text must actually begin with "open" / "launch" (after
        optional politeness filler) — no web request, file query or
        chat turn starts that way;
      - the recovered reference still runs through the safe resolver
        (found / ambiguous / not_found) and folder/path text is
        rejected, so a bad extraction degrades to an honest miss,
        never a wrong launch.

    Returns the reference string, or None.
    """
    if not raw_text:
        return None
    text = re.sub(r"[^a-z0-9 ]", " ", str(raw_text).lower())
    tokens = text.split()
    while tokens and tokens[0] in _PRE_VERB_FILLER:
        tokens.pop(0)
    if not tokens or tokens[0] not in {"open", "launch"}:
        return None
    ref = _fallback_app_reference(" ".join(tokens))
    if not ref:
        return None
    if _FOLDER_TEXT_HINT.search(ref):
        return None
    return ref


def _filesystem_reference(entity_items, action="list"):
    """
    Builds the file_manager path parameter from structured entities.
    Folder/path/location-labeled entities are the reference; machine
    scope words ("my pc") are never the target. For a locate action an
    "application"-labeled entity is also the target (the model
    mislabels the thing being located as an app). Otherwise an
    "application" label only counts when its text is really a
    folder/path token (the model conflates "photos folder" with the
    File Explorer app). Returns a single joined reference string, or
    None when no filesystem reference was extracted.
    """
    parts = []
    for text, label in entity_items:
        if label in _FS_PATH_LABELS:
            if label == "location" and _SCOPE_LOCATION_RE.search(text):
                continue
            parts.append(text)
        elif action == "locate" and label == "application":
            parts.append(text)
        elif label == "application" and _FOLDER_TEXT_HINT.search(text):
            parts.append(text)
    reference = " ".join(parts).strip()
    return reference or None


def _filesystem_action(intent, goal, raw_text, entity_items):
    """
    Picks the file_manager action deterministically:
      - "locate" when the turn asks WHERE something is;
      - "read" when the user asked to open/view a labeled file, OR the
        goal/intent itself is a read request (entities may have been
        dropped — "read my rootfile file" still must read, not list);
      - "list" (the safe default) otherwise.
    """
    text = f"{intent or ''} {goal or ''}".lower()

    if _LOCATE_PHRASE.search(text) or (
        raw_text and _LOCATE_PHRASE.search(raw_text)
    ):
        return "locate"

    labels = {label for _, label in entity_items}

    if "file" in labels and any(word in text for word in _READ_WORDS):
        return "read"

    # The Understanding model expressed a read request through its
    # structured goal/intent, even when it dropped the file entity.
    if any(word in text for word in ("read", "read_file", "readfile")):
        return "read"

    # The user's own words are a read request even when the model
    # classified the turn as an app launch ("read my rootfile dot txt
    # file" -> goal=open_application). A literal "read" verb in the raw
    # text, before a file-ish token, is an unambiguous read.
    if raw_text:
        raw = str(raw_text).lower()
        if re.search(r"\bread\b", raw):
            return "read"

    return "list"


# Conversation-frame words that carry no folder/file identity and are
# stripped when recovering the filesystem reference from the user's own
# words. Never includes folder-name words ("folder", "games", "c drive")
# — the resolver drops what it considers stopwords on its own.
_FS_FRAME_WORDS = {
    # verbs
    "tell", "show", "list", "read", "open", "locate", "find", "give",
    "search", "check", "see", "display", "view", "print", "scan",
    "go", "come", "look", "get", "access", "take", "bring", "grab",
    "pull", "pass", "turn", "say", "stop", "start",
    # modals / politeness / attention
    "can", "could", "would", "will", "do", "does", "did", "may",
    "might", "should", "please", "kindly", "hey", "hello", "okay",
    "ok", "sure", "yes", "yeah", "yep", "no", "nah", "thanks",
    "thank", "now", "then", "just", "only", "some", "all",
    "everything", "anything", "something",
    # pronouns / possessives / articles
    "me", "my", "your", "you", "our", "us", "we", "i", "it", "its",
    "that", "this", "those", "these", "the", "a", "an", "them",
    "they", "him", "her", "their", "there", "here",
    # prepositions
    "of", "in", "on", "for", "from", "to", "at", "with", "into",
    "under", "within", "inside", "about", "up", "down", "by", "over",
    "onto", "upon",
    # linking / copula
    "and", "or", "but", "is", "are", "was", "were", "have", "has",
    "had", "be", "being", "been", "not",
    # question words
    "what", "whats", "which", "where", "whose", "why", "how", "when",
    "who",
    # generic object words that never name a specific folder
    "file", "files", "folder", "folders", "directory", "thing",
    "things", "stuff", "items", "one",
    # filesystem-request frame words (never part of the target name)
    "location", "contents", "content", "path", "permission",
    "permissions", "grant", "granted", "granting",
    # machine-scope words (the resolver treats them as stopwords too).
    # NOTE: "drive" is deliberately NOT stripped — keeping "c drive"
    # as a unit lets the resolver scope the search to C:\ instead of
    # leaving a lone letter that drifts over every drive.
    "pc", "computer", "laptop", "system", "machine", "device",
    "hard", "disk", "installed", "install", "setup",
}


def _raw_filesystem_reference(raw_text, action):
    """
    Recovers a filesystem reference from the user's own words when the
    Understanding model dropped or fragmented the entities (the games
    bug: "whats inside my games folder in my c drive" arrived with no
    entity at all, or with only the "c drive" scope). The stripped
    words still run through the safe resolver — found / not_found only,
    never a guess. A reference needs at least two real tokens, so a
    bare deictic "list the files in there" stays an honest empty miss
    instead of matching some unrelated folder. Returns a string or None.

    A single-letter frame word ("i", "a") is re-attached when it sits
    directly next to a surviving name token ("list what is inside friday
    probe i folder" — the "i" is the folder's name letter, not the
    pronoun; stripping it would silently resolve to a different
    folder). Standalone or article-position letters ("i want...",
    "show me a file") stay stripped.
    """
    if not raw_text:
        return None
    # Apostrophes are merged, not split: a contraction ("what's inside")
    # would otherwise leave a stray single letter ("what s inside") that
    # survives frame-stripping and poisons the reference ("s python
    # project c drive" never resolves, silently falling back to the drive
    # root). "what's" -> "whats" (a frame word), "don't" -> "dont".
    text = re.sub(r"[^a-z0-9 ]", " ", str(raw_text).lower().replace("'", ""))
    tokens = text.split()
    survivors = [tok for tok in tokens if tok not in _FS_FRAME_WORDS]
    survivors_set = set(survivors)
    keep = []
    for idx, tok in enumerate(tokens):
        if tok not in _FS_FRAME_WORDS:
            keep.append(tok)
            continue
        # Re-attach a single-letter frame token ("i", "a") when it sits
        # directly next to a surviving name token — "friday probe i
        # folder": the "i" is the folder's name letter, not the
        # pronoun. Stripping it would silently resolve to a different
        # folder ("friday probe a"). Standalone / article-position
        # letters ("i want...", "show me a file") stay dropped.
        if len(tok) == 1:
            left = tokens[idx - 1] if idx > 0 else None
            right = tokens[idx + 1] if idx < len(tokens) - 1 else None
            if left in survivors_set or right in survivors_set:
                keep.append(tok)
    ref = " ".join(keep).strip()
    if len(keep) < 2 or not any(ch.isalnum() for ch in ref):
        return None
    return ref


def _best_filesystem_reference(structured_ref, raw_ref):
    """
    Picks the reference that reaches the most specific real target.
    The structured entities are preferred when both sources resolve to
    the same place; the user's own words take over when the entities
    were dropped or only carried the drive scope ("c drive" alone lists
    the drive root, while "games folder in c drive" lists C:\\games).
    When neither resolves, the raw reference is kept so the executor's
    not_found names exactly what the user asked. Never returns a target
    that did not exist — both candidates go through the safe resolver.
    """
    def resolved(ref):
        if not ref:
            return None
        return resolve_reference(ref)

    raw_res = resolved(raw_ref)
    struct_res = resolved(structured_ref)

    if raw_res is not None and raw_res.found:
        if struct_res is None or not struct_res.found:
            return raw_ref
        # Both resolve — keep the more specific (deeper) target.
        if len(raw_res.path or "") > len(struct_res.path or ""):
            return raw_ref
        return structured_ref

    if struct_res is not None and struct_res.found:
        return structured_ref

    return raw_ref or structured_ref


def _filesystem_locate_signal(raw_text, tool_cap, goal, labels, folder_text):
    """
    True when the user's own words are a filesystem-locate request
    that drifted into the device/web path ("tell me the location of
    spiderman 2 in my pc" fired the launcher and a web search). The
    phrase must be an explicit locate ask combined with either a
    machine-filesystem scope ("in my pc", "in my device") or a
    file/folder-labeled entity — world-knowledge questions ("where is
    paris") never match. An "application"-labeled entity also counts:
    the user asked WHERE something is, so the thing being located
    (often a game the model mislabels as an app) is never a launch.

    The STRONG phrasing ("find the location of X", "locate X",
    "search my files") is decisive on its own — no world-knowledge
    question ever uses it, so the turn is pinned to the filesystem
    even when the Understanding model called it a web search with no
    local labels at all (the "find the location of my spiderman game"
    -> web drift). Weak phrasing ("where is X") still needs a label.
    """
    if not raw_text or not _LOCATE_PHRASE.search(raw_text):
        return False

    if _LOCATE_STRONG_RE.search(raw_text):
        return True

    # "in my pc" / "on my device" scope is an unambiguous local
    # signal — a world-knowledge question never says it. It must win
    # even when the model dropped every filesystem label and the
    # capability drifted to web, or a legit local locate turn goes to
    # a web search.
    if _MACHINE_SCOPE.search(raw_text):
        return True

    # A filesystem-object noun in the user's own words is equally
    # decisive ("folder", "file", "directory", "desktop", "downloads",
    # "documents", "drive"). The small model can drop every entity
    # label on a long repeat (the assassins-creed bug: "help me the
    # location of ... folder" with no labels and a "general" capability
    # fired a web search); raw text is the only signal it cannot
    # hallucinate. A world question never names a filesystem object.
    if _FS_NOUN_RE.search(raw_text):
        return True

    if tool_cap == "web" and not (labels & _FS_ENTITY_LABELS):
        return False

    if labels & _FS_ENTITY_LABELS or folder_text:
        return True

    if "application" in labels:
        return True

    return False


# Capabilities that are strictly local device/automation actions.
# When one of these is resolved, a web search is NEVER fired even
# if Reasoning set the web flag — the small model occasionally
# turns an app-launch or file request into "need web" (the chrome
# bug). A local action wins.
_LOCAL_TOOL_CAPS = {"device", "system", "automation"}


def _resolve_tool_capability(semantic):
    """
    The tool-relevant capability of a turn, resolved from BOTH
    structured signals:

      1. semantic.capability — normalized through the variant table
      2. semantic.category  — fallback when the capability label is
         off-enum (KI-007) or too vague to route

    Returns a canonical capability in _CAPABILITY_TO_TOOL when one
    resolves, otherwise the best-effort label. Never parses text.
    """
    capability = _canonical_capability(
        getattr(semantic, "capability", None)
    )

    if capability in _CAPABILITY_TO_TOOL:
        return capability

    category = _canonical_capability(
        getattr(semantic, "category", None)
    )

    if category in _CAPABILITY_TO_TOOL:
        return category

    return capability or category


class ToolRouter:

    def route(self, understanding, reasoning) -> list:
        """
        Select tools for the current turn.
        Returns a list of ToolRequest objects (possibly empty).

        Selection is driven by the resolved tool capability AND the
        Reasoning flags. The capability alone can activate a tool —
        the Understanding model is nondeterministic about the
        required_systems.tools/web booleans, so routing must not
        depend on those flags alone (the file-queries-never-fire bug).
        """
        ensure_loaded()

        if understanding is None:
            return []

        requests = []

        semantic = getattr(understanding, "semantic", None)

        if semantic is None:
            return []

        tool_cap = _resolve_tool_capability(semantic)
        goal     = _norm(semantic.goal)
        intent   = _norm(semantic.intent)
        entities = _entity_texts(understanding)
        entity_items = _entity_items(understanding)
        raw_text = getattr(understanding, "raw_text", None)

        # Deterministic launch gate — structured fields AND, when the
        # Understanding model lost every structured field on a long
        # repeat (KI-009), the user's own "open/launch X" words. A
        # launch signal pins the turn to the device path and forces
        # web off, so a repeat launch can never drift into a web
        # search or die silently.
        launch_signal = has_launch_signal(understanding)

        # A "device" turn whose entity is a folder/path is a file-system
        # operation misclassified as an app launch (the model conflates
        # "folder" with the File Explorer app). Redirect to file_manager.
        # A place-like goal keeps the rescue off weather/web turns.
        labels = {label for _, label in entity_items}
        folder_text = any(_FOLDER_TEXT_HINT.search(text) for text, _ in entity_items)
        if (
            tool_cap == "device"
            and goal not in _NON_FILE_GOALS
            and ((labels & _FILE_LABELS) or folder_text)
        ):
            tool_cap = "automation"

        # A raw-text filesystem query is decisive even when the small
        # Understanding model classified the turn as an app launch, a
        # memory turn, or hardware ("what is inside my friday probe a
        # folder" -> device/open_application/application; "list what is
        # inside friday probe e on my desktop" -> memory/hardware). The
        # user's own words ("what is inside X folder", "list X folder",
        # "read X file") are an unambiguous file-system ask, so the turn
        # is pinned to file_manager before the open_application pin can
        # override it. Explicit web-search goals are never hijacked.
        fs_query_text = bool(raw_text) and bool(
            _FS_QUERY_TEXT_RE.search(str(raw_text))
        )
        if fs_query_text and goal not in _NON_FILE_GOALS and tool_cap != "web":
            tool_cap = "automation"

        # A filesystem-locate request that drifted into the device/web
        # path (the spiderman bug: "tell me the location of X in my pc"
        # launched the game). The user's own words say LOCATE, so the
        # turn is pinned to automation BEFORE the launch pins run — a
        # locate is never a launch and never a web search.
        locate_rescue = _filesystem_locate_signal(
            raw_text, tool_cap, goal, labels, folder_text
        )
        if locate_rescue:
            tool_cap = "automation"

        # A goal of "open_application" is, by definition, an app launch.
        # The capability label is unreliable (the small model sometimes
        # calls "launch spotify" a web search or leaves it general), so
        # the explicit open_application goal pins the turn to the device
        # capability. File-system turns already rescued to "automation"
        # are never overwritten.
        if goal == _OPEN_APPLICATION_GOAL and tool_cap != "automation":
            tool_cap = "device"

        # A reference the Understanding model labeled "application"
        # names a real app. The small model occasionally classifies
        # "launch brave browser" as a web search (capability=web,
        # goal=create/search) while STILL tagging the entity
        # "application" — that label is the deterministic launch
        # signal. Only an explicit web-search goal overrides it.
        if (
            tool_cap == "web"
            and goal not in _EXPLICIT_WEB_GOALS
            and any(label == "application" for _, label in entity_items)
        ):
            tool_cap = "device"

        # A launch signal is an app launch no matter what the noisy
        # capability label says — including when the goal AND the
        # capability BOTH drift ("open spotify" -> capability=general,
        # goal=create) on a turn that still carries an application
        # entity. This keeps a launch request evaluated on its own
        # every turn: a repeat "open spotify" still launches even
        # though prior conversation already mentioned Spotify.
        # Capabilities already resolved to a concrete non-device tool
        # (system->terminal, automation->file_manager) are never
        # overwritten; explicit web-search goals never become launches.
        if (
            launch_signal
            and tool_cap not in {"device", "system", "automation"}
        ):
            tool_cap = "device"

        use_web  = bool(getattr(reasoning, "use_web", False))
        use_tool = bool(getattr(reasoning, "use_tools", False))

        is_web_cap = tool_cap == "web"
        is_local   = tool_cap in _LOCAL_TOOL_CAPS

        # A turn whose goal is explicitly "search the web" is a web
        # search no matter what the (noisy) capability label says.
        goal_search_web = goal == "search_web"

        # A launch signal is decisive: the user's own words are a
        # launch command ("open X"), so the turn never fires a web
        # search even when the drifted structured goal says otherwise
        # ("open steam" -> goal=search_web on a long repeat). The
        # raw-text gate (_raw_text_launch_ref) requires a literal
        # "open/launch X" prefix, which a genuine web request never
        # has, so this can never cannibalize a real search. The same
        # holds for a filesystem-locate request — a locate is never a
        # web search.
        if launch_signal or locate_rescue:
            use_web = False
            goal_search_web = False

        # A local device/automation/system action must never also
        # fire a web search (the app-launch bug) — unless the goal
        # itself is an explicit web search.
        local_blocked = is_local and not goal_search_web

        # ------------------------------------------
        # WEB — fires when Reasoning asked for the web
        # OR the capability itself is web OR the goal is
        # an explicit web search (a strong deterministic
        # signal that must never be dropped).
        # ------------------------------------------

        if (use_web or is_web_cap or goal_search_web) and not local_blocked:
            request = self._build_web_request(goal, tool_cap, entities, raw_text)
            if request is not None:
                requests.append(request)

        # ------------------------------------------
        # TOOLS — fires when Reasoning decided tools
        # are needed OR the resolved capability maps
        # to a concrete tool (capability alone is a
        # sufficient signal — the flags are unreliable).
        # ------------------------------------------

        if (
            (use_tool or tool_cap in _CAPABILITY_TO_TOOL)
            and not is_web_cap
            and not goal_search_web
            and tool_cap in _CAPABILITY_TO_TOOL
        ):
            request = self._build_tool_request(
                _CAPABILITY_TO_TOOL[tool_cap],
                tool_cap,
                goal,
                intent,
                entity_items,
                raw_text=getattr(understanding, "raw_text", None),
            )
            if request is not None:
                requests.append(request)

        return requests

    # ==========================================
    # REQUEST BUILDERS
    # ==========================================

    def _build_web_request(self, goal, capability, entities, raw_text=None):
        """
        Web search query is built from the user's raw query to preserve
        their information need. Falls back to entities/goal when raw
        text is unavailable.
        """
        tool = skill_registry.get_tool("web_search")

        if tool is None:
            return None

        # Use raw user query to preserve intent (e.g., "weather", "current", "price")
        # Clean filler words but preserve the semantic request
        query = ""
        if raw_text:
            query = self._clean_query_for_search(raw_text)
        
        if not query:
            query = " ".join(entities).strip()

        if not query:
            query = goal or capability

        if not query:
            return None

        return ToolRequest(
            tool_name="web_search",
            action="search",
            parameters={"query": query},
            reason=f"capability={capability}, goal={goal or 'unknown'}",
            permission=tool.metadata.permission,
        )

    def _clean_query_for_search(self, raw_text: str) -> str:
        """
        Clean filler words from raw query while preserving the user's
        information need (entity + requested info + time/freshness).
        """
        if not raw_text:
            return ""
        
        # Filler words that don't add search value
        filler_words = {
            "google", "search", "find", "look up", "look for", "tell me", "what is",
            "what are", "what's", "whats", "who is", "who's", "how to", "how do",
            "can you", "could you", "please", "kindly", "the", "a", "an", "for",
            "about", "on", "in", "at", "to", "of", "with", "from", "by", "my",
            "your", "our", "their", "his", "her", "its", "me", "i", "we", "you",
            "tell", "show", "give", "get", "know", "find out",
        }
        
        words = raw_text.lower().split()
        filtered = [w for w in words if w not in filler_words]
        
        # If too much was stripped, fall back to original
        if len(filtered) < 2 and len(words) >= 2:
            return raw_text.strip()
        
        return " ".join(filtered).strip() if filtered else raw_text.strip()

    def _build_tool_request(self, tool_name, capability, goal,
                            intent, entity_items, raw_text=None):
        """
        Builds a structured request for a non-web tool. If no
        usable parameter can be derived deterministically, returns
        None so the router never fires a tool with garbage input.

        entity_items is a list of (text, label) pairs; labels rescue
        structured misclassifications (a command mislabeled as a
        device app, a query mislabeled as an app launch).
        """
        tool = skill_registry.get_tool(tool_name)

        if tool is None:
            return None

        # ---- app launcher ----
        if tool_name == "app_launcher":
            # PRE-LAUNCH GATE (see _raw_text_is_launch): the user's own
            # words must be an explicit launch command. The small model
            # occasionally FABRICATES launch structs on a pure chat turn
            # (goal=open_application + an invented "application" entity
            # like "chrome browser"); raw text is the only signal it
            # cannot hallucinate, so without a launch verb there is no
            # launch — ever.
            if not _raw_text_is_launch(raw_text):
                return None

            if not entity_items:
                # The small model occasionally drops the entity for a
                # launch ("open file explorer") — and on a long repeat
                # it can drop every structured field at once (KI-009).
                # When the user's own words are an unambiguous
                # "open/launch X" command, the reference is recovered
                # from them; the structured goal+capability recovery
                # below covers the partial case. Either way the
                # reference still runs through the safe resolver
                # (found / ambiguous / not_found). Folder/path text is
                # never treated as an app.
                reference = None
                if raw_text:
                    reference = _raw_text_launch_ref(raw_text)
                    if not reference and (
                        goal == _OPEN_APPLICATION_GOAL
                        and capability == "device"
                    ):
                        reference = _fallback_app_reference(raw_text)
                    if reference and _FOLDER_TEXT_HINT.search(reference):
                        reference = None
                if not reference:
                    return None
                entity_items = [(reference, "application")]

            labels = {label for _, label in entity_items}

            # A command entity means the "device" label is a
            # misclassification of a terminal intent.
            if labels & _COMMAND_LABELS:
                terminal = skill_registry.get_tool("terminal")
                if terminal is not None:
                    return ToolRequest(
                        tool_name="terminal",
                        action="run",
                        parameters={
                            "command": " ".join(
                                text for text, _ in entity_items
                            )
                        },
                        reason=f"capability={capability}, goal={goal or 'unknown'}",
                        permission=terminal.metadata.permission,
                    )
                return None

            # A query/system/location label means this is NOT an app
            # launch — never fire app_launcher on it.
            if labels & _NON_APP_LABELS:
                return None

            return ToolRequest(
                tool_name="app_launcher",
                action="launch",
                parameters={"app": entity_items[0][0]},
                reason=f"capability={capability}, goal={goal or 'unknown'}",
                permission=tool.metadata.permission,
            )

        # ---- terminal ----
        if tool_name == "terminal":
            if not entity_items:
                return None
            return ToolRequest(
                tool_name="terminal",
                action="run",
                parameters={
                    "command": " ".join(
                        text for text, _ in entity_items
                    )
                },
                reason=f"capability={capability}, goal={goal or 'unknown'}",
                permission=tool.metadata.permission,
            )

        # ---- file manager ----
        if tool_name == "file_manager":
            # The path parameter is built from structured entities
            # (folder/file/path/location labels; an "application" label
            # only when the text is really a folder token or the action
            # is a locate). The action is locate/read/list chosen
            # deterministically from the intent, goal, and the user's
            # own words. When the entities were dropped or fragmented
            # (the games bug: "whats inside my games folder in my c
            # drive" arrives with no entity, or with only "c drive"),
            # the reference is recovered from the user's own words and
            # both candidates run through the safe resolver — so the
            # request always points at the most specific real target,
            # never at a bare drive root and never at the workspace.
            # When nothing at all resolves, the request still fires
            # with an empty path so the executor returns a structured
            # empty_path failure — the response model can never
            # hallucinate contents.
            action = _filesystem_action(
                intent, goal, raw_text, entity_items
            )
            structured = _filesystem_reference(entity_items, action=action)
            raw_ref = _raw_filesystem_reference(raw_text, action)
            reference = _best_filesystem_reference(structured, raw_ref)
            return ToolRequest(
                tool_name="file_manager",
                action=action,
                parameters={"path": reference} if reference else {},
                reason=f"capability={capability}, goal={goal}",
                permission=tool.metadata.permission,
            )

        # ---- calculator ----
        if tool_name == "calculate":
            if not entity_items:
                return None
            return ToolRequest(
                tool_name="calculate",
                action="evaluate",
                parameters={
                    "expression": " ".join(
                        text for text, _ in entity_items
                    )
                },
                reason=f"capability={capability}, goal={goal or 'unknown'}",
                permission=tool.metadata.permission,
            )

        return None


tool_router = ToolRouter()


def route_tool(understanding, reasoning):
    """
    Phase 5 entry point. Replaces the old route_tool(user_message).
    Returns a list of ToolRequest objects.
    """
    return tool_router.route(understanding, reasoning)


def resolved_tool_capability(understanding):
    """
    Public, read-only view of the canonical tool-relevant capability
    a turn resolves to. Never decides execution — it exists so other
    layers (e.g. the ExecutionManager) can tell whether a tool
    capability was genuinely present.
    """
    if understanding is None:
        return ""
    semantic = getattr(understanding, "semantic", None)
    if semantic is None:
        return ""
    return _resolve_tool_capability(semantic)


def capability_has_tool(capability):
    """True when a canonical capability maps to a registered tool."""
    return capability in _CAPABILITY_TO_TOOL


def has_launch_signal(understanding):
    """
    True when the turn is an application launch — INDEPENDENT of the
    unreliable required_systems.tools flag (and of the goal/capability
    labels, which the small model also drifts on repeat turns).

    Reads structured fields, PLUS the user's own words as a last
    resort (KI-009): when the Understanding model lost every structured
    signal on a long repeat ("open notepad" with goal/capability/
    intent/entities all dropped), a literal "open/launch X" prefix
    keeps the tool path alive. The raw-text gate is narrow — the text
    must begin with "open"/"launch" and the recovered reference still
    runs through the safe resolver (found / ambiguous / not_found), so
    a bad extraction degrades to an honest miss. Structured signals:
      - goal == "open_application", OR
      - intent is a command/request carrying an entity labeled
        "application".
    Explicit web-search goals never count as launches (a genuine
    "search the web" turn with an "application"-labeled entity stays a
    web search); a raw launch command wins because no web request
    begins with "open/launch <noun>".

    This is the anchor that lets the ExecutionManager treat every
    launch request independently: even when the Understanding model
    drops the tools flag after seeing prior conversation, the tool
    path stays live, so TOOL RESULTS can never silently come back
    empty and the response model can never fabricate a success.
    """
    if understanding is None:
        return False

    semantic = getattr(understanding, "semantic", None)

    if semantic is None:
        return False

    raw_text = getattr(understanding, "raw_text", None)

    # Raw-text gate first: the strongest signal is the user's own
    # words. It wins over a drifted web goal because no web request
    # literally begins "open/launch <noun>".
    if _raw_text_launch_ref(raw_text):
        return True

    goal = _norm(semantic.goal)

    if goal in _EXPLICIT_WEB_GOALS:
        return False

    # A structured open_application goal counts as a launch ONLY when
    # the user's own words are also an explicit launch command. The
    # small model occasionally fabricates launch structs on a pure chat
    # turn (the chrome-launch bug: goal=open_application + an invented
    # "chrome browser" entity invented out of "lets have some brief
    # conversation"); raw text is the only signal that cannot be
    # hallucinated, so a verbless turn is never treated as a launch.
    if goal == _OPEN_APPLICATION_GOAL:
        return _raw_text_is_launch(raw_text)

    intent = _norm(semantic.intent)

    if intent in {"command", "request"}:
        for _, label in _entity_items(understanding):
            if label == "application":
                return _raw_text_is_launch(raw_text)

    return False


def tool_required(understanding, reasoning):
    """
    True when this turn needs the tool/web execution path at all.

    Decisive when Reasoning set a flag, OR when the resolved
    capability maps to a real tool — the Understanding model is
    nondeterministic about the tools/web booleans, and a file or
    web request must still execute a tool even when the flag was
    missed (the file-queries-never-fire bug). A launch turn also
    enters the path deterministically (has_launch_signal) so a
    repeat launch never slips through when the flag AND the
    capability label both drift. Pure memory / chat / knowledge
    turns never resolve a tool capability or launch signal, so
    this stays False for them.
    """
    if bool(getattr(reasoning, "use_tools", False)) or \
            bool(getattr(reasoning, "use_web", False)):
        return True

    if understanding is None:
        return False

    semantic = getattr(understanding, "semantic", None)

    if semantic is None:
        return False

    raw_text = getattr(understanding, "raw_text", None)

    capability = _resolve_tool_capability(semantic)

    # A raw-text filesystem query ("what is inside X folder", "list X
    # folder", "read X file") must reach the router even when the small
    # Understanding model classified the turn as memory/hardware (no
    # tool capability resolves and no launch signal fires) — the
    # router's own rescue then pins it to file_manager. Web-search
    # goals stay out so a knowledge turn is never pulled into the tool
    # path. Computed here so it can override the device short-circuit
    # below: the model classifies a folder query as "device"
    # (open_application) and the device gate would otherwise drop the
    # turn before the rescue ever runs ("what is inside my downloads
    # folder" -> capability=device, no tool fired).
    fs_query = bool(raw_text) and bool(
        _FS_QUERY_TEXT_RE.search(str(raw_text))
        and _norm(semantic.goal) not in _NON_FILE_GOALS
    )

    # A locate phrase ("where is X", "location of X", "tell me the
    # path of X") must reach the router even when the small model
    # classified the turn as a device/hardware/memory turn with no tool
    # capability — the router's own locate rescue then pins it to
    # file_manager or lets a genuine world question fall through to
    # web/knowledge. Without this, a locate ask that drifts to
    # "device" (open_application) is dropped before the rescue runs and
    # the response model fabricates a path with zero tool results (the
    # "python 3.12 installer.exe" bug). Explicit non-file goals
    # (weather/web knowledge) stay out so a world question is never
    # forced into the tool path.
    locate_ask = bool(raw_text) and bool(
        _LOCATE_PHRASE.search(str(raw_text))
        and _norm(semantic.goal) not in _NON_FILE_GOALS
    )

    # A "device" capability on a turn whose own words are not a launch
    # is a fabricated struct, not a tool request (the chrome-launch-on-
    # chat bug: the model invented goal=open_application + a chrome
    # entity out of a pure conversation turn, with no tool flag set).
    # No launch verb, no tool path — a chat turn stays chat instead of
    # launching a browser. When the model DID set the tools flag, the
    # turn enters the path and the router's own app_launcher gate
    # degrades it to an honest failure (H1), never a silent success. A
    # raw-text filesystem query or locate ask is never a chat turn, so
    # it also passes through to the router (whose fs-query rescue pins
    # it to file_manager before the device path can claim it).
    if (
        capability == "device"
        and not _raw_text_is_launch(raw_text)
        and not fs_query
        and not locate_ask
    ):
        return False

    if capability in _CAPABILITY_TO_TOOL:
        return True

    if fs_query:
        return True

    if locate_ask:
        return True

    return has_launch_signal(understanding)
