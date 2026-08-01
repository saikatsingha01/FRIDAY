RESPONSES = {

    "greeting": [

        "Hello! How can I help you today?",

        "Hi! What can I do for you?",

        "Hello! I'm ready whenever you are."

    ],

    "identity": [

        "I am FRIDAY, your personal AI assistant.",

        "I'm FRIDAY. I'm here to help you think, build, and get things done."

    ],

    "unknown": [

        "I'm not sure how to help with that yet."

    ]

}


def get_response(response_type):
    """
    Returns a predefined response.

    Falls back to the 'unknown' response if the
    requested type doesn't exist.
    """

    responses = RESPONSES.get(
        response_type,
        RESPONSES["unknown"]
    )

    return responses[0]