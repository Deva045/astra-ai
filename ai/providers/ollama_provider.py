"""
Ollama AI provider.

This provider integrates Nexus AI with a locally running Ollama
server while conforming to the AIProvider interface.
"""

from __future__ import annotations

import json
from collections.abc import Iterator

import requests

from .base import AIProvider


class OllamaProvider(AIProvider):
    """
    AI provider backed by a local Ollama server.
    """

    def __init__(
        self,
        model_name: str = "llama3.1:8b",
        host: str = "http://localhost:11434",
        timeout: float = 120.0,
    ) -> None:
        self._model_name = model_name
        self._host = host.rstrip("/")
        self._timeout = timeout

    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return "ollama"

    @property
    def model_name(self) -> str:
        """Return the configured model."""
        return self._model_name

    @property
    def host(self) -> str:
        """Return the Ollama server URL."""
        return self._host

    def is_available(self) -> bool:
        """
        Return True if the Ollama server is reachable.
        """
        try:
            response = requests.get(
                f"{self._host}/api/tags",
                timeout=5,
            )
            return response.status_code == 200

        except requests.RequestException:
            return False

    def available_models(self) -> list[str]:
        """
        Return installed Ollama models.
        """
        try:
            response = requests.get(
                f"{self._host}/api/tags",
                timeout=self._timeout,
            )

            response.raise_for_status()

            data = response.json()

            return [
                model["name"]
                for model in data.get("models", [])
            ]

        except requests.RequestException:
            return []

    def generate(self, prompt: str) -> str:
        """
        Generate a complete response.
        """
        payload = {
            "model": self._model_name,
            "prompt": prompt,
            "stream": False,
        }

        response = requests.post(
            f"{self._host}/api/generate",
            json=payload,
            timeout=self._timeout,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]

    def stream_generate(
        self,
        prompt: str,
    ) -> Iterator[str]:
        """
        Stream a response from Ollama.
        """
        payload = {
            "model": self._model_name,
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
