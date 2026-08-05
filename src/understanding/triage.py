import math
from src.ai.llm_interface import llm


# =====================================================
# TRIAGE CATEGORIES
#
# Each category has a set of short exemplar phrases.
# The triage computes cosine similarity between the
# user's message embedding and each exemplar embedding.
#
# If similarity exceeds THRESHOLD, the message is
# classified as trivial and the full LLM Understanding
# call is skipped.
#
# Exemplars are embedded once at startup and cached.
# They are never sent to the generative model.
# =====================================================

EXEMPLARS = {

    "greeting": [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good evening",
        "good afternoon",
        "hey there",
        "hi friday",
        "hello friday",
        "howdy",
    ],

    "farewell": [
        "goodbye",
        "bye",
        "see you later",
        "talk to you soon",
        "take care",
        "good night",
        "catch you later",
        "see ya",
    ],

    "gratitude": [
        "thank you",
        "thanks",
        "thank you so much",
        "thanks a lot",
        "appreciate it",
        "cheers",
        "many thanks",
    ],

    "affirmation": [
        "yes",
        "yeah",
        "yep",
        "sure",
        "okay",
        "ok",
        "alright",
        "sounds good",
        "got it",
        "understood",
        "exactly",
        "correct",
        "right",
    ],

    "small_talk": [
        "how are you",
        "how are you doing",
        "what is up",
        "whats up",
        "how is it going",
        "hows it going",
        "nice to meet you",
        "how do you feel",
        "are you okay",
    ],

}

# Similarity threshold.
# Higher = stricter = fewer false positives.
# A false positive here means a real request gets
# treated as small talk — that is the costly error.
# False negatives (greeting goes to full pipeline)
# just cost one extra LLM call — acceptable.
THRESHOLD = 0.85

# Cache — computed once, reused every call.
_exemplar_vectors: dict = {}
_cache_ready: bool = False


# =====================================================
# MATH
# =====================================================

def _cosine(a, b):

    dot    = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)


# =====================================================
# CACHE LOADER
# =====================================================

def _load_exemplar_cache():
    """
    Embeds all exemplar phrases once and caches them.
    Called lazily on first triage request.
    """

    global _exemplar_vectors, _cache_ready

    if _cache_ready:
        return

    provider = llm.get_provider()

    if not hasattr(provider, "embed"):
        _cache_ready = True
        return

    print("TRIAGE: Building exemplar cache...")

    for category, phrases in EXEMPLARS.items():

        vectors = []

        for phrase in phrases:

            vec = provider.embed(phrase)

            if vec is not None:
                vectors.append(vec)

        _exemplar_vectors[category] = vectors

    _cache_ready = True

    print("TRIAGE: Cache ready.")


# =====================================================
# MAIN TRIAGE FUNCTION
# =====================================================

def classify_trivial(user_message: str):
    """
    Returns a category string if the message is
    confidently trivial social interaction.
    Returns None if the message needs full Understanding.

    Called from understanding_orchestrator.analyze()
    as the very first step — before any LLM call.

    Never raises — on any error, returns None so the
    full pipeline runs as normal fallback.
    """

    try:

        _load_exemplar_cache()

        provider = llm.get_provider()

        if not hasattr(provider, "embed"):
            return None

        if not _exemplar_vectors:
            return None

        vec = provider.embed(user_message.lower().strip())

        if vec is None:
            return None

        best_category = None
        best_score    = 0.0

        for category, vectors in _exemplar_vectors.items():

            for ex_vec in vectors:

                score = _cosine(vec, ex_vec)

                if score > best_score:
                    best_score    = score
                    best_category = category

        if best_score >= THRESHOLD:

            print(
                f"TRIAGE: '{user_message}' -> "
                f"{best_category} ({best_score:.3f})"
            )

            return best_category

        return None

    except Exception as error:

        print("TRIAGE ERROR:", error)

        return None