from src.contracts.language_understanding import (
    LanguageUnderstanding,
)


# =====================================================
# MODEL ROUTING TABLE
#
# Maps Understanding category → model to use for
# the final response generation call.
#
# Rules:
# - Category comes from Understanding LLM output.
# - This is a pure Python dict lookup. No LLM call.
# - Falls back to DEFAULT_MODEL on unknown category.
# - Add new models here as you pull them with ollama.
#
# To add a model:
#   ollama pull <model-name>
#   Add the category → model entry below.
# =====================================================

CATEGORY_MODEL_MAP = {

    # Fast small model — trivial social interaction
    "social":      {"model": "llama3.2:3b"},

    # Default capable model — general conversation
    "general":     {"model": "llama3.2:3b"},
    "preference":  {"model": "llama3.2:3b"},
    "gaming":      {"model": "llama3.2:3b"},
    "food":        {"model": "llama3.2:3b"},
    "memory":      {"model": "llama3.2:3b"},
    "emotional":   {"model": "llama3.2:3b"},
    "identity":    {"model": "llama3.2:3b"},

    # Larger capable model — reasoning-heavy tasks
    "science":     {"model": "llama3.2:3b"},
    "planning":    {"model": "llama3.2:3b"},
    "hardware":    {"model": "llama3.2:3b"},
    "project":     {"model": "llama3.2:3b"},

    # Specialized coding model
    "programming": {"model": "llama3.2:3b"},

}

# Fallback when category is unknown or missing.
DEFAULT_MODEL = {"model": "llama3.2:3b"}


def select_model(understanding: LanguageUnderstanding) -> dict:
    """
    Returns the model config for this understanding.

    Pure lookup — no LLM call, no network, no side effects.
    Called from brain.py between prompt building and generation.

    Returns a dict with at minimum a "model" key.
    Provider always stays "ollama" for now.
    """

    if understanding is None:
        return DEFAULT_MODEL

    category = (
        understanding.semantic.category or ""
    ).lower().strip()

    selected = CATEGORY_MODEL_MAP.get(category, DEFAULT_MODEL)

    print(
        f"MODEL ROUTER: category='{category}' "
        f"-> model='{selected['model']}'"
    )

    return selected