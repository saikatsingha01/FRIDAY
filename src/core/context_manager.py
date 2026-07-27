conversation_context = []


# Maximum number of recent conversations to keep
MAX_CONTEXT = 5



def add_context(user_message, friday_response):

    conversation_context.append(
        {
            "user": user_message,
            "friday": friday_response
        }
    )


    # Remove oldest context when limit exceeds
    if len(conversation_context) > MAX_CONTEXT:

        conversation_context.pop(0)



def get_context():

    return conversation_context



def get_recent_context(limit=3):

    return conversation_context[-limit:]



def clear_context():

    conversation_context.clear()