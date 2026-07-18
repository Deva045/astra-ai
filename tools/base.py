"""
Base interfaces for Astra AI tools.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Tool(ABC):
    """
    Base class for all AI tools.
    """

    name: str = ""

    description: str = ""

    @abstractmethod
    def execute(
        self,
        **kwargs,
    ) -> str:
        """
        Execute the tool.
        """
        raise NotImplementedError
