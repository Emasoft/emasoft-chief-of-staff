# Memory Directory Structure - Part 2: Naming and Validation

## Table of Contents
- 2.1 [Timestamp Format](#21-timestamp-format)
- 2.2 [Pattern Files](#22-pattern-files)
- 2.3 [Snapshot Directories](#23-snapshot-directories)
- 2.4 [Validation Script](#24-validation-script)
- 2.5 [Repair Damaged Structure](#25-repair-damaged-structure)

---

## 2.1 Timestamp Format

Use ISO-8601 compatible format for consistency:
- Format: `YYYYMMDD_HHMMSS`
- Example: `20260101_143022` (January 1, 2026, 14:30:22)
- Always use UTC timezone

```bash
# Generate timestamp
timestamp=$(date -u +"%Y%m%d_%H%M%S")
```

---

## 2.2 Pattern Files

Format: `{prefix}_{number}_{description}.md`

**Prefix Codes**:
- `ps`: Problem-Solution
- `wf`: Workflow
- `dl`: Decision-Logic
- `er`: Error-Recovery
- `cfg`: Configuration

**Number**: Zero-padded 3-digit sequential number (001, 002, ...)

**Description**: Brief kebab-case description (lowercase, hyphens)

**Examples**:
```
ps_001_git-auth-failure.md
wf_002_parallel-agent-spawning.md
dl_003_approve-feature-requests.md
er_004_context-overflow-recovery.md
cfg_005_eslint-configuration.md
```

---

## 2.3 Snapshot Directories

Format: `snapshot_{timestamp}` or `pre_compaction_{count}`

**Examples**:
```
snapshot_20260101_143022/
snapshot_20260101_150000/
pre_compaction_1/
pre_compaction_2/
```

---

## 2.4 Validation Script

```bash
#!/bin/bash
# validate_structure.sh - Validate memory directory structure

validate_memory_structure() {
    local errors=0

    # Check root directory exists
    if [ ! -d ".session_memory" ]; then
        echo "ERROR: .session_memory directory not found"
        return 1
    fi

    # Check required subdirectories
    required_dirs=(
        "active_context"
        "patterns"
        "progress"
        "snapshots"
        "archived"
    )

    for dir in "${required_dirs[@]}"; do
        if [ ! -d ".session_memory/$dir" ]; then
            echo "ERROR: Missing directory: $dir"
            ((errors++))
        fi
    done

    # Check required root files
    required_files=(
        "session_info.md"
        "active_context.md"
        "progress_tracker.md"
        "pattern_index.md"
    )

    for file in "${required_files[@]}"; do
        if [ ! -f ".session_memory/$file" ]; then
            echo "ERROR: Missing file: $file"
            ((errors++))
        fi
    done

    # Check pattern subdirectories
    pattern_categories=(
        "problem_solution"
        "workflow"
        "decision_logic"
        "error_recovery"
        "configuration"
    )

    for category in "${pattern_categories[@]}"; do
        if [ ! -d ".session_memory/patterns/$category" ]; then
            echo "WARNING: Missing pattern category: $category"
            # Create it
            mkdir -p ".session_memory/patterns/$category"
        fi
    done

    if [ $errors -eq 0 ]; then
        echo "✓ Memory structure is valid"
        return 0
    else
        echo "✗ Found $errors errors in memory structure"
        return 1
    fi
}

validate_memory_structure
```

---

## 2.5 Repair Damaged Structure

```bash
#!/bin/bash
# repair_structure.sh - Repair damaged memory structure

repair_memory_structure() {
    echo "Repairing memory structure..."

    # Create missing directories
    mkdir -p .session_memory/{active_context,patterns,progress,snapshots,archived}
    mkdir -p .session_memory/patterns/{problem_solution,workflow,decision_logic,error_recovery,configuration}

    # Create missing root files with minimal content
    if [ ! -f ".session_memory/session_info.md" ]; then
        cat > .session_memory/session_info.md << EOF
# Session Information
**Repaired:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Status:** Structure repaired
EOF
    fi

    if [ ! -f ".session_memory/active_context.md" ]; then
        cat > .session_memory/active_context.md << EOF
# Active Context
**Repaired:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")

## Current Focus
[Context lost - needs reconstruction]
EOF
    fi

    if [ ! -f ".session_memory/progress_tracker.md" ]; then
        cat > .session_memory/progress_tracker.md << EOF
# Progress Tracker
**Repaired:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")

## Active Tasks
[Tasks lost - needs reconstruction]
EOF
    fi

    if [ ! -f ".session_memory/pattern_index.md" ]; then
        cat > .session_memory/pattern_index.md << EOF
# Pattern Index
**Repaired:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")

## Recorded Patterns
[Pattern index lost - needs reconstruction]
EOF
    fi

    echo "✓ Structure repaired - validate manually"
}

repair_memory_structure
```
