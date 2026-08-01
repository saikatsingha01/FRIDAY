from src.memory.episode_manager import add_episode


MIN_MESSAGES = 8

STOP_WORDS = {
    "the", "a", "an",
    "and", "or", "but",
    "that", "this", "with",
    "have", "has", "had",
    "what", "when", "where",
    "which", "would", "could",
    "should", "there", "their",
    "about", "because", "from",
    "into", "your", "you're",
    "my", "our", "you",
    "was", "were", "been",
    "just", "very", "really"
}


def summarize_conversation(conversation):
    """
    Converts a finished conversation
    into one episodic memory.
    """

    if len(conversation) < MIN_MESSAGES:
        return None

    user_messages = []
    keywords = set()

    for item in conversation:

        user = item.get("user", "").strip()

        if not user:
            continue

        user_messages.append(user)

        for word in user.lower().split():

            word = word.strip(".,?!()[]{}\"'")

            if len(word) < 4:
                continue

            if word in STOP_WORDS:
                continue

            keywords.add(word)

    if not user_messages:
        return None

    preview = user_messages[:3]

    summary = "Conversation about "

    summary += ", ".join(preview)

    if len(user_messages) > 3:
        summary += "..."

    importance = 5

    important_topics = {
        "friday",
        "memory",
        "brain",
        "assistant",
        "architecture",
        "project",
        "coding",
        "python",
        "ollama",
        "voice"
    }

    if keywords & important_topics:
        importance = 8

    if len(conversation) >= 20:
        importance = 10

    return add_episode(

        summary=summary,

        keywords=sorted(keywords),

        importance=importance

    )