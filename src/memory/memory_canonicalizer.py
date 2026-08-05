from src.memory.knowledge_normalizer import normalize_fact
from src.memory.memory_fact import MemoryFact


class MemoryCanonicalizer:
    """
    Canonicalization stage of the memory pipeline.

    The Understanding LLM is the authority on meaning. This stage
    only does deterministic text hygiene and never rewrites meaning:

      - Preserves the original user message in source_text
        (provenance only — never used for understanding).
      - Produces a normalized comparison form (separator variants,
        case, whitespace collapsed) used for duplicate detection
        and subject matching.
      - Records canonicalization_confidence (Issue 12).

    It is fail-open: if anything here fails, the fact passes through
    unchanged with a neutral confidence. It never gates on keywords.
    """

    def canonicalize(self, fact: MemoryFact) -> MemoryFact:
        if fact is None:
            return None

        if not fact.canonical_fact or not fact.canonical_fact.strip():
            fact.canonicalization_confidence = 0.0
            return fact

        text = fact.canonical_fact.strip()

        comparison = normalize_fact(text)

        if not comparison:
            fact.canonicalization_confidence = 0.0
            return fact

        # The stored text is the LLM's canonical sentence. Only
        # whitespace around the edges is cleaned.
        fact.canonical_fact = " ".join(text.split())
        fact.canonicalization_confidence = 1.0

        return fact


memory_canonicalizer = MemoryCanonicalizer()
