def validate_input(text):

    if not text:
        return False


    text = text.strip().lower()


    # Known short valid commands
    valid_short_inputs = [
        "hi",
        "hey",
        "yo",
        "ok",
        "bye"
    ]


    if text in valid_short_inputs:
        return True



    # Ignore extremely short accidental sounds
    if len(text) < 3:
        return False



    # Ignore common noise outputs
    noise_words = [
        "uh",
        "um",
        "hmm",
        "huh"
    ]


    if text in noise_words:
        return False


    return True