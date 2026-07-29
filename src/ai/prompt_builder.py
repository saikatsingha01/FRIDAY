def build_prompt(message, memories=None, context=None, episodes=None):

    prompt = ""

    # ---------------------------------
    # SYSTEM INSTRUCTIONS
    # ---------------------------------

    prompt += (
        "You are FRIDAY, an intelligent voice assistant.\n\n"

        "You have access to three different information sources:\n\n"

        "1. FACT MEMORY:\n"
        "Stable information about the user.\n"
        "Examples: device specifications, preferences, projects.\n\n"

        "2. EPISODE MEMORY:\n"
        "Summaries of previous conversations.\n"
        "Use these only when the user asks about previous discussions "
        "or when they are relevant.\n\n"

        "3. CURRENT CONTEXT:\n"
        "Recent messages from the current conversation.\n\n"

        "Rules:\n"
        "- Use memories only when relevant.\n"
        "- Never expose internal metadata like importance scores.\n"
        "- Never invent memories.\n"
        "- Never claim you cannot remember previous conversations if relevant "
        "episode information is provided.\n"
        "- If information is unavailable, say you do not know.\n"
        "- Respond naturally and conversationally.\n\n"
    )


    # ---------------------------------
    # FACT MEMORY
    # ---------------------------------

    if memories:

        prompt += "FACT MEMORY:\n"

        for memory in memories:

            if isinstance(memory, dict):
                prompt += f"- {memory.get('text', '')}\n"

            else:
                prompt += f"- {memory}\n"

        prompt += "\n"


    # ---------------------------------
    # EPISODE MEMORY
    # ---------------------------------

    if episodes:

        prompt += "EPISODE MEMORY:\n"

        for episode in episodes:

            if isinstance(episode, dict):

                if "summary" in episode:
                    prompt += f"- {episode['summary']}\n"

                elif "text" in episode:
                    prompt += f"- {episode['text']}\n"

                else:
                    prompt += f"- {episode}\n"

            else:
                prompt += f"- {episode}\n"

        prompt += "\n"


    # ---------------------------------
    # CURRENT CONVERSATION CONTEXT
    # ---------------------------------

    if context:

        prompt += "CURRENT CONTEXT:\n"

        for item in context:

            if isinstance(item, dict):

                prompt += (
                    f"User: {item.get('user', '')}\n"
                    f"FRIDAY: {item.get('friday', '')}\n"
                )

            else:

                prompt += f"- {item}\n"

        prompt += "\n"


    # ---------------------------------
    # CURRENT USER MESSAGE
    # ---------------------------------

    prompt += (
        "CURRENT USER MESSAGE:\n"
        f"User: {message}\n\n"
        "FRIDAY:"
    )


    # ---------------------------------
    # DEBUG
    # ---------------------------------

    print("\n--- PROMPT DEBUG ---")
    print(prompt)
    print("Prompt size:", len(prompt), "characters")
    print("--- END PROMPT DEBUG ---\n")


    return prompt