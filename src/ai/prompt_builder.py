import re
import sys

from datetime import datetime

from src.contracts.language_understanding import (
    LanguageUnderstanding,
)

from src.contracts.execution import (
    ExecutionResult,
)


def _safe_print(*args, **kwargs):
    """Print that handles Unicode encoding errors on Windows cp1252 console."""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        safe_args = []
        for arg in args:
            if isinstance(arg, str):
                safe_args.append(arg.encode("cp1252", errors="replace").decode("cp1252"))
            else:
                safe_args.append(str(arg).encode("cp1252", errors="replace").decode("cp1252"))
        print(*safe_args, **kwargs)


# =====================================================
# FORMATTERS
# =====================================================

def _format_memories_grouped(memories):

    if not memories:
        return "None"

    groups = {}

    for memory in memories:

        if isinstance(memory, dict):
            text     = memory.get("text", "")
            category = memory.get("category", "general")
        else:
            text     = str(memory)
            category = "general"

        if not text:
            continue

        if category not in groups:
            groups[category] = []

        groups[category].append(text)

    CATEGORY_LABELS = {
        "preference":  "Preferences and Likes",
        "device":      "Devices and Hardware",
        "identity":    "Identity",
        "project":     "Projects",
        "emotional":   "Relationships",
        "general":     "Other",
    }

    lines = []

    for category, texts in groups.items():
        label = CATEGORY_LABELS.get(
            category, category.capitalize()
        )
        lines.append(f"{label}:")
        for text in texts:
            lines.append(f"  - {text}")
        lines.append("")

    return "\n".join(lines).strip()


def _format_context(context):

    if not context:
        return "None"

    if isinstance(context, list):
        lines = []
        for item in context:
            if isinstance(item, dict):
                user   = item.get("user", "")
                friday = item.get("friday", "")
                if user:
                    lines.append(f"User: {user}")
                if friday:
                    lines.append(f"FRIDAY: {friday}")
                lines.append("")
            else:
                lines.append(f"- {item}")
        return "\n".join(lines).strip()

    return str(context)


def _format_history(history):

    if not history:
        return "None"

    lines = []

    for entry in history:

        old_memory = entry.get("old_memory") or {}
        new_memory = entry.get("new_memory") or {}

        old_text = old_memory.get("text", "")
        new_text = new_memory.get("text", "")
        changed = (entry.get("changed_at") or "")[:10]

        if changed:
            lines.append(
                f"- Changed on {changed}: "
                f"\"{old_text}\" -> \"{new_text}\""
            )
        else:
            lines.append(
                f"- Previously: \"{old_text}\" "
                f"-> now \"{new_text}\""
            )

    return "\n".join(lines)


def _format_episodes(episodes):

    if not episodes:
        return "None"

    lines = []

    for episode in episodes:

        if isinstance(episode, dict):
            summary   = episode.get("summary", "")
            timestamp = episode.get("timestamp", "")
            if summary:
                if timestamp:
                    lines.append(
                        f"- [{timestamp[:10]}] {summary}"
                    )
                else:
                    lines.append(f"- {summary}")
        else:
            lines.append(f"- {episode}")

    return "\n".join(lines)


def _format_tool_results(tool_results):
    """
    Formats structured ToolResults for the prompt. Renders the
    outcome and payload of each tool so the response LLM can explain
    it naturally.

    Two hard rules drive this renderer:
      - Never expose tool names / implementation internals — the
        response LLM echoes whatever it sees (the "file_manager /
        web_search" leak bug).
      - Never expose raw absolute paths, URLs, or dict dumps — the
        reply is spoken aloud and must not read out long Windows
        paths or JSON (the path-reading bug).

    Each entry keeps its ACTION label (e.g. "list", "search",
    "launch") because the response instructions judge completion by
    the action that actually ran, not the user's wording.
    """
    if not tool_results:
        return "None"

    lines = []

    for result in tool_results:

        name = getattr(result, "tool_name", "")
        action = getattr(result, "action", "")
        status = getattr(result, "status", "success")
        data   = getattr(result, "data", None)

        lines.append(f"- Action: {action or name}")

        if status == "success":
            if isinstance(data, dict) and data.get("ambiguous"):
                candidates = data.get("candidates") or []
                lines.append(
                    "  Outcome: the request matches more than one "
                    "application — ask the user which one they meant:"
                )
                for candidate in candidates:
                    lines.append(f"    - {candidate}")
            else:
                rendered = _render_tool_payload(name, data)
                if rendered:
                    lines.append(rendered)
        elif status == "permission_denied":
            lines.append(
                "  Outcome: permission needed — this was not done."
            )
        elif status == "not_found":
            requested = (getattr(result, "metadata", None) or {}).get(
                "requested"
            )
            if requested:
                lines.append(
                    f"  Outcome: not found: '{requested}'."
                )
            else:
                lines.append(
                    "  Outcome: not found."
                )
        else:
            error = getattr(result, "error", None)
            if error:
                lines.append(
                    f"  Outcome: could not be done ({error})."
                )
            else:
                lines.append(
                    "  Outcome: could not be done."
                )

        lines.append("")

    return "\n".join(lines).strip()


def _render_tool_payload(name, data):
    """
    Renders a successful tool payload into compact, natural lines.
    Scalar values only — no absolute paths, URLs, or nested dicts.
    Returns "" when there is nothing safe to say.
    """
    if not isinstance(data, dict):
        return ""

    lines = []

    if name == "web_search":
        results = data.get("results")
        if isinstance(results, list):
            if not results:
                return ""
            # Internet results are never a location on the local
            # machine — state that up front so the response model can
            # never turn a web page into a made-up local path.
            lines.append(
                "  (These are internet search results, not a location "
                "on this computer.)"
            )
            lines.append(
                "  IMPORTANT: Only state facts that appear VERBATIM in "
                "the snippets below. Do NOT infer prices, versions, "
                "release dates, or specifications that are not "
                "explicitly written in the snippets. If a snippet "
                "mentions a product but not its price, do NOT guess "
                "the price. If the current price cannot be verified "
                "from the snippets, say so honestly."
            )
            for index, result in enumerate(results[:8], 1):
                if not isinstance(result, dict):
                    continue
                title = result.get("title") or ""
                if not title:
                    continue
                entry = f"  {index}. {title}"
                snippet = result.get("snippet") or ""
                if snippet:
                    entry += f" — {snippet[:180]}"
                lines.append(entry)
            return "\n".join(lines)
        return ""

    if name == "file_manager":
        # A locate result is the answer itself — the user asked WHERE
        # something is, so the resolved location is spoken aloud. The
        # match kind (exact / normalized / fuzzy) and every real
        # candidate are surfaced so the response model distinguishes
        # them instead of inventing a "cleaner" path, and the requested
        # object is repeated so kind/name drift is visible.
        if data.get("found") and data.get("path"):
            kind = data.get("kind") or "item"
            requested = data.get("requested")
            match = data.get("match")
            head = f"  Locate result for {requested!r}:" if requested \
                else "  Locate result:"
            line = f"  Found: {data['path']} ({kind})"
            if match in ("exact", "normalized", "fuzzy"):
                line += f" — {match} match"
            candidates = data.get("candidates")
            if isinstance(candidates, list) and len(candidates) > 1:
                lines = [head, line]
                for cand in candidates:
                    if not isinstance(cand, dict) or not cand.get("path"):
                        continue
                    ckind = cand.get("kind") or "item"
                    cmatch = cand.get("match") or match or "fuzzy"
                    lines.append(
                        f"  Also found: {cand['path']} ({ckind}) — "
                        f"{cmatch} match"
                    )
                lines.append(
                    "  (Every match above is a real entry that exists "
                    "on the computer right now.)"
                )
                return "\n".join(lines)
            return head + "\n" + line

        entries = data.get("entries")
        if isinstance(entries, list):
            # Bind the listing to the folder it came from so the
            # response LLM cannot mistake it for a different folder
            # mentioned in memory or earlier turns. Only the folder's
            # display name is shown (never the full absolute path).
            listing_path = data.get("path")
            folder = ""
            if isinstance(listing_path, str) and listing_path:
                parts = [p for p in re.split(r"[\\/]+", listing_path) if p]
                folder = parts[-1] if parts else listing_path
            if not entries:
                header = "  Folder listed: " + f'"{folder}"' + "\n" if folder \
                    else ""
                return (
                    header
                    + "  Result: the folder is empty — it contains no "
                    "files or subfolders."
                )
            if folder:
                lines.append(f'  Folder listed: "{folder}"')
            lines.append(
                f"  Complete listing ({len(entries)} entries):"
            )
            for entry in entries:
                if isinstance(entry, dict) and entry.get("name"):
                    kind = entry.get("type") or "item"
                    lines.append(f"    - {entry['name']} ({kind})")
            lines.append(
                "  (The folders above are listed as folders only — "
                "this listing shows nothing inside any of them, and "
                "nothing was opened or read.)"
            )
            return "\n".join(lines)
        content = data.get("content")
        if isinstance(content, str):
            shown = content
            if len(shown) > 400:
                shown = shown[:400] + "..."
            lines.append(f"  - {shown.replace(chr(10), ' ')}")
            size = data.get("size")
            if size:
                lines.append(f"  Size: {size} characters")
            return "\n".join(lines)
        return ""

    if name == "app_launcher":
        detail = data.get("detail")
        if data.get("launched") and detail:
            return f"  Opened application: {detail}"
        return ""

    # Default: scalar key/value lines only. Lists and dicts are
    # skipped so raw structured data never reaches the reply.
    for key, value in data.items():
        if isinstance(value, (dict, list)):
            continue
        lines.append(f"  {key}: {value}")

    return "\n".join(lines)


def _format_entities(understanding):

    entities = understanding.semantic.entities

    if not entities:
        return "None"

    lines = []

    for entity in entities:
        if hasattr(entity, "text"):
            lines.append(
                f"- {entity.text} ({entity.label})"
            )
        elif isinstance(entity, dict):
            lines.append(
                f"- {entity.get('text')} "
                f"({entity.get('label')})"
            )
        else:
            lines.append(str(entity))

    return "\n".join(lines)


def _format_plan(execution):

    plan = execution.planner_result

    if not plan:
        return None

    lines = []
    lines.append(f"Goal: {plan.goal}")

    if plan.expected_result:
        lines.append(
            f"Expected outcome: {plan.expected_result}"
        )

    if plan.estimated_complexity:
        lines.append(
            f"Complexity: {plan.estimated_complexity}"
        )

    lines.append("")
    lines.append("Steps required:")

    for step in plan.steps:
        lines.append(
            f"  {step.step_id}. {step.title}"
            f" — {step.description}"
        )

    return "\n".join(lines)


# Values in past-change questions that are generic enough to never
# be the fact being asked about ("favorite food", "my game", ...).
_GENERIC_VALUE_WORDS = {
    "favorite", "favourite", "food", "game", "games", "movie",
    "movies", "book", "books", "song", "songs", "place",
    "friend", "friends", "name", "best", "my", "your", "the",
    "a", "an", "i", "is", "was", "are", "did", "do", "what",
    "before", "every", "day", "thing", "things", "stuff",
    "something", "about",
}

# Grammatical past/temporal frames — universal grammar markers, not
# topic keywords. The deterministic history flag is only injected
# when one is present, so current-state questions are never
# mis-flagged.
_PAST_FRAME_MARKERS = (
    "before", "used to", "use to", "what was", "was my",
    "previous", "previously", "back then", "earlier",
    "before that", "at first", "originally",
)


def _history_named_value(understanding):
    """
    The specific value a past-change question names ("chicken curry",
    "Sekiro", "ramen"). Entities are tried first, then the
    Understanding layer's uncertain terms. Generic words are never
    the fact being asked about.
    """
    candidates = []

    for entity in understanding.semantic.entities:
        if isinstance(entity, dict):
            text = entity.get("text", "")
        else:
            text = getattr(entity, "text", "")
        if text:
            candidates.append(text)

    for term in (understanding.metadata or {}).get("uncertain_terms") or []:
        if isinstance(term, str) and term.strip():
            candidates.append(term.strip())

    for candidate in candidates:
        tokens = set(re.findall(r"[a-z0-9']+", candidate.lower()))
        if tokens and not (tokens & _GENERIC_VALUE_WORDS):
            return candidate

    return None


def _is_past_frame(raw_text):
    lowered = (raw_text or "").lower()
    return any(marker in lowered for marker in _PAST_FRAME_MARKERS)


def _before_value(raw_text):
    """
    The literal value right after "before" — fully deterministic,
    no LLM dependency. "what was my favorite food before chicken
    curry" -> "chicken curry"; "before lasagna" -> "lasagna".
    """
    lowered = (raw_text or "").lower()
    match = re.search(r"\bbefore\s+([^.,;!?\n]+)", lowered)
    if not match:
        return None
    value = match.group(1).strip()
    if not value:
        return None
    return value


def _history_flag(history, understanding):
    """
    Deterministic guidance for past-change questions. Pins the exact
    entry being asked about (or states there is no such record), and
    for "before X" questions states the before-value outright. The
    answer never depends on the small model resolving the
    "OLD -> NEW" trail by itself.

    Returns "" when the question is not a past-frame question or no
    usable value was extracted (no injection).
    """
    if not _is_past_frame(understanding.raw_text):
        return ""

    raw_lower = (understanding.raw_text or "").lower()
    value = _before_value(raw_lower) or _history_named_value(understanding)

    if not value:
        return ""

    needle = value.lower()
    framed_before = bool(
        re.search(r"\bbefore\s+" + re.escape(needle), raw_lower)
    )

    entry = None

    if framed_before:
        # "before X" — X is the value the user asks about the change
        # TO; the entry that changed TO X holds the answer on the left.
        for item in history:
            new_text = (item.get("new_memory") or {}).get("text", "")
            if needle in new_text.lower():
                entry = item
                break
    else:
        # "I used to X" — X is the value that was replaced; the
        # (most recent) entry that changed FROM X shows that change.
        for item in reversed(history):
            old_text = (item.get("old_memory") or {}).get("text", "")
            if needle in old_text.lower():
                entry = item
                break

    if entry is None:
        # Fall back to any entry containing the value.
        for item in history:
            new_text = (item.get("new_memory") or {}).get("text", "")
            old_text = (item.get("old_memory") or {}).get("text", "")
            if needle in new_text.lower() or needle in old_text.lower():
                entry = item
                break

    if entry is None:
        return (
            "NO RECORD FOUND — memory history contains no change "
            f"involving \"{value}\"."
        )

    old_text = (entry.get("old_memory") or {}).get("text", "")
    new_text = (entry.get("new_memory") or {}).get("text", "")

    if framed_before:
        return (
            "RELEVANT CHANGE FOUND — the record shows "
            f"\"{old_text}\" changed to \"{new_text}\".\n"
            f"The value that was there before \"{value}\" is "
            f"\"{old_text}\"."
        )

    return (
        "RELEVANT CHANGE FOUND — the record shows "
        f"\"{old_text}\" changed to \"{new_text}\"."
    )


def _is_profile_question(understanding):
    """
    True when the message asks FRIDAY what it knows about the user.

    Unambiguous phrasings ("who am i", "what do you know about me")
    always mean profile. Ambiguous phrasings — "tell me about",
    "what do you know", "everything about" — only mean profile when
    their object is the user themselves ("tell me about yourself",
    "everything about me"). A third-person object ("can you tell me
    about it", "what do you know about the RTX 4050") is a
    world-knowledge question, not a profile dump.
    """

    raw = understanding.raw_text.lower()

    PROFILE_PHRASES_STRONG = {
        "know about me", "know me",
        "all about me", "about me",
        "who am i", "what am i like",
        "about myself",
    }

    PROFILE_PHRASES_AMBIGUOUS = {
        "tell me about",
        "what do you know",
        "everything about",
    }

    # Objects of "tell me about X" / "what do you know X" that
    # refer to the user themselves, so the ambiguous phrasings
    # resolve to a profile question.
    USER_REFERENTS = (
        "me", "myself", "my",
        "you", "your", "yourself",
        "us", "our",
    )

    if any(p in raw for p in PROFILE_PHRASES_STRONG):
        return True

    for phrase in PROFILE_PHRASES_AMBIGUOUS:
        idx = raw.find(phrase)
        if idx == -1:
            continue
        tail = raw[idx + len(phrase):].lstrip(" ,.!?")
        if tail.startswith("about "):
            tail = tail[len("about "):].lstrip()
        if not tail:
            return True
        if tail.startswith(USER_REFERENTS):
            return True

    return False


def _is_summary_question(understanding):

    raw = understanding.raw_text.lower()

    SUMMARY_PHRASES = {
        "what have we", "what did we", "what were we",
        "what have you", "what have i",
        "been discussing", "been talking",
        "our conversation", "this chat",
        "previous chat", "previous conversation",
        "summarize", "summary",
    }

    return any(phrase in raw for phrase in SUMMARY_PHRASES) or _structured_recall(understanding)


def _structured_recall(understanding):
    """
    Universal structured fallback: the Understanding model labels
    past-conversation requests through its own taxonomy
    (category=conversation, goal=summarize/recall), and the memory
    analyzer routes those requests to episodic scope. Routing on
    those fields handles any phrasing without a phrase list.
    """
    semantic = understanding.semantic
    return (
        (semantic.category or "").lower() == "conversation"
        or (semantic.goal or "").lower() in ("summarize", "recall")
        or (understanding.memory.memory_scope or "").lower() == "episodic"
    )


def _references_user(understanding):
    """
    True when the message refers to the user's own data
    ("my favorite food", "do you know my name", "what do I have").
    Personal queries virtually always self-reference; world-knowledge
    questions ("Do you know about the B.Tech course?") never do.
    Used only for conversation-layer routing — never for memory meaning.
    """
    raw = understanding.raw_text.lower()

    tokens = set(raw.split())

    return bool(tokens & {
        "my", "mine", "me", "myself", "i",
        "i'm", "im", "i've", "ive", "i'd", "id",
    })


# =====================================================
# PROMPT BUILDER
# =====================================================

def build_prompt(
    understanding: LanguageUnderstanding,
    execution: ExecutionResult,
):

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    print("\n========== EXECUTION DEBUG ==========\n")
    print("Memory count :", len(execution.memories))
    print("Episode count:", len(execution.episodes))
    print("Context count:", len(execution.context))
    print("History count:", len(execution.history))
    print()

    if execution.memories:
        print("MEMORIES:\n")
        for memory in execution.memories:
            print(memory)
        print()

    if execution.episodes:
        print("EPISODES:\n")
        for episode in execution.episodes:
            print(episode)
        print()

    if execution.context:
        print("CONTEXT:\n")
        for ctx in execution.context:
            print(ctx)
        print()

    if execution.history:
        print("MEMORY HISTORY:\n")
        for entry in execution.history:
            old_text = (entry.get("old_memory") or {}).get("text")
            new_text = (entry.get("new_memory") or {}).get("text")
            print(f"  {old_text} -> {new_text}")
        print()

    print("=====================================\n")

    memories_text = _format_memories_grouped(execution.memories)
    episodes_text = _format_episodes(execution.episodes)
    context_text  = _format_context(execution.context)
    entities_text = _format_entities(understanding)
    emotion       = understanding.emotion.emotion or "neutral"
    plan_text     = _format_plan(execution)
    history_text  = _format_history(execution.history)
    tools_text    = _format_tool_results(execution.tool_results)

    # Terms the Understanding layer could not confidently
    # interpret — likely speech-to-text mishearings or typos.
    # The LLM must never assume their meaning.
    uncertain_terms = (
        understanding.metadata or {}
    ).get("uncertain_terms") or []

    if not isinstance(uncertain_terms, list):
        uncertain_terms = []

    is_profile  = _is_profile_question(understanding)
    is_summary  = _is_summary_question(understanding)
    is_planning = plan_text is not None
    is_history  = bool(execution.history)
    is_tool     = bool(execution.tool_results)

    # Deterministic flag for past-change questions. Pins the exact
    # entry being asked about (or states there is no such record),
    # so the answer never depends on the model resolving the
    # "OLD -> NEW" trail by itself.
    history_flag = ""

    if is_history:
        history_flag = _history_flag(
            execution.history, understanding
        )

        if history_flag:
            history_text = history_flag + "\n\n" + history_text


    # A question about the world (science, facts, concepts) — not
    # about the user. Fires when the goal is knowledge-seeking AND
    # either memory was not required OR retrieval found nothing
    # personal OR the question does not refer to the user at all
    # ("Do you know about the B.Tech course?"). Never fires for
    # profile, summary, or planning paths.
    is_world_knowledge = (
        (
            not understanding.memory.requires_memory
            or len(execution.memories) == 0
            or not _references_user(understanding)
        )
        and (understanding.semantic.goal or "").lower()
            in {"retrieve_information", "explain", "compare"}
        and not is_profile
        and not is_summary
        and not is_planning
        and not is_history
        and (understanding.semantic.category or "").lower()
            not in {"preference", "food", "gaming", "hardware",
                    "identity", "emotional", "project"}
    )

    # =====================================================
    # INSTRUCTIONS
    # All paths include the anti-hallucination constraint.
    # The source-of-truth rule varies by path: personal
    # questions answer only from memory; world-knowledge
    # questions answer from the model's own knowledge.
    # =====================================================

    # These rules always apply — they protect the user's
    # personal facts from invention.
    BASE_HONESTY_RULES = (
        "CRITICAL — honesty rules that always apply:\n"
        "- Never invent assessments of the user's knowledge, "
        "performance, weaknesses, or skill level.\n"
        "- Never assume chapter content, page numbers, "
        "or textbook structure the user did not mention.\n"
        "- Never claim to have 'reviewed notes' or 'checked' "
        "anything — you have not.\n"
        "- Never say 'based on past performance' unless "
        "the user's past performance appears in memory above.\n"
        "- Do not say 'we have just started' if facts "
        "exist in memory.\n"
        "- Never claim you are shutting down, sleeping, "
        "recharging, or going offline unless the system is "
        "actually doing that right now.\n"
    )

    # Personal/conversational answers draw only on what the
    # user actually said or stored.
    USER_SOURCE_RULE = (
        "- Only use facts explicitly stated by the user "
        "in the current message or recent conversation above.\n"
        "- If you do not have specific information, "
        "use only what the user explicitly provided "
        "and say so honestly when you are generalizing.\n"
    )

    # World-knowledge answers draw on the model's knowledge,
    # but never invent facts about the user personally.
    WORLD_SOURCE_RULE = (
        "- For questions about the world, answer directly "
        "from your own general knowledge.\n"
        "- The memories above are about the user personally. "
        "Use them only if the question concerns the user.\n"
        "- Never invent personal facts about the user beyond "
        "what appears in memory above.\n"
    )

    if is_tool:
        _statuses = [
            getattr(r, "status", "success")
            for r in (execution.tool_results or [])
        ]
        _all_success = bool(_statuses) and all(
            s == "success" for s in _statuses
        )
        _is_ambiguous = any(
            isinstance(getattr(r, "data", None), dict)
            and getattr(r, "data", {}).get("ambiguous")
            for r in (execution.tool_results or [])
        )
        _all_launches = bool(execution.tool_results) and all(
            getattr(r, "tool_name", "") == "app_launcher"
            and getattr(r, "action", "") == "launch"
            for r in (execution.tool_results or [])
        )

    if is_tool and _is_ambiguous:
        special_instructions = (
            "The request above matched more than one installed "
            "application — NONE of them was launched.\n"
            "List the matching options naturally and ask the user "
            "which one they meant.\n"
            "Never pick an option yourself. Never claim the "
            "application was opened — it was not.\n"
            "Respond only to the current message and the TOOL "
            "RESULTS above. Ignore file listings or results from "
            "earlier turns in RECENT CONVERSATION — never carry "
            "them into this reply.\n"
            "Write as if speaking aloud. "
            "No markdown. No bullet symbols. No asterisks.\n\n"
            + BASE_HONESTY_RULES
        )

    elif is_tool and not _all_success:
        special_instructions = (
            "One or more of the actions above did NOT complete.\n"
            "There is no output to describe — none of the actions "
            "that show permission denied or failure produced any "
            "result.\n"
            "DO NOT describe files, folders, content, or any outcome "
            "that is not shown as successful above.\n"
            "For each action whose status is permission denied, say "
            "only that you need the user's permission to do it.\n"
            "For each action that failed, say only, briefly and "
            "honestly, that it could not be done.\n"
            "Reading, listing, or locating files and folders NEVER "
            "requires permission — never ask for it, and never say a "
            "special word or keyword grants access.\n"
            "A status of 'not found' means the item does not exist or "
            "could not be found. It has NOTHING to do with permission: "
            "only a result whose status literally says 'permission "
            "denied' may ever be answered with a permission request.\n"
            "When a result is 'not found', say plainly that you could "
            "not find it and ask the user to name the exact folder or "
            "file again. Never ask permission for a not found result.\n"
            "If you could not find a folder or file, say you could "
            "not find it and ask the user to name the exact folder "
            "again.\n"
            "Never name any file, folder, or content that is not "
            "shown in the TOOL RESULTS above.\n"
            "Never say the action happened. Never invent a result.\n"
            "If the TOOL RESULTS section is empty or shows only "
            "failures, you did NOT run anything — say honestly that "
            "you could not do it, and never claim success.\n"
            "If the user is re-asking something from an earlier "
            "turn, a 'not found' here means it is NOT on the disk "
            "right now — never fill the gap with a location or file "
            "names from memory or from earlier turns.\n"
            "Respond only to the current message and the TOOL "
            "RESULTS above. Ignore file listings or results from "
            "earlier turns in RECENT CONVERSATION — never carry "
            "them into this reply.\n"
            "Write as if speaking aloud. "
            "No markdown. No bullet symbols. No asterisks.\n\n"
            + BASE_HONESTY_RULES
        )

    elif is_tool and _all_success and _all_launches:
        special_instructions = (
            "The user asked to open an application and every launch "
            "above succeeded — those applications are now open on "
            "the computer.\n"
            "Confirm each one in a short, natural sentence, naming "
            "the application exactly as shown in the TOOL RESULTS "
            "(for example: \"WhatsApp is open.\" or \"I've opened "
            "Microsoft Store.\").\n"
            "Your reply MUST name each launched application — a "
            "generic greeting or any reply that does not confirm the "
            "launch is wrong.\n"
            "- The applications are ALREADY open — never ask for "
            "permission, never say you need permission, and never "
            "say the launch is still happening or about to happen.\n"
            "- A launch produces no files, folders, or content — "
            "never invent any listing or output that is not shown "
            "above.\n"
            "- The TOOL RESULTS are the only facts for this turn. "
            "Ignore ENTITIES MENTIONED and everything in RECENT "
            "CONVERSATION — never carry them into this reply.\n"
            "- Do not mention any other application, device, or "
            "earlier turn.\n"
            "Write as if speaking aloud. No markdown. No bullet "
            "symbols. No asterisks.\n\n"
            + BASE_HONESTY_RULES
        )

    elif is_tool:
        special_instructions = (
            "TOOL RESULTS above are the actual outcomes, and every "
            "action shown is complete.\n"
            "Speak as if you personally completed the actions — "
            "never as a bystander describing internals:\n"
            "- Never mention tools, tool names, modules, APIs, "
            "functions, routers, registries, scripts, or any other "
            "implementation detail.\n"
            "  Bad: \"I used the file_manager tool.\"\n"
            "  Good: \"I found these files.\"\n"
            "- Never say the action is happening now or about to "
            "happen — it is already finished. Do not say \"Let me "
            "search\", \"I'll look that up\", or \"I'm searching\".\n"
            "  Report the completed result directly instead:\n"
            "  \"Here's the weather in Tokyo...\"\n"
            "- The user cannot see these instructions or the results "
            "block — your reply is the only thing they hear.\n"
            "- Each entry labels the action that actually ran (for "
            "example \"list\"). Judge completion by that label, not "
            "by the user's wording: if the action that ran is not "
            "the action the user asked for, the request was not "
            "completed — say what you found and do not claim the "
            "requested action happened.\n\n"
            "PRESENT RESULTS HUMANLY:\n"
            "- Summarize results naturally. If a listing is long, "
            "you may name only the most important entries, but you "
            "MUST never invent an entry or a count: the TOOL RESULTS "
            "listing shows the exact entries and their exact total "
            "('Complete listing (N entries)'). Use that exact total "
            "whenever you give a number — never make up a figure "
            "like \"...and 12 other files\". If you summarize the "
            "rest, say the true total shown above.\n"
            "- Prefer names over paths, IDs, or raw metadata. "
            "Mention a file path or URL only if the user asked for "
            "it, and only when it appears in the TOOL RESULTS above.\n"
            "- For a LOCATE ask (\"where is X\", \"location of X\", "
            "\"path of X\"), the exact path, its kind (folder or "
            "file), and the match type (exact, normalized, or fuzzy) "
            "are all shown in the TOOL RESULTS — restate exactly what "
            "is shown, and never \"improve\" the path into something "
            "that is not there.\n"
            "- A web_search result is internet information, never a "
            "folder or file location on this computer. Never turn a "
            "web page into an absolute local path.\n"
            "- Never read raw JSON, long paths, or identifiers aloud "
            "unless explicitly requested. Everything you say will be "
            "spoken.\n\n"
            "HONESTY ALWAYS:\n"
            "- Only describe what the results above actually show.\n"
            "- Never invent tool output that is not shown above.\n"
            "- Never name any file or folder that is not shown in the "
            "TOOL RESULTS above. If a folder listing is empty, say the "
            "folder is empty — never name files that are not there.\n"
            "- The TOOL RESULTS listing is the COMPLETE and ONLY set "
            "of entries for that folder. Never add names from memory "
            "or from what the folder name makes you expect — if the "
            "listing shows one entry, the folder has one entry.\n"
            "- A folder shown as \"name (dir)\" contains only what a "
            "later listing shows. Never guess what is inside a folder "
            "and never attach a file name to one — never turn \"logs "
            "(dir)\" into \"logs/main.log\" or invent any nested path.\n"
            "- The user's wording is NOT a source of file names — only "
            "the TOOL RESULTS above are. If the user said a name that "
            "is not in the listing above, the listing is the truth: "
            "never turn a word the user said into a file name, and "
            "never name any file except the entries in the TOOL "
            "RESULTS above.\n"
            "- An absolute local path (\"C:\\...\") may be spoken "
            "ONLY when it appears in the TOOL RESULTS of the current "
            "locate. Never write a path from memory, from a web page, "
            "or from what the name \"should\" be.\n"
            "- If the results show the item WAS found or located, say "
            "so — never claim you could not find it or that you are "
            "unsure when the results above show it was found.\n"
            "- Never claim an action completed when the results show "
            "it did not.\n"
            "- Respond only to the current message and the TOOL "
            "RESULTS above. Ignore file listings or results from "
            "earlier turns in RECENT CONVERSATION — never carry "
            "them into this reply.\n"
            "- If the user re-asks or repeats a question from an "
            "earlier turn, the current TOOL RESULTS are still the "
            "only facts for this reply — never restate a location, "
            "path, count, or listing that came from an earlier turn "
            "or from memory unless it appears in the TOOL RESULTS "
            "above.\n"
            "- If the user asked you to create or change something but "
            "the results only show what already exists, never claim "
            "you created or changed anything — say what you found "
            "instead.\n\n"
            "Write as if speaking aloud. "
            "No markdown. No bullet symbols. No asterisks.\n\n"
            + BASE_HONESTY_RULES
            + USER_SOURCE_RULE
        )

    elif is_planning:
        special_instructions = (
            "You are helping the user with a structured task.\n"
            "The execution plan above defines the required steps.\n"
            "The recent conversation contains everything the user "
            "has told you — use it as your only source of facts.\n"
            "Produce a complete, actionable response based "
            "strictly on what the user provided.\n"
            "When you do not have specific details, say so "
            "clearly and work with what you have been given.\n"
            "Write as if speaking aloud. "
            "No markdown. No bullet symbols. No asterisks.\n\n"
            + BASE_HONESTY_RULES
            + USER_SOURCE_RULE
        )

    elif is_profile:
        special_instructions = (
            "The user is asking what you know about them.\n"
            "List everything from long-term memory clearly.\n"
            "Only mention categories that have data above.\n"
            "Do not invent empty sections.\n"
            "State what you know confidently.\n"
            "Write as if speaking aloud. "
            "No markdown. No asterisks. No bold text.\n\n"
            + BASE_HONESTY_RULES
            + USER_SOURCE_RULE
        )

    elif is_history:
        special_instructions = (
            "The user asked about a PAST or previously changed fact.\n"
            "Answer only from MEMORY HISTORY.\n"
            "Never answer a 'before/what was' question from "
            "'WHAT YOU KNOW ABOUT THE USER'.\n"
            "Write as if speaking aloud. "
            "No markdown. No asterisks. No bold text.\n\n"
            + BASE_HONESTY_RULES
            + USER_SOURCE_RULE
        )

        if history_flag:
            special_instructions += (
                "\nFINAL NOTE — the record for this question:\n"
                f"{history_flag}\n"
                "If the record states a before-value, "
                "that is the answer."
            )

    elif is_summary:
        special_instructions = (
            "The user wants a summary of what has been discussed.\n"
            "The RECENT CONVERSATION above may only show how a session "
            "ended — a greeting or farewell is not the topic of the "
            "discussion.\n"
            "The actual previous conversations are summarized in the "
            "PAST EXPERIENCES section above; those are the primary "
            "source for this answer.\n"
            "Combine past experiences, long-term memory, and any recent "
            "conversation together.\n"
            "Cover every topic — do not focus on only one.\n"
            "Write as if speaking aloud. "
            "No markdown. No asterisks. No bold text.\n\n"
            + BASE_HONESTY_RULES
        )

    elif is_world_knowledge:
        special_instructions = (
            "The user is asking a question about the world — "
            "not about themselves.\n"
            "Answer directly and naturally from your own knowledge.\n"
            "Do not look for the answer in the user's memories.\n"
            "If you genuinely do not know, say so honestly "
            "and briefly.\n"
            "Write as if speaking aloud. "
            "No markdown. No asterisks. No bold text.\n\n"
            + BASE_HONESTY_RULES
            + WORLD_SOURCE_RULE
        )

    else:
        special_instructions = (
            "Answer using only the memories and context "
            "listed above.\n"
            "If the answer is in memory or context, "
            "state it clearly.\n"
            "If it is not, say you do not have that "
            "information yet.\n"
            "Write as if speaking aloud. "
            "No markdown. No asterisks. No bold text.\n\n"
            + BASE_HONESTY_RULES
            + USER_SOURCE_RULE
        )

    plan_section = ""

    if getattr(execution, "end_session", False):
        special_instructions += (
            "\nSESSION ENDING — you are going offline right now. "
            "The system will stop listening after this reply.\n"
            "Acknowledge the user's goodbye naturally and briefly "
            "— a warm, final farewell.\n"
            "Do not refuse. Do not continue the conversation. "
            "Do not ask new questions.\n"
            "Keep it to one or two sentences.\n"
        )

    if is_planning and plan_text:
        plan_section = (
            "\n==================================================\n"
            "EXECUTION PLAN\n"
            "==================================================\n\n"
            + plan_text
            + "\n"
        )

    uncertain_section = ""

    # World-knowledge questions answer from the model's own knowledge;
    # surfacing "unconfirmed terms" here makes the model hedge a
    # question it can actually answer (Bug 7). Writes still surface
    # them so a mishearing is never baked into memory.
    if uncertain_terms and not is_world_knowledge:
        terms = ", ".join(str(t) for t in uncertain_terms)
        uncertain_section = (
            "\n==================================================\n"
            "UNCONFIRMED TERMS\n"
            "==================================================\n\n"
            "The user used term(s) that could not be confidently "
            f"interpreted: {terms}.\n"
            "Do NOT assume or invent their meaning.\n"
            "If the answer depends on one of these terms and you "
            "cannot recognize it at all, briefly ask the user what "
            "they meant. Otherwise answer with what you know, "
            "honestly noting any uncertainty.\n"
        )

    prompt = (
        "You are FRIDAY — an intelligent AI operating companion "
        "built for one person.\n\n"

        "You are not a generic assistant. You are a long-term "
        "companion who remembers, learns, and adapts.\n\n"

        "Your personality is calm, confident, curious, and direct. "
        "You never sound robotic or templated.\n"
        "You vary your sentence structure naturally. "
        "You never repeat the same phrasing twice.\n"
        "You are honest — if you do not know something, "
        "you say so clearly without apology.\n\n"

        f"Current time: {current_time}\n"
        f"User emotional state: {emotion}\n\n"

        "==================================================\n"
        "WHAT YOU KNOW ABOUT THE USER\n"
        "==================================================\n\n"
        f"{memories_text}\n\n"

        "==================================================\n"
        "PAST EXPERIENCES\n"
        "==================================================\n\n"
        f"{episodes_text}\n\n"

        "==================================================\n"
        "RECENT CONVERSATION\n"
        "==================================================\n\n"
        f"{context_text}\n\n"

        "==================================================\n"
        "MEMORY HISTORY\n"
        "==================================================\n\n"
        f"{history_text}\n\n"

        "==================================================\n"
        "ENTITIES MENTIONED\n"
        "==================================================\n"
        f"{entities_text}\n"

        "==================================================\n"
        "TOOL RESULTS\n"
        "==================================================\n\n"
        f"{tools_text}\n\n"

        f"{uncertain_section}\n"

        f"{plan_section}\n"

        "==================================================\n"
        "INSTRUCTIONS\n"
        "==================================================\n"
        f"{special_instructions}\n"

        "Style rules:\n"
        "- Match your tone to the user emotional state: "
        f"{emotion}.\n"
        "- Keep responses concise unless the user asks for detail.\n"
        "- Never expose your internal pipeline or reasoning steps.\n"
        "- Use plain natural language only. No markdown. "
        "No asterisks. No bold. No bullet symbols.\n"
        "  This response will be spoken aloud.\n\n"

        "==================================================\n"
        "USER MESSAGE\n"
        "==================================================\n\n"
        f"{understanding.raw_text}\n\n"

        "==================================================\n"
        "FRIDAY RESPONSE\n"
        "=================================================="
    )

    _safe_print("\n========== FINAL PROMPT ==========\n")
    _safe_print(prompt)
    _safe_print("\n==================================\n")

    return prompt