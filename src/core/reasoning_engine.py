from dataclasses import dataclass

from src.contracts.language_understanding import (
    LanguageUnderstanding,
)


@dataclass
class ReasoningResult:

    understanding: LanguageUnderstanding

    use_memory: bool = False
    use_episodes: bool = False
    use_context: bool = False

    use_tools: bool = False
    use_web: bool = False
    use_vision: bool = False

    continue_conversation: bool = True


class ReasoningEngine:
    """
    Converts Language Understanding into
    execution decisions.

    It never parses English.
    It only reasons over structured understanding.
    """

    def reason(

        self,

        understanding: LanguageUnderstanding,

    ) -> ReasoningResult:

        result = ReasoningResult(

            understanding=understanding,

        )

        # ==========================================
        # MEMORY
        # ==========================================

        result.use_memory = (

            understanding.memory.requires_memory

        )

        # ==========================================
        # CONTEXT
        # ==========================================

        result.use_context = (

            understanding.context.requires_context

        )

        # ==========================================
        # FUTURE ROUTING
        # ==========================================

        systems = understanding.required_systems

        result.use_tools = systems.tools

        result.use_web = systems.web

        result.use_vision = systems.vision

        result.use_episodes = systems.episodes

        return result


reasoning_engine = ReasoningEngine()