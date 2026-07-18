"""
Context Window Manager.

Responsible for preparing optimized context before sending
requests to the LLM.

This module is provider-independent and works with both
MockLLM and OllamaLLM.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ContextMessage:
    """
    Represents a conversation message.
    """

    role: str
    content: str


@dataclass(slots=True)
class ContextWindow:
    """
    Final optimized context window.
    """

    messages: list[ContextMessage] = field(
        default_factory=list
    )

    memories: list[str] = field(
        default_factory=list
    )

    def to_prompt(self) -> str:
        """
        Convert context into a prompt string.
        """

        parts: list[str] = []

        for message in self.messages:
            parts.append(
                f"{message.role.capitalize()}: "
                f"{message.content}"
            )

        if self.memories:
            parts.append(
                "\nRelevant memories:"
            )

            for memory in self.memories:
                parts.append(
                    f"- {memory}"
                )

        return "\n".join(parts)


class ContextManager:
    """
    Manages conversation context size and priority.
    """

    def __init__(
        self,
        max_messages: int = 20,
        max_chars: int = 12000,
    ) -> None:

        self._max_messages = max_messages
        self._max_chars = max_chars

    @property
    def max_messages(self) -> int:
        """Return message limit."""
        return self._max_messages

    @property
    def max_chars(self) -> int:
        """Return character limit."""
        return self._max_chars

    def build_context(
        self,
        messages: list[ContextMessage],
        memories: list[str] | None = None,
    ) -> ContextWindow:
        """
        Build an optimized context window.

        Keeps recent messages while respecting limits.
        """

        memories = memories or []

        selected_messages = (
            messages[-self._max_messages:]
        )

        context = ContextWindow(
            messages=selected_messages,
            memories=memories,
        )

        return self._trim_context(context)

    def _trim_context(
        self,
        context: ContextWindow,
    ) -> ContextWindow:
        """
        Reduce context size if it exceeds limits.
        """

        while (
            len(context.to_prompt())
            > self._max_chars
            and len(context.messages) > 1
        ):
            context.messages.pop(0)

        return context

    def clear(self) -> ContextWindow:
        """
        Return an empty context.
        """

        return ContextWindow()
