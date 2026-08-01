def validate_input(text):
    """
    Validates speech-to-text output before it enters
    the reasoning pipeline.
    """

    if text is None:
        return False

    text = text.strip().lower()

    if not text:
        return False

    # Valid short commands
    valid_short_inputs = {
        "hi",
        "hey",
        "yo",
        "ok",
        "okay",
        "bye",
        "hello"
    }

    if text in valid_short_inputs:
        return True

    # Ignore accidental one-character inputs
    if len(text) < 2:
        return False

    # Common speech recognition noise
    noise_words = {
        "uh",
        "um",
        "hmm",
        "huh",
        "ah",
        "eh",
        "mm"
    }

    if text in noise_words:
        return False

    # Reject inputs with no alphabetic characters
    if not any(char.isalpha() for char in text):
        return False

    return True