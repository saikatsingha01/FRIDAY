from src.memory.memory_history import add_history
from src.memory.episode_manager import add_episode


COMMON_WORDS = {
    "my", "i", "is", "are", "was", "the", "a", "an",
    "have", "has", "had", "be", "been", "am",
    "favorite", "favourite", "like", "love", "enjoy",
    "use", "used", "using", "do", "does", "did",
    "and", "or", "but", "in", "on", "at", "to",
    "for", "of", "with", "that", "this", "it"
}


class MemoryConflictResolver:

    REPLACEABLE_CATEGORIES = [
        "preference",
        "device",
        "identity"
    ]

    def check_conflict(self, existing_memories, new_memory):

        conflicts = []

        category = new_memory.get("category")

        if category not in self.REPLACEABLE_CATEGORIES:
            return conflicts

        for memory in existing_memories:

            if memory.get("category") != category:
                continue

            if self.is_related(
                memory["text"],
                new_memory["text"]
            ):
                conflicts.append(memory)

        return conflicts

    def is_related(self, old_text, new_text):

        old_words = {
            w for w in old_text.lower().split()
            if w not in COMMON_WORDS and len(w) > 2
        }

        new_words = {
            w for w in new_text.lower().split()
            if w not in COMMON_WORDS and len(w) > 2
        }

        if not old_words or not new_words:
            return False

        common = old_words.intersection(new_words)

        return len(common) >= 1

    def resolve(self, memories, conflicts, new_memory):

        for old_memory in conflicts:

            # ----------------------------------------
            # 1. Archive to memory_history.json
            #    (preserves raw old/new pair)
            # ----------------------------------------

            add_history(old_memory, new_memory)

            # ----------------------------------------
            # 2. Write an episode to episodes.json
            #    so episode_retriever can surface it
            #    when the user asks "what was before".
            #
            #    Extract meaningful keywords from the
            #    old memory text for retrieval scoring.
            # ----------------------------------------

            old_text = old_memory.get("text", "")
            new_text = new_memory.get("text", "")

            keywords = [
                w for w in old_text.lower().split()
                if w not in COMMON_WORDS and len(w) > 2
            ] + [
                w for w in new_text.lower().split()
                if w not in COMMON_WORDS and len(w) > 2
            ]

            # Summary written as a natural statement
            # so the LLM can read it directly in the prompt.
            summary = (
                f"Previously: {old_text}. "
                f"This was updated to: {new_text}."
            )

            add_episode(
                summary=summary,
                keywords=list(set(keywords)),
                importance=old_memory.get("importance", 5)
            )

            # ----------------------------------------
            # 3. Remove old memory from active store
            # ----------------------------------------

            memories.remove(old_memory)

        memories.append(new_memory)

        return memories


memory_conflict_resolver = MemoryConflictResolver()