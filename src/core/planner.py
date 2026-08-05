import json
import re

from src.contracts.language_understanding import (
    LanguageUnderstanding,
)

from src.contracts.planner import (
    ExecutionPlan,
    PlanStep,
    PlanStatus,
)

from src.ai.llm_interface import llm

from src.ai.prompt_builder import (
    _format_episodes,
    _format_memories_grouped,
)


class Planner:

    """
    Universal planning engine.

    Converts understood goals into structured ExecutionPlans.

    Responsibilities:
    - Create structured plans from user goals
    - Identify what information is genuinely missing
    - Define step dependencies
    - Describe expected outcomes

    Does NOT:
    - Execute tasks
    - Call tools
    - Retrieve memory
    - Generate the final response
    - Invent information about the user
    - Contain domain-specific workflows
    """

    VALID_ACTIONS = {
        "retrieve_memory",
        "search_web",
        "use_tool",
        "generate_response",
        "ask_clarification",
        "analyze",
    }

    DEFAULT_ACTION = "generate_response"

    def _build_prompt(
        self,
        understanding: LanguageUnderstanding,
        recent_context: list = None,
        memories: list = None,
        episodes: list = None,
    ) -> str:

        # Inject recent conversation so planner
        # understands corrections, follow-ups, and
        # ambiguous messages in full context.
        context_block = ""
        if recent_context:
            lines = []
            for item in recent_context[-4:]:
                if isinstance(item, dict):
                    u = item.get("user", "")
                    f = item.get("friday", "")
                    if u:
                        lines.append(f"User: {u}")
                    if f:
                        f_short = f[:200] + "..." if len(f) > 200 else f
                        lines.append(f"FRIDAY: {f_short}")
            if lines:
                context_block = (
                    "Recent conversation (for context):\n"
                    + "\n".join(lines)
                    + "\n\n"
                )

        # Known user memories — the planner must not invent
        # user-specific details that already exist here.
        memory_block = ""
        if memories:
            text = _format_memories_grouped(memories)
            if text and text != "None":
                memory_block = (
                    "Known user memories:\n"
                    + text
                    + "\n\n"
                )

        episodes_block = ""
        if episodes:
            text = _format_episodes(episodes)
            if text and text != "None":
                episodes_block = (
                    "Past experiences:\n"
                    + text
                    + "\n\n"
                )

        # Entities, time reference and urgency from Understanding.
        entity_lines = []
        for entity in understanding.semantic.entities:
            if hasattr(entity, "text"):
                entity_lines.append(
                    f"- {entity.text} ({entity.label})"
                )
            elif isinstance(entity, dict):
                entity_lines.append(
                    f"- {entity.get('text')} "
                    f"({entity.get('label')})"
                )
        entities_text = (
            "\n".join(entity_lines) if entity_lines else "None"
        )

        time_ref = understanding.semantic.time_reference
        if isinstance(time_ref, dict):
            time_text = (
                f"{time_ref.get('type')}: {time_ref.get('value')}"
            )
        elif time_ref is not None and getattr(time_ref, "type", None):
            time_text = f"{time_ref.type}: {time_ref.value}"
        else:
            time_text = "None"

        urgency = understanding.emotion.urgency or "unknown"

        return (
            "You are FRIDAY's Universal Planning Engine.\n\n"

            "Your only job is to create an execution plan.\n"
            "Do NOT solve the user's request.\n"
            "Do NOT generate the actual answer.\n"
            "Do NOT invent information about the user.\n\n"

            "Return ONLY valid JSON. No markdown. "
            "No explanation. No text before or after.\n\n"

            "Required JSON structure:\n"
            "{\n"
            '    "goal": "concise description of what the user wants",\n'
            '    "goal_type": "research / creative / technical / planning / operational / conversational",\n'
            '    "requires_clarification": false,\n'
            '    "missing_information": [],\n'
            '    "expected_result": "what a successful outcome looks like",\n'
            '    "estimated_complexity": "low / medium / high",\n'
            '    "estimated_duration": "e.g. 2 minutes or null",\n'
            '    "steps": [\n'
            "        {\n"
            '            "step_id": 1,\n'
            '            "title": "short step title",\n'
            '            "description": "what this step does and why",\n'
            '            "action": "generate_response",\n'
            '            "parameters": {},\n'
            '            "depends_on": []\n'
            "        }\n"
            "    ],\n"
            '    "parallel_groups": []\n'
            "}\n\n"

            "Valid actions (use ONLY these):\n"
            "  retrieve_memory    — look up stored facts about the user\n"
            "  search_web         — find real-time external information\n"
            "  use_tool           — invoke a specific tool\n"
            "  generate_response  — produce the final answer\n"
            "  ask_clarification  — ONLY when the goal is genuinely unclear\n"
            "  analyze            — internal reasoning step\n\n"

            "goal_type classification rules:\n"
            "  - \"research\" — user wants to learn, understand, or study "
            "something.\n"
            "    Key signals: \"learn\", \"understand\", \"study\", "
            "\"how do I\", \"teach me\", \"explain\", \"what is\", "
            "\"introduce me to\".\n"
            "    These produce LEARNING PLANS, not implementation plans.\n"
            "  - \"planning\" — user wants a schedule, outline, or roadmap.\n"
            "    Key signals: \"make me a schedule\", \"plan my\", "
            "\"organize\", \"outline\".\n"
            "  - \"technical\" — user wants something built or implemented.\n"
            "    Key signals: \"build\", \"create\", \"code\", "
            "\"implement\", \"write\".\n\n"

            "IMPORTANT:\n"
            "  \"I want to learn Python game dev\" → goal_type: \"research\"\n"
            "  \"Make me a Python game\" → goal_type: \"technical\"\n"
            "  \"Plan my study for Python\" → goal_type: \"planning\"\n\n"

            "Rules:\n"
            "  1. Use the fewest steps that accomplish the goal.\n"
            "  2. Always end with generate_response unless clarification is truly needed.\n"
            "  3. Only set requires_clarification to true when you cannot make any progress.\n"
            "     If the user gave enough context to attempt the task, set it to false.\n"
            "  4. missing_information must list ONLY fields the user genuinely did not provide.\n"
            "     Do not list things you can infer from the request.\n"
            "  5. Never invent user-specific details.\n"
            "  6. Never use action values outside the valid list.\n"
            "  7. Return ONLY valid JSON.\n"
            "  8. Use every constraint the user provided (time available, "
            "deadlines, specific topics, breaks, resources) directly in the "
            "steps. Do not invent constraints the user did not give.\n\n"

            + memory_block
            + episodes_block
            + context_block

            + "User goal:\n"
            + understanding.raw_text + "\n\n"

            "Context:\n"
            f"Intent: {understanding.semantic.intent}\n"
            f"Category: {understanding.semantic.category}\n"
            f"Goal type: {understanding.semantic.goal}\n"
            f"Entities:\n{entities_text}\n"
            f"Time reference: {time_text}\n"
            f"Urgency: {urgency}\n"
        )

    def plan(
        self,
        understanding: LanguageUnderstanding,
        recent_context: list = None,
        memories: list = None,
        episodes: list = None,
    ) -> ExecutionPlan:

        print("\n========== PLANNER ==========")
        print("Goal     :", understanding.raw_text)
        print("Category :", understanding.semantic.category)

        response = llm.generate(
            self._build_prompt(
                understanding,
                recent_context,
                memories,
                episodes,
            ),
            num_predict=4096,
            format_json=True,
        )

        if not response:
            print("Planner: LLM returned nothing, fallback.")
            print("=============================\n")
            return self._fallback(understanding.raw_text)

        data = self._parse(response)

        if not isinstance(data, dict):
            print("Planner: Parse failed, fallback.")
            print("=============================\n")
            return self._fallback(understanding.raw_text)

        # Issue 8: strict schema validation. Invalid structure falls
        # back to a single generate_response step.
        if not self._validate(data):
            print("Planner: Schema validation failed, fallback.")
            print("=============================\n")
            return self._fallback(understanding.raw_text)

        plan = self._build(data, understanding)

        print("Steps    :", len(plan.steps))
        print("Needs clarification:", plan.requires_clarification)
        if plan.requires_clarification:
            print("Missing  :", plan.missing_information)
        print("Expected :", plan.expected_result)
        print("=============================\n")

        return plan

    def _parse(self, response: str):
        """
        Robust JSON extraction from an LLM response.

        Handles the failure modes a small model actually produces:
        markdown code fences, prose wrapped around the JSON, smart
        quotes, trailing commas, unquoted keys, and single-quoted
        strings. Returns a dict on success, None on total failure.
        """

        if not response:
            return None

        text = self._strip_markdown(response.strip())

        candidates = []

        extracted = self._extract_json_object(text)

        if extracted is not None:
            candidates.append(extracted)
        else:
            candidates.append(text)

        for candidate in candidates:
            parsed = self._try_repairs(candidate)
            if parsed is not None:
                return parsed

        print("Planner: could not recover JSON.")
        print("Raw response:", response[:300])
        return None

    def _strip_markdown(self, text: str) -> str:

        if text.startswith("```"):

            lines = text.splitlines()

            if lines:
                lines = lines[1:]

            if lines and lines[-1].strip().startswith("```"):
                lines = lines[:-1]

            text = "\n".join(lines).strip()

        return text

    def _extract_json_object(self, text: str):
        """
        Finds the first top-level balanced {...} object,
        ignoring braces inside string literals.
        """

        start = text.find("{")

        if start == -1:
            return None

        depth = 0
        in_string = False
        escape = False

        for i in range(start, len(text)):

            char = text[i]

            if in_string:

                if escape:
                    escape = False
                elif char == "\\":
                    escape = True
                elif char == '"':
                    in_string = False
                continue

            if char == '"':
                in_string = True
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    return text[start:i + 1]

        return None

    def _try_repairs(self, candidate: str):
        """
        Tries progressively repaired variants until json.loads
        succeeds and returns a dict.
        """

        # 1. Smart quotes -> straight quotes.
        repaired = candidate.replace("\u201c", '"')
        repaired = repaired.replace("\u201d", '"')
        repaired = repaired.replace("\u2018", "'")
        repaired = repaired.replace("\u2019", "'")

        # 2. Trailing commas.
        repaired = re.sub(r",\s*}", "}", repaired)
        repaired = re.sub(r",\s*\]", "]", repaired)

        # 3. Unquoted keys following { or ,.
        repaired = re.sub(
            r"([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)(\s*:)",
            r'\1"\2"\3',
            repaired,
        )

        # 4. Single-quoted strings -> double-quoted strings,
        #    only when the payload uses no double quotes at all.
        single_quote_variant = None
        if '"' not in repaired:
            single_quote_variant = re.sub(
                r"'([^']*)'",
                r'"\1"',
                repaired,
            )

        for variant in [
            repaired,
            single_quote_variant,
        ]:

            if variant is None:
                continue

            try:
                parsed = json.loads(variant)
            except Exception:
                continue

            if isinstance(parsed, dict):
                return parsed

        return None

    def _validate(self, data: dict) -> bool:
        """
        Issue 8: strict structural validation of the parsed plan.

        Returns False (triggering a safe single-step fallback) when
        the plan cannot be trusted:
        - goal missing or not a string
        - steps missing, not a list, or empty
        - any step not a dict, or using an action outside VALID_ACTIONS
        - requires_clarification present but not a boolean

        Type repairs still go through _build; this is the gate.
        """

        if not isinstance(data, dict):
            return False

        goal = data.get("goal")
        if not isinstance(goal, str) or not goal.strip():
            return False

        steps = data.get("steps")
        if not isinstance(steps, list) or not steps:
            return False

        for step in steps:
            if not isinstance(step, dict):
                return False
            action = step.get("action", self.DEFAULT_ACTION)
            if action not in self.VALID_ACTIONS:
                return False

        if "requires_clarification" in data:
            if not isinstance(data["requires_clarification"], bool):
                return False

        if "missing_information" in data:
            if not isinstance(data["missing_information"], list):
                return False

        return True

    def _repair(self, data: dict, understanding: LanguageUnderstanding):
        """
        Issue 9: deterministic no-domain-expansion repairs.

        - Rule 2: unless clarification is genuinely needed, the plan
          must end with a generate_response step. Append one if the
          LLM forgot.
        - Rule 4: missing_information items that the user already
          provided (present as an entity or in the raw text) are not
          missing — drop them.
        - A clarification-only plan whose missing items were all
          provided collapses back to a normal plan.
        - ask_clarification steps without a matching missing item are
          dropped (clarification is never invented).
        """

        missing = list(data.get("missing_information", []))

        def _provided(item: str) -> bool:
            if not isinstance(item, str):
                return True
            tokens = {
                t.lower() for t in re.findall(r"[a-zA-Z0-9]+", item)
            }
            entity_texts = []
            for entity in understanding.semantic.entities:
                if isinstance(entity, dict):
                    entity_texts.append(entity.get("text", ""))
                elif hasattr(entity, "text"):
                    entity_texts.append(entity.text)
            haystack = (
                " ".join(entity_texts) + " "
                + understanding.raw_text
            ).lower()
            return bool(tokens) and all(
                t in haystack for t in tokens
            )

        kept = [item for item in missing if not _provided(item)]

        if kept != missing:
            data["missing_information"] = kept

        if kept and not data.get("requires_clarification", False):
            data["requires_clarification"] = True

        if not kept:
            data["requires_clarification"] = False

        steps = data.get("steps", [])

        if not data.get("requires_clarification", False):
            steps = [
                step for step in steps
                if step.get("action") != "ask_clarification"
            ]
            last = steps[-1] if steps else {}
            if last.get("action") != "generate_response":
                steps.append({
                    "step_id": len(steps) + 1,
                    "title": "Generate response",
                    "description": "Produce the final answer.",
                    "action": "generate_response",
                    "parameters": {},
                    "depends_on": [],
                })
        else:
            steps = [
                step for step in steps
                if not (
                    step.get("action") == "ask_clarification"
                    and not data.get("missing_information")
                )
            ]

        data["steps"] = steps

        return data

    def _build(self, data: dict, understanding: LanguageUnderstanding) -> ExecutionPlan:

        data = self._repair(data, understanding)

        steps = []

        for item in data.get("steps", []):

            action = item.get("action", self.DEFAULT_ACTION)

            if action not in self.VALID_ACTIONS:
                print(
                    f"Planner: unknown action '{action}', "
                    f"replacing with '{self.DEFAULT_ACTION}'"
                )
                action = self.DEFAULT_ACTION

            steps.append(PlanStep(
                step_id=item.get("step_id", len(steps) + 1),
                title=item.get("title", "Step"),
                description=item.get("description", ""),
                action=action,
                parameters=item.get("parameters", {}),
                depends_on=item.get("depends_on", []),
                metadata=item.get("metadata", {}),
            ))

        if not steps:
            steps = [PlanStep(
                step_id=1,
                title="Generate response",
                description="Produce the final answer.",
                action="generate_response",
                depends_on=[],
                metadata={},
            )]

        return ExecutionPlan(
            goal=data.get("goal", ""),
            goal_type=data.get("goal_type", "general"),
            steps=steps,
            requires_clarification=data.get(
                "requires_clarification", False
            ),
            missing_information=data.get(
                "missing_information", []
            ),
            expected_result=data.get("expected_result", ""),
            parallel_groups=data.get("parallel_groups", []),
            estimated_complexity=data.get(
                "estimated_complexity", "medium"
            ),
            estimated_duration=data.get(
                "estimated_duration", None
            ),
        )

    def _fallback(self, goal: str) -> ExecutionPlan:

        return ExecutionPlan(
            goal=goal,
            goal_type="unknown",
            steps=[PlanStep(
                step_id=1,
                title="Generate response",
                description="Produce a direct response.",
                action="generate_response",
                depends_on=[],
                metadata={},
            )],
            requires_clarification=False,
            expected_result="A helpful direct response.",
        )


planner = Planner()