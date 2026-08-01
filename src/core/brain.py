from src.understanding.understanding_orchestrator import analyze

from src.core.reasoning_engine import reasoning_engine

from src.execution.execution_manager import execution_manager

from src.core.tool_router import route_tool

from src.memory.memory_decision import process_memory

from src.core.response_generator import generate_response

from src.ai.prompt_builder import build_prompt

from src.ai.llm_interface import llm


def think(user_message: str):

    # ============================================
    # 1. UNDERSTANDING
    # ============================================

    understanding = analyze(user_message)

    if understanding is None:

        return {

            "response": "I couldn't understand the request."

        }

    # ============================================
    # 2. REASONING
    # ============================================

    reasoning = reasoning_engine.reason(

        understanding

    )

    # ============================================
    # 3. EXECUTION
    # ============================================

    execution = execution_manager.execute(

        user_message,

        reasoning,

    )

    # ============================================
    # 4. TOOLS
    # ============================================

    tool_result = route_tool(

        user_message

    )

    print("\n========== BRAIN ==========")
    print("Tool Result :", repr(tool_result))
    print("===========================\n")

    if tool_result is not None:

        return {

            "understanding": understanding,

            "reasoning": reasoning,

            "execution": execution,

            "response": generate_response(

                tool_result

            ),

        }

    # ============================================
    # 5. MEMORY DECISION
    # ============================================

    memory_instruction = {
        "operation": understanding.memory.memory_operation,
        "fact":      understanding.memory.memory_payload,
    }

    memory_result = process_memory(memory_instruction)

    print("\n========== MEMORY ==========")
    print("Operation :", understanding.memory.memory_operation)
    print("Payload   :", understanding.memory.memory_payload)
    print("Result    :", repr(memory_result))
    print("============================\n")

    if memory_result == "stored":

        # Let the LLM generate a natural confirmation.
        # Responses vary: "Got it.", "Noted.", "I'll keep that in mind."
        # MemoryDecision never generates dialogue — that's the LLM's job.

        prompt = build_prompt(understanding, execution)

        response = llm.generate(prompt)

        if not response:
            response = "Got it, I'll remember that."

        return {

            "understanding": understanding,

            "reasoning": reasoning,

            "execution": execution,

            "response": response,

        }

    # ============================================
    # 6. PROMPT
    # ============================================

    prompt = build_prompt(

        understanding,

        execution,

    )

    # ============================================
    # 7. LLM
    # ============================================

    response = llm.generate(

        prompt

    )

    if not response:

        response = "I'm not sure how to respond."

    # ============================================
    # 8. RESULT
    # ============================================

    return {

        "understanding": understanding,

        "reasoning": reasoning,

        "execution": execution,

        "response": response,

    }