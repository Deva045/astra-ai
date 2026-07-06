"""
Built-in commands for Nexus AI.
"""

from ai.commands.calculate_command import CalculateCommand
from ai.commands.clear_command import ClearCommand
from ai.commands.date_command import DateCommand
from ai.commands.echo_command import EchoCommand
from ai.commands.exit_command import ExitCommand
from ai.commands.help_command import HelpCommand
from ai.commands.history_command import HistoryCommand
from ai.commands.time_command import TimeCommand
from ai.commands.version_command import VersionCommand

__all__ = [
    "CalculateCommand",
    "ClearCommand",
    "DateCommand",
    "EchoCommand",
    "ExitCommand",
    "HelpCommand",
    "HistoryCommand",
    "TimeCommand",
    "VersionCommand",
]
