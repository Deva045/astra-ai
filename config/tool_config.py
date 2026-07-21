
"""
Tool configuration.

Central configuration for Astra AI tool system.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ToolConfig:
    """
    Configuration values for the tool system.
    """

    # Minimum confidence required
    # before a tool is selected.
    confidence_threshold: float = 0.15

    # Maximum confidence score.
    max_confidence: float = 1.0


DEFAULT_TOOL_CONFIG = ToolConfig()
