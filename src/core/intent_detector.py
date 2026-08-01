import re


def contains_any(text, phrases):
    """
    Matches whole words or whole phrases.

    Prevents bugs like:
        "hi" matching "this"
        "bye" matching "goodbyeing"
    """

    text = text.lower().strip()

    for phrase in phrases:

        phrase = phrase.lower().strip()

        # Multi-word phrase
        if " " in phrase:

            pattern = r"\b" + re.escape(phrase) + r"\b"

        # Single word
        else:

            pattern = r"\b" + re.escape(phrase) + r"\b"

        if re.search(pattern, text):

            return True

    return False


def detect_intent(command):

    command = command.lower().strip()

    # =====================================================
    # GREETING
    # =====================================================

    if contains_any(command, [

        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"

    ]):

        return "greeting"

    # =====================================================
    # EXIT
    # =====================================================

    if contains_any(command, [

        "bye",
        "goodbye",
        "exit",
        "quit",
        "shutdown",
        "shut down",
        "turn off"

    ]):

        return "exit"

    # =====================================================
    # IDENTITY
    # =====================================================

    if contains_any(command, [

        "who are you",
        "who r you",
        "what are you",
        "introduce yourself",
        "tell me about yourself"

    ]):

        return "identity"

    # =====================================================
    # REMEMBER
    # =====================================================

    if command.startswith("remember "):

        return "remember"

    # =====================================================
    # FORGET
    # =====================================================

    if command.startswith("forget "):

        return "forget"

    # =====================================================
    # MEMORY COUNT
    # =====================================================

    if contains_any(command, [

        "how many memories",
        "memory count",
        "number of memories"

    ]):

        return "memory_count"

    # =====================================================
    # MEMORY LIST
    # =====================================================

    if contains_any(command, [

        "what do you remember",
        "show my memories",
        "list memories",
        "list your memories",
        "what memories do you have"

    ]):

        return "memory_list"

    # =====================================================
    # MEMORY RECALL
    # =====================================================

    if contains_any(command, [

        "do you remember",
        "can you remember",
        "can you recall",
        "what is my",
        "what was my",
        "who am i",
        "who was i",
        "tell me my",
        "recall my"

    ]):

        return "memory_recall"

    # =====================================================
    # CATEGORY SEARCH
    # =====================================================

    if command.startswith("show my"):

        return "category_memory"

    # =====================================================
    # SKILLS
    # =====================================================

    if command.startswith("calculate"):

        return "skill"

    # =====================================================
    # DEFAULT
    # =====================================================

    return "unknown"