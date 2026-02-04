# Context Update Patterns - Part 3: Pre-Compaction Update

This document covers the mandatory pre-compaction update pattern.

## Table of Contents

- [Pattern 5: Pre-Compaction Update](#pattern-5-pre-compaction-update)

## Pattern 5: Pre-Compaction Update

### When to Use

**Mandatory** before every compaction.

### Procedure

#### Step 1: Create Full Snapshot

```bash
#!/bin/bash
# pre_compaction_snapshot.sh - Create complete pre-compaction snapshot

timestamp=$(date -u +"%Y%m%d_%H%M%S")
snapshot_dir=".session_memory/snapshots/snapshot_$timestamp"

# Create snapshot directory
mkdir -p "$snapshot_dir"

# Copy all current state
cp .session_memory/active_context.md "$snapshot_dir/context.md"
cp .session_memory/progress_tracker.md "$snapshot_dir/progress.md"
cp .session_memory/pattern_index.md "$snapshot_dir/patterns.md"

# Create metadata
cat > "$snapshot_dir/metadata.txt" << EOF
Timestamp: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
Trigger: Pre-compaction
Compaction: Pending
EOF

# Update symlink
ln -sf "snapshot_$timestamp" .session_memory/snapshots/snapshot_latest

echo "✓ Full snapshot created: $snapshot_dir"
```

#### Step 2: Validate Memory Structure

```bash
# Run validation before compaction
./validate_all.sh

if [ $? -ne 0 ]; then
    echo "✗ Validation failed - DO NOT COMPACT"
    exit 1
fi
```

#### Step 3: Create Pre-Compaction Archive

```bash
# Get current compaction count
compaction_count=$(grep "Compaction Count:" .session_memory/session_info.md | grep -oP '\d+')
next_count=$((compaction_count + 1))

# Create archive directory
archive_dir=".session_memory/archived/pre_compaction_$next_count"
mkdir -p "$archive_dir"

# Copy state
cp .session_memory/active_context.md "$archive_dir/"
cp .session_memory/progress_tracker.md "$archive_dir/"
cp .session_memory/pattern_index.md "$archive_dir/"

# Create timestamp
echo "$(date -u +"%Y-%m-%d %H:%M:%S UTC")" > "$archive_dir/timestamp.txt"

echo "✓ Pre-compaction archive created: $archive_dir"
```

#### Step 4: Update Session Info

```bash
# Increment compaction count in session_info.md
sed -i '' "s/Compaction Count: $compaction_count/Compaction Count: $next_count/" .session_memory/session_info.md

# Add compaction record
cat >> .session_memory/session_info.md << EOF

## Compaction $next_count
**Date**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Pre-Compaction Snapshot**: $snapshot_dir
**Pre-Compaction Archive**: $archive_dir
**Status**: Ready

EOF
```

#### Step 5: Final Checklist

```markdown
## Pre-Compaction Checklist

- [ ] Full snapshot created
- [ ] Memory validation passed
- [ ] Pre-compaction archive created
- [ ] Session info updated
- [ ] All changes committed to git (if applicable)
- [ ] Ready to proceed with compaction
```

### Complete Example

```bash
#!/bin/bash
# prepare_for_compaction.sh - Complete pre-compaction preparation

prepare_for_compaction() {
    echo "=== Pre-Compaction Preparation ==="
    echo ""

    # Step 1: Full snapshot
    echo "Creating full snapshot..."
    timestamp=$(date -u +"%Y%m%d_%H%M%S")
    snapshot_dir=".session_memory/snapshots/snapshot_$timestamp"
    mkdir -p "$snapshot_dir"
    cp .session_memory/active_context.md "$snapshot_dir/context.md"
    cp .session_memory/progress_tracker.md "$snapshot_dir/progress.md"
    cp .session_memory/pattern_index.md "$snapshot_dir/patterns.md"
    cat > "$snapshot_dir/metadata.txt" << EOF
Timestamp: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
Trigger: Pre-compaction
EOF
    echo "✓ Snapshot: $snapshot_dir"
    echo ""

    # Step 2: Validate
    echo "Running validation..."
    if ! ./validate_all.sh; then
        echo "✗ VALIDATION FAILED - ABORTING"
        return 1
    fi
    echo "✓ Validation passed"
    echo ""

    # Step 3: Archive
    echo "Creating archive..."
    compaction_count=$(grep "Compaction Count:" .session_memory/session_info.md | grep -oP '\d+' || echo "0")
    next_count=$((compaction_count + 1))
    archive_dir=".session_memory/archived/pre_compaction_$next_count"
    mkdir -p "$archive_dir"
    cp .session_memory/active_context.md "$archive_dir/"
    cp .session_memory/progress_tracker.md "$archive_dir/"
    cp .session_memory/pattern_index.md "$archive_dir/"
    date -u +"%Y-%m-%d %H:%M:%S UTC" > "$archive_dir/timestamp.txt"
    echo "✓ Archive: $archive_dir"
    echo ""

    # Step 4: Update session info
    echo "Updating session info..."
    # (Update logic here)
    echo "✓ Session info updated"
    echo ""

    echo "=== Pre-Compaction Preparation Complete ==="
    echo "Ready to proceed with compaction"
    echo ""
    echo "Snapshot: $snapshot_dir"
    echo "Archive: $archive_dir"
    echo "Compaction: #$next_count"
}

prepare_for_compaction
```
