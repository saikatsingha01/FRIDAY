from collections import deque


# ==========================================================
# CONFIG
# ==========================================================

MAX_CONTEXT = 10


# ==========================================================
# STORAGE
# ==========================================================

conversation_context = deque(maxlen=MAX_CONTEXT)


# ==========================================================
# ADD
# ==========================================================

def add_context(user_message, friday_response):

    conversation_context.append({

        "user": user_message,

        "friday": friday_response

    })


# ==========================================================
# READ
# ==========================================================

def get_context():

    return list(conversation_context)


def get_recent_context(limit=5):

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
# MANAGEMENT
# ==========================================================

def clear_context():

    conversation_context.clear()