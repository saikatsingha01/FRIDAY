class MemoryValidator:
    """
    Validates whether a canonical fact is suitable for storage.

    This validator receives clean extracted facts from memory_decision,
    never raw user sentences.

    Responsibilities:
    - Reject empty strings
    - Reject questions
    - Reject instruction phrases that leaked through

    These are fail-safe structural backstops only. They never score
    meaning and never decide what a fact means — the Understanding LLM
    is the sole authority on meaning.

    Does NOT:
    - Score importance
    - Evaluate relevance
    - Understand language
    """

    QUESTION_WORDS = [
        "what",
        "who",
        "where",
        "when",
        "why",
        "how",
        "do you",
        "can you",
        "tell me"
    ]

    # Instruction phrases that should never reach storage.
    # If any of these appear at the start of a payload,
    # the LLM failed to strip the wrapper — reject it.
    INSTRUCTION_PREFIXES = [
        "remember",
        "update your memory",
        "please remember",
        "can you remember",
        "store this",
        "forget",
        "delete"
    ]

    def validate(self, text):

        text = text.lower().strip()

        result = {
            "valid": True,
            "reason": "",
            "confidence": 50
        }

        # -----------------------------
        # Empty check
        # -----------------------------

        if not text:
            result["valid"] = False
            result["reason"] = "empty"
            return result

        # -----------------------------
        # Question detection
        # -----------------------------

        for word in self.QUESTION_WORDS:
            if text.startswith(word):
                result["valid"] = False
                result["reason"] = "question"
                return result

        # -----------------------------
        # Instruction leak detection
        # Catches cases where the LLM
        # failed to strip the wrapper.
        # -----------------------------

        for prefix in self.INSTRUCTION_PREFIXES:
            if text.startswith(prefix):
                result["valid"] = False
                result["reason"] = "instruction_leak"
                return result

        # Confidence is structural validity only. No keyword-based
        # boosting — the Understanding LLM owns meaning confidence.
        result["confidence"] = 50 if result["valid"] else 0

        return result


memory_validator = MemoryValidator()