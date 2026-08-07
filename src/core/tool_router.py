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
    "okay", "ok", "sure", "yes", "kindly",
}

_FALLBACK_TRAILING = {"please", "now", "thanks", "thank", "me", "you"}


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
        # has, so this can never cannibalize a real search.
        if launch_signal:
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
            request = self._build_web_request(goal, tool_cap, entities)
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

    def _build_web_request(self, goal, capability, entities):
        """
        Web search query is built from structured entities only.
        Falls back to the goal label when no entity was extracted,
        so a bare "search the web for python" still works.
        """
        tool = skill_registry.get_tool("web_search")

        if tool is None:
            return None

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
            # Capability alone gates it: the default action (list)
            # is read-only and safe. Write/delete are separately
            # permission-gated in the executor. The Understanding
            # goal is unreliable (the model emits "open_application"
            # for file operations), so it is not a hard filter.
            return ToolRequest(
                tool_name="file_manager",
                action="list",
                parameters={},
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

    # Raw-text gate first: the strongest signal is the user's own
    # words. It wins over a drifted web goal because no web request
    # literally begins "open/launch <noun>".
    if _raw_text_launch_ref(getattr(understanding, "raw_text", None)):
        return True

    goal = _norm(semantic.goal)

    if goal in _EXPLICIT_WEB_GOALS:
        return False

    if goal == _OPEN_APPLICATION_GOAL:
        return True

    intent = _norm(semantic.intent)

    if intent in {"command", "request"}:
        for _, label in _entity_items(understanding):
            if label == "application":
                return True

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

    if _resolve_tool_capability(semantic) in _CAPABILITY_TO_TOOL:
        return True

    return has_launch_signal(understanding)
