# ==========================================================
# TOOL REGISTRY
#
# Phase 5 — single source of truth for every registered tool.
#
# Replaces the old keyword/startswith skill dict. Tools register
# themselves by name; the router, executor, permission gate and
# Reflection all read from here. Nothing in Brain or Execution
# hardcodes a tool import.
# ==========================================================

from typing import List, Optional

from src.skills.tool_base import BaseTool


_tools = {}


def register(tool: BaseTool) -> None:
    """
    Register a tool instance. Called at import time by each tool
    module (via the auto-discovery loader). initialize() runs
    exactly once here.
    """
    if not isinstance(tool, BaseTool):
        raise TypeError(f"register() expects a BaseTool, got {type(tool)}")

    name = tool.metadata.name

    if not name:
        raise ValueError("Tool must declare a metadata.name")

    tool.initialize()

    _tools[name] = tool


def get_tool(name: str) -> Optional[BaseTool]:
    return _tools.get(name)


def has_tool(name: str) -> bool:
    return name in _tools


def all_tools() -> List[BaseTool]:
    return list(_tools.values())


def clear() -> None:
    """Test hook: drop all registered tools."""
    _tools.clear()
