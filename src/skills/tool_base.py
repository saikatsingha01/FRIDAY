# ==========================================================
# TOOL BASE
#
# Every tool subclasses BaseTool. A tool:
#
#   - declares its ToolMetadata (name, description, permissions,
#     actions, status, errors) — the single source of truth for
#     what it can do;
#   - is initialized once at registration;
#   - executes a ToolRequest and returns a ToolResult.
#
# Tools never see raw user text and never decide whether they
# should run — the ToolRouter decides that, the ExecutionManager
# executes it, and the permission gate approves it.
# ==========================================================

from typing import Any

from src.contracts.tool import (
    ToolRequest,
    ToolResult,
    ToolMetadata,
)


class BaseTool:
    """
    Interface every tool must implement.
    """

    # Subclasses override with a ToolMetadata instance.
    metadata: ToolMetadata = None

    # ==========================================
    # LIFECYCLE
    # ==========================================

    def initialize(self) -> None:
        """
        Called once at registration. Subclasses set up any state
        or connections needed to execute. May be a no-op.
        """
        pass

    def shutdown(self) -> None:
        """
        Called once at process end (best-effort). Subclasses
        release connections. May be a no-op.
        """
        pass

    # ==========================================
    # EXECUTION
    # ==========================================

    def execute(self, request: ToolRequest) -> ToolResult:
        """
        Execute a single ToolRequest and return a structured
        ToolResult. Must never raise: wrap all failures into a
        ToolResult with status="failure" so the caller can
        aggregate without crashing the Brain.
        """
        raise NotImplementedError(
            f"{type(self).__name__} must implement execute()"
        )

    # ==========================================
    # HELPERS
    # ==========================================

    def ok(self, request: ToolRequest, data: Any = None, **metadata):
        return ToolResult(
            tool_name=request.tool_name,
            action=request.action,
            status="success",
            data=data,
            metadata=metadata,
        )

    def fail(self, request: ToolRequest, error: str = "execution_error",
             **metadata):
        return ToolResult(
            tool_name=request.tool_name,
            action=request.action,
            status="failure",
            error=error,
            metadata=metadata,
        )

    def denied(self, request: ToolRequest, reason: str = "permission_required",
               **metadata):
        return ToolResult(
            tool_name=request.tool_name,
            action=request.action,
            status="permission_denied",
            error=reason,
            metadata=metadata,
        )
