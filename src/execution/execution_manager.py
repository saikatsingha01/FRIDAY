from src.contracts.execution import ExecutionResult
from src.core.memory_router import memory_router


class ExecutionManager:

    """
    Coordinates every execution subsystem.

    The Brain never directly calls memory,
    tools, web, planner or vision.

    Everything runs through here.

    Each subsystem is a branch activated only
    when Reasoning decided it is needed.

    Does NOT:
    - Understand user intent
    - Create plans
    - Generate responses
    - Execute domain actions directly
    """

    def execute(
        self,
        user_message: str,
        reasoning,
    ) -> ExecutionResult:

        result = ExecutionResult()

        # ==========================================
        # END-SESSION MAPPING
        # The Understanding Layer classifies a
        # natural-language session end ("you can
        # sleep now", "go to sleep", "shut down")
        # as the canonical intent end_session. The
        # ExecutionManager decides the runtime
        # mapping — never the response LLM.
        # ==========================================

        intent = (
            (reasoning.understanding.semantic.intent or "")
            .lower()
            .strip()
        )

        goal = (
            (reasoning.understanding.semantic.goal or "")
            .lower()
            .strip()
        )

        end_session_metadata = (
            reasoning.understanding.metadata or {}
        ).get("end_session")

        result.end_session = (
            end_session_metadata is True
            or intent == "end_session"
            or goal in {"exit", "shutdown", "end_conversation"}
        )

        # ==========================================
        # MEMORY + EPISODES + CONTEXT via router
        # ==========================================

        if reasoning.use_memory:

            memory_bundle = memory_router.retrieve(
                user_message,
                reasoning,
            )

            result.memories = memory_bundle.get("memory", [])
            result.episodes = memory_bundle.get("episodes", [])
            result.context  = memory_bundle.get("context", [])
            result.history  = memory_bundle.get("history", [])

        # ==========================================
        # CONTEXT — always pull recent turns
        # when planning, context is needed, or
        # when the user is clearly continuing a thread.
        # ==========================================

        if not result.context and (
            reasoning.use_context
            or reasoning.use_planning
        ):

            from src.core.context_manager import (
                get_recent_context,
            )

            recent = get_recent_context()

            if recent:
                result.context = list(recent)

        # ==========================================
        # PLANNING
        # Pass everything available (recent context,
        # retrieved memories, past experiences) so the
        # planner can incorporate real constraints and
        # never invent user details.
        # ==========================================

        if reasoning.use_planning:

            from src.core.planner import planner

            result.planner_result = planner.plan(
                reasoning.understanding,
                recent_context=result.context,
                memories=result.memories,
                episodes=result.episodes,
            )

        # ==========================================
        # TOOLS — Phase 5
        # ==========================================

        if reasoning.use_tools:
            pass

        # ==========================================
        # WEB — Phase 5
        # ==========================================

        if reasoning.use_web:
            pass

        # ==========================================
        # VISION — Phase 10
        # ==========================================

        if reasoning.use_vision:
            pass

        # ==========================================
        # DEBUG
        # ==========================================

        print("\n========== EXECUTION ==========")
        print("Need Memory   :", reasoning.use_memory)
        print("Need Episodes :", reasoning.use_episodes)
        print("Need Context  :", reasoning.use_context)
        print("Need Tools    :", reasoning.use_tools)
        print("Need Web      :", reasoning.use_web)
        print("Need Vision   :", reasoning.use_vision)
        print("Need Planning :", reasoning.use_planning)
        print()
        print("Retrieved Memories :", len(result.memories))
        print("Retrieved Episodes :", len(result.episodes))
        print("Retrieved Context  :", len(result.context))

        if result.planner_result:
            print(
                "Plan Steps         :",
                len(result.planner_result.steps)
            )
            print(
                "Needs Clarification:",
                result.planner_result.requires_clarification
            )

        print("===============================\n")

        return result


execution_manager = ExecutionManager()