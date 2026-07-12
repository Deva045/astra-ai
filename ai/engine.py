"""
AI Engine

Coordinates conversation management, memory management, and delegates
response generation to the configured LLM provider.
"""

from __future__ import annotations

from typing import Generator

from ai.conversation import Conversation
from ai.factory import LLMFactory
from ai.llm import BaseLLM
from ai.memory_extractor import MemoryExtractor
from ai.memory_manager import MemoryManager
from ai.memory_query import MemoryQuery
from ai.prompts import PromptBuilder
from ai.sqlite_memory_repository import SQLiteMemoryRepository
from database.sqlite_database import SQLiteDatabase


class AIEngine:
    """Main AI Engine."""

    def __init__(
        self,
        llm: BaseLLM | None = None,
        memory_manager: MemoryManager | None = None,
        memory_extractor: MemoryExtractor | None = None,
    ) -> None:
        """Initialize the AI engine.

        Args:
            llm: Optional language model implementation.
            memory_manager: Optional memory manager.
            memory_extractor: Optional memory extractor.
        """

        self.llm = llm or LLMFactory.create()

        self.conversation = Conversation()

        if memory_manager is None:
            database = SQLiteDatabase()
            repository = SQLiteMemoryRepository(database)
            memory_manager = MemoryManager(repository)

        self.memory_manager = memory_manager

        self.memory_extractor = (
            memory_extractor
            if memory_extractor is not None
            else MemoryExtractor()
        )

    def chat(self, text: str) -> str:
        """Generate a complete AI response."""

        prompt = self._prepare_prompt(text)

        response = self.llm.generate(prompt)

        self.conversation.add_assistant(response)

        return response

    def stream_chat(
        self,
        text: str,
    ) -> Generator[str, None, None]:
        """Stream an AI response."""

        prompt = self._prepare_prompt(text)

        collected = ""

        for chunk in self.llm.stream(prompt):
            collected += chunk
            yield chunk

        self.conversation.add_assistant(collected)

    def _prepare_prompt(self, text: str) -> str:
        """Prepare the prompt for the language model.

        This method updates the conversation history, stores any
        extracted memories, retrieves relevant memories, and builds
        the final prompt.

        Args:
            text: User input.

        Returns:
            Fully formatted prompt.
        """

        self.conversation.add_user(text)

        memory = self.memory_extractor.extract(text)

        if memory is not None:
            self.memory_manager.add_memory(memory)

        context = self._build_context(text)

        return PromptBuilder.build(
            user_input=text,
            context=context,
        )

    def _build_context(self, text: str) -> str:
        """Build the complete conversation context.

        Args:
            text: Current user input.

        Returns:
            Combined conversation and memory context.
        """

        conversation_context = self.conversation.get_context()

        result = self.memory_manager.search_memories(
            MemoryQuery(
                text=text,
                limit=5,
            )
        )

        if not result.memories:
            return conversation_context

        memory_context = "\n".join(
            memory.content
            for memory in result.memories
        )

        return (
            f"{conversation_context}\n\n"
            "Relevant memories:\n"
            f"{memory_context}"
        )
