from dataclasses import dataclass, field
from typing import List, Optional

from src.memory.knowledge_normalizer import normalize_fact


@dataclass
class MemoryQuery:
    """
    A structured retrieval instruction built from
    LanguageUnderstanding.

    The retriever never sees raw user text.
    It only sees what the user actually wants to find.

    Fields:
        intent          — what kind of retrieval this is
        categories      — which memory categories to prioritize
        keywords        — meaningful content words to match against
        scope           — current / history / all
        profile_query   — True when user asks about themselves broadly
        max_results     — how many memories to return
    """

    intent: Optional[str] = None
    # "specific"   — user wants one particular fact
    # "profile"    — user wants everything known about them
    # "summary"    — user wants a summary of topics discussed
    # "history"    — user wants past values of something

    query_text: Optional[str] = None
    # Normalized user question, used ONLY for semantic
    # embedding scoring in the retriever (cross-vocabulary
    # recall like "educational course" → "B.Tech").
    # Never parsed or keyword-matched here.

    categories: List[str] = field(default_factory=list)
    # e.g. ["preference", "hardware", "identity"]

    keywords: List[str] = field(default_factory=list)
    # meaningful content words extracted from entities + category

    scope: str = "current"
    # "current" | "history" | "all"

    profile_query: bool = False
    # True when user is asking broadly about themselves

    max_results: int = 5


# Words that signal the user wants everything known about them.
# These are semantic signals, not keyword matches —
# the category field from Understanding is "memory" or "identity"
# when the LLM correctly classifies profile questions.
PROFILE_GOALS = {
    "retrieve_information",
    "recall",
    "summarize",
}

PROFILE_CATEGORIES = {
    "memory", "identity", "profile", "general"
}

# Fine-grained Understanding categories mapped onto the legacy coarse
# taxonomy the retrieval layers understand. Module-level constants so
# the history branch can use them too.
CATEGORY_MAP = {
    "food":        ["preference"],
    "gaming":      ["preference"],
    "preference":  ["preference"],
    "hardware":    ["device", "hardware"],
    "identity":    ["identity"],
    "education":   ["education", "identity", "general"],
    "project":     ["project"],
    "programming": ["project", "preference"],
    "emotional":   ["emotional"],
    "science":     ["general"],
    "planning":    ["project"],
    "memory":      ["preference", "identity", "device", "project", "education"],
    "general":     ["preference", "identity", "device", "project", "education"],
    "social":      [],
}

# Category-level keyword fallbacks for retrieval when the Understanding
# LLM produced no named entities.
CATEGORY_KEYWORDS = {
    "food":        ["food", "eat", "meal", "cuisine", "favorite"],
    "gaming":      ["game", "gaming", "play", "favorite"],
    "preference":  ["like", "love", "prefer", "favorite", "favourite"],
    "hardware":    ["laptop", "gpu", "ram", "cpu", "device", "phone"],
    "identity":    ["name", "age", "birthday", "identity"],
    "education":   ["study", "studying", "course", "degree", "education",
                    "university", "college", "subject", "major", "school"],
    "project":     ["project", "building", "work", "develop"],
    "programming": ["code", "language", "framework", "editor"],
    "emotional":   ["friend", "family", "relationship", "girlfriend"],
}

PROFILE_PHRASES = {
    "about me", "know about me", "know me",
    "about myself", "tell me about", "what do you know",
    "everything about", "all about me",
    "who am i", "what am i like",
}

# Fail-open backstop for historical questions. The Understanding LLM
# is supposed to set memory_scope "history" for "what was my favorite
# food before chicken curry", but it is unreliable; a question that
# explicitly reaches into the past must be able to read changed-fact
# history. This only widens the retrieval scope — if no history entry
# matches, current retrieval is unaffected.
HISTORY_PHRASES = {
    "what was", "what were",
    "used to", "used to be",
    "previously", "earlier",
    "before", "previous",
}


def _entity_words(understanding):
    """
    Content words from the Understanding entities.
    Entities are structured data the LLM already extracted —
    a more reliable retrieval signal than parsing raw text.
    """
    words = []

    for entity in understanding.semantic.entities:
        if hasattr(entity, "text"):
            text = entity.text.lower()
        elif isinstance(entity, dict):
            text = entity.get("text", "").lower()
        else:
            continue

        for word in text.split():
            if len(word) > 2:
                words.append(word)

    return words


def _categories_from_text(raw_text):
    """
    Categories whose representative keywords appear in the raw
    question. This is the inverse of CATEGORY_KEYWORDS and uses
    the same generic vocabulary. It lets a question that names a
    concrete topic ("favorite food") be treated as a specific
    query instead of a broad profile overview, and supplies the
    retrieval categories when the Understanding LLM falls back to
    a weak category like "general".
    """
    matched = []

    if not raw_text:
        return matched

    for category, hints in CATEGORY_KEYWORDS.items():
        if any(hint in raw_text for hint in hints):
            matched.append(category)

    return matched


def build_memory_query(understanding) -> MemoryQuery:
    """
    Builds a MemoryQuery from a LanguageUnderstanding object.

    This is the only function that should be called
    from memory_router. Never pass raw user_message
    into the retriever directly.
    """

    query = MemoryQuery()

    if understanding is None:
        return query

    # ------------------------------------------------
    # Determine scope from memory_scope
    # ------------------------------------------------

    scope = (understanding.memory.memory_scope or "current").lower()

    if scope == "history":
        query.scope = "history"
    else:
        query.scope = "current"

    # ------------------------------------------------
    # Detect profile query
    # User is asking broadly about themselves.
    # Check raw_text for profile phrases since the LLM
    # sometimes misclassifies these as category=general.
    # ------------------------------------------------

    raw_text = understanding.raw_text.lower()

    category = (understanding.semantic.category or "").lower()
    goal = (understanding.semantic.goal or "").lower()

    # ------------------------------------------------
    # Detect historical query
    # "what was my favorite food before chicken curry" reaches into
    # the past. The LLM's memory_scope proposal may already be
    # "history"/"episodic"; this backstop also fires on explicit
    # past-tense wording. A historical question is never a profile
    # question, so this must run before the profile branch.
    # ------------------------------------------------

    is_history_phrase = any(
        phrase in raw_text for phrase in HISTORY_PHRASES
    )

    llm_scope = (understanding.memory.memory_scope or "current").lower()
    # Episodic scope means "recap what was discussed before" — that is
    # served by the episode retriever, not the changed-fact trail. Only
    # an explicit history scope (or a history phrasing) reads history.
    is_episodic_scope = llm_scope == "episodic"

    if (not is_episodic_scope) and (
        is_history_phrase or llm_scope == "history"
    ):
        query.intent = "history"
        query.scope = "history"
        query.categories = CATEGORY_MAP.get(category, ["preference"])
        if understanding.raw_text:
            query.query_text = normalize_fact(understanding.raw_text)
        entity_words = _entity_words(understanding)
        query.keywords = list(set(
            entity_words + CATEGORY_KEYWORDS.get(category, [])
        ))
        return query

    # ------------------------------------------------
    # Detect profile query
    # User is asking broadly about themselves.
    # Check raw_text for profile phrases since the LLM
    # sometimes misclassifies these as category=general.
    #
    # A question that names a concrete topic ("what is my
    # favorite food") is specific, not a profile overview,
    # so the presence of a matched category keyword blocks
    # the profile path. Recap/summarize/history turns are
    # never profile questions either — they read the past.
    # ------------------------------------------------

    matched = _categories_from_text(raw_text)

    is_profile_category = category in PROFILE_CATEGORIES
    is_profile_goal = goal in PROFILE_GOALS

    is_profile_phrase = any(
        phrase in raw_text for phrase in PROFILE_PHRASES
    )

    is_recall_turn = (
        llm_scope in ("history", "episodic")
        or goal in ("recall", "summarize")
        or category == "conversation"
    )

    if (
        (
            (is_profile_category and is_profile_goal and not matched)
            or is_profile_phrase
        )
        and not is_recall_turn
    ):
        query.profile_query = True
        query.intent = "profile"
        query.categories = [
            "preference", "identity", "device",
            "project", "education", "emotional", "general"
        ]
        query.max_results = 20
        return query

    # ------------------------------------------------
    # Determine categories from Understanding
    # ------------------------------------------------

    query.categories = CATEGORY_MAP.get(category, ["preference"])

    if category:
        query.categories = list(set(query.categories + [category]))

    if matched:
        if category in ("general", "memory", "social", "conversation"):
            # Weak/fallback classification: the concrete topic comes
            # from the matched category keywords, not the LLM label.
            query.categories = []
            for matched_category in matched:
                query.categories += CATEGORY_MAP.get(
                    matched_category, []
                )
                query.categories.append(matched_category)
            query.categories = list(set(query.categories))
        else:
            for matched_category in matched:
                query.categories += CATEGORY_MAP.get(
                    matched_category, []
                )
            query.categories = list(set(query.categories))

    # ------------------------------------------------
    # Semantic query text for embedding-based scoring.
    # Raw text is only embedded — never parsed —
    # so structured retrieval stays intact.
    # ------------------------------------------------

    if understanding.raw_text:
        query.query_text = normalize_fact(understanding.raw_text)

    # ------------------------------------------------
    # Extract keywords from entities
    # Entities are the most reliable signal — they are
    # structured data the LLM already extracted,
    # not raw text we're trying to parse ourselves.
    # ------------------------------------------------

    entity_words = _entity_words(understanding)

    query.keywords = entity_words

    # ------------------------------------------------
    # Add category-level keywords as fallback
    # so "what is my favorite food" retrieves
    # food preferences even with no named entity.
    # ------------------------------------------------

    extra = CATEGORY_KEYWORDS.get(category, [])

    for matched_category in matched:
        extra += CATEGORY_KEYWORDS.get(matched_category, [])

    query.keywords = list(set(query.keywords + extra))

    # ------------------------------------------------
    # Determine retrieval intent
    # ------------------------------------------------

    memory_scope = understanding.memory.memory_scope or "current"

    if memory_scope == "history":
        query.intent = "history"
        query.scope = "history"
    else:
        query.intent = "specific"

    return query