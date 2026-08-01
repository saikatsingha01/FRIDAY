def analyze_emotion(raw_understanding: dict):
    """
    Extracts emotion-related information
    from the shared understanding JSON.

    This module NEVER calls the LLM.

    Responsibilities:
    - Emotion
    - Sentiment
    - Urgency
    """

    if raw_understanding is None:

        return {

            "emotion": None,

            "sentiment": None,

            "urgency": None,

            "confidence": 0.0,

        }

    return {

        "emotion": raw_understanding.get(
            "emotion"
        ),

        "sentiment": raw_understanding.get(
            "sentiment"
        ),

        "urgency": raw_understanding.get(
            "urgency"
        ),

        "confidence": raw_understanding.get(
            "confidence",
            1.0,
        ),

    }