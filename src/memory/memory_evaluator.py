from src.memory.memory_fact import PERSISTENCE_CLASSES


# Durability of each persistence class. This is an enum table, not a
# keyword matcher — it maps the LLM's structured proposal to a numeric
# weight. "unknown" is not the same as transient: an unclassified fact
# may still be stored when its confidence is high enough.
DURABILITY = {
    "permanent": 1.0,
    "temporal":  0.7,
    "transient": 0.1,
    "unknown":   0.5,
}

STORE_THRESHOLD = 0.30


def _as_float(value):
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def evaluate_memory(
    text,
    persistence_class="unknown",
    memory_confidence=None,
    stt_confidence=None,
):
    """
    Decides whether a canonical fact is durable enough to store.

    Durability comes from the persistence class proposed by the
    Understanding LLM and validated by the classifier. Confidence
    comes from the Understanding LLM (and optional STT stage).

    The confidence components are combined as the MEAN of the values
    that actually fired, not their minimum. A minimum lets a single
    weak component veto a fact every other signal supports (an STT
    stage with no audio to score reports a low value and would sink
    a fully-confident permanent fact). A mean keeps the gate honest
    while letting corroborating signals compensate.

    Deterministic structural guards below are fail-safe backstops
    only — they reject obviously broken payloads (empty, questions,
    fragments). They never decide meaning from keywords.

    Returns:
        {"should_remember": bool, "confidence": int (0-100)}
    """
    text = (text or "").strip()

    result = {
        "should_remember": False,
        "confidence": 0,
    }

    # ----- fail-safe structural guards -----
    if not text:
        return result

    lowered = text.lower()

    if lowered.endswith("?"):
        return result

    # A two-word fragment carries no durable meaning on its own.
    if len(text.split()) <= 2:
        return result

    if not text.endswith((".", "!", "")) and len(text.split()) < 4:
        return result

    # ----- durability -----
    cls = (persistence_class or "unknown").lower()
    if cls not in PERSISTENCE_CLASSES:
        cls = "unknown"

    durability = DURABILITY.get(cls, DURABILITY["unknown"])

    mem_conf = _as_float(memory_confidence)
    stt_conf = _as_float(stt_confidence)

    components = [
        value for value in (mem_conf, stt_conf) if value is not None
    ]

    if components:
        combined = durability * (
            sum(components) / len(components)
        )
    else:
        combined = durability

    result["confidence"] = int(combined * 100)

    result["should_remember"] = (
        combined >= STORE_THRESHOLD
    )

    return result
