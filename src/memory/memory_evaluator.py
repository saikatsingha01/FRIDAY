def evaluate_memory(text):

    text = text.lower().strip()

    score = 0

    # =====================================================
    # Reject obvious questions
    # =====================================================

    if text.endswith("?"):
        return {
            "should_remember": False,
            "confidence": 0
        }

    question_starters = [
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
        "do",
        "does",
        "did",
        "is",
        "are",
        "will"
    ]

    first_word = text.split()[0] if text.split() else ""

    if first_word in question_starters:
        return {
            "should_remember": False,
            "confidence": 5
        }

    # =====================================================
    # Personal information
    # =====================================================

    personal_patterns = [

        "my name",

        "i am",

        "i'm",

        "i live",

        "my birthday",

        "my age",

        "my laptop",

        "my pc",

        "my computer",

        "my phone",

        "my gpu",

        "my cpu",

        "my ram"

    ]

    for pattern in personal_patterns:

        if pattern in text:
            score += 40

    # =====================================================
    # Preferences
    # =====================================================

    preference_patterns = [

        "favorite",

        "favourite",

        "i like",

        "i love",

        "i hate",

        "i enjoy",

        "i prefer"

    ]

    for pattern in preference_patterns:

        if pattern in text:
            score += 35

    # =====================================================
    # Long-term projects
    # =====================================================

    project_patterns = [

        "working on",

        "building",

        "developing",

        "creating",

        "my project"

    ]

    for pattern in project_patterns:

        if pattern in text:
            score += 35

    # =====================================================
    # Relationships
    # =====================================================

    relationship_patterns = [

        "girlfriend",

        "boyfriend",

        "friend",

        "family",

        "mother",

        "father",

        "brother",

        "sister"

    ]

    for pattern in relationship_patterns:

        if pattern in text:
            score += 30

    # =====================================================
    # Temporary information
    # =====================================================

    temporary_patterns = [

        "today",

        "yesterday",

        "tomorrow",

        "right now",

        "currently",

        "just now",

        "this morning",

        "this evening"

    ]

    for pattern in temporary_patterns:

        if pattern in text:
            score -= 35

    # =====================================================
    # Very short statements
    # =====================================================

    if len(text.split()) <= 2:
        score -= 25

    # =====================================================
    # Commands should never become memories
    # =====================================================

    command_words = [

        "remember",

        "forget",

        "show",

        "list",

        "calculate",

        "search",

        "open",

        "close",

        "delete"

    ]

    if any(text.startswith(word) for word in command_words):

        return {

            "should_remember": False,

            "confidence": 0

        }

    # =====================================================
    # Clamp confidence
    # =====================================================

    confidence = max(0, min(score, 100))

    return {

        "should_remember": confidence >= 35,

        "confidence": confidence

    }