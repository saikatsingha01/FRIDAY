def analyze_memory(raw_understanding: dict):
    """
    Extracts memory-related understanding from the
    shared LLM JSON.

    Primary source of truth is the Understanding prompt.
    Rules here are backstops that catch LLM variance.

    Does NOT:
    - Retrieve memories
    - Search databases
    - Store or modify memories
    - Understand language
    """

    if raw_understanding is None:
        return {
            "requires_memory": False,
            "memory_types": [],
            "memory_scope": "none",
            "memory_operation": None,
            "memory_payload": None,
            "reason": "",
            "confidence": 0.0,
        }

    required         = raw_understanding.get("required_systems", {})
    memory_scope     = raw_understanding.get("memory_scope", "none") or "none"
    memory_operation = raw_understanding.get("memory_operation", None)
    memory_payload   = raw_understanding.get("memory_payload", None)

    goal     = (raw_understanding.get("goal",     "") or "").lower().strip()
    intent   = (raw_understanding.get("intent",   "") or "").lower().strip()
    category = (raw_understanding.get("category", "") or "").lower().strip()
    raw_text = (raw_understanding.get("raw_text", "") or "").lower().strip()

    memory_types = []

    if required.get("memory"):
        memory_types.append("semantic")
    if required.get("episodes"):
        memory_types.append("episodic")
    if required.get("context"):
        memory_types.append("context")

    # --------------------------------------------------
    # Rule 1
    # Any explicit memory operation requires semantic.
    # --------------------------------------------------

    MEMORY_OPS = {"store", "update", "query", "forget"}

    if memory_operation in MEMORY_OPS:
        if "semantic" not in memory_types:
            memory_types.append("semantic")

    # --------------------------------------------------
    # Rule 2
    # Retrieval question about personal topic.
    # Catches LLM variance in goal/intent values.
    # --------------------------------------------------

    PERSONAL_CATEGORIES = {
        "preference", "food", "meal", "diet", "cuisine",
        "game", "gaming", "games", "sport", "hobby",
        "hardware", "device", "laptop", "gpu", "phone",
        "identity", "name", "age", "birthday",
        "project", "work", "building", "developing",
        "emotional", "relationship", "friend", "family",
        "memory", "personal", "profile",
        "favorite", "favourite",
    }

    RETRIEVAL_GOALS = {
        "retrieve_information", "retrieve", "query",
        "lookup", "find", "get", "current_state",
        "status", "check", "recall", "compare",
    }

    RETRIEVAL_INTENTS = {
        "question", "query", "inquiry", "request",
    }

    is_retrieval = (
        goal in RETRIEVAL_GOALS or
        intent in RETRIEVAL_INTENTS
    )

    category_is_personal = any(
        kw in category for kw in PERSONAL_CATEGORIES
    )

    text_is_personal = any(
        kw in raw_text for kw in PERSONAL_CATEGORIES
    )

    if is_retrieval and (category_is_personal or text_is_personal):
        if "semantic" not in memory_types:
            memory_types.append("semantic")
        if memory_operation is None:
            memory_operation = "query"

    # --------------------------------------------------
    # Rule 3
    # Broad retrieval fallback.
    # If retrieval detected but nothing activated yet,
    # activate semantic anyway.
    # --------------------------------------------------

    if is_retrieval and "semantic" not in memory_types:
        memory_types.append("semantic")
        if memory_operation is None:
            memory_operation = "query"

    # --------------------------------------------------
    # Rule 4
    # History scope always requires episodes.
    # --------------------------------------------------

    if memory_scope in ("history", "episodic"):
        if "episodic" not in memory_types:
            memory_types.append("episodic")

    # --------------------------------------------------
    # Rule 5
    # Episodes always need semantic alongside them.
    # --------------------------------------------------

    if "episodic" in memory_types:
        if "semantic" not in memory_types:
            memory_types.append("semantic")

    requires_memory = len(memory_types) > 0

    return {
        "requires_memory":  requires_memory,
        "memory_types":     memory_types,
        "memory_scope":     memory_scope,
        "memory_operation": memory_operation,
        "memory_payload":   memory_payload,
        "reason":           "Requested by Understanding Layer.",
        "confidence":       raw_understanding.get("confidence", 1.0),
    }