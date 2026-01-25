# Progress Tracking: Task Management Procedures

## Table of Contents
1. [Procedure 1: Add New Task](#procedure-1-add-new-task)
2. [Procedure 2: Start Task (Planned → Active)](#procedure-2-start-task-planned--active)
3. [Procedure 3: Complete Task (Active → Completed)](#procedure-3-complete-task-active--completed)
4. [Procedure 4: Block Task (Active → Blocked)](#procedure-4-block-task-active--blocked)
5. [Procedure 5: Unblock Task (Blocked → Active)](#procedure-5-unblock-task-blocked--active)
6. [Procedure 6: Update Task Progress](#procedure-6-update-task-progress)

---

## Procedure 1: Add New Task

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

    echo "✓ Task added: $task_name"
}

# Usage
add_task "Implement user authentication" "High" "None"
```

---

## Procedure 2: Start Task (Planned → Active)

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

---

## Procedure 3: Complete Task (Active → Completed)

```bash
#!/bin/bash
# complete_task.sh - Move task to completed

complete_task() {
    local task_pattern="$1"
    local outcome="$2"
    local learnings="$3"

    completed_time=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

    echo "To complete task '$task_pattern':"
    echo "1. Change checkbox: - [ ] → - [x]"
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

---

## Procedure 4: Block Task (Active → Blocked)

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

---

## Procedure 5: Unblock Task (Blocked → Active)

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

---

## Procedure 6: Update Task Progress

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

**Previous**: See [Part 1: Structure and States](./08-manage-progress-tracking-part1-structure-states.md) for tracker structure.

**Next**: See [Part 3: Dependencies and Snapshots](./08-manage-progress-tracking-part3-dependencies-snapshots.md) for dependency management.
