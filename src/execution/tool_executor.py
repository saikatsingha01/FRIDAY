# ==========================================================
# TOOL EXECUTOR
#
# Phase 5 — executes a list of ToolRequests through the
# registered tools, enforcing the permission gate, recording
# duration/log events, and aggregating structured ToolResults.
#
# Never crashes the Brain: every failure is captured into a
# ToolResult and aggregated. It reasons about nothing, decides
# nothing — it only executes what the ToolRouter selected.
# ==========================================================

import time

from src.contracts.tool import ToolRequest, ToolResult
from src.skills import skill_registry
from src.skills.permissions import permission_gate
from src.utils.tool_logger import log_tool_event


class ToolExecutor:

    def execute(self, requests) -> list:
        """
        Execute all given ToolRequests (a list — possibly empty)
        and return a list of structured ToolResults.

        Permission-gating happens HERE, in the tool execution
        path — never in the Brain or the ToolRouter.
        """
        if not requests:
            return []

        results = []

        for request in requests:

            if not isinstance(request, ToolRequest):
                results.append(self._malformed_result(request))
                continue

            results.append(self._execute_one(request))

        return results

    # ==========================================
    # INTERNAL
    # ==========================================

    def _execute_one(self, request: ToolRequest) -> ToolResult:

        started = time.time()

        tool = skill_registry.get_tool(request.tool_name)

        if tool is None:
            return self._record(
                ToolResult(
                    tool_name=request.tool_name,
                    action=request.action,
                    status="failure",
                    error=f"unknown_tool: {request.tool_name}",
                    metadata={"duration_ms": _elapsed(started)},
                ),
                request,
                started,
                outcome="failure",
            )

        permission = request.permission

        if permission is None:
            action_schema = (
                tool.metadata.actions.get(request.action) or {}
            )
            permission = action_schema.get("permission")

        if permission is None:
            permission = tool.metadata.permission

        verdict = permission_gate.check(permission)

        if verdict == "denied":
            return self._record(
                ToolResult(
                    tool_name=request.tool_name,
                    action=request.action,
                    status="permission_denied",
                    error="permission_required",
                    metadata={"permission": permission},
                ),
                request,
                started,
                outcome="permission_denied",
                permission=permission,
            )

        try:
            result = tool.execute(request)
        except Exception as exc:
            result = ToolResult(
                tool_name=request.tool_name,
                action=request.action,
                status="failure",
                error=f"tool_raised: {type(exc).__name__}: {exc}",
            )

        return self._record(result, request, started,
                            outcome=result.status,
                            permission=permission)

    def _malformed_result(self, request):
        return ToolResult(
            tool_name=getattr(request, "tool_name", "unknown"),
            action=getattr(request, "action", "unknown"),
            status="failure",
            error="malformed_request",
        )

    def _record(self, result: ToolResult, request: ToolRequest,
                started, outcome: str, permission=None) -> ToolResult:
        duration = _elapsed(started)
        result.metadata["duration_ms"] = duration
        result.metadata["reason"] = request.reason

        log_tool_event({
            "event": "tool_execution",
            "tool": result.tool_name,
            "action": result.action,
            "outcome": outcome,
            "duration_ms": duration,
            "permission": permission,
        })

        return result


def _elapsed(started):
    return int((time.time() - started) * 1000)


tool_executor = ToolExecutor()
