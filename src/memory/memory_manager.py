import json
import os
from datetime import datetime

from src.memory.memory_evaluator import evaluate_memory
from src.memory.memory_validator import memory_validator
from src.memory.memory_conflict_resolver import memory_conflict_resolver
from src.memory.memory_fact import MemoryFact, now_iso


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
# CATEGORY DETECTION — fail-open backstop only.
#
# The Understanding LLM proposes the category. This table is
# used ONLY when no structured proposal exists (legacy text-only
# remember calls). It never drives the primary pipeline.
# =====================================================

def detect_category(fact):

    fact = fact.lower()

    if any(word in fact for word in [
        "study", "studying", "studied",
        "course", "degree", "education", "educational",
        "university", "college", "subject", "major",
        "exam", "school", "semester"
    ]):
        return "education"

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

def calculate_importance(category, persistence_class=None):
    """
    Importance from the category enum (deterministic table) with a
    small durability influence: a permanent fact outranks a temporal
    one of the same category.
    """
    importance_table = {
        "identity":   10,
        "emotional":  10,
        "education":   9,
        "project":     9,
        "device":      8,
        "preference":  7,
        "general":     3
    }

    importance = importance_table.get(category, 3)

    if persistence_class == "temporal":
        importance = max(1, importance - 2)

    if persistence_class == "transient":
        importance = 1

    return importance


# =====================================================
# RECORD BUILDING
# =====================================================

def build_record(fact, memories=None):
    """
    Builds a stored memory record from a structured MemoryFact.

    Confidence is stored on the legacy 0-100 scale so existing
    readers keep working; the 0-1 per-stage breakdown is preserved
    separately for the conflict/retrieval stages (Issue 12).
    """
    memories = memories or load_memory()["memories"]

    now = now_iso()

    category = fact.category or detect_category(
        fact.canonical_fact or ""
    )
    persistence = fact.persistence_class or "unknown"

    record = {
        "id":         next_memory_id(memories),
        "text":       fact.canonical_fact,
        "category":   category,
        "importance": calculate_importance(category, persistence),
        "confidence": int(fact.gate_confidence() * 100),
        "persistence": persistence,
        "tags":       list(fact.tags),
        "source_text": fact.source_text,
        "created_at": fact.created_at or now,
        "updated_at": fact.updated_at or now,
        "confidence_breakdown": fact.confidence_breakdown(),
    }

    return record


# =====================================================
# CORE STORE
# =====================================================

def store_fact(fact):
    """
    Persists a canonical MemoryFact through the Memory Store stage.

    Returns:
        {"status": "stored"|"updated"|"ignored"|"duplicate",
         "record": {...}, "old": {...} or None}

    Never returns dialogue.
    """
    memory = load_memory()
    memories = memory["memories"]

    new_memory = build_record(fact, memories)

    # ----- duplicate -----
    for item in memories:
        if (
            item.get("text", "").strip().lower()
            == new_memory["text"].strip().lower()
        ):
            return {
                "status": "duplicate",
                "record": new_memory,
                "old": item,
            }

    # ----- conflict resolution -----
    conflicts = memory_conflict_resolver.check_conflict(
        memories,
        new_memory,
        operation=fact.operation,
    )

    if conflicts:
        memories, event = memory_conflict_resolver.resolve(
            memories,
            conflicts,
            new_memory,
            operation=fact.operation,
        )

        save_memory({"memories": memories})

        if event and not event.get("replaced"):
            return {
                "status": "needs_confirmation",
                "record": new_memory,
                "old": event.get("old"),
                "event": event,
            }

        return {
            "status": "updated",
            "record": new_memory,
            "old": event.get("old") if event else None,
        }

    memories.append(new_memory)

    save_memory({"memories": memories})

    return {
        "status": "stored",
        "record": new_memory,
        "old": None,
    }


# =====================================================
# CORE DELETE
# =====================================================

def delete_fact(fact):
    """
    Persists a DELETE operation through the Memory Store stage.

    Symmetric with store_fact: the delete target (the canonical_fact
    on the MemoryFact) is matched against the store with the exact
    conflict/subject machinery UPDATE uses, so any future improvement
    to semantic subject matching benefits forgetting automatically.

    Returns:
        {"status": "deleted"|"not_found",
         "record": {...target...}, "old": [...] or None}

    Never returns dialogue.
    """
    memory = load_memory()
    memories = memory["memories"]

    if not memories:
        return {
            "status": "not_found",
            "record": None,
            "old": None,
        }

    target = build_record(fact, memories)

    conflicts = memory_conflict_resolver.check_conflict(
        memories,
        target,
        operation="forget",
    )

    if not conflicts:
        return {
            "status": "not_found",
            "record": target,
            "old": None,
        }

    memories, event = memory_conflict_resolver.resolve_delete(
        memories,
        conflicts,
        target,
    )

    save_memory({"memories": memories})

    return {
        "status": "deleted",
        "record": target,
        "old": event.get("old") if event else None,
    }


# =====================================================
# MANUAL MEMORY (legacy text-only path)
# =====================================================

def remember(
    fact,
    persistence_class="permanent",
    confidence=None,
    stt_confidence=None,
):

    validation = memory_validator.validate(fact)

    if not validation["valid"]:
        return (
            "I don't think this should be stored "
            f"as memory. Reason: {validation['reason']}"
        )

    evaluation = evaluate_memory(
        fact,
        persistence_class=persistence_class,
        memory_confidence=confidence,
        stt_confidence=stt_confidence,
    )

    if not evaluation["should_remember"]:
        return (
            "I don't think this is important "
            "enough to remember."
        )

    memory = load_memory()

    for item in memory["memories"]:
        if item["text"].lower() == fact.lower():
            return "I already remember that."

    fact_obj = MemoryFact(
        operation="store",
        canonical_fact=fact,
        uncertain_terms=[],
        confidence=(
            (confidence / 100.0)
            if confidence is not None and confidence > 1
            else (confidence if confidence is not None else 1.0)
        ),
        source_text=fact,
        persistence_class=persistence_class,
        category=None,
        tags=[],
        created_at=now_iso(),
        updated_at=now_iso(),
        stt_confidence=stt_confidence,
        memory_confidence=(
            (confidence / 100.0)
            if confidence is not None and confidence > 1
            else confidence
        ),
    )

    result = store_fact(fact_obj)

    if result["status"] in ("stored", "updated"):
        return "I will remember that."

    if result["status"] == "needs_confirmation":
        return "I already have a different value for that."

    return "I won't store that."


# =====================================================
# AUTOMATIC MEMORY (used by the write jury)
# =====================================================

def auto_remember(fact, persistence_class="unknown", confidence=None):
    """
    Legacy boolean wrapper. Prefer the pipeline store_fact.
    """
    if not fact:
        return False

    validation = memory_validator.validate(fact)

    if not validation["valid"]:
        return False

    evaluation = evaluate_memory(
        fact,
        persistence_class=persistence_class,
        memory_confidence=confidence,
    )

    if not evaluation["should_remember"]:
        return False

    fact_obj = MemoryFact(
        operation="store",
        canonical_fact=fact,
        uncertain_terms=[],
        confidence=(
            confidence if confidence is not None else 1.0
        ),
        source_text=fact,
        persistence_class=persistence_class,
        category=None,
        tags=[],
        created_at=now_iso(),
        updated_at=now_iso(),
    )

    result = store_fact(fact_obj)

    return result["status"] in ("stored", "updated")


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
