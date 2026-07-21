"""
OpenWakeWord backend for the Nexus AI voice subsystem.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, TYPE_CHECKING

from ..exceptions import WakeWordError
from ..interfaces import WakeWordDetector

# Only import for static type checking.
# The runtime import is performed in start() so the module
# can still be imported even if openwakeword is not installed.
if TYPE_CHECKING:
    from openwakeword.model import Model
else:
    Model = Any


class OpenWakeWordDetector(WakeWordDetector):
    """
    Wake-word detector powered by OpenWakeWord.
    """

    def __init__(
        self,
        model_path: str |Path,
        threshold: float = 0.5,
    ) -> None:
        self._model_path = Path(model_path)
        self._threshold = threshold

        # Runtime model instance
        self._model: Any = None

        self._running = False
        self._detected = False

        if not self._model_path.exists():
            raise WakeWordError(
                f"Wake-word model not found: {self._model_path}"
            )

    @property
    def is_running(self) -> bool:
        """Return whether the detector is running."""
        return self._running

    @property
    def threshold(self) -> float:
        """Detection threshold."""
        return self._threshold

    def start(self) -> None:
        """
        Load the wake-word model and start detection.
        """
        if self._running:
            return

        try:
            from openwakeword.model import Model
        except ImportError as exc:
            raise WakeWordError(
                "OpenWakeWord is not installed."
            ) from exc

        try:
            self._model = Model(
                wakeword_models=[str(self._model_path)]
            )
        except Exception as exc:
            raise WakeWordError(
                f"Failed to load wake-word model: {exc}"
            ) from exc

        self._running = True
        self._detected = False

    def stop(self) -> None:
        """
        Stop wake-word detection.
        """
        self._running = False
        self._model = None
        self._detected = False

    def process(self, pcm) -> bool:
        """
        Process one frame of PCM audio.

        Args:
            pcm:
                16-bit mono PCM samples at 16 kHz.

        Returns:
            True if the wake word was detected.
        """
        if not self._running:
            raise WakeWordError(
                "Wake-word detector is not running."
            )

        if self._model is None:
            raise WakeWordError(
                "Wake-word model has not been loaded."
            )

        try:
            predictions = self._model.predict(pcm)

            self._detected = any(
                score >= self._threshold
                for score in predictions.values()
            )

            return self._detected

        except Exception as exc:
            raise WakeWordError(
                f"Wake-word detection failed: {exc}"
            ) from exc

    def detected(self) -> bool:
        """
        Return whether the wake word has been detected.
        """
        return self._detected

    def reset(self) -> None:
        """
        Reset the detector state.
        """
        self._detected = False
