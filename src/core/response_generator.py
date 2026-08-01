def sentence_case(text):

    if not text:
        return ""

    text = text.strip()

    return text[0].upper() + text[1:]


# ==========================================================
# MEMORY FORMATTING
# ==========================================================

def format_memory(memory):

    text = sentence_case(
        memory["text"]
    )

    category = memory.get(
        "category",
        "general"
    )

    if category == "identity":

        return text + "."

    if category == "device":

        return text + "."

    if category == "project":

        return text + "."

    if category == "preference":

        return text + "."

    if category == "emotional":

        return text + "."

    return text + "."


# ==========================================================
# MAIN
# ==========================================================

def generate_response(data):

    # --------------------------------------
    # None
    # --------------------------------------

    if data is None:

        return None

    # --------------------------------------
    # Already a response
    # --------------------------------------

    if isinstance(data, str):

        return data

    # --------------------------------------
    # Single Memory
    # --------------------------------------

    if isinstance(data, dict):

        if "text" in data:

            return format_memory(data)

        return str(data)

    # --------------------------------------
    # Memory List
    # --------------------------------------

    if isinstance(data, list):

        if len(data) == 0:

            return "I couldn't find anything relevant."

        if len(data) == 1:

            return format_memory(data[0])

        response = []

        for memory in data:

            response.append(
                format_memory(memory)
            )

        return "\n".join(response)

    # --------------------------------------
    # Fallback
    # --------------------------------------

    return str(data)