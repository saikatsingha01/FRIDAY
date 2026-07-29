def sentence_case(text):

    if not text:
        return text

    text = text.strip()

    return text[0].upper() + text[1:]


def generate_memory_response(memory):

    text = memory["text"]
    category = memory.get("category", "general")

    if category == "preference":

        if text.startswith("my favorite"):
            return sentence_case(text).replace("my ", "Your ", 1) + "."

        if text.startswith("i like"):
            return "You told me that you like " + text[7:] + "."

        if text.startswith("i love"):
            return "You once told me that you love " + text[7:] + "."

        return "You told me: " + sentence_case(text) + "."


    elif category == "device":

        return sentence_case(text).replace("my ", "Your ", 1) + "."


    elif category == "identity":

        return "I remember that " + text + "."


    elif category == "project":

        return "You're currently working on " + text + "."


    elif category == "emotional":

        return "I remember you telling me that " + text + "."


    return "I remember: " + sentence_case(text) + "."


def generate_response(data):

    # Already a sentence
    if isinstance(data, str):
        return data


    # Memory list
    if isinstance(data, list):

        if len(data) == 0:
            return "I couldn't find anything about that."

        if len(data) == 1:
            return generate_memory_response(data[0])

        responses = []

        for memory in data:
            responses.append(generate_memory_response(memory))

        return " ".join(responses)


    # Single memory object
    if isinstance(data, dict):

        if "text" in data:
            return generate_memory_response(data)


    return str(data)