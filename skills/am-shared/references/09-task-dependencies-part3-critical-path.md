# Task Dependencies - Part 3: Critical Path Analysis and Validation

## Table of Contents
1. [Critical Path Analysis](#critical-path-analysis)
   - 1.1 [Definition](#definition)
   - 1.2 [Calculation Procedure](#calculation-procedure)
   - 1.3 [Critical Path Script](#critical-path-script)
2. [Dependency Validation](#dependency-validation)
   - 2.1 [Validation Checklist](#validation-checklist)
   - 2.2 [Validation Script](#validation-script)

---

## Critical Path Analysis

### Definition

**Critical Path**: The longest sequence of dependent tasks from start to finish. Determines minimum project completion time.

### Calculation Procedure

```markdown
## Critical Path Calculation

### Step 1: List All Tasks with Duration
- Task A: 2 hours
- Task B: 3 hours (depends on A)
- Task C: 1 hour (depends on A)
- Task D: 2 hours (depends on B, C)

### Step 2: Calculate Paths
Path 1: A → B → D = 2 + 3 + 2 = 7 hours
Path 2: A → C → D = 2 + 1 + 2 = 5 hours

### Step 3: Identify Critical Path
**Critical Path**: A → B → D (7 hours)

**Implications**:
- Minimum completion: 7 hours
- Task B is critical (any delay extends project)
- Task C has 2 hours slack (can delay without affecting project)
```

### Critical Path Script

```bash
#!/bin/bash
# calculate_critical_path.sh - Find critical path through tasks

calculate_critical_path() {
    echo "=== Critical Path Analysis ==="
    echo ""

    echo "Dependency-based calculation (per RULE 13):"
    echo "1. List all tasks with dependencies"
    echo "2. Identify dependency chains"
    echo "3. Find longest blocking chain"
    echo "4. Chain with most dependencies is critical path"
    echo ""

    echo "Tasks on critical path block others"
    echo "Tasks not on critical path can be parallelized"
}

calculate_critical_path
```

---

## Dependency Validation

### Validation Checklist

```markdown
## Dependency Validation Checklist

- [ ] All dependencies are recorded
- [ ] No circular dependencies
- [ ] No missing dependencies
- [ ] Dependency types are specified
- [ ] Dependency graph is up to date
- [ ] Critical path identified
- [ ] Blocked tasks properly marked
```

### Validation Script

```bash
#!/bin/bash
# validate_dependencies.sh - Validate dependency configuration

validate_dependencies() {
    local errors=0

    echo "=== Dependency Validation ==="
    echo ""

    # Check 1: All active tasks have dependency info
    echo "Check 1: All tasks have dependency information..."
    while IFS= read -r task; do
        if ! grep -A 5 "$task" .session_memory/progress_tracker.md | grep -q "Dependencies:"; then
            echo "  ✗ Missing dependency info: $task"
            ((errors++))
        fi
    done < <(grep "^- \[ \]" .session_memory/progress_tracker.md | sed 's/- \[ \] //')

    # Check 2: Circular dependencies
    echo ""
    echo "Check 2: Circular dependencies..."
    detect_circular_dependencies

    # Check 3: Referenced dependencies exist
    echo ""
    echo "Check 3: All referenced dependencies exist..."
    all_deps=$(grep "Dependencies:" .session_memory/progress_tracker.md | \
               cut -d: -f2- | tr ',' '\n' | sed 's/^ *//' | grep -v "^None$" | sort -u)

    while IFS= read -r dep; do
        # Remove milestone notation if present
        dep_task=$(echo "$dep" | sed 's/ (.*//')

        if ! grep -q "^- \[.\] $dep_task" .session_memory/progress_tracker.md; then
            echo "  ✗ Referenced dependency not found: $dep_task"
            ((errors++))
        fi
    done <<< "$all_deps"

    # Summary
    echo ""
    if [ $errors -eq 0 ]; then
        echo "✓ Dependency validation PASSED"
        return 0
    else
        echo "✗ Dependency validation FAILED ($errors errors)"
        return 1
    fi
}

validate_dependencies
```

---

**Navigation**:
- [Back to main: Task Dependencies](./09-task-dependencies.md)
- [Previous: Part 2 - Dependency Management](./09-task-dependencies-part2-management.md)
- [Next: Part 4 - Examples and Troubleshooting](./09-task-dependencies-part4-examples.md)
