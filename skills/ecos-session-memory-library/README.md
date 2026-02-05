# Session Memory Skill

## Purpose

Critical persistence mechanism enabling the EOA orchestrator to maintain continuity across multiple interactions, survive context window compaction, and recover gracefully from interruptions.

## When to Use

- When initializing a new orchestration session
- When recovering from context compaction
- When resuming interrupted work
- When persisting learned patterns

## Key Features

- Three-document memory structure
- Compaction-safe persistence
- Config snapshot integration
- Drift detection and resolution

## Memory Components

### 1. activeContext.md
- Current task being executed
- Active file and line number
- Open dialog states
- Recent decisions and rationale
- Pending operations

### 2. patterns.md
- Code patterns and anti-patterns
- Architecture insights
- Recurring issues and solutions
- Project conventions
- Performance characteristics

### 3. progress.md
- Master todo list with status
- Task dependencies
- Completion state
- Blocked items

## Entry Point

See [SKILL.md](./SKILL.md) for complete instructions.

## Related Skills

- `eama-role-routing` - Uses session memory for continuity
- `verification-patterns` - Task completion tracking
