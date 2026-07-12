# Nexus AI Memory Database

## Overview

The Nexus AI Memory System currently uses SQLite as its storage backend.

The database layer is intentionally isolated from the rest of the application through the `MemoryRepository` abstraction.

```
AI Engine
     │
     ▼
Memory Manager
     │
     ▼
Memory Repository
     │
     ▼
SQLite Repository
     │
     ▼
SQLite Database
     │
     ▼
memory.db
```

---

# Database File

Current database:

```
database/memory.db
```

The database is automatically created during application startup if it does not already exist.

---

# Current Schema

Table:

```
memories
```

Columns:

| Column | Type | Description |
|---------|------|-------------|
| id | TEXT | Primary key |
| content | TEXT | Memory text |
| memory_type | TEXT | Memory category |
| importance | TEXT | Importance level |
| created_at | TEXT | Creation timestamp |
| updated_at | TEXT | Last update timestamp |
| last_accessed | TEXT | Last retrieval timestamp |
| access_count | INTEGER | Number of accesses |
| metadata | TEXT | JSON metadata |

---

# Primary Key

```
id
```

Every memory is uniquely identified by its UUID.

---

# Metadata

Metadata is stored as JSON.

Example:

```json
{
    "source": "conversation",
    "confidence": 1.0
}
```

---

# Transactions

The SQLiteDatabase class manages transactions.

Supported operations:

- commit()
- rollback()

Context manager support:

```python
with SQLiteDatabase() as database:
    ...
```

Successful execution:

```
commit()
```

Exception:

```
rollback()
```

---

# Repository Responsibilities

The SQLiteMemoryRepository is responsible for:

- Insert
- Retrieve
- Update
- Delete
- Search
- Count
- List
- Clear

It contains no business logic.

---

# Data Flow

```
MemoryRecord
      │
      ▼
Memory Mapper
      │
      ▼
SQLite Row
      │
      ▼
SQLite Database
```

Reading follows the reverse path.

---

# Current Performance

Current implementation:

- Simple text search
- SQLite persistence
- In-memory filtering after retrieval
- Offline-first

Designed for desktop-scale personal assistants.

---

# Future Enhancements

Possible future improvements:

- SQL-based filtering
- Indexed searches
- Full-text search (FTS5)
- Semantic vector search
- ChromaDB backend
- Automatic cleanup policies

These enhancements can be introduced without changing the public Memory API.

---

# Design Principles

The database layer follows these principles:

- Single Responsibility
- Repository Pattern
- Storage Independence
- Offline First
- Production Quality
- Fully Testable

---

# Current Status

Storage backend:

- SQLite

Database:

- memory.db

Architecture:

- Repository-based

Persistence:

- Automatic

Current test status:

```
174 / 174 tests passing
```
