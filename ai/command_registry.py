"""
Command registry for Nexus AI.

Stores and retrieves executable commands.
"""

from __future__ import annotations

from typing import Dict

from ai.command import Command


class CommandRegistry:
    """
    Stores all available commands.
    """

    def __init__(self) -> None:
        self._commands: Dict[str, Command] = {}
        self._primary_commands: Dict[str, Command] = {}

    def register(self, command: Command) -> None:
        """
        Register a command and all of its aliases.

        Raises:
            ValueError:
                If the command name or any alias is already registered.
        """
        primary_name = command.name.lower()

        if primary_name in self._commands:
            raise ValueError(
                f"Command '{command.name}' is already registered."
            )

        self._commands[primary_name] = command
        self._primary_commands[primary_name] = command

        for alias in command.aliases:
            alias = alias.lower()

            if alias in self._commands:
                raise ValueError(
                    f"Alias '{alias}' is already registered."
                )

            self._commands[alias] = command

    def get(self, name: str) -> Command | None:
        """
        Retrieve a command by its name or alias.
        """
        return self._commands.get(name.lower())

    def exists(self, name: str) -> bool:
        """
        Check whether a command name or alias exists.
        """
        return name.lower() in self._commands

    def list_commands(self) -> list[str]:
        """
        Return a sorted list of primary command names.
        """
        return sorted(self._primary_commands.keys())
