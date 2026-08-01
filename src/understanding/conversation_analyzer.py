def analyze_conversation(raw_understanding: dict):
    """
    Extracts conversation-related information
    from the shared understanding JSON.

    This module NEVER calls the LLM.
    """

    if raw_understanding is None:

        return {

            "conversation_state": None,

            "requires_previous_context": False,

            "continues_previous_topic": False,

            "confidence": 0.0,

        }

    state = raw_understanding.get(
        "conversation_state"
    )

    return {

        "conversation_state": state,

        "requires_previous_context": (
            state in [
                "follow_up",
                "clarification",
                "correction",
            ]
        ),

        "continues_previous_topic": (
            state == "follow_up"
        ),

        "confidence": raw_understanding.get(
            "confidence",
            1.0,
        ),

    }