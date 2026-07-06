"""
Conversation manager.
"""

from __future__ import annotations

from ai.history import History


class Conversation:
    """Manages conversation context."""

    def __init__(self):
        self.history = History()

    def add_user(self, text: str) -> None:
        self.history.add("user", text)

    def add_assistant(self, text: str) -> None:
        self.history.add("assistant", text)

    def clear(self) -> None:
        self.history.clear()

    def get_context(self, limit: int = 10) -> str:
        """
        Build conversation context for an LLM.
        """

        lines = []

        for message in self.history.last(limit):
            lines.append(
                f"{message.role.capitalize()}: {message.content}"
            )

        return "\n".join(lines)

    def size(self) -> int:
        return self.history.size()
