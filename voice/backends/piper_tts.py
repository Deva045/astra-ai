"""
Piper Text-to-Speech backend for the Nexus AI voice subsystem.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional

from ..exceptions import TextToSpeechError
from ..interfaces import TextToSpeech


class PiperTextToSpeech(TextToSpeech):
    """
    Offline Text-to-Speech backend powered by Piper.

    This backend invokes the Piper executable using a local
    voice model and streams synthesized audio to an output file
    or directly to the configured audio device (future support).
    """

    def __init__(
        self,
        executable: str | Path,
        model_path: str | Path,
        output_file: Optional[str | Path] = None,
    ) -> None:
        self._executable = Path(executable)
        self._model_path = Path(model_path)
        self._output_file = (
            Path(output_file)
            if output_file is not None
            else Path("piper_output.wav")
        )

        if not self._executable.exists():
            raise TextToSpeechError(
                f"Piper executable not found: {self._executable}"
            )

        if not self._model_path.exists():
            raise TextToSpeechError(
                f"Piper model not found: {self._model_path}"
            )

    @property
    def executable(self) -> Path:
        """Return the Piper executable path."""
        return self._executable

    @property
    def model_path(self) -> Path:
        """Return the Piper model path."""
        return self._model_path

    @property
    def output_file(self) -> Path:
        """Return the synthesized audio file."""
        return self._output_file

    def speak(self, text: str) -> None:
        """
        Convert text into speech.

        Args:
            text:
                Text to synthesize.

        Raises:
            TextToSpeechError:
                If synthesis fails.
        """

        if not isinstance(text, str):
            raise TextToSpeechError(
                "Text must be a string."
            )

        text = text.strip()

        if not text:
            raise TextToSpeechError(
                "Cannot synthesize empty text."
            )

        command = [
            str(self._executable),
            "--model",
            str(self._model_path),
            "--output_file",
            str(self._output_file),
        ]

        try:
            subprocess.run(
                command,
                input=text.encode("utf-8"),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                check=True,
            )

        except FileNotFoundError as exc:
            raise TextToSpeechError(
                "Piper executable could not be found."
            ) from exc

        except subprocess.CalledProcessError as exc:
            message = exc.stderr.decode(
                "utf-8",
                errors="ignore",
            )

            raise TextToSpeechError(
                f"Piper synthesis failed: {message}"
            ) from exc
