from src.core.skill_manager import run_skill
from src.core.intent_detector import detect_intent
from src.core.response_manager import get_response

from src.memory.memory_manager import (
    save_memory_direct,
    auto_remember,
    get_important_memories,
    get_memories_by_category,
    forget_memory,
    memory_count
)


def handle_command(command):

    command = command.lower().strip()

    intent = detect_intent(command)

    # ---------------------------------
    # Greeting
    # ---------------------------------

    if intent == "greeting":

        return get_response("greeting")

    # ---------------------------------
    # Identity
    # ---------------------------------

    if intent == "identity":

        return get_response("identity")

    # ---------------------------------
    # Exit
    # ---------------------------------

    if intent == "exit":

        return "shutdown"

    # ---------------------------------
    # Remember
    # ---------------------------------

    if intent == "remember":

        fact = command.replace(
            "remember",
            "",
            1
        ).strip()

        if fact:

            return save_memory_direct(fact)

        return "What should I remember?"

    # ---------------------------------
    # Forget
    # ---------------------------------

    if intent == "forget":

        keyword = command.replace(
            "forget",
            "",
            1
        ).strip()

        if keyword:

            return forget_memory(keyword)

        return "What should I forget?"

    # ---------------------------------
    # Memory Count
    # ---------------------------------

    if intent == "memory_count":

        return f"I have {memory_count()} memories stored."

    # ---------------------------------
    # Memory List
    # ---------------------------------

    if intent == "memory_list":

        memories = get_important_memories()

        if not memories:

            return "I don't remember anything yet."

        facts = []

        for item in memories:

            facts.append(item["text"])

        return "I remember: " + ", ".join(facts)

    # ---------------------------------
    # Category Search
    # ---------------------------------

    if command.startswith("show my"):

        category = command.replace(
            "show my",
            "",
            1
        ).strip()

        memories = get_memories_by_category(category)

        if not memories:

            return "I don't have any memories in that category."

        facts = []

        for item in memories:

            facts.append(item["text"])

        return "I remember: " + ", ".join(facts)

    # ---------------------------------
    # Automatic Memory
    # ---------------------------------

    if intent == "unknown":

        if not command.endswith("?"):

            print("DEBUG: Checking automatic memory...")

            if auto_remember(command):

                print("DEBUG: Memory saved")

                return "I'll remember that."

            else:

                print("DEBUG: Memory rejected")

    # ---------------------------------
    # Skills
    # ---------------------------------

    skill_response = run_skill(command)

    if skill_response:

        return skill_response

    # ---------------------------------
    # Let Brain send it to the LLM
    # ---------------------------------

    return "I don't understand that yet."