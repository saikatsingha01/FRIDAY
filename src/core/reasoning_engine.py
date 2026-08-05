from dataclasses import dataclass

from src.contracts.language_understanding import (
    LanguageUnderstanding,
)


@dataclass
class ReasoningResult:

    understanding: LanguageUnderstanding

    use_memory:   bool = False
    use_episodes: bool = False
    use_context:  bool = False
    use_tools:    bool = False
    use_web:      bool = False
    use_vision:   bool = False
    use_planning: bool = False

    continue_conversation: bool = True


PLANNING_GOALS = {
    "create",
    "plan",
    "solve_problem",
}


class ReasoningEngine:

    """
    Converts LanguageUnderstanding into execution decisions.

    Never parses English.
    Only reads structured fields from the understanding contract
    and applies deterministic rules.

    Decides:
    - Which systems are needed
    - Whether planning is required
    """

    def _has_recent_context(self) -> bool:
        """
        Checks if there are any recent conversation turns.
        If yes, context should always be pulled so FRIDAY
        never loses the thread mid-conversation.
        """
        try:
            from src.core.context_manager import get_recent_context
            return len(get_recent_context()) > 0
        except Exception:
            return False

    def _is_short_followup(self, understanding) -> bool:
        """
        Short follow-ups ("yes you tell me", "go ahead") are planning
        triggers when the Understanding LLM itself flagged that the
        message depends on prior conversation. The planner receives
        that context, so it builds the plan from the earlier request.
        Conservative: requires the model's context flag, existing
        turns, and a message too short to be a standalone request.
        """
        if not understanding.required_systems.context:
            return False

        if not self._has_recent_context():
            return False

        if len((understanding.raw_text or "").split()) > 5:
            return False

        return True

    def reason(
        self,
        understanding: LanguageUnderstanding,
    ) -> ReasoningResult:

        result = ReasoningResult(
            understanding=understanding,
        )

        systems = understanding.required_systems
        goal    = (understanding.semantic.goal or "").lower()

        # ==========================================
        # MEMORY
        # ==========================================

        result.use_memory = (
            understanding.memory.requires_memory
        )

        # ==========================================
        # EPISODES
        # ==========================================

        result.use_episodes = (
            systems.episodes
            or (understanding.semantic.category or "").lower() == "conversation"
            or (understanding.semantic.goal or "").lower() in ("summarize", "recall")
        )

        # ==========================================
        # CONTEXT
        # Always pull context when there are recent
        # turns — the LLM often misses the flag for
        # short follow-up messages ("yes", "okay",
        # "what about that") that are clearly part
        # of an ongoing exchange.
        # ==========================================

        result.use_context = (
            understanding.context.requires_context
            or self._has_recent_context()
        )

        # ==========================================
        # TOOLS / WEB / VISION
        # ==========================================

        result.use_tools  = systems.tools
        result.use_web    = systems.web
        result.use_vision = systems.vision

        # ==========================================
        # PLANNING
        # Driven by the Understanding LLM's structured
        # required_systems.planning flag, with a narrow
        # goal fallback. Categories are topics, not
        # tasks — a science question is NOT a plan.
        # ==========================================

        result.use_planning = (
            understanding.required_systems.planning
            or goal in PLANNING_GOALS
            or self._is_short_followup(understanding)
        )

        return result


reasoning_engine = ReasoningEngine()