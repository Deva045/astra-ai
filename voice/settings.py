"""
Voice settings for the Nexus AI voice subsystem.

This module defines the runtime configuration used by the voice
backends. It is independent from any specific implementation and
contains only validated configuration values.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class VoiceBackendSettings:
    """
    Runtime settings shared by all voice backends.
    """

    # Audio
    sample_rate: int = 16_000
    channels: int = 1
    chunk_size: int = 1024

    # Devices
    input_device: str | None = None
    output_device: str | None = None

    # Wake Word
    wake_word_enabled: bool = True
    wake_word: str = "Hey Nexus"

    # Speech Recognition
    language: str = "en"

    # Timeouts
    speech_timeout: float = 5.0
    silence_timeout: float = 1.0

    # Voice Output
    voice_name: str = "default"
    volume: float = 1.0
    speech_rate: float = 1.0

    @property
    def frame_duration_ms(self) -> float:
        """
        Duration of one audio chunk in milliseconds.
        """
        return (
            self.chunk_size
            / self.sample_rate
        ) * 1000.0
