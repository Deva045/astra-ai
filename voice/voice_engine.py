"""
Voice Engine for the Nexus AI voice subsystem.

The VoiceEngine coordinates all voice-related components without
depending on any specific audio, STT, TTS, or wake-word backend.

AI interaction is performed through the VoiceAssistant interface,
keeping the voice subsystem independent of the AI implementation.
"""

from __future__ import annotations

from .assistant import VoiceAssistant
from .audio_manager import AudioManager
from .microphone_manager import MicrophoneManager
from .models import AudioChunk, VoiceState
from .speech_to_text import SpeechToTextManager
from .text_to_speech import TextToSpeechManager
from .wake_word import WakeWordManager


class VoiceEngine:
    """
    High-level coordinator for the Nexus AI voice subsystem.
    """

    def __init__(
        self,
        audio_manager: AudioManager,
        microphone_manager: MicrophoneManager,
        speech_to_text: SpeechToTextManager,
        text_to_speech: TextToSpeechManager,
        wake_word: WakeWordManager,
        assistant: VoiceAssistant,
    ) -> None:
        """
        Initialize the Voice Engine.

        Args:
            audio_manager:
                Audio configuration manager.

            microphone_manager:
                Microphone lifecycle manager.

            speech_to_text:
                Speech recognition manager.

            text_to_speech:
                Speech synthesis manager.

            wake_word:
                Wake-word detection manager.

            assistant:
                AI assistant adapter used to process user speech.
        """
        self._audio_manager = audio_manager
        self._microphone_manager = microphone_manager
        self._speech_to_text = speech_to_text
        self._text_to_speech = text_to_speech
        self._wake_word = wake_word
        self._assistant = assistant

        self._state = VoiceState.IDLE

    @property
    def state(self) -> VoiceState:
        """Return the current engine state."""
        return self._state

    def start(self) -> None:
        """
        Start the voice engine.

        This currently starts wake-word detection only.
        """
        self._wake_word.start()
        self._state = VoiceState.IDLE

    def stop(self) -> None:
        """
        Stop the voice engine.
        """
        self._microphone_manager.stop()
        self._wake_word.stop()
        self._state = VoiceState.IDLE

    def listen_once(self) -> str:
        """
        Capture one audio chunk and transcribe it.

        Returns
        -------
        str
            Recognized text.
        """
        self._state = VoiceState.LISTENING

        self._microphone_manager.start()

        audio: AudioChunk = self._microphone_manager.read_chunk()

        self._microphone_manager.stop()

        self._state = VoiceState.PROCESSING

        text = self._speech_to_text.transcribe(audio)

        self._state = VoiceState.IDLE

        return text

    def speak(self, text: str) -> None:
        """
        Speak a text response.
        """
        self._state = VoiceState.SPEAKING

        self._text_to_speech.speak(text)

        self._state = VoiceState.IDLE

    def process_once(self) -> str | None:
        """
        Execute one wake-word processing cycle.

        Workflow

            Wake Word
                ↓
            Record
                ↓
            Speech-to-Text

        Returns
        -------
        str | None

            Recognized text if the wake word was detected,
            otherwise None.
        """
        if not self._wake_word.detect():
            return None

        return self.listen_once()

    def chat_once(self) -> str | None:
        """
        Execute one complete voice interaction.

        Workflow

            Wake Word
                ↓
            Speech-to-Text
                ↓
            AI Assistant
                ↓
            Text-to-Speech

        Returns
        -------
        str | None

            AI response if a wake word was detected,
            otherwise None.
        """
        text = self.process_once()

        if text is None:
            return None

        response = self._assistant.process_text(text)

        self.speak(response)

        return response

    def reset(self) -> None:
        """
        Reset the engine to its initial state.
        """
        self.stop()
        self._state = VoiceState.IDLE
