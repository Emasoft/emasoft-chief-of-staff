# Pre-Compaction Checklist - Part 2: Validation and Decision

## Table of Contents
1. [Completing validation phase](#validation-phase)
   - 1.1 [Running all validation checks](#complete-validation-script)
2. [Performing final verification](#final-verification)
   - 2.1 [Testing restoration capability](#restoration-test)
3. [Making go/no-go decision](#gono-go-decision)
   - 3.1 [Decision criteria matrix](#decision-criteria)
4. [Implementation examples](#examples)
   - 4.1 [Complete checklist execution](#example-1-complete-checklist-execution)
   - 4.2 [Checklist with manual stop points](#example-2-checklist-with-stop-points)

**See also**: [Part 1: Preparation and Backup](12-pre-compaction-checklist-part1-preparation-backup.md) for purpose, master checklist, preparation phase, and backup phase.

---

## Validation Phase

### Complete Validation Script

```bash
#!/bin/bash
# run_all_validations.sh - Run all validation checks

run_all_validations() {
    local errors=0

    echo "=== Running All Validations ==="
    echo ""

    # 1. Structure validation
    echo "1. Structure Validation"
    echo "----------------------"
    if ./validate_structure.sh; then
        echo "✓ Structure validation passed"
    else
        echo "✗ Structure validation failed"
        ((errors++))
    fi

    # 2. Content validation
    echo ""
    echo "2. Content Validation"
    echo "--------------------"
    if ./validate_content.sh; then
        echo "✓ Content validation passed"
    else
        echo "✗ Content validation failed"
        ((errors++))
    fi

    # 3. Consistency validation
    echo ""
    echo "3. Consistency Validation"
    echo "------------------------"
    if ./validate_consistency.sh; then
        echo "✓ Consistency validation passed"
    else
        echo "⚠ Consistency validation warnings (non-fatal)"
    fi

    # 4. Recovery validation
    echo ""
    echo "4. Recovery Validation"
    echo "---------------------"
    if ./validate_recovery.sh; then
        echo "✓ Recovery validation passed"
    else
        echo "✗ Recovery validation failed"
        ((errors++))
    fi

    # Summary
    echo ""
    echo "=== Validation Summary ==="
    if [ $errors -eq 0 ]; then
        echo "✓ ALL VALIDATIONS PASSED"
        return 0
    else
        echo "✗ $errors VALIDATION(S) FAILED"
        return 1
    fi
}

run_all_validations
```

## Final Verification

### Restoration Test

```bash
#!/bin/bash
# test_restoration.sh - Test restoration capability

test_restoration() {
    echo "=== Testing Restoration Capability ==="
    echo ""

    # Get latest snapshot
    latest_snapshot=$(ls -t .session_memory/snapshots/snapshot_*/metadata.txt 2>/dev/null | head -1)
    if [ -z "$latest_snapshot" ]; then
        echo "✗ No snapshot available"
        return 1
    fi

    snapshot_dir=$(dirname "$latest_snapshot")
    echo "Testing with snapshot: $snapshot_dir"
    echo ""

    # Create test directory
    test_dir=$(mktemp -d)
    echo "Test directory: $test_dir"

    # Test: Copy files
    echo "Test 1: Copy snapshot files..."
    if cp "$snapshot_dir"/* "$test_dir/" 2>/dev/null; then
        echo "✓ Files copied successfully"
    else
        echo "✗ Failed to copy files"
        rm -rf "$test_dir"
        return 1
    fi

    # Test: Read files
    echo ""
    echo "Test 2: Read snapshot files..."
    if [ -r "$test_dir/context.md" ] && \
       [ -r "$test_dir/progress.md" ] && \
       [ -r "$test_dir/patterns.md" ]; then
        echo "✓ All files readable"
    else
        echo "✗ Some files not readable"
        rm -rf "$test_dir"
        return 1
    fi

    # Test: Validate content
    echo ""
    echo "Test 3: Validate file content..."
    if grep -q "# Active Context" "$test_dir/context.md" && \
       grep -q "# Progress Tracker" "$test_dir/progress.md" && \
       grep -q "# Pattern Index" "$test_dir/patterns.md"; then
        echo "✓ File content valid"
    else
        echo "✗ Invalid file content"
        rm -rf "$test_dir"
        return 1
    fi

    # Cleanup
    rm -rf "$test_dir"

    echo ""
    echo "✓ Restoration test PASSED"
    echo "  Can successfully restore from snapshot"

    return 0
}

test_restoration
```

## Go/No-Go Decision

### Decision Criteria

```markdown
# Compaction Go/No-Go Decision Matrix

## CRITICAL CRITERIA (All must be YES to proceed)

| Criterion | Status | Notes |
|-----------|--------|-------|
| Context snapshot created | ☐ YES ☐ NO | |
| Progress snapshot created | ☐ YES ☐ NO | |
| Full snapshot created | ☐ YES ☐ NO | |
| Pre-compaction archive created | ☐ YES ☐ NO | |
| Structure validation passed | ☐ YES ☐ NO | |
| Content validation passed | ☐ YES ☐ NO | |
| Recovery validation passed | ☐ YES ☐ NO | |
| Restoration test passed | ☐ YES ☐ NO | |

## WARNING CONDITIONS (Review but may proceed)

| Condition | Present | Reviewed | Accepted |
|-----------|---------|----------|----------|
| Low disk space | ☐ | ☐ | ☐ |
| Old snapshots need cleanup | ☐ | ☐ | ☐ |
| Git uncommitted changes | ☐ | ☐ | ☐ |
| Pattern index warnings | ☐ | ☐ | ☐ |
| Consistency warnings | ☐ | ☐ | ☐ |

## NO-GO CONDITIONS (STOP if present)

| Condition | Present |
|-----------|---------|
| Any backup creation failed | ☐ |
| Any critical validation failed | ☐ |
| Restoration test failed | ☐ |
| Corrupted files detected | ☐ |
| Insufficient disk space (<50MB) | ☐ |
| Critical work in progress | ☐ |
| No recovery capability | ☐ |

---

## FINAL DECISION

**GO** ☐ / **NO-GO** ☐

**If GO**:
- All critical criteria met: YES
- Warnings reviewed and accepted: YES
- No no-go conditions present: YES
- Ready to proceed: YES

**If NO-GO**:
- Reason: _______________________________
- Action required: _______________________
- Estimated fix time: ____________________
- Retry after: ___________________________
```

## Examples

### Example 1: Complete Checklist Execution

```bash
#!/bin/bash
# execute_checklist.sh - Execute full pre-compaction checklist

execute_checklist() {
    echo "==================================="
    echo "  PRE-COMPACTION CHECKLIST"
    echo "==================================="
    echo ""

    # PHASE 1: Preparation
    echo "PHASE 1: PREPARATION"
    echo "===================="
    if ! ./prepare_context.sh; then
        echo "✗ Preparation failed - STOP"
        return 1
    fi
    if ! ./extract_patterns.sh; then
        echo "✗ Pattern extraction failed - STOP"
        return 1
    fi
    if ! ./review_progress.sh; then
        echo "✗ Progress review failed - STOP"
        return 1
    fi
    echo "✓ Preparation phase complete"
    echo ""

    # PHASE 2: Backups
    echo "PHASE 2: BACKUPS"
    echo "================"
    if ! ./create_all_backups.sh; then
        echo "✗ Backup creation failed - STOP"
        return 1
    fi
    echo "✓ Backup phase complete"
    echo ""

    # PHASE 3: Validation
    echo "PHASE 3: VALIDATION"
    echo "==================="
    if ! ./run_all_validations.sh; then
        echo "✗ Validation failed - STOP"
        return 1
    fi
    echo "✓ Validation phase complete"
    echo ""

    # PHASE 4: Final verification
    echo "PHASE 4: FINAL VERIFICATION"
    echo "==========================="
    if ! ./test_restoration.sh; then
        echo "✗ Restoration test failed - STOP"
        return 1
    fi
    echo "✓ Final verification complete"
    echo ""

    # DECISION
    echo "==================================="
    echo "  GO/NO-GO DECISION"
    echo "==================================="
    echo "All checks passed"
    echo ""
    echo "DECISION: GO"
    echo "Ready to proceed with compaction"
    echo ""

    return 0
}

execute_checklist
```

### Example 2: Checklist with Stop Points

```bash
#!/bin/bash
# checklist_with_stops.sh - Checklist with manual approval points

# Phase 1
./prepare_context.sh || exit 1
read -p "Preparation OK? Continue? (y/n) " -r
[[ ! $REPLY =~ ^[Yy]$ ]] && exit 1

# Phase 2
./create_all_backups.sh || exit 1
read -p "Backups OK? Continue? (y/n) " -r
[[ ! $REPLY =~ ^[Yy]$ ]] && exit 1

# Phase 3
./run_all_validations.sh || exit 1
read -p "Validation OK? Continue? (y/n) " -r
[[ ! $REPLY =~ ^[Yy]$ ]] && exit 1

# Phase 4
./test_restoration.sh || exit 1
read -p "All checks passed. Proceed with compaction? (y/n) " -r
[[ ! $REPLY =~ ^[Yy]$ ]] && exit 1

echo "GO - Proceeding with compaction"
```

---

**Previous**: See [Part 1: Preparation and Backup](12-pre-compaction-checklist-part1-preparation-backup.md) for purpose, master checklist, preparation phase, and backup phase.
