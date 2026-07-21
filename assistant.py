"""
Voice assistant adapter.

This module connects the Voice subsystem to the existing AIEngine
without creating a direct dependency on the rest of the application.

VoiceEngine communicates only with this interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ai.engine import AIEngine


class VoiceAssistant(ABC):
    """
    Abstract interface used by the VoiceEngine.
    """

    @abstractmethod
    def process_text(self, text: str) -> str:
        """
        Process user speech and return the assistant response.
        """

    @abstractmethod
    def stream_text(self, text: str):
        """
        Stream the assistant response.
        """


class AIEngineVoiceAssistant(VoiceAssistant):
    """
    Adapter around the existing AIEngine.
    """

    def __init__(
        self,
        engine: AIEngine,
    ) -> None:
        self._engine = engine

    def process_text(
        self,
        text: str,
    ) -> str:
        """
        Generate a complete response.
        """
        return self._engine.chat(text)

    def stream_text(
        self,
        text: str,
    ):
        """
        Stream the AI response.
        """
        yield from self._engine.stream_chat(text)
