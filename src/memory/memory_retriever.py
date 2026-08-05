from src.memory.memory_manager import get_all_memories
from src.memory.knowledge_normalizer import normalize_fact
from src.memory.memory_query_builder import (
    MemoryQuery,
    CATEGORY_MAP,
)
from src.ai.llm_interface import llm


STOP_WORDS = {
    "the", "a", "an",
    "is", "are", "was", "were",
    "i", "me", "my", "you", "your",
    "do", "does", "did",
    "can", "could", "would", "should",
    "what", "who", "where", "when", "why", "how",
    "tell", "about",
    "remember", "recall",
    "please",
    "our", "we",
    "conversation", "chat", "previous", "last"
}


CATEGORY_HINTS = {
    "device": [
        "laptop", "computer", "pc", "phone",
        "gpu", "cpu", "ram", "ssd", "monitor"
    ],
    "preference": [
        "favorite", "favourite", "like", "love",
        "hate", "prefer", "movie", "game", "music"
    ],
    "project": [
        "project", "building", "developing",
        "creating", "working"
    ],
    "identity": [
        "name", "age", "birthday", "who am i"
    ],
    "emotional": [
        "girlfriend", "friend", "family", "relationship"
    ]
}


def extract_keywords(text):

    words = []
    text = normalize_fact(text)

    for word in text.split():
        if len(word) < 3:
            continue
        if word in STOP_WORDS:
            continue
        words.append(word)

    return words


def _get_embedding(text):
    """
    Embedding for semantic scoring. Falls back to None
    on any failure so retrieval never breaks.
    """

    try:
        provider = llm.get_provider()
        if provider is None or not hasattr(provider, "embed"):
            return None
        return provider.embed(text)
    except Exception as error:
        print("EMBED ERROR:", error)
        return None


def _cosine(a, b):

    if not a or not b or len(a) != len(b):
        return 0.0

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = (sum(x * x for x in a) ** 0.5) or 1.0
    norm_b = (sum(y * y for y in b) ** 0.5) or 1.0

    return dot / (norm_a * norm_b)


def _category_matches(memory_category, query_categories):
    """
    Category match that understands both the coarse legacy taxonomy
    the retriever queries with ("preference", "device") and the fine
    categories actually stored on memory records ("food", "memory").
    A stored memory matches when its category equals a query category
    or maps into the same family through the shared CATEGORY_MAP.
    """
    if not memory_category or not query_categories:
        return False

    if memory_category in query_categories:
        return True

    families = CATEGORY_MAP.get(memory_category, [])

    return bool(set(families) & set(query_categories))


# =====================================================
# PRIMARY — structured query retrieval (Phase 2.7)
# =====================================================

def retrieve_with_query(query: MemoryQuery, max_results=None):
    """
    Retrieves memories using a structured MemoryQuery.
    Never receives raw user text.

    For profile queries: returns all memories across
    all relevant categories, sorted by importance.

    For specific queries: scores by keyword + category match.
    """

    memories = get_all_memories()

    if not memories:
        return []

    limit = max_results or query.max_results

    # ------------------------------------------------
    # Profile query — return all known memories
    # sorted by importance, no keyword scoring needed.
    # A profile overview covers every category the store
    # holds (food, memory, social, ...), so no category
    # whitelist is applied.
    # ------------------------------------------------

    if query.profile_query:
        relevant = list(memories)

        relevant.sort(
            key=lambda m: m.get("importance", 0),
            reverse=True
        )

        max_importance = 1
        for m in relevant:
            if m.get("importance", 0) > max_importance:
                max_importance = m["importance"]

        for m in relevant:
            m["retrieval_confidence"] = min(
                1.0,
                m.get("importance", 1) / max_importance
            )

        return relevant[:limit]

    # ------------------------------------------------
    # Specific query — score by keyword + category + semantics
    # ------------------------------------------------

    # High-value long-term facts get a small priority boost.
    HIGH_VALUE_CATEGORIES = {"identity", "education", "project", "device"}

    # Pre-compute embeddings for semantic scoring.
    # This bridges vocabulary gaps: "educational course"
    # vs a stored "B.Tech" memory that shares no words.
    query_vec = None
    if query.query_text:
        query_vec = _get_embedding(query.query_text)

    memory_vecs = {}
    if query_vec is not None:
        for memory in memories:
            vec = _get_embedding(memory["text"])
            if vec is not None:
                memory_vecs[id(memory)] = vec

    scored = []
    seen = set()

    for memory in memories:

        memory_text = normalize_fact(memory["text"])

        if memory_text in seen:
            continue
        seen.add(memory_text)

        score = 0
        matched_signal = False

        # Category match — highest signal
        # If the query knows what category it wants,
        # memories in that category score much higher.
        if query.categories and _category_matches(
            memory.get("category"),
            query.categories,
        ):
            score += 40
            matched_signal = True

        # Keyword overlap against memory text
        for keyword in query.keywords:
            if keyword in memory_text:
                score += 20
                matched_signal = True

        # Semantic similarity — cross-vocabulary recall.
        # Only contributes for genuinely similar text so
        # unrelated memories are not pulled in: 0.5 floor,
        # full weight reached at 0.7 similarity.
        vec = memory_vecs.get(id(memory))
        if vec is not None:
            sim = _cosine(query_vec, vec)
            if sim > 0.5:
                score += int(60 * min(1.0, (sim - 0.5) / 0.2))

        # High-value category boost — only ranks memories
        # that already matched category or keyword. It must
        # never create relevance by itself, or every important
        # memory would clear the threshold for any query.
        if matched_signal and memory.get("category") in HIGH_VALUE_CATEGORIES:
            score += 5

        # Importance bonus
        score += memory.get("importance", 0)

        # Confidence bonus
        score += memory.get("confidence", 0) // 10

        # Threshold — only return if there is some relevance signal
        if score > 15:
            scored.append((score, memory))

    scored.sort(key=lambda x: x[0], reverse=True)

    results = [memory for _, memory in scored[:limit]]

    if scored:
        for score, memory in scored[:limit]:
            memory["retrieval_confidence"] = min(
                1.0,
                max(0.0, (score - 15) / 85.0)
            )

    return results


# =====================================================
# HISTORY — previously changed facts
# "what was my favorite food before chicken curry" reads
# the change trail, not current memory. Each history entry
# carries old_memory/new_memory; the old value is the answer.
# =====================================================

def retrieve_history(query, max_results=None):
    """
    Retrieves changed-fact entries from memory_history.json.

    Scores by content-word overlap with the query (query keywords
    plus keywords extracted from the raw query text) and a category
    match. Fail-open: a miss returns [] and current-only retrieval
    is unaffected.
    """
    from src.memory.memory_history import get_history

    history = get_history()

    if not history:
        return []

    limit = max_results or getattr(query, "max_results", 5)

    keywords = list(getattr(query, "keywords", []) or [])
    if getattr(query, "query_text", None):
        keywords = list(set(
            keywords + extract_keywords(query.query_text)
        ))

    categories = set(getattr(query, "categories", []) or [])

    scored = []

    for entry in history:

        old_memory = entry.get("old_memory") or {}
        new_memory = entry.get("new_memory") or {}
        # Deleted facts are archived with a null new_memory (the fact
        # was removed, not replaced). The old value alone still answers
        # "what was X before".

        old_text = str(old_memory.get("text", "") or "")
        new_text = str(new_memory.get("text", "") or "")

        if not old_text and not new_text:
            continue

        old_lower = old_text.lower()
        new_lower = new_text.lower()

        # A "before X" question names the NEWER value. The answer is
        # the OLD value of the entry where that named value sits on
        # the right (NEW) side, so new-side matches are weighted
        # double. This separates "rice -> chicken curry" (target for
        # "before chicken curry") from the reverse "chicken curry ->
        # rice" when both are in the store.
        old_overlap = sum(
            1 for keyword in keywords
            if keyword and keyword in old_lower
        )
        new_overlap = sum(
            1 for keyword in keywords
            if keyword and keyword in new_lower
        )
        score = (new_overlap * 2 + old_overlap) * 10

        entry_categories = {
            (old_memory.get("category") or "").lower(),
            (new_memory.get("category") or "").lower(),
        }
        if categories and (entry_categories & categories):
            score += 15

        if score > 0:
            scored.append((score, entry))

    scored.sort(key=lambda x: x[0], reverse=True)

    # Repeated identical changes (e.g. a fact toggled back and forth,
    # or duplicate archive records) add noise, not information. Each
    # unique change is presented once so the LLM reads a clean trail.
    deduped = []
    seen_pairs = set()

    for _, entry in scored:

        old_memory = entry.get("old_memory") or {}
        new_memory = entry.get("new_memory") or {}

        old_text = str(old_memory.get("text", "") or "")
        new_text = str(new_memory.get("text", "") or "")

        pair = (old_text, new_text)

        if pair in seen_pairs:
            continue

        seen_pairs.add(pair)
        deduped.append(entry)

        if len(deduped) >= limit:
            break

    return deduped


# =====================================================
# LEGACY — raw text retrieval (kept for compatibility)
# Not called from the main pipeline after Phase 2.7.
# =====================================================

def retrieve_relevant_memories(message, max_results=5):

    query = normalize_fact(message)
    keywords = extract_keywords(query)
    memories = get_all_memories()

    scored = []
    seen = set()

    for memory in memories:

        memory_text = normalize_fact(memory["text"])

        if memory_text in seen:
            continue
        seen.add(memory_text)

        score = 0

        if query == memory_text:
            score += 120
        elif query in memory_text:
            score += 70
        elif memory_text in query:
            score += 60

        overlap = 0
        for word in keywords:
            if word in memory_text:
                overlap += 1
        score += overlap * 20

        for category, hints in CATEGORY_HINTS.items():
            if any(hint in query for hint in hints):
                if memory["category"] == category:
                    score += 25

        score += memory.get("importance", 0)
        score += memory.get("confidence", 0) // 10

        if score > 25:
            scored.append((score, memory))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [memory for _, memory in scored[:max_results]]