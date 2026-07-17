"""
Voice backend implementations.

Concrete implementations of the interfaces defined in
voice.interfaces live in this package.
"""

from .mock_audio_input import MockAudioInput
from .sounddevice_input import SoundDeviceInput

__all__ = [
    "MockAudioInput",
    "SoundDeviceInput",
]
