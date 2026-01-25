# Pre-Compaction Checklist - Part 1: Preparation and Backup

## Table of Contents
1. [Purpose of the pre-compaction checklist](#purpose)
2. [Using the master checklist](#master-checklist)
3. [Completing preparation phase](#preparation-phase)
   - 3.1 [Context preparation steps](#step-1-context-preparation)
   - 3.2 [Pattern extraction before compaction](#step-2-pattern-extraction)
   - 3.3 [Progress review before compaction](#step-3-progress-review)
4. [Completing backup phase](#backup-phase)
   - 4.1 [Creating all required backups](#backup-creation-script)

**See also**: [Part 2: Validation and Decision](12-pre-compaction-checklist-part2-validation-decision.md) for validation phase, final verification, go/no-go decision, and examples.

---

## Purpose

The pre-compaction checklist ensures all safety measures are in place before compaction. Following this checklist:
- Prevents data loss
- Enables recovery if compaction fails
- Validates readiness
- Documents pre-compaction state
- Provides go/no-go decision criteria

## Master Checklist

```markdown
# Pre-Compaction Master Checklist

**Compaction Number**: ___
**Date**: _______________
**Initiated By**: Orchestrator
**Reason**: Context size / User request / Scheduled

---

## PREPARATION PHASE

### Context Preparation
- [ ] Current focus documented
- [ ] All important decisions recorded
- [ ] Open questions documented
- [ ] No critical work in progress

### Pattern Extraction
- [ ] Reusable patterns identified
- [ ] Patterns extracted to pattern files
- [ ] Pattern index updated
- [ ] No valuable patterns left in context

### Progress Review
- [ ] Active tasks documented
- [ ] Completed tasks recorded
- [ ] Blocked tasks identified
- [ ] Dependencies mapped

### Git Status (if applicable)
- [ ] Recent work committed
- [ ] Working directory clean
- [ ] Branch status noted
- [ ] No uncommitted critical changes

---

## BACKUP PHASE

### Context Snapshot
- [ ] Context snapshot created
- [ ] Snapshot timestamp: _______________
- [ ] Snapshot location: _______________
- [ ] Snapshot file readable

### Progress Snapshot
- [ ] Progress snapshot created
- [ ] Snapshot timestamp: _______________
- [ ] Snapshot location: _______________
- [ ] Snapshot file readable

### Full Session Snapshot
- [ ] Snapshot directory created
- [ ] context.md copied
- [ ] progress.md copied
- [ ] patterns.md copied
- [ ] metadata.txt created
- [ ] Latest symlink updated

### Pre-Compaction Archive
- [ ] Archive directory created: pre_compaction_[N]
- [ ] active_context.md archived
- [ ] progress_tracker.md archived
- [ ] pattern_index.md archived
- [ ] timestamp.txt created
- [ ] Archive index updated

---

## VALIDATION PHASE

### Structure Validation
- [ ] .session_memory directory exists
- [ ] All required subdirectories present
- [ ] All required files exist
- [ ] Pattern categories complete
- [ ] No broken symlinks
- [ ] Permissions correct

### Content Validation
- [ ] active_context.md valid markdown
- [ ] progress_tracker.md valid markdown
- [ ] pattern_index.md valid markdown
- [ ] All required sections present
- [ ] No corrupted files

### Consistency Validation
- [ ] Pattern index matches files
- [ ] No orphaned patterns
- [ ] Snapshots complete
- [ ] Timestamps consistent
- [ ] No contradictions

### Recovery Validation
- [ ] Recent snapshot exists
- [ ] Snapshot is complete
- [ ] Archive exists
- [ ] Test restoration succeeds
- [ ] Validation scripts run successfully

---

## FINAL VERIFICATION

### System Checks
- [ ] Sufficient disk space (>100MB free)
- [ ] No running compaction processes
- [ ] No file system errors
- [ ] Memory structure intact

### Restoration Test
- [ ] Test directory created
- [ ] Files copied to test directory
- [ ] Files readable in test directory
- [ ] Test directory cleaned up
- [ ] Restoration capability confirmed

### Metadata Update
- [ ] Compaction count identified: ___
- [ ] Next compaction number: ___
- [ ] session_info.md prepared for update
- [ ] Compaction record ready

---

## GO/NO-GO DECISION

### Critical Criteria (ALL must be YES)
- [ ] All backups created successfully
- [ ] All validation checks passed
- [ ] Restoration test successful
- [ ] No data integrity issues

### Warning Conditions (Review required)
- [ ] Low disk space (but sufficient)
- [ ] Old snapshots need cleanup
- [ ] Git uncommitted changes (non-critical)
- [ ] Pattern index warnings

### No-Go Conditions (STOP if ANY)
- [ ] Any backup creation failed
- [ ] Any validation failed
- [ ] Restoration test failed
- [ ] Corrupted files detected
- [ ] Insufficient disk space
- [ ] Critical work in progress

---

## DECISION

**GO** / **NO-GO**: __________

**If NO-GO**:
Reason: _______________________________________________
Action Required: ______________________________________

**If GO**:
Approved By: Orchestrator
Timestamp: _______________
Proceed to Compaction: YES

---

## SIGNATURES

**Checklist Completed By**: Orchestrator
**Date**: _______________
**Time**: _______________

**Notes**: _______________________________________________
```

## Preparation Phase

### Step 1: Context Preparation

```bash
#!/bin/bash
# prepare_context.sh - Prepare context for compaction

prepare_context() {
    echo "=== Context Preparation ==="
    echo ""

    # Check current focus is documented
    echo "Check: Current focus documented..."
    if grep -q "^## Current Focus" .session_memory/active_context.md && \
       ! grep -A 5 "^## Current Focus" .session_memory/active_context.md | grep -q "\[To be filled\]"; then
        echo "✓ Current focus documented"
    else
        echo "✗ Current focus needs update"
        return 1
    fi

    # Check decisions recorded
    echo ""
    echo "Check: Recent decisions recorded..."
    if grep -q "^## Recent Decisions" .session_memory/active_context.md; then
        decision_count=$(grep "^### Decision:" .session_memory/active_context.md | wc -l)
        echo "✓ $decision_count decision(s) recorded"
    else
        echo "⚠ No decisions section found"
    fi

    # Check open questions
    echo ""
    echo "Check: Open questions documented..."
    if grep -q "^## Open Questions" .session_memory/active_context.md; then
        question_count=$(grep "^### Q:" .session_memory/active_context.md | wc -l)
        echo "✓ $question_count open question(s) documented"
    else
        echo "⚠ No open questions section found"
    fi

    echo ""
    echo "✓ Context preparation check complete"
}

prepare_context
```

### Step 2: Pattern Extraction

```bash
#!/bin/bash
# extract_patterns.sh - Extract patterns before compaction

extract_patterns() {
    echo "=== Pattern Extraction ==="
    echo ""

    # Review context for patterns
    echo "Review context for extractable patterns..."
    echo ""
    echo "Look for:"
    echo "1. Problems solved (Problem-Solution patterns)"
    echo "2. Effective procedures (Workflow patterns)"
    echo "3. Important decisions (Decision-Logic patterns)"
    echo "4. Error recoveries (Error-Recovery patterns)"
    echo ""

    # Count existing patterns
    pattern_count=$(find .session_memory/patterns -name "*.md" -type f | wc -l)
    echo "Current pattern count: $pattern_count"
    echo ""

    # Prompt for pattern extraction
    echo "Manual review required:"
    echo "1. Read through active_context.md"
    echo "2. Identify reusable knowledge"
    echo "3. Create pattern files for each"
    echo "4. Update pattern index"
    echo ""

    read -p "Patterns extracted and index updated? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "✓ Pattern extraction complete"
        return 0
    else
        echo "✗ Pattern extraction incomplete"
        return 1
    fi
}

extract_patterns
```

### Step 3: Progress Review

```bash
#!/bin/bash
# review_progress.sh - Review progress before compaction

review_progress() {
    echo "=== Progress Review ==="
    echo ""

    # Count tasks by status
    active=$(grep -c "^- \[ \].*In progress" .session_memory/progress_tracker.md 2>/dev/null || echo "0")
    completed=$(grep -c "^- \[x\]" .session_memory/progress_tracker.md 2>/dev/null || echo "0")
    blocked=$(grep -c "^- \[ \].*Blocked" .session_memory/progress_tracker.md 2>/dev/null || echo "0")

    echo "Active tasks: $active"
    echo "Completed tasks: $completed"
    echo "Blocked tasks: $blocked"
    echo ""

    # Check for critical work
    if [ "$active" -gt 0 ]; then
        echo "⚠ WARNING: $active active task(s)"
        echo "  Review active tasks before compaction"
        grep "^- \[ \]" .session_memory/progress_tracker.md | head -5
        echo ""
        read -p "Safe to proceed with active tasks? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return 1
        fi
    fi

    echo "✓ Progress review complete"
}

review_progress
```

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

**Next**: See [Part 2: Validation and Decision](12-pre-compaction-checklist-part2-validation-decision.md) for validation phase, final verification, go/no-go decision criteria, and complete examples.
