"""
Factory for creating AI providers.

The ProviderFactory is responsible for constructing the
appropriate AI provider implementation based on a provider name.
"""

from __future__ import annotations

from .base import AIProvider
from .mock_provider import MockProvider
from .ollama_provider import OllamaProvider


class ProviderFactory:
    """
    Factory responsible for creating AI providers.
    """

    _providers: dict[str, type[AIProvider]] = {
        "mock": MockProvider,
        "ollama": OllamaProvider,
    }

    @classmethod
    def register(
        cls,
        name: str,
        provider: type[AIProvider],
    ) -> None:
        """
        Register a provider.

        Args:
            name:
                Provider identifier.

            provider:
                AIProvider implementation.
        """
        cls._providers[name.lower()] = provider

    @classmethod
    def unregister(
        cls,
        name: str,
    ) -> None:
        """
        Unregister a provider.

        Args:
            name:
                Provider identifier.
        """
        cls._providers.pop(name.lower(), None)

    @classmethod
    def create(
        cls,
        provider_name: str,
        **kwargs,
    ) -> AIProvider:
        """
        Create a provider instance.

        Args:
            provider_name:
                Provider identifier.

        Returns:
            AIProvider

        Raises:
            ValueError:
                If the provider is unknown.
        """
        provider_class = cls._providers.get(
            provider_name.lower()
        )

        if provider_class is None:
            available = ", ".join(
                sorted(cls._providers.keys())
            )

            raise ValueError(
                f"Unknown AI provider '{provider_name}'. "
                f"Available providers: {available}"
            )

        return provider_class(**kwargs)

    @classmethod
    def available_providers(cls) -> list[str]:
        """
        Return all registered providers.
        """
        return sorted(cls._providers.keys())

    @classmethod
    def is_registered(
        cls,
        provider_name: str,
    ) -> bool:
        """
        Return True if a provider is registered.
        """
        return provider_name.lower() in cls._providers
