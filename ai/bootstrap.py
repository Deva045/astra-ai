"""
Bootstrap utilities for Astra AI.

Responsible for initializing application components.
"""

from __future__ import annotations

from ai.command_registry import CommandRegistry
from ai.history import History

from ai.commands.help_command import HelpCommand
from ai.commands.version_command import VersionCommand
from ai.commands.clear_command import ClearCommand
from ai.commands.exit_command import ExitCommand
from ai.commands.date_command import DateCommand
from ai.commands.time_command import TimeCommand
from ai.commands.echo_command import EchoCommand
from ai.commands.calculate_command import CalculateCommand
from ai.commands.history_command import HistoryCommand


def create_command_registry(history: History) -> CommandRegistry:
    """
    Create and configure the application's command registry.

    Args:
        history:
            Shared History instance.

    Returns:
        A fully initialized CommandRegistry.
    """

    registry = CommandRegistry()

    registry.register(HelpCommand(registry))
    registry.register(VersionCommand())
    registry.register(ClearCommand())
    registry.register(ExitCommand())
    registry.register(DateCommand())
    registry.register(TimeCommand())
    registry.register(EchoCommand())
    registry.register(CalculateCommand())
    registry.register(HistoryCommand(history))

    return registry
