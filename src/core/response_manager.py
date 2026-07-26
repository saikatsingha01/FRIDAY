def get_response(response_type):

    responses = {

        "greeting":
            "Hello! How can I help?",

        "identity":
            "I am Friday, your personal assistant."
    }

    return responses.get(
        response_type,
        "I don't understand that yet."
    )