def detect_intent(command):

    command = command.lower().strip()


    # Greeting
    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    if command in greetings:
        return "greeting"


    # Exit
    if command in [
        "exit",
        "quit",
        "shutdown",
        "shut down",
        "turn off",
        "bye"
    ]:
        return "exit"


    # Identity
    identity_phrases = [
        "who are you",
        "who r you",
        "what are you",
        "tell me about yourself",
        "introduce yourself"
    ]

    if any(
        phrase in command
        for phrase in identity_phrases
    ):
        return "identity"


    # Remember
    if command.startswith("remember"):
        return "remember"


    # Forget
    if command.startswith("forget"):
        return "forget"


    # Memory count
    if (
        "how many memories" in command
        or "memory count" in command
    ):
        return "memory_count"


    # Show all memories
    if (
        "what do you remember" in command
        or "show my memories" in command
        or "list memories" in command
        or "what memories do you have" in command
    ):
        return "memory_list"


    # Memory question
    memory_phrases = [
        "what is my",
        "who am i",
        "what do i",
        "do you remember"
    ]

    if any(
        phrase in command
        for phrase in memory_phrases
    ):
        return "memory_recall"


    return "unknown"