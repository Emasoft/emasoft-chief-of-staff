# Pre-Compaction Verification and Decision

This file contains final verification procedures, go/no-go decision criteria, and execution examples.

## Table of Contents
1. [Restoration Test Script](#restoration-test)
2. [Go/No-Go Decision Matrix](#gono-go-decision)
3. [Complete Checklist Execution Example](#example-1-complete-checklist-execution)
4. [Checklist with Stop Points Example](#example-2-checklist-with-stop-points)

---

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

---

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

---

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

## Summary

The pre-compaction checklist ensures safe compaction by:

1. **Preparation** - Documenting context, extracting patterns, reviewing progress
2. **Backup** - Creating multiple backup types for recovery
3. **Validation** - Verifying structure, content, consistency, and recovery capability
4. **Verification** - Testing actual restoration before proceeding
5. **Decision** - Making informed go/no-go based on clear criteria

**NEVER proceed with compaction if any critical check fails.**
