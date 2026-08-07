import re

from src.contracts.language_understanding import (
    LanguageUnderstanding,
    SemanticUnderstanding,
    ConversationUnderstanding,
    MemoryUnderstanding,
    ContextUnderstanding,
    EmotionUnderstanding,
    RequiredSystems,
)

from src.understanding.llm_understanding import understand
from src.understanding.semantic_analyzer import analyze_semantics
from src.understanding.conversation_analyzer import analyze_conversation
from src.understanding.memory_analyzer import analyze_memory
from src.understanding.emotion_analyzer import analyze_emotion
from src.understanding.context_analyzer import analyze_context
from src.understanding.triage import classify_trivial

from src.contracts.capability import (
    CapabilityCategory,
)

from src.memory.memory_fact import MemoryFact, now_iso
from src.memory.knowledge_normalizer import (
    normalize_for_understanding,
)


def _float_or_none(value):
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


# Closed-class English words that may appear capitalized mid-sentence
# ("Priya and I built a chess bot") without being invented proper
# nouns. A token is checked against this set, the user's message,
# and the recent context before being called an invention.
_COMMON_WORDS = frozenset(
    """
    the a an of to in on at for from with by my i you he she it we
    they this that is are was were be been have has had do does did
    not no yes so and or but if then than as
    """.split()
)


def _alnum_lower(token):
    return "".join(ch for ch in token if ch.isalnum()).lower()


def _provenance_allowed_tokens(
    user_message, recent_context=None
):
    """
    The set of grounded tokens a candidate fact token may be
    proven against: every token in the user's message plus every
    user turn in the recent conversation it references.
    """
    allowed = {
        _alnum_lower(token)
        for token in str(user_message).split()
    }
    if recent_context:
        for item in recent_context:
            if not isinstance(item, dict):
                continue
            user = item.get("user") or ""
            allowed.update(
                _alnum_lower(token)
                for token in str(user).split()
            )
    return allowed


def _proven(lowered, allowed):
    """
    True when a candidate token is grounded in the message or its
    context. Exact matches count, and so do merged-word
    normalizations: "capetown" covers "Cape" and "Town",
    "the handmaid tale" covers "Handmaid's" and "Tale". A genuine
    invention ("lenovo loq" -> "ThinkPad") shares no prefix or
    suffix with any allowed token and is still flagged.
    Prefix/suffix checks require both sides to be >= 3 letters so
    a 2-letter word ("is", "my") never subsumes an unrelated
    capitalized token ("Island", "Myth").
    """
    if lowered in allowed:
        return True
    for token in allowed:
        if len(lowered) >= 3 and len(token) >= 3:
            if token.startswith(lowered) or token.endswith(lowered):
                return True
            if lowered.startswith(token) or lowered.endswith(token):
                return True
    return False


def _invented_proper_nouns(
    canonical_fact, user_message, recent_context=None
):
    """
    Detects proper nouns in a canonical fact that were NOT present
    in the user's message (or the recent conversation it references).

    The small Understanding model occasionally "completes" a brand
    or product name it half-recognizes ("my laptop is lenovo loq"
    -> "My laptop is Lenovo ThinkPad LoQ"). Those invented words
    would be baked into long-term memory as fact, so any
    non-initial, capitalized token that appears nowhere in the
    message or its context is treated as unconfirmed. The check is
    purely structural (capitalization + provenance) — it never
    looks at which brand the user named, so it generalizes to every
    message.
    """
    if not canonical_fact:
        return []

    allowed = _provenance_allowed_tokens(
        user_message, recent_context
    )

    tokens = str(canonical_fact).split()

    invented = []

    for index, token in enumerate(tokens):
        lowered = _alnum_lower(token)
        if not lowered or len(lowered) < 2:
            continue
        if lowered[0].isdigit():
            continue
        if index == 0:
            continue
        if lowered in _COMMON_WORDS or _proven(lowered, allowed):
            continue
        if token[0].isupper():
            invented.append(token)

    return invented


def _unproven_uncertain_terms(
    uncertain_terms, user_message, recent_context=None
):
    """
    Filters the Understanding model's uncertain_terms down to the
    terms that are NOT verbatim in the user's message (or the recent
    conversation it references).

    The small model routinely flags perfectly ordinary words it DID
    hear — "beetle", "coleslaw" — as uncertain simply because the
    value feels uncommon. A term the user actually spoke is not a
    fabrication, so it must not trip the strict uncertainty gate by
    itself; confidence alone (the LOW_CONFIDENCE_FLOOR) then guards
    the write. Only a genuinely unproven term — a hallucinated name,
    a word never said — keeps blocking. Purely structural provenance;
    it never judges meaning.
    """
    if not uncertain_terms:
        return []

    allowed = _provenance_allowed_tokens(
        user_message, recent_context
    )

    unproven = []

    for term in uncertain_terms:
        if not isinstance(term, str):
            continue
        lowered = _alnum_lower(term)
        if not lowered or _proven(lowered, allowed):
            continue
        unproven.append(term)

    return unproven


# Copulas used to separate a fact's subject from its value.
_VALUE_COPULAS = (" is ", " are ", " was ", " were ")

# Leading temporal fillers the small model copies into a rebuilt
# value ("now", "currently") that are not part of the fact itself.
_VALUE_FILLERS = ("now", "currently", "still", "actually")


def _extract_fact_value(canonical_fact):
    """
    Extracts the VALUE of a canonical copula fact ("My favorite
    coffee is mocha" -> "mocha"). Non-copula facts (habits,
    preferences like "I like jazz") return None — they carry no
    separable value and are never touched by the value-origin guard.
    """
    if not isinstance(canonical_fact, str):
        # The Understanding model occasionally fills canonical_fact
        # with structured content (dict/list) instead of a sentence.
        # The value-origin guard is a no-op for those — never crash
        # on a non-string fact.
        return None
    text = (canonical_fact or "").strip()
    if not text:
        return None
    lowered = text.lower()
    for copula in _VALUE_COPULAS:
        idx = lowered.rfind(copula)
        if idx > 0:
            value = text[idx + len(copula):].strip()
            if value:
                return value
    return None


def _value_tokens(value):
    """
    The alphanumeric token set of a value, used for provenance
    comparison ("root beer" -> {"root", "beer"}).
    """
    if not value:
        return set()
    return {
        _alnum_lower(token)
        for token in value.split()
        if _alnum_lower(token)
    }


def _message_value_candidates(user_message):
    """
    Deterministically extracts a candidate replacement value from the
    user's own words when a fact's value was clearly taken from the
    recent context instead. This is the mirror image of the invented-
    noun gate: rather than fabricate a brand, the model copied the
    OLD value from the conversation buffer ("my favorite coffee is
    root beer" from a previous turn). The user's actual new value is
    still present in the current message and can be recovered.

    Matches structural phrasings only:
      "now my favorite coffee is mocha"          -> "mocha"
      "actually my favorite coffee is now flat white" -> "flat white"
      "no wait, i prefer sangria for my favorite coffee" -> "sangria"
    """
    msg = " " + str(user_message or "").lower() + " "

    for pattern in (
        r"favorite\b.+?\bis\b\s+(.+?)[.,!]?\s*$",
        r"\bprefer\b\s+(.+?)\s+for\b",
    ):
        match = re.search(pattern, msg)
        if not match:
            continue
        candidate = match.group(1).strip().strip(".,!")
        if not candidate:
            continue
        parts = [p for p in candidate.split() if p not in _VALUE_FILLERS]
        if parts:
            return " ".join(parts)
    return None


def _value_leaks_from_context(fact, user_message, recent_context):
    """
    True when a pending write's value appears in the recent
    conversation but NOT in the user's current message. That is the
    signature of the model copying a stale value out of the RECENT
    CONVERSATION block ("now my favorite coffee is mocha" stored as
    the old "root beer" from the previous turn). Such a fact must
    never reach long-term memory with a value the user did not just
    confirm.
    """
    if not (fact.is_write() and fact.canonical_fact):
        return False
    if not recent_context:
        return False

    value = _extract_fact_value(fact.canonical_fact)
    if not value:
        return False

    value_set = _value_tokens(value)
    if not value_set:
        return False

    message_set = _value_tokens(str(user_message or ""))
    if message_set & value_set:
        return False

    for item in recent_context:
        if not isinstance(item, dict):
            continue
        context_set = _value_tokens(item.get("user") or "")
        if context_set & value_set:
            return True

    return False


def _replace_fact_value(canonical_fact, new_value):
    """
    Rebuilds a copula fact with a corrected value, preserving the
    subject the model (correctly) extracted: "My favorite coffee is
    root beer" + "mocha" -> "My favorite coffee is mocha".
    """
    text = (canonical_fact or "").strip()
    if not text or not new_value:
        return None
    lowered = text.lower()
    for copula in _VALUE_COPULAS:
        idx = lowered.rfind(copula)
        if idx > 0:
            return (text[:idx + len(copula)] + new_value).strip()
    return None


# =====================================================
# TRIVIAL RESPONSE TEMPLATES
#
# brain.py answers trivial social messages ("hello",
# "bye", "thanks") with a template via the "trivial"
# metadata marker — the generative LLM is never invoked
# on that path (zero LLM calls).
# =====================================================

TRIVIAL_GOALS = {
    "greeting":    "continue_conversation",
    "farewell":    "continue_conversation",
    "gratitude":   "continue_conversation",
    "affirmation": "continue_conversation",
    "small_talk":  "continue_conversation",
}

TRIVIAL_INTENTS = {
    "greeting":    "conversation",
    "farewell":    "conversation",
    "gratitude":   "conversation",
    "affirmation": "conversation",
    "small_talk":  "conversation",
}

TRIVIAL_CATEGORIES = {
    "greeting":    "social",
    "farewell":    "social",
    "gratitude":   "social",
    "affirmation": "social",
    "small_talk":  "social",
}


class UnderstandingOrchestrator:

    """
    Runs the complete Understanding pipeline.

    Fast path:
    User message → Triage (embedding similarity)
    → If trivial: return lightweight Understanding
    → If not trivial: full LLM call + analyzers

    Slow path (full pipeline):
    User message → LLM call → analyzers → contract

    analyze() returns a (understanding, memory_fact) tuple.
    MemoryFact carries only the memory write instruction —
    the Memory layer never receives raw user text.
    """

    def _build_trivial_understanding(
        self,
        user_message: str,
        category: str,
    ):
        """
        Builds a minimal LanguageUnderstanding for
        messages that don't need deep understanding.
        No memory, no reasoning, no execution needed.
        The generative LLM still replies naturally.
        """

        understanding = LanguageUnderstanding(
            raw_text=user_message
        )

        understanding.semantic = SemanticUnderstanding(
            goal=TRIVIAL_GOALS.get(
                category, "continue_conversation"
            ),
            intent=TRIVIAL_INTENTS.get(
                category, "conversation"
            ),
            category=TRIVIAL_CATEGORIES.get(
                category, "social"
            ),
            capability=CapabilityCategory.SOCIAL,
            entities=[],
            confidence=1.0,
        )

        understanding.conversation = ConversationUnderstanding(
            conversation_state=category,
            requires_previous_context=False,
            continues_previous_topic=False,
            confidence=1.0,
        )

        understanding.memory = MemoryUnderstanding(
            requires_memory=False,
            memory_scope="none",
            reason="Trivial message — no memory needed.",
            confidence=1.0,
            memory_operation=None,
            memory_payload=None,
            persistence_class="unknown",
            memory_category=None,
            memory_tags=[],
            missing_information=[],
            confidence_breakdown={},
        )

        understanding.emotion = EmotionUnderstanding(
            emotion="neutral",
            sentiment="neutral",
            urgency="low",
            confidence=1.0,
        )

        understanding.context = ContextUnderstanding(
            requires_context=False,
            context_scope="none",
            reason="Trivial message.",
            confidence=1.0,
        )

        understanding.required_systems = RequiredSystems(
            memory=False,
            episodes=False,
            context=False,
            tools=False,
            web=False,
            vision=False,
            planning=False,
            reasoning=False,
        )

        understanding.confidence = 1.0

        # Triage fast-path marker so brain.py can answer with a
        # template response and skip the generative LLM entirely
        # (zero LLM calls on trivial social messages).
        understanding.metadata["trivial"] = category

        memory_fact = MemoryFact(
            operation=None,
            canonical_fact=None,
            uncertain_terms=[],
            confidence=1.0,
            source_text=user_message,
            persistence_class="unknown",
            category=None,
            tags=[],
            created_at=now_iso(),
            updated_at=now_iso(),
        )

        return understanding, memory_fact

    def analyze(self, user_message: str, recent_context=None):

        # =====================================
        # FAST PATH — TRIAGE
        # Check if this is a trivial social
        # message before calling the LLM.
        # =====================================

        trivial_category = classify_trivial(user_message)

        if trivial_category is not None:

            return self._build_trivial_understanding(
                user_message,
                trivial_category,
            )

        # =====================================
        # SLOW PATH — FULL LLM UNDERSTANDING
        # =====================================

        # Short follow-ups ("yes you tell me", "go ahead") are
        # unclassifiable without the recent exchange. Pull the
        # working buffer (same source the reasoning engine uses)
        # so the Understanding LLM can classify them correctly.
        # Local import mirrors reasoning_engine._has_recent_context.
        if recent_context is None:
            try:
                from src.core.context_manager import get_recent_context
                recent_context = get_recent_context()
            except Exception:
                recent_context = None

        # Normalize variant spellings BEFORE the LLM decides
        # uncertain_terms. The detector must read a canonical form
        # ("b.tech" -> "b tech") so it never flags a valid concept
        # as a typo. raw_text below still keeps the original.
        normalized_message = normalize_for_understanding(
            user_message
        )

        raw_understanding = understand(
            normalized_message or user_message,
            recent_context=recent_context,
        )

        if raw_understanding is None:
            return None, None

        # Inject raw_text so analyzers can inspect
        # the original message when LLM output is
        # unreliable for edge cases.
        raw_understanding["raw_text"] = (
            user_message.lower().strip()
        )

        # =====================================
        # ANALYZERS
        # =====================================

        semantic     = analyze_semantics(raw_understanding)
        conversation = analyze_conversation(raw_understanding)
        memory       = analyze_memory(raw_understanding)
        emotion      = analyze_emotion(raw_understanding)
        context      = analyze_context(raw_understanding)

        # =====================================
        # CONTRACT
        # =====================================

        understanding = LanguageUnderstanding(
            raw_text=user_message
        )

        understanding.semantic = SemanticUnderstanding(
            goal=semantic.get("goal"),
            intent=semantic.get("intent"),
            category=semantic.get("category"),
            capability=semantic.get("capability"),
            entities=semantic.get("entities", []),
            time_reference=semantic.get("time_reference"),
            confidence=semantic.get("confidence", 0.0),
        )

        understanding.conversation = ConversationUnderstanding(
            conversation_state=conversation.get(
                "conversation_state"
            ),
            requires_previous_context=conversation.get(
                "requires_previous_context", False
            ),
            continues_previous_topic=conversation.get(
                "continues_previous_topic", False
            ),
            confidence=conversation.get("confidence", 0.0),
        )

        understanding.memory = MemoryUnderstanding(
            requires_memory=memory.get(
                "requires_memory", False
            ),
            memory_scope=memory.get("memory_scope"),
            reason=memory.get("reason", ""),
            confidence=memory.get("confidence", 0.0),
            memory_operation=memory.get("memory_operation"),
            memory_payload=memory.get("memory_payload"),
            persistence_class=memory.get("persistence_class"),
            memory_category=memory.get("memory_category"),
            memory_tags=memory.get("memory_tags", []),
            missing_information=memory.get(
                "missing_information", []
            ),
            confidence_breakdown=memory.get(
                "confidence_breakdown", {}
            ),
        )

        understanding.emotion = EmotionUnderstanding(
            emotion=emotion.get("emotion"),
            sentiment=emotion.get("sentiment"),
            urgency=emotion.get("urgency"),
            confidence=emotion.get("confidence", 0.0),
        )

        understanding.context = ContextUnderstanding(
            requires_context=context.get(
                "requires_context", False
            ),
            context_scope=context.get("context_scope"),
            reason=context.get("reason", ""),
            confidence=context.get("confidence", 0.0),
        )

        # =====================================
        # REQUIRED SYSTEMS
        # Memory and episodes pulled from the
        # analyzer — not from raw LLM JSON.
        # Analyzer is the authority.
        # =====================================

        systems = raw_understanding.get(
            "required_systems", {}
        )

        understanding.required_systems = RequiredSystems(
            memory=memory.get("requires_memory", False),
            episodes="episodic" in memory.get(
                "memory_types", []
            ),
            context=systems.get("context", False),
            tools=systems.get("tools", False),
            web=systems.get("web", False),
            vision=systems.get("vision", False),
            planning=systems.get("planning", False),
            reasoning=systems.get("reasoning", True),
        )

        # =====================================
        # PLANNING FLAG AUTHORITY
        # The full understanding prompt is too
        # large for the small model to label
        # goal-accomplishment requests reliably:
        # "i want to learn python" comes back as
        # goal=remember_information with
        # planning=False, so the plan never runs.
        # For command/request messages a dedicated
        # micro-classifier is the authority — the
        # same precedent as end_session above.
        # =====================================

        if (
            not understanding.required_systems.planning
            and semantic.get("intent")
            in ("command", "request")
        ):
            from src.understanding.end_session_analyzer import (
                detect_planning_request,
            )

            understanding.required_systems.planning = (
                detect_planning_request(user_message)
            )

        understanding.constraints = raw_understanding.get(
            "constraints", {}
        )
        understanding.metadata = raw_understanding.get(
            "metadata", {}
        )
        understanding.confidence = raw_understanding.get(
            "confidence", 0.0
        )

        # =====================================
        # CANONICAL END_SESSION SIGNAL
        # The full understanding prompt is too
        # large for the small model to label
        # session ends reliably, so a dedicated
        # micro-classifier decides. The
        # ExecutionManager maps this to the
        # runtime (exit voice loop / stop
        # listening) — never the response LLM.
        # =====================================

        from src.understanding.end_session_analyzer import (
            detect_end_session,
            detect_topic_dismissal,
        )

        understanding.metadata["end_session"] = (
            detect_end_session(user_message)
        )

        # =====================================
        # MEMORY FACT
        # A structured write/update instruction.
        # The Memory layer receives this object,
        # never the raw user message.
        # =====================================

        uncertain_terms = memory.get("uncertain_terms", [])

        breakdown = memory.get("confidence_breakdown", {})

        memory_fact = MemoryFact(
            operation=memory.get("memory_operation"),
            canonical_fact=memory.get("canonical_fact"),
            uncertain_terms=list(uncertain_terms),
            confidence=understanding.confidence,
            source_text=user_message,
            persistence_class=memory.get("persistence_class"),
            category=memory.get("memory_category"),
            tags=list(memory.get("memory_tags", [])),
            created_at=now_iso(),
            updated_at=now_iso(),
            stt_confidence=_float_or_none(breakdown.get("stt")),
            understanding_confidence=_float_or_none(
                breakdown.get("understanding")
            ),
            canonicalization_confidence=_float_or_none(
                breakdown.get("canonicalization")
            ),
            memory_confidence=_float_or_none(
                breakdown.get("memory")
            ),
            retrieval_confidence=_float_or_none(
                breakdown.get("retrieval")
            ),
        )

        # =====================================
        # META-DISCOURSE WRITE SUPPRESSION
        # Messages that end the session or dismiss
        # the current topic ("miss this topic",
        # "i am done for today") are meta-discourse
        # about the conversation itself — never a
        # durable user fact. The small model has
        # been observed storing garbage canonical
        # facts for them. Both micro-classifiers are
        # conservative; the topic-dismissal check
        # only runs when a write is actually pending
        # (no write, no cost).
        # =====================================

        if memory_fact.is_write():
            understanding.metadata["topic_dismissal"] = (
                detect_topic_dismissal(user_message)
            )

        if (
            understanding.metadata.get("end_session")
            or understanding.metadata.get("topic_dismissal")
        ):
            memory_fact.operation = None
            memory_fact.canonical_fact = None
            memory_fact.uncertain_terms = []
            memory_fact.persistence_class = None
            memory_fact.category = None
            memory_fact.tags = []
            understanding.memory = MemoryUnderstanding(
                requires_memory=False,
                memory_scope="none",
                reason=(
                    "Session or topic ending — meta-discourse is "
                    "never stored."
                ),
                confidence=1.0,
                memory_operation=None,
                memory_payload=None,
                persistence_class="unknown",
                memory_category=None,
                memory_tags=[],
                missing_information=[],
                confidence_breakdown={},
            )

        # =====================================
        # BRAND/MODEL FIDELITY GATE
        # The small Understanding model sometimes "completes" a
        # half-recognized brand or product name into a different
        # model ("my laptop is lenovo loq" -> "My laptop is Lenovo
        # ThinkPad LoQ"). An invented proper noun — one present in
        # neither the message nor the recent conversation it refers
        # to — is marked uncertain so it is never written to
        # long-term memory. Values drawn from the user's own words
        # or from the chat context pass through untouched.
        # =====================================

        if (
            memory_fact.is_write()
            and memory_fact.canonical_fact
        ):
            invented = _invented_proper_nouns(
                memory_fact.canonical_fact,
                user_message,
                recent_context=recent_context,
            )

            if invented:
                memory_fact.uncertain_terms.extend(invented)
                # An invented brand is exactly the "unconfirmed
                # extraction" the gate must catch. Since is_uncertain
                # is now corroborated by confidence (two-signal gate),
                # the invention must also pull confidence below the
                # threshold or it would slip through.
                if memory_fact.confidence is not None:
                    memory_fact.confidence = min(
                        memory_fact.confidence, 0.3
                    )
                surfacing = understanding.metadata.get(
                    "uncertain_terms", []
                )
                if isinstance(surfacing, list):
                    understanding.metadata["uncertain_terms"] = (
                        surfacing + invented
                    )
                else:
                    understanding.metadata["uncertain_terms"] = (
                        invented
                    )

        # =====================================
        # TERM-PROVENANCE DE-FLAG
        # The Understanding model also flags ordinary words it DID
        # hear ("my favorite animal is beetle" -> term "beetle").
        # A term verbatim in the user's message is grounded, not
        # fabricated, so it must not trigger the strict uncertainty
        # gate on its own. Unproven terms (hallucinated names) stay
        # flagged. Runs after the brand-fidelity gate so invented
        # proper nouns — unproven by construction — always survive.
        # =====================================

        if (
            memory_fact.is_write()
            and memory_fact.uncertain_terms
        ):
            memory_fact.uncertain_terms = _unproven_uncertain_terms(
                memory_fact.uncertain_terms,
                user_message,
                recent_context=recent_context,
            )

        # =====================================
        # VALUE-ORIGIN GUARD
        # The small model occasionally copies the OLD value from the
        # RECENT CONVERSATION block instead of the value the user is
        # now stating ("now my favorite coffee is mocha" stored as the
        # previous "root beer"). The invented-noun gate cannot catch
        # this: the stale value legitimately appears in the chat
        # context, so it passes provenance. This deterministic guard
        # compares the fact's value against the CURRENT message and
        # the recent context:
        #   * value in the message only -> healthy, untouched
        #   * value in the context only  -> stale copy: rebuild the
        #     value from the user's own words when a structural
        #     phrasing is present, otherwise suppress the write.
        # =====================================

        if _value_leaks_from_context(
            memory_fact,
            user_message,
            recent_context,
        ):
            replacement = _message_value_candidates(user_message)
            if replacement:
                rebuilt = _replace_fact_value(
                    memory_fact.canonical_fact,
                    replacement,
                )
                if rebuilt:
                    memory_fact.canonical_fact = rebuilt
                    memory_fact.updated_at = now_iso()
            else:
                memory_fact.operation = None
                memory_fact.canonical_fact = None
                memory_fact.uncertain_terms = []
                memory_fact.persistence_class = None
                memory_fact.category = None
                memory_fact.tags = []
                understanding.metadata["value_suppressed"] = True

        # Surface uncertain terms in the final prompt only when a
        # memory WRITE is at risk — a mishearing would be baked
        # into long-term memory. The Understanding prompt contracts
        # that any listed term lowers confidence below 0.5; if the
        # model listed a term but kept confidence high, it did not
        # really mean it blocks anything.
        # Queries never surface them: the honesty rules already
        # prevent FRIDAY from inventing answers, and flagging a
        # well-known term would make it hedge a question it can
        # actually answer.
        if (
            uncertain_terms
            and understanding.confidence < 0.5
            and memory_fact.is_write()
        ):
            understanding.metadata["uncertain_terms"] = (
                uncertain_terms
            )

        return understanding, memory_fact


understanding_orchestrator = UnderstandingOrchestrator()


def analyze(user_message: str):

    return understanding_orchestrator.analyze(
        user_message
    )