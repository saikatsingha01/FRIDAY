from datetime import datetime

from src.contracts.language_understanding import (
    LanguageUnderstanding,
)

from src.contracts.execution import (
    ExecutionResult,
)


# =====================================================
# FORMATTERS
# =====================================================

def _format_context(context):

    if not context:
        return "None"

    if isinstance(context, list):
        lines = []
        for item in context:
            if isinstance(item, dict):
                user = item.get("user", "")
                friday = item.get("friday", "")
                if user:
                    lines.append(f"User: {user}")
                if friday:
                    lines.append(f"FRIDAY: {friday}")
                lines.append("")
            else:
                lines.append(f"- {item}")
        return "\n".join(lines).strip()

    return str(context)


def _format_memories(memories):

    if not memories:
        return "None"

    lines = []

    for memory in memories:

        if isinstance(memory, dict):

            text = memory.get("text", "")

            if text:
                lines.append(f"- {text}")

        else:

            lines.append(f"- {memory}")

    return "\n".join(lines)


def _format_episodes(episodes):

    if not episodes:
        return "None"

    lines = []

    for episode in episodes:

        if isinstance(episode, dict):

            summary = episode.get("summary", "")
            timestamp = episode.get("timestamp", "")

            if summary:
                if timestamp:
                    lines.append(f"- [{timestamp[:10]}] {summary}")
                else:
                    lines.append(f"- {summary}")

        else:

            lines.append(f"- {episode}")

    return "\n".join(lines)


def _format_entities(understanding):

    entities = understanding.semantic.entities

    if not entities:
        return "None"

    lines = []

    for entity in entities:

        if hasattr(entity, "text"):
            lines.append(f"- {entity.text} ({entity.label})")

        elif isinstance(entity, dict):
            lines.append(f"- {entity.get('text')} ({entity.get('label')})")

        else:
            lines.append(str(entity))

    return "\n".join(lines)


# =====================================================
# PROMPT BUILDER
# =====================================================

def build_prompt(

    understanding: LanguageUnderstanding,

    execution: ExecutionResult,

):

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n========== EXECUTION DEBUG ==========\n")
    print("Memory count :", len(execution.memories))
    print("Episode count:", len(execution.episodes))
    print("Context count:", len(execution.context))
    print()

    if execution.memories:
        print("MEMORIES:\n")
        for memory in execution.memories:
            print(memory)
        print()

    if execution.episodes:
        print("EPISODES:\n")
        for episode in execution.episodes:
            print(episode)
        print()

    if execution.context:
        print("CONTEXT:\n")
        for ctx in execution.context:
            print(ctx)
        print()

    print("=====================================\n")

    memories_text = _format_memories(execution.memories)
    episodes_text = _format_episodes(execution.episodes)
    context_text = _format_context(execution.context)
    entities_text = _format_entities(understanding)
    emotion = understanding.emotion.emotion or "neutral"

    prompt = f"""You are FRIDAY — an intelligent AI operating companion built for one person.

You are not a generic assistant. You are a long-term companion who remembers, learns, and adapts.

Your personality is calm, confident, curious, and direct. You never sound robotic or templated.
You vary your sentence structure and vocabulary naturally. You never repeat the same phrasing twice.
You are honest — if you don't know something, you say so clearly without apology.

Current time: {current_time}
User's emotional state: {emotion}

==================================================
WHAT YOU KNOW ABOUT THE USER
==================================================

Long-term memory:
{memories_text}

Past experiences:
{episodes_text}

Recent conversation:
{context_text}

Relevant entities mentioned:
{entities_text}

==================================================
RULES
==================================================

- Use memories only when they are directly relevant to what the user asked.
- Never invent facts. Never claim to remember something not listed above.
- If the user asked about something and it is not in memory, say you don't have that information yet — do not guess.
- If the user is storing or updating a fact and you confirmed it, respond naturally. Vary your confirmations. Never use the same phrase twice.
- Match your tone to the user's emotional state.
- Keep responses concise unless the user asks for detail.
- Never expose your internal pipeline, reasoning steps, or memory system names.

==================================================
USER MESSAGE
==================================================

{understanding.raw_text}

==================================================
FRIDAY RESPONSE
==================================================""".strip()

    print("\n========== FINAL PROMPT ==========\n")
    print(prompt)
    print("\n==================================\n")

    return prompt