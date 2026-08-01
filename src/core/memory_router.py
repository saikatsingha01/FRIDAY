from src.core.reasoning_engine import (
    ReasoningResult,
)

from src.memory.memory_retriever import (
    retrieve_relevant_memories,
)

from src.memory.episode_retriever import (
    retrieve_relevant_episodes,
)

from src.core.context_manager import (
    get_recent_context,
)

from src.core.context_reasoner import (
    find_relevant_context,
)


class MemoryRouter:

    """
    Responsible for gathering every kind
    of information FRIDAY needs before
    planning a response.
    """

    def retrieve(

        self,

        user_message: str,

        reasoning: ReasoningResult

    ):

        understanding = reasoning.understanding

        memory = []

        episodes = []

        context = []

        # -------------------------------------

        if reasoning.use_memory:

            memory = retrieve_relevant_memories(

                user_message

            )

        # -------------------------------------

        if reasoning.use_episodes:

            episodes = retrieve_relevant_episodes(

                user_message

            )

        # -------------------------------------

        if reasoning.use_context:

            recent = get_recent_context()

            context = find_relevant_context(

                user_message,

                recent

            )

        # -------------------------------------

        return {

            "understanding": understanding,

            "memory": memory,

            "episodes": episodes,

            "context": context

        }


memory_router = MemoryRouter()