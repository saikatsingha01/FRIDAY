from src.memory.memory_fact import (
    MemoryFact,
    PERSISTENCE_CLASSES,
)


# The LLM sometimes uses "temporary" (plain English) for what the
# pipeline calls "transient". It is an explicit low-durability signal,
# so alias it to the enum it describes instead of degrading it to
# "unknown" (which would make a confidently-worded transient remark
# look durable enough to store).
PERSISTENCE_ALIASES = {
    "temporary": "transient",
}


VALID_CATEGORIES = {
    "preference",
    "programming",
    "hardware",
    "gaming",
    "food",
    "identity",
    "project",
    "science",
    "education",
    "planning",
    "memory",
    "social",
    "general",
}


class MemoryClassifier:
    """
    Classification stage of the memory pipeline.

    The Understanding LLM proposes persistence_class, category and
    tags. This stage validates those proposals against fixed enums
    and sanitizes the payload. It NEVER classifies meaning from
    keywords — it only checks that a structured proposal is legal.

    Persistence (Issue 2): unknown degrades to transient downstream,
    so an unclassified fact is never silently stored.
    """

    def classify(self, fact: MemoryFact) -> MemoryFact:
        if fact is None:
            return None

        # ---------- persistence ----------
        proposed = (fact.persistence_class or "unknown").lower()
        proposed = PERSISTENCE_ALIASES.get(proposed, proposed)
        if proposed not in PERSISTENCE_CLASSES:
            proposed = "unknown"
        # When the Understanding model provided NO persistence class
        # (None), it is an omission, not a considered "unknown". The
        # prompt's own default for a clear personal statement is
        # "temporal" ("current preferences"), so an absent class
        # follows that default instead of degrading to the much
        # stricter "unknown" (durability 0.5). An EXPLICIT "unknown"
        # stays unknown — that is the conservative signal.
        if fact.persistence_class is None:
            proposed = "temporal"
        fact.persistence_class = proposed

        # ---------- category ----------
        proposed_category = (fact.category or "general").lower()
        fact.category = (
            proposed_category
            if proposed_category in VALID_CATEGORIES
            else "general"
        )

        # ---------- tags ----------
        tags = []
        for tag in fact.tags or []:
            if isinstance(tag, str):
                cleaned = " ".join(tag.lower().split())
                if cleaned and cleaned not in tags:
                    tags.append(cleaned)
            if len(tags) >= 5:
                break
        fact.tags = tags

        return fact


memory_classifier = MemoryClassifier()
