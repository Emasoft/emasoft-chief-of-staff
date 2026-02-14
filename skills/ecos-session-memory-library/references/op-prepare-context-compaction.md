---
procedure: support-skill
workflow-instruction: support
operation: prepare-context-compaction
parent-skill: ecos-session-memory-library
---

# Operation: Prepare for Context Compaction


## Contents

- [Purpose](#purpose)
- [When To Use This Operation](#when-to-use-this-operation)
- [Context Compaction Risks](#context-compaction-risks)
- [Steps](#steps)
  - [Step 1: Check Context Usage](#step-1-check-context-usage)
  - [Step 2: Update All Memory Files](#step-2-update-all-memory-files)
  - [Step 3: Run Validation](#step-3-run-validation)
  - [Step 4: Write to Disk](#step-4-write-to-disk)
  - [Step 5: Create Backup (Optional)](#step-5-create-backup-optional)
  - [Step 6: Confirm Ready](#step-6-confirm-ready)
- [Pre-Compaction Checklist Complete](#pre-compaction-checklist-complete)
- [Pre-Compaction Checklist](#pre-compaction-checklist)
  - [Preparation Phase](#preparation-phase)
  - [Update Phase](#update-phase)
  - [Backup Phase](#backup-phase)
  - [Validation Phase](#validation-phase)
  - [Final Phase](#final-phase)
- [Output](#output)
- [After Compaction](#after-compaction)
- [Related References](#related-references)
- [Next Operation](#next-operation)

## Purpose

Ensure all session memory is fully updated and persisted before context compaction to survive the operation.

## When To Use This Operation

- When context usage exceeds 70%
- Before long-running operations
- Proactively before intensive work
- When system warns of approaching limit

## Context Compaction Risks

| Risk | Impact | Prevention |
|------|--------|------------|
| Unsaved changes | Work lost | Write immediately |
| Stale context | Resume with old state | Update before compaction |
| Corrupted files | Recovery needed | Validate before compaction |

## Steps

### Step 1: Check Context Usage

```bash
# If context monitoring available, check percentage
echo "Current context usage: [percentage]%"
```

If above 70%, proceed with preparation.

### Step 2: Update All Memory Files

Ensure all three files are current:

**activeContext.md:**
- Current Focus is accurate
- Open Questions are listed
- Recent Decisions documented
- Session Notes captured

**patterns.md:**
- Any new patterns recorded
- Index is current

**progress.md:**
- Task statuses accurate
- Blockers documented
- Dependencies current

### Step 3: Run Validation

```bash
MEMORY_DIR="$CLAUDE_PROJECT_DIR/design/memory"

# Check file integrity
for file in activeContext.md patterns.md progress.md; do
  if [ -f "$MEMORY_DIR/$file" ]; then
    echo "$file: EXISTS"
    # Check not empty
    if [ -s "$MEMORY_DIR/$file" ]; then
      echo "$file: NOT EMPTY"
    else
      echo "$file: WARNING - EMPTY"
    fi
  else
    echo "$file: MISSING"
  fi
done
```

### Step 4: Write to Disk

Force write all files:

```bash
# Sync filesystem
sync

# Verify files written
ls -la "$MEMORY_DIR"/*.md
```

### Step 5: Create Backup (Optional)

```bash
BACKUP_DIR="$MEMORY_DIR/backups/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp "$MEMORY_DIR"/*.md "$BACKUP_DIR/"
echo "Backup created: $BACKUP_DIR"
```

### Step 6: Confirm Ready

```markdown
## Pre-Compaction Checklist Complete

- [x] activeContext.md updated and saved
- [x] patterns.md updated and saved
- [x] progress.md updated and saved
- [x] Files validated
- [x] Filesystem synced
- [x] Backup created (optional)

**Ready for context compaction.**

After compaction, run session recovery to resume.
```

## Pre-Compaction Checklist

Copy this checklist and track your progress:

### Preparation Phase
- [ ] Context usage checked
- [ ] Decision to compact confirmed

### Update Phase
- [ ] activeContext.md current
- [ ] patterns.md current
- [ ] progress.md current
- [ ] All timestamps updated

### Backup Phase
- [ ] Backup directory created
- [ ] Files copied to backup

### Validation Phase
- [ ] Files exist
- [ ] Files not empty
- [ ] No syntax errors
- [ ] Cross-references valid

### Final Phase
- [ ] Filesystem synced
- [ ] Ready for compaction

## Output

After completing this operation:
- All memory files fully updated
- Files validated and persisted
- Backup created (optional)
- Safe to proceed with compaction

## After Compaction

After context compaction completes:
1. Run [op-recover-session.md](op-recover-session.md)
2. Load memory files
3. Resume work

## Related References

- [11-compaction-safety.md](11-compaction-safety.md) - Compaction safety guide
- [12-pre-compaction-checklist.md](12-pre-compaction-checklist.md) - Detailed checklist
- [10-recovery-procedures.md](10-recovery-procedures.md) - Post-compaction recovery

## Next Operation

After compaction: [op-recover-session.md](op-recover-session.md)
