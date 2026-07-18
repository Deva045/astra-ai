
"""
Base interfaces for Astra AI tools.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Tool(ABC):
    """
    Base class for all Astra AI tools.
    """

    name: str = ""

    description: str = ""

    category: str = "general"

    examples: list[str] = []

    @abstractmethod
    def execute(
        self,
        **kwargs,
    ) -> str:
        """
        Execute the tool.
        """
        raise NotImplementedError
