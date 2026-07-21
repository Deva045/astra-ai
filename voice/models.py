"""
Shared models for the Nexus AI voice subsystem.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class VoiceState(str, Enum):
    """Current state of the voice engine."""

    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"
    SPEAKING = "speaking"
    ERROR = "error"


@dataclass(slots=True)
class AudioChunk:
    """
    Represents a chunk of raw audio.
    """

    data: bytes
    sample_rate: int
    channels: int
    sample_width: int


@dataclass(slots=True)
class VoiceSettings:
    """
    Configuration shared across the voice subsystem.
    """

    sample_rate: int = 16000
    channels: int = 1
    chunk_size: int = 1024
    wake_word_enabled: bool = True
    speech_timeout: float = 5.0
    silence_timeout: float = 1.5
    input_device: Optional[str] = None
    output_device: Optional[str] = None
    metadata: dict[str, str] = field(default_factory=dict)
