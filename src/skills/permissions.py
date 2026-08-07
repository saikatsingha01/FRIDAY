# ==========================================================
# PERMISSION GATE
#
# Phase 5 — the only place that decides whether a tool action is
# permitted. Lives in the tool execution path (never the Brain,
# never the ToolRouter).
#
# Policy:
#   - ToolPermission.SAFE is allowed by default.
#   - Dangerous classes (file write/delete, terminal, app launch)
#     are DENIED by default.
#   - Grants come from the environment variable FRIDAY_TOOL_PERMS
#     (comma-separated permission names) — e.g.
#       FRIDAY_TOOL_PERMS=terminal,file_write
#   - Grants can also come from a per-process list the caller
#     (e.g. a test harness or config loader) passes to grant().
#
# The gate never fails closed silently: a denied action returns a
# structured permission_denied ToolResult upstream — never a crash.
# ==========================================================

import os
from typing import Iterable, Set

from src.contracts.tool import ToolPermission


class PermissionGate:

    def __init__(self):
        # Start from the static defaults.
        self._allowed: Set[str] = {
            perm
            for perm, default in ToolPermission.DEFAULT_ALLOWED.items()
            if default
        }
        self._load_environment()

    def _load_environment(self):
        raw = os.environ.get("FRIDAY_TOOL_PERMS", "")
        for token in raw.split(","):
            token = token.strip()
            if token:
                self._allowed.add(token)

    def grant(self, *permissions: str) -> None:
        """Explicitly allow one or more permission classes."""
        for perm in permissions:
            self._allowed.add(perm)

    def revoke(self, *permissions: str) -> None:
        for perm in permissions:
            self._allowed.discard(perm)

    def reset(self) -> None:
        """Restore default-safe state (test hook)."""
        self._allowed = {
            perm
            for perm, default in ToolPermission.DEFAULT_ALLOWED.items()
            if default
        }
        self._load_environment()

    def allowed(self, permission: str) -> bool:
        if permission is None:
            # None means the tool declared no permission class,
            # which is treated as safe.
            return True
        return permission in self._allowed

    def check(self, permission: str) -> str:
        """
        Returns the enforcement verdict as a closed string:
        "allowed" | "denied". Structured, never English prose.
        """
        if self.allowed(permission):
            return "allowed"
        return "denied"


permission_gate = PermissionGate()
