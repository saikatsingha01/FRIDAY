from src.ai.llm_interface import llm


STOP_WORDS = {

    "the",
    "a",
    "an",

    "is",
    "are",
    "was",
    "were",

    "i",
    "me",
    "my",
    "you",
    "your",

    "do",
    "does",
    "did",

    "what",
    "who",
    "where",
    "when",
    "why",
    "how",

    "can",
    "could",
    "would",
    "should",

    "please",

    "tell",

    "remember",

    "recall"
}


def extract_keywords(text):

    words = []

    for word in (text or "").lower().split():

        word = word.strip(".,?!")

        if len(word) < 3:
            continue

        if word in STOP_WORDS:
            continue

        words.append(word)

    return words


def similarity(words1, words2):

    if not words1 or not words2:
        return 0

    return len(set(words1) & set(words2))


def _get_embedding(text):

    try:
        provider = llm.get_provider()
        if provider is None or not hasattr(provider, "embed"):
            return None
        return provider.embed(text)
    except Exception:
        return None


def _cosine(a, b):

    if not a or not b or len(a) != len(b):
        return 0.0

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = (sum(x * x for x in a) ** 0.5) or 1.0
    norm_b = (sum(y * y for y in b) ** 0.5) or 1.0

    return dot / (norm_a * norm_b)


def _message_text(message):
    """
    Extracts the comparable text from either a LanguageUnderstanding
    object or a plain string (legacy callers).
    """
    if message is None:
        return ""

    if isinstance(message, str):
        return message

    return getattr(message, "raw_text", "") or ""


def find_relevant_context(
    message,
    context,
    max_results=3
):

    if not context:
        return []

    message_text = _message_text(message)

    query_keywords = extract_keywords(message_text)

    # Short dependent follow-ups ("yes, no, tell me, what about it,
    # go on") strip to zero keywords after stop-word removal and
    # therefore never score. They can only be understood through the
    # immediately preceding turns, so the recency fallback below
    # guarantees the working buffer is still served.
    short_followup = not query_keywords and not message_text.endswith(
        ("?", "!")
    )

    query_vec = None
    if message_text:
        query_vec = _get_embedding(message_text)

    context_vecs = {}
    if query_vec is not None:
        for item in context:
            previous = (
                item.get("user", "")
                + " "
                + item.get("friday", "")
            ).strip()
            if previous:
                vec = _get_embedding(previous)
                if vec is not None:
                    context_vecs[id(item)] = vec

    scored = []

    for item in context:

        previous = (
            item.get("user", "")
            + " "
            + item.get("friday", "")
        )

        previous_keywords = extract_keywords(previous)

        score = similarity(
            query_keywords,
            previous_keywords
        )

        # Semantic similarity — the primary universal signal.
        vec = context_vecs.get(id(item))
        if vec is not None:
            sim = _cosine(query_vec, vec)
            if sim > 0.5:
                score += int(60 * min(1.0, (sim - 0.5) / 0.2))

        # Exact phrase boost (cheap, unambiguous)
        if message_text and message_text.lower() in previous.lower():
            score += 5

        if score > 0:
            scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)

    ranked = [
        item
        for _, item in scored[:max_results]
    ]

    # Recency fallback: a keywordless follow-up scores nothing, but
    # the immediately preceding turns are still the correct context.
    # The most recent turns are also appended when relevance matched
    # fewer than max_results so a dependent message always sees the
    # tail of the buffer.
    if short_followup or len(ranked) < max_results:
        for item in reversed(context):
            if len(ranked) >= max_results:
                break
            if item not in ranked:
                ranked.append(item)

    return ranked
