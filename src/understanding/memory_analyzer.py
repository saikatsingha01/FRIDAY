_RECALL_CENTROIDS = (
    "recap what we talked about in a previous conversation",
    "did we work on something together in an earlier conversation",
    "what did we discuss or plan last time we talked",
    "tell me anything that happened in my last session",
    "remind me what we planned in an earlier conversation",
    "anything you remember from our chat",
    "did we talk about something in a previous conversation",
)
_RECALL_CENTROID_THRESHOLD = 0.55
_RECALL_QUESTION_NO_USER_THRESHOLD = 0.60
_RECALL_STATEMENT_THRESHOLD = 0.70
_RECALL_REF_VECS = None

# Generic past-conversation phrasing backstop. A handful of closed
# conversational frames for "ask FRIDAY about a past conversation"
# that the small Understanding model under-labels ("anything from our
# chat about X", "remind me what we planned for Y"). This is a small
# frame set, not a topic keyword list: the frames carry no content
# about WHAT was discussed, only that the user wants the past chat
# recalled, so they generalize to any topic without keyword logic.
RECALL_PHRASES = (
    "anything from our chat",
    "anything from our conversation",
    "anything from our talk",
    "anything from our earlier",
    "remind me what",
    "remind me of what",
    "did we talk",
    "did we discuss",
    "did we plan",
    "what did we plan",
    "what did we talk",
    "what did we discuss",
    "from our earlier conversation",
    "from our previous conversation",
    "from our last chat",
)

# Generic grammatical/structural signals, not topic keywords. These
# distinguish "what did we plan for my guitar" (user + question) from
# "what did the weather report say earlier" (no user reference).
INTERROGATIVE_WORDS = {
    "what", "who", "where", "when", "why", "how",
    "which", "whose", "whom",
}

USER_PRONOUNS = {
    "my", "mine", "me", "myself",
    "i", "im", "i'm",
    "we", "our", "us", "ours",
}

# Second-person address to FRIDAY plus a knowledge-state verb is a
# question about what FRIDAY knows or remembers, never a fact to
# store. "you remember my favorite food is sushi" asks FRIDAY to
# recall; "remember my favorite food is sushi" (imperative, no
# "you") is the store form. Closed grammatical classes (pronouns,
# verbs) — the same signal class as USER_PRONOUNS and
# INTERROGATIVE_WORDS, not topic keywords. "did you know X" is
# excluded: it is the fact-drop form ("did you know I play Zelda"
# introduces new information) and is not forced to a query.
SECOND_PERSON_PRONOUNS = {"you", "your", "yours"}

KNOWLEDGE_VERBS = {"remember", "know", "recall"}

# Closed-class imperative removal verbs. A message whose FIRST token
# is one of these is a command to delete a stored fact, never a new
# fact to store. The leading-position check is structural (like the
# declination frames in Rule 12) — "I forget my keys" (statement) and
# "don't forget the milk" (reminder) both leave the verb in a
# non-leading position and are untouched. Topic-dismissal uses of the
# same verbs ("forget it", "drop this topic") are already suppressed
# by the dedicated conversation-flow classifier upstream.
REMOVAL_VERBS = {"forget", "delete", "remove", "erase"}

# Leading clauses that a delete target should never contain. When the
# Understanding LLM emits a forget target it built by echoing the
# command ("I forget that I like coffee"), the echoed clause is
# stripped so the target is the fact itself ("I like coffee").
REMOVAL_LEAD_CLAUSES = (
    "i forget that", "i forgot that", "i forget", "i forgot",
    "forget that", "forget about", "forget",
)


def _recall_similarity(text):
    """
    Semantic similarity between a message and the general
    concept of recapping a previous conversation or session.
    The message is compared against several generic centroids
    and the highest similarity is used; this generalizes to
    any phrasing. The centroid embeddings are computed once
    and reused. Fail-open: returns None if no provider is
    available or the call errors.
    """
    global _RECALL_REF_VECS

    if not text:
        return None

    try:
        from src.memory.episode_retriever import (
            _get_embedding,
            _cosine,
        )

        if _RECALL_REF_VECS is None:
            _RECALL_REF_VECS = [
                _get_embedding(c) for c in _RECALL_CENTROIDS
            ]
        if not _RECALL_REF_VECS or any(
            v is None for v in _RECALL_REF_VECS
        ):
            return None

        msg_vec = _get_embedding(text)
        if msg_vec is None:
            return None

        return max(
            _cosine(msg_vec, vec)
            for vec in _RECALL_REF_VECS
        )
    except Exception:
        return None


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
            "canonical_fact": None,
            "uncertain_terms": [],
            "reason": "",
            "confidence": 0.0,
        }

    required         = raw_understanding.get("required_systems", {})
    memory_scope     = raw_understanding.get("memory_scope", "none") or "none"
    memory_operation = raw_understanding.get("memory_operation", None)
    if not isinstance(memory_operation, str):
        memory_operation = None
    else:
        memory_operation = memory_operation.lower().strip() or None
    canonical_fact   = raw_understanding.get("canonical_fact", None)
    uncertain_terms  = raw_understanding.get("uncertain_terms", []) or []

    # The Understanding LLM speaks plain English for the delete intent
    # ("delete"), while the contract names the same operation "forget".
    # This is an enum alias on a structured field — the same treatment
    # PERSISTENCE_ALIASES gives "temporary" -> "transient". It is not a
    # message-parsing rule and carries no keyword logic.
    if memory_operation in ("delete", "remove"):
        memory_operation = "forget"

    if not isinstance(uncertain_terms, list):
        uncertain_terms = []

    persistence_class = raw_understanding.get(
        "persistence_class", "unknown"
    ) or "unknown"
    memory_category = raw_understanding.get("memory_category", None)
    memory_tags = raw_understanding.get("memory_tags", []) or []
    missing_information = raw_understanding.get(
        "missing_information", []
    ) or []

    if not isinstance(memory_tags, list):
        memory_tags = []
    if not isinstance(missing_information, list):
        missing_information = []

    confidence_breakdown = raw_understanding.get(
        "confidence_breakdown", {}
    ) or {}
    if not isinstance(confidence_breakdown, dict):
        confidence_breakdown = {}

    goal     = (raw_understanding.get("goal",     "") or "").lower().strip()
    intent   = (raw_understanding.get("intent",   "") or "").lower().strip()
    category = (raw_understanding.get("category", "") or "").lower().strip()
    raw_text = (raw_understanding.get("raw_text", "") or "").lower().strip()

    # Structural flags shared across the rules. Token-level
    # grammatical signals (user pronouns) — never topic keywords.
    tokens = set(raw_text.split())
    references_user = bool(tokens & USER_PRONOUNS)

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

    # A retrieval question that references the user ("what do i
    # do every morning", "whats my morning routine") is about the
    # user's own facts even when the Understanding LLM labels the
    # category "general" and sets an empty scope. The pronoun is a
    # structural signal, not a topic keyword — the same signal
    # prompt_builder already uses to decide personal vs world.
    if is_retrieval and (
        category_is_personal or text_is_personal or references_user
    ):
        if "semantic" not in memory_types:
            memory_types.append("semantic")
        if memory_operation is None:
            memory_operation = "query"

    # --------------------------------------------------
    # Rule 3
    # Broad retrieval fallback.
    # Activates semantic when retrieval was detected but
    # nothing else matched. Never overrides an explicit
    # "none" scope — pure world questions ("what is the
    # capital of France") have no memory needs.
    # --------------------------------------------------

    if (
        memory_scope != "none"
        and is_retrieval
        and "semantic" not in memory_types
    ):
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
    # Rule 7
    # Structured recall of past conversation.
    # The Understanding model signals a request to recap
    # or recall what was previously discussed through its
    # own taxonomy (category=conversation, goal=summarize/
    # recall, or required_systems.episodes). No message
    # text is inspected here; the model's structured output
    # is the only signal. Those requests are routed to
    # episodic memory so the past session is retrieved.
    # --------------------------------------------------

    structured_recall = (
        category == "conversation"
        or goal in ("summarize", "recall")
        or bool(required.get("episodes"))
    )

    if structured_recall:
        if "episodic" not in memory_types:
            memory_types.append("episodic")
        if memory_scope not in ("history", "episodic"):
            memory_scope = "episodic"

    # Structural flags shared by Rule 8 and Rule 10. Token-level
    # grammatical signals (interrogatives, user pronouns) and the
    # generic history phrasing set — never topic keywords. A trailing
    # tag-question marker ("we were working on the c program, right")
    # makes a statement read as the confirmation question it is, so
    # recall detection engages for it too.
    starts_as_question = raw_text.startswith(
        tuple(INTERROGATIVE_WORDS)
    )
    is_question_turn = (
        starts_as_question
        or raw_text.rstrip().endswith("?")
        or raw_text.rstrip().endswith((" right", " right?"))
        or is_retrieval
    )

    # --------------------------------------------------
    # Rule 8
    # Universal semantic recall.
    # The Understanding LLM does not always label a request
    # to recap a previous conversation (its output is
    # nondeterministic). Keyword lists are forbidden by
    # design, so instead the message is compared against
    # several semantic centroids of the general concept
    # "recap what was discussed before". Embedding
    # similarity generalizes to any phrasing. Fail-open:
    # no provider or low similarity means the rule does
    # nothing.
    #
    # Triggers:
    #   - a question that references the user ("did we work
    #     on a rust problem together") at >= 0.55
    #   - a question with no user pronoun only when clearly
    #     past-conversation ("what happened in the last
    #     session") at >= 0.60
    #   - a non-question statement only when unmistakably a
    #     recap request ("anything from my last session")
    #     at >= 0.70, so ordinary statements that merely
    #     mention "previous episode" or "earlier" are never
    #     misrouted to episodes.
    # --------------------------------------------------

    if not structured_recall:
        sim = _recall_similarity(raw_text)

        # Structural backstop: the message uses a closed
        # past-conversation frame ("remind me what we planned",
        # "anything from our chat about X") AND references the user.
        # Engages episodic even when the small model under-labels the
        # turn and the centroid similarity is low.
        recall_phrase = (
            references_user
            and any(
                phrase in raw_text
                for phrase in RECALL_PHRASES
            )
        )

        if (
            recall_phrase
            or (
                sim is not None
                and (
                    (
                        is_question_turn
                        and references_user
                        and sim >= _RECALL_CENTROID_THRESHOLD
                    )
                    or (
                        is_question_turn
                        and not references_user
                        and sim >= _RECALL_QUESTION_NO_USER_THRESHOLD
                    )
                    or (
                        not is_question_turn
                        and references_user
                        and sim >= _RECALL_STATEMENT_THRESHOLD
                    )
                )
            )
        ):
            if "episodic" not in memory_types:
                memory_types.append("episodic")
            if memory_scope not in ("history", "episodic"):
                memory_scope = "episodic"

    # --------------------------------------------------
    # Rule 9
    # A recall turn is never a write.
    # When the message is understood as a recap of a previous
    # conversation or session (structured or centroid
    # detected), it is asking about the past — it must never
    # store a canonical fact. The Understanding LLM sometimes
    # emits a store operation and a hallucinated canonical_fact
    # for such questions ("anything from my last session" ->
    # "I study btag"). Force the operation to a query and drop
    # the fabricated fact so the message reads memory instead
    # of poisoning it.
    # --------------------------------------------------

    if "episodic" in memory_types:
        if memory_operation in ("store", "update", None):
            memory_operation = "query"
        canonical_fact = None

    # --------------------------------------------------
    # Rule 10
    # History-phrased questions never write.
    # A message that explicitly reaches into the past
    # ("used to", "previously", "before", "what was") AND
    # contains a question is a read of the changed-fact trail,
    # never a store. Without this the LLM happily emits
    # "I used to eat ramen every day" as a canonical_fact for
    # "i used to eat ramen every day who is my best friend".
    # The history scope lets the query builder read the change
    # trail; the write is suppressed.
    # --------------------------------------------------

    from src.memory.memory_query_builder import HISTORY_PHRASES

    has_interrogative_word = bool(
        (set(raw_text.split()) & INTERROGATIVE_WORDS)
        or "?" in raw_text
    )
    history_phrase_present = any(
        phrase in raw_text for phrase in HISTORY_PHRASES
    )

    if (
        history_phrase_present
        and references_user
        and has_interrogative_word
    ):
        if memory_scope not in ("history", "episodic"):
            memory_scope = "history"
        if "semantic" not in memory_types:
            memory_types.append("semantic")
        memory_operation = "query"
        canonical_fact = None

    # --------------------------------------------------
    # Rule 11
    # "You remember/know/recall X" is a question to FRIDAY,
    # never a store. A second-person address ("you") joined
    # with a knowledge-state verb asks FRIDAY what it has
    # stored — "you remember my favorite food is sushi?"
    # reads memory, it does not overwrite it. Without this
    # the Understanding LLM emits a store and a canonical
    # fact for the question, clobbering the stored value.
    # The fact-drop form "did you know X" is excluded so a
    # shared fact ("did you know I play Zelda") still stores.
    # Force a query and drop the fact.
    # --------------------------------------------------

    has_second_person = bool(
        set(raw_text.split()) & SECOND_PERSON_PRONOUNS
    )
    has_knowledge_verb = bool(
        set(raw_text.split()) & KNOWLEDGE_VERBS
    )
    is_fact_drop = "did you know" in raw_text

    if (
        has_second_person
        and has_knowledge_verb
        and not is_fact_drop
        and memory_operation != "forget"
    ):
        memory_operation = "query"
        canonical_fact = None
        if "semantic" not in memory_types:
            memory_types.append("semantic")

    # --------------------------------------------------
    # Rule 12
    # Declining an offer is never a memory write.
    # "you don't have to write it again" / "no need to X"
    # tells FRIDAY NOT to do something — the LLM misreads
    # the verb ("write") as a memory store and emits a
    # garbage canonical fact. A first-person subject
    # ("I don't have to work tomorrow") is a statement
    # about the user's own situation and stays a store.
    # Force the operation off and drop the fact.
    # --------------------------------------------------

    DECLINATION_FRAMES = (
        "dont have to", "don't have to", "do not have to",
        "doesn't have to", "does not have to",
        "dont need to", "don't need to", "do not need to",
        "no need to", "no need",
        "dont bother", "don't bother", "do not bother",
    )

    has_declination = any(
        frame in raw_text for frame in DECLINATION_FRAMES
    )
    # "me" is always an object pronoun ("tell me about it") and never
    # marks a first-person declarative, so it must not exempt a
    # declination. Only true first-person subjects/possessives do.
    first_person_declination = bool(
        tokens & {"i", "im", "i'm", "i've", "ive",
                  "we", "my", "mine", "myself"}
    )

    if (
        has_declination
        and not first_person_declination
        and memory_operation != "forget"
    ):
        memory_operation = None
        canonical_fact = None

    # --------------------------------------------------
    # Rule 13
    # Imperative removal commands never store.
    # "forget my favorite food is lasagna" is a command to
    # DELETE a stored fact, but the Understanding LLM emits
    # a store/update with a garbage canonical fact for it
    # ("My favorite food"). A message whose FIRST token is
    # a removal verb is forced to the forget operation; any
    # echoed command clause is stripped from the delete
    # target so the target is the fact itself. Structured
    # goal 'delete' is honored the same way regardless of
    # phrasing. Topic dismissals ("forget it", "drop this
    # topic") are already suppressed by the conversation-
    # flow classifier, so they never reach this rule as a
    # write.
    # --------------------------------------------------

    first_token = (raw_text.split() or [""])[0]
    goal_is_delete = goal in ("delete", "forget", "remove")

    if (
        first_token in REMOVAL_VERBS or goal_is_delete
    ) and memory_operation != "forget":
        memory_operation = "forget"
        if "semantic" not in memory_types:
            memory_types.append("semantic")

    if memory_operation == "forget" and canonical_fact:
        cleaned = str(canonical_fact).strip()
        lowered = cleaned.lower()
        for clause in REMOVAL_LEAD_CLAUSES:
            if lowered.startswith(clause):
                cleaned = cleaned[len(clause):].strip()
                break
        if cleaned:
            canonical_fact = (
                cleaned[0].upper() + cleaned[1:]
            )

    # --------------------------------------------------
    # Rule 5
    # Episodes always need semantic alongside them.
    # --------------------------------------------------

    if "episodic" in memory_types:
        if "semantic" not in memory_types:
            memory_types.append("semantic")

    # --------------------------------------------------
    # Rule 6
    # Canonical fact present but operation forgotten.
    # The Understanding prompt only allows canonical_fact
    # for store/update, so a present canonical with no
    # operation is the LLM dropping the operation field,
    # not a query. Default to store. Downstream gates
    # (classifier, evaluator, validator) still apply, so
    # a weak or transient fact is never silently kept.
    # --------------------------------------------------

    if (
        memory_operation is None
        and canonical_fact
        and str(canonical_fact).strip()
    ):
        memory_operation = "store"
        if "semantic" not in memory_types:
            memory_types.append("semantic")

    requires_memory = len(memory_types) > 0

    return {
        "requires_memory":  requires_memory,
        "memory_types":     memory_types,
        "memory_scope":     memory_scope,
        "memory_operation": memory_operation,
        "canonical_fact":   canonical_fact,
        "uncertain_terms":  uncertain_terms,
        "persistence_class": persistence_class,
        "memory_category":  memory_category,
        "memory_tags":      memory_tags,
        "missing_information": missing_information,
        "confidence_breakdown": confidence_breakdown,
        "reason":           "Requested by Understanding Layer.",
        "confidence":       raw_understanding.get("confidence", 1.0),
    }