"""
Voice assistant adapter.

This module connects the Voice subsystem to the existing AI Engine
while keeping VoiceEngine independent of the concrete AI implementation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Protocol, runtime_checkable


@runtime_checkable
class AIEngineProtocol(Protocol):
    """
    Protocol describing the functionality required by
    AIEngineVoiceAssistant.
    """

    def chat(self, text: str) -> str:
        ...

    def stream_chat(self, text: str) -> Iterator[str]:
        ...


class VoiceAssistant(ABC):
    """
    Abstract interface used by VoiceEngine.
    """

    @abstractmethod
    def process_text(self, text: str) -> str:
        """
        Process user speech and return the assistant response.
        """
        raise NotImplementedError

    def stream_text(self, text: str) -> Iterator[str]:
        """
        Stream assistant responses.

        Concrete implementations may override this method.
        """
        yield self.process_text(text)


class AIEngineVoiceAssistant(VoiceAssistant):
    """
    Adapter around an AI engine implementation.

    Any object implementing AIEngineProtocol can be used.
    """

    def __init__(
        self,
        engine: AIEngineProtocol,
    ) -> None:
        self._engine = engine

    @property
    def engine(self) -> AIEngineProtocol:
        """Return the wrapped AI engine."""
        return self._engine

    def process_text(self, text: str) -> str:
        """Generate a complete AI response."""
        return self._engine.chat(text)

    def stream_text(self, text: str) -> Iterator[str]:
        """Stream the AI response."""
        yield from self._engine.stream_chat(text)
