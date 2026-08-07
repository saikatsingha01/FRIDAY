# ==========================================================
# FILE MANAGER TOOL
#
# Phase 5 — read / write / list / delete files and directories.
#
# Scoped to a base directory so a structured action can never
# wander outside the workspace. Write and delete are
# permission-gated (denied by default). Never decides whether to
# run; never sees raw user text.
# ==========================================================

import os
import time

from src.contracts.tool import (
    ToolRequest,
    ToolResult,
    ToolMetadata,
    ToolPermission,
)
from src.skills.skill_registry import register
from src.skills.tool_base import BaseTool


# Base sandbox for file actions. All paths resolve inside this.
DEFAULT_BASE = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)


class FileManagerTool(BaseTool):

    metadata = ToolMetadata(
        name="file_manager",
        description=(
            "Read, write, list or delete files and directories "
            "inside the workspace sandbox."
        ),
        capabilities=["tool_use", "automation"],
        goals=["create", "plan", "solve_problem"],
        permission=ToolPermission.SAFE,
        actions={
            "read": {
                "permission": ToolPermission.SAFE,
                "input": {"path": "str — file path relative to base"},
                "output": {"content": "str", "size": "int"},
            },
            "write": {
                "permission": ToolPermission.FILE_WRITE,
                "input": {"path": "str", "content": "str"},
                "output": {"written": "bool", "size": "int"},
            },
            "list": {
                "permission": ToolPermission.SAFE,
                "input": {"path": "str (optional, default base)"},
                "output": {"entries": "list of {name, path, type}"},
            },
            "delete": {
                "permission": ToolPermission.FILE_DELETE,
                "input": {"path": "str"},
                "output": {"deleted": "bool"},
            },
        },
        needs_network=False,
        errors=[
            "unsupported_action", "empty_path", "path_escape",
            "not_found", "is_dir", "io_error",
        ],
    )

    def execute(self, request: ToolRequest) -> ToolResult:

        action = request.action

        if action not in self.metadata.actions:
            return self.fail(
                request,
                f"unsupported_action: {action}",
            )

        path = self._resolve(request.parameters.get("path"))

        if path is False:
            return self.fail(request, "path_escape")

        if action == "list" and not path:
            path = DEFAULT_BASE

        if action != "list" and not path:
            return self.fail(request, "empty_path")

        try:
            if action == "read":
                return self._read(request, path)
            if action == "write":
                return self._write(request, path)
            if action == "list":
                return self._list(request, path)
            if action == "delete":
                return self._delete(request, path)
        except Exception as exc:
            return self.fail(
                request,
                f"io_error: {type(exc).__name__}: {exc}",
            )

        return self.fail(request, f"unsupported_action: {action}")

    # ==========================================
    # ACTIONS
    # ==========================================

    def _read(self, request, path):
        if os.path.isdir(path):
            return self.fail(request, "is_dir")

        if not os.path.exists(path):
            return self.fail(request, "not_found")

        started = time.time()

        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        return self.ok(
            request,
            data={"content": content, "size": len(content)},
            duration_ms=int((time.time() - started) * 1000),
        )

    def _write(self, request, path):
        if os.path.isdir(path):
            return self.fail(request, "is_dir")

        content = request.parameters.get("content")
        if content is None:
            content = ""

        started = time.time()

        directory = os.path.dirname(path)
        if directory and not os.path.isdir(directory):
            os.makedirs(directory, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(str(content))

        return self.ok(
            request,
            data={"written": True, "size": os.path.getsize(path)},
            duration_ms=int((time.time() - started) * 1000),
        )

    def _list(self, request, path):
        if os.path.isfile(path):
            return self.ok(
                request,
                data={"entries": [{
                    "name": os.path.basename(path),
                    "path": path,
                    "type": "file",
                }]},
            )

        if not os.path.isdir(path):
            return self.fail(request, "not_found")

        entries = []

        for name in sorted(os.listdir(path)):
            full = os.path.join(path, name)
            entries.append({
                "name": name,
                "path": full,
                "type": "dir" if os.path.isdir(full) else "file",
            })

        return self.ok(request, data={"entries": entries})

    def _delete(self, request, path):
        if not os.path.exists(path):
            return self.fail(request, "not_found")

        started = time.time()

        if os.path.isdir(path):
            import shutil
            shutil.rmtree(path)
        else:
            os.remove(path)

        return self.ok(
            request,
            data={"deleted": True},
            duration_ms=int((time.time() - started) * 1000),
        )

    # ==========================================
    # SAFETY
    # ==========================================

    def _resolve(self, raw_path):
        """
        Resolve a structured relative path against DEFAULT_BASE.
        Returns:
          - an absolute normalized path on success
          - False when the path escapes the sandbox
          - None when the path is empty
        """
        if raw_path is None:
            return None

        path = str(raw_path).strip()

        if not path:
            return None

        # Strip a leading slash / drive letter so only relative
        # paths within the workspace are addressable.
        path = path.replace("\\", "/").lstrip("/")

        path = re_sub_drive(path)

        full = os.path.normpath(os.path.join(DEFAULT_BASE, path))

        if not full.startswith(os.path.normpath(DEFAULT_BASE)):
            return False

        return full


def re_sub_drive(path):
    import re
    return re.sub(r"^[a-zA-Z]:", "", path)


file_manager_tool = FileManagerTool()

register(file_manager_tool)
