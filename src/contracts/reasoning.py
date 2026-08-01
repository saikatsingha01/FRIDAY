from dataclasses import dataclass, field
from typing import List

from src.contracts.language_understanding import (
    LanguageUnderstanding,
)


# ==========================================================
# EXECUTION PLAN
# ==========================================================

@dataclass
class ExecutionPlan:

    use_memory: bool = False

    use_context: bool = False

    use_episodes: bool = False

    use_tools: bool = False

    use_web: bool = False

    use_vision: bool = False

    use_planner: bool = False

    use_reflection: bool = False

    use_llm: bool = True


# ==========================================================
# REASONING CONTRACT
# ==========================================================

@dataclass
class ReasoningResult:

    understanding: LanguageUnderstanding

    plan: ExecutionPlan = field(
        default_factory=ExecutionPlan
    )

    notes: List[str] = field(
        default_factory=list
    )