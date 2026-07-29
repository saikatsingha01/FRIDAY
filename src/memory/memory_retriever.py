from src.memory.memory_manager import get_memory


STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were",
    "i", "me", "my", "you", "your",
    "do", "does", "did",
    "can", "could", "would",
    "tell", "about",
    "what", "who", "where", "when", "why", "how",
    "please",
    "remember",
    "previous",
    "context"
}


def retrieve_relevant_memories(message, max_results=5):

    message = message.lower().strip()

    memories = get_memory()["memories"]

    scored = []

    query_words = []

    for word in message.split():

        word = word.strip(".,?!")

        if len(word) < 3:
            continue

        if word in STOP_WORDS:
            continue

        query_words.append(word)

    for memory in memories:

        score = 0

        text = memory["text"].lower()

        # -------------------------
        # Exact match
        # -------------------------

        if message == text:

            score += 100

        # -------------------------
        # Phrase match
        # -------------------------

        if message in text or text in message:

            score += 50

        # -------------------------
        # Keyword overlap
        # -------------------------

        for word in query_words:

            if word in text:

                score += 20

        # -------------------------
        # Category boosts
        # -------------------------

        if any(w in message for w in [
            "game",
            "favorite",
            "prefer",
            "like",
            "hate"
        ]):

            if memory["category"] == "preference":

                score += 30

        if any(w in message for w in [
            "laptop",
            "gpu",
            "ram",
            "pc",
            "phone"
        ]):

            if memory["category"] == "device":

                score += 30

        if any(w in message for w in [
            "project",
            "building",
            "working"
        ]):

            if memory["category"] == "project":

                score += 30

        if any(w in message for w in [
            "name",
            "identity"
        ]):

            if memory["category"] == "identity":

                score += 30

        # -------------------------
        # Small importance bonus
        # -------------------------

        score += memory["importance"]

        if score >= 25:

            scored.append((score, memory))

    scored.sort(key=lambda x: x[0], reverse=True)

    results = [item[1] for item in scored[:max_results]]

    print("MEMORY RETRIEVER:", results)

    return results