"""
Base interfaces for all Large Language Model (LLM) providers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generator


class BaseLLM(ABC):
    """Abstract base class for language model providers."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a complete response."""
        raise NotImplementedError

    @abstractmethod
    def stream(self, prompt: str) -> Generator[str, None, None]:
        """Stream a response."""
        raise NotImplementedError
