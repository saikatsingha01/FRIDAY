class QueryUnderstanding:
    """
    Converts a raw user message into a structured query
    that the reasoning system can use.

    This prevents every module from having to perform its
    own keyword detection.
    """

    MEMORY_KEYWORDS = {
        "remember",
        "recall",
        "memory",
        "memories",
        "know",
        "stored"
    }

    PREVIOUS_CHAT_KEYWORDS = {
        "previous",
        "last",
        "earlier",
        "before",
        "yesterday",
        "conversation",
        "chat",
        "discuss",
        "talked"
    }

    PREFERENCE_KEYWORDS = {
        "favorite",
        "favourite",
        "prefer",
        "like",
        "love",
        "hate"
    }

    DEVICE_KEYWORDS = {
        "laptop",
        "computer",
        "pc",
        "phone",
        "gpu",
        "cpu",
        "ram",
        "rtx"
    }

    PROJECT_KEYWORDS = {
        "project",
        "building",
        "working",
        "developing",
        "creating",
        "friday"
    }

    IDENTITY_KEYWORDS = {
        "name",
        "age",
        "who am i",
        "identity"
    }

    def understand(self, message):

        text = message.lower().strip()

        result = {

            "intent": "conversation",

            "memory_type": None,

            "category": None,

            "needs_context": True,

            "needs_memory": False,

            "needs_episode": False

        }

        # -------------------------
        # Memory recall
        # -------------------------

        if any(word in text for word in self.MEMORY_KEYWORDS):

            result["intent"] = "memory_recall"

            result["needs_memory"] = True

        # -------------------------
        # Previous conversations
        # -------------------------

        if any(word in text for word in self.PREVIOUS_CHAT_KEYWORDS):

            result["needs_episode"] = True

        # -------------------------
        # Categories
        # -------------------------

        if any(word in text for word in self.PREFERENCE_KEYWORDS):

            result["category"] = "preference"

            result["needs_memory"] = True

        elif any(word in text for word in self.DEVICE_KEYWORDS):

            result["category"] = "device"

            result["needs_memory"] = True

        elif any(word in text for word in self.PROJECT_KEYWORDS):

            result["category"] = "project"

            result["needs_memory"] = True

        elif any(word in text for word in self.IDENTITY_KEYWORDS):

            result["category"] = "identity"

            result["needs_memory"] = True

        return result


query_understanding = QueryUnderstanding()