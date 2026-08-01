from src.core.skill_manager import run_skill


class ToolRouter:
    """
    Routes deterministic tools only.

    This class DOES NOT perform:

    - Greetings
    - Identity responses
    - Memory recall
    - Memory saving
    - Conversation handling
    - Intent detection

    Those belong to the Understanding,
    Reasoning and LLM pipeline.

    The Tool Router is responsible ONLY
    for deterministic tools.
    """

    def route(self, user_message: str):

        if not user_message:
            return None

        command = user_message.strip().lower()

        # ==========================================
        # SHUTDOWN
        # ==========================================

        if command in {

            "exit",
            "quit",
            "shutdown",
            "shut down",
            "turn off",

        }:

            return "shutdown"

        # ==========================================
        # DETERMINISTIC SKILLS
        # ==========================================

        skill_result = run_skill(command)

        if skill_result is not None:

            return skill_result

        # ==========================================
        # NOT A TOOL
        # ==========================================

        return None


tool_router = ToolRouter()


def route_tool(user_message: str):

    return tool_router.route(

        user_message

    )