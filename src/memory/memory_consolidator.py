class MemoryConsolidator:
    """
    Converts multiple memories about the same topic
    into one structured knowledge object.

    This is the first step toward a Knowledge Graph.

    Future:
    - LLM-based consolidation
    - Entity linking
    - Relationship extraction
    - Knowledge graph generation
    """


    def consolidate(self, memories):

        consolidated = {}

        for memory in memories:

            category = memory.get(
                "category",
                "general"
            )

            if category not in consolidated:

                consolidated[category] = []


            consolidated[category].append(

                memory["text"]

            )


        return consolidated



    def summarize_category(

        self,

        memories,

        category

    ):

        return [

            memory["text"]

            for memory in memories

            if memory.get("category") == category

        ]



memory_consolidator = MemoryConsolidator()