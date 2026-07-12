"""SQLite implementation of the Nexus AI memory repository.

This module provides the SQLite-backed implementation of the
``MemoryRepository`` interface.

The repository is responsible only for persistence. All business logic
belongs in the memory manager or higher application layers.
"""

from __future__ import annotations

from ai.memory_importance import MemoryImportance
from ai.memory_mapper import memory_to_row, row_to_memory
from ai.memory_query import MemoryQuery
from ai.memory_record import MemoryRecord
from ai.memory_repository import MemoryRepository
from ai.memory_result import MemoryResult
from database.sqlite_database import SQLiteDatabase


class SQLiteMemoryRepository(MemoryRepository):
    """SQLite-backed implementation of ``MemoryRepository``."""

    _IMPORTANCE_ORDER: dict[MemoryImportance, int] = {
        MemoryImportance.LOW: 0,
        MemoryImportance.MEDIUM: 1,
        MemoryImportance.HIGH: 2,
        MemoryImportance.CRITICAL: 3,
    }

    def __init__(self, database: SQLiteDatabase) -> None:
        """Initialize the repository.

        Args:
            database: SQLite database manager.
        """
        self._database = database

    def add(self, memory: MemoryRecord) -> None:
        """Store a memory record.

        Args:
            memory: Memory to store.
        """
        self._database.connection.execute(
            """
            INSERT INTO memories (
                id,
                content,
                memory_type,
                importance,
                created_at,
                updated_at,
                last_accessed,
                access_count,
                metadata
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            memory_to_row(memory),
        )
        self._database.commit()

    def get(self, memory_id: str) -> MemoryRecord | None:
        """Retrieve a memory by its identifier.

        Args:
            memory_id: Memory identifier.

        Returns:
            The matching memory if found, otherwise ``None``.
        """
        cursor = self._database.connection.execute(
            """
            SELECT *
            FROM memories
            WHERE id = ?
            """,
            (memory_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return row_to_memory(row)

    def update(self, memory: MemoryRecord) -> None:
        """Update an existing memory.

        Args:
            memory: Updated memory.
        """
        self._database.connection.execute(
            """
            UPDATE memories
            SET
                content = ?,
                memory_type = ?,
                importance = ?,
                created_at = ?,
                updated_at = ?,
                last_accessed = ?,
                access_count = ?,
                metadata = ?
            WHERE id = ?
            """,
            (
                memory.content,
                memory.memory_type.value,
                memory.importance.value,
                memory.created_at.isoformat(),
                memory.updated_at.isoformat(),
                memory.last_accessed.isoformat(),
                memory.access_count,
                __import__("json").dumps(memory.metadata),
                memory.id,
            ),
        )

        self._database.commit()

    def delete(self, memory_id: str) -> None:
        """Delete a memory.

        Args:
            memory_id: Memory identifier.
        """
        self._database.connection.execute(
            """
            DELETE FROM memories
            WHERE id = ?
            """,
            (memory_id,),
        )

        self._database.commit()

    def search(self, query: MemoryQuery) -> MemoryResult:
        """Search stored memories.

        Args:
            query: Search criteria.

        Returns:
            Search results.
        """
        memories = self.list_all()

        results: list[MemoryRecord] = []

        for memory in memories:
            if query.text:
                if query.text.lower() not in memory.content.lower():
                    continue

            if query.memory_types:
                if memory.memory_type not in query.memory_types:
                    continue

            if query.minimum_importance is not None:
                if (
                    self._IMPORTANCE_ORDER[memory.importance]
                    < self._IMPORTANCE_ORDER[query.minimum_importance]
                ):
                    continue

            results.append(memory)

        total_matches = len(results)

        results = results[: query.limit]

        return MemoryResult(
            memories=results,
            total_matches=total_matches,
            returned_count=len(results),
            truncated=total_matches > len(results),
        )

    def list_all(self) -> list[MemoryRecord]:
        """Return every stored memory.

        Returns:
            All memories.
        """
        cursor = self._database.connection.execute(
            """
            SELECT *
            FROM memories
            ORDER BY created_at ASC
            """
        )

        return [row_to_memory(row) for row in cursor.fetchall()]

    def clear(self) -> None:
        """Remove every stored memory."""
        self._database.connection.execute(
            """
            DELETE FROM memories
            """
        )

        self._database.commit()

    def count(self) -> int:
        """Return the number of stored memories.

        Returns:
            Total memory count.
        """
        cursor = self._database.connection.execute(
            """
            SELECT COUNT(*) AS total
            FROM memories
            """
        )

        row = cursor.fetchone()

        if row is None:
            return 0

        return int(row["total"])
