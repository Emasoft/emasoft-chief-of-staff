# Progress Tracking: Dependencies and Snapshots

## Table of Contents
1. [Dependency Management](#dependency-management)
   - 1.1 [Recording Dependencies](#recording-dependencies)
   - 1.2 [Dependency Tracking Script](#dependency-tracking-script)
2. [Progress Snapshots](#progress-snapshots)
   - 2.1 [When to Create Snapshots](#when-to-create-snapshots)
   - 2.2 [Snapshot Procedure](#snapshot-procedure)
   - 2.3 [Restore from Snapshot](#restore-from-snapshot)

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
        echo "✓ No dependencies - can start immediately"
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
            echo "  ✓ $dep - Completed"
        else
            echo "  ✗ $dep - Not completed"
            all_met=false
        fi
    done

    if $all_met; then
        echo "✓ All dependencies met - can proceed"
        return 0
    else
        echo "✗ Dependencies not met - task should be blocked or waiting"
        return 1
    fi
}

# Usage
check_dependencies "Implement token refresh"
```

---

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

    echo "✓ Progress snapshot created: $snapshot_file"

    # Keep only last 10 snapshots
    cd .session_memory/progress
    ls -t progress_*.md | tail -n +11 | xargs rm -f 2>/dev/null || true

    echo "✓ Old snapshots cleaned up"
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
        echo "✗ Snapshot not found: $snapshot_pattern"
        return 1
    fi

    # Backup current progress
    backup_file=".session_memory/progress_tracker.md.bak.$(date +%Y%m%d_%H%M%S)"
    cp .session_memory/progress_tracker.md "$backup_file"

    # Restore from snapshot
    cp "$snapshot_file" .session_memory/progress_tracker.md

    echo "✓ Progress restored from: $snapshot_file"
    echo "✓ Backup saved to: $backup_file"
}

# Usage
restore_progress "20260101"
```

---

**Previous**: See [Part 2: Task Management Procedures](./08-manage-progress-tracking-part2-task-management.md) for task operations.

**Next**: See [Part 4: Examples and Troubleshooting](./08-manage-progress-tracking-part4-examples-troubleshooting.md) for practical examples.
