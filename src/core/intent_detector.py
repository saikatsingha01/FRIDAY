def detect_intent(command):

    command = command.lower().strip()

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

    if command.startswith("remember"):
        return "remember"

    if command.startswith("forget"):
        return "forget"

    if "how many memories" in command:
        return "memory_count"

    if (
        "what is my" in command
        or "who am i" in command
        or "whom do i" in command
        or "what do i" in command
    ):
        return "memory_recall"

    if command == "who are you":
        return "identity"

    if command == "exit":
        return "exit"

    return "unknown"