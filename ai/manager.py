"""
AI Manager.

Provides a high-level interface for interacting with the configured
AI provider.
"""

from __future__ import annotations

from collections.abc import Iterator

from config.ai_config import AIConfig

from ai.providers import AIProvider, ProviderFactory


class AIManager:
    """
    High-level manager for AI providers.
    """

    def __init__(
        self,
        config: AIConfig | None = None,
    ) -> None:
        """
        Initialize the AI manager.

        Args:
            config:
                AI configuration. If omitted, the default configuration
                is used.
        """
        if config is None:
            config = AIConfig()

        self._config = config

        self._provider: AIProvider = ProviderFactory.create(
            config.provider,
            model_name=config.model,
            host=config.host,
            timeout=config.timeout,
        )

    @property
    def config(self) -> AIConfig:
        """
        Return the active configuration.
        """
        return self._config

    @property
    def provider(self) -> AIProvider:
        """
        Return the active provider instance.
        """
        return self._provider

    @property
    def provider_name(self) -> str:
        """
        Return the active provider name.
        """
        return self._provider.provider_name

    @property
    def model_name(self) -> str:
        """
        Return the active model name.
        """
        return self._provider.model_name

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a response.
        """
        return self._provider.generate(prompt)

    def stream_generate(
        self,
        prompt: str,
    ) -> Iterator[str]:
        """
        Stream a response.
        """
        yield from self._provider.stream_generate(prompt)

    def available_models(self) -> list[str]:
        """
        Return the available models.
        """
        return self._provider.available_models()

    def is_available(self) -> bool:
        """
        Return whether the active provider is available.
        """
        return self._provider.is_available()

    def set_provider(
        self,
        provider: str,
        **provider_kwargs,
    ) -> None:
        """
        Switch to a different provider.

        Args:
            provider:
                Provider name.

            **provider_kwargs:
                Arguments forwarded to the provider constructor.
        """
        self._provider = ProviderFactory.create(
            provider,
            **provider_kwargs,
        )

        if "model_name" in provider_kwargs:
            self._config.model = provider_kwargs["model_name"]

        self._config.provider = provider

    def reload(self) -> None:
        """
        Reload the provider using the current configuration.
        """
        self._provider = ProviderFactory.create(
            self._config.provider,
            model_name=self._config.model,
            host=self._config.host,
            timeout=self._config.timeout,
        )
