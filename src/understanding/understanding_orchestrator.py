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


class UnderstandingOrchestrator:

    """
    Runs the complete Understanding pipeline.

    User
      ↓
    One LLM call
      ↓
    Specialized analyzers
      ↓
    LanguageUnderstanding contract
    """

    def analyze(self, user_message: str):

        # =====================================
        # SINGLE LLM CALL
        # =====================================

        raw_understanding = understand(user_message)

        if raw_understanding is None:
            return None

        # =====================================
        # Inject raw_text so analyzers can
        # inspect the original message directly
        # when LLM classification is unreliable.
        # =====================================

        raw_understanding["raw_text"] = user_message.lower().strip()

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

        understanding = LanguageUnderstanding(raw_text=user_message)

        understanding.semantic = SemanticUnderstanding(
            goal=semantic.get("goal"),
            intent=semantic.get("intent"),
            category=semantic.get("category"),
            entities=semantic.get("entities", []),
            time_reference=semantic.get("time_reference"),
            confidence=semantic.get("confidence", 0.0),
        )

        understanding.conversation = ConversationUnderstanding(
            conversation_state=conversation.get("conversation_state"),
            requires_previous_context=conversation.get(
                "requires_previous_context", False
            ),
            continues_previous_topic=conversation.get(
                "continues_previous_topic", False
            ),
            confidence=conversation.get("confidence", 0.0),
        )

        understanding.memory = MemoryUnderstanding(
            requires_memory=memory.get("requires_memory", False),
            memory_scope=memory.get("memory_scope"),
            reason=memory.get("reason", ""),
            confidence=memory.get("confidence", 0.0),
            memory_operation=memory.get("memory_operation"),
            memory_payload=memory.get("memory_payload"),
        )

        understanding.emotion = EmotionUnderstanding(
            emotion=emotion.get("emotion"),
            sentiment=emotion.get("sentiment"),
            urgency=emotion.get("urgency"),
            confidence=emotion.get("confidence", 0.0),
        )

        understanding.context = ContextUnderstanding(
            requires_context=context.get("requires_context", False),
            context_scope=context.get("context_scope"),
            reason=context.get("reason", ""),
            confidence=context.get("confidence", 0.0),
        )

        # =====================================
        # REQUIRED SYSTEMS
        # Pull memory and episodes from the
        # analyzer result, not from the raw LLM
        # JSON. Analyzer is the authority here.
        # =====================================

        systems = raw_understanding.get("required_systems", {})

        understanding.required_systems = RequiredSystems(
            memory=memory.get("requires_memory", False),
            episodes="episodic" in memory.get("memory_types", []),
            context=systems.get("context", False),
            tools=systems.get("tools", False),
            web=systems.get("web", False),
            vision=systems.get("vision", False),
            planning=systems.get("planning", False),
            reasoning=systems.get("reasoning", True),
        )

        understanding.constraints = raw_understanding.get("constraints", {})
        understanding.metadata    = raw_understanding.get("metadata", {})
        understanding.confidence  = raw_understanding.get("confidence", 0.0)

        return understanding


understanding_orchestrator = UnderstandingOrchestrator()


def analyze(user_message: str):
    return understanding_orchestrator.analyze(user_message)