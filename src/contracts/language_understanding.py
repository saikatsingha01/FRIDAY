from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


# ==========================================================
# ENTITY
# ==========================================================

@dataclass
class Entity:

    text: str
    label: str
    confidence: float = 1.0


# ==========================================================
# TIME
# ==========================================================

@dataclass
class TimeReference:

    type: Optional[str] = None
    value: Optional[str] = None


# ==========================================================
# REQUIRED SYSTEMS
# ==========================================================

@dataclass
class RequiredSystems:

    memory: bool = False
    episodes: bool = False
    context: bool = False

    tools: bool = False
    web: bool = False
    vision: bool = False

    planning: bool = False
    reasoning: bool = True


# ==========================================================
# SEMANTIC UNDERSTANDING
# ==========================================================

@dataclass
class SemanticUnderstanding:

    goal: Optional[str] = None

    intent: Optional[str] = None

    category: Optional[str] = None

    entities: List[Entity] = field(
        default_factory=list
    )

    time_reference: Optional[TimeReference] = None

    confidence: float = 0.0


# ==========================================================
# CONVERSATION UNDERSTANDING
# ==========================================================

@dataclass
class ConversationUnderstanding:

    conversation_state: Optional[str] = None

    requires_previous_context: bool = False

    continues_previous_topic: bool = False

    confidence: float = 0.0


# ==========================================================
# MEMORY UNDERSTANDING
# ==========================================================

@dataclass
class MemoryUnderstanding:

    requires_memory: bool = False

    memory_scope: Optional[str] = None

    reason: str = ""

    confidence: float = 0.0

    # ----------------------------------------------------------
    # Memory write/update/query instruction from the LLM.
    # Populated by memory_analyzer, used by memory_decision.
    # Never used by LanguageUnderstanding for anything else.
    # ----------------------------------------------------------

    memory_operation: Optional[str] = None
    # "store" | "update" | "query" | "forget" | None

    memory_payload: Optional[str] = None
    # The clean extracted fact. Null if no write operation.


# ==========================================================
# CONTEXT UNDERSTANDING
# ==========================================================

@dataclass
class ContextUnderstanding:

    requires_context: bool = False

    context_scope: Optional[str] = None

    reason: str = ""

    confidence: float = 0.0


# ==========================================================
# EMOTION UNDERSTANDING
# ==========================================================

@dataclass
class EmotionUnderstanding:

    emotion: Optional[str] = None

    sentiment: Optional[str] = None

    urgency: Optional[str] = None

    confidence: float = 0.0


# ==========================================================
# LANGUAGE UNDERSTANDING
# ==========================================================

@dataclass
class LanguageUnderstanding:

    # Original user message

    raw_text: str

    # Specialized Understanding

    semantic: SemanticUnderstanding = field(
        default_factory=SemanticUnderstanding
    )

    conversation: ConversationUnderstanding = field(
        default_factory=ConversationUnderstanding
    )

    memory: MemoryUnderstanding = field(
        default_factory=MemoryUnderstanding
    )

    context: ContextUnderstanding = field(
        default_factory=ContextUnderstanding
    )

    emotion: EmotionUnderstanding = field(
        default_factory=EmotionUnderstanding
    )

    # Temporary routing information
    # (Will later move into the Reasoning contract.)

    required_systems: RequiredSystems = field(
        default_factory=RequiredSystems
    )

    # Global constraints

    constraints: Dict[str, Any] = field(
        default_factory=dict
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    confidence: float = 0.0