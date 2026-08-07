from src.contracts.execution import ExecutionResult
from src.contracts.planner import (
    PlannerInput,
    PlanStatus,
)
from src.contracts.tool import ToolResult
from src.core.memory_router import memory_router
from src.core.tool_router import (
    route_tool,
    tool_required,
    resolved_tool_capability,
    capability_has_tool,
    has_launch_signal,
)
from src.execution.tool_executor import tool_executor


class ExecutionManager:

    """
    Coordinates every execution subsystem.

    The Brain never directly calls memory,
    tools, web, planner or vision.

    Everything runs through here.

    Each subsystem is a branch activated only
    when Reasoning decided it is needed.

    Does NOT:
    - Understand user intent
    - Create plans
    - Generate responses
    - Execute domain actions directly
    """

    def execute(
        self,
        user_message: str,
        reasoning,
    ) -> ExecutionResult:

        result = ExecutionResult()

        # ==========================================
        # END-SESSION MAPPING
        # The Understanding Layer classifies a
        # natural-language session end ("you can
        # sleep now", "go to sleep", "shut down")
        # as the canonical intent end_session. The
        # ExecutionManager decides the runtime
        # mapping — never the response LLM.
        # ==========================================

        intent = (
            (reasoning.understanding.semantic.intent or "")
            .lower()
            .strip()
        )

        goal = (
            (reasoning.understanding.semantic.goal or "")
            .lower()
            .strip()
        )

        end_session_metadata = (
            reasoning.understanding.metadata or {}
        ).get("end_session")

        result.end_session = (
            end_session_metadata is True
            or intent == "end_session"
            or goal in {"exit", "shutdown", "end_conversation"}
        )

        # ==========================================
        # MEMORY + EPISODES + CONTEXT via router
        # ==========================================

        if reasoning.use_memory:

            memory_bundle = memory_router.retrieve(
                user_message,
                reasoning,
            )

            result.memories = memory_bundle.get("memory", [])
            result.episodes = memory_bundle.get("episodes", [])
            result.context  = memory_bundle.get("context", [])
            result.history  = memory_bundle.get("history", [])

        # ==========================================
        # CONTEXT — always pull recent turns
        # when planning, context is needed, or
        # when the user is clearly continuing a thread.
        # ==========================================

        if not result.context and (
            reasoning.use_context
            or reasoning.use_planning
        ):

            from src.core.context_manager import (
                get_recent_context,
            )

            recent = get_recent_context()

            if recent:
                result.context = list(recent)

        # ==========================================
        # PLANNING
        # Pass everything available (recent context,
        # retrieved memories, past experiences) so the
        # planner can incorporate real constraints and
        # never invent user details.
        # ==========================================

        if reasoning.use_planning:

            from src.core.planner import planner
            from src.core.context_manager import get_active_plan

            active_plan = get_active_plan()

            result.planner_result = planner.plan(
                PlannerInput(
                    understanding=reasoning.understanding,
                    reasoning=reasoning,
                    recent_context=result.context,
                    memories=result.memories,
                    episodes=result.episodes,
                    history=result.history,
                    active_plan=active_plan,
                )
            )

            # With no active plan there is nothing to continue — the
            # planner's continues_active_plan judgment is meaningless
            # (the small model sometimes sets it TRUE anyway). Force it
            # False so a first-turn goal is never treated as a
            # continuation. This only guards the no-active-plan case;
            # once a plan exists the planner is the arbiter.
            if active_plan is None and result.planner_result:
                result.planner_result.continues_active_plan = False

        # ==========================================
        # TOOLS — Phase 5
        # The ToolRouter selects the tools; the
        # ToolExecutor runs them under the permission
        # gate. Structured ToolResults are collected —
        # never free-form text.
        #
        # The gate is tool_required() — Reasoning flags
        # OR the resolved capability alone. The small
        # Understanding model sometimes misses the
        # tools/web booleans for file/web requests, so
        # the capability itself must be enough to enter
        # this path (file-queries-never-fire bug).
        #
        # HONESTY (BUG 5/6/7): when the tool path was
        # entered because a tool capability genuinely
        # resolved — OR because the structured fields prove
        # this is an application launch (has_launch_signal;
        # the small model sometimes drifts the flag AND the
        # capability label on repeat turns) — but the router
        # could not build a single concrete request, an
        # explicit failure ToolResult is synthesized. The
        # prompt then shows an action that did not complete
        # instead of an empty TOOL RESULTS block, so the
        # response model can never hallucinate a silent
        # success ("I opened the file manager"). Pure flag
        # noise (use_tools without any tool capability) is left
        # untouched so chat turns stay chat.
        # ==========================================

        if tool_required(reasoning.understanding, reasoning):
            requests = route_tool(
                reasoning.understanding,
                reasoning,
            )
            results = tool_executor.execute(requests)

            if not results and (
                capability_has_tool(
                    resolved_tool_capability(reasoning.understanding)
                )
                or has_launch_signal(reasoning.understanding)
            ):
                results = [
                    ToolResult(
                        tool_name="tool_router",
                        action="dispatch",
                        status="failure",
                        error="no_tool_selected",
                    )
                ]

            result.tool_results = results

        # ==========================================
        # WEB — Phase 5
        # Web is handled as a tool (web_search).
        # ==========================================

        if reasoning.use_web and not result.tool_results:
            pass

        # ==========================================
        # VISION — Phase 10
        # ==========================================

        if reasoning.use_vision:
            pass

        # ==========================================
        # DEBUG
        # ==========================================

        print("\n========== EXECUTION ==========")
        print("Need Memory   :", reasoning.use_memory)
        print("Need Episodes :", reasoning.use_episodes)
        print("Need Context  :", reasoning.use_context)
        print("Need Tools    :", reasoning.use_tools)
        print("Need Web      :", reasoning.use_web)
        print("Need Vision   :", reasoning.use_vision)
        print("Need Planning :", reasoning.use_planning)
        print()
        print("Retrieved Memories :", len(result.memories))
        print("Retrieved Episodes :", len(result.episodes))
        print("Retrieved Context  :", len(result.context))

        if result.planner_result:
            print(
                "Plan Steps         :",
                len(result.planner_result.steps)
            )
            print(
                "Needs Clarification:",
                result.planner_result.requires_clarification
            )

        print("===============================\n")

        return result

    # ==========================================
    # PLAN EXECUTION
    # The Planner creates structured plans;
    # the ExecutionManager executes them.
    #
    # Steps run in dependency order. Each step
    # is dispatched to the subsystem Reasoning
    # granted for it. Steps whose executor does
    # not exist yet (web/tools — Phase 5) are
    # recorded and skipped, never fatal.
    # ==========================================

    def execute_plan(
        self,
        plan,
        understanding,
        reasoning,
        execution,
        model=None,
    ):

        # A plan that cannot make progress asks before doing anything
        # else. This is a request for the missing input, not a promise
        # to act on half a goal.
        if plan.requires_clarification and plan.missing_information:
            plan.status = PlanStatus.WAITING_FOR_INPUT
            self._record_active_plan(plan, understanding)
            return (
                f"To help you with this I need a bit more detail. "
                f"Could you tell me: "
                f"{', '.join(plan.missing_information)}?"
            )

        plan.status = PlanStatus.RUNNING
        self._record_active_plan(plan, understanding)

        completed = set()
        pending = list(plan.steps)

        # Dependency-ordered walk. A step whose dependencies are not
        # complete yet is deferred to the next pass. Bounded by the
        # number of steps so a cyclic or broken plan can never loop.
        for _ in range(len(plan.steps) + 1):

            if not pending:
                break

            deferred = []

            for step in pending:

                if (
                    step.depends_on
                    and not set(step.depends_on).issubset(completed)
                ):
                    deferred.append(step)
                    continue

                step.completed = True

                outcome = self._dispatch_step(
                    step,
                    plan,
                    understanding,
                    reasoning,
                    execution,
                    model,
                )

                if outcome is not None:
                    # A step produced the turn's final answer.
                    plan.status = PlanStatus.COMPLETED
                    return outcome

                completed.add(step.step_id)

            pending = deferred

        plan.status = PlanStatus.COMPLETED

        return self._final_response(
            plan,
            understanding,
            execution,
            model,
        )

    def _record_active_plan(self, plan, understanding):
        """
        Persists the running plan as the session's active goal so a
        follow-up on the next turn continues it (Phase 3 planning
        continuity). Session state only — never the memory store.
        A continuation plan updates the existing goal; a fresh plan
        replaces it.
        """
        try:
            from src.core.context_manager import set_active_plan
            set_active_plan(
                plan,
                goal_text=(understanding.raw_text or ""),
            )
        except Exception:
            pass

    def _dispatch_step(
        self,
        step,
        plan,
        understanding,
        reasoning,
        execution,
        model=None,
    ):

        action = step.action

        if action == "generate_response":
            response = self._final_response(
                plan,
                understanding,
                execution,
                model,
            )
            if response:
                step.result  = response
                step.success = True
                return response
            return None

        if action == "ask_clarification":
            if plan.missing_information:
                return (
                    f"To help you with this I need: "
                    f"{', '.join(plan.missing_information)}."
                )
            return "Could you give me a bit more detail about what you need?"

        if action == "retrieve_memory":
            self._retrieve_for_plan(
                step,
                understanding,
                reasoning,
                execution,
            )
            return None

        if action == "analyze":
            # Internal reasoning step — produces no user-facing
            # output. It exists so plans can structure their thinking;
            # the final generate_response step carries the answer.
            step.success = True
            step.result  = "analyzed"
            return None

        # search_web / use_tool — their executors arrive in Phase 5.
        # A plan never fails because an executor does not exist yet;
        # the step is recorded and the plan continues to its response
        # step, which answers honestly with what is available.
        step.success = False
        step.error    = f"executor not available yet (Phase 5): {action}"
        step.result   = None
        return None

    def _retrieve_for_plan(
        self,
        step,
        understanding,
        reasoning,
        execution,
    ):

        try:
            bundle = memory_router.retrieve(
                understanding.raw_text,
                reasoning,
            )
        except Exception as exc:
            step.success = False
            step.error   = str(exc)
            return

        known = {
            m.get("text")
            for m in execution.memories
            if isinstance(m, dict)
        }

        for memory in bundle.get("memory", []):
            if (
                isinstance(memory, dict)
                and memory.get("text")
                and memory["text"] not in known
            ):
                execution.memories.append(memory)

        for episode in bundle.get("episodes", []):
            if episode not in execution.episodes:
                execution.episodes.append(episode)

        step.success = True
        step.result  = (
            f"retrieved {len(bundle.get('memory', []))} memory "
            f"entries and {len(bundle.get('episodes', []))} episodes"
        )

    def _final_response(
        self,
        plan,
        understanding,
        execution,
        model=None,
    ):

        from src.ai.prompt_builder import build_prompt
        from src.ai.llm_interface import llm
        import dataclasses

        # Continuation turns already carry everything needed inside the
        # plan and the conversation: the goal, the corrected facts, and
        # the steps. Re-injecting the retrieved memory bundle into the
        # response risks the model anchoring on unrelated stored facts
        # (e.g. asking about "B.Tech" mid-Python-plan). Suppress stored
        # memories for the reply on continuation turns only; fresh-plan
        # and all non-planning responses keep the full bundle.
        if plan.continues_active_plan:
            execution = dataclasses.replace(execution, memories=[])

        prompt = build_prompt(understanding, execution)

        # Planning-only focus instruction. Never touches the memory /
        # conversation path: this method runs only when a plan executed.
        # Keeps the reply anchored to the goal and prevents re-asking
        # for information the plan or conversation already establishes.
        prompt += (
            "\n\nThe user is mid-plan on the goal in the EXECUTION PLAN "
            "above. Keep your reply focused on that goal. Do not ask for "
            "information that the plan or the recent conversation already "
            "establishes, and do not ask about unrelated stored facts."
        )

        response = llm.generate(prompt, model=model)

        if not response:
            return "I'm not sure how to respond."

        return response


execution_manager = ExecutionManager()