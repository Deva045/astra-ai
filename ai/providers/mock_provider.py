"""
Mock AI provider used for testing.

This provider returns deterministic responses and does not require
any external AI model or network connection.
"""

from __future__ import annotations

from .base import AIProvider


class MockProvider(AIProvider):
    """
    Simple deterministic AI provider.

    Primarily intended for unit and integration tests.
    """

    def __init__(
        self,
        model_name: str = "mock-model",
    ) -> None:
        self._model_name = model_name

    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return "mock"

    @property
    def model_name(self) -> str:
        """Return the configured model."""
        return self._model_name

    def generate(self, prompt: str) -> str:
        """
        Generate a deterministic response.

        Args:
            prompt:
                User prompt.

        Returns:
            Mock response.
        """
        return f"Mock Response: {prompt}"

    def available_models(self) -> list[str]:
        """
        Return supported models.

        Returns:
            List containing the single mock model.
        """
        return [self._model_name]

    def is_available(self) -> bool:
        """
        Mock provider is always available.
        """
        return True
