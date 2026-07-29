from src.utils.logger import debug



QUESTION_WORDS = [

    "what",
    "why",
    "how",
    "when",
    "where",
    "who",
    "can",
    "do",
    "does",
    "did"

]


TEMPORARY_WORDS = [

    "today",
    "right now",
    "currently",
    "just now",
    "yesterday",
    "tomorrow",
    "this morning",
    "tonight"

]


FACT_INDICATORS = [

    "my",
    "i am",
    "i'm",
    "i have",
    "i own",
    "my favorite",
    "i like",
    "i love",
    "i hate",
    "i prefer"

]



def evaluate_memory(fact):

    text = fact.lower().strip()


    score = 0


    debug(
        f"Evaluating memory candidate: {text}"
    )


    # -----------------------------
    # Reject questions
    # -----------------------------

    words = text.split()


    if words:

        if words[0] in QUESTION_WORDS:

            debug(
                "Rejected: question"
            )

            return {

                "should_remember": False,

                "confidence": 0

            }



    # -----------------------------
    # Stable fact indicators
    # -----------------------------


    for indicator in FACT_INDICATORS:

        if indicator in text:

            score += 30



    # -----------------------------
    # Temporary information
    # -----------------------------


    for word in TEMPORARY_WORDS:

        if word in text:

            score -= 40



    # -----------------------------
    # Length check
    # -----------------------------


    if len(words) <= 2:

        score -= 50



    # -----------------------------
    # Conversation phrases
    # -----------------------------


    conversation_noise = [

        "tell me",
        "remember",
        "what is",
        "what was",
        "can you"

    ]


    for phrase in conversation_noise:

        if phrase in text:

            score -= 20



    confidence = max(
        0,
        min(score,100)
    )


    debug(
        f"Memory score: {confidence}"
    )


    return {

        "should_remember": confidence >= 60,

        "confidence": confidence

    }