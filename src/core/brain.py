from src.understanding.understanding_orchestrator import analyze
from src.core.reasoning_engine import reasoning_engine
from src.execution.execution_manager import execution_manager
from src.memory.memory_decision import process_memory, memory_decision
from src.core.response_generator import (
    generate_trivial_response,
    guard_listing_response,
    guard_path_response,
    guard_web_response,
)
from src.ai.prompt_builder import build_prompt
from src.ai.llm_interface import llm
from src.ai.model_router import route as route_model
from src.core.context_manager import maybe_rollover


def _safe_print(*args, **kwargs):
    """Print that handles Unicode encoding errors on Windows cp1252 console."""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        safe_args = []
        for arg in args:
            if isinstance(arg, str):
                safe_args.append(arg.encode("cp1252", errors="replace").decode("cp1252"))
            else:
                safe_args.append(str(arg).encode("cp1252", errors="replace").decode("cp1252"))
        print(*safe_args, **kwargs)


# Passive knowledge-lookup goals. When the planner decides such a
# message does NOT continue the active plan, it is a mid-plan
# question ("what is the weather in tokyo", "how far is X from Y",
# "tell me a joke") â€” never a plan to execute. Deterministic and
# independent of the flaky Understanding planning flag, so a weather
# question detours even when Understanding routed it to the planner.
DETOUR_GOALS = {
    "retrieve_information",
    "amusement",
}


def _clean_response(text: str) -> str:
    """
    Strips markdown formatting that breaks TTS.
    The LLM sometimes ignores the no-markdown instruction â€”
    this is a safety net, not the primary fix.
    """

    if not text:
        return text

    import re

    # Remove bold/italic markers
    text = re.sub(r"\*{1,3}(.+?)\*{1,3}", r"\1", text)

    # Remove leading bullet symbols (*, -, â€¢) from lines
    lines = []
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("* ", "- ", "â€¢ ", "Â· ")):
            line = line.replace(
                stripped[:2], "", 1
            )
        lines.append(line)

    text = "\n".join(lines)

    # Collapse multiple blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def _final_response(response: str, execution, understanding=None):
    """
    Applies the filesystem answer guard (deterministic) then the
    local-path truth guard, then the web grounding guard, then the
    TTS cleanup, in that order. The listing guard guarantees the
    reply never names a file or folder the tool results did not
    produce; the path guard guarantees a local path is only ever
    spoken when a successful file_manager result on this turn
    produced it (never from a web page or memory); the web guard
    guarantees factual claims from web search are grounded in snippets.
    """
    guarded = guard_listing_response(response, execution.tool_results)
    guarded = guard_path_response(
        guarded,
        execution.tool_results,
        getattr(understanding, "raw_text", None) if understanding else None,
    )
    guarded = guard_web_response(
        guarded,
        execution.tool_results,
        getattr(understanding, "raw_text", None) if understanding else None,
    )
    return _clean_response(guarded)


def think(user_message: str):

    # ============================================
    # 0. CONTEXT â€” roll an idle session into an
    # episode before reading the working buffer.
    # ============================================

    maybe_rollover()

    # ============================================
    # 1. UNDERSTANDING
    # analyze() returns (understanding, memory_fact).
    # MemoryFact carries only the memory write
    # instruction â€” never raw user text.
    # ============================================

    understanding, memory_fact = analyze(user_message)

    if understanding is None:
        return {
            "response": "I couldn't understand the request."
        }

    # ============================================
    # 1b. TRIAGE FAST-PATH â€” zero LLM calls.
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

    # A "detour" is a message the planner judged unrelated to the
    # active plan (not a continuation) AND not something to execute:
    # either its semantic goal is a passive lookup (weather, distance,
    # joke) â€” deterministic, independent of the flaky planning flag â€”
    # or the planner itself rejected it as a goal request. Detours are
    # answered on the normal path with the active plan left intact.
    # A genuine NEW goal â€” flag recognized or not â€” has an actionable
    # goal AND the planner flagged it as a goal request, so it
    # executes as a fresh plan and replaces the active one.
    plan_detour = bool(
        execution.planner_result
        and not execution.planner_result.continues_active_plan
        and (
            (understanding.semantic.goal or "").lower() in DETOUR_GOALS
            or not execution.planner_result.is_goal_request
        )
    )

    # ============================================
    # 4. TOOLS
    # Tool selection and execution happen inside the
    # ExecutionManager (use_tools branch): Reasoning
    # decided need, the ToolRouter selected, the
    # ToolExecutor ran them under the permission gate.
    # The structured ToolResults ride on
    # execution.tool_results into the prompt builder â€”
    # the Brain never touches raw tool text.
    # ============================================

    # ============================================
    # 4b. MODEL SELECTION
    # The Brain requests a routing decision from the
    # Model Router and passes the decision's model
    # into the LLM Interface. The Brain never knows
    # model names or routing rules.
    # ============================================

    routing_decision = route_model(
        understanding.semantic.capability
    )
    response_model = routing_decision.model

    _safe_print("\n========== BRAIN ==========")
    _safe_print("Tool Results  :", len(execution.tool_results))
    for tr in execution.tool_results:
        _safe_print("  -", tr.tool_name, "->", tr.status)
    _safe_print("Use Planning :", reasoning.use_planning)
    _safe_print("Capability   :", routing_decision.category)
    _safe_print("Model        :", response_model, f"({routing_decision.role})")
    _safe_print("===========================\n")

    # ============================================
    # 5. MEMORY DECISION
    # process_memory receives a MemoryFact object.
    # It returns a status string, never dialogue.
    # ============================================

    memory_result = process_memory(memory_fact)

    _safe_print("\n========== MEMORY ==========")
    _safe_print("Operation :", memory_fact.operation)
    _safe_print("Fact      :", memory_fact.canonical_fact)
    _safe_print("Uncertain :", memory_fact.uncertain_terms)
    _safe_print("Confidence:", memory_fact.confidence)
    _safe_print("Result    :", repr(memory_result))
    _safe_print("============================\n")

    if memory_result == "stored":

        # A goal-accomplishment request ("build a game", "learn
        # python") is often ALSO extracted as a memory write. The
        # write has already happened â€” the side effect is kept. But
        # when Reasoning flagged planning, the user asked for a
        # plan, so the plan is the answer. This only widens the
        # stored path; the memory write is a quiet side effect.
        if (
            reasoning.use_planning
            and execution.planner_result
            and not plan_detour
        ):

            response = execution_manager.execute_plan(
                execution.planner_result,
                understanding,
                reasoning,
                execution,
                model=response_model,
            )

            return {
                "understanding": understanding,
                "reasoning":     reasoning,
                "execution":     execution,
                "response":      _final_response(response, execution, understanding),
            }

        # Mid-plan detour: answer as a plain stored-fact ack. The
        # planner output was judged unrelated to the active plan, so
        # it must not shape this response â€” and the active plan stays.
        if plan_detour:
            execution.planner_result = None

        prompt   = build_prompt(understanding, execution)
        response = llm.generate(prompt, model=response_model)

        if not response:
            response = "Got it, I'll remember that."

        return {
            "understanding": understanding,
            "reasoning":     reasoning,
            "execution":     execution,
            "response":      _final_response(response, execution, understanding),
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
            "Briefly acknowledge the change naturally â€” e.g. "
            "\"I've updated that from [old] to [new].\" â€” without "
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
            "response":      _final_response(response, execution, understanding),
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
            "Briefly acknowledge the removal naturally â€” e.g. "
            "\"I've forgotten that.\" â€” without adding any other "
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
            "response":      _final_response(response, execution, understanding),
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
            "response":      _final_response(response, execution, understanding),
        }

    # ============================================
    # 5d. NEEDS CLARIFICATION
    # A term in the message could not be
    # confidently interpreted (likely a mishearing
    # or typo). Never store it. Ask the user what
    # they meant â€” universally, no keyword lists.
    # ============================================

    if memory_result == "needs_clarification":

        # If the underlying question is world-knowledge (not personal),
        # answer from general knowledge first, then surface the
        # uncertain term. Bug 7 â€” a misheard "btag" should not block
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
            # Fall through to conversation path â€” world knowledge
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
                "response":      _final_response(response, execution, understanding),
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
            "response":      _final_response(response, execution, understanding),
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
            "response":      _final_response(response, execution, understanding),
        }

    # ============================================
    # 6. PLANNING PATH
    # ============================================

    if (
        reasoning.use_planning
        and execution.planner_result
        and not plan_detour
    ):

        response = execution_manager.execute_plan(
            execution.planner_result,
            understanding,
            reasoning,
            execution,
            model=response_model,
        )

        return {
            "understanding": understanding,
            "reasoning":     reasoning,
            "execution":     execution,
            "response":      _final_response(response, execution, understanding),
        }

    # ============================================
    # 7. CONVERSATION PATH
    # ============================================

    # A detour reaches here with planner output that is unrelated to
    # the active plan. Drop it so the normal answer is not shaped by
    # a plan the user never asked for; the active plan is untouched.
    if plan_detour:
        execution.planner_result = None

    prompt   = build_prompt(understanding, execution)
    response = llm.generate(prompt, model=response_model)

    if not response:
        response = "I'm not sure how to respond."

    return {
        "understanding": understanding,
        "reasoning":     reasoning,
        "execution":     execution,
        "response":      _final_response(response, execution, understanding),
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

    This is universal â€” driven by the LLM's judgment of
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
