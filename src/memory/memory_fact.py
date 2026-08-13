from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


# A canonical fact whose meaning could not be confirmed
# is never written to long-term memory. Below this
# confidence the fact is considered unconfirmed.
UNCERTAINTY_THRESHOLD = 0.5

# When the model explicitly flagged NO uncertain term, its raw
# confidence is treated as noise: clear casual facts ("my favorite
# drink is frappe") are regularly scored 0.3-1.0 depending on how
# common the value word feels, with no actual ambiguity present.
# Only a very low floor acts as a tripwire for broken output.
LOW_CONFIDENCE_FLOOR = 0.2

WRITE_OPERATIONS = ("store", "update", "forget")

# Persistence classes the classifier understands.
PERSISTENCE_CLASSES = (
    "permanent",
    "temporal",
    "transient",
    "unknown",
)

# A single place that names every confidence component.
CONFIDENCE_SOURCES = (
    "stt",
    "understanding",
    "canonicalization",
    "memory",
    "retrieval",
)


@dataclass
class MemoryFact:
    """
    A structured memory write/update instruction.

    Owned by the Memory layer. Built by the Understanding
    layer from the LLM output. Passed to MemoryDecision.

    Never carries raw user text. Only what the LLM
    confidently extracted as a durable canonical fact.

    Fields:
        operation             — "store" | "update" | "query" | "forget" | None
        canonical_fact        — clean durable sentence, or None
        uncertain_terms       — terms the LLM could not confidently interpret
        confidence            — 0.0 .. 1.0 overall (compatibility + write gate)
        source_text           — original user message (provenance only; never
                                used by the Memory layer for understanding)
        persistence_class     — permanent | temporal | transient | unknown
        category              — category the LLM proposed (validated downstream)
        tags                  — retrieval tags proposed by the LLM
        created_at/updated_at — ISO timestamps (recency/conflict rules)
        *_confidence          — independent per-stage confidences (Issue 12)
    """

    operation: Optional[str] = None

    canonical_fact: Optional[str] = None

    uncertain_terms: List[str] = field(
        default_factory=list
    )

    confidence: float = 0.0

    source_text: Optional[str] = None

    persistence_class: Optional[str] = None

    category: Optional[str] = None

    tags: List[str] = field(default_factory=list)

    created_at: Optional[str] = None

    updated_at: Optional[str] = None

    # Independent confidence components. None means the
    # stage did not produce a value (treated as 1.0 when
    # the gate is combined).
    stt_confidence: Optional[float] = None
    understanding_confidence: Optional[float] = None
    canonicalization_confidence: Optional[float] = None
    memory_confidence: Optional[float] = None
    retrieval_confidence: Optional[float] = None

    # ==========================================
    # PREDICATES
    # ==========================================

    def is_write(self) -> bool:
        return self.operation in WRITE_OPERATIONS

    def is_uncertain(self) -> bool:
        """
        True when the extraction cannot be trusted, so the fact
        is never written.

        A two-signal gate with asymmetric bars:

          * When the model explicitly listed an ``uncertain_terms``
            entry, it is only a block when corroborated by confidence
            below UNCERTAINTY_THRESHOLD. A term listed with high
            confidence is a mis-flagged extraction, not a real
            ambiguity — the small model sometimes hedges a perfectly
            ordinary word ("smoothie") while confident.
          * When NO term was flagged, the model has contractually
            declared the message fully understood. Its raw confidence
            is then noisy (0.3-1.0 for equally clear facts), so only
            a very low floor (LOW_CONFIDENCE_FLOOR) blocks broken
            output. Fabricated content is caught upstream by the
            brand-fidelity gate, which adds terms and lowers
            confidence below UNCERTAINTY_THRESHOLD.
        """
        if self.uncertain_terms:
            if self.confidence is None:
                return False
            return self.confidence < UNCERTAINTY_THRESHOLD

        if self.confidence is None:
            return False
        return self.confidence < LOW_CONFIDENCE_FLOOR

    def confidence_breakdown(self) -> Dict[str, float]:
        """
        The full per-stage confidence map (Issue 12).
        Missing stages default to 1.0 so a quiet stage
        never silently blocks a high-quality write.
        """
        return {
            "stt": self.stt_confidence if self.stt_confidence is not None else 1.0,
            "understanding": (
                self.understanding_confidence
                if self.understanding_confidence is not None
                else self.confidence
            ),
            "canonicalization": (
                self.canonicalization_confidence
                if self.canonicalization_confidence is not None
                else 1.0
            ),
            "memory": (
                self.memory_confidence
                if self.memory_confidence is not None
                else self.confidence
            ),
            "retrieval": (
                self.retrieval_confidence
                if self.retrieval_confidence is not None
                else 1.0
            ),
        }

    def gate_confidence(self) -> float:
        """
        Combined gate value used by the write jury.
        A write may proceed only when every stage that
        produced a value clears its own threshold.
        """
        breakdown = self.confidence_breakdown()
        values = [v for v in breakdown.values() if v is not None]
        if not values:
            return 0.0
        return min(values)


def now_iso() -> str:
    return datetime.now().isoformat()
