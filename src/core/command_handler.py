from src.core.skill_manager import run_skill
from src.core.intent_detector import detect_intent
from src.core.response_manager import get_response

from src.memory.memory_manager import (
    save_memory_direct,
    auto_remember,
    get_important_memories,
    get_memories_by_category,
    forget_memory,
    memory_count,
    recall_from_question
)


def handle_command(command):

    command = command.lower().strip()

    intent = detect_intent(command)

    # Greeting
    if intent == "greeting":
        return get_response("greeting")

    # Identity
    if intent == "identity":
        return get_response("identity")

    # Exit
    if intent == "exit":
        return "shutdown"

    # Remember
    if intent == "remember":

        fact = command.replace("remember", "").strip()

        if fact:
            return save_memory_direct(fact)

        return "What should I remember?"

    # Forget
    if intent == "forget":

        keyword = command.replace("forget", "").strip()

        if keyword:
            return forget_memory(keyword)

        return "What should I forget?"

    # Memory Count
    if intent == "memory_count":
        return f"I have {memory_count()} memories stored."

    # Smart Memory Recall
    if intent == "memory_recall":

        answer = recall_from_question(command)

        if answer:
            return answer

    # Show all memories
    if "what do you remember" in command:

        memories = get_important_memories()

        if memories:

            facts = []

            for item in memories:
                facts.append(
                    f"{item['text']} (importance {item['importance']})"
                )

            return "I remember: " + ", ".join(facts)

        return "I don't remember anything yet."

    # Category Search
    if command.startswith("show my"):

        category = command.replace("show my", "").strip()

        memories = get_memories_by_category(category)

        if memories:

            facts = []

            for item in memories:
                facts.append(item["text"])

            return "I remember: " + ", ".join(facts)

        return "I don't have any memories in that category."

    # Skills
    skill_response = run_skill(command)

    if skill_response:
        return skill_response

    # Automatic Memory
    if (
        not command.endswith("?")
        and intent == "unknown"
    ):

        if auto_remember(command):
            return "I'll remember that."

    return "I don't understand that yet."