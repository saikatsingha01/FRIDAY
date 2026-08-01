from src.contracts.execution import (
    ExecutionResult,
)

from src.core.memory_router import (
    memory_router,
)


class ExecutionManager:
    """
    Coordinates every execution subsystem.

    The Brain never directly calls memory,
    tools, web, planner or vision.

    Everything is executed through here.
    """

    def execute(

        self,

        user_message,

        reasoning,

    ):

        result = ExecutionResult()

        # ==========================================
        # MEMORY
        # ==========================================

        if reasoning.use_memory:

            memory_bundle = memory_router.retrieve(

                user_message,

                reasoning,

            )

            result.memories = memory_bundle.get(

                "memory",

                [],

            )

            result.episodes = memory_bundle.get(

                "episodes",

                [],

            )

            result.context = memory_bundle.get(

                "context",

                [],

            )

        # ==========================================
        # CONTEXT
        # ==========================================

        if reasoning.use_context:

            pass

        # ==========================================
        # TOOLS
        # ==========================================

        if reasoning.use_tools:

            pass

        # ==========================================
        # WEB
        # ==========================================

        if reasoning.use_web:

            pass

        # ==========================================
        # VISION
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

        print()

        print("Retrieved Memories :", len(result.memories))
        print("Retrieved Episodes :", len(result.episodes))
        print("Retrieved Context  :", len(result.context))

        print("===============================\n")

        return result


execution_manager = ExecutionManager()