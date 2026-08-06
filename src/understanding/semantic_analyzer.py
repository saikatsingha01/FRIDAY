def analyze_semantics(raw_understanding: dict):
    """
    Extracts semantic information from the raw
    understanding JSON.

    This module NEVER calls the LLM.

    Responsibilities:

    - Goal
    - Intent
    - Category
    - Capability
    - Entities
    - Time Reference
    """

    if raw_understanding is None:

        return {

            "goal": None,

            "intent": None,

            "category": None,

            "capability": None,

            "entities": [],

            "time_reference": None,

            "confidence": 0.0,

        }

    return {

        "goal": raw_understanding.get(
            "goal"
        ),

        "intent": raw_understanding.get(
            "intent"
        ),

        "category": raw_understanding.get(
            "category"
        ),

        "capability": raw_understanding.get(
            "capability"
        ),

        "entities": raw_understanding.get(
            "entities",
            [],
        ),

        "time_reference": raw_understanding.get(
            "time_reference"
        ),

        "confidence": raw_understanding.get(
            "confidence",
            1.0,
        ),

    }