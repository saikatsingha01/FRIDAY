import json
import os

from src.memory.memory_evaluator import evaluate_memory

MEMORY_FILE = os.path.join(
    os.path.dirname(__file__),
    "memory.json"
)


def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return {
            "memories": []
        }

    with open(MEMORY_FILE, "r") as file:
        return json.load(file)



def save_memory(memory):

    with open(MEMORY_FILE, "w") as file:
        json.dump(
            memory,
            file,
            indent=4
        )



def detect_category(fact):

    if any(word in fact for word in [
        "laptop",
        "pc",
        "computer",
        "phone",
        "ram",
        "gpu",
        "rtx"
    ]):
        return "device"


    elif any(word in fact for word in [
        "love",
        "relationship",
        "family",
        "friend",
        "important",
        "never forget"
    ]):
        return "emotional"


    elif any(word in fact for word in [
        "like",
        "prefer",
        "favorite",
        "hate"
    ]):
        return "preference"


    elif any(word in fact for word in [
        "project",
        "building",
        "working on",
        "code"
    ]):
        return "project"


    elif any(word in fact for word in [
        "name",
        "called"
    ]):
        return "identity"


    else:
        return "general"



def calculate_importance(category):

    if category == "identity":
        return 10

    elif category == "emotional":
        return 10

    elif category == "project":
        return 9

    elif category == "device":
        return 8

    elif category == "preference":
        return 6

    else:
        return 3



def save_memory_direct(fact):

    memory = load_memory()


    for item in memory["memories"]:

        if item["text"] == fact:

            return "I already remember that."



    category = detect_category(fact)


    new_memory = {
        "id": len(memory["memories"]) + 1,
        "text": fact,
        "category": category,
        "importance": calculate_importance(category)
    }


    memory["memories"].append(new_memory)

    save_memory(memory)


    return "I will remember that."


def remember(fact):

    evaluation = evaluate_memory(fact)


    if not evaluation["should_remember"]:

        return (
            "I don't think this is important enough to remember. "
            f"Confidence: {evaluation['confidence']}%"
        )


    memory = load_memory()


    for item in memory["memories"]:

        if item["text"] == fact:

            return "I already remember that."



    category = detect_category(fact)


    new_memory = {
        "id": len(memory["memories"]) + 1,
        "text": fact,
        "category": category,
        "importance": calculate_importance(category),
        "confidence": evaluation["confidence"]
    }


    memory["memories"].append(new_memory)

    save_memory(memory)


    return "I will remember that."



def auto_remember(fact):

    evaluation = evaluate_memory(fact)


    if not evaluation["should_remember"]:

        return False


    memory = load_memory()


    for item in memory["memories"]:

        if item["text"] == fact:

            return False


    category = detect_category(fact)


    new_memory = {
        "id": len(memory["memories"]) + 1,
        "text": fact,
        "category": category,
        "importance": calculate_importance(category),
        "confidence": evaluation["confidence"]
    }


    memory["memories"].append(new_memory)

    save_memory(memory)


    return True



def get_memory():

    return load_memory()


def get_important_memories():

    memory = load_memory()

    memories = memory["memories"]

    memories.sort(
        key=lambda item: item["importance"],
        reverse=True
    )

    return memories



def get_memories_by_category(category):

    memory = load_memory()

    results = []

    for item in memory["memories"]:

        if item["category"] == category:
            results.append(item)

    return results



def memory_count():

    memory = load_memory()

    return len(memory["memories"])



def forget_memory(keyword):

    memory = load_memory()

    old_count = len(memory["memories"])


    memory["memories"] = [
        item for item in memory["memories"]
        if keyword not in item["text"]
    ]


    save_memory(memory)


    if len(memory["memories"]) < old_count:
        return "I forgot that."

    else:
        return "I couldn't find that memory."



def recall_from_question(question):

    question = question.lower()


    memories = []


    # Device questions
    if any(word in question for word in [
        "laptop",
        "computer",
        "pc",
        "gpu",
        "ram",
        "phone"
    ]):

        memories = get_memories_by_category("device")



    # Preference questions
    elif any(word in question for word in [
        "game",
        "games",
        "like",
        "favorite",
        "prefer",
        "hate"
    ]):

        memories = get_memories_by_category("preference")



    # Project questions
    elif any(word in question for word in [
        "project",
        "building",
        "working on"
    ]):

        memories = get_memories_by_category("project")



    # Identity questions
    elif "name" in question:

        memories = get_memories_by_category("identity")



    # Emotional questions
    elif any(word in question for word in [
        "love",
        "relationship",
        "family",
        "friend"
    ]):

        memories = get_memories_by_category("emotional")



    else:

        return None



    if not memories:

        return None



    return memories