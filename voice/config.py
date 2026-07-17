"""
Voice configuration manager for the Nexus AI voice subsystem.

This module provides loading, saving, and resetting of the
voice backend configuration.

Configuration is stored as JSON and is independent of any
specific backend implementation.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .settings import VoiceBackendSettings


class VoiceConfig:
    """
    Manages persistent voice configuration.
    """

    DEFAULT_FILENAME = "voice_settings.json"

    def __init__(
        self,
        config_path: str | Path | None = None,
    ) -> None:
        if config_path is None:
            config_path = self.DEFAULT_FILENAME

        self._config_path = Path(config_path)
        self._settings = VoiceBackendSettings()

    @property
    def path(self) -> Path:
        """Return the configuration file path."""
        return self._config_path

    @property
    def settings(self) -> VoiceBackendSettings:
        """Return the current settings."""
        return self._settings

    def load(self) -> VoiceBackendSettings:
        """
        Load configuration from disk.

        If the file does not exist, default settings are returned.
        """
        if not self._config_path.exists():
            self._settings = VoiceBackendSettings()
            return self._settings

        with self._config_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        self._settings = VoiceBackendSettings(**data)

        return self._settings

    def save(self) -> None:
        """
        Save the current configuration.
        """
        self._config_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self._config_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                asdict(self._settings),
                file,
                indent=4,
                sort_keys=True,
            )

    def update(
        self,
        settings: VoiceBackendSettings,
    ) -> None:
        """
        Replace the current settings.
        """
        self._settings = settings

    def reset(self) -> VoiceBackendSettings:
        """
        Restore default settings.
        """
        self._settings = VoiceBackendSettings()
        return self._settings
