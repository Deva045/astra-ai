"""
AI configuration.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AIConfig:
    """
    Configuration for the AI subsystem.
    """

    provider: str = "mock"

    model: str = "mock-model"

    host: str = "http://localhost:11434"

    timeout: float = 120.0

    temperature: float = 0.7

    max_tokens: int = 2048

    stream: bool = False
