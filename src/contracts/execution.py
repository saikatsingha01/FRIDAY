from dataclasses import dataclass, field
from typing import Any, List


# ==========================================================
# EXECUTION RESULT
# ==========================================================

@dataclass
class ExecutionResult:
    """
    Output of the Execution Layer.

    Every executor contributes to this object.

    Example:

    Memory Executor
        -> memories

    Context Executor
        -> context

    Tool Executor
        -> tool_results

    Web Executor
        -> web_results

    Planner Executor
        -> planner_result
    """

    # Memory

    memories: List[Any] = field(
        default_factory=list
    )

    episodes: List[Any] = field(
        default_factory=list
    )

    context: List[Any] = field(
        default_factory=list
    )

    # Executors

    tool_results: List[Any] = field(
        default_factory=list
    )

    web_results: List[Any] = field(
        default_factory=list
    )

    planner_result: Any = None

    vision_result: Any = None

    # Metadata

    execution_time: float = 0.0

    success: bool = True