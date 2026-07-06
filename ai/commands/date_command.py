"""
Date command for Nexus AI.
"""

from __future__ import annotations

from datetime import datetime

from ai.command import Command


class DateCommand(Command):
    """
    Display today's date.
    """

    @property
    def name(self) -> str:
        return "date"

    @property
    def aliases(self) -> list[str]:
        return ["today"]

    @property
    def category(self) -> str:
        return "Utilities"

    @property
    def description(self) -> str:
        return "Show today's date."

    @property
    def usage(self) -> str:
        return "date"

    @property
    def examples(self) -> list[str]:
        return [
            "date",
            "today",
        ]

    def execute(self, arguments: str) -> str:
        return datetime.now().strftime("%A, %d %B %Y")
