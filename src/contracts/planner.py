from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


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