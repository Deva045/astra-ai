"""
Shared command context for Astra AI.
"""

from __future__ import annotations

from dataclasses import dataclass

from ai.command_registry import CommandRegistry
from ai.history import History


@dataclass(slots=True)
class CommandContext:
    """
    Shared services available to commands.
    """

    registry: CommandRegistry
    history: History
