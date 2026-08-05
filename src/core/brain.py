from src.understanding.understanding_orchestrator import analyze
from src.core.reasoning_engine import reasoning_engine
from src.execution.execution_manager import execution_manager
from src.core.tool_router import route_tool
from src.memory.memory_decision import process_memory, memory_decision
from src.core.response_generator import (
    generate_response,
    generate_trivial_response,
)
from src.ai.prompt_builder import build_prompt
from src.ai.llm_interface import llm
from src.ai.model_router import select_model
from src.core.context_manager import maybe_rollover


def _clean_response(text: str) -> str:
    """
    Strips markdown formatting that breaks TTS.
    The LLM sometimes ignores the no-markdown instruction —
    this is a safety net, not the primary fix.
    """

    if not text:
        return text

    import re

    # Remove bold/italic markers
    text = re.sub(r"\*{1,3}(.+?)\*{1,3}", r"\1", text)

    # Remove leading bullet symbols (*, -, •) from lines
    lines = []
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("* ", "- ", "• ", "· ")):
            line = line.replace(
                stripped[:2], "", 1
            )
        lines.append(line)

    text = "\n".join(lines)

    # Collapse multiple blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def think(user_message: str):

    # ============================================
    # 0. CONTEXT — roll an idle session into an
    # episode before reading the working buffer.
    # ============================================

    maybe_rollover()

    # ============================================
    # 1. UNDERSTANDING
    # analyze() returns (understanding, memory_fact).
    # MemoryFact carries only the memory write
    # instruction — never raw user text.
    # ============================================

    understanding, memory_fact = analyze(user_message)

    if understanding is None:
        return {
            "response": "I couldn't understand the request."
        }

    # ============================================
    # 1b. TRIAGE FAST-PATH — zero LLM calls.
    # Trivial social messages ("hello", "bye",
    # "thanks") get a template response. The
    # generative LLM is never invoked.
    # ============================================

    trivial_category = understanding.metadata.get("trivial")

    if trivial_category is not None:

        if trivial_category == "farewell":
            from src.core.context_manager import rollover
            rollover(force=True)

        try:
            response = generate_trivial_response(
                trivial_category,
                user_message,
            )
        except (KeyError, TypeError):
            response = None

        # Fail-open: if no template exists, fall through to the
        # full pipeline instead of returning nothing.
        if response:
            return {
                "understanding": understanding,
                "reasoning": None,
                "execution": None,
                "response": response,
                "trivial": trivial_category,
            }

    # ============================================
    # 2. REASONING
    # ============================================

    reasoning = reasoning_engine.reason(understanding)

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

    tool_result = route_tool(user_message)

    # ============================================
    # 4b. MODEL SELECTION
    # Deterministic lookup — no LLM call.
    # ============================================

    model_config = select_model(understanding)
    response_model = model_config.get("model")

    print("\n========== BRAIN ==========")
    print("Tool Result  :", repr(tool_result))
    print("Use Planning :", reasoning.use_planning)
    print("Model        :", response_model)
    print("===========================\n")

    if tool_result is not None:
        return {
            "understanding": understanding,
            "reasoning":     reasoning,
            "execution":     execution,
            "response":      generate_response(tool_result),
        }

    # ============================================
    # 5. MEMORY DECISION
    # process_memory receives a MemoryFact object.
    # It returns a status string, never dialogue.
    # ============================================

    memory_result = process_memory(memory_fact)

    print("\n========== MEMORY ==========")
    print("Operation :", memory_fact.operation)
    print("Fact      :", memory_fact.canonical_fact)
    print("Uncertain :", memory_fact.uncertain_terms)
    print("Confidence:", memory_fact.confidence)
    print("Result    :", repr(memory_result))
    print("============================\n")

    if memory_result == "stored":

        prompt   = build_prompt(understanding, execution)
        response = llm.generate(prompt, model=response_model)

        if not response:
            response = "Got it, I'll remember that."

        return {
            "understanding": understanding,
            "reasoning":     reasoning,
            "execution":     execution,
            "response":      _clean_response(response),
        }

    # ============================================
    # 5a. UPDATED
    # A stored fact was replaced. Surface the change
    # in the reply (Issue 14) so the user sees FRIDAY
    # is tracking the correction.
    # ============================================

    if memory_result == "updated":

        event = memory_decision.last_event or {}

        old_text = (event.get("old") or {}).get("text")
        new_text = (event.get("record") or {}).get("text")

        change_note = (
            "\n\n==================================================\n"
            "MEMORY UPDATE\n"
            "==================================================\n\n"
            "A stored fact was just replaced by the user.\n"
            f"  Old: {old_text}\n"
            f"  New: {new_text}\n"
            "Briefly acknowledge the change naturally — e.g. "
            "\"I've updated that from [old] to [new].\" — without "
            "adding any other memory details.\n"
        )

        prompt   = build_prompt(understanding, execution) + change_note
        response = llm.generate(prompt, model=response_model)

        if not response:
            response = "I've updated that."

        return {
            "understanding": understanding,
            "reasoning":     reasoning,
            "execution":     execution,
            "response":      _clean_response(response),
            "memory_update": {
                "old": old_text,
                "new": new_text,
            },
        }

    # ============================================
    # 5b. DELETED
    # A stored fact was forgotten. Surface the removal
    # in the reply, symmetric with the UPDATE note.
    # ============================================

    if memory_result == "deleted":

        event = memory_decision.last_event or {}

        deleted = event.get("old") or []
        old_texts = [
            (m or {}).get("text")
            for m in deleted
            if (m or {}).get("text")
        ]

        change_note = (
            "\n\n==================================================\n"
            "MEMORY DELETED\n"
            "==================================================\n\n"
            "The user just asked you to forget one or more stored "
            "facts.\n"
            f"  Removed: {', '.join(old_texts) if old_texts else 'memory'}\n"
            "Briefly acknowledge the removal naturally — e.g. "
            "\"I've forgotten that.\" — without adding any other "
            "memory details.\n"
        )

        prompt   = build_prompt(understanding, execution) + change_note
        response = llm.generate(prompt, model=response_model)

        if not response:
            response = "I've forgotten that."

        return {
            "understanding": understanding,
            "reasoning":     reasoning,
            "execution":     execution,
            "response":      _clean_response(response),
            "memory_update": {
                "deleted": old_texts,
            },
        }

    # ============================================
    # 5c. NOT FOUND
    # The user asked to forget something, but nothing
    # in the store matches the target.
    # ============================================

    if memory_result == "not_found":

        event = memory_decision.last_event or {}

        target_text = (event.get("record") or {}).get("text")

        change_note = (
            "\n\n==================================================\n"
            "MEMORY NOT FOUND\n"
            "==================================================\n\n"
            "The user asked you to forget something, but you have "
            "no stored memory matching the target.\n"
            f"  Target: {target_text or 'unknown'}\n"
            "Briefly and naturally say you couldn't find that in "
            "memory, without inventing facts.\n"
        )

        prompt   = build_prompt(understanding, execution) + change_note
        response = llm.generate(prompt, model=response_model)

        if not response:
            response = "I couldn't find that in my memory."

        return {
            "understanding": understanding,
            "reasoning":     reasoning,
            "execution":     execution,
            "response":      _clean_response(response),
        }

    # ============================================
    # 5d. NEEDS CLARIFICATION
    # A term in the message could not be
    # confidently interpreted (likely a mishearing
    # or typo). Never store it. Ask the user what
    # they meant — universally, no keyword lists.
    # ============================================

    if memory_result == "needs_clarification":

        # If the underlying question is world-knowledge (not personal),
        # answer from general knowledge first, then surface the
        # uncertain term. Bug 7 — a misheard "btag" should not block
        # an answer about B.Tech. "requires_memory" alone is not
        # reliable here (the Understanding LLM sometimes flags memory
        # for "Do you know about the B.Tech course?"); a question
        # that does not refer to the user is world-knowledge even so.
        raw_tokens = set((understanding.raw_text or "").lower().split())
        references_user = bool(raw_tokens & {
            "my", "mine", "me", "myself", "i",
            "i'm", "im", "i've", "ive", "i'd", "id",
        })

        is_world_q = (
            (understanding.semantic.goal or "").lower()
                in {"retrieve_information", "explain", "compare"}
            and (not understanding.memory.requires_memory
                 or not references_user)
            and (understanding.semantic.category or "").lower()
                not in {"preference", "food", "gaming", "hardware",
                        "identity", "emotional", "project"}
        )

        if is_world_q:
            # Fall through to conversation path — world knowledge
            # questions should be answered, not blocked by uncertain
            # terms.
            prompt   = build_prompt(understanding, execution)
            response = llm.generate(prompt, model=response_model)

            if not response:
                response = "I'm not sure how to respond."

            return {
                "understanding": understanding,
                "reasoning":     reasoning,
                "execution":     execution,
                "response":      _clean_response(response),
            }

        response = _ask_for_clarification(
            understanding,
            memory_fact,
            execution,
            response_model,
        )

        return {
            "understanding": understanding,
            "reasoning":     reasoning,
            "execution":     execution,
            "response":      _clean_response(response),
        }

    # ============================================
    # 5e. NEEDS CONFIRMATION
    # The new value conflicts with a stored one and
    # either carries less confidence or looks like a
    # numeric anomaly (70 kg -> 700 kg). Keep the
    # stored value and ask before overwriting.
    # ============================================

    if memory_result == "needs_confirmation":

        event = memory_decision.last_event or {}

        old_text = (event.get("old") or {}).get("text")
        new_text = (event.get("record") or {}).get("text")

        response = _ask_for_confirmation(
            old_text,
            new_text,
            response_model,
        )

        return {
            "understanding": understanding,
            "reasoning":     reasoning,
            "execution":     execution,
            "response":      _clean_response(response),
        }

    # ============================================
    # 6. PLANNING PATH
    # ============================================

    if reasoning.use_planning and execution.planner_result:

        response = _execute_plan(
            execution.planner_result,
            understanding,
            execution,
            response_model,
        )

        return {
            "understanding": understanding,
            "reasoning":     reasoning,
            "execution":     execution,
            "response":      _clean_response(response),
        }

    # ============================================
    # 7. CONVERSATION PATH
    # ============================================

    prompt   = build_prompt(understanding, execution)
    response = llm.generate(prompt, model=response_model)

    if not response:
        response = "I'm not sure how to respond."

    return {
        "understanding": understanding,
        "reasoning":     reasoning,
        "execution":     execution,
        "response":      _clean_response(response),
    }


def _ask_for_clarification(
    understanding,
    memory_fact,
    execution,
    model=None,
):
    """
    Builds a response that asks the user to clarify a
    term FRIDAY could not confidently interpret.

    This is universal — driven by the LLM's judgment of
    uncertain_terms, never by a hardcoded word list.

    Falls back to a safe generic request if the LLM
    returns nothing.
    """

    prompt = build_prompt(understanding, execution)

    prompt += (
        "\n\nA term in the user's message could not be "
        "confidently interpreted, so nothing may be stored "
        "or answered as if understood.\n"
        "Do NOT guess its meaning. Do NOT answer the request.\n"
        "Briefly and naturally ask the user what they meant "
        "by the unconfirmed term, as if confirming you heard "
        "them correctly.\n"
    )

    response = llm.generate(prompt, model=model)

    if not response:
        response = (
            "I'm not sure I caught that correctly. "
            "Could you repeat or spell it for me?"
        )

    return response


def _ask_for_confirmation(old_text, new_text, model=None):
    """
    Builds a response that asks the user to confirm a conflicting
    memory value before it is overwritten (Issue 15).

    Deterministic fallback keeps FRIDAY honest even if the LLM
    returns nothing.
    """

    prompt = (
        "You are FRIDAY, an AI companion.\n\n"
        "A memory conflict needs confirmation.\n"
        f"  Stored value: {old_text}\n"
        f"  User just said: {new_text}\n\n"
        "The two values conflict and the new one could be a mistake "
        "or mishearing. Ask the user, briefly and naturally, which "
        "one is correct. Do not overwrite anything yet.\n\n"
        "Write as if speaking aloud. No markdown. No asterisks.\n\n"
        "FRIDAY response:"
    )

    response = llm.generate(prompt, model=model)

    if not response:
        response = (
            f"I have \"{old_text}\" stored, but it sounds like you "
            f"now said \"{new_text}\". Which one should I keep?"
        )

    return response


def _execute_plan(plan, understanding, execution, model=None):
    """
    Executes an ExecutionPlan and returns the final response.

    Handles clarification requests, then walks steps.
    All steps currently route through the prompt builder.
    Phase 5 adds real tool/web branching here.
    """

    if plan.requires_clarification and plan.missing_information:
        missing = ", ".join(plan.missing_information)
        return (
            f"To help you with this I need a bit more detail. "
            f"Could you tell me: {missing}?"
        )

    for step in plan.steps:

        step.completed = True

        if step.action == "generate_response":
            prompt   = build_prompt(understanding, execution)
            response = llm.generate(prompt, model=model)
            if response:
                step.result  = response
                step.success = True
                return response

        if step.action == "ask_clarification":
            if plan.missing_information:
                missing = ", ".join(plan.missing_information)
                return f"To help you with this I need: {missing}."
            return (
                "Could you give me a bit more detail "
                "about what you need?"
            )

        # retrieve_memory, search_web, use_tool, analyze —
        # real implementations in Phase 5.
        step.completed = True

    prompt   = build_prompt(understanding, execution)
    response = llm.generate(prompt, model=model)
    return response or "I'm not sure how to respond."