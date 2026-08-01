from src.core.brain import think


class ConversationManager:
    """
    Central conversation orchestrator.

    Responsibilities:
    - Receive user input
    - Pass it to Brain
    - Maintain conversation flow

    Future responsibilities:
    - Conversation state
    - Planner integration
    - Task execution
    - Reflection
    - Multi-turn workflows
    - Tool orchestration
    """


    def process(self, message):

        result = think(
            message
        )


        if result is None:

            return {

                "message": message,

                "understanding": None,

                "reasoning": None,

                "memory": {},

                "response":
                    "I couldn't process that."

            }


        result.setdefault(

            "message",

            message

        )


        result.setdefault(

            "understanding",

            None

        )


        result.setdefault(

            "reasoning",

            None

        )


        result.setdefault(

            "memory",

            {}

        )


        result.setdefault(

            "response",

            "I'm not sure how to respond."

        )


        return result



conversation_manager = ConversationManager()



def process_conversation(message):

    return conversation_manager.process(

        message

    )