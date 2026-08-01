"""
memory_updater.py

Responsible for deciding whether a new memory should
replace an existing one or be inserted as a new memory.
"""

from copy import deepcopy


# ---------------------------------------------
# Unique attributes
# Only one of these should exist.
# ---------------------------------------------

UNIQUE_ATTRIBUTES = {

    "name",

    "favorite_game",

    "favorite_movie",

    "laptop",

    "computer",

    "pc",

    "phone",

    "current_project"

}


# ---------------------------------------------
# Update memory list
# ---------------------------------------------

def update_existing_memory(memories, new_memory):

    """
    Returns:

    updated, memories
    """

    memories = deepcopy(memories)

    attribute = new_memory.get("attribute")

    if attribute in UNIQUE_ATTRIBUTES:

        for index, memory in enumerate(memories):

            if memory.get("attribute") == attribute:

                memories[index] = new_memory

                return True, memories

    return False, memories


# ---------------------------------------------
# Duplicate detection
# ---------------------------------------------

def is_duplicate(memories, new_memory):

    for memory in memories:

        if (

            memory.get("attribute") == new_memory.get("attribute")

            and

            str(memory.get("value")).lower()

            ==

            str(new_memory.get("value")).lower()

        ):

            return True

    return False


# ---------------------------------------------
# Add new memory
# ---------------------------------------------

def add_memory(memories, new_memory):

    memories = deepcopy(memories)

    memories.append(new_memory)

    return memories


# ---------------------------------------------
# Save helper
# ---------------------------------------------

def apply_memory_update(memories, new_memory):

    """
    Master function.

    Returns

    updated_memories,
    action

    action =

    "duplicate"

    "updated"

    "added"
    """

    if is_duplicate(memories, new_memory):

        return memories, "duplicate"

    updated, memories = update_existing_memory(

        memories,

        new_memory

    )

    if updated:

        return memories, "updated"

    memories = add_memory(

        memories,

        new_memory

    )

    return memories, "added"