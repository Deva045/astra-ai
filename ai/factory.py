"""
Factory for creating LLM providers.
"""

from ai.llm import BaseLLM
from ai.mock_llm import MockLLM

from config.settings import AI_PROVIDER


class LLMFactory:
    """Creates configured LLM providers."""

    @staticmethod
    def create() -> BaseLLM:
        provider = AI_PROVIDER.lower()

        if provider == "mock":
            return MockLLM()

        raise ValueError(
            f"Unsupported AI provider: {AI_PROVIDER}"
        )
