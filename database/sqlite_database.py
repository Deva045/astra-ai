"""Provides SQLite database management for the Nexus AI memory system.

This module defines the ``SQLiteDatabase`` class, which is responsible for
managing the SQLite connection and initializing the database schema.

The class is intentionally generic and contains no memory-specific business
logic. Repository implementations should use this class instead of directly
interacting with the sqlite3 module.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path


class SQLiteDatabase:
    """Manages the SQLite database connection.

    This class encapsulates connection management, schema initialization,
    transaction handling, and clean shutdown for the SQLite database.

    Attributes:
        database_path: Filesystem path to the SQLite database.
    """

    def __init__(self, database_path: str | Path = "database/memory.db") -> None:
        """Initialize the database manager.

        Args:
            database_path: Path to the SQLite database file.
        """
        self._database_path = Path(database_path)

        self._database_path.parent.mkdir(parents=True, exist_ok=True)

        self._connection = sqlite3.connect(self._database_path)
        self._connection.row_factory = sqlite3.Row

        self.initialize()

    @property
    def connection(self) -> sqlite3.Connection:
        """Return the active SQLite connection."""
        return self._connection

    def initialize(self) -> None:
        """Create all required database tables if they do not exist."""

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                memory_type TEXT NOT NULL,
                importance TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                last_accessed TEXT NOT NULL,
                access_count INTEGER NOT NULL DEFAULT 0,
                metadata TEXT NOT NULL
            )
            """
        )

        self._connection.commit()

    def commit(self) -> None:
        """Commit the current transaction."""
        self._connection.commit()

    def rollback(self) -> None:
        """Rollback the current transaction."""
        self._connection.rollback()

    def close(self) -> None:
        """Close the database connection."""
        self._connection.close()

    def __enter__(self) -> "SQLiteDatabase":
        """Enter the runtime context."""
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        """Exit the runtime context."""
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

        self.close()
