# Compaction Safety - Part 1: Preparation and Execution

## Table of Contents
1. [When you need to understand the purpose](#purpose)
2. [Understanding compaction risks](#compaction-risks)
   - 2.1 [Risk 1: Data Loss](#risk-1-data-loss)
   - 2.2 [Risk 2: Compaction Failure](#risk-2-compaction-failure)
   - 2.3 [Risk 3: Information Loss Without Data Loss](#risk-3-information-loss-without-data-loss)
   - 2.4 [Risk 4: Incomplete Recovery After Failure](#risk-4-incomplete-recovery-after-failure)
3. [Pre-compaction safety checks](#pre-compaction-safety-checks)
   - 3.1 [Safety Checklist](#safety-checklist)
   - 3.2 [Automated Pre-Check Script](#automated-pre-check-script)
4. [How to perform safe compaction](#safe-compaction-procedure)
   - 4.1 [Step-by-Step Safe Compaction](#step-by-step-safe-compaction)

**Related**: See [11-compaction-safety-part2-verification.md](11-compaction-safety-part2-verification.md) for:
- Post-compaction verification procedures
- Rollback procedures
- Implementation examples
- Troubleshooting guide

---

## Purpose

Compaction safety procedures prevent data loss during context compaction. Safe compaction:
- Preserves critical information
- Enables recovery if compaction fails
- Validates data integrity
- Maintains traceability
- Minimizes risk

## Compaction Risks

### Risk 1: Data Loss

**Description**: Critical information permanently deleted during compaction

**Likelihood**: Medium (if safety procedures not followed)

**Impact**: High (lost context cannot be recovered)

**Mitigation**:
- Create pre-compaction snapshot
- Create pre-compaction archive
- Validate snapshot before proceeding
- Test restoration capability

### Risk 2: Compaction Failure

**Description**: Compaction process fails mid-way, corrupting memory

**Likelihood**: Low (but possible)

**Impact**: High (memory left in inconsistent state)

**Mitigation**:
- Use atomic operations
- Create backups before changes
- Validate each step
- Have rollback procedure ready

### Risk 3: Information Loss Without Data Loss

**Description**: Data preserved but important relationships or context lost

**Likelihood**: Medium (easy to accidentally delete important references)

**Impact**: Medium (information exists but hard to find or understand)

**Mitigation**:
- Review what will be removed
- Preserve patterns and key decisions
- Maintain index integrity
- Document what was archived

### Risk 4: Incomplete Recovery After Failure

**Description**: Restoration doesn't fully recover to pre-compaction state

**Likelihood**: Low (if proper backups created)

**Impact**: Medium (some manual reconstruction needed)

**Mitigation**:
- Test restoration before compaction
- Multiple backup layers (snapshot + archive)
- Validate restored state
- Keep multiple recovery points

## Pre-Compaction Safety Checks

### Safety Checklist

```markdown
# Pre-Compaction Safety Checklist

## Prerequisites
- [ ] No critical work in progress
- [ ] All important decisions recorded
- [ ] Patterns extracted from context
- [ ] Progress tracker up to date

## Snapshot Creation
- [ ] Context snapshot created
- [ ] Progress snapshot created
- [ ] Pattern index snapshot created
- [ ] Full session snapshot created
- [ ] Snapshot completeness verified

## Archive Creation
- [ ] Pre-compaction archive directory created
- [ ] All files copied to archive
- [ ] Archive timestamp recorded
- [ ] Archive index updated

## Validation
- [ ] Memory structure validation passed
- [ ] Content validation passed
- [ ] Consistency validation passed
- [ ] Recovery validation passed

## Recovery Readiness
- [ ] Restoration procedure tested
- [ ] Rollback script available
- [ ] Latest archive timestamp verified
- [ ] Snapshot integrity confirmed

## Final Checks
- [ ] Git changes committed (if applicable)
- [ ] No running processes accessing memory
- [ ] Sufficient disk space
- [ ] Ready to proceed
```

### Automated Pre-Check Script

```bash
#!/bin/bash
# pre_compaction_checks.sh - Automated safety checks before compaction

pre_compaction_checks() {
    local errors=0
    local warnings=0

    echo "=== Pre-Compaction Safety Checks ==="
    echo ""

    # Check 1: Disk space
    echo "Check 1: Disk space..."
    available=$(df . | tail -1 | awk '{print $4}')
    if [ "$available" -lt 100000 ]; then
        echo "WARNING: Low disk space ($available KB)"
        ((warnings++))
    else
        echo "OK: Sufficient disk space"
    fi

    # Check 2: No running processes
    echo ""
    echo "Check 2: Running processes..."
    if ps aux | grep -E "(compaction|snapshot)" | grep -v grep > /dev/null; then
        echo "ERROR: Compaction or snapshot process already running"
        ((errors++))
    else
        echo "OK: No conflicting processes"
    fi

    # Check 3: Recent snapshot exists
    echo ""
    echo "Check 3: Recent snapshot..."
    latest_snapshot=$(ls -t .session_memory/snapshots/snapshot_*/metadata.txt 2>/dev/null | head -1)
    if [ -z "$latest_snapshot" ]; then
        echo "ERROR: No snapshot available"
        ((errors++))
    else
        snapshot_time=$(grep "Timestamp:" "$latest_snapshot" | cut -d: -f2- | xargs)
        echo "OK: Snapshot available: $snapshot_time"
    fi

    # Check 4: Git status (if in git repo)
    echo ""
    echo "Check 4: Git status..."
    if git rev-parse --git-dir > /dev/null 2>&1; then
        if git diff --quiet && git diff --cached --quiet; then
            echo "OK: No uncommitted changes"
        else
            echo "WARNING: Uncommitted git changes"
            ((warnings++))
        fi
    else
        echo "WARNING: Not in git repository"
    fi

    # Check 5: Memory validation
    echo ""
    echo "Check 5: Memory validation..."
    if ./validate_all.sh > /dev/null 2>&1; then
        echo "OK: Memory validation passed"
    else
        echo "ERROR: Memory validation failed"
        echo "  Run './validate_all.sh' for details"
        ((errors++))
    fi

    # Summary
    echo ""
    echo "=== Pre-Check Summary ==="
    echo "Errors: $errors"
    echo "Warnings: $warnings"
    echo ""

    if [ $errors -eq 0 ]; then
        if [ $warnings -eq 0 ]; then
            echo "OK: ALL CHECKS PASSED - Safe to proceed with compaction"
            return 0
        else
            echo "WARNING: CHECKS PASSED WITH WARNINGS - Review warnings before proceeding"
            return 0
        fi
    else
        echo "ERROR: CHECKS FAILED - DO NOT PROCEED with compaction"
        echo "Fix errors before attempting compaction"
        return 1
    fi
}

pre_compaction_checks
```

## Safe Compaction Procedure

### Step-by-Step Safe Compaction

```bash
#!/bin/bash
# safe_compaction.sh - Compaction with full safety procedures

safe_compaction() {
    local timestamp=$(date -u +"%Y%m%d_%H%M%S")
    local compaction_count=$(grep "Compaction Count:" .session_memory/session_info.md | grep -oP '\d+' || echo "0")
    local next_count=$((compaction_count + 1))

    echo "=== Safe Compaction Procedure ==="
    echo "Compaction #$next_count"
    echo "Timestamp: $timestamp"
    echo ""

    # PHASE 1: Pre-Flight Checks
    echo "PHASE 1: Pre-Flight Checks"
    echo "----------------------------"
    if ! ./pre_compaction_checks.sh; then
        echo "ERROR: Pre-flight checks failed - ABORTING"
        return 1
    fi
    echo "OK: Pre-flight checks passed"
    echo ""

    # PHASE 2: Create Safety Backups
    echo "PHASE 2: Create Safety Backups"
    echo "-------------------------------"

    # Full snapshot
    echo "Creating full snapshot..."
    snapshot_dir=".session_memory/snapshots/snapshot_$timestamp"
    mkdir -p "$snapshot_dir"
    cp .session_memory/active_context.md "$snapshot_dir/context.md"
    cp .session_memory/progress_tracker.md "$snapshot_dir/progress.md"
    cp .session_memory/pattern_index.md "$snapshot_dir/patterns.md"
    cat > "$snapshot_dir/metadata.txt" << EOF
Timestamp: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
Trigger: Pre-compaction
Compaction: $next_count
EOF
    echo "OK: Full snapshot created: $snapshot_dir"

    # Pre-compaction archive
    echo "Creating pre-compaction archive..."
    archive_dir=".session_memory/archived/pre_compaction_$next_count"
    mkdir -p "$archive_dir"
    cp .session_memory/active_context.md "$archive_dir/"
    cp .session_memory/progress_tracker.md "$archive_dir/"
    cp .session_memory/pattern_index.md "$archive_dir/"
    date -u +"%Y-%m-%d %H:%M:%S UTC" > "$archive_dir/timestamp.txt"
    echo "OK: Pre-compaction archive created: $archive_dir"
    echo ""

    # PHASE 3: Validation Before Compaction
    echo "PHASE 3: Validation"
    echo "-------------------"
    if ! ./validate_all.sh > /dev/null 2>&1; then
        echo "ERROR: Validation failed - ABORTING"
        return 1
    fi
    echo "OK: Validation passed"
    echo ""

    # PHASE 4: Test Restoration
    echo "PHASE 4: Test Restoration Capability"
    echo "-------------------------------------"
    test_restore_dir=$(mktemp -d)
    if cp "$snapshot_dir"/* "$test_restore_dir/" 2>/dev/null; then
        echo "OK: Snapshot files are restorable"
        rm -rf "$test_restore_dir"
    else
        echo "ERROR: Cannot restore from snapshot - ABORTING"
        rm -rf "$test_restore_dir"
        return 1
    fi
    echo ""

    # PHASE 5: Perform Compaction
    echo "PHASE 5: Compaction"
    echo "-------------------"
    echo "WARNING: COMPACTION WOULD OCCUR HERE"
    echo "  (Actual compaction logic not shown for safety)"
    echo ""

    # PHASE 6: Post-Compaction Validation
    echo "PHASE 6: Post-Compaction Validation"
    echo "------------------------------------"
    if ! ./validate_all.sh > /dev/null 2>&1; then
        echo "ERROR: Post-compaction validation failed"
        echo "  INITIATING ROLLBACK"
        ./rollback_compaction.sh "$next_count"
        return 1
    fi
    echo "OK: Post-compaction validation passed"
    echo ""

    # PHASE 7: Update Metadata
    echo "PHASE 7: Update Metadata"
    echo "------------------------"
    sed -i '' "s/Compaction Count: $compaction_count/Compaction Count: $next_count/" .session_memory/session_info.md
    cat >> .session_memory/session_info.md << EOF

## Compaction $next_count
**Date**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Status**: Success
**Pre-Compaction Snapshot**: $snapshot_dir
**Pre-Compaction Archive**: $archive_dir
**Post-Compaction Validation**: Passed

EOF
    echo "OK: Metadata updated"
    echo ""

    # PHASE 8: Cleanup
    echo "PHASE 8: Cleanup"
    echo "----------------"
    # Keep last 5 snapshots
    cd .session_memory/snapshots
    ls -t | grep "^snapshot_" | tail -n +6 | xargs rm -rf 2>/dev/null || true
    cd - > /dev/null
    echo "OK: Old snapshots cleaned up"
    echo ""

    echo "=== Compaction Complete ==="
    echo "Compaction #$next_count successful"
    echo "All safety checks passed"
}

safe_compaction
```
