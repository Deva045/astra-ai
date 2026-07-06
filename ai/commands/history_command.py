"""
History command for Nexus AI.
"""

from __future__ import annotations

from ai.command import Command
from ai.history import History


class HistoryCommand(Command):
    """
    Displays the history of executed commands.
    """

    def __init__(self, history: History) -> None:
        self._history = history

    @property
    def name(self) -> str:
        return "history"

    @property
    def aliases(self) -> list[str]:
        return ["hist"]

    @property
    def category(self) -> str:
        return "Information"

    @property
    def description(self) -> str:
        return "Show previously executed commands."

    @property
    def usage(self) -> str:
        return "history"

    @property
    def examples(self) -> list[str]:
        return [
            "history",
            "hist",
        ]

    def execute(self, arguments: str) -> str:
        """
        Display the stored command history.
        """
        entries = self._history.all()

        if not entries:
            return "Command history is empty."

        lines = [
            "Command History",
            "---------------",
            "",
        ]

        for index, command in enumerate(entries, start=1):
            lines.append(f"{index}. {command}")

        return "\n".join(lines)
