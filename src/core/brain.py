from src.core.response_generator import generate_response
from src.core.command_handler import handle_command

from src.core.context_manager import get_recent_context
from src.core.context_reasoner import find_relevant_context

from src.memory.memory_retriever import retrieve_relevant_memories

from src.memory.episode_retriever import retrieve_relevant_episodes

from src.ai.prompt_builder import build_prompt
from src.ai.llm_interface import llm



def think(message):

    print("BRAIN: Processing input...")


    # =================================================
    # SHORT TERM CONTEXT
    # =================================================

    context = get_recent_context()


    relevant_context = find_relevant_context(
        message,
        context
    )


    print(
        "BRAIN CONTEXT:",
        relevant_context
    )


    # =================================================
    # LONG TERM FACT MEMORY
    # =================================================

    relevant_memories = retrieve_relevant_memories(
        message
    )


    print(
        "BRAIN MEMORIES:",
        relevant_memories
    )



    # =================================================
    # EPISODE MEMORY
    # =================================================

    relevant_episodes = retrieve_relevant_episodes(
        message
    )


    print(
        "BRAIN EPISODES:",
        relevant_episodes
    )



    # =================================================
    # COMMAND ROUTE
    # =================================================

    command_response = handle_command(
        message
    )


    if command_response != "I don't understand that yet.":


        response = generate_response(
            command_response
        )


        return {

            "message": message,

            "context": relevant_context,

            "memories": relevant_memories,

            "episodes": relevant_episodes,

            "response": response

        }




    # =================================================
    # LLM REASONING
    # =================================================


    prompt = build_prompt(

        message=message,

        memories=relevant_memories,

        context=relevant_context,

        episodes=relevant_episodes

    )


    print("\n========== FINAL PROMPT ==========")

    print(prompt)

    print("==================================\n")



    response = llm.generate(
        prompt
    )



    if response:


        print(
            "BRAIN: LLM answered"
        )


        return {

            "message": message,

            "context": relevant_context,

            "memories": relevant_memories,

            "episodes": relevant_episodes,

            "response": response

        }



    return {

        "message": message,

        "context": relevant_context,

        "memories": relevant_memories,

        "episodes": relevant_episodes,

        "response": "I don't understand that yet."

    }