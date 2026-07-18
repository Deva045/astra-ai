"""
Factory for creating LLM providers.
"""

from __future__ import annotations

from ai.llm import BaseLLM
from ai.mock_llm import MockLLM
from ai.ollama_llm import OllamaLLM

from config.settings import (
    AI_PROVIDER,
    DEFAULT_MODEL,
    OLLAMA_HOST,
)


class LLMFactory:
    """Creates configured LLM providers."""

    @staticmethod
    def create() -> BaseLLM:
        """
        Create the configured LLM provider.

        Returns:
            BaseLLM: Configured language model provider.

        Raises:
            ValueError:
                If the configured provider is unsupported.
        """

        provider = AI_PROVIDER.lower()

        if provider == "mock":
            return MockLLM()

        if provider == "ollama":
            return OllamaLLM(
                model=DEFAULT_MODEL,
                host=OLLAMA_HOST,
            )

        raise ValueError(
            f"Unsupported AI provider: {AI_PROVIDER}"
        )
