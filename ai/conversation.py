"""
Conversation manager.
"""

from __future__ import annotations

from ai.conversation_history import ConversationHistory


class Conversation:
    """
    Manages conversation context.
    """

    def __init__(self) -> None:
        self.history = ConversationHistory()

    def add_user(
        self,
        text: str,
    ) -> None:
        """
        Store a user message.
        """
        self.history.add(
            "user",
            text,
        )

    def add_assistant(
        self,
        text: str,
    ) -> None:
        """
        Store an assistant message.
        """
        self.history.add(
            "assistant",
            text,
        )

    def clear(self) -> None:
        """
        Clear conversation history.
        """
        self.history.clear()

    def get_context(
        self,
        limit: int = 10,
    ) -> str:
        """
        Build conversation context.
        """

        lines: list[str] = []

        for message in self.history.last(limit):
            lines.append(
                f"{message.role.capitalize()}: {message.content}"
            )

        return "\n".join(lines)

    def size(self) -> int:
        """
        Return conversation size.
        """
        return self.history.size()
