"""
Echo command for Nexus AI.
"""

from __future__ import annotations

from ai.command import Command


class EchoCommand(Command):
    """
    Echo the supplied text.
    """

    @property
    def name(self) -> str:
        return "echo"

    @property
    def aliases(self) -> list[str]:
        return ["repeat"]

    @property
    def category(self) -> str:
        return "Utilities"

    @property
    def description(self) -> str:
        return "Repeat the supplied text."

    @property
    def usage(self) -> str:
        return "echo <text>"

    @property
    def examples(self) -> list[str]:
        return [
            "echo Hello",
            "repeat Hello Nexus",
        ]

    def execute(self, arguments: str) -> str:
        if not arguments.strip():
            return "Nothing to echo."

        return arguments
