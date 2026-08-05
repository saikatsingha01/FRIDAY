def sentence_case(text):

    if not text:

        return ""

    text = text.strip()

    return text[0].upper() + text[1:]


# ==========================================================
# TRIVIAL RESPONSE TEMPLATES
#
# Used by brain.py's triage fast-path: zero LLM calls on trivial
# social messages (hello/bye/thanks/etc). Each category has a few
# natural variants selected randomly so replies are not robotic.
# ==========================================================

import random

TRIVIAL_TEMPLATES = {

    "greeting": [
        "Hey! Good to see you. What can I do for you?",
        "Hello! What are we working on today?",
        "Hi there! How can I help?",
        "Hey! I'm ready when you are.",
    ],

    "farewell": [
        "Take care! See you soon.",
        "Goodbye! I'll be here whenever you need me.",
        "Bye for now. Talk soon!",
    ],

    "gratitude": [
        "You're welcome!",
        "Anytime. That's what I'm here for.",
        "Happy to help!",
        "No problem at all.",
    ],

    "affirmation": [
        "Got it.",
        "Sounds good.",
        "Alright, understood.",
        "On it.",
    ],

    "small_talk": [
        "I'm doing well, thanks for asking. What about you?",
        "All good on my end! What's on your mind?",
        "Everything's running smoothly. What do you need?",
    ],

}


def generate_trivial_response(category: str, message: str = "") -> str:
    """
    Returns a template response for a trivial triage category.
    Raises KeyError when the category has no templates — the caller
    must fall back to the full pipeline (fail-open).
    """

    templates = TRIVIAL_TEMPLATES[category]

    return random.choice(templates)


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