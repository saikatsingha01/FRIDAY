from src.memory.memory_fact import MemoryFact, UNCERTAINTY_THRESHOLD
from src.memory.memory_canonicalizer import memory_canonicalizer
from src.memory.memory_validator import memory_validator
from src.memory.memory_classifier import memory_classifier
from src.memory.memory_evaluator import evaluate_memory
from src.memory.memory_manager import store_fact, delete_fact


class MemoryDecision:

    """
    The Memory write jury.

    Receives a structured MemoryFact from the Understanding layer
    and runs it through the memory pipeline:

        Memory Intent Detector (Understanding LLM, already done)
        → Fact Extractor (Understanding LLM, already done)
        → Canonicalizer
        → Memory Validator
        → Memory Classifier
        → Conflict Resolver
        → Memory Store

    This class NEVER parses natural language and NEVER makes meaning
    decisions from keywords. It applies deterministic gates to the
    LLM's structured proposal.

    Returns a status string, never English dialogue:
        "stored"              — new fact written
        "updated"             — existing fact replaced (change surfaced)
        "needs_clarification" — a term could not be trusted
        "needs_confirmation"  — a conflicting/anomalous value, ask user
        "ignored"             — valid but not durable (transient/unknown)
        None                  — no write operation happened

    The last event (old/new record, status) is kept on
    memory_decision.last_event so brain.py can surface a change in
    the reply ("I've updated that from X to Y").
    """

    def __init__(self):
        self.last_event = None

    def process(self, fact: MemoryFact):

        self.last_event = None

        if fact is None:
            return None

        if not fact.is_write():
            return None

        if not fact.canonical_fact or not fact.canonical_fact.strip():
            return None

        # ----------------------------------------
        # UNCONFIRMED FACT
        # A mishearing or typo would be baked into long-term memory.
        # Ask the user to clarify instead. The forget path is exempt:
        # DELETE never writes new meaning, it only removes a fact
        # already confirmed in the store, so value-level uncertainty
        # cannot corrupt anything (a miss simply means "nothing to
        # delete"). Only the delete-path structural gates apply.
        # ----------------------------------------

        if fact.operation == "forget":
            return self._process_delete(fact)

        if fact.is_uncertain():
            return "needs_clarification"

        # ----------------------------------------
        # TRUST NORMALIZATION
        # A fact that cleared the uncertainty gate WITHOUT any flagged
        # terms is the pipeline's "clear statement": the gate has
        # decided the extraction is trusted, and the Understanding
        # model's raw confidence is noisy (0.3-1.0 for equally clear
        # facts). That trust decision is now authoritative for every
        # downstream consumer — the evaluator, the stored record and
        # the conflict resolver all read the same floored value — so
        # the noisy raw number cannot veto the write a second time.
        # Facts carrying flagged uncertain terms keep their raw
        # confidence: for them confidence remains an active signal.
        # ----------------------------------------

        if (
            not fact.uncertain_terms
            and fact.confidence is not None
            and fact.confidence < UNCERTAINTY_THRESHOLD
        ):
            fact.confidence = UNCERTAINTY_THRESHOLD

        # ----------------------------------------
        # DELETE
        # A first-class memory operation, symmetric with
        # STORE/UPDATE. The canonical_fact is the delete
        # target; it is matched against the store with the
        # same subject machinery UPDATE uses. Durability is
        # irrelevant to an explicit deletion, so the
        # evaluator is skipped.
        # ----------------------------------------

        # ----------------------------------------
        # CANONICALIZER
        # ----------------------------------------

        fact = memory_canonicalizer.canonicalize(fact)

        if fact.canonical_fact is None:
            return None

        # ----------------------------------------
        # MEMORY VALIDATOR — structural gate
        # ----------------------------------------

        validation = memory_validator.validate(fact.canonical_fact)

        if not validation["valid"]:
            self.last_event = {
                "status": "ignored",
                "reason": validation.get("reason", "invalid"),
            }
            return "ignored"

        # ----------------------------------------
        # MEMORY CLASSIFIER — persistence + category
        # ----------------------------------------

        fact = memory_classifier.classify(fact)

        # ----------------------------------------
        # MEMORY EVALUATOR — durability gate
        # Transient/unknown facts are never stored (Issue 2/11).
        #
        # For a fact that cleared the uncertainty gate WITHOUT any
        # flagged terms, the gate has already decided the extraction
        # is trusted. The same noisy confidence must not veto the fact
        # a second time here, so it is floored at the trust bar. Facts
        # carrying flagged uncertain terms keep their raw confidence —
        # for them confidence is still an active durability signal.
        # ----------------------------------------

        conf = (
            fact.understanding_confidence
            if fact.understanding_confidence is not None
            else fact.confidence
        )

        # A gate-cleared fact is the pipeline's "clear statement" —
        # is_uncertain() already removed any genuinely-uncertain
        # extraction before this point. The prompt rule for clear
        # personal statements is "Never default to unknown", so an
        # unclassified fact that passed the gate follows the prompt's
        # temporal default instead of being vetoed by a durability it
        # never proposed. An EXPLICIT transient/promoted class is
        # untouched (transient stays a veto).
        persistence = fact.persistence_class
        if persistence == "unknown":
            persistence = "temporal"
            fact.persistence_class = persistence

        evaluation = evaluate_memory(
            fact.canonical_fact,
            persistence_class=persistence,
            memory_confidence=conf,
            stt_confidence=fact.stt_confidence,
        )

        if not evaluation["should_remember"]:
            self.last_event = {
                "status": "ignored",
                "reason": "not_durable",
                "persistence_class": fact.persistence_class,
            }
            return "ignored"

        # ----------------------------------------
        # CONFLICT RESOLVER + MEMORY STORE
        # ----------------------------------------

        result = store_fact(fact)

        self.last_event = {
            "status": result["status"],
            "record": result.get("record"),
            "old": result.get("old"),
            "event": result.get("event"),
        }

        if result["status"] == "stored":
            return "stored"

        if result["status"] == "updated":
            return "updated"

        if result["status"] == "needs_confirmation":
            return "needs_confirmation"

        # duplicate or anything else — nothing new to store
        return "ignored"

    def _process_delete(self, fact):
        """
        The DELETE gate path, symmetric with the STORE/UPDATE path:
        canonicalizer → validator → classifier → Memory Store
        (delete_fact). The evaluator is skipped on purpose — an
        explicit deletion is not subject to durability scoring.

        Returns:
            "deleted"   — one or more facts were removed
            "not_found" — nothing in the store matched the target
            "ignored"   — the target is not a valid delete subject
        """
        fact = memory_canonicalizer.canonicalize(fact)

        if not fact.canonical_fact or not fact.canonical_fact.strip():
            return "ignored"

        validation = memory_validator.validate(fact.canonical_fact)

        if not validation["valid"]:
            self.last_event = {
                "status": "ignored",
                "reason": validation.get("reason", "invalid"),
            }
            return "ignored"

        fact = memory_classifier.classify(fact)

        result = delete_fact(fact)

        self.last_event = {
            "status": result["status"],
            "record": result.get("record"),
            "old": result.get("old"),
        }

        return result["status"]


memory_decision = MemoryDecision()


def process_memory(fact: MemoryFact):

    return memory_decision.process(fact)
