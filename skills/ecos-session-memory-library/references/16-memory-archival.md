# Memory Archival Procedures

## Table of Contents

1. [When you need to understand the overview](#overview)
2. [When to archive](#when-to-archive)
3. [What to archive](#what-to-archive)
4. [How to archive](#archival-procedures) - See [Part 1: Detailed Procedures](16-memory-archival-part1-procedures.md)
5. [Understanding archive organization](#archive-organization)
6. [For implementation examples](#examples) - See [Part 2: Examples](16-memory-archival-part2-examples.md)
7. [If issues occur](#troubleshooting) - See [Part 2: Troubleshooting](16-memory-archival-part2-examples.md#troubleshooting)

---

## Part Files

### [16-memory-archival-part1-procedures.md](16-memory-archival-part1-procedures.md)

Detailed step-by-step procedures for memory archival:

- PROCEDURE 1: Archive Completed Tasks
  - When completed tasks section has > 50 tasks
  - When oldest completed task is > 30 days old
  - When progress.md file size exceeds 200KB
- PROCEDURE 2: Archive Old Patterns
  - When patterns.md exceeds 150KB
  - When many patterns are no longer referenced
  - When patterns from old project phases exist
- PROCEDURE 3: Consolidate Active Context
  - When activeContext.md exceeds 100KB
  - When many old decisions accumulated
  - When file navigation history is very long
- PROCEDURE 4: Create Archival Snapshot
  - Before major project milestone
  - Before long project hiatus
  - Before major memory restructuring
- PROCEDURE 5: Restore from Archive
  - When you need to review old decisions
  - When you need to understand past patterns
  - When recovering from data loss

### [16-memory-archival-part2-examples.md](16-memory-archival-part2-examples.md)

Practical examples and troubleshooting:

- Example 1: Archiving Old Completed Tasks
- Example 2: Creating Milestone Snapshot
- Troubleshooting: Archive file corrupted
- Troubleshooting: Too much data archived, need to recover

---

## Overview

### What Is Memory Archival?

Memory archival is the process of moving completed, outdated, or no-longer-active session memory content to separate archive files. This keeps the active memory files (activeContext.md, patterns.md, progress.md) lean and fast-loading while preserving historical information for future reference.

### Why Archive?

**Without archival:**
- Memory files grow to hundreds of kilobytes
- Session initialization becomes slow
- Finding current information is difficult
- Memory operations are sluggish
- Historical data is lost when files are cleaned

**With archival:**
- Active memory stays under 50KB per file
- Fast session initialization
- Current information is easy to find
- Historical data is preserved
- Can review past decisions and patterns

---

## When to Archive

### Trigger 1: File Size Threshold

**Archive when:**
- activeContext.md exceeds 100KB
- patterns.md exceeds 150KB
- progress.md exceeds 200KB

**How to check:**
```bash
du -k design/memory/*.md | while read size file; do
  if [ $size -gt 100 ]; then
    echo "Archive needed: $file is ${size}KB"
  fi
done
```

---

### Trigger 2: Completed Task Accumulation

**Archive when:**
- More than 50 tasks in Completed Tasks section
- Completed tasks are older than 30 days
- Completed tasks section is longer than Todo List section

**How to check:**
```bash
completed_count=$(grep -c "^- \[x\]" design/memory/progress.md)
if [ $completed_count -gt 50 ]; then
  echo "Archive needed: $completed_count completed tasks"
fi
```

---

### Trigger 3: Pattern Obsolescence

**Archive when:**
- Patterns are no longer relevant to current work
- Patterns are over 90 days old
- Patterns contradict newer patterns

**How to check:**
```python
from datetime import datetime, timedelta

patterns = extract_patterns(patterns_md)
now = datetime.now()

for pattern in patterns:
    age = now - datetime.fromisoformat(pattern.discovered_at)
    if age > timedelta(days=90):
        print(f"Archive candidate: {pattern.name} (age: {age.days} days)")
```

---

### Trigger 4: Session Milestone

**Archive when:**
- Major project milestone reached
- Before starting new major feature
- After project phase completion
- Before long project hiatus

---

### Trigger 5: Performance Degradation

**Archive when:**
- Session initialization takes > 5 seconds
- Memory updates take > 2 seconds
- File operations are noticeably slow

---

## What to Archive

### Archive Candidates from progress.md

**Archive:**
- Completed tasks older than 30 days
- Cancelled tasks older than 14 days
- Tasks from completed milestones
- Historical task metadata

**Keep:**
- Active tasks (pending, in progress, blocked)
- Recently completed tasks (last 30 days)
- Tasks needed for dependency tracking
- Current milestone tasks

---

### Archive Candidates from patterns.md

**Archive:**
- Patterns not referenced in last 60 days
- Patterns superseded by newer patterns
- Patterns from completed project phases
- Deprecated patterns

**Keep:**
- Actively used patterns
- Recent patterns (last 60 days)
- Patterns referenced by current work
- Core architectural patterns

---

### Archive Candidates from activeContext.md

**Archive:**
- Decisions older than 60 days
- Historical context no longer relevant
- Old file navigation history
- Superseded decisions

**Keep:**
- Current task information
- Recent decisions (last 60 days)
- Active context needed for current work
- Recent file history

---

## Archival Procedures

For detailed step-by-step procedures, see **[16-memory-archival-part1-procedures.md](16-memory-archival-part1-procedures.md)**.

Quick reference:

| Procedure | When to Use | Target File |
|-----------|-------------|-------------|
| Archive Completed Tasks | > 50 completed tasks or > 30 days old | progress.md |
| Archive Old Patterns | > 150KB or unused patterns | patterns.md |
| Consolidate Active Context | > 100KB or old decisions | activeContext.md |
| Create Archival Snapshot | Milestone or hiatus | All memory files |
| Restore from Archive | Need historical data | Archive files |

---

## Archive Organization

### Directory Structure

```
design/memory/
├── activeContext.md
├── patterns.md
├── progress.md
├── config-snapshot.md
├── archive/
│   ├── 2024/
│   │   ├── completed-tasks-202412.md
│   │   ├── patterns-202412.md
│   │   └── decisions-202412.md
│   └── 2025/
│       ├── completed-tasks-202501.md
│       ├── completed-tasks-202502.md
│       ├── patterns-202501.md
│       └── decisions-202501.md
└── snapshots/
    ├── 20241215-143000.tar.gz
    ├── 20250101-090000.tar.gz
    └── 20250115-153000.tar.gz
```

### Naming Conventions

**Archive files:**
- `completed-tasks-YYYYMM.md` - Archived completed tasks
- `patterns-YYYYMM.md` - Archived patterns
- `decisions-YYYYMM.md` - Archived decisions

**Snapshot files:**
- `YYYYMMDD-HHMMSS.tar.gz` - Complete memory snapshot
- `YYYYMMDD-HHMMSS/` - Extracted snapshot directory

---

## Examples

For detailed examples, see **[16-memory-archival-part2-examples.md](16-memory-archival-part2-examples.md)**.

---

## Troubleshooting

For troubleshooting guide, see **[16-memory-archival-part2-examples.md](16-memory-archival-part2-examples.md#troubleshooting)**.

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Target Audience:** Chief of Staff Agents
**Related:** SKILL.md (Troubleshooting - Memory files grow too large)
