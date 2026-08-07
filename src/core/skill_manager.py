# ==========================================================
# SKILL MANAGER (compatibility adapter)
#
# Phase 5 — the old keyword-based run_skill() is gone. Skills
# are now registered BaseTools executed via the ToolExecutor.
# This module keeps a thin compatibility wrapper for any caller
# that still references run_skill() by name; it executes a named
# tool directly without keyword matching.
# ==========================================================

from src.contracts.tool import ToolRequest
from src.skills import skill_registry
from src.execution.tool_executor import tool_executor


def run_skill(name, action="evaluate", parameters=None):
    """
    Execute a registered tool by name. Keyword matching is gone —
    callers must pass the registered tool name explicitly.
    Returns the structured ToolResult.
    """
    if not name:
        return None

    tool = skill_registry.get_tool(name)

    if tool is None:
        return None

    request = ToolRequest(
        tool_name=name,
        action=action,
        parameters=parameters or {},
        permission=tool.metadata.permission,
    )

    results = tool_executor.execute([request])

    if not results:
        return None

    return results[0]
