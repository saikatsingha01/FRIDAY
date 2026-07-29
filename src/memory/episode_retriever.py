from src.memory.episode_manager import get_all_episodes


STOP_WORDS = {

    "the", "a", "an",

    "is", "are", "was", "were",

    "i", "me", "my",

    "you", "your",

    "tell", "about",

    "what", "who", "where",

    "when", "why", "how",

    "did", "do", "does",

    "remember",

    "conversation",

    "conversations",

    "chat",

    "previous",

    "context"

}


def retrieve_relevant_episodes(

    message,

    max_results=3

):

    message = message.lower().strip()

    query_words = []

    for word in message.split():

        word = word.strip(".,?!")

        if len(word) < 3:

            continue

        if word in STOP_WORDS:

            continue

        query_words.append(word)

    scored = []

    episodes = get_all_episodes()

    for episode in episodes:

        score = 0

        summary = episode["summary"].lower()

        keywords = [

            k.lower()

            for k in episode["keywords"]

        ]

        # ------------------------
        # Keyword overlap
        # ------------------------

        for word in query_words:

            if word in summary:

                score += 20

            if word in keywords:

                score += 25

        # ------------------------
        # Previous conversation boost
        # ------------------------

        if any(

            phrase in message

            for phrase in [

                "previous chat",

                "previous conversation",

                "remember yesterday",

                "remember last time",

                "what were we doing",

                "what did we discuss",

                "our conversation",

                "last conversation"

            ]

        ):

            score += 40

        # ------------------------
        # Importance bonus
        # ------------------------

        score += episode["importance"]

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

    results = [

        item[1]

        for item in scored[:max_results]

    ]

    print(

        "EPISODE RETRIEVER:",

        results

    )

    return results