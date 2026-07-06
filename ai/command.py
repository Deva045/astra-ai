"""
Base command abstraction for Astra AI.

Every executable command inherits from this class.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Command(ABC):
    """
    Base class for all Astra commands.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Primary command name.
        """
        raise NotImplementedError

    @property
    def aliases(self) -> list[str]:
        """
        Alternative names.

        Example:
            calculate
            calc
            math
        """
        return []

    @property
    def category(self) -> str:
        """
        Command category.
        """
        return "General"

    @property
    def description(self) -> str:
        """
        Human-readable description.
        """
        return "No description available."

    @property
    def usage(self) -> str:
        """
        Usage string.
        """
        return self.name

    @property
    def examples(self) -> list[str]:
        """
        Example command usages.
        """
        return []

    @abstractmethod
    def execute(self, arguments: str) -> str:
        """
        Execute the command.

        Args:
            arguments:
                User supplied arguments.

        Returns:
            Command output.
        """
        raise NotImplementedError
