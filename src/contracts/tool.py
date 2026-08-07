# ==========================================================
# TOOL CONTRACTS
#
# Phase 5 — Tool Intelligence.
#
# The ToolRouter produces ToolRequest objects; the
# ExecutionManager executes them; every tool returns a
# ToolResult. Raw user text never flows into any tool —
# the ToolRouter reads only structured Understanding and
# Reasoning fields, and parameters carry structured values.
# ==========================================================

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ToolRequest:
    """
    A structured request to execute one tool.

    Produced deterministically by the ToolRouter from
    Understanding + Reasoning — never from raw message text.
    """

    # Registered tool name (registry is the single source of truth).
    tool_name: str

    # A named operation the tool declares in its metadata
    # (e.g. "read", "write", "run", "launch", "search").
    action: str

    # Structured parameters for the action. Never raw prose —
    # only fields the ToolRouter extracted from understanding
    # (entities, goal, intent, capability, ...).
    parameters: Dict[str, Any] = field(
        default_factory=dict
    )

    # Reason this request exists (structured, human-readable for
    # logs/Reflection): the capability and goal that drove it.
    reason: Optional[str] = None

    # Permission class the tool requires (see ToolPermission).
    permission: Optional[str] = None


@dataclass
class ToolResult:
    """
    Structured outcome of a tool execution.

    Never free-form English dialogue: the response LLM explains
    results to the user in natural language. status is a closed
    enum value; data/error/metadata are structured.
    """

    tool_name: str

    action: str

    # One of: success | failure | permission_denied | not_found
    status: str = "success"

    # Structured payload for a successful execution.
    # Tools decide its shape (documented in their metadata).
    data: Any = None

    # Structured error information (code + message) on failure.
    # Not a user-facing sentence.
    error: Optional[str] = None

    # Diagnostic metadata: duration, request reason, warnings, ...
    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def is_ok(self) -> bool:
        return self.status == "success"

    def is_denied(self) -> bool:
        return self.status == "permission_denied"


# ==========================================================
# PERMISSIONS
#
# A closed vocabulary of permission classes. Tools declare the
# class they need in their metadata; the permission gate in the
# tool execution path enforces it (never the Brain, never the
# ToolRouter). Defaults lean safe: anything not explicitly
# granted is denied.
# ==========================================================

class ToolPermission:

    SAFE     = "safe"       # read-only / network read, default allowed
    FILE_WRITE = "file_write"  # writing files
    FILE_DELETE = "file_delete"  # deleting files or directories
    TERMINAL = "terminal"   # arbitrary shell execution
    APP_LAUNCH = "app_launch"   # launching applications / changing system state

    # Maps a permission class to whether it is allowed by default.
    DEFAULT_ALLOWED = {
        SAFE:       True,
        FILE_WRITE: False,
        FILE_DELETE: False,
        TERMINAL:   False,
        APP_LAUNCH: False,
    }


# ==========================================================
# TOOL METADATA
#
# Every tool declares this in its metadata dict so the router,
# permission gate, and Reflection can all read it without
# hardcoding anything about a specific tool.
# ==========================================================

@dataclass
class ToolMetadata:
    """
    Declarative description of a registered tool.

    The ToolRouter uses capability/goal mappings to decide which
    tools may apply; the permission gate uses the permission class;
    Reflection (Phase 6) uses the log fields.
    """

    name: str

    description: str

    # Capabilities this tool can serve (subset of
    # CapabilityCategory values) — structured routing input.
    capabilities: List[str] = field(default_factory=list)

    # Goals this tool can serve (subset of Understanding goal
    # strings) — structured routing input.
    goals: List[str] = field(default_factory=list)

    # Permission class required to execute any action of this tool.
    permission: str = ToolPermission.SAFE

    # Supported actions -> their input/output descriptions.
    actions: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # Tool lifecycle/health status.
    status: str = "ready"

    # Structured error vocabulary the tool may return in
    # ToolResult.error[code].
    errors: List[str] = field(default_factory=list)

    # Whether this tool needs an external capability to function
    # (e.g. network). When False and the environment is offline,
    # the executor can short-circuit without crashing.
    needs_network: bool = False
