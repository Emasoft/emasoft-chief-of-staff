# Manage Progress Tracking

## Table of Contents

1. [Purpose](#purpose)
2. [Part Files](#part-files)
3. [Quick Reference](#quick-reference)

---

## Purpose

Progress tracking maintains accurate record of task status, dependencies, and completion. Effective progress tracking enables:
- Clear visibility of work status
- Dependency management
- Milestone tracking
- Recovery after compaction
- Progress reporting

---

## Part Files

This reference is split into 4 parts for easier navigation:

### Part 1: Structure and States
**File**: [08-manage-progress-tracking-part1-structure-states.md](./08-manage-progress-tracking-part1-structure-states.md)

**Contents**:
- 1.1 Progress Tracker Structure
- 1.2 File Location (`.session_memory/progress_tracker.md`)
- 1.3 Standard Structure Template
- 1.4 Task States (Active, Completed, Blocked, Planned)
- 1.5 State Transitions

**When to read**: When you need to understand the tracker file format or task states.

---

### Part 2: Task Management Procedures
**File**: [08-manage-progress-tracking-part2-task-management.md](./08-manage-progress-tracking-part2-task-management.md)

**Contents**:
- 2.1 Procedure 1: Add New Task
- 2.2 Procedure 2: Start Task (Planned → Active)
- 2.3 Procedure 3: Complete Task (Active → Completed)
- 2.4 Procedure 4: Block Task (Active → Blocked)
- 2.5 Procedure 5: Unblock Task (Blocked → Active)
- 2.6 Procedure 6: Update Task Progress

**When to read**: When you need to add, start, complete, block, or update a task.

---

### Part 3: Dependencies and Snapshots
**File**: [08-manage-progress-tracking-part3-dependencies-snapshots.md](./08-manage-progress-tracking-part3-dependencies-snapshots.md)

**Contents**:
- 3.1 Dependency Management
  - 3.1.1 Recording Dependencies (linear, parallel, complex)
  - 3.1.2 Dependency Tracking Script
- 3.2 Progress Snapshots
  - 3.2.1 When to Create Snapshots
  - 3.2.2 Snapshot Procedure
  - 3.2.3 Restore from Snapshot

**When to read**: When managing task dependencies or creating/restoring snapshots.

---

### Part 4: Examples and Troubleshooting
**File**: [08-manage-progress-tracking-part4-examples-troubleshooting.md](./08-manage-progress-tracking-part4-examples-troubleshooting.md)

**Contents**:
- 4.1 Example 1: Complete Task Lifecycle (Planned → Active → Blocked → Active → Completed)
- 4.2 Example 2: Dependency Chain (sequential tasks)
- 4.3 Example 3: Parallel Tasks with Merge
- 4.4 Troubleshooting
  - 4.4.1 Problem: Task Counts Out of Sync
  - 4.4.2 Problem: Circular Dependencies
  - 4.4.3 Problem: Progress Tracker Lost
  - 4.4.4 Problem: Too Many Tasks in Active

**When to read**: When you need examples or encounter problems.

---

## Quick Reference

### Task States Summary

| State | Checkbox | Location | Next States |
|-------|----------|----------|-------------|
| Planned | `- [ ]` | Future Tasks | Active |
| Active | `- [ ]` | Active Tasks | Completed, Blocked |
| Blocked | `- [ ]` | Blocked Tasks | Active, Completed |
| Completed | `- [x]` | Completed Tasks | (terminal) |

### Key Files

| File | Purpose |
|------|---------|
| `.session_memory/progress_tracker.md` | Main progress tracker |
| `.session_memory/progress/progress_*.md` | Snapshots |
| `.session_memory/progress/progress_latest.md` | Symlink to latest snapshot |

### Common Operations

| Operation | See Part |
|-----------|----------|
| Add new task | Part 2, Procedure 1 |
| Start working on task | Part 2, Procedure 2 |
| Mark task complete | Part 2, Procedure 3 |
| Block a task | Part 2, Procedure 4 |
| Unblock a task | Part 2, Procedure 5 |
| Update progress % | Part 2, Procedure 6 |
| Check dependencies | Part 3, Section 3.1.2 |
| Create snapshot | Part 3, Section 3.2.2 |
| Restore snapshot | Part 3, Section 3.2.3 |
| Fix task counts | Part 4, Troubleshooting |
