# Memory Directory Structure - Part 3: Examples and Troubleshooting

## Table of Contents
- 3.1 [Create Complete Structure from Scratch](#31-create-complete-structure-from-scratch)
- 3.2 [Verify Structure Integrity](#32-verify-structure-integrity)
- 3.3 [Create Snapshot with Proper Structure](#33-create-snapshot-with-proper-structure)
- 3.4 [Problem: Pattern Category Directories Missing](#34-problem-pattern-category-directories-missing)
- 3.5 [Problem: Symlinks Broken](#35-problem-symlinks-broken)
- 3.6 [Problem: Excessive Disk Usage](#36-problem-excessive-disk-usage)
- 3.7 [Problem: Cannot Determine Structure Version](#37-problem-cannot-determine-structure-version)
- 3.8 [Problem: File Permissions Prevent Access](#38-problem-file-permissions-prevent-access)

---

## 3.1 Create Complete Structure from Scratch

```bash
#!/bin/bash

create_memory_structure() {
    # Create all directories
    mkdir -p .session_memory/{active_context,patterns,progress,snapshots,archived}

    # Create pattern category subdirectories
    mkdir -p .session_memory/patterns/{problem_solution,workflow,decision_logic,error_recovery,configuration}

    # Create root files
    cat > .session_memory/session_info.md << 'EOF'
# Session Information
**Created:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Compaction Count:** 0
EOF

    cat > .session_memory/active_context.md << 'EOF'
# Active Context
**Last Updated:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")

## Current Focus
Initial setup
EOF

    cat > .session_memory/progress_tracker.md << 'EOF'
# Progress Tracker

## Active Tasks
- [ ] Initialize session memory
EOF

    cat > .session_memory/pattern_index.md << 'EOF'
# Pattern Index

## Recorded Patterns
None yet
EOF

    # Create archive README
    cat > .session_memory/archived/README.md << 'EOF'
# Archived Memory

## Archives
None yet
EOF

    echo "✓ Complete structure created"
}

create_memory_structure
```

---

## 3.2 Verify Structure Integrity

```bash
#!/bin/bash

check_structure_integrity() {
    echo "Checking structure integrity..."

    # Count expected vs actual directories
    expected_dirs=9  # Root + 5 subdirs + 5 pattern categories
    actual_dirs=$(find .session_memory -type d | wc -l)

    echo "Directories: Expected $expected_dirs, Found $actual_dirs"

    # List all directories
    echo -e "\nDirectory tree:"
    tree -d .session_memory 2>/dev/null || find .session_memory -type d

    # Count files by type
    echo -e "\nFile counts:"
    echo "Root files: $(find .session_memory -maxdepth 1 -type f | wc -l)"
    echo "Context snapshots: $(find .session_memory/active_context -type f | wc -l)"
    echo "Patterns: $(find .session_memory/patterns -type f -name '*.md' | wc -l)"
    echo "Progress snapshots: $(find .session_memory/progress -type f | wc -l)"
    echo "Full snapshots: $(find .session_memory/snapshots -type d -mindepth 1 | wc -l)"
    echo "Archives: $(find .session_memory/archived -type d -mindepth 1 | wc -l)"
}

check_structure_integrity
```

---

## 3.3 Create Snapshot with Proper Structure

```bash
#!/bin/bash

create_snapshot() {
    # Generate timestamp
    timestamp=$(date -u +"%Y%m%d_%H%M%S")
    snapshot_dir=".session_memory/snapshots/snapshot_$timestamp"

    # Create snapshot directory
    mkdir -p "$snapshot_dir"

    # Copy current state
    cp .session_memory/active_context.md "$snapshot_dir/context.md"
    cp .session_memory/progress_tracker.md "$snapshot_dir/progress.md"
    cp .session_memory/pattern_index.md "$snapshot_dir/patterns.md"

    # Create metadata
    cat > "$snapshot_dir/metadata.txt" << EOF
Timestamp: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
Trigger: Manual snapshot
Compaction: N/A
EOF

    # Update symlink
    ln -sf "snapshot_$timestamp" .session_memory/snapshots/snapshot_latest

    echo "✓ Snapshot created: $snapshot_dir"
}

create_snapshot
```

---

## 3.4 Problem: Pattern Category Directories Missing

**Cause**: Initialization incomplete or manual deletion

**Solution**:
```bash
# Recreate all pattern categories
mkdir -p .session_memory/patterns/{problem_solution,workflow,decision_logic,error_recovery,configuration}
```

---

## 3.5 Problem: Symlinks Broken

**Cause**: Target file deleted or moved

**Solution**:
```bash
# Remove broken symlinks
find .session_memory -type l -! -exec test -e {} \; -delete

# Recreate symlinks to latest files
latest_context=$(ls -t .session_memory/active_context/context_*.md 2>/dev/null | head -1)
if [ -n "$latest_context" ]; then
    ln -sf "$(basename "$latest_context")" .session_memory/active_context/context_latest.md
fi
```

---

## 3.6 Problem: Excessive Disk Usage

**Cause**: Too many snapshots accumulated

**Solution**:
```bash
# Keep only last 10 snapshots, archive the rest
cd .session_memory/snapshots
ls -t snapshot_* | tail -n +11 | while read old_snapshot; do
    mv "$old_snapshot" ../archived/
done
```

---

## 3.7 Problem: Cannot Determine Structure Version

**Cause**: No version tracking in session_info.md

**Solution**:
```bash
# Add version to session_info.md
echo "**Memory Version:** 1.0" >> .session_memory/session_info.md
```

---

## 3.8 Problem: File Permissions Prevent Access

**Cause**: Incorrect permissions on directories or files

**Solution**:
```bash
# Fix permissions recursively
chmod -R u+rw .session_memory
find .session_memory -type d -exec chmod u+x {} \;
```
