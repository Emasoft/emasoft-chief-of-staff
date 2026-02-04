# Recovery from Snapshot Failure and Emergency Recovery

**Parent Document**: [10-recovery-procedures.md](10-recovery-procedures.md)

## Table of Contents

1. [Recovery from Snapshot Failure](#recovery-from-snapshot-failure)
   - [Scenario](#snapshot-scenario)
   - [Symptoms](#snapshot-symptoms)
   - [Recovery Procedure](#snapshot-recovery-procedure)
2. [Emergency Recovery](#emergency-recovery)
   - [Scenario](#emergency-scenario)
   - [Recovery Procedure](#emergency-recovery-procedure)

---

## Recovery from Snapshot Failure

### Snapshot Scenario

Unable to create snapshots (disk full, permission errors, etc.).

**When this happens:**
- Disk space exhausted
- Permission errors on snapshot directory
- Snapshots directory missing or corrupted
- File system errors

**Severity**: Low (current data intact, just can't backup)
**Recovery Time**: 1-2 minutes
**Data Loss Risk**: Low (no data lost yet, but vulnerable)

### Snapshot Symptoms

How to recognize snapshot failure:

- Snapshot creation fails with error
- Error messages about disk space
- Permission denied errors
- Snapshots directory missing or inaccessible
- No new snapshots appearing

### Snapshot Recovery Procedure

```bash
#!/bin/bash
# recover_snapshot_capability.sh - Restore ability to create snapshots

recover_snapshot_capability() {
    echo "=== Recovering Snapshot Capability ==="

    # Check 1: Disk space
    echo "Check 1: Disk space..."
    df -h . | tail -1
    available=$(df . | tail -1 | awk '{print $4}')
    if [ "$available" -lt 10000 ]; then
        echo "WARNING: Low disk space: ${available}KB available"
        echo "  Consider cleaning up old snapshots or archives"
        cleanup_old_snapshots
    else
        echo "OK: Sufficient disk space"
    fi

    # Check 2: Permissions
    echo ""
    echo "Check 2: Permissions..."
    if [ ! -w ".session_memory/snapshots" ]; then
        echo "ERROR: Snapshots directory not writable"
        echo "  Fixing permissions..."
        chmod u+w .session_memory/snapshots
        echo "OK: Permissions fixed"
    else
        echo "OK: Permissions are correct"
    fi

    # Check 3: Directory exists
    echo ""
    echo "Check 3: Directory structure..."
    if [ ! -d ".session_memory/snapshots" ]; then
        echo "ERROR: Snapshots directory missing"
        echo "  Creating directory..."
        mkdir -p .session_memory/snapshots
        echo "OK: Directory created"
    else
        echo "OK: Directory exists"
    fi

    # Check 4: Test snapshot creation
    echo ""
    echo "Check 4: Testing snapshot creation..."
    test_snapshot_dir=".session_memory/snapshots/test_$(date +%Y%m%d_%H%M%S)"
    if mkdir "$test_snapshot_dir" 2>/dev/null; then
        rm -rf "$test_snapshot_dir"
        echo "OK: Snapshot creation works"
    else
        echo "ERROR: Cannot create snapshot directory"
        echo "  Check file system errors"
        return 1
    fi

    echo ""
    echo "Snapshot capability restored"
}

cleanup_old_snapshots() {
    echo "Cleaning up old snapshots..."

    # Keep only last 10 snapshots
    snapshots=$(ls -dt .session_memory/snapshots/snapshot_* 2>/dev/null)
    count=0
    for snapshot in $snapshots; do
        count=$((count + 1))
        if [ $count -gt 10 ]; then
            echo "  Removing old snapshot: $snapshot"
            rm -rf "$snapshot"
        fi
    done

    # Clean up old archives
    archives=$(ls -dt .session_memory/archived/pre_compaction_* 2>/dev/null)
    count=0
    for archive in $archives; do
        count=$((count + 1))
        if [ $count -gt 5 ]; then
            echo "  Removing old archive: $archive"
            rm -rf "$archive"
        fi
    done

    echo "Cleanup complete"
}

recover_snapshot_capability
```

**What this does:**
1. Checks available disk space
2. Verifies and fixes directory permissions
3. Creates missing directories
4. Tests snapshot creation capability
5. Optionally cleans up old snapshots/archives

---

## Emergency Recovery

### Emergency Scenario

Complete memory loss - all session memory deleted or severely corrupted.

**When this happens:**
- Entire .session_memory directory deleted
- All files corrupted beyond recovery
- No snapshots or archives available
- Fresh start required

**Severity**: Critical
**Recovery Time**: 15-30 minutes
**Data Loss Risk**: High (historical context lost)

### Emergency Recovery Procedure

```bash
#!/bin/bash
# emergency_recovery.sh - Rebuild session memory from scratch

emergency_recovery() {
    echo "=== EMERGENCY RECOVERY ==="
    echo "WARNING: Complete memory rebuild required"
    echo ""

    # Step 1: Reinitialize structure
    echo "Step 1: Reinitializing directory structure..."

    # Create base directories
    mkdir -p .session_memory/{patterns,snapshots,archived,active_context,progress}
    mkdir -p .session_memory/patterns/{decision,problem,solution,workflow}

    echo "OK: Directory structure created"

    # Step 2: Recover from git (if available)
    echo ""
    echo "Step 2: Recovering from git history..."
    if git rev-parse --git-dir > /dev/null 2>&1; then
        # Mine commit messages for context
        echo "Recent commits (for context reconstruction):"
        git log --oneline -20

        # Check for any session memory backups in git
        echo ""
        echo "Session memory files in git history:"
        git log --all --full-history --pretty=format: --name-only -- .session_memory/ | \
        sort -u | head -20
    else
        echo "No git repository found"
    fi

    # Step 3: Recover from documentation
    echo ""
    echo "Step 3: Recovering from documentation..."
    if [ -d "docs" ] || [ -d "docs_dev" ]; then
        echo "Documentation files found:"
        find docs docs_dev -name "*.md" -type f 2>/dev/null | head -10
    fi

    # Step 4: Create minimal recovery context
    echo ""
    echo "Step 4: Creating minimal recovery context..."

    create_emergency_active_context
    create_emergency_progress_tracker
    create_emergency_session_info
    create_emergency_pattern_index

    # Step 5: Report
    echo ""
    echo "=== Emergency Recovery Complete ==="
    echo ""
    echo "OK: Directory structure recreated"
    echo "OK: Minimal files created"
    echo ""
    echo "MANUAL ACTIONS REQUIRED:"
    echo "1. Review git history for recent work"
    echo "2. Review documentation for project state"
    echo "3. Update active context with current focus"
    echo "4. Recreate progress tracker from memory"
    echo "5. Document what was lost"
    echo ""
    echo "WARNING: Some historical context may be permanently lost"
}

create_emergency_active_context() {
    cat > .session_memory/active_context.md << 'EOF'
# Active Context

**Status**: EMERGENCY RECOVERY MODE
**Recovery Date**: [AUTO-FILLED ON CREATION]

## Current Focus

**RECONSTRUCTION REQUIRED**

Action items:
1. Review recent git commits for context
2. Check documentation for current project state
3. Review progress tracker (if any backup exists)
4. Reconstruct open questions from memory
5. Update this context with current state

## Recent Decisions

[Mine from git commit messages and documentation]

## Open Questions

[Reconstruct from memory or ask user]

## Recovery Notes

- Session memory was completely lost
- Rebuilding from available sources
- Some historical context may be permanently lost
- Manual review and update required

EOF
    # Update the date
    sed -i '' "s/\[AUTO-FILLED ON CREATION\]/$(date -u +"%Y-%m-%d %H:%M:%S UTC")/" \
        .session_memory/active_context.md 2>/dev/null || true
    echo "  Created: active_context.md"
}

create_emergency_progress_tracker() {
    cat > .session_memory/progress_tracker.md << 'EOF'
# Progress Tracker

**Status**: EMERGENCY RECOVERY MODE
**Recovery Date**: [AUTO-FILLED ON CREATION]

## Active Tasks

[Reconstruct from git commits, documentation, or memory]

| Task | Status | Priority | Notes |
|------|--------|----------|-------|
| Reconstruct context | In Progress | High | Emergency recovery |

## Completed Tasks

[Cannot recover - historical data lost]

## Blocked Tasks

[Review and reconstruct from memory]

## Notes

This progress tracker was recreated after emergency recovery.
Historical task data has been lost. Reconstruct current tasks
from available sources.

EOF
    sed -i '' "s/\[AUTO-FILLED ON CREATION\]/$(date -u +"%Y-%m-%d %H:%M:%S UTC")/" \
        .session_memory/progress_tracker.md 2>/dev/null || true
    echo "  Created: progress_tracker.md"
}

create_emergency_session_info() {
    cat > .session_memory/session_info.md << 'EOF'
# Session Info

**Status**: EMERGENCY RECOVERY
**Recovery Date**: [AUTO-FILLED ON CREATION]
**Compaction Count**: 0
**Session Start**: [UNKNOWN - data lost]

## Emergency Recovery Event

- Complete session memory loss occurred
- All historical data lost
- Rebuilt from scratch
- Manual reconstruction required

## Recovery Actions Taken

1. Recreated directory structure
2. Created minimal active_context.md
3. Created minimal progress_tracker.md
4. Created minimal pattern_index.md
5. Created this session_info.md

## Data Loss

- All historical context lost
- All recorded patterns lost
- All snapshots lost
- All archives lost

## Next Steps

- Reconstruct current state from memory
- Review git history for recent work
- Review documentation for context
- Document what was lost

EOF
    sed -i '' "s/\[AUTO-FILLED ON CREATION\]/$(date -u +"%Y-%m-%d %H:%M:%S UTC")/" \
        .session_memory/session_info.md 2>/dev/null || true
    echo "  Created: session_info.md"
}

create_emergency_pattern_index() {
    cat > .session_memory/pattern_index.md << 'EOF'
# Pattern Index

**Status**: EMERGENCY RECOVERY MODE
**Recovery Date**: [AUTO-FILLED ON CREATION]

## Patterns by Category

### decision

[No patterns - data lost]

### problem

[No patterns - data lost]

### solution

[No patterns - data lost]

### workflow

[No patterns - data lost]

## Notes

Pattern index recreated after emergency recovery.
All historical patterns have been lost.
New patterns will be recorded as they are discovered.

EOF
    sed -i '' "s/\[AUTO-FILLED ON CREATION\]/$(date -u +"%Y-%m-%d %H:%M:%S UTC")/" \
        .session_memory/pattern_index.md 2>/dev/null || true
    echo "  Created: pattern_index.md"
}

emergency_recovery
```

---

## Post-Emergency Actions

After emergency recovery completes:

### 1. Immediate Snapshot

```bash
# Create snapshot of recovered state
mkdir -p ".session_memory/snapshots/snapshot_recovered_$(date +%Y%m%d_%H%M%S)"
cp .session_memory/*.md ".session_memory/snapshots/snapshot_recovered_$(date +%Y%m%d_%H%M%S)/"
```

### 2. Context Reconstruction Checklist

```markdown
## Context Reconstruction

- [ ] Review last 20 git commits
- [ ] Extract task information from commit messages
- [ ] Review TODO.md if exists
- [ ] Review docs/docs_dev for current state
- [ ] Ask user for current focus
- [ ] Document what was lost
- [ ] Update active_context.md
- [ ] Update progress_tracker.md
```

### 3. Prevention Measures

```markdown
## Prevent Future Emergency

- [ ] Set up regular snapshot schedule
- [ ] Add session memory to git tracking
- [ ] Create external backup location
- [ ] Monitor disk space
- [ ] Test recovery procedures periodically
```

---

## Quick Reference Checklist

### For Snapshot Failure:

```
[ ] 1. Check disk space
[ ] 2. Check permissions
[ ] 3. Verify directory exists
[ ] 4. Clean up old snapshots if needed
[ ] 5. Test snapshot creation
[ ] 6. Document fix
```

### For Emergency Recovery:

```
[ ] 1. Create directory structure
[ ] 2. Check git history
[ ] 3. Check documentation
[ ] 4. Create minimal files
[ ] 5. Create immediate snapshot
[ ] 6. Reconstruct context
[ ] 7. Update progress tracker
[ ] 8. Document data loss
[ ] 9. Implement prevention measures
```

---

## Related Documents

- [10-recovery-procedures.md](10-recovery-procedures.md) - Main recovery index
- [Part 1: Failed Compaction](10-recovery-procedures-part1-failed-compaction.md) - Compaction recovery
- [Part 2: Corruption and Context](10-recovery-procedures-part2-corruption-context.md) - File corruption
- [Part 4a: Examples](10-recovery-procedures-part4a-examples.md) - Complete workflow examples
- [Part 4b: Troubleshooting](10-recovery-procedures-part4b-troubleshooting.md) - Common problems and solutions
