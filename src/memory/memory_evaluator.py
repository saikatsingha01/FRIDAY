def evaluate_memory(fact):

    fact = fact.lower()


    important_words = [
        "name",
        "called",
        "laptop",
        "computer",
        "phone",
        "project",
        "working on",
        "favorite",
        "prefer",
        "love",
        "hate",
        "important",
        "family",
        "friend"
    ]


    temporary_words = [
        "today",
        "just",
        "right now",
        "currently",
        "for now"
    ]


    score = 50


    for word in important_words:

        if word in fact:
            score += 20


    for word in temporary_words:

        if word in fact:
            score -= 30



    if score >= 70:

        return {
            "should_remember": True,
            "confidence": score
        }


    else:

        return {
            "should_remember": False,
            "confidence": score
        }