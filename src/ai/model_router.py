from dataclasses import dataclass, field
from typing import Optional, Dict, Any

from src.contracts.capability import (
    CapabilityCategory,
    CAPABILITY_CATEGORIES,
)

from src.contracts.language_understanding import (
    LanguageUnderstanding,
)


# =====================================================
# MODEL ROLES
#
# Logical roles — physical model names are known only to
# ROLE_MODEL_MAP (configuration). No other module in the
# project references a physical model name.
#
# Future roles (VISION, AUDIO, LARGE_REASONING,
# MULTIMODAL) are added here when their models exist.
# =====================================================

class ModelRole:

    FAST_CHAT    = "FAST_CHAT"
    DEFAULT_CHAT = "DEFAULT_CHAT"
    REASONING    = "REASONING"
    CODING       = "CODING"


MODEL_ROLES = frozenset({
    ModelRole.FAST_CHAT,
    ModelRole.DEFAULT_CHAT,
    ModelRole.REASONING,
    ModelRole.CODING,
})


# =====================================================
# ROLE -> PHYSICAL MODEL CONFIGURATION
#
# The ONLY place physical model names live. Everything
# else routes through roles. Pull a new model with
# `ollama pull <model>` and add the role -> model entry
# here — no other file changes.
# =====================================================

ROLE_MODEL_MAP = {
    ModelRole.FAST_CHAT:    "llama3.2:1b",
    ModelRole.DEFAULT_CHAT: "llama3.2:3b",
    ModelRole.REASONING:    "llama3.1:8b",
    ModelRole.CODING:       "qwen2.5-coder:7b",
}


# =====================================================
# ROUTING TABLE — Capability Category -> Model Role
#
# Deterministic dictionary lookup. No LLM call.
# No keyword matching. No semantic understanding.
# Replaceable without touching the Brain.
# =====================================================

CATEGORY_ROLE_MAP = {
    CapabilityCategory.SOCIAL:        ModelRole.FAST_CHAT,
    CapabilityCategory.GENERAL:       ModelRole.DEFAULT_CHAT,
    CapabilityCategory.KNOWLEDGE:     ModelRole.DEFAULT_CHAT,
    CapabilityCategory.WRITING:       ModelRole.DEFAULT_CHAT,
    CapabilityCategory.CREATIVE:      ModelRole.DEFAULT_CHAT,
    CapabilityCategory.TRANSLATION:   ModelRole.DEFAULT_CHAT,
    CapabilityCategory.SUMMARIZATION: ModelRole.DEFAULT_CHAT,
    CapabilityCategory.MEMORY:        ModelRole.DEFAULT_CHAT,
    CapabilityCategory.WEB:           ModelRole.DEFAULT_CHAT,
    CapabilityCategory.TOOL_USE:      ModelRole.DEFAULT_CHAT,
    # Vision/audio currently temporary until a dedicated
    # vision / audio model exists.
    CapabilityCategory.VISION:        ModelRole.DEFAULT_CHAT,
    CapabilityCategory.AUDIO:         ModelRole.DEFAULT_CHAT,
    # Device actions (app launches) produce a real side effect the user
    # must hear confirmed. The 1b FAST_CHAT model answers launch
    # confirmations with a canned greeting instead of naming the
    # launched app, so device turns use the default chat model.
    CapabilityCategory.DEVICE:        ModelRole.DEFAULT_CHAT,
    CapabilityCategory.AUTOMATION:    ModelRole.DEFAULT_CHAT,
    CapabilityCategory.SECURITY:      ModelRole.FAST_CHAT,
    CapabilityCategory.SYSTEM:        ModelRole.FAST_CHAT,
    CapabilityCategory.REASONING:     ModelRole.REASONING,
    CapabilityCategory.SCIENCE:       ModelRole.REASONING,
    CapabilityCategory.MATHEMATICS:   ModelRole.REASONING,
    CapabilityCategory.PLANNING:      ModelRole.REASONING,
    CapabilityCategory.LEARNING:      ModelRole.REASONING,
    CapabilityCategory.PROGRAMMING:   ModelRole.CODING,
}


# =====================================================
# FALLBACK
#
# None / invalid / unknown / malformed / empty category
# routes to GENERAL -> DEFAULT_CHAT. The router never
# crashes — worst case is a default model.
# =====================================================

FALLBACK_CATEGORY = CapabilityCategory.GENERAL
FALLBACK_ROLE     = ModelRole.DEFAULT_CHAT


# =====================================================
# ROUTING DECISION
#
# The router's only output. Future fields (temperature,
# max_tokens, latency, complexity, confidence,
# gpu_requirement, historical_success) are added as
# optional dataclass fields — the public route() API
# never changes.
# =====================================================

@dataclass
class RoutingDecision:

    model: str
    role: str
    category: Optional[str]
    reason: str
    fallback: bool

    extra: Dict[str, Any] = field(default_factory=dict)


# =====================================================
# LOOKUP HELPERS
# =====================================================

def _normalize(capability) -> Optional[str]:
    """
    Standardizes the capability input. Anything that is
    not a non-empty string (None, numbers, lists, junk)
    normalizes to None, which triggers the fallback.
    """
    if not isinstance(capability, str):
        return None

    normalized = capability.strip().lower()

    if not normalized:
        return None

    return normalized


def _model_for_role(role: str) -> Optional[str]:
    """
    Returns the physical model for a role. Falls back to
    the fallback role's model when a role has no model
    configured, so a config gap can never crash the router.
    """
    model = ROLE_MODEL_MAP.get(role)

    if model:
        return model

    return ROLE_MODEL_MAP.get(FALLBACK_ROLE)


def _log(decision: RoutingDecision) -> None:
    """
    Logs every routing decision in a fixed, parseable
    block. This is the router's only side effect.
    """
    print("\n========== MODEL ROUTER ==========")
    print(f"Category:\n{decision.category or ''}")
    print(f"Role:\n{decision.role}")
    print(f"Model:\n{decision.model}")
    print(f"Reason:\n{decision.reason}")
    print(f"Fallback:\n{decision.fallback}")
    print("==================================\n")


# =====================================================
# ROUTE
#
# Capability Category
#      ↓
# Dictionary Lookup
#      ↓
# RoutingDecision
#
# Nothing else. No reasoning. No inference.
# No classification. No LLM. No keywords.
# =====================================================

def route(capability=None) -> RoutingDecision:
    """
    Routes a capability category to a RoutingDecision.

    Deterministic lookup. Unknown / None / invalid values
    fall back to GENERAL -> DEFAULT_CHAT.
    """

    normalized = _normalize(capability)

    role = CATEGORY_ROLE_MAP.get(normalized)

    if role is None:

        decision = RoutingDecision(
            model=_model_for_role(FALLBACK_ROLE),
            role=FALLBACK_ROLE,
            category=FALLBACK_CATEGORY,
            reason=(
                f"Unknown category '{capability}', "
                f"falling back to {FALLBACK_CATEGORY}"
            ),
            fallback=True,
        )

    else:

        decision = RoutingDecision(
            model=_model_for_role(role),
            role=role,
            category=normalized,
            reason="Category Lookup",
            fallback=False,
        )

    _log(decision)

    return decision


# =====================================================
# BACKWARD-COMPATIBLE WRAPPER
#
# The previous API returned {"model": ...} for an
# understanding object. Kept so any external caller or
# script that still uses select_model keeps working.
# The Brain calls route() directly.
# =====================================================

def select_model(understanding: LanguageUnderstanding) -> dict:
    """
    Legacy wrapper. Returns {"model": ...} for the
    capability the Understanding layer assigned to the
    message. Missing capability -> fallback model.
    """

    if understanding is None:
        return {"model": route(None).model}

    return {
        "model": route(
            understanding.semantic.capability
        ).model
    }
