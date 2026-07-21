"""
AI Response Models.

Provides structured AI responses while maintaining
compatibility with the existing Router system.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ResponseStatus(str, Enum):
    """
    Response execution status.
    """

    SUCCESS = "success"
    ERROR = "error"


@dataclass(slots=True)
class Response:
    """
    Existing response model used by Router.

    Kept for backward compatibility.
    """

    success: bool
    message: str


@dataclass(slots=True)
class AIResponse:
    """
    Extended structured AI response.

    Used internally for future AI features.
    """

    content: str

    status: ResponseStatus = (
        ResponseStatus.SUCCESS
    )

    provider: str = ""

    model: str = ""

    metadata: dict[str, str] = field(
        default_factory=dict
    )

    @property
    def is_success(self) -> bool:
        """
        Return True if response succeeded.
        """

        return (
            self.status
            == ResponseStatus.SUCCESS
        )

    @classmethod
    def error(
        cls,
        message: str,
    ) -> "AIResponse":
        """
        Create an error response.
        """

        return cls(
            content=message,
            status=ResponseStatus.ERROR,
        )
