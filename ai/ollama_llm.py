"""
Ollama LLM Provider.

Implements BaseLLM using a local Ollama server.
"""

from __future__ import annotations

import json
import time
from typing import Generator

import requests

from ai.llm import BaseLLM
from config.settings import (
    OLLAMA_HOST,
    OLLAMA_MAX_RETRIES,
    OLLAMA_RETRY_DELAY,
    OLLAMA_TIMEOUT,
)


class OllamaLLMError(Exception):
    """Base exception for Ollama errors."""


class OllamaConnectionError(OllamaLLMError):
    """Raised when Ollama cannot be reached."""


class OllamaResponseError(OllamaLLMError):
    """Raised when Ollama returns invalid data."""


class OllamaLLM(BaseLLM):
    """
    LLM implementation using Ollama API.
    """

    def __init__(
        self,
        model: str = "qwen3",
        host: str = OLLAMA_HOST,
        timeout: float = OLLAMA_TIMEOUT,
        retries: int = OLLAMA_MAX_RETRIES,
        retry_delay: float = OLLAMA_RETRY_DELAY,
    ) -> None:

        self._model = model
        self._host = host.rstrip("/")
        self._timeout = timeout
        self._retries = retries
        self._retry_delay = retry_delay

    @property
    def model(self) -> str:
        """Return active model."""
        return self._model

    @property
    def host(self) -> str:
        """Return Ollama host."""
        return self._host

    def is_available(self) -> bool:
        """
        Check Ollama availability.
        """

        try:
            response = requests.get(
                f"{self._host}/api/tags",
                timeout=5,
            )

            return response.status_code == 200

        except requests.RequestException:
            return False

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a complete response.
        """

        payload = {
            "model": self._model,
            "prompt": prompt,
            "stream": False,
        }

        response = self._request(
            payload
        )

        try:
            data = response.json()

        except ValueError as exc:
            raise OllamaResponseError(
                "Invalid JSON response from Ollama."
            ) from exc

        result = data.get("response")

        if not isinstance(result, str):
            raise OllamaResponseError(
                "Ollama response missing text."
            )

        return result.strip()

    def stream(
        self,
        prompt: str,
    ) -> Generator[str, None, None]:
        """
        Stream response chunks.
        """

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

            try:
                chunk = json.loads(
                    line.decode("utf-8")
                )

            except json.JSONDecodeError:
                continue

            text = chunk.get(
                "response"
            )

            if isinstance(text, str):
                yield text

            if chunk.get("done"):
                break

    def _request(
        self,
        payload: dict,
    ) -> requests.Response:
        """
        Execute request with retries.
        """

        last_error: Exception | None = None

        for attempt in range(
            self._retries + 1
        ):

            try:
                response = requests.post(
                    f"{self._host}/api/generate",
                    json=payload,
                    timeout=self._timeout,
                )

                response.raise_for_status()

                return response

            except requests.RequestException as exc:

                last_error = exc

                if attempt < self._retries:
                    time.sleep(
                        self._retry_delay
                    )

        raise OllamaConnectionError(
            "Unable to connect to Ollama."
        ) from last_error
