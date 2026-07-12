"""Provides conversion utilities for memory persistence.

This module contains helper functions for converting between
``MemoryRecord`` objects and SQLite-compatible representations.

The mapper isolates serialization and deserialization logic from the
repository, keeping the repository focused solely on persistence.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime

from ai.memory_importance import MemoryImportance
from ai.memory_record import MemoryRecord
from ai.memory_type import MemoryType


def memory_to_row(memory: MemoryRecord) -> tuple:
    """Convert a memory record into SQLite-compatible values.

    Args:
        memory: Memory record to convert.

    Returns:
        A tuple matching the database schema.
    """
    return (
        memory.id,
        memory.content,
        memory.memory_type.value,
        memory.importance.value,
        memory.created_at.isoformat(),
        memory.updated_at.isoformat(),
        memory.last_accessed.isoformat(),
        memory.access_count,
        json.dumps(memory.metadata),
    )


def row_to_memory(row: sqlite3.Row) -> MemoryRecord:
    """Convert a SQLite row into a MemoryRecord.

    Args:
        row: SQLite row returned from a query.

    Returns:
        A populated MemoryRecord.
    """
    return MemoryRecord(
        id=row["id"],
        content=row["content"],
        memory_type=MemoryType(row["memory_type"]),
        importance=MemoryImportance(row["importance"]),
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"]),
        last_accessed=datetime.fromisoformat(row["last_accessed"]),
        access_count=row["access_count"],
        metadata=json.loads(row["metadata"]),
    )
