# Pre-Compaction Master Checklist Template

This file contains the complete master checklist template for pre-compaction validation.

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

## How to Use This Checklist

1. **Copy the template** to a working document before each compaction
2. **Fill in header fields** (compaction number, date, reason)
3. **Work through each phase** sequentially
4. **Check off items** as they are completed
5. **Document any issues** in the notes section
6. **Make final go/no-go decision** based on criteria
7. **Archive the completed checklist** with the compaction record
