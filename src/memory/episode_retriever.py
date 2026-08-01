from src.memory.episode_manager import get_all_episodes


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

    "what",
    "who",
    "where",
    "when",
    "why",
    "how",

    "do",
    "does",
    "did",

    "remember",
    "recall",

    "conversation",
    "chat",
    "previous",
    "last",

    "please"

}


def extract_keywords(text):

    words = []

    for word in text.lower().split():

        word = word.strip(".,?!")

        if len(word) < 3:
            continue

        if word in STOP_WORDS:
            continue

        words.append(word)

    return words


def retrieve_relevant_episodes(

    message,

    max_results=3

):

    query = extract_keywords(message)

    episodes = get_all_episodes()

    scored = []

    for episode in episodes:

        score = 0

        summary = episode.get(

            "summary",

            ""

        ).lower()

        keywords = [

            k.lower()

            for k in episode.get(

                "keywords",

                []

            )

        ]

        # ==========================================
        # Keyword overlap
        # ==========================================

        overlap = 0

        for word in query:

            if word in summary:

                overlap += 1

            if word in keywords:

                overlap += 1

        score += overlap * 20

        # ==========================================
        # Previous conversation boost
        # ==========================================

        if any(

            phrase in message.lower()

            for phrase in [

                "previous chat",

                "previous conversation",

                "last conversation",

                "last chat",

                "remember yesterday",

                "remember last time",

                "what were we doing",

                "what did we discuss",

                "our conversation"

            ]

        ):

            score += 25

        # ==========================================
        # Importance bonus
        # ==========================================

        score += episode.get(

            "importance",

            0

        )

        if score >= 30:

            scored.append(

                (

                    score,

                    episode

                )

            )

    scored.sort(

        key=lambda x: x[0],

        reverse=True

    )

    return [

        episode

        for _, episode in scored[:max_results]

    ]