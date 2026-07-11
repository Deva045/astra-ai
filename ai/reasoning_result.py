"""
Reasoning result for Nexus AI.

Represents the outcome of request classification.
"""

from __future__ import annotations

from dataclasses import dataclass

from ai.reasoning_type import ReasoningType


@dataclass(slots=True)
class ReasoningResult:
    """
    Result returned by the ReasoningEngine.
    """

    reasoning: ReasoningType
    confidence: float = 1.0
