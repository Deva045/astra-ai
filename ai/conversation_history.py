"""
Conversation history for Nexus AI.

Stores user and assistant messages.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ConversationMessage:
    """
    Represents one conversation message.
    """

    role: str
    content: str


class ConversationHistory:
    """
    Stores conversation messages.
    """

    def __init__(self) -> None:
        self._messages: list[ConversationMessage] = []

    def add(
        self,
        role: str,
        content: str,
    ) -> None:
        """
        Store a conversation message.
        """
        self._messages.append(
            ConversationMessage(
                role=role,
                content=content,
            )
        )

    def last(
        self,
        limit: int = 10,
    ) -> list[ConversationMessage]:
        """
        Return the last conversation messages.
        """
        return self._messages[-limit:]

    def clear(self) -> None:
        """
        Clear conversation history.
        """
        self._messages.clear()

    def size(self) -> int:
        """
        Return the number of stored messages.
        """
        return len(self._messages)
