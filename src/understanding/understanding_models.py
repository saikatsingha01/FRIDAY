from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class Entity:

    text: str

    label: str

    confidence: float = 1.0



@dataclass
class TimeReference:

    type: Optional[str] = None

    value: Optional[str] = None

    confidence: float = 1.0



@dataclass
class LanguageUnderstanding:

    # Original user input
    original_text: str

    # High-level meaning
    intent: str = "conversation"

    # Extracted entities
    entities: List[Entity] = field(default_factory=list)

    # Current memory / history / episode / etc.
    memory_scope: Optional[str] = None

    # Device / project / preference / identity...
    category: Optional[str] = None

    # Previous / yesterday / tomorrow / etc.
    time_reference: Optional[TimeReference] = None

    # Is this asking a question?
    is_question: bool = False

    # Should previous conversation be searched?
    needs_context: bool = False

    # Should long-term memory be searched?
    needs_memory: bool = False

    # Should episodic memory be searched?
    needs_episode: bool = False

    # Future planner
    goal: Optional[str] = None

    # Future tool router
    suggested_tool: Optional[str] = None

    # Overall confidence
    confidence: float = 1.0

    # Extra information
    metadata: Dict[str, Any] = field(default_factory=dict)