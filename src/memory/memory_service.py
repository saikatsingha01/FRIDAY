from src.memory.memory_manager import (
    remember,
)


class MemoryService:

    """
    Handles explicit memory operations.

    This will later handle:

    - remember
    - forget
    - memory recall
    - memory updates
    - conflict resolution
    """

    def remember(self, text: str):

        return remember(text)


memory_service = MemoryService()