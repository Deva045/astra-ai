"""
Vosk Speech-to-Text backend for the Nexus AI voice subsystem.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from vosk import KaldiRecognizer, Model

from ..exceptions import SpeechToTextError
from ..interfaces import SpeechToText
from ..models import AudioChunk


class VoskSpeechToText(SpeechToText):
    """
    Offline Speech-to-Text backend using Vosk.

    This backend loads a local Vosk model and converts
    raw PCM audio into text.
    """

    def __init__(
        self,
        model_path: str | Path,
        sample_rate: int = 16000,
    ) -> None:
        self._sample_rate = sample_rate
        self._model_path = Path(model_path)

        if not self._model_path.exists():
            raise SpeechToTextError(
                f"Vosk model not found: {self._model_path}"
            )

        try:
            self._model = Model(str(self._model_path))
        except Exception as exc:
            raise SpeechToTextError(
                f"Failed to load Vosk model: {exc}"
            ) from exc

        self._recognizer = KaldiRecognizer(
            self._model,
            self._sample_rate,
        )

    @property
    def sample_rate(self) -> int:
        """Configured sample rate."""
        return self._sample_rate

    @property
    def model_path(self) -> Path:
        """Return the loaded model path."""
        return self._model_path

    def reset(self) -> None:
        """
        Reset the recognizer state.
        """
        self._recognizer = KaldiRecognizer(
            self._model,
            self._sample_rate,
        )

    def transcribe(self, audio: AudioChunk) -> str:
        """
        Convert an AudioChunk into text.

        Args:
            audio:
                Raw PCM audio.

        Returns:
            Recognized text.

        Raises:
            SpeechToTextError:
                If transcription fails.
        """

        if audio.sample_rate != self._sample_rate:
            raise SpeechToTextError(
                f"Expected {self._sample_rate} Hz audio, "
                f"received {audio.sample_rate} Hz."
            )

        try:
            accepted = self._recognizer.AcceptWaveform(audio.data)

            if accepted:
                result = json.loads(
                    self._recognizer.Result()
                )
            else:
                result = json.loads(
                    self._recognizer.FinalResult()
                )

            return result.get("text", "").strip()

        except Exception as exc:
            raise SpeechToTextError(
                f"Speech recognition failed: {exc}"
            ) from exc
