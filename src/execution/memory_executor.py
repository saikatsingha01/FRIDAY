from src.core.memory_router import memory_router


class MemoryExecutor:
    """
    Responsible for executing all memory-related retrieval.

    The Execution Layer should never know how memory works.
    It only asks this executor.
    """

    def execute(

        self,

        user_message,

        reasoning,

    ):

        return memory_router.retrieve(

            user_message,

            reasoning,

        )


memory_executor = MemoryExecutor()