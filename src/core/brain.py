from src.core.response_generator import generate_response
from src.core.command_handler import handle_command
from src.core.context_manager import get_recent_context
from src.core.context_reasoner import find_relevant_context
from src.memory.memory_manager import recall_from_question



def think(message):

    print("BRAIN: Processing input...")


    # Get recent conversation
    context = get_recent_context()


    # Find related previous conversation
    relevant_context = find_relevant_context(
        message,
        context
    )


    print(
        "BRAIN CONTEXT:",
        relevant_context
    )



    # --------------------------------
    # MEMORY REASONING
    # --------------------------------

    memory_answer = recall_from_question(
        message
    )


    if memory_answer:

        print(
            "BRAIN: Memory answer found"
        )


        response = generate_response(
            memory_answer
        )


        return {
            "message": message,
            "context": relevant_context,
            "response": response
        }



    # --------------------------------
    # CONTEXT REASONING
    # --------------------------------

    if relevant_context:

        print(
            "BRAIN: Using conversation context"
        )


        context_text = ""


        for item in relevant_context:

            context_text += (
                item["user"]
                + " "
            )



        # Temporary reasoning
        # Will be replaced by LLM later

        if "game" in message:

            memory_answer = recall_from_question(
                "favorite game"
            )


            if memory_answer:

                response = generate_response(
                    memory_answer
                )


                return {
                    "message": message,
                    "context": relevant_context,
                    "response": response
                }



    # --------------------------------
    # NORMAL COMMAND ROUTE
    # --------------------------------

    response = handle_command(
        message
    )


    response = generate_response(
        response
    )


    return {
        "message": message,
        "context": relevant_context,
        "response": response
    }