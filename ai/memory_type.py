"""Defines the memory types used throughout the Nexus AI memory system.

This module contains the ``MemoryType`` enumeration, which categorizes the
different kinds of memories managed by the application.

Using an enumeration instead of raw string values improves type safety,
readability, maintainability, and consistency across the codebase.
"""

from enum import Enum


class MemoryType(str, Enum):
    """Represents the category of a stored memory.

    The memory type determines how a memory should be interpreted and
    processed by the memory system. It enables filtering, retrieval,
    prioritization, and future extensibility while keeping the codebase
    strongly typed.

    Attributes:
        SHORT_TERM: Temporary conversational context.
        LONG_TERM: Persistent memory retained across sessions.
        SYSTEM: Internal system-generated memory.
        USER: User profile or identity information.
        FACT: Facts learned from conversations.
        PREFERENCE: User preferences and personalization data.
        TASK: Tasks or reminders.
        CONVERSATION: Conversation history entries.
    """

    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    SYSTEM = "system"
    USER = "user"
    FACT = "fact"
    PREFERENCE = "preference"
    TASK = "task"
    CONVERSATION = "conversation"
