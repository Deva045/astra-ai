# Nexus AI Memory API

## Overview

The Memory API provides a storage-independent interface for working with memories throughout Nexus AI.

The application communicates only with the `MemoryManager`, which delegates persistence to a `MemoryRepository` implementation.

```
AI Engine
    │
    ▼
MemoryManager
    │
    ▼
MemoryRepository
    │
    ▼
SQLiteMemoryRepository
```

---

# Public API

## MemoryManager

The `MemoryManager` is the primary entry point for all memory operations.

---

### add_memory()

Stores a new memory.

```python
memory_manager.add_memory(memory)
```

---

### get_memory()

Retrieves a memory by its unique identifier.

```python
memory = memory_manager.get_memory(memory_id)
```

Returns:

- MemoryRecord
- None

---

### update_memory()

Updates an existing memory.

```python
memory_manager.update_memory(memory)
```

---

### delete_memory()

Deletes a memory.

```python
memory_manager.delete_memory(memory_id)
```

---

### search_memories()

Searches stored memories.

```python
result = memory_manager.search_memories(query)
```

Returns:

```
MemoryResult
```

---

### list_memories()

Returns every stored memory.

```python
memories = memory_manager.list_memories()
```

---

### clear_memories()

Deletes every stored memory.

```python
memory_manager.clear_memories()
```

---

### memory_count()

Returns the total number of stored memories.

```python
count = memory_manager.memory_count()
```

---

# MemoryRepository Interface

Every repository implementation must implement:

- add()
- get()
- update()
- delete()
- search()
- list_all()
- clear()
- count()

This allows the memory backend to be replaced without changing higher-level code.

---

# MemoryQuery

Used for searches.

Example:

```python
MemoryQuery(
    text="Python",
    limit=5,
)
```

Supports:

- text search
- memory type filtering
- importance filtering
- result limits

---

# MemoryResult

Returned by every search.

Contains:

- memories
- total_matches
- returned_count
- truncated

---

# MemoryRecord

Represents one stored memory.

Fields:

- id
- content
- memory_type
- importance
- created_at
- updated_at
- last_accessed
- access_count
- metadata

---

# Thread Safety

The current implementation is intended for a single local application instance.

Future versions may introduce synchronization for concurrent access if required.

---

# Future Extensions

The API has been designed to support future enhancements without breaking existing code.

Planned extensions include:

- Semantic search
- Embedding-based retrieval
- Memory ranking
- Memory summarization
- Memory consolidation
- Multiple storage backends
- Cloud synchronization (optional)

---

# Stability

Current status:

- Storage-independent
- Offline-first
- Fully typed
- Production-ready
- Backed by SQLite
- 174/174 tests passing
