# Session Memory Fundamentals

## Table of Contents

- [What Is Session Memory](#what-is-session-memory) - Understanding the core persistence mechanism
- [Key Characteristics](#key-characteristics) - Properties that define session memory
- [Session Memory Components](#session-memory-components) - The three coordinated documents
  - [activeContext.md](#1-activecontextmd---current-working-state) - Current task and focus state
  - [patterns.md](#2-patternsmd---learned-patterns-and-heuristics) - Discovered patterns and conventions
  - [progress.md](#3-progressmd---task-tracking-and-completion-state) - Task status and dependencies

---

## What Is Session Memory?

Session memory is a structured data storage system that persists an agent's working state across multiple conversations and context window compressions. Unlike conversation history (which can be lost when context is compacted), session memory is explicitly saved to disk and reloaded at each session start.

## Key Characteristics

- **Persistent**: Survives conversation context limits
- **Structured**: Organized into three specialized documents
- **Recoverable**: Can be restored if the agent is interrupted
- **Compaction-safe**: Not affected by context window management

## Session Memory Components

Session memory consists of three coordinated documents stored in the `design/memory/` directory:

### 1. **activeContext.md** - Current Working State

Captures the immediate context needed to continue work:
- Current task being executed
- Active file being edited and its line number
- Open dialog states or interactive prompts
- Recent decisions and their rationale
- Pending operations waiting for completion

### 2. **patterns.md** - Learned Patterns and Heuristics

Records patterns discovered during the session:
- Code patterns and anti-patterns identified
- Architecture insights and recommendations
- Recurring issues and their solutions
- Project-specific conventions learned
- Performance characteristics observed

### 3. **progress.md** - Task Tracking and Completion State

Maintains the complete task execution state:
- Master todo list with task status
- Dependencies between tasks
- Completed tasks with timestamps
- Failed tasks with error details
- Critical milestones reached
- Blocked tasks and their blockers

---

**Version:** 1.0
**Last Updated:** 2025-02-03
