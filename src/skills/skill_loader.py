# ==========================================================
# TOOL AUTO-DISCOVERY
#
# Phase 5 — scans the skills package, imports every tool module,
# and lets each module register its tool(s) via the registry.
#
# No hardcoded imports: adding a new tool = dropping a new
# *_tool.py file into src/skills/.
# ==========================================================

import importlib
import os

from src.skills import skill_registry


# Modules that are part of the framework, not tools.
_SKIP = {
    "__init__.py",
    "skill_loader.py",
    "skill_registry.py",
    "tool_base.py",
    "permissions.py",
}


def load_skills():
    """
    Import every tool module in the package so it can register
    itself. Returns the names of all registered tools after the scan.
    """

    skill_folder = os.path.dirname(__file__)

    for file in sorted(os.listdir(skill_folder)):

        if not file.endswith(".py"):
            continue

        if file in _SKIP:
            continue

        module_name = file[:-3]

        try:
            importlib.import_module(f"src.skills.{module_name}")
        except Exception as exc:
            print(
                f"[tool_loader] failed to import {module_name}: "
                f"{type(exc).__name__}: {exc}"
            )

    return sorted(tool.metadata.name for tool in skill_registry.all_tools())


_loaded = False


def ensure_loaded():
    """
    Idempotent discovery: import tool modules exactly once per
    process. Tools may already be registered if a module imported
    them directly — registration is by name so re-imports are safe.
    """
    global _loaded
    if not _loaded:
        load_skills()
        _loaded = True
