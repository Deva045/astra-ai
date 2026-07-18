"""
Abstract AI provider interface.

Every language model backend must implement this interface.
The AI Engine communicates only with AIProvider and remains
independent of the underlying LLM implementation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator


class AIProvider(ABC):
    """
    Base interface for all AI providers.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Return the provider name.

        Examples
        --------
        ollama
        openai
        gemini
        claude
        """

    @property
    @abstractmethod
    def model_name(self) -> str:
        """
        Return the active model name.
        """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a complete response.
        """

    def stream_generate(self, prompt: str) -> Iterator[str]:
        """
        Stream a response.

        Providers without streaming support automatically
        fall back to generate().
        """
        yield self.generate(prompt)

    @abstractmethod
    def available_models(self) -> list[str]:
        """
        Return available models.
        """

    @abstractmethod
    def is_available(self) -> bool:
        """
        Return True if the provider is usable.
        """
