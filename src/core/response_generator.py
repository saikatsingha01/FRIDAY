def generate_response(data):

    # Already a normal response
    if isinstance(data, str):
        return data


    # Memory result list
    if isinstance(data, list):

        if not data:
            return "I couldn't find anything about that."


        facts = []


        for item in data:

            if "text" in item:
                facts.append(
                    item["text"]
                )


        if facts:

            return (
                "You told me: "
                + ", ".join(facts)
            )


    # Dictionary response handling
    if isinstance(data, dict):

        if "text" in data:

            return (
                "You told me: "
                + data["text"]
            )


    # Fallback
    return str(data)