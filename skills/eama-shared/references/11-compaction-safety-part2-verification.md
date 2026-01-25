# Compaction Safety - Part 2: Verification and Recovery

## Table of Contents
1. [Post-compaction verification](#post-compaction-verification)
   - 1.1 [Verification Checklist](#verification-checklist)
   - 1.2 [Automated Verification Script](#automated-verification-script)
2. [How to rollback if needed](#rollback-procedure)
   - 2.1 [When to Rollback](#when-to-rollback)
   - 2.2 [Rollback Script](#rollback-script)
3. [For implementation examples](#examples)
   - 3.1 [Example 1: Complete Safe Compaction](#example-1-complete-safe-compaction)
   - 3.2 [Example 2: Compaction with Manual Review](#example-2-compaction-with-manual-review)
4. [If issues occur](#troubleshooting)
   - 4.1 [Problem: Pre-Flight Checks Fail](#problem-pre-flight-checks-fail)
   - 4.2 [Problem: Compaction Fails Mid-Way](#problem-compaction-fails-mid-way)
   - 4.3 [Problem: Cannot Rollback - Archive Missing](#problem-cannot-rollback---archive-missing)
   - 4.4 [Problem: Post-Compaction Validation Fails](#problem-post-compaction-validation-fails)

**Related**: See [11-compaction-safety-part1-preparation.md](11-compaction-safety-part1-preparation.md) for:
- Understanding compaction purpose
- Compaction risk analysis
- Pre-compaction safety checks
- Safe compaction procedure

---

## Post-Compaction Verification

### Verification Checklist

```markdown
# Post-Compaction Verification Checklist

## File Integrity
- [ ] active_context.md exists and readable
- [ ] progress_tracker.md exists and readable
- [ ] pattern_index.md exists and readable
- [ ] All files have valid markdown syntax

## Content Integrity
- [ ] Current focus preserved or updated
- [ ] Critical decisions preserved
- [ ] Open questions preserved or resolved
- [ ] Active tasks preserved
- [ ] Pattern index accurate

## Structure Integrity
- [ ] All required sections present
- [ ] No broken links or references
- [ ] Timestamps updated
- [ ] Compaction count incremented

## Recovery Capability
- [ ] Pre-compaction snapshot exists
- [ ] Pre-compaction archive exists
- [ ] Archives are complete
- [ ] Test restoration works

## Validation
- [ ] Structure validation passes
- [ ] Content validation passes
- [ ] Consistency validation passes
- [ ] Recovery validation passes
```

### Automated Verification Script

```bash
#!/bin/bash
# post_compaction_verification.sh - Verify compaction success

post_compaction_verification() {
    local compaction_count="$1"
    local errors=0

    echo "=== Post-Compaction Verification ==="
    echo "Compaction #$compaction_count"
    echo ""

    # Verify files exist
    echo "Verifying files..."
    required_files=(
        "active_context.md"
        "progress_tracker.md"
        "pattern_index.md"
        "session_info.md"
    )

    for file in "${required_files[@]}"; do
        if [ ! -f ".session_memory/$file" ]; then
            echo "ERROR: Missing: $file"
            ((errors++))
        else
            echo "OK: Exists: $file"
        fi
    done

    # Verify backups exist
    echo ""
    echo "Verifying backups..."
    snapshot_dir=".session_memory/snapshots/snapshot_latest"
    archive_dir=".session_memory/archived/pre_compaction_$compaction_count"

    if [ -L "$snapshot_dir" ]; then
        echo "OK: Snapshot exists"
    else
        echo "ERROR: Snapshot missing"
        ((errors++))
    fi

    if [ -d "$archive_dir" ]; then
        echo "OK: Archive exists"
    else
        echo "ERROR: Archive missing"
        ((errors++))
    fi

    # Run full validation
    echo ""
    echo "Running full validation..."
    if ./validate_all.sh > /dev/null 2>&1; then
        echo "OK: Validation passed"
    else
        echo "ERROR: Validation failed"
        ((errors++))
    fi

    # Summary
    echo ""
    if [ $errors -eq 0 ]; then
        echo "OK: POST-COMPACTION VERIFICATION PASSED"
        return 0
    else
        echo "ERROR: POST-COMPACTION VERIFICATION FAILED ($errors errors)"
        echo "WARNING: CONSIDER ROLLBACK"
        return 1
    fi
}

# Usage
post_compaction_verification 3
```

## Rollback Procedure

### When to Rollback

Rollback if:
- Post-compaction validation fails
- Critical information lost
- Memory corrupted during compaction
- User explicitly requests rollback

### Rollback Script

```bash
#!/bin/bash
# rollback_compaction.sh - Rollback to pre-compaction state

rollback_compaction() {
    local compaction_count="$1"
    local archive_dir=".session_memory/archived/pre_compaction_$compaction_count"

    echo "=== ROLLBACK INITIATED ==="
    echo "Compaction #$compaction_count"
    echo ""

    # Verify archive exists
    if [ ! -d "$archive_dir" ]; then
        echo "ERROR: Archive not found: $archive_dir"
        echo "Cannot rollback - archive missing"
        return 1
    fi

    echo "Archive found: $archive_dir"
    echo ""

    # Backup current state (post-compaction)
    echo "Backing up post-compaction state..."
    backup_dir=".session_memory/failed_compaction_${compaction_count}_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    cp .session_memory/*.md "$backup_dir/" 2>/dev/null || true
    echo "OK: Post-compaction state saved to: $backup_dir"

    # Restore from archive
    echo ""
    echo "Restoring from archive..."
    cp "$archive_dir/active_context.md" .session_memory/
    cp "$archive_dir/progress_tracker.md" .session_memory/
    cp "$archive_dir/pattern_index.md" .session_memory/

    # Verify restoration
    echo ""
    echo "Verifying restoration..."
    if [ -f ".session_memory/active_context.md" ] && \
       [ -f ".session_memory/progress_tracker.md" ] && \
       [ -f ".session_memory/pattern_index.md" ]; then
        echo "OK: Files restored"
    else
        echo "ERROR: Restoration failed"
        return 1
    fi

    # Decrement compaction count
    echo ""
    echo "Reverting compaction count..."
    prev_count=$((compaction_count - 1))
    sed -i '' "s/Compaction Count: $compaction_count/Compaction Count: $prev_count/" .session_memory/session_info.md

    # Document rollback
    cat >> .session_memory/session_info.md << EOF

## Compaction $compaction_count - ROLLED BACK
**Date**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Status**: Rolled back due to failure
**Restored From**: $archive_dir
**Failed State Saved To**: $backup_dir
**Action Required**: Investigate failure before re-attempting compaction

EOF

    # Validate
    echo ""
    echo "Validating restored state..."
    if ./validate_all.sh > /dev/null 2>&1; then
        echo "OK: Validation passed"
    else
        echo "WARNING: Validation failed after rollback"
        echo "  Manual intervention required"
    fi

    echo ""
    echo "=== ROLLBACK COMPLETE ==="
    echo "Rolled back to pre-compaction state"
    echo "Investigate failure before re-attempting"
}

# Usage
rollback_compaction 3
```

## Examples

### Example 1: Complete Safe Compaction

```bash
#!/bin/bash
# Full safe compaction workflow

echo "Starting safe compaction..."
echo ""

# 1. Pre-flight checks
echo "1. Running pre-flight checks..."
if ! ./pre_compaction_checks.sh; then
    echo "ERROR: Pre-flight failed - ABORTING"
    exit 1
fi

# 2. Create backups
echo "2. Creating backups..."
./create_full_snapshot.sh
./create_precompaction_archive.sh

# 3. Test restoration
echo "3. Testing restoration..."
./test_restore_capability.sh

# 4. Perform compaction
echo "4. Performing compaction..."
# [Actual compaction logic]

# 5. Verify
echo "5. Post-compaction verification..."
if ! ./post_compaction_verification.sh 3; then
    echo "ERROR: Verification failed - ROLLING BACK"
    ./rollback_compaction.sh 3
    exit 1
fi

echo "OK: Compaction successful"
```

### Example 2: Compaction with Manual Review

```bash
#!/bin/bash
# Compaction with manual approval at each step

compaction_with_approval() {
    echo "=== Compaction with Manual Approval ==="

    # Pre-flight
    echo "Running pre-flight checks..."
    ./pre_compaction_checks.sh
    read -p "Pre-flight OK? Proceed with backups? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted"
        return 1
    fi

    # Backups
    echo "Creating backups..."
    ./create_full_snapshot.sh
    ./create_precompaction_archive.sh
    read -p "Backups created. Proceed with compaction? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted"
        return 1
    fi

    # Compaction
    echo "Performing compaction..."
    # [Compaction logic]

    # Verification
    echo "Running verification..."
    ./post_compaction_verification.sh
    read -p "Verification complete. Accept result? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Rolling back..."
        ./rollback_compaction.sh
        return 1
    fi

    echo "OK: Compaction accepted"
}

compaction_with_approval
```

## Troubleshooting

### Problem: Pre-Flight Checks Fail

**Solution**:
```bash
# Identify specific failure
./pre_compaction_checks.sh

# Fix each issue:
# - Low disk space: Clean up old snapshots
# - Validation fails: Fix memory structure
# - Running processes: Wait for completion
# - No snapshot: Create snapshot

# Re-run checks
./pre_compaction_checks.sh
```

### Problem: Compaction Fails Mid-Way

**Solution**:
```bash
# DO NOT RETRY - Rollback first
./rollback_compaction.sh [compaction_number]

# Investigate failure
# Check logs, disk space, permissions

# Fix root cause
# Re-run pre-flight checks
# Retry compaction
```

### Problem: Cannot Rollback - Archive Missing

**Solution**:
```bash
# Attempt recovery from snapshot
latest_snapshot=$(ls -t .session_memory/snapshots/snapshot_*/context.md | head -1)
snapshot_dir=$(dirname "$latest_snapshot")

# Restore from snapshot
cp "$snapshot_dir/context.md" .session_memory/active_context.md
cp "$snapshot_dir/progress.md" .session_memory/progress_tracker.md
cp "$snapshot_dir/patterns.md" .session_memory/pattern_index.md

# Validate
./validate_all.sh
```

### Problem: Post-Compaction Validation Fails

**Solution**:
```bash
# Immediate rollback
./rollback_compaction.sh [compaction_number]

# Do not attempt to fix in-place
# Rollback first, then investigate
# Fix issues, then retry compaction
```
