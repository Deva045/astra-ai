"""
Version command for Astra AI.
"""

from __future__ import annotations

from ai.command import Command


class VersionCommand(Command):
    """
    Displays the current Astra AI version.
    """

    @property
    def name(self) -> str:
        return "version"

    @property
    def aliases(self) -> list[str]:
        return ["ver", "about"]

    @property
    def category(self) -> str:
        return "Information"

    @property
    def description(self) -> str:
        return "Show the current Astra AI version."

    @property
    def usage(self) -> str:
        return "version"

    @property
    def examples(self) -> list[str]:
        return [
            "version",
            "ver",
            "about",
        ]

    def execute(self, arguments: str) -> str:
        return "Astra AI v0.1.0 (Development Build)"
