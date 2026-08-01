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

    for word in text.lower().split():

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

    common = len(

        set(words1) & set(words2)

    )

    return common


def find_relevant_context(

    message,

    context,

    max_results=3

):

    if not context:

        return []

    query_keywords = extract_keywords(message)

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

        # Exact phrase boost

        if message.lower() in previous.lower():

            score += 5

        if score > 0:

            scored.append(

                (

                    score,

                    item

                )

            )

    scored.sort(

        key=lambda x: x[0],

        reverse=True

    )

    return [

        item

        for _, item in scored[:max_results]

    ]