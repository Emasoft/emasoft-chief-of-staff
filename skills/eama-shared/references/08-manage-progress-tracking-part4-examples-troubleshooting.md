# Progress Tracking: Examples and Troubleshooting

## Table of Contents
1. [Examples](#examples)
   - 1.1 [Example 1: Complete Task Lifecycle](#example-1-complete-task-lifecycle)
   - 1.2 [Example 2: Dependency Chain](#example-2-dependency-chain)
   - 1.3 [Example 3: Parallel Tasks with Merge](#example-3-parallel-tasks-with-merge)
2. [Troubleshooting](#troubleshooting)
   - 2.1 [Problem: Task Counts Out of Sync](#problem-task-counts-out-of-sync)
   - 2.2 [Problem: Circular Dependencies](#problem-circular-dependencies)
   - 2.3 [Problem: Progress Tracker Lost](#problem-progress-tracker-lost)
   - 2.4 [Problem: Too Many Tasks in Active](#problem-too-many-tasks-in-active)

---

## Examples

### Example 1: Complete Task Lifecycle

```markdown
## 1. Add Task (Planned)

- [ ] Implement user authentication
  - **Priority**: High
  - **Added**: 2026-01-01 08:00 UTC
  - **Dependencies**: None
  - **Progress**: 0%
  - **Status**: Planned

## 2. Start Task (Active)

- [ ] Implement user authentication
  - **Priority**: High
  - **Added**: 2026-01-01 08:00 UTC
  - **Started**: 2026-01-01 09:00 UTC
  - **Dependencies**: None
  - **Progress**: 10%
  - **Status**: In progress

## 3. Update Progress

- [ ] Implement user authentication
  - **Priority**: High
  - **Started**: 2026-01-01 09:00 UTC
  - **Progress**: 60%
  - **Status**: In progress
  - **Note**: OAuth setup complete, working on JWT

## 4. Hit Blocker (Blocked)

- [ ] Implement user authentication
  - **Priority**: High
  - **Started**: 2026-01-01 09:00 UTC
  - **Progress**: 60%
  - **Blocked By**: Need decision on token expiry (Q1)
  - **Blocking Since**: 2026-01-01 12:00 UTC
  - **Status**: Blocked

## 5. Resolve Blocker (Active)

- [ ] Implement user authentication
  - **Priority**: High
  - **Started**: 2026-01-01 09:00 UTC
  - **Progress**: 75%
  - **Previously Blocked By**: Token expiry decision (resolved: 1 hour)
  - **Unblocked**: 2026-01-01 13:00 UTC
  - **Status**: In progress

## 6. Complete Task (Completed)

- [x] Implement user authentication
  - **Started**: 2026-01-01 09:00 UTC
  - **Completed**: 2026-01-01 15:00 UTC
  - **Duration**: 6 hours (actual work: 5 hours, blocked: 1 hour)
  - **Outcome**: Successfully implemented OAuth2 with GitHub and JWT tokens
  - **Learnings**: 1-hour token expiry works well with refresh tokens, session cookies had browser compatibility issues
```

---

### Example 2: Dependency Chain

```markdown
## Active Tasks

- [ ] Task A: Set up OAuth app in GitHub
  - **Priority**: High
  - **Started**: 2026-01-01 09:00 UTC
  - **Dependencies**: None
  - **Progress**: 90%
  - **Status**: In progress

- [ ] Task B: Implement OAuth callback handler
  - **Priority**: High
  - **Added**: 2026-01-01 09:00 UTC
  - **Dependencies**: Task A
  - **Progress**: 0%
  - **Status**: Waiting for Task A

- [ ] Task C: Implement token refresh
  - **Priority**: Medium
  - **Added**: 2026-01-01 09:00 UTC
  - **Dependencies**: Task B
  - **Progress**: 0%
  - **Status**: Waiting for Task B

## Task Dependencies

```
Task A (90% complete)
  └─> Task B (waiting)
      └─> Task C (waiting)
```

**Critical Path**: A → B → C (sequential)
**Status**: On track, A nearly complete
```

---

### Example 3: Parallel Tasks with Merge

```markdown
## Active Tasks

- [ ] Task X: Write unit tests
  - **Priority**: High
  - **Started**: 2026-01-01 10:00 UTC
  - **Dependencies**: None
  - **Progress**: 50%
  - **Status**: In progress

- [ ] Task Y: Write integration tests
  - **Priority**: High
  - **Started**: 2026-01-01 10:00 UTC
  - **Dependencies**: None
  - **Progress**: 40%
  - **Status**: In progress

- [ ] Task Z: Run full test suite and deploy
  - **Priority**: High
  - **Added**: 2026-01-01 10:00 UTC
  - **Dependencies**: Task X, Task Y
  - **Progress**: 0%
  - **Status**: Waiting for X and Y

## Task Dependencies

```
Task X (50%) ─┐
              ├─> Task Z (waiting)
Task Y (40%) ─┘
```

**Parallelization**: X and Y proceeding in parallel
**Status**: Z cannot start until both X and Y complete
```

---

## Troubleshooting

### Problem: Task Counts Out of Sync

**Symptoms**: Header shows wrong number of active/completed tasks

**Solution**:
```bash
# Recount tasks
active=$(grep -c "^- \[ \]" .session_memory/progress_tracker.md)
completed=$(grep -c "^- \[x\]" .session_memory/progress_tracker.md)

# Update header
sed -i '' "s/\*\*Active Tasks\*\*: [0-9]\+/**Active Tasks**: $active/" .session_memory/progress_tracker.md
sed -i '' "s/\*\*Completed Tasks\*\*: [0-9]\+/**Completed Tasks**: $completed/" .session_memory/progress_tracker.md
```

---

### Problem: Circular Dependencies

**Symptoms**: Task A depends on B, Task B depends on A

**Solution**:
```markdown
# Resolution Steps:
1. Identify the circular dependency
2. Break the circle by:
   - Splitting one task into two parts
   - Removing unnecessary dependency
   - Reordering task implementation
3. Update dependency graph
```

---

### Problem: Progress Tracker Lost

**Symptoms**: progress_tracker.md missing or corrupted

**Solution**:
```bash
# Restore from latest snapshot
cp .session_memory/progress/progress_latest.md .session_memory/progress_tracker.md

# Or from archived state
latest_archive=$(ls -t .session_memory/archived/pre_compaction_*/progress_tracker.md | head -1)
cp "$latest_archive" .session_memory/progress_tracker.md
```

---

### Problem: Too Many Tasks in Active

**Symptoms**: Active Tasks section has 10+ items, hard to track

**Solution**:
```bash
# Review active tasks
grep "^- \[ \]" .session_memory/progress_tracker.md

# Recommended actions:
# 1. Move paused tasks to Future Tasks
# 2. Keep only actively worked-on tasks in Active
# 3. Maximum 3-5 active tasks at once
```

---

**Previous**: See [Part 3: Dependencies and Snapshots](./08-manage-progress-tracking-part3-dependencies-snapshots.md) for dependency management.

**Back to Index**: See [08-manage-progress-tracking.md](./08-manage-progress-tracking.md) for the overview.
