# ==========================================================
# APPLICATION LAUNCHER TOOL
#
# Phase 5 — launch an application by name/path on the host.
# Permission-gated: denied by default. Never decides whether to
# run; never sees raw user text. Windows uses os.startfile.
#
# The launcher holds NO hardcoded application names or install
# paths. Every reference is resolved through the universal
# AppCatalog, which discovers installed applications from the
# OS (Start Menu, Desktop, registry, WindowsApps, Steam, Epic)
# and matches the user's natural phrasing against that catalog
# with generic rules. When several apps match with similar
# confidence it reports an ambiguity (and never guesses); when
# nothing matches it reports not found.
# ==========================================================

import os
import platform
import subprocess
import time

from src.contracts.tool import (
    ToolRequest,
    ToolResult,
    ToolMetadata,
    ToolPermission,
)
from src.skills.app_catalog import app_catalog
from src.skills.skill_registry import register
from src.skills.tool_base import BaseTool


class ApplicationLauncherTool(BaseTool):

    metadata = ToolMetadata(
        name="app_launcher",
        description=(
            "Launch an application on the host machine. "
            "Permission-gated, denied by default."
        ),
        capabilities=["device", "automation"],
        goals=["create", "plan", "solve_problem"],
        permission=ToolPermission.APP_LAUNCH,
        actions={
            "launch": {
                "input": {
                    "app": "str — application name or path",
                },
                "output": {
                    "launched": "bool",
                    "detail": "str — display name (never a path)",
                },
            },
        },
        needs_network=False,
        errors=[
            "unsupported_action", "empty_app", "unsupported_platform",
            "launch_error", "not_found", "ambiguous",
        ],
    )

    def execute(self, request: ToolRequest) -> ToolResult:

        action = request.action

        if action != "launch":
            return self.fail(
                request,
                f"unsupported_action: {action}",
            )

        app = str(request.parameters.get("app") or "").strip()

        if not app:
            return self.fail(request, "empty_app")

        if platform.system() != "Windows":
            return self.fail(
                request,
                f"unsupported_platform: {platform.system()}",
            )

        resolved = app_catalog.resolve(app)

        # --------------------------------------------------
        # NOT FOUND — no installed application matches. This
        # is an honest "couldn't do it", never a guess.
        # --------------------------------------------------
        if resolved["status"] == "not_found":
            return ToolResult(
                tool_name=request.tool_name,
                action=request.action,
                status="not_found",
                error="not_found",
                data={"app": app},
            )

        # --------------------------------------------------
        # AMBIGUOUS — several installed applications match the
        # reference with similar confidence. Never pick one:
        # report the options so the user can choose.
        # --------------------------------------------------
        if resolved["status"] == "ambiguous":
            return self.ok(
                request,
                data={
                    "launched": False,
                    "ambiguous": True,
                    "candidates": resolved.get("candidates", []),
                },
            )

        # --------------------------------------------------
        # FOUND — resolved to one concrete launchable.
        # The result carries only the display label, never the
        # absolute path, so the response never reads paths aloud.
        # --------------------------------------------------
        target = resolved["target"]
        label  = resolved["label"]
        aumid  = resolved.get("aumid") or None

        started = time.time()

        # Packaged (Store) apps resolve to a WindowsApps alias stub
        # or to a Start-Apps AUMID entry that os.startfile cannot
        # activate reliably — the shell returns success but the app may
        # never surface (observed: the launcher process starts, the UI
        # never does). Activating by AUMID through the shell:AppsFolder
        # namespace is the reliable path; os.startfile remains the
        # fallback for entries with a real target file, and a second
        # shell activation is retried for AUMID-only entries.
        try:
            if aumid:
                subprocess.Popen(
                    ["explorer.exe", "shell:AppsFolder\\" + aumid],
                    creationflags=0x08000000,  # CREATE_NO_WINDOW
                )
            else:
                os.startfile(target)
        except Exception as exc:
            if aumid:
                try:
                    if os.path.isfile(target):
                        os.startfile(target)
                    else:
                        subprocess.Popen(
                            ["explorer.exe", "shell:AppsFolder\\" + aumid],
                            creationflags=0x08000000,
                        )
                except Exception as fallback_exc:
                    return self.fail(
                        request,
                        f"launch_error: "
                        f"{type(fallback_exc).__name__}: {fallback_exc}",
                    )
            else:
                return self.fail(
                    request,
                    f"launch_error: {type(exc).__name__}: {exc}",
                )

        return self.ok(
            request,
            data={
                "launched": True,
                "detail": label,
            },
            duration_ms=int((time.time() - started) * 1000),
        )


app_launcher_tool = ApplicationLauncherTool()

register(app_launcher_tool)
