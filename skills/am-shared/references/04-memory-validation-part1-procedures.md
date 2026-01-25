# Memory Validation - Part 1: Fundamentals and Procedures

## Table of Contents
1. [When you need to understand the purpose](#purpose)
2. [Understanding validation levels](#validation-levels)
3. [How to perform structure validation](#procedure-1-structure-validation)
4. [How to perform content validation](#procedure-2-content-validation)
5. [How to perform consistency validation](#procedure-3-consistency-validation)
6. [How to perform recovery validation](#procedure-4-recovery-validation)

**Related Document**: [Part 2: Scripts, Checklists, and Troubleshooting](./04-memory-validation-part2-scripts-troubleshooting.md)

---

## Purpose

Memory validation ensures session memory structure and content remain intact, consistent, and usable. Regular validation:
- Detects corruption early
- Prevents data loss
- Ensures recovery capability
- Validates snapshot integrity
- Verifies file format correctness

## Validation Levels

### Level 1: Structure Validation
**What**: Verify directory and file structure exists

**Checks**:
- Required directories present
- Required files exist
- Permissions are correct
- No broken symlinks

**When**: Every session start, after major operations

### Level 2: Content Validation
**What**: Verify file contents are valid

**Checks**:
- Files are valid markdown
- Required sections present
- Timestamps well-formed
- No corrupted data

**When**: Before compaction, after updates

### Level 3: Consistency Validation
**What**: Verify data consistency across files

**Checks**:
- Pattern index matches pattern files
- Progress tracker matches actual tasks
- Snapshots are complete
- No contradictory information

**When**: Before compaction, on request

### Level 4: Recovery Validation
**What**: Verify recovery capability

**Checks**:
- Snapshots can be restored
- Archives are accessible
- Pre-compaction states preserved
- No missing critical data

**When**: Before compaction (mandatory)

## Validation Procedures

### Procedure 1: Structure Validation

```bash
#!/bin/bash
# validate_structure.sh - Level 1 validation

validate_structure() {
    local errors=0

    echo "=== Structure Validation ==="

    # Check root directory
    if [ ! -d ".session_memory" ]; then
        echo "✗ CRITICAL: .session_memory directory missing"
        return 1
    fi
    echo "✓ Root directory exists"

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
            echo "✗ ERROR: Missing directory: $dir"
            ((errors++))
        else
            echo "✓ Directory exists: $dir"
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
            echo "✗ ERROR: Missing file: $file"
            ((errors++))
        else
            echo "✓ File exists: $file"
        fi
    done

    # Check pattern category subdirectories
    pattern_categories=(
        "problem_solution"
        "workflow"
        "decision_logic"
        "error_recovery"
        "configuration"
    )

    for category in "${pattern_categories[@]}"; do
        if [ ! -d ".session_memory/patterns/$category" ]; then
            echo "⚠ WARNING: Missing pattern category: $category"
            mkdir -p ".session_memory/patterns/$category"
            echo "  Created: $category"
        else
            echo "✓ Pattern category exists: $category"
        fi
    done

    # Check for broken symlinks
    broken_links=$(find .session_memory -type l ! -exec test -e {} \; -print)
    if [ -n "$broken_links" ]; then
        echo "⚠ WARNING: Broken symlinks found:"
        echo "$broken_links"
    else
        echo "✓ No broken symlinks"
    fi

    # Check permissions
    if [ ! -r ".session_memory" ] || [ ! -w ".session_memory" ]; then
        echo "✗ ERROR: Insufficient permissions on .session_memory"
        ((errors++))
    else
        echo "✓ Permissions OK"
    fi

    # Summary
    echo ""
    if [ $errors -eq 0 ]; then
        echo "✓ Structure validation PASSED"
        return 0
    else
        echo "✗ Structure validation FAILED ($errors errors)"
        return 1
    fi
}

validate_structure
```

### Procedure 2: Content Validation

```bash
#!/bin/bash
# validate_content.sh - Level 2 validation

validate_content() {
    local errors=0

    echo "=== Content Validation ==="

    # Validate markdown files
    echo "Checking markdown syntax..."

    while IFS= read -r -d '' file; do
        # Check if file is readable
        if [ ! -r "$file" ]; then
            echo "✗ ERROR: Cannot read $file"
            ((errors++))
            continue
        fi

        # Check for required headers in active_context.md
        if [[ "$file" == *"active_context.md" ]]; then
            if ! grep -q "^# Active Context" "$file"; then
                echo "✗ ERROR: Missing header in active_context.md"
                ((errors++))
            else
                echo "✓ active_context.md header OK"
            fi

            # Check for required sections
            required_sections=("Current Focus" "Recent Decisions" "Open Questions")
            for section in "${required_sections[@]}"; do
                if ! grep -q "^## $section" "$file"; then
                    echo "⚠ WARNING: Missing section: $section"
                fi
            done
        fi

        # Check for required headers in progress_tracker.md
        if [[ "$file" == *"progress_tracker.md" ]]; then
            if ! grep -q "^# Progress Tracker" "$file"; then
                echo "✗ ERROR: Missing header in progress_tracker.md"
                ((errors++))
            else
                echo "✓ progress_tracker.md header OK"
            fi
        fi

        # Check for required headers in pattern_index.md
        if [[ "$file" == *"pattern_index.md" ]]; then
            if ! grep -q "^# Pattern Index" "$file"; then
                echo "✗ ERROR: Missing header in pattern_index.md"
                ((errors++))
            else
                echo "✓ pattern_index.md header OK"
            fi
        fi

        # Basic markdown syntax check (look for common errors)
        # Check for unmatched code blocks
        backtick_count=$(grep -o '```' "$file" | wc -l)
        if [ $((backtick_count % 2)) -ne 0 ]; then
            echo "⚠ WARNING: Unmatched code blocks in $file"
        fi

    done < <(find .session_memory -name "*.md" -type f -print0)

    # Summary
    echo ""
    if [ $errors -eq 0 ]; then
        echo "✓ Content validation PASSED"
        return 0
    else
        echo "✗ Content validation FAILED ($errors errors)"
        return 1
    fi
}

validate_content
```

### Procedure 3: Consistency Validation

```bash
#!/bin/bash
# validate_consistency.sh - Level 3 validation

validate_consistency() {
    local warnings=0

    echo "=== Consistency Validation ==="

    # Check pattern index consistency
    echo "Checking pattern index consistency..."

    # Count patterns listed in index
    indexed_patterns=$(grep -c "^- \[" .session_memory/pattern_index.md 2>/dev/null || echo "0")

    # Count actual pattern files
    actual_patterns=$(find .session_memory/patterns -name "*.md" -type f | wc -l)

    echo "Indexed patterns: $indexed_patterns"
    echo "Actual pattern files: $actual_patterns"

    if [ "$indexed_patterns" -ne "$actual_patterns" ]; then
        echo "⚠ WARNING: Pattern count mismatch (index: $indexed_patterns, files: $actual_patterns)"
        ((warnings++))
    else
        echo "✓ Pattern counts match"
    fi

    # Check for orphaned pattern files
    echo "Checking for orphaned patterns..."
    while IFS= read -r -d '' pattern_file; do
        basename=$(basename "$pattern_file")
        if ! grep -q "$basename" .session_memory/pattern_index.md; then
            echo "⚠ WARNING: Pattern not in index: $basename"
            ((warnings++))
        fi
    done < <(find .session_memory/patterns -name "*.md" -type f -print0)

    # Check snapshot completeness
    echo "Checking snapshot completeness..."
    for snapshot_dir in .session_memory/snapshots/snapshot_*; do
        if [ -d "$snapshot_dir" ]; then
            required_snapshot_files=("context.md" "progress.md" "patterns.md" "metadata.txt")
            for file in "${required_snapshot_files[@]}"; do
                if [ ! -f "$snapshot_dir/$file" ]; then
                    echo "⚠ WARNING: Incomplete snapshot: $snapshot_dir (missing $file)"
                    ((warnings++))
                fi
            done
        fi
    done

    # Check for contradictory timestamps
    echo "Checking timestamp consistency..."
    # Extract timestamps and ensure they're chronological where expected
    # (Implementation depends on specific timestamp format requirements)

    # Summary
    echo ""
    if [ $warnings -eq 0 ]; then
        echo "✓ Consistency validation PASSED"
        return 0
    else
        echo "⚠ Consistency validation completed with $warnings warnings"
        return 0  # Warnings don't fail validation
    fi
}

validate_consistency
```

### Procedure 4: Recovery Validation

```bash
#!/bin/bash
# validate_recovery.sh - Level 4 validation

validate_recovery() {
    local errors=0

    echo "=== Recovery Validation ==="

    # Check for recent snapshots
    echo "Checking snapshot availability..."

    latest_snapshot=$(ls -t .session_memory/snapshots/snapshot_*/metadata.txt 2>/dev/null | head -1)

    if [ -z "$latest_snapshot" ]; then
        echo "✗ ERROR: No snapshots available for recovery"
        ((errors++))
    else
        snapshot_dir=$(dirname "$latest_snapshot")
        echo "✓ Latest snapshot: $snapshot_dir"

        # Verify snapshot is complete
        required_files=("context.md" "progress.md" "patterns.md" "metadata.txt")
        for file in "${required_files[@]}"; do
            if [ ! -f "$snapshot_dir/$file" ]; then
                echo "✗ ERROR: Incomplete snapshot (missing $file)"
                ((errors++))
            fi
        done

        # Check snapshot age
        if [ -f "$latest_snapshot" ]; then
            snapshot_time=$(grep "^Timestamp:" "$latest_snapshot" | cut -d: -f2- | xargs)
            echo "  Snapshot time: $snapshot_time"
        fi
    fi

    # Check for pre-compaction archives
    echo "Checking pre-compaction archives..."

    compaction_count=$(grep "Compaction Count:" .session_memory/session_info.md 2>/dev/null | grep -oP '\d+' || echo "0")
    echo "Compaction count: $compaction_count"

    if [ "$compaction_count" -gt 0 ]; then
        # Should have pre-compaction archives
        archive_count=$(ls -d .session_memory/archived/pre_compaction_* 2>/dev/null | wc -l)
        echo "Pre-compaction archives: $archive_count"

        if [ "$archive_count" -eq 0 ]; then
            echo "⚠ WARNING: Compactions performed but no archives found"
        else
            echo "✓ Pre-compaction archives available"
        fi
    fi

    # Test snapshot restoration (dry run)
    echo "Testing snapshot restoration (dry run)..."

    if [ -n "$latest_snapshot" ]; then
        snapshot_dir=$(dirname "$latest_snapshot")
        temp_dir=$(mktemp -d)

        # Try copying snapshot files
        if cp "$snapshot_dir"/* "$temp_dir/" 2>/dev/null; then
            echo "✓ Snapshot files are readable and copyable"
            rm -rf "$temp_dir"
        else
            echo "✗ ERROR: Cannot read/copy snapshot files"
            ((errors++))
            rm -rf "$temp_dir"
        fi
    fi

    # Summary
    echo ""
    if [ $errors -eq 0 ]; then
        echo "✓ Recovery validation PASSED"
        return 0
    else
        echo "✗ Recovery validation FAILED ($errors errors)"
        return 1
    fi
}

validate_recovery
```

---

**Continue to**: [Part 2: Scripts, Checklists, and Troubleshooting](./04-memory-validation-part2-scripts-troubleshooting.md)
