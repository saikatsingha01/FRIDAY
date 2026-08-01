def analyze_context(raw_understanding: dict):
    """
    Extracts context requirements from the
    shared understanding JSON.

    This module NEVER calls the LLM.

    Responsibilities:
    - Decide whether previous conversation
      context is required.
    - Determine the required context scope.

    Does NOT:
    - Retrieve context
    - Retrieve memory
    - Perform reasoning
    """

    if raw_understanding is None:

        return {

            "requires_context": False,

            "context_scope": "none",

            "reason": "",

            "confidence": 0.0,

        }

    required_systems = raw_understanding.get(

        "required_systems",

        {}

    )

    conversation_state = raw_understanding.get(

        "conversation_state",

        ""

    )

    requires_context = required_systems.get(

        "context",

        False

    )

    if conversation_state in [

        "follow_up",

        "clarification",

        "correction",

    ]:

        requires_context = True

    context_scope = (

        "recent"

        if requires_context

        else "none"

    )

    return {

        "requires_context": requires_context,

        "context_scope": context_scope,

        "reason": "Requested by Understanding Layer.",

        "confidence": raw_understanding.get(

            "confidence",

            1.0,

        ),

    }