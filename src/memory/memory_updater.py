def update_existing_memory(memories, new_memory):

    for index, memory in enumerate(memories):

        if memory["category"] == new_memory["category"]:

            memories[index] = new_memory

            return True

    return False