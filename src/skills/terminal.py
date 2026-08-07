# ==========================================================
# TERMINAL TOOL
#
# Phase 5 — arbitrary shell execution. Permission-gated: denied
# by default, requires FRIDAY_TOOL_PERMS=terminal or an explicit
# gate.grant(). Never decides whether to run; never sees raw
# user text; short timeout so a command can never hang the Brain.
# ==========================================================

import subprocess
import time

from src.contracts.tool import (
    ToolRequest,
    ToolResult,
    ToolMetadata,
    ToolPermission,
)
from src.skills.skill_registry import register
from src.skills.tool_base import BaseTool


class TerminalTool(BaseTool):

    metadata = ToolMetadata(
        name="terminal",
        description=(
            "Run a shell command on the host machine. Dangerous: "
            "permission-gated, denied by default."
        ),
        capabilities=["system", "tool_use", "automation"],
        goals=["solve_problem", "create", "plan"],
        permission=ToolPermission.TERMINAL,
        actions={
            "run": {
                "input": {
                    "command": "str — the shell command to execute",
                    "timeout": "int (optional, seconds, default 30)",
                },
                "output": {
                    "exit_code": "int",
                    "stdout": "str",
                    "stderr": "str",
                },
            },
        },
        needs_network=False,
        errors=[
            "unsupported_action", "empty_command", "timeout",
            "spawn_error",
        ],
    )

    def execute(self, request: ToolRequest) -> ToolResult:

        action = request.action

        if action != "run":
            return self.fail(
                request,
                f"unsupported_action: {action}",
            )

        command = str(request.parameters.get("command") or "").strip()

        if not command:
            return self.fail(request, "empty_command")

        timeout = int(request.parameters.get("timeout") or 30)

        started = time.time()

        try:
            proc = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as exc:
            return self.fail(
                request,
                f"timeout: {exc}",
            )
        except Exception as exc:
            return self.fail(
                request,
                f"spawn_error: {type(exc).__name__}: {exc}",
            )

        return self.ok(
            request,
            data={
                "exit_code": proc.returncode,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
            },
            duration_ms=int((time.time() - started) * 1000),
        )


terminal_tool = TerminalTool()

register(terminal_tool)
