"""
Voice session management for the Nexus AI voice subsystem.

This module manages the runtime state of a voice conversation.
It is independent of the VoiceEngine and backend implementations.

A VoiceSession represents one active interaction between the user
and Nexus AI.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(slots=True)
class VoiceSession:
    """
    Represents the current runtime voice session.
    """

    listening: bool = False
    processing: bool = False
    speaking: bool = False
    paused: bool = False
    interrupted: bool = False

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    last_activity: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    interaction_count: int = 0

    @property
    def active(self) -> bool:
        """
        Return True if any voice activity is occurring.
        """
        return (
            self.listening
            or self.processing
            or self.speaking
        )

    def touch(self) -> None:
        """
        Update the last activity timestamp.
        """
        self.last_activity = datetime.now(UTC)

    def start_listening(self) -> None:
        """
        Enter the listening state.
        """
        self.reset_flags()
        self.listening = True
        self.touch()

    def start_processing(self) -> None:
        """
        Enter the processing state.
        """
        self.reset_flags()
        self.processing = True
        self.touch()

    def start_speaking(self) -> None:
        """
        Enter the speaking state.
        """
        self.reset_flags()
        self.speaking = True
        self.interaction_count += 1
        self.touch()

    def pause(self) -> None:
        """
        Pause the session.
        """
        self.paused = True
        self.touch()

    def resume(self) -> None:
        """
        Resume the session.
        """
        self.paused = False
        self.touch()

    def interrupt(self) -> None:
        """
        Interrupt the current interaction.
        """
        self.interrupted = True
        self.reset_flags()
        self.touch()

    def reset_flags(self) -> None:
        """
        Clear all runtime state flags.
        """
        self.listening = False
        self.processing = False
        self.speaking = False

    def reset(self) -> None:
        """
        Restore the session to its initial state.
        """
        self.listening = False
        self.processing = False
        self.speaking = False
        self.paused = False
        self.interrupted = False
        self.interaction_count = 0
        self.touch()
