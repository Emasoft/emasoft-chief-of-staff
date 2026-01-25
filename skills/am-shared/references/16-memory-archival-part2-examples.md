# Memory Archival - Examples and Troubleshooting

**Parent Document:** [16-memory-archival.md](16-memory-archival.md)

---

## Table of Contents

1. [Example 1: Archiving Old Completed Tasks](#example-1-archiving-old-completed-tasks)
2. [Example 2: Creating Milestone Snapshot](#example-2-creating-milestone-snapshot)
3. [Troubleshooting](#troubleshooting)
   - [Issue: Archive file corrupted](#issue-archive-file-corrupted)
   - [Issue: Too much data archived, need to recover](#issue-too-much-data-archived-need-to-recover)

---

## Example 1: Archiving Old Completed Tasks

**Before archival:**
```bash
$ du -h .atlas/memory/progress.md
245K    .atlas/memory/progress.md

$ grep -c "^- \[x\]" .atlas/memory/progress.md
78
```

**Run archival:**
```bash
$ python scripts/archive-memory.py --type completed-tasks --cutoff-days 30

Analyzing completed tasks...
Found 78 completed tasks
45 tasks are older than 30 days
Creating archive: .atlas/memory/archive/2025/completed-tasks-202512.md
Writing 45 tasks to archive...
Removing archived tasks from progress.md...
Done.

Archived: 45 tasks
Remaining: 33 tasks
Space saved: 123KB
```

**After archival:**
```bash
$ du -h .atlas/memory/progress.md
122K    .atlas/memory/progress.md

$ grep -c "^- \[x\]" .atlas/memory/progress.md
33

$ ls -lh .atlas/memory/archive/2025/completed-tasks-202512.md
-rw-r--r--  1 user  staff   98K Dec 31 16:30 completed-tasks-202512.md
```

---

## Example 2: Creating Milestone Snapshot

**Scenario:** Completing major project phase

**Create snapshot:**
```bash
$ python scripts/snapshot-memory.py --reason "Phase 1 completion"

Creating snapshot...
Snapshot directory: .atlas/memory/snapshots/20251231-163000
Copying activeContext.md... Done
Copying patterns.md... Done
Copying progress.md... Done
Creating metadata... Done
Creating compressed archive... Done

Snapshot created: 20251231-163000.tar.gz (156KB)
```

**Snapshot contents:**
```bash
$ tar tzf .atlas/memory/snapshots/20251231-163000.tar.gz
20251231-163000/
20251231-163000/activeContext.md
20251231-163000/patterns.md
20251231-163000/progress.md
20251231-163000/SNAPSHOT_INFO.md
```

---

## Troubleshooting

### Issue: Archive file corrupted

**Symptoms:**
- Cannot read archive file
- Invalid format errors

**Solution:**
1. Check if compressed snapshot exists
2. Restore from snapshot instead
3. If no snapshot, archive is lost
4. Implement regular snapshot creation

---

### Issue: Too much data archived, need to recover

**Symptoms:**
- Archived task is needed for current work
- Current memory missing important information

**Solution:**
1. Find relevant archive file
2. Extract needed information
3. Copy to current memory file
4. Do not restore entire archive
5. Only restore specific needed items

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Parent:** [16-memory-archival.md](16-memory-archival.md)
