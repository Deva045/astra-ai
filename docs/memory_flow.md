# Nexus AI Memory Flow

## Overview

This document describes how information flows through the Nexus AI Memory System.

The architecture is designed to be modular, offline-first, and storage-independent.

---

# High-Level Flow

```
User
 │
 ▼
AI Engine
 │
 ▼
Conversation
 │
 ▼
Memory Extractor
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

# Conversation Flow

When the user sends a message:

```
User Input
      │
      ▼
Conversation.add_user()
      │
      ▼
MemoryExtractor.extract()
      │
      ▼
MemoryManager.add_memory()
      │
      ▼
SQLiteMemoryRepository.add()
      │
      ▼
Database Commit
```

---

# Retrieval Flow

Before generating a response:

```
Current User Message
         │
         ▼
MemoryQuery
         │
         ▼
MemoryManager.search_memories()
         │
         ▼
SQLiteMemoryRepository.search()
         │
         ▼
MemoryResult
         │
         ▼
PromptBuilder
         │
         ▼
LLM
```

---

# Prompt Generation

The final prompt consists of:

- System prompt
- Conversation history
- Relevant memories
- Current user message

```
System Prompt
        │
        ▼
Conversation History
        │
        ▼
Relevant Memories
        │
        ▼
Current User Message
        │
        ▼
LLM
```

---

# Memory Storage Pipeline

Each stored memory follows this lifecycle:

```
Extract
   │
   ▼
Validate
   │
   ▼
Create MemoryRecord
   │
   ▼
Repository
   │
   ▼
SQLite
```

---

# Search Pipeline

```
MemoryQuery
      │
      ▼
Repository
      │
      ▼
Filtering
      │
      ▼
MemoryResult
```

---

# Components

## AIEngine

Coordinates the complete pipeline.

---

## Conversation

Stores short-term conversation history.

---

## MemoryExtractor

Determines whether a user message should become a long-term memory.

---

## MemoryManager

Coordinates all memory operations.

---

## MemoryRepository

Abstract persistence interface.

---

## SQLiteMemoryRepository

SQLite implementation of the repository.

---

## SQLiteDatabase

Handles SQLite connections, schema initialization, transactions, and commits.

---

# Current Implementation

Implemented:

- Memory extraction
- Memory persistence
- Memory retrieval
- Conversation integration
- Prompt integration
- SQLite backend

---

# Future Flow

Future releases will extend the pipeline:

```
User
 │
 ▼
Conversation
 │
 ▼
Memory Extraction
 │
 ▼
Semantic Search
 │
 ▼
Memory Ranking
 │
 ▼
Prompt Builder
 │
 ▼
LLM
```

This future architecture can be implemented without changing the existing public memory API.
