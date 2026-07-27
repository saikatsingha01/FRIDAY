def evaluate_memory(fact):

    print("DEBUG EVALUATOR INPUT:", repr(fact))


    fact = fact.lower().strip()


    score = 50



    # Strong personal identity facts
    high_value_words = [
        "my name",
        "i am",
        "i'm",
        "called",
        "my laptop",
        "my phone",
        "my pc",
        "my project"
    ]


    for word in high_value_words:

        if word in fact:

            print("DEBUG HIGH VALUE FOUND:", word)

            score += 30



    # Preferences and interests
    preference_words = [
        "favorite",
        "favourite",
        "prefer",
        "like",
        "love",
        "hate",
        "enjoy",
        "interested in"
    ]


    for word in preference_words:

        if word in fact:

            print("DEBUG PREFERENCE FOUND:", word)

            score += 25



    # Life/project information
    context_words = [
        "working on",
        "building",
        "learning",
        "studying",
        "college",
        "friend",
        "family"
    ]


    for word in context_words:

        if word in fact:

            print("DEBUG CONTEXT FOUND:", word)

            score += 20



    # Temporary information should not stay forever
    temporary_words = [
        "today",
        "right now",
        "currently",
        "just now",
        "for now"
    ]


    for word in temporary_words:

        if word in fact:

            print("DEBUG TEMPORARY FOUND:", word)

            score -= 30



    # Very short messages are usually not memories
    if len(fact.split()) <= 2:

        print("DEBUG TOO SHORT")

        score -= 40



    print("DEBUG FINAL SCORE:", score)



    return {

        "should_remember": score >= 60,

        "confidence": min(score,100)

    }