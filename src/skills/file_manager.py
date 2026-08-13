# ==========================================================
# FILE MANAGER TOOL
#
# Phase 5 — read / write / list / delete / locate files and
# directories anywhere on the machine. Every reference runs
# through the universal path resolver: absolute paths, drive
# letters, known folders, and folder/file names all resolve to
# a real absolute path or an explicit not_found. There is NO
# silent fallback to the workspace — a reference that cannot be
# resolved is an honest miss, never an implicit listing.
#
# Write and delete are permission-gated (denied by default).
# Never decides whether to run; never sees raw user text.
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
from src.utils.path_resolver import (
    locate_reference,
    resolve_reference,
    set_last_listed_scope,
)


class FileManagerTool(BaseTool):

    metadata = ToolMetadata(
        name="file_manager",
        description=(
            "Read, write, list, delete or locate files and directories "
            "anywhere on the machine."
        ),
        capabilities=["tool_use", "automation"],
        goals=["create", "plan", "solve_problem"],
        permission=ToolPermission.SAFE,
        actions={
            "read": {
                "permission": ToolPermission.SAFE,
                "input": {"path": "str — file path, folder name, or drive"},
                "output": {"content": "str", "size": "int"},
            },
            "write": {
                "permission": ToolPermission.FILE_WRITE,
                "input": {"path": "str", "content": "str"},
                "output": {"written": "bool", "size": "int"},
            },
            "list": {
                "permission": ToolPermission.SAFE,
                "input": {"path": "str — folder path, name, or drive"},
                "output": {"entries": "list of {name, path, type}"},
            },
            "delete": {
                "permission": ToolPermission.FILE_DELETE,
                "input": {"path": "str"},
                "output": {"deleted": "bool"},
            },
            "locate": {
                "permission": ToolPermission.SAFE,
                "input": {"path": "str — file or folder reference"},
                "output": {"found": "bool", "path": "str", "kind": "str"},
            },
        },
        needs_network=False,
        errors=[
            "unsupported_action", "empty_path", "not_found",
            "is_dir", "io_error",
        ],
    )

    def execute(self, request: ToolRequest) -> ToolResult:

        action = request.action

        if action not in self.metadata.actions:
            return self.fail(
                request,
                f"unsupported_action: {action}",
            )

        raw = request.parameters.get("path")

        if raw is None or not str(raw).strip():
            return self.fail(request, "empty_path")

        reference = str(raw).strip()

        # A locate is resolved through locate_reference — it only ever
        # reports paths that EXIST right now, distinguishes exact /
        # normalized / fuzzy matches, and collects multiple matches so
        # a duplicate name can be reported honestly. It runs before the
        # shared not_found gate because its miss shape differs.
        if action == "locate":
            return self._locate(request, reference)

        resolved = resolve_reference(reference)

        if not resolved.found:
            return self._not_found(request, reference)

        path = resolved.path

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
            return self._not_found(request, path)

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
                }], "path": path},
            )

        if not os.path.isdir(path):
            return self._not_found(request, path)

        entries = []

        for name in sorted(os.listdir(path)):
            full = os.path.join(path, name)
            entries.append({
                "name": name,
                "path": full,
                "type": "dir" if os.path.isdir(full) else "file",
            })

        # The entries are now "recently seen" by the user. A follow-up
        # that refers to one of them ("whats inside that <name>
        # directory") can resolve tolerantly inside this directory even
        # when a whispered name drifts a token.
        set_last_listed_scope(path)

        return self.ok(request, data={"entries": entries, "path": path})

    def _delete(self, request, path):
        if not os.path.exists(path):
            return self._not_found(request, path)

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

    def _locate(self, request, reference):
        located = locate_reference(reference)
        if not located.found:
            return self._not_found(request, reference)
        kind = located.kind or (
            "dir" if os.path.isdir(located.path) else "file"
        )
        data = {
            "found": True,
            "path": located.path,
            "kind": kind,
            "match": located.match,
            "requested": reference,
        }
        if len(located.candidates) > 1:
            data["candidates"] = [
                {
                    "path": cand.path,
                    "kind": cand.kind or (
                        "dir" if os.path.isdir(cand.path) else "file"
                    ),
                    "match": cand.match,
                }
                for cand in located.candidates
            ]
        return self.ok(request, data=data)

    # ==========================================
    # FAILURE
    # ==========================================

    def _not_found(self, request, requested):
        return ToolResult(
            tool_name=request.tool_name,
            action=request.action,
            status="not_found",
            error="not_found",
            metadata={"requested": requested},
        )


file_manager_tool = FileManagerTool()

register(file_manager_tool)
