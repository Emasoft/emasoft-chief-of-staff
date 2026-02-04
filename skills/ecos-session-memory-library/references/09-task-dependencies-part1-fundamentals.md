# Task Dependencies - Part 1: Fundamentals

## Table of Contents
1. [When you need to understand the purpose](#purpose)
2. [Understanding dependency types](#dependency-types)
3. [Using dependency notation](#dependency-notation)
4. [Managing dependencies](#dependency-management)

**See also**: [Part 2: Analysis & Practice](09-task-dependencies-part2-analysis.md) for critical path analysis, validation, examples, and troubleshooting.

## Purpose

Task dependency management tracks relationships between tasks to:
- Prevent starting tasks before prerequisites complete
- Identify parallelization opportunities
- Calculate critical path
- Estimate completion time
- Avoid circular dependencies

## Dependency Types

### Type 1: Sequential Dependency

**Definition**: Task B cannot start until Task A completes.

**Notation**: `A → B`

**Example**:
```
OAuth setup → Implement callback handler
```

**Use Case**: Task B needs artifacts or knowledge from Task A

### Type 2: Parallel with Merge

**Definition**: Tasks A and B can run in parallel, both required for Task C.

**Notation**:
```
A ─┐
   ├─> C
B ─┘
```

**Example**:
```
Unit tests ─┐
            ├─> Deploy
Integration tests ─┘
```

**Use Case**: Independent tasks with common successor

### Type 3: Split Dependency

**Definition**: Task A produces multiple independent follow-up tasks.

**Notation**:
```
    ├─> B
A ─┼─> C
    └─> D
```

**Example**:
```
        ├─> Frontend implementation
API design ─┼─> Backend implementation
        └─> Documentation update
```

**Use Case**: One task enables multiple parallel workstreams

### Type 4: Partial Dependency

**Definition**: Task B can start after Task A reaches certain milestone.

**Notation**: `A (milestone) → B`

**Example**:
```
API implementation (basic endpoints done) → Frontend development
```

**Use Case**: Don't wait for full completion, start based on partial progress

### Type 5: Optional Dependency

**Definition**: Task B is enhanced by Task A, but can proceed without it.

**Notation**: `A ~~> B` (dashed arrow)

**Example**:
```
Performance optimization ~~> Deploy
```

**Use Case**: Nice-to-have prerequisite, not blocking

## Dependency Notation

### Text-Based Notation

```markdown
## Task Dependencies

### Linear Chain
```
Task A → Task B → Task C
```

### Parallel Paths
```
Task A → Task C
Task B → Task C
```

### Complex Graph
```
Task A
  ├─> Task B
  │     └─> Task D
  └─> Task C
        └─> Task D
```

### Dependency Table
| Task | Depends On | Type | Status |
|------|------------|------|--------|
| Task A | None | - | Complete |
| Task B | Task A | Sequential | Active |
| Task C | Task A | Sequential | Waiting |
| Task D | Task B, Task C | Merge | Waiting |
```

### In-Task Dependency Recording

```markdown
- [ ] Task name
  - **Dependencies**: Task A, Task B
  - **Dependency Type**: Merge (requires both)
  - **Can Start When**: Both Task A and Task B complete
```

## Dependency Management

### Procedure 1: Record Dependency

```bash
#!/bin/bash
# record_dependency.sh - Record task dependency

record_dependency() {
    local task_name="$1"
    local depends_on="$2"
    local dep_type="$3"

    echo "Recording dependency:"
    echo "  Task: $task_name"
    echo "  Depends on: $depends_on"
    echo "  Type: $dep_type"

    # Add to task definition
    echo "1. Find task in progress_tracker.md"
    echo "2. Add dependency line: **Dependencies**: $depends_on"
    echo "3. Add dependency type: **Dependency Type**: $dep_type"
    echo "4. Update dependency graph"
}

# Usage
record_dependency "Implement callback" "OAuth setup" "Sequential"
```

### Procedure 2: Check Dependencies Met

```bash
#!/bin/bash
# check_dependencies_met.sh - Verify all dependencies are satisfied

check_dependencies_met() {
    local task_name="$1"

    echo "Checking dependencies for: $task_name"

    # Extract dependencies
    dependencies=$(grep -A 10 "$task_name" .session_memory/progress_tracker.md | \
                   grep "Dependencies:" | cut -d: -f2- | xargs)

    if [ "$dependencies" = "None" ]; then
        echo "✓ No dependencies"
        return 0
    fi

    echo "Dependencies: $dependencies"

    # Split on comma
    IFS=',' read -ra DEPS <<< "$dependencies"
    all_met=true

    for dep in "${DEPS[@]}"; do
        dep=$(echo "$dep" | xargs)

        # Check if completed
        if grep -q "- \[x\] $dep" .session_memory/progress_tracker.md; then
            echo "  ✓ $dep (completed)"
        else
            # Check if it's a partial dependency
            if [[ "$dep" =~ \(.*\) ]]; then
                # Extract task and milestone
                task=$(echo "$dep" | sed 's/ (.*//')
                milestone=$(echo "$dep" | grep -oP '\((.*?)\)' | tr -d '()')

                echo "  ? $task - Check milestone: $milestone"
                # Manual verification required
            else
                echo "  ✗ $dep (not completed)"
                all_met=false
            fi
        fi
    done

    if $all_met; then
        echo "✓ All dependencies met"
        return 0
    else
        echo "✗ Dependencies not met - task should wait"
        return 1
    fi
}

# Usage
check_dependencies_met "Implement callback handler"
```

### Procedure 3: Update Dependencies After Task Completion

```bash
#!/bin/bash
# update_dependencies_after_completion.sh - Unblock waiting tasks

update_dependencies_after_completion() {
    local completed_task="$1"

    echo "Task completed: $completed_task"
    echo "Checking for tasks waiting on this dependency..."

    # Find tasks that depend on this one
    waiting_tasks=$(grep -B 2 "Dependencies:.*$completed_task" .session_memory/progress_tracker.md | \
                    grep "^- \[ \]" | sed 's/- \[ \] //')

    if [ -z "$waiting_tasks" ]; then
        echo "No tasks waiting on this dependency"
        return 0
    fi

    echo "Tasks that depended on this:"
    echo "$waiting_tasks"

    echo ""
    echo "For each task, check if all dependencies are now met:"
    while IFS= read -r task; do
        echo "  - Checking: $task"
        check_dependencies_met "$task"
    done <<< "$waiting_tasks"
}

# Usage
update_dependencies_after_completion "OAuth setup"
```

### Procedure 4: Detect Circular Dependencies

```bash
#!/bin/bash
# detect_circular_dependencies.sh - Find circular dependency chains

detect_circular_dependencies() {
    echo "Detecting circular dependencies..."

    # Extract all task-dependency pairs
    declare -A deps

    while IFS= read -r line; do
        if [[ "$line" =~ ^-\ \[.?\]\ (.+)$ ]]; then
            current_task="${BASH_REMATCH[1]}"
        fi

        if [[ "$line" =~ Dependencies:\ (.+)$ ]]; then
            dep_list="${BASH_REMATCH[1]}"
            if [ "$dep_list" != "None" ]; then
                deps["$current_task"]="$dep_list"
            fi
        fi
    done < .session_memory/progress_tracker.md

    # Simple cycle detection (checks direct cycles)
    for task in "${!deps[@]}"; do
        dep_list="${deps[$task]}"
        IFS=',' read -ra DEPS <<< "$dep_list"

        for dep in "${DEPS[@]}"; do
            dep=$(echo "$dep" | xargs)

            # Check if dep depends back on task
            if [[ "${deps[$dep]}" == *"$task"* ]]; then
                echo "⚠ Circular dependency detected: $task ↔ $dep"
            fi
        done
    done

    echo "✓ Circular dependency check complete"
}

detect_circular_dependencies
```
