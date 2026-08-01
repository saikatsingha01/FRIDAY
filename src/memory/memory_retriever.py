from src.memory.memory_manager import get_all_memories
from src.memory.knowledge_normalizer import normalize_fact


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

    "can",
    "could",
    "would",
    "should",

    "what",
    "who",
    "where",
    "when",
    "why",
    "how",

    "tell",
    "about",

    "remember",
    "recall",

    "please",

    "our",
    "we",

    "conversation",
    "chat",
    "previous",
    "last"
}


CATEGORY_HINTS = {

    "device": [
        "laptop",
        "computer",
        "pc",
        "phone",
        "gpu",
        "cpu",
        "ram",
        "ssd",
        "monitor"
    ],

    "preference": [
        "favorite",
        "favourite",
        "like",
        "love",
        "hate",
        "prefer",
        "movie",
        "game",
        "music"
    ],

    "project": [
        "project",
        "building",
        "developing",
        "creating",
        "working"
    ],

    "identity": [
        "name",
        "age",
        "birthday",
        "who am i"
    ],

    "emotional": [
        "girlfriend",
        "friend",
        "family",
        "relationship"
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

        # =====================================
        # Exact match
        # =====================================

        if query == memory_text:
            score += 120

        # =====================================
        # Phrase match
        # =====================================

        elif query in memory_text:

            score += 70

        elif memory_text in query:

            score += 60

        # =====================================
        # Keyword overlap
        # =====================================

        overlap = 0

        for word in keywords:

            if word in memory_text:
                overlap += 1

        score += overlap * 20

        # =====================================
        # Category boost
        # =====================================

        for category, hints in CATEGORY_HINTS.items():

            if any(hint in query for hint in hints):

                if memory["category"] == category:

                    score += 25

        # =====================================
        # Importance bonus
        # =====================================

        score += memory.get("importance", 0)

        # =====================================
        # Confidence bonus
        # =====================================

        score += memory.get("confidence", 0) // 10

        if score > 25:

            scored.append((score, memory))

    scored.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [

        memory

        for _, memory in scored[:max_results]

    ]