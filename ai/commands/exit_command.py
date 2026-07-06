"""
Exit command for Astra AI.
"""

from __future__ import annotations

from ai.command import Command


class ExitCommand(Command):
    """
    Exit Astra AI.
    """

    @property
    def name(self) -> str:
        return "exit"

    @property
    def aliases(self) -> list[str]:
        return ["quit"]

    @property
    def category(self) -> str:
        return "System"

    @property
    def description(self) -> str:
        return "Exit Astra AI."

    @property
    def usage(self) -> str:
        return "exit"

    @property
    def examples(self) -> list[str]:
        return [
            "exit",
            "quit",
        ]

    def execute(self, arguments: str) -> str:
        """
        Return the exit signal.
        """
        return "__EXIT__"
