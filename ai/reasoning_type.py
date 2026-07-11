"""
Reasoning types for Nexus AI.
"""

from __future__ import annotations

from enum import Enum


class ReasoningType(str, Enum):
    """
    Types of reasoning supported by Nexus.
    """

    COMMAND = "command"
    PLANNING = "planning"
    CHAT = "chat"
    AUTOMATION = "automation"
    MEMORY = "memory"
