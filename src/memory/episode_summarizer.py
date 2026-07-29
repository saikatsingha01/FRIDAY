from src.memory.episode_manager import add_episode


MIN_MESSAGES = 8


def summarize_conversation(conversation):

    """
    Converts a conversation into
    one episodic memory.
    """

    if len(conversation) < MIN_MESSAGES:
        return None

    user_messages = []

    keywords = set()

    for item in conversation:

        user = item.get("user", "").strip()

        if user:

            user_messages.append(user)

            for word in user.lower().split():

                word = word.strip(".,?!")

                if len(word) < 4:
                    continue

                keywords.add(word)

    if not user_messages:
        return None

    summary = "Conversation about "

    summary += ", ".join(user_messages[:3])

    if len(user_messages) > 3:

        summary += "..."

    important_words = sorted(
        list(keywords)
    )[:10]

    importance = 5

    if len(conversation) >= 20:

        importance = 8

    if any(word in keywords for word in [

        "friday",
        "project",
        "memory",
        "brain",
        "architecture",
        "assistant"

    ]):

        importance = 10

    return add_episode(

        summary=summary,

        keywords=important_words,

        importance=importance

    )