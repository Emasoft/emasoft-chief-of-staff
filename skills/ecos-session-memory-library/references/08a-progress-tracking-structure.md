# Progress Tracking: Structure and Task Management

## Table of Contents
1. [When you need to understand the purpose](#purpose)
2. [Understanding tracker structure](#progress-tracker-structure)
3. [Understanding task states](#task-states)
4. [How to manage tasks](#task-management-procedures)

---

## Purpose

Progress tracking maintains accurate record of task status, dependencies, and completion. Effective progress tracking enables:
- Clear visibility of work status
- Dependency management
- Milestone tracking
- Recovery after compaction
- Progress reporting

## Progress Tracker Structure

### File Location
`.session_memory/progress_tracker.md`

### Standard Structure

```markdown
# Progress Tracker

**Last Updated**: 2026-01-01 14:30 UTC
**Active Tasks**: 3
**Completed Tasks**: 12
**Blocked Tasks**: 1

---

## Active Tasks

- [ ] Task 1 - Brief description
  - **Priority**: High/Medium/Low
  - **Started**: 2026-01-01 10:00 UTC
  - **Estimated Completion**: 2026-01-01 16:00 UTC
  - **Dependencies**: None
  - **Progress**: 60%
  - **Status**: In progress

- [ ] Task 2 - Brief description
  - **Priority**: Medium
  - **Started**: 2026-01-01 11:00 UTC
  - **Dependencies**: Task 1
  - **Progress**: 20%
  - **Status**: Waiting for dependency

---

## Completed Tasks

- [x] Task 0 - Brief description
  - **Started**: 2026-01-01 08:00 UTC
  - **Completed**: 2026-01-01 10:00 UTC
  - **Duration**: 2 hours
  - **Outcome**: Successfully implemented
  - **Learnings**: Key insight 1, Key insight 2

---

## Blocked Tasks

- [ ] Task 3 - Brief description
  - **Priority**: High
  - **Blocked By**: Open question Q1
  - **Blocking Since**: 2026-01-01 12:00 UTC
  - **Impact**: Cannot proceed with Task 4

---

## Task Dependencies

```
Task 1 (active)
  └─> Task 2 (waiting)
      └─> Task 4 (planned)

Task 3 (blocked by Q1)
  └─> Task 5 (planned)
```

---

## Milestones

### Milestone 1: Authentication System
**Target**: 2026-01-05
**Progress**: 75%
**Tasks**:
- [x] OAuth setup
- [x] JWT implementation
- [ ] Role management
- [ ] Integration tests

---

## Future Tasks

- [ ] Task 6 - Brief description (Planned)
- [ ] Task 7 - Brief description (Planned)
```

## Task States

### State Definitions

| State | Checkbox | Meaning | Location |
|-------|----------|---------|----------|
| Active | `- [ ]` | Currently being worked on | Active Tasks |
| Completed | `- [x]` | Finished successfully | Completed Tasks |
| Blocked | `- [ ]` | Cannot proceed due to blocker | Blocked Tasks |
| Planned | `- [ ]` | Not yet started | Future Tasks |

### State Transitions

```
Planned → Active
  Trigger: Start working on task

Active → Completed
  Trigger: Task finished successfully

Active → Blocked
  Trigger: Hit blocker or dependency

Blocked → Active
  Trigger: Blocker resolved

Blocked → Completed
  Trigger: Blocker resolved and task finished
```

## Task Management Procedures

### Procedure 1: Add New Task

```bash
#!/bin/bash
# add_task.sh - Add new task to progress tracker

add_task() {
    local task_name="$1"
    local priority="$2"
    local dependencies="$3"

    timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

    cat >> .session_memory/progress_tracker.md << EOF

- [ ] $task_name
  - **Priority**: $priority
  - **Added**: $timestamp
  - **Dependencies**: ${dependencies:-None}
  - **Progress**: 0%
  - **Status**: Planned

EOF

    # Update task counts
    update_task_counts

    echo "Task added: $task_name"
}

# Usage
add_task "Implement user authentication" "High" "None"
```

### Procedure 2: Start Task (Planned to Active)

```bash
#!/bin/bash
# start_task.sh - Move task from planned to active

start_task() {
    local task_pattern="$1"

    timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

    # Manual update required:
    echo "To start task '$task_pattern':"
    echo "1. Find task in Future Tasks or Active Tasks (if paused)"
    echo "2. Update status to 'In progress'"
    echo "3. Add started timestamp: **Started**: $timestamp"
    echo "4. Move to Active Tasks section if in Future"
    echo "5. Update task counts"
}

# Usage
start_task "Implement user authentication"
```

### Procedure 3: Complete Task (Active to Completed)

```bash
#!/bin/bash
# complete_task.sh - Move task to completed

complete_task() {
    local task_pattern="$1"
    local outcome="$2"
    local learnings="$3"

    completed_time=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

    echo "To complete task '$task_pattern':"
    echo "1. Change checkbox: - [ ] to - [x]"
    echo "2. Add completed timestamp: **Completed**: $completed_time"
    echo "3. Calculate duration (completed - started)"
    echo "4. Add outcome: **Outcome**: $outcome"
    echo "5. Add learnings: **Learnings**: $learnings"
    echo "6. Move task to Completed Tasks section"
    echo "7. Update task counts"
    echo "8. Check if any blocked tasks can now proceed"
}

# Usage
complete_task "Implement user authentication" "Successfully implemented" "JWT works well, session cookies had issues"
```

### Procedure 4: Block Task (Active to Blocked)

```bash
#!/bin/bash
# block_task.sh - Move task to blocked

block_task() {
    local task_pattern="$1"
    local blocker="$2"

    blocked_time=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

    echo "To block task '$task_pattern':"
    echo "1. Find task in Active Tasks"
    echo "2. Add blocker: **Blocked By**: $blocker"
    echo "3. Add timestamp: **Blocking Since**: $blocked_time"
    echo "4. Add impact: **Impact**: [What this blocks]"
    echo "5. Move to Blocked Tasks section"
    echo "6. Update task counts"
    echo "7. Add question to Open Questions if needed"
}

# Usage
block_task "Implement token refresh" "Need decision on token expiry duration"
```

### Procedure 5: Unblock Task (Blocked to Active)

```bash
#!/bin/bash
# unblock_task.sh - Resume blocked task

unblock_task() {
    local task_pattern="$1"
    local resolution="$2"

    unblocked_time=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

    echo "To unblock task '$task_pattern':"
    echo "1. Find task in Blocked Tasks"
    echo "2. Add resolution: **Resolved**: $resolution"
    echo "3. Add timestamp: **Unblocked**: $unblocked_time"
    echo "4. Remove blocker info or move to notes"
    echo "5. Update status to 'In progress'"
    echo "6. Move to Active Tasks section"
    echo "7. Update task counts"
}

# Usage
unblock_task "Implement token refresh" "Decided on 1-hour expiry"
```

### Procedure 6: Update Task Progress

```bash
#!/bin/bash
# update_progress.sh - Update task progress percentage

update_progress() {
    local task_pattern="$1"
    local progress="$2"

    timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

    echo "To update progress for '$task_pattern':"
    echo "1. Find task in Active Tasks"
    echo "2. Update progress: **Progress**: $progress%"
    echo "3. Update timestamp"
    echo "4. Optionally add progress note"
}

# Usage
update_progress "Implement user authentication" "75"
```

---

## Related Documents

For dependency management, snapshots, examples, and troubleshooting, see:
- [08b-progress-tracking-advanced.md](08b-progress-tracking-advanced.md)
  - Dependency Management
  - Progress Snapshots
  - Complete Lifecycle Examples
  - Troubleshooting Guide
