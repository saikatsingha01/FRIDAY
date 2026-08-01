import json
import os

from src.memory.memory_evaluator import evaluate_memory
from src.memory.memory_validator import memory_validator
from src.memory.memory_conflict_resolver import memory_conflict_resolver


MEMORY_FILE = os.path.join(
    os.path.dirname(__file__),
    "memory.json"
)


# =====================================================
# LOAD / SAVE
# =====================================================

def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return {"memories": []}

    with open(
        MEMORY_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def save_memory(memory):

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            memory,
            file,
            indent=4,
            ensure_ascii=False
        )


# =====================================================
# ID GENERATION
# =====================================================

def next_memory_id(memories):
    """
    Always returns max existing ID + 1.
    Safe after conflict resolution removes entries.
    """
    if not memories:
        return 1
    return max(m.get("id", 0) for m in memories) + 1


# =====================================================
# CATEGORY DETECTION
# =====================================================

def detect_category(fact):

    fact = fact.lower()

    if any(word in fact for word in [
        "laptop", "computer", "pc", "phone",
        "gpu", "ram", "rtx", "cpu"
    ]):
        return "device"

    if any(word in fact for word in [
        "favorite", "favourite", "prefer",
        "like", "love", "hate", "enjoy"
    ]):
        return "preference"

    if any(word in fact for word in [
        "project", "building", "working on",
        "developing", "creating"
    ]):
        return "project"

    if any(word in fact for word in [
        "my name", "i am", "i'm", "called"
    ]):
        return "identity"

    if any(word in fact for word in [
        "girlfriend", "family", "friend", "relationship"
    ]):
        return "emotional"

    return "general"


# =====================================================
# IMPORTANCE
# =====================================================

def calculate_importance(category):

    importance_table = {
        "identity":   10,
        "emotional":  10,
        "project":     9,
        "device":      8,
        "preference":  7,
        "general":     3
    }

    return importance_table.get(category, 3)


# =====================================================
# CREATE MEMORY
# =====================================================

def create_memory(fact, confidence=None):

    memory = load_memory()

    category = detect_category(fact)

    new_memory = {
        "id":        next_memory_id(memory["memories"]),
        "text":      fact,
        "category":  category,
        "importance": calculate_importance(category)
    }

    if confidence is not None:
        new_memory["confidence"] = confidence

    # =================================================
    # CONFLICT RESOLUTION
    # =================================================

    conflicts = memory_conflict_resolver.check_conflict(
        memory["memories"],
        new_memory
    )

    if conflicts:

        print("MEMORY CONFLICT:", conflicts)

        memory["memories"] = memory_conflict_resolver.resolve(
            memory["memories"],
            conflicts,
            new_memory
        )

    else:

        memory["memories"].append(new_memory)

    save_memory(memory)

    return new_memory


# =====================================================
# MANUAL MEMORY
# =====================================================

def remember(fact):

    validation = memory_validator.validate(fact)

    if not validation["valid"]:
        return (
            "I don't think this should be stored "
            f"as memory. Reason: {validation['reason']}"
        )

    evaluation = evaluate_memory(fact)

    if not evaluation["should_remember"]:
        return (
            "I don't think this is important "
            "enough to remember."
        )

    memory = load_memory()

    for item in memory["memories"]:
        if item["text"].lower() == fact.lower():
            return "I already remember that."

    create_memory(fact, evaluation["confidence"])

    return "I will remember that."


# =====================================================
# AUTOMATIC MEMORY
# =====================================================

def auto_remember(fact):

    validation = memory_validator.validate(fact)

    if not validation["valid"]:
        return False

    evaluation = evaluate_memory(fact)

    if not evaluation["should_remember"]:
        return False

    memory = load_memory()

    for item in memory["memories"]:
        if item["text"].lower() == fact.lower():
            return False

    create_memory(fact, evaluation["confidence"])

    return True


# =====================================================
# DIRECT SAVE
# =====================================================

def save_memory_direct(fact):
    return remember(fact)


# =====================================================
# READ
# =====================================================

def get_memory():
    return load_memory()


def get_all_memories():
    return load_memory()["memories"]


def get_important_memories():

    memories = load_memory()["memories"]

    return sorted(
        memories,
        key=lambda x: x["importance"],
        reverse=True
    )


def get_memories_by_category(category):

    return [
        item
        for item in load_memory()["memories"]
        if item["category"] == category
    ]


def memory_count():
    return len(load_memory()["memories"])


# =====================================================
# DELETE
# =====================================================

def forget_memory(keyword):

    memory = load_memory()

    old_count = len(memory["memories"])

    memory["memories"] = [
        item
        for item in memory["memories"]
        if keyword.lower() not in item["text"].lower()
    ]

    save_memory(memory)

    if len(memory["memories"]) < old_count:
        return "I forgot that."

    return "I couldn't find that memory."