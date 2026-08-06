from collections import deque
from datetime import datetime


# ==========================================================
# CONFIG
# ==========================================================

MAX_CONTEXT = 15

# Inactivity (seconds) after which the session is rolled into a
# single episode summary (Issue 7).
INACTIVITY_TIMEOUT = 600.0


# ==========================================================
# STORAGE — the working-memory buffer.
# Bounded in-memory only. Never persisted directly; on rollover
# the whole buffer becomes one episode.
# ==========================================================

conversation_context = deque(maxlen=MAX_CONTEXT)

_session_started = datetime.now().isoformat()

# Active plan state (Phase 3 planning continuity).
# Session-scoped, in-memory, never persisted. Carries the goal the
# user is currently working toward so a correction or follow-up keeps
# planning instead of dropping the goal mid-thread. Cleared when the
# session rolls over or is explicitly cleared (never touches the
# long-term memory store).
_active_plan = None


# ==========================================================
# ADD
# ==========================================================

def add_context(user_message, friday_response):

    conversation_context.append({
        "user": user_message,
        "friday": friday_response,
        "_ts": datetime.now().isoformat(),
    })


# ==========================================================
# READ
# ==========================================================

def get_context():

    return list(conversation_context)


def get_recent_context(limit=8):

    if limit <= 0:

        return []

    return list(conversation_context)[-limit:]


def last_exchange():

    if not conversation_context:

        return None

    return conversation_context[-1]


def context_size():

    return len(conversation_context)


# ==========================================================
# ACTIVE PLAN — the goal the user is currently working toward.
# Universal session state: never inspects message text, never
# keyword-based. The planner sets it after a plan runs and reads
# it on the next turn so follow-ups continue the goal.
# ==========================================================

def set_active_plan(plan, goal_text: str = ""):
    """
    Records the plan currently in progress. Called by the
    ExecutionManager after a plan runs (fresh or continued).
    """
    global _active_plan

    if plan is None:
        return

    steps = []
    for step in getattr(plan, "steps", []):
        title = getattr(step, "title", "")
        desc  = getattr(step, "description", "")
        if title:
            steps.append(
                title if not desc else f"{title} — {desc}"
            )

    now = datetime.now().isoformat()

    if (
        _active_plan
        and getattr(plan, "continues_active_plan", False)
    ):
        _active_plan["goal"]       = getattr(plan, "goal", "")
        _active_plan["steps"]      = steps
        _active_plan["updated_at"] = now
    else:
        _active_plan = {
            "goal":       getattr(plan, "goal", ""),
            "goal_text":  goal_text,
            "steps":      steps,
            "created_at": now,
            "updated_at": now,
        }


def get_active_plan():
    return _active_plan


def clear_active_plan():
    global _active_plan
    _active_plan = None


# ==========================================================
# SESSION
# ==========================================================

def session_started():

    return _session_started


# ==========================================================
# ROLLOVER — turn the working buffer into one episode.
# ==========================================================

def rollover(force=False):
    """
    Writes the current buffer as a single episode and clears it.

    Called on farewell (Issue 10 triage signal), inactivity timeout,
    or buffer overflow. Returns the created episode or None.
    """

    from src.memory.episode_summarizer import summarize_conversation

    if not conversation_context:
        return None

    episode = summarize_conversation(
        conversation_context,
        force=force,
    )

    if episode is not None:
        conversation_context.clear()
        clear_active_plan()
        _reset_session()

    return episode


def maybe_rollover(force=False):
    """
    Rolls over when the buffer is idle too long or force is set.
    """
    if force:
        return rollover(force=True)

    if not conversation_context:
        return None

    last = conversation_context[-1].get("_ts")

    try:
        last_time = datetime.fromisoformat(last)
        idle = (datetime.now() - last_time).total_seconds()
    except Exception:
        idle = 0.0

    if idle >= INACTIVITY_TIMEOUT:
        return rollover(force=True)

    return None


def _reset_session():

    global _session_started

    _session_started = datetime.now().isoformat()


# ==========================================================
# MANAGEMENT
# ==========================================================

def clear_context():

    conversation_context.clear()
    clear_active_plan()
    _reset_session()
