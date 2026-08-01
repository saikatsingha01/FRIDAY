from src.memory.memory_manager import auto_remember


class MemoryDecision:

    """
    Receives a structured memory instruction dict.

    Keys:
        operation  — "store" | "update" | "query" | "forget" | None
        fact       — clean canonical fact string, or None

    This class NEVER parses natural language.
    It ONLY decides whether a memory operation should happen.

    Returns a status string, never English dialogue.
    The LLM in brain.py generates the natural response.
    """

    def process(self, memory_data: dict):

        if not memory_data:
            return None

        operation = memory_data.get("operation")
        fact = memory_data.get("fact")

        if not operation:
            return None

        if not fact:
            return None

        # ----------------------------------------
        # STORE / UPDATE
        # ----------------------------------------

        if operation in ("store", "update"):

            remembered = auto_remember(fact)

            if remembered:
                return "stored"

            return None

        # ----------------------------------------
        # FORGET — future phase
        # ----------------------------------------

        # if operation == "forget":
        #     handled in Phase 5 (Tool Intelligence)

        return None


memory_decision = MemoryDecision()


def process_memory(memory_data: dict):

    return memory_decision.process(memory_data)