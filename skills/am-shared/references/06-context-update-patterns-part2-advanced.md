# Context Update Patterns - Part 2: Advanced Patterns

## Table of Contents
1. [When reaching milestones](#pattern-4-progress-milestone-update)
2. [When preparing before compaction](#pattern-5-pre-compaction-update)
3. [For implementation examples](#examples)
4. [If issues occur](#troubleshooting)

**See Also**: [Part 1: Core Patterns](06-context-update-patterns-part1-core.md) for:
- Purpose and Overview
- Pattern 1: Task Switch Update
- Pattern 2: Decision Recording Update
- Pattern 3: Question Addition Update

## Pattern 4: Progress Milestone Update

### When to Use

Use this pattern when:
- Completing major task or phase
- Reaching project milestone
- Finishing sprint or iteration
- Achieving significant goal

### Procedure

#### Step 1: Create Context Snapshot

```bash
# Snapshot current state
timestamp=$(date -u +"%Y%m%d_%H%M%S")
cp .session_memory/active_context.md ".session_memory/active_context/context_$timestamp.md"
cp .session_memory/progress_tracker.md ".session_memory/progress/progress_$timestamp.md"
```

#### Step 2: Update Progress Tracker

Move completed task:

```markdown
## Completed Tasks

- [x] [Task name]
  - **Started**: 2026-01-01 10:00 UTC
  - **Completed**: 2026-01-01 14:30 UTC
  - **Duration**: 4.5 hours
  - **Outcome**: [What was achieved]
  - **Learnings**: [What was learned]
```

#### Step 3: Update Active Context

Add to Recent Decisions:

```markdown
## Recent Decisions

### Milestone: [Milestone Name]
**Date**: 2026-01-01 14:30 UTC

**What Was Achieved**:
- Achievement 1
- Achievement 2

**Key Learnings**:
- Learning 1
- Learning 2

**Next Phase**:
[What comes next]
```

#### Step 4: Record Pattern (if reusable)

If milestone involved reusable knowledge, create pattern:

```bash
# Create workflow pattern for reusable procedures
./record_pattern.sh "workflow" "Task completion procedure"
```

### Complete Example

```bash
#!/bin/bash
# milestone_update.sh - Update context after milestone

milestone_update() {
    local milestone_name="$1"

    timestamp=$(date -u +"%Y%m%d_%H%M%S")
    timestamp_display=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

    # Create snapshots
    cp .session_memory/active_context.md ".session_memory/active_context/context_$timestamp.md"
    cp .session_memory/progress_tracker.md ".session_memory/progress/progress_$timestamp.md"

    # Add milestone to context
    cat >> .session_memory/active_context.md << EOF

### Milestone: $milestone_name
**Date**: $timestamp_display

**What Was Achieved**:
[To be filled]

**Key Learnings**:
[To be filled]

**Next Phase**:
[To be filled]

EOF

    echo "✓ Milestone snapshot created"
    echo "✓ Update context with milestone details"
}

milestone_update "Authentication System Complete"
```

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

## Examples

### Example 1: Combined Update - Task Switch with Decision

```bash
# Switching tasks after making decision

# 1. Create snapshot
timestamp=$(date -u +"%Y%m%d_%H%M%S")
cp .session_memory/active_context.md ".session_memory/active_context/context_$timestamp.md"

# 2. Record decision about completed task
cat >> .session_memory/active_context.md << 'EOF'

### Decision: Completed testing approach selection
**Date**: 2026-01-01 14:30 UTC
**Outcome**: Selected Jest over Mocha for better TypeScript support

EOF

# 3. Archive old focus
# (Move to Recent Decisions)

# 4. Update to new focus
cat > .session_memory/active_context.md << 'EOF'
# Active Context

**Last Updated**: 2026-01-01 14:35 UTC

## Current Focus

### Primary Task
Implement user authentication system

[Rest of context...]
EOF
```

### Example 2: Milestone with Pattern Recording

```bash
# Completed milestone, record reusable pattern

# 1. Snapshot
timestamp=$(date -u +"%Y%m%d_%H%M%S")
cp .session_memory/active_context.md ".session_memory/active_context/context_$timestamp.md"
cp .session_memory/progress_tracker.md ".session_memory/progress/progress_$timestamp.md"

# 2. Record pattern
./record_pattern.sh "workflow" "parallel-testing-setup"

# 3. Update context with milestone
cat >> .session_memory/active_context.md << 'EOF'

### Milestone: Testing Infrastructure Complete
**Date**: 2026-01-01 15:00 UTC

**Achievements**:
- Parallel test execution working
- Test time reduced from 30min to 8min
- Pattern recorded for future use

**Pattern**: wf_001 - Parallel testing workflow

EOF
```

## Troubleshooting

### Problem: Forgot to Create Snapshot Before Update

**Solution**:
```bash
# If changes not yet made, create snapshot now
timestamp=$(date -u +"%Y%m%d_%H%M%S")
cp .session_memory/active_context.md ".session_memory/active_context/context_$timestamp.md"

# If changes already made, check git
git diff .session_memory/active_context.md  # If in git
# Or check for .bak files
```

### Problem: Context Update Interrupted

**Solution**:
```bash
# Restore from latest snapshot
latest_snapshot=$(ls -t .session_memory/active_context/context_*.md | head -1)
cp "$latest_snapshot" .session_memory/active_context.md

# Resume update
```

### Problem: Multiple Updates Needed Simultaneously

**Solution**:
```bash
# Create snapshot once
timestamp=$(date -u +"%Y%m%d_%H%M%S")
cp .session_memory/active_context.md ".session_memory/active_context/context_$timestamp.md"

# Make all updates
# 1. Update focus
# 2. Record decision
# 3. Add question
# etc.

# Update timestamp once at end
```

### Problem: Pre-Compaction Validation Fails

**Solution**:
```bash
# DO NOT PROCEED with compaction
# Fix validation errors first

# Run detailed validation
./validate_all.sh

# Address each error
# Re-run validation
# Only proceed when all checks pass
```
