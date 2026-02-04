# Pre-Compaction Backup and Validation Phase

This file contains scripts for creating backups and running validations before compaction.

## Table of Contents
1. [Backup Creation Script](#backup-creation-script)
2. [Complete Validation Script](#complete-validation-script)

---

## Backup Phase

### Backup Creation Script

```bash
#!/bin/bash
# create_all_backups.sh - Create all required backups

create_all_backups() {
    local timestamp=$(date -u +"%Y%m%d_%H%M%S")
    local compaction_count=$(grep "Compaction Count:" .session_memory/session_info.md | grep -oP '\d+' || echo "0")
    local next_count=$((compaction_count + 1))

    echo "=== Creating All Backups ==="
    echo "Timestamp: $timestamp"
    echo "Compaction: #$next_count"
    echo ""

    # 1. Context snapshot
    echo "1. Creating context snapshot..."
    snapshot_file=".session_memory/active_context/context_$timestamp.md"
    cp .session_memory/active_context.md "$snapshot_file"
    ln -sf "context_$timestamp.md" .session_memory/active_context/context_latest.md
    if [ -f "$snapshot_file" ]; then
        echo "✓ Context snapshot: $snapshot_file"
    else
        echo "✗ Failed to create context snapshot"
        return 1
    fi

    # 2. Progress snapshot
    echo ""
    echo "2. Creating progress snapshot..."
    progress_file=".session_memory/progress/progress_$timestamp.md"
    cp .session_memory/progress_tracker.md "$progress_file"
    ln -sf "progress_$timestamp.md" .session_memory/progress/progress_latest.md
    if [ -f "$progress_file" ]; then
        echo "✓ Progress snapshot: $progress_file"
    else
        echo "✗ Failed to create progress snapshot"
        return 1
    fi

    # 3. Full session snapshot
    echo ""
    echo "3. Creating full session snapshot..."
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
    ln -sf "snapshot_$timestamp" .session_memory/snapshots/snapshot_latest
    if [ -d "$snapshot_dir" ]; then
        echo "✓ Full snapshot: $snapshot_dir"
    else
        echo "✗ Failed to create full snapshot"
        return 1
    fi

    # 4. Pre-compaction archive
    echo ""
    echo "4. Creating pre-compaction archive..."
    archive_dir=".session_memory/archived/pre_compaction_$next_count"
    mkdir -p "$archive_dir"
    cp .session_memory/active_context.md "$archive_dir/"
    cp .session_memory/progress_tracker.md "$archive_dir/"
    cp .session_memory/pattern_index.md "$archive_dir/"
    date -u +"%Y-%m-%d %H:%M:%S UTC" > "$archive_dir/timestamp.txt"
    if [ -d "$archive_dir" ]; then
        echo "✓ Pre-compaction archive: $archive_dir"
    else
        echo "✗ Failed to create archive"
        return 1
    fi

    echo ""
    echo "✓ All backups created successfully"
    echo ""
    echo "Summary:"
    echo "  Context snapshot: $snapshot_file"
    echo "  Progress snapshot: $progress_file"
    echo "  Full snapshot: $snapshot_dir"
    echo "  Archive: $archive_dir"

    return 0
}

create_all_backups
```

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

---

## Backup and Validation Summary

### Backup Phase Creates:
1. **Context snapshot** - Timestamped copy of active_context.md
2. **Progress snapshot** - Timestamped copy of progress_tracker.md
3. **Full session snapshot** - Complete snapshot with all files + metadata
4. **Pre-compaction archive** - Numbered archive for recovery

### Validation Phase Checks:
1. **Structure** - Directory structure and required files exist
2. **Content** - Files contain valid markdown with required sections
3. **Consistency** - Pattern index matches files, no orphans
4. **Recovery** - Snapshots exist and restoration is possible

**CRITICAL**: All backups must succeed and all validations must pass before proceeding.
