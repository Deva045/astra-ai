"""
AI Engine

Coordinates conversation management and delegates
response generation to the configured LLM provider.
"""

from __future__ import annotations

from typing import Generator

from ai.conversation import Conversation
from ai.factory import LLMFactory
from ai.llm import BaseLLM
from ai.prompts import PromptBuilder


class AIEngine:
    """Main AI Engine."""

    def __init__(self, llm: BaseLLM | None = None):
        self.llm = llm or LLMFactory.create()
        self.conversation = Conversation()

    def chat(self, text: str) -> str:
        """
        Generate a complete AI response.
        """

        # Store user message
        self.conversation.add_user(text)

        # Build conversation context
        context = self.conversation.get_context()

        # Build the final prompt
        prompt = PromptBuilder.build(
            user_input=text,
            context=context
        )

        # Generate response
        response = self.llm.generate(prompt)

        # Store assistant response
        self.conversation.add_assistant(response)

        return response

    def stream_chat(self, text: str) -> Generator[str, None, None]:
        """
        Stream an AI response.
        """

        # Store user message
        self.conversation.add_user(text)

        # Build conversation context
        context = self.conversation.get_context()

        # Build the final prompt
        prompt = PromptBuilder.build(
            user_input=text,
            context=context
        )

        collected = ""

        for chunk in self.llm.stream(prompt):
            collected += chunk
            yield chunk

        # Store complete response
        self.conversation.add_assistant(collected)
