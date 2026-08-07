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

    # True when use_planning was enabled ONLY by the continuity
    # gate — i.e. the message itself was not a goal (no planning
    # flag, not a planning goal, not a short follow-up), but an
    # active plan exists. Lets the caller distinguish a genuine
    # new goal from a mid-plan detour (question, fact statement)
    # so a detour never replaces the active plan.
    continuity_only: bool = False

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

    def _is_launch_signal(self, understanding) -> bool:
        """
        True when the structured fields prove an application launch,
        regardless of the Understanding model's tools flag. Lazy import
        keeps the layers decoupled (tool_router never imports this
        module). A repeat "open spotify" keeps need_tools live even
        when prior conversation makes the small model drop the flag.
        """
        try:
            from src.core.tool_router import has_launch_signal
            return has_launch_signal(understanding)
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

    def _continues_active_plan(self, understanding) -> bool:
        """
        Universal planning-continuity gate.

        A plan was generated in an earlier turn and is still the
        active goal. A follow-up that keeps that conversation alive
        stays on the planning path so the goal is never abandoned
        mid-thread ("no, not game dev — just python" after a learn-
        python plan; "ok so what is the first step"). The PLANNER is
        the arbiter of whether the new message truly continues the
        goal; this gate only decides whether the planner gets a
        chance.

        Reads structured contract fields only — never message text.
        Questions are passed through deliberately: a continuation
        question ("what is the first step") is indistinguishable
        from an unrelated one ("what is the weather") at the intent
        level, so the planner arbitrates both. When the planner
        decides the question does NOT continue the goal, the
        reasoning layer marks it as a detour (continuity_only) and
        the caller answers it on the normal path without replacing
        the active plan. Pure conversation and greetings are strong
        signals the user is not driving a goal forward and are
        skipped. Ends the active plan on a detected session end.
        """
        from src.core.context_manager import (
            get_active_plan,
            clear_active_plan,
        )

        if get_active_plan() is None:
            return False

        if understanding.metadata.get("end_session") is True:
            clear_active_plan()
            return False

        intent = (understanding.semantic.intent or "").lower().strip()

        if intent in {"conversation", "greeting"}:
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

        # Deterministic launch gate — structured fields plus, on a
        # long repeat where the Understanding model lost every signal
        # (KI-009), the user's own "open/launch X" words. Computed
        # once; it keeps the tool path live AND shields the turn from
        # the planning gate.
        launch_signal = self._is_launch_signal(understanding)

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
        # use_tools follows the Understanding flag OR the
        # deterministic launch signal. The flag alone is not
        # trustworthy for launches: on a repeat "open spotify"
        # the small model sees prior conversation mentioning
        # Spotify and drops required_systems.tools — the
        # structured launch signal keeps the decision stable
        # and the request evaluated fresh every turn.
        # ==========================================

        result.use_tools  = (
            systems.tools or launch_signal
        )
        result.use_web    = systems.web
        result.use_vision = systems.vision

        # ==========================================
        # PLANNING
        # Driven by the Understanding LLM's structured
        # required_systems.planning flag, with a narrow
        # goal fallback. Categories are topics, not
        # tasks — a science question is NOT a plan.
        # The continuity gate adds messages that keep
        # an existing active plan alive. continuity_only
        # records when the gate is the sole reason
        # planning is on, so mid-plan detours can be
        # answered normally without replacing the goal.
        # ==========================================

        base_planning = (
            understanding.required_systems.planning
            or goal in PLANNING_GOALS
            or self._is_short_followup(understanding)
        )
        continuity = self._continues_active_plan(understanding)

        # A launch command is a fresh, self-contained action request —
        # the planning gate must never hijack it. On a long repeat the
        # small model drifts launch turns into the planning path
        # (KI-009: "open notepad" -> "I'll continue with step 2 of the
        # execution plan", empty TOOL RESULTS). And the Phase 5
        # planner's tool steps do not execute tools anyway, so a
        # planned launch would only produce an empty tool block. The
        # launch signal pins the turn to the direct tool path.
        result.use_planning = (base_planning or continuity) and not launch_signal
        result.continuity_only = (
            continuity and not base_planning and not launch_signal
        )

        return result


reasoning_engine = ReasoningEngine()