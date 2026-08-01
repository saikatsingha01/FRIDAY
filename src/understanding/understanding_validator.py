from src.contracts.language_understanding import (
    Entity,
    TimeReference,
    RequiredSystems,
    LanguageUnderstanding,
)


def validate_understanding(data):

    """
    Converts raw LLM JSON into a validated
    LanguageUnderstanding object.
    """

    if data is None:

        return None

    # =====================================================
    # ENTITIES
    # =====================================================

    entities = []

    for entity in data.get("entities", []):

        entities.append(

            Entity(

                text=entity.get("text", ""),

                label=entity.get("label", ""),

                confidence=float(
                    entity.get("confidence", 1.0)
                )

            )

        )

    # =====================================================
    # TIME
    # =====================================================

    time_reference = None

    raw_time = data.get("time_reference")

    if isinstance(raw_time, dict):

        time_reference = TimeReference(

            type=raw_time.get("type"),

            value=raw_time.get("value")

        )

    # =====================================================
    # REQUIRED SYSTEMS
    # =====================================================

    raw_systems = data.get(
        "required_systems",
        {}
    )

    systems = RequiredSystems(

        memory=raw_systems.get(
            "memory",
            False
        ),

        episodes=raw_systems.get(
            "episodes",
            False
        ),

        context=raw_systems.get(
            "context",
            False
        ),

        tools=raw_systems.get(
            "tools",
            False
        ),

        web=raw_systems.get(
            "web",
            False
        ),

        vision=raw_systems.get(
            "vision",
            False
        ),

        planning=raw_systems.get(
            "planning",
            False
        ),

        reasoning=raw_systems.get(
            "reasoning",
            True
        )

    )

    # =====================================================
    # CONFIDENCE
    # =====================================================

    confidence = data.get(
        "confidence",
        0.0
    )

    try:

        confidence = float(confidence)

    except Exception:

        confidence = 0.0

    confidence = max(
        0.0,
        min(
            confidence,
            1.0
        )
    )

    # =====================================================
    # RETURN CONTRACT
    # =====================================================

    return LanguageUnderstanding(

        raw_text=data.get(
            "raw_text",
            ""
        ),

        goal=data.get(
            "goal"
        ),

        intent=data.get(
            "intent"
        ),

        category=data.get(
            "category"
        ),

        memory_scope=data.get(
            "memory_scope"
        ),

        conversation_state=data.get(
            "conversation_state"
        ),

        emotion=data.get(
            "emotion"
        ),

        entities=entities,

        time_reference=time_reference,

        required_systems=systems,

        constraints=data.get(
            "constraints",
            {}
        ),

        metadata=data.get(
            "metadata",
            {}
        ),

        confidence=confidence

    )