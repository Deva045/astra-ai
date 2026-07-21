"""
Wake Word manager for the Nexus AI voice subsystem.

This module provides a backend-independent wake-word manager.
Concrete implementations (e.g. Porcupine, OpenWakeWord) will
be integrated later without changing this interface.
"""

from __future__ import annotations

from typing import Optional

from .exceptions import WakeWordError
from .interfaces import WakeWordDetector


class WakeWordManager:
    """
    Coordinates wake-word detection using a pluggable backend.
    """

    def __init__(
        self,
        backend: Optional[WakeWordDetector] = None,
    ) -> None:
        self._backend = backend
        self._running = False

    @property
    def backend(self) -> Optional[WakeWordDetector]:
        """Return the configured wake-word backend."""
        return self._backend

    @property
    def is_running(self) -> bool:
        """Return whether wake-word detection is active."""
        return self._running

    def set_backend(
        self,
        backend: WakeWordDetector,
    ) -> None:
        """
        Configure the wake-word backend.

        Args:
            backend:
                Concrete WakeWordDetector implementation.
        """
        self._backend = backend

    def has_backend(self) -> bool:
        """Return True if a backend has been configured."""
        return self._backend is not None

    def start(self) -> None:
        """
        Start wake-word detection.

        Raises:
            WakeWordError:
                If no backend has been configured.
        """
        if self._backend is None:
            raise WakeWordError(
                "No wake-word backend has been configured."
            )

        if self._running:
            return

        self._backend.start()
        self._running = True

    def stop(self) -> None:
        """
        Stop wake-word detection.

        Safe to call multiple times.
        """
        if self._backend is None:
            self._running = False
            return

        if not self._running:
            return

        self._backend.stop()
        self._running = False

    def detect(self) -> bool:
        """
        Check whether the wake word has been detected.

        Returns:
            True if the wake word is detected.

        Raises:
            WakeWordError:
                If no backend is configured or the
                detector is not running.
        """
        if self._backend is None:
            raise WakeWordError(
                "No wake-word backend has been configured."
            )

        if not self._running:
            raise WakeWordError(
                "Wake-word detector is not running."
            )

        return self._backend.detected()

    def reset(self) -> None:
        """
        Reset the wake-word manager.

        Stops detection if necessary and removes
        the configured backend.
        """
        self.stop()
        self._backend = None
