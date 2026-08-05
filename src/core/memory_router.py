from src.core.reasoning_engine import ReasoningResult
from src.memory.memory_retriever import (
    retrieve_with_query,
    retrieve_history,
)
from src.memory.episode_retriever import (
    retrieve_relevant_episodes,
    build_episode_query,
)
from src.memory.memory_query_builder import build_memory_query
from src.core.context_manager import get_recent_context
from src.core.context_reasoner import find_relevant_context


class MemoryRouter:

    """
    Coordinates all information retrieval.

    Receives structured LanguageUnderstanding — never raw text.
    Builds structured queries and passes them to the retrievers.

    No raw user_message flows to any retriever:
    - Semantic memory: MemoryQuery built from understanding.
    - Episodic memory: EpisodeQuery built from understanding.
    - Context: keyword/embedding scoring over the working buffer
      (context_reasoner), driven by understanding where available.
    """

    def retrieve(
        self,
        user_message: str,
        reasoning: ReasoningResult
    ):

        understanding = reasoning.understanding

        memory   = []
        episodes = []
        context  = []
        history  = []

        # ------------------------------------------
        # SEMANTIC MEMORY
        # ------------------------------------------

        if reasoning.use_memory:

            query = build_memory_query(understanding)

            memory = retrieve_with_query(query)

            # Historical questions also read the changed-fact trail
            # ("what was my favorite food before chicken curry").
            if query.scope == "history":
                history = retrieve_history(query)

        # ------------------------------------------
        # EPISODIC MEMORY
        # Structured query — the episode retriever never
        # sees raw user_message (Issue 6).
        # ------------------------------------------

        if reasoning.use_episodes:

            episode_query = build_episode_query(understanding)

            episodes = retrieve_relevant_episodes(
                episode_query
            )

        # ------------------------------------------
        # CONTEXT
        # ------------------------------------------

        if reasoning.use_context:

            recent  = get_recent_context()

            context = find_relevant_context(
                understanding,
                recent,
            )

        return {
            "understanding": understanding,
            "memory":        memory,
            "episodes":      episodes,
            "context":       context,
            "history":       history,
        }


memory_router = MemoryRouter()
