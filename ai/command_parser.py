"""
Command parser for Astra AI.

Parses raw user input into a command name and arguments.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ParsedCommand:
    """
    Represents a parsed command.
    """

    name: str
    arguments: str


class CommandParser:
    """
    Parses raw user input into structured command data.
    """

    def parse(self, text: str) -> ParsedCommand | None:
        """
        Parse user input.

        Args:
            text: Raw user input.

        Returns:
            ParsedCommand if valid, otherwise None.
        """
        text = text.strip()

        if not text:
            return None

        parts = text.split(maxsplit=1)

        name = parts[0].lower()
        arguments = parts[1] if len(parts) > 1 else ""

        return ParsedCommand(
            name=name,
            arguments=arguments,
        )
