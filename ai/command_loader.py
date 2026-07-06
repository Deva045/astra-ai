"""
Automatic command loader for Nexus AI.
"""

from __future__ import annotations

import importlib
import inspect
import pkgutil

from ai.command import Command
import ai.commands


class CommandLoader:
    """
    Discovers all available command classes.
    """

    def discover(self) -> list[type[Command]]:
        """
        Discover every Command subclass inside ai.commands.

        Returns:
            List of command classes.
        """

        command_classes: list[type[Command]] = []

        package = ai.commands

        for _, module_name, _ in pkgutil.iter_modules(
            package.__path__
        ):
            module = importlib.import_module(
                f"{package.__name__}.{module_name}"
            )

            for _, obj in inspect.getmembers(
                module,
                inspect.isclass,
            ):
                if (
                    issubclass(obj, Command)
                    and obj is not Command
                ):
                    command_classes.append(obj)

        command_classes.sort(key=lambda cls: cls.__name__)

        return command_classes
