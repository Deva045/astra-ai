"""
Mock LLM Provider.

Used during development when no real LLM provider
is available.
"""

from __future__ import annotations

from typing import Generator
import re

from ai.llm import BaseLLM


class MockLLM(BaseLLM):
    """Mock implementation of a language model."""

    def _extract_user_input(self, prompt: str) -> str:
        """
        Extract the latest user message from the prompt.
        """

        match = re.search(
            r"User:\s*(.*?)\s*Assistant:$",
            prompt,
            re.DOTALL,
        )

        if match:
            return match.group(1).strip()

        return prompt.strip()

    def generate(self, prompt: str) -> str:
        """
        Generate a mock AI response.
        """

        user_input = self._extract_user_input(prompt)

        return (
            "Hello! I'm Astra.\n\n"
            "✅ AI Engine: Online\n"
            "✅ Conversation Manager: Active\n"
            "✅ Prompt Builder: Active\n"
            "⚠ LLM Provider: Mock Mode\n\n"
            "I'm currently running in development mode.\n"
            "A real LLM (Ollama) will be connected later.\n\n"
            f"I received your message:\n"
            f"'{user_input}'"
        )

    def stream(self, prompt: str) -> Generator[str, None, None]:
        """
        Stream the mock response.
        """

        response = self.generate(prompt)

        for word in response.split():
            yield word + " "
