# ==========================================================
# TOOL LOGGER
#
# Phase 5 — structured execution log for tools. Feeds Phase 6
# (Reflection): every event records tool name, action, start/
# finish timestamps, duration, outcome and denial state in a
# machine-readable line (JSON) appended to logs/tools.log.
# ==========================================================

import json
import os
import time

from src.utils.logger import LOG_FOLDER


TOOL_LOG = os.path.join(LOG_FOLDER, "tools.log")


def _iso():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def log_tool_event(event: dict) -> None:
    """
    Append one structured tool event. Never raises — logging
    must not crash the tool path.
    """
    record = dict(event)
    record.setdefault("ts", _iso())

    try:
        with open(TOOL_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, default=str) + "\n")
    except Exception:
        pass
