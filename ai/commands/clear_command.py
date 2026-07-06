"""
Clear command for Astra AI.
"""

from __future__ import annotations

import os

from ai.command import Command


class ClearCommand(Command):
    """
    Clears the terminal screen.
    """

    @property
    def name(self) -> str:
        return "clear"

    @property
    def aliases(self) -> list[str]:
        return ["cls"]

    @property
    def category(self) -> str:
        return "System"

    @property
    def description(self) -> str:
        return "Clear the terminal screen."

    @property
    def usage(self) -> str:
        return "clear"

    @property
    def examples(self) -> list[str]:
        return [
            "clear",
            "cls",
        ]

    def execute(self, arguments: str) -> str:
        """
        Clear the console screen.
        """
        os.system("cls" if os.name == "nt" else "clear")
        return "Screen cleared."
