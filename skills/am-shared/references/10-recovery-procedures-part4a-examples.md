# Recovery Examples

**Parent Document**: [10-recovery-procedures.md](10-recovery-procedures.md)

## Table of Contents

1. [Example 1: Complete Recovery Workflow](#example-1-complete-recovery-workflow)
2. [Example 2: Partial Recovery (One File)](#example-2-partial-recovery-one-file)

---

## Example 1: Complete Recovery Workflow

Full recovery from failed compaction scenario.

```bash
#!/bin/bash
# complete_recovery_workflow.sh - Full recovery from failed compaction

echo "=== Starting Recovery ==="
echo "Time: $(date)"

# 1. Stop operations
echo ""
echo "Step 1: Stopping operations..."
running=$(ps aux | grep compaction | grep -v grep)
if [ -n "$running" ]; then
    echo "WARNING: Compaction still running"
    echo "$running"
    echo "Waiting for process to complete..."
    sleep 5
else
    echo "OK: No conflicting processes"
fi

# 2. Identify state
echo ""
echo "Step 2: Identifying last good state..."
compaction_count=$(grep "Compaction Count:" .session_memory/session_info.md 2>/dev/null | grep -oP '\d+' || echo "0")
echo "Compaction count: $compaction_count"

archive_dir=".session_memory/archived/pre_compaction_$compaction_count"
if [ -d "$archive_dir" ]; then
    echo "Found archive: $archive_dir"
else
    echo "ERROR: No archive found at $archive_dir"
    echo "Trying snapshots..."
    latest_snapshot=$(ls -dt .session_memory/snapshots/snapshot_* 2>/dev/null | head -1)
    if [ -n "$latest_snapshot" ]; then
        archive_dir="$latest_snapshot"
        echo "Using snapshot: $archive_dir"
    else
        echo "ERROR: No recovery source found"
        echo "Emergency recovery required"
        exit 1
    fi
fi

# 3. Backup corrupted state
echo ""
echo "Step 3: Backing up corrupted state..."
backup_dir=".session_memory/corrupted_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$backup_dir"
cp .session_memory/*.md "$backup_dir/" 2>/dev/null || true
echo "Backup saved to: $backup_dir"

# 4. Restore
echo ""
echo "Step 4: Restoring from archive..."
for file in active_context.md progress_tracker.md pattern_index.md; do
    if [ -f "$archive_dir/$file" ]; then
        cp "$archive_dir/$file" ".session_memory/$file"
        echo "  Restored: $file"
    else
        echo "  WARNING: $file not in archive"
    fi
done

# 5. Validate
echo ""
echo "Step 5: Validating..."
errors=0
for file in active_context.md progress_tracker.md pattern_index.md; do
    if [ -f ".session_memory/$file" ] && [ -s ".session_memory/$file" ]; then
        echo "  OK: $file"
    else
        echo "  ERROR: $file missing or empty"
        errors=$((errors + 1))
    fi
done

if [ $errors -gt 0 ]; then
    echo "Validation failed with $errors errors"
    exit 1
fi

# 6. Document
echo ""
echo "Step 6: Documenting recovery..."
cat >> .session_memory/session_info.md << EOF

## Recovery $(date -u +"%Y-%m-%d %H:%M:%S UTC")
- **Reason**: Failed compaction #$compaction_count
- **Source**: $archive_dir
- **Corrupted backup**: $backup_dir
- **Status**: Successful

EOF

echo ""
echo "=== Recovery Complete ==="
echo "Time: $(date)"
```

**When to use this example:**
- Compaction failed mid-process
- Session memory in inconsistent state
- Archives available for recovery

---

## Example 2: Partial Recovery (One File)

Recover just one corrupted file while preserving others.

```bash
#!/bin/bash
# recover_single_file.sh - Recover just one corrupted file

# Configuration
recover_file="active_context.md"
full_path=".session_memory/$recover_file"

echo "=== Single File Recovery ==="
echo "Target: $recover_file"

# Check current state
echo ""
echo "Current file state:"
if [ -f "$full_path" ]; then
    echo "  Exists: yes"
    echo "  Size: $(wc -c < "$full_path") bytes"
    echo "  Lines: $(wc -l < "$full_path")"

    # Check if readable/valid
    if head -1 "$full_path" | grep -q "^#"; then
        echo "  Valid header: yes"
    else
        echo "  Valid header: no (corruption likely)"
    fi
else
    echo "  Exists: no"
fi

# Backup corrupted version
echo ""
echo "Backing up corrupted version..."
backup_path="${full_path}.corrupted.$(date +%Y%m%d_%H%M%S)"
cp "$full_path" "$backup_path" 2>/dev/null || true
echo "Backup: $backup_path"

# Find best recovery source
echo ""
echo "Finding recovery source..."

case "$recover_file" in
    "active_context.md")
        snapshot_pattern=".session_memory/active_context/context_*.md"
        ;;
    "progress_tracker.md")
        snapshot_pattern=".session_memory/progress/progress_*.md"
        ;;
    *)
        snapshot_pattern=".session_memory/snapshots/snapshot_*/$recover_file"
        ;;
esac

latest=$(ls -t $snapshot_pattern 2>/dev/null | head -1)

if [ -n "$latest" ]; then
    echo "Found: $latest"
    echo "  Created: $(stat -f "%Sm" "$latest" 2>/dev/null || stat -c "%y" "$latest" 2>/dev/null)"

    # Restore
    cp "$latest" "$full_path"
    echo "Restored from snapshot"
else
    echo "No snapshot found"
    echo "Trying archives..."

    archive_file=$(ls -t .session_memory/archived/pre_compaction_*/$recover_file 2>/dev/null | head -1)
    if [ -n "$archive_file" ]; then
        cp "$archive_file" "$full_path"
        echo "Restored from archive: $archive_file"
    else
        echo "ERROR: No recovery source available"
        exit 1
    fi
fi

# Validate
echo ""
echo "Validating restored file..."
if [ -f "$full_path" ] && grep -q "^#" "$full_path"; then
    echo "OK: File recovered successfully"
    echo "  Size: $(wc -c < "$full_path") bytes"
    echo "  Lines: $(wc -l < "$full_path")"
else
    echo "ERROR: Recovery failed"
    exit 1
fi
```

**When to use this example:**
- Single file corrupted
- Other files intact
- Want minimal changes

---

## Related Documents

- [10-recovery-procedures.md](10-recovery-procedures.md) - Main recovery index
- [Part 4b: Troubleshooting](10-recovery-procedures-part4b-troubleshooting.md) - Common problems
- [Part 1: Failed Compaction](10-recovery-procedures-part1-failed-compaction.md) - Detailed procedure
- [Part 2: Corruption](10-recovery-procedures-part2-corruption-context.md) - File corruption recovery
