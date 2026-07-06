"""
Command history for Astra AI.
"""

from __future__ import annotations


class History:
    """
    Stores the history of executed commands.
    """

    def __init__(self) -> None:
        self._entries: list[str] = []

    def add(self, command: str) -> None:
        """
        Store a command in history.

        Args:
            command:
                Raw command entered by the user.
        """
        self._entries.append(command)

    def all(self) -> list[str]:
        """
        Return the complete command history.
        """
        return self._entries.copy()

    def clear(self) -> None:
        """
        Remove all history entries.
        """
        self._entries.clear()

    def size(self) -> int:
        """
        Return the number of stored commands.
        """
        return len(self._entries)
