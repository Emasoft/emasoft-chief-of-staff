# Progress Tracking: Advanced Features

## Table of Contents
1. [Managing dependencies](#dependency-management)
2. [Creating progress snapshots](#progress-snapshots)
3. [For implementation examples](#examples)
4. [If issues occur](#troubleshooting)

---

## Dependency Management

### Recording Dependencies

```markdown
## Task Dependencies

### Linear Dependencies
```
Task A → Task B → Task C
```

**Explanation**:
- Task B depends on Task A (cannot start B until A completes)
- Task C depends on Task B (cannot start C until B completes)

### Parallel with Merge
```
Task A → Task C
Task B → Task C
```

**Explanation**:
- Tasks A and B can proceed in parallel
- Task C requires both A and B to complete

### Complex Dependencies
```
Task A
  ├─> Task B
  │     └─> Task D
  └─> Task C
        └─> Task D
```

**Explanation**:
- Task B depends on A
- Task C depends on A
- Task D depends on both B and C
- B and C can proceed in parallel after A completes
```

### Dependency Tracking Script

```bash
#!/bin/bash
# check_dependencies.sh - Check if task dependencies are met

check_dependencies() {
    local task_name="$1"

    echo "Checking dependencies for: $task_name"

    # Extract dependencies from task
    dependencies=$(grep -A 5 "$task_name" .session_memory/progress_tracker.md | grep "Dependencies:" | cut -d: -f2- | xargs)

    if [ "$dependencies" = "None" ]; then
        echo "No dependencies - can start immediately"
        return 0
    fi

    echo "Dependencies: $dependencies"

    # Check each dependency
    IFS=',' read -ra DEPS <<< "$dependencies"
    all_met=true

    for dep in "${DEPS[@]}"; do
        dep=$(echo "$dep" | xargs)  # Trim whitespace

        # Check if dependency is in Completed Tasks
        if grep -q "- \[x\] $dep" .session_memory/progress_tracker.md; then
            echo "  [OK] $dep - Completed"
        else
            echo "  [FAIL] $dep - Not completed"
            all_met=false
        fi
    done

    if $all_met; then
        echo "All dependencies met - can proceed"
        return 0
    else
        echo "Dependencies not met - task should be blocked or waiting"
        return 1
    fi
}

# Usage
check_dependencies "Implement token refresh"
```

## Progress Snapshots

### When to Create Snapshots

Create progress snapshots:
- Before compaction (mandatory)
- After completing major milestone
- At end of work session
- Before making significant changes
- On user request

### Snapshot Procedure

```bash
#!/bin/bash
# create_progress_snapshot.sh - Create timestamped progress snapshot

create_progress_snapshot() {
    local timestamp=$(date -u +"%Y%m%d_%H%M%S")
    local snapshot_file=".session_memory/progress/progress_$timestamp.md"
    local source_file=".session_memory/progress_tracker.md"

    # Copy current progress
    cp "$source_file" "$snapshot_file"

    # Update symlink to latest
    ln -sf "progress_$timestamp.md" .session_memory/progress/progress_latest.md

    echo "Progress snapshot created: $snapshot_file"

    # Keep only last 10 snapshots
    cd .session_memory/progress
    ls -t progress_*.md | tail -n +11 | xargs rm -f 2>/dev/null || true

    echo "Old snapshots cleaned up"
}

create_progress_snapshot
```

### Restore from Snapshot

```bash
#!/bin/bash
# restore_progress.sh - Restore progress from snapshot

restore_progress() {
    local snapshot_pattern="$1"

    if [ -z "$snapshot_pattern" ]; then
        # Use latest
        snapshot_file=".session_memory/progress/progress_latest.md"
    else
        # Find matching snapshot
        snapshot_file=$(find .session_memory/progress -name "*$snapshot_pattern*.md" | head -1)
    fi

    if [ -z "$snapshot_file" ] || [ ! -f "$snapshot_file" ]; then
        echo "Snapshot not found: $snapshot_pattern"
        return 1
    fi

    # Backup current progress
    backup_file=".session_memory/progress_tracker.md.bak.$(date +%Y%m%d_%H%M%S)"
    cp .session_memory/progress_tracker.md "$backup_file"

    # Restore from snapshot
    cp "$snapshot_file" .session_memory/progress_tracker.md

    echo "Progress restored from: $snapshot_file"
    echo "Backup saved to: $backup_file"
}

# Usage
restore_progress "20260101"
```

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

## Troubleshooting

### Problem: Task Counts Out of Sync

**Solution**:
```bash
# Recount tasks
active=$(grep -c "^- \[ \]" .session_memory/progress_tracker.md)
completed=$(grep -c "^- \[x\]" .session_memory/progress_tracker.md)

# Update header
sed -i '' "s/\*\*Active Tasks\*\*: [0-9]\+/**Active Tasks**: $active/" .session_memory/progress_tracker.md
sed -i '' "s/\*\*Completed Tasks\*\*: [0-9]\+/**Completed Tasks**: $completed/" .session_memory/progress_tracker.md
```

### Problem: Circular Dependencies

**Solution**:
```markdown
# Detected: Task A depends on B, Task B depends on A

# Resolution:
1. Identify the circular dependency
2. Break the circle by:
   - Splitting one task into two parts
   - Removing unnecessary dependency
   - Reordering task implementation
3. Update dependency graph
```

### Problem: Progress Tracker Lost

**Solution**:
```bash
# Restore from latest snapshot
cp .session_memory/progress/progress_latest.md .session_memory/progress_tracker.md

# Or from archived state
latest_archive=$(ls -t .session_memory/archived/pre_compaction_*/progress_tracker.md | head -1)
cp "$latest_archive" .session_memory/progress_tracker.md
```

### Problem: Too Many Tasks in Active

**Solution**:
```bash
# Review active tasks
grep "^- \[ \]" .session_memory/progress_tracker.md

# Move paused tasks to Future Tasks
# Keep only actively worked-on tasks in Active
# Recommended: Max 3-5 active tasks at once
```

---

## Related Documents

For tracker structure, states, and basic procedures, see:
- [08a-progress-tracking-structure.md](08a-progress-tracking-structure.md)
  - Purpose and Overview
  - Progress Tracker Structure
  - Task States and Transitions
  - Task Management Procedures
