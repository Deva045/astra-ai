"""
Ollama LLM Provider.

Implements the BaseLLM interface using a locally running
Ollama server.
"""

from __future__ import annotations

import json
from typing import Generator

import requests

from ai.llm import BaseLLM


class OllamaLLM(BaseLLM):
    """LLM backed by a local Ollama server."""

    def __init__(
        self,
        model: str = "llama3.1:8b",
        host: str = "http://localhost:11434",
        timeout: float = 120.0,
    ) -> None:
        self._model = model
        self._host = host.rstrip("/")
        self._timeout = timeout

    @property
    def model(self) -> str:
        """Return the active model."""
        return self._model

    @property
    def host(self) -> str:
        """Return Ollama server URL."""
        return self._host

    def is_available(self) -> bool:
        """Return True if Ollama is reachable."""
        try:
            response = requests.get(
                f"{self._host}/api/tags",
                timeout=5,
            )
            return response.status_code == 200

        except requests.RequestException:
            return False

    def generate(self, prompt: str) -> str:
        """Generate a complete response."""

        payload = {
            "model": self._model,
            "prompt": prompt,
            "stream": False,
        }

        response = requests.post(
            f"{self._host}/api/generate",
            json=payload,
            timeout=self._timeout,
        )

        response.raise_for_status()

        return response.json()["response"]

    def stream(
        self,
        prompt: str,
    ) -> Generator[str, None, None]:
        """Stream a response."""

        payload = {
            "model": self._model,
            "prompt": prompt,
            "stream": True,
        }

        response = requests.post(
            f"{self._host}/api/generate",
            json=payload,
            stream=True,
            timeout=self._timeout,
        )

        response.raise_for_status()

        for line in response.iter_lines():

            if not line:
                continue

            chunk = json.loads(
                line.decode("utf-8")
            )

            text = chunk.get("response")

            if text:
                yield text

            if chunk.get("done", False):
                break
