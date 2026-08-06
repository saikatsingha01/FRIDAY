from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from src.contracts.language_understanding import (
    LanguageUnderstanding,
)


class PlanStatus(Enum):
    """
    Lifecycle state of an execution plan.
    """

    CREATED = "CREATED"
    WAITING_FOR_INPUT = "WAITING_FOR_INPUT"
    READY = "READY"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


@dataclass
class PlannerInput:
    """
    Everything the Planner is allowed to see.

    Built by the Execution Layer from structured outputs only:
    - LanguageUnderstanding (never raw user text directly)
    - ReasoningResult (the systems Reasoning decided are needed)
    - Recent conversation context
    - Retrieved memories / episodes / history

    The Planner never receives anything downstream of Reasoning
    (no tool results, no prior plan state). It creates a plan and
    nothing else.
    """

    understanding: LanguageUnderstanding

    reasoning: Optional[Any] = None

    recent_context: Optional[List[Any]] = None

    memories: Optional[List[Any]] = None

    episodes: Optional[List[Any]] = None

    history: Optional[List[Any]] = None

    # The plan currently in progress (session state, never persisted).
    # When present, the Planner decides whether the new message
    # CONTINUES that goal (update the plan) or is a genuinely new
    # goal (replace it). Never a hardcoded list — the planner is the
    # arbiter, and its decision is surfaced via
    # ExecutionPlan.continues_active_plan.
    active_plan: Optional[Dict[str, Any]] = None


@dataclass
class PlanStep:
    """
    Represents one atomic unit of work.

    Planner creates this.
    ExecutionManager executes this.

    Planner does not care what domain the step belongs to.
    """

    step_id: int

    title: str

    description: str

    action: str

    parameters: Dict[str, Any] = field(
        default_factory=dict
    )

    depends_on: List[int] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    # Runtime execution fields.
    # These are modified by ExecutionManager.

    completed: bool = False

    success: bool = False

    result: Optional[Any] = None

    error: Optional[str] = None


@dataclass
class ExecutionPlan:
    """
    Universal execution blueprint.

    Planner responsibility:
    - Define the goal
    - Define required steps
    - Define dependencies
    - Identify missing information

    ExecutionManager responsibility:
    - Run steps
    - Update status
    - Store results

    Planner never solves the task.
    """

    goal: str

    goal_type: str = "general"

    # True when this plan is a CONTINUATION of the previously active
    # plan (the user corrected, extended, or answered within the same
    # goal), False when it is a fresh plan. The ExecutionManager uses
    # this to keep or replace the session's active plan.
    continues_active_plan: bool = False

    # The planner's own judgment of whether the user's message is a
    # goal-driven request that warrants an execution plan at all.
    # False for on-the-spot trivia (an unrelated question, a bare
    # fact statement) even when the continuity gate routed it to the
    # planner. The caller uses this to distinguish a genuine new goal
    # (execute and replace the active plan) from a mid-plan detour
    # (answer normally, keep the active plan).
    is_goal_request: bool = False

    steps: List[PlanStep] = field(
        default_factory=list
    )

    requires_clarification: bool = False

    missing_information: List[str] = field(
        default_factory=list
    )

    expected_result: Optional[str] = None

    parallel_groups: List[List[int]] = field(
        default_factory=list
    )

    estimated_complexity: str = "medium"

    estimated_duration: Optional[str] = None

    notes: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    status: PlanStatus = PlanStatus.CREATED