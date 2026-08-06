# ==========================================================
# CAPABILITY CATEGORIES
#
# FRIDAY's capabilities — NOT individual user tasks.
#
# This is the single shared definition of capability
# categories. Every module that reasons about what FRIDAY
# must do references these constants:
#
#   - Understanding layer  (outputs the capability)
#   - Model Router         (routes capability -> model role)
#   - Planner              (goal classification)
#   - Future agents        (agent <-> capability alignment)
#   - Future memory        (capability-aware retrieval)
#   - Future analytics     (per-capability telemetry)
#
# One source of truth so category strings are never
# duplicated across the project.
#
# Capability describes the KIND OF WORK FRIDAY must do for
# a request. It is deliberately broader than the semantic
# category, which describes the TOPIC of the request.
# ==========================================================


class CapabilityCategory:

    SOCIAL        = "social"
    GENERAL       = "general"
    KNOWLEDGE     = "knowledge"
    REASONING     = "reasoning"
    PLANNING      = "planning"
    PROGRAMMING   = "programming"
    MATHEMATICS   = "mathematics"
    SCIENCE       = "science"
    WRITING       = "writing"
    CREATIVE      = "creative"
    TRANSLATION   = "translation"
    SUMMARIZATION = "summarization"
    MEMORY        = "memory"
    VISION        = "vision"
    AUDIO         = "audio"
    WEB           = "web"
    TOOL_USE      = "tool_use"
    DEVICE        = "device"
    AUTOMATION    = "automation"
    LEARNING      = "learning"
    SECURITY      = "security"
    SYSTEM        = "system"


CAPABILITY_CATEGORIES = frozenset({
    CapabilityCategory.SOCIAL,
    CapabilityCategory.GENERAL,
    CapabilityCategory.KNOWLEDGE,
    CapabilityCategory.REASONING,
    CapabilityCategory.PLANNING,
    CapabilityCategory.PROGRAMMING,
    CapabilityCategory.MATHEMATICS,
    CapabilityCategory.SCIENCE,
    CapabilityCategory.WRITING,
    CapabilityCategory.CREATIVE,
    CapabilityCategory.TRANSLATION,
    CapabilityCategory.SUMMARIZATION,
    CapabilityCategory.MEMORY,
    CapabilityCategory.VISION,
    CapabilityCategory.AUDIO,
    CapabilityCategory.WEB,
    CapabilityCategory.TOOL_USE,
    CapabilityCategory.DEVICE,
    CapabilityCategory.AUTOMATION,
    CapabilityCategory.LEARNING,
    CapabilityCategory.SECURITY,
    CapabilityCategory.SYSTEM,
})
