import re
from datetime import datetime

from src.memory.memory_fact import UNCERTAINTY_THRESHOLD
from src.memory.memory_history import add_history
from src.memory.episode_manager import add_episode


# Numeric anomaly threshold: if the same numeric fact changes by more
# than this relative amount, FRIDAY asks before overwriting (Issue 15).
ANOMALY_RATIO = 0.10

# Closed preference/frame words that carry no subject identity. Two
# facts sharing ONLY these words ("favorite food is rice" vs
# "favorite game is sekiro") are different subjects; treating the
# overlap as identity would merge unrelated preferences. Structural
# closed-class list — never topic keywords.
GENERIC_SUBJECT_WORDS = frozenset({
    "favorite", "favourite", "like", "likes", "love", "loves",
    "prefer", "prefers", "preferred", "currently", "really",
    "just", "always", "still", "used", "usedto",
})

# Embedding fallback threshold for ambiguous subject matching: when
# lexical overlap is inconclusive, two facts are the same subject
# only if their embeddings agree strongly.
_SAME_SUBJECT_EMBED_THRESHOLD = 0.70

# Small embed cache shared across a process run; embeddings are
# immutable per text so the cache only saves compute, never
# changes behavior.
_same_subject_embed_cache = {}

# Fine-grained LLM categories that map onto the legacy coarse taxonomy
# for conflict purposes. Legacy records ("favorite game", "favorite
# food") were stored as preference; new records use gaming/food. The
# alias only affects conflict/subject matching — it is a structural
# enum mapping, never a meaning decision.
CATEGORY_ALIASES = {
    "gaming":       "preference",
    "food":         "preference",
    "programming":  "project",
    "hardware":     "device",
    "science":      "education",
    "social":       "general",
    "planning":     "general",
    "memory":       "general",
}


# Copulas separating a fact's subject from its value in a
# "favorite X is Y" frame (used by _favorite_attribute).
_COPULAS = (" is ", " are ", " was ", " were ")

# Leading temporal fillers a small model copies into a fact's
# attribute span ("my favorite food NOW is lasagna"); skipped when
# the attribute is extracted. Structural, never topic keywords.
_VALUE_FILLERS = ("now", "currently", "still", "actually")


class MemoryConflictResolver:
    """
    Conflict stage of the memory pipeline.

    Decides whether a new fact replaces an existing one.

    Rules (Issue 14 + 15):
      - Same subject: same category plus a shared subject signal
        (exact text, shared tags, or token overlap). Tag overlap and
        token overlap are fail-open backstops — a miss just means the
        fact is stored alongside instead of replacing.
      - Explicit updates win on recency when the new value carries
        enough confidence (new confidence >= old).
      - A numeric anomaly (same number changed by > ANOMALY_RATIO)
        or a low-confidence new value blocks the write and asks the
        user instead of silently overwriting.
      - Replaced facts are archived to memory_history.json and a
        change episode is written so "what was before" still works.
    """

    def _conflict_category(self, category):
        return CATEGORY_ALIASES.get(
            (category or "").lower().strip(), (category or "").lower().strip()
        )

    def check_conflict(
        self,
        existing_memories,
        new_memory,
        operation="store",
    ):
        conflicts = []

        new_category = self._conflict_category(
            new_memory.get("category")
        )

        for memory in existing_memories:
            old_category = self._conflict_category(
                memory.get("category")
            )
            if (
                old_category != new_category
                and old_category != "general"
                and new_category != "general"
            ):
                continue

            if not self._same_subject(memory, new_memory):
                continue

            conflicts.append(memory)

        return conflicts

    @staticmethod
    def _tokens(text):
        """
        Subject tokens: any number (regardless of length) plus any
        word longer than 2 letters. Numbers always count so numeric
        facts like "70 kg" vs "65 kg" conflict instead of silently
        co-existing as two records.
        """
        tokens = set()
        for word in (text or "").lower().split():
            if word.isdigit() or any(c.isdigit() for c in word):
                tokens.add(word)
            elif len(word) > 2:
                tokens.add(word)
        return tokens

    @staticmethod
    def _favorite_attribute(text):
        """
        The attribute noun of a "favorite X is Y" frame — the span
        between "favorite" and a copula ("my favorite CONDIMENT is
        lobster roll" -> "condiment"). None when the frame is absent.

        Purely positional/structural: two facts sharing the SAME
        attribute in the same frame are the same subject no matter
        how different the values are — the value slot is exactly what
        an update replaces. Leading temporal fillers ("now",
        "currently") inside the span are skipped.
        """
        lowered = (text or "").lower()
        for key in ("favorite", "favourite"):
            idx = lowered.find(key)
            if idx < 0:
                continue
            tail = lowered[idx + len(key):]
            for copula in _COPULAS:
                end = tail.find(copula)
                if end < 0:
                    continue
                attr = tail[:end].strip().split()
                attr = [w for w in attr if w not in _VALUE_FILLERS]
                if attr:
                    return " ".join(attr)
        return None

    def _same_subject(self, memory, new_memory):
        old_text = (memory.get("text") or "").strip().lower()
        new_text = (new_memory.get("text") or "").strip().lower()

        if not old_text or not new_text:
            return False

        if old_text == new_text:
            return True

        old_tags = set(memory.get("tags", []) or [])
        new_tags = set(new_memory.get("tags", []) or [])
        if old_tags and new_tags and (old_tags & new_tags):
            return True

        # Numeric facts (weight, age, height, scores) in the same
        # category are the same subject whenever both carry a number.
        # The anomaly rule below decides whether the change is a real
        # update (70 -> 65) or a likely mishearing (70 -> 700).
        if (
            re.search(r"\d", old_text)
            and re.search(r"\d", new_text)
        ):
            return True

        # Fail-open token overlap backstop. A miss here only means the
        # fact is stored separately — it never gates on keywords.
        # At least two shared tokens are required so a single generic
        # word ("favorite", "like") never merges unrelated subjects
        # like "favorite food" and "favorite game".
        old_tokens = self._tokens(old_text)
        new_tokens = self._tokens(new_text)
        shared = old_tokens & new_tokens

        if len(shared) < 2:
            return False

        # When the shared tokens are all preference/frame words
        # ("favorite food is rice" vs "favorite drink is rice"), the
        # overlap alone is not identity. Embedding similarity decides;
        # it fails open (not the same subject) if no provider exists.
        meaningful = shared - GENERIC_SUBJECT_WORDS
        if len(meaningful) >= 2:
            return True

        # Same "favorite X is Y" frame with the SAME attribute X is
        # the same subject by construction — the attribute defines the
        # slot ("my favorite CONDIMENT is lobster roll" vs "my
        # favorite CONDIMENT is idli" are two values of one slot).
        # Deterministic/structural; no meaning is inferred. This also
        # removes the embedding dependency for updates of the same
        # attribute, so an update cannot silently land as a separate
        # record because two value words happen to embed far apart.
        old_attr = self._favorite_attribute(old_text)
        new_attr = self._favorite_attribute(new_text)
        if old_attr and old_attr == new_attr:
            return True

        return self._embedding_similarity(old_text, new_text)

    @staticmethod
    def _embed_text(text):
        """
        Embedding for a fact text, cached and fail-open (None on any
        error). Used only by the ambiguous-subject fallback.
        """
        cached = _same_subject_embed_cache.get(text)
        if cached is not None:
            return cached
        try:
            from src.memory.episode_retriever import _get_embedding
            vector = _get_embedding(text)
        except Exception:
            vector = None
        _same_subject_embed_cache[text] = vector
        return vector

    def _embedding_similarity(self, old_text, new_text):
        """
        True when the two facts are embedding-similar enough to be
        the same subject. Fail-open: returns False (separate facts)
        when no embedding provider is available or either vector
        fails.
        """
        old_vec = self._embed_text(old_text)
        new_vec = self._embed_text(new_text)
        if old_vec is None or new_vec is None:
            return False
        try:
            from src.memory.episode_retriever import _cosine
            return _cosine(old_vec, new_vec) >= (
                _SAME_SUBJECT_EMBED_THRESHOLD
            )
        except Exception:
            return False

    def _conf_as_float(self, memory):
        confidence = memory.get("confidence", 0) or 0
        try:
            value = float(confidence)
        except (TypeError, ValueError):
            return 0.0
        # Legacy records store 0-100 ints; new records use the same
        # scale (see memory_manager). Normalize anything above 1.
        if value > 1.0:
            value = value / 100.0
        return max(0.0, min(1.0, value))

    @staticmethod
    def _numbers(text):
        return [
            (m.group(), float(m.group()))
            for m in re.finditer(r"\d+(?:\.\d+)?", text)
        ]

    def _numeric_anomaly(self, old_text, new_text):
        """
        True when the same numeric slot changed by more than 10%.
        Numbers at the same index in the two sentences are paired.
        """
        old_nums = self._numbers(old_text)
        new_nums = self._numbers(new_text)

        if not old_nums or not new_nums:
            return False

        pairs = min(len(old_nums), len(new_nums))

        for i in range(pairs):
            _, old_val = old_nums[i]
            _, new_val = new_nums[i]

            base = max(abs(old_val), abs(new_val), 1.0)

            if abs(new_val - old_val) / base > ANOMALY_RATIO:
                return True

        return False

    def resolve(self, memories, conflicts, new_memory, operation="store"):
        """
        Applies conflict decisions.

        Returns:
            (memories, event)
        where event is None when nothing changed, or:
            {"replaced": bool, "anomaly": bool, "old": ..., "new": ...}
        """
        now = datetime.now().isoformat()

        if not conflicts:
            memories.append(new_memory)
            return memories, None

        for old_memory in conflicts:

            old_text = old_memory.get("text", "")
            new_text = new_memory.get("text", "")

            # Duplicate — nothing changes.
            if old_text.strip().lower() == new_text.strip().lower():
                return memories, {
                    "replaced": False,
                    "anomaly": False,
                    "duplicate": True,
                    "old": old_memory,
                    "new": new_memory,
                }

            old_conf = self._conf_as_float(old_memory)
            new_conf = self._conf_as_float(new_memory)

            # A numeric anomaly (e.g. 70 kg -> 700 kg) is never
            # silently applied. A confidence comparison only blocks
            # when the NEW fact is below the trust bar: the uncertainty
            # gate has already adjudicated extraction trust upstream,
            # and gate-cleared facts are normalized to at least
            # UNCERTAINTY_THRESHOLD before they reach the store, so a
            # same-subject fact that passed the gate replaces on
            # recency (the user's current statement wins). Only a
            # genuinely-uncertain new value (one that kept a raw
            # sub-threshold confidence) is held back from overwriting
            # a more-confident stored fact, and the user is asked.
            if self._numeric_anomaly(old_text, new_text) or (
                new_conf < UNCERTAINTY_THRESHOLD
                and new_conf < old_conf
            ):
                return memories, {
                    "replaced": False,
                    "anomaly": self._numeric_anomaly(old_text, new_text),
                    "old": old_memory,
                    "new": new_memory,
                }

            # Recency wins: archive + episode + replace.
            add_history(old_memory, new_memory)

            new_memory["updated_at"] = now
            new_memory["created_at"] = (
                old_memory.get("created_at") or new_memory.get("created_at")
                or now
            )
            new_memory["source_text"] = (
                new_memory.get("source_text")
                or old_memory.get("source_text")
            )

            keywords = self._keywords(old_text) + self._keywords(new_text)
            summary = (
                f"Previously: {old_text}. "
                f"This was updated to: {new_text}."
            )

            add_episode(
                summary=summary,
                keywords=sorted(set(keywords)),
                importance=old_memory.get("importance", 5),
                session_id=old_memory.get("session_id"),
                semantic_ids=[old_memory.get("id")],
            )

            memories.remove(old_memory)
            memories.append(new_memory)

            return memories, {
                "replaced": True,
                "anomaly": False,
                "old": old_memory,
                "new": new_memory,
            }

        return memories, None

    def resolve_delete(self, memories, conflicts, target):
        """
        Applies a DELETE operation to every memory that matched the
        delete target.

        Architecturally symmetric with resolve(): the same archive +
        episode + remove flow, except there is no replacement. Each
        removed memory is archived to memory_history.json with a null
        new_memory (the fact was removed, not replaced) so "what was
        X before" still resolves through the change trail.

        Returns:
            (memories, event)
        where event is None when nothing changed, or:
            {"deleted": bool, "old": [...], "target": {...}}
        """
        if not conflicts:
            return memories, None

        deleted = []

        for old_memory in conflicts:

            old_text = old_memory.get("text", "")

            add_history(old_memory, None)

            keywords = self._keywords(old_text)
            summary = f"{old_text} — this memory was forgotten."

            add_episode(
                summary=summary,
                keywords=sorted(set(keywords)),
                importance=old_memory.get("importance", 5),
                session_id=old_memory.get("session_id"),
                semantic_ids=[old_memory.get("id")],
            )

            memories.remove(old_memory)
            deleted.append(old_memory)

        return memories, {
            "deleted": True,
            "old": deleted,
            "target": target,
        }

    @staticmethod
    def _keywords(text):
        return [
            w for w in (text or "").lower().split()
            if len(w) > 2
        ]


memory_conflict_resolver = MemoryConflictResolver()
