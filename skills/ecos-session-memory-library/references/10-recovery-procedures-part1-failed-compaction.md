# Recovery from Failed Compaction

**Parent Document**: [10-recovery-procedures.md](10-recovery-procedures.md)

## Table of Contents

1. [Scenario Description](#scenario)
2. [Symptoms to Identify](#symptoms)
3. [Recovery Procedure](#recovery-procedure)
   - [Step 1: Stop All Operations](#step-1-stop-all-operations)
   - [Step 2: Identify Last Good State](#step-2-identify-last-good-state)
   - [Step 3: Restore from Archive](#step-3-restore-from-archive)
   - [Step 4: Validate Restored State](#step-4-validate-restored-state)
   - [Step 5: Document Recovery](#step-5-document-recovery)

---

## Scenario

Compaction process failed mid-way, leaving session memory in inconsistent state.

**When this happens:**
- During automatic compaction triggered by token threshold
- During manual compaction via script
- When system interrupts compaction (crash, restart, etc.)

**Severity**: High
**Recovery Time**: 5-15 minutes
**Data Loss Risk**: Medium (changes during compaction may be lost)

## Symptoms

How to recognize a failed compaction:

- Incomplete context files (truncated content)
- Missing pattern entries (patterns recorded but not indexed)
- Inconsistent progress tracker (tasks show wrong status)
- Error messages about corrupted files
- Session info shows compaction in progress but it's not running
- Timestamps don't match (newer archive than current file)

---

## Recovery Procedure

### Step 1: Stop All Operations

Before attempting any recovery, ensure no other processes are modifying memory files.

```bash
#!/bin/bash
# stop_operations.sh - Halt any ongoing memory operations

echo "STOPPING ALL OPERATIONS"
echo "Do not make any changes until recovery completes"

# Check for running processes that might access memory
ps aux | grep -E "(compaction|snapshot|pattern)" || true
```

**What this does:**
- Announces recovery mode
- Checks for any processes that might interfere

**Expected output:**
- List of any running memory-related processes
- If processes found, wait for them to complete or terminate them

---

### Step 2: Identify Last Good State

Find the most recent valid state to restore from.

```bash
#!/bin/bash
# identify_last_good_state.sh - Find most recent valid state

echo "=== Identifying Last Good State ==="

# Check for pre-compaction archive
compaction_count=$(grep "Compaction Count:" .session_memory/session_info.md 2>/dev/null | grep -oP '\d+' || echo "0")

echo "Current compaction count: $compaction_count"

# Find pre-compaction archive
archive_dir=".session_memory/archived/pre_compaction_$compaction_count"

if [ -d "$archive_dir" ]; then
    echo "Found pre-compaction archive: $archive_dir"
    archive_time=$(cat "$archive_dir/timestamp.txt" 2>/dev/null || echo "Unknown")
    echo "  Archive timestamp: $archive_time"
else
    echo "No pre-compaction archive found"
    # Try snapshots instead
    latest_snapshot=$(ls -t .session_memory/snapshots/snapshot_*/metadata.txt 2>/dev/null | head -1)
    if [ -n "$latest_snapshot" ]; then
        snapshot_dir=$(dirname "$latest_snapshot")
        echo "Found snapshot: $snapshot_dir"
    else
        echo "No snapshots available - emergency recovery required"
        echo "See Part 3: Emergency Recovery"
        exit 1
    fi
fi
```

**What this does:**
1. Reads current compaction count from session info
2. Looks for pre-compaction archive at expected location
3. Falls back to snapshots if no archive exists
4. Reports what was found for manual decision

**Expected output:**
- Compaction count number
- Path to archive or snapshot
- Timestamp of the backup

---

### Step 3: Restore from Archive

Restore files from the pre-compaction archive.

```bash
#!/bin/bash
# restore_from_precompaction.sh - Restore from pre-compaction archive

restore_from_precompaction() {
    local compaction_count="$1"
    local archive_dir=".session_memory/archived/pre_compaction_$compaction_count"

    if [ ! -d "$archive_dir" ]; then
        echo "Archive not found: $archive_dir"
        return 1
    fi

    echo "=== Restoring from Pre-Compaction Archive ==="
    echo "Archive: $archive_dir"

    # Backup current corrupted state (might have useful data)
    backup_dir=".session_memory/corrupted_backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    cp .session_memory/*.md "$backup_dir/" 2>/dev/null || true
    echo "Corrupted state backed up to: $backup_dir"

    # Restore files from archive
    cp "$archive_dir/active_context.md" .session_memory/active_context.md
    cp "$archive_dir/progress_tracker.md" .session_memory/progress_tracker.md
    cp "$archive_dir/pattern_index.md" .session_memory/pattern_index.md

    echo "Files restored from archive"

    # Update session info with recovery event
    cat >> .session_memory/session_info.md << EOF

## Recovery Event
**Date**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Reason**: Failed compaction #$compaction_count
**Action**: Restored from pre-compaction archive
**Data Loss**: Minimal (rolled back to pre-compaction state)

EOF

    echo "Recovery complete"
}

# Usage example:
# compaction_count=3
# restore_from_precompaction "$compaction_count"
```

**What this does:**
1. Verifies archive exists
2. Backs up current (corrupted) state before overwriting
3. Copies archived files to active locations
4. Records recovery event in session info

**Important:**
- Always backup corrupted state first - it might contain useful partial data
- The corrupted backup can be reviewed later to recover any lost work

---

### Step 4: Validate Restored State

Verify the recovery was successful.

```bash
#!/bin/bash
# validate_after_recovery.sh - Verify recovery was successful

echo "=== Validating Restored State ==="

errors=0

# Check active_context.md
if [ -f ".session_memory/active_context.md" ]; then
    if grep -q "# Active Context" .session_memory/active_context.md; then
        echo "active_context.md: OK"
    else
        echo "active_context.md: INVALID (missing header)"
        errors=$((errors + 1))
    fi
else
    echo "active_context.md: MISSING"
    errors=$((errors + 1))
fi

# Check progress_tracker.md
if [ -f ".session_memory/progress_tracker.md" ]; then
    if grep -q "# Progress Tracker" .session_memory/progress_tracker.md; then
        echo "progress_tracker.md: OK"
    else
        echo "progress_tracker.md: INVALID (missing header)"
        errors=$((errors + 1))
    fi
else
    echo "progress_tracker.md: MISSING"
    errors=$((errors + 1))
fi

# Check pattern_index.md
if [ -f ".session_memory/pattern_index.md" ]; then
    if grep -q "# Pattern Index" .session_memory/pattern_index.md; then
        echo "pattern_index.md: OK"
    else
        echo "pattern_index.md: INVALID (missing header)"
        errors=$((errors + 1))
    fi
else
    echo "pattern_index.md: MISSING"
    errors=$((errors + 1))
fi

echo ""
if [ $errors -eq 0 ]; then
    echo "Validation passed - recovery successful"
    exit 0
else
    echo "Validation failed with $errors errors"
    echo "Additional recovery steps needed"
    exit 1
fi
```

**What this does:**
1. Checks each core file exists
2. Validates file has correct header
3. Reports pass/fail status

**If validation fails:**
- Check which files failed
- Try restoring from different source (older archive or snapshot)
- If no valid source, use emergency recovery (Part 3)

---

### Step 5: Document Recovery

Create a record of the recovery for future reference.

```markdown
# Recovery Log Template

**Date**: [YYYY-MM-DD HH:MM UTC]
**Incident**: Failed compaction #[N]
**Root Cause**: [To be investigated]

## Recovery Actions Taken

1. Stopped all operations
2. Identified pre-compaction archive #[N]
3. Restored from archive:
   - active_context.md
   - progress_tracker.md
   - pattern_index.md
4. Validated restored state
5. Updated session_info.md

## Data Loss Assessment

**Lost**:
- Changes made during the failed compaction
- [List any specific items if known]

**Recovered**:
- All pre-compaction state intact
- [List specific recovered items]

## Prevention Measures

- [ ] Investigate compaction failure cause
- [ ] Add more validation before compaction
- [ ] Improve compaction error handling
- [ ] Test compaction in isolated environment

## Notes

[Any additional observations or lessons learned]
```

**Where to save:**
- Add to session_info.md under a "Recovery History" section
- Optionally create `.session_memory/recovery_logs/recovery_YYYYMMDD.md`

---

## Quick Reference Checklist

```
[ ] 1. Stop all operations
[ ] 2. Identify compaction count
[ ] 3. Locate pre-compaction archive
[ ] 4. Backup corrupted state
[ ] 5. Restore from archive
[ ] 6. Validate restored files
[ ] 7. Update session_info.md
[ ] 8. Create recovery log
[ ] 9. Create new snapshot
[ ] 10. Resume normal operations
```

---

## Related Documents

- [10-recovery-procedures.md](10-recovery-procedures.md) - Main recovery index
- [Part 2: Corruption and Context](10-recovery-procedures-part2-corruption-context.md) - If files are corrupted
- [Part 3: Emergency Recovery](10-recovery-procedures-part3-snapshot-emergency.md) - If no archive available
- [Part 4a: Examples](10-recovery-procedures-part4a-examples.md) - Complete workflow examples
- [Part 4b: Troubleshooting](10-recovery-procedures-part4b-troubleshooting.md) - Common problems and solutions
