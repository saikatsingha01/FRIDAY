from datetime import datetime

from src.memory.episode_manager import add_episode


MIN_MESSAGES = 8


def summarize_conversation(conversation, force=False):
    """
    Converts a finished session (the working context buffer) into one
    episodic memory (Issue 6/7).

    Importance is derived from session length only — no keyword-based
    topic scoring. Keywords are a retrieval index over the session
    text, never a behavior driver.
    """

    if len(conversation) < MIN_MESSAGES and not force:
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

            keywords.add(word)

    if not user_messages:
        return None

    preview = user_messages[:3]

    summary = "Conversation about "

    summary += ", ".join(preview)

    if len(user_messages) > 3:
        summary += "..."

    if len(conversation) >= 20:
        importance = 10
    elif len(conversation) >= 12:
        importance = 8
    else:
        importance = 5

    now = datetime.now().isoformat()

    return add_episode(
        summary=summary,
        keywords=sorted(keywords),
        importance=importance,
        session_id="session-" + now[:19].replace(":", "").replace(" ", "T"),
        start_time=conversation[0].get("_ts"),
        end_time=now,
    )
