"""
Time command for Nexus AI.
"""

from __future__ import annotations

from datetime import datetime

from ai.command import Command


class TimeCommand(Command):
    """
    Display the current time.
    """

    @property
    def name(self) -> str:
        return "time"

    @property
    def aliases(self) -> list[str]:
        return ["clock"]

    @property
    def category(self) -> str:
        return "Utilities"

    @property
    def description(self) -> str:
        return "Show the current time."

    @property
    def usage(self) -> str:
        return "time"

    @property
    def examples(self) -> list[str]:
        return [
            "time",
            "clock",
        ]

    def execute(self, arguments: str) -> str:
        return datetime.now().strftime("%I:%M:%S %p")
