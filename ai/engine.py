
"""
AI Engine

Coordinates conversation management, memory management,
context optimization, tool execution, and delegates
response generation to the configured LLM provider.
"""

from __future__ import annotations

from typing import Generator

from ai.context_manager import (
    ContextManager,
    ContextMessage,
)
from ai.conversation import Conversation
from ai.factory import LLMFactory
from ai.llm import BaseLLM
from ai.memory_extractor import MemoryExtractor
from ai.memory_manager import MemoryManager
from ai.memory_query import MemoryQuery
from ai.prompts import PromptBuilder
from ai.response import AIResponse
from ai.sqlite_memory_repository import SQLiteMemoryRepository
from ai.tool_router import ToolRouter
from database.sqlite_database import SQLiteDatabase


class AIEngine:
    """Main AI Engine."""

    def __init__(
        self,
        llm: BaseLLM | None = None,
        memory_manager: MemoryManager | None = None,
        memory_extractor: MemoryExtractor | None = None,
        context_manager: ContextManager | None = None,
        tool_router: ToolRouter | None = None,
    ) -> None:
        """
        Initialize the AI engine.
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

        self.context_manager = (
            context_manager
            if context_manager is not None
            else ContextManager()
        )

        self.tool_router = tool_router

        self.last_response: AIResponse | None = None

    def chat(
        self,
        text: str,
    ) -> str:
        """
        Generate a complete AI response.

        Returns:
            Plain text response.
        """

        if self.tool_router is not None:
            tool_result = self.tool_router.route(
                text
            )

            if tool_result is not None:
                self.conversation.add_user(
                    text
                )

                self.conversation.add_assistant(
                    tool_result
                )

                self.last_response = AIResponse(
                    content=tool_result,
                    provider="Tool",
                    model="",
                )

                return tool_result

        prompt = self._prepare_prompt(text)

        response = self.llm.generate(prompt)

        self.last_response = AIResponse(
            content=response,
            provider=self.llm.__class__.__name__,
            model=getattr(
                self.llm,
                "model",
                "",
            ),
        )

        self.conversation.add_assistant(
            response
        )

        return response

    def stream_chat(
        self,
        text: str,
    ) -> Generator[str, None, None]:
        """
        Stream an AI response.
        """

        prompt = self._prepare_prompt(text)

        collected = ""

        for chunk in self.llm.stream(prompt):
            collected += chunk
            yield chunk

        self.last_response = AIResponse(
            content=collected,
            provider=self.llm.__class__.__name__,
            model=getattr(
                self.llm,
                "model",
                "",
            ),
        )

        self.conversation.add_assistant(
            collected
        )

    def _prepare_prompt(
        self,
        text: str,
    ) -> str:
        """
        Prepare optimized prompt.
        """

        self.conversation.add_user(text)

        memory = self.memory_extractor.extract(
            text
        )

        if memory is not None:
            self.memory_manager.add_memory(
                memory
            )

        context = self._build_context(text)

        return PromptBuilder.build(
            user_input=text,
            context=context,
        )

    def _build_context(
        self,
        text: str,
    ) -> str:
        """
        Build optimized context.
        """

        result = self.memory_manager.search_memories(
            MemoryQuery(
                text=text,
                limit=5,
            )
        )

        memories: list[str] = []

        if result.memories:
            memories = [
                memory.content
                for memory in result.memories
            ]

        messages = [
            ContextMessage(
                role=message.role,
                content=message.content,
            )
            for message in self.conversation.history.last(
                self.context_manager.max_messages
            )
        ]

        context = self.context_manager.build_context(
            messages=messages,
            memories=memories,
        )

        return context.to_prompt()
