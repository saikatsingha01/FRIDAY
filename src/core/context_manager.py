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
    _reset_session()
