# Using Memory Scripts: Load, Save, Archive, and Repair

## Table of Contents

1. [load-memory.py](#load-memorypy)
2. [save-memory.py](#save-memorypy)
3. [archive-memory.py](#archive-memorypy)
4. [repair-memory.py](#repair-memorypy)

---

## load-memory.py

**Purpose:** Load session memory into agent state.

**Usage:**
```bash
python scripts/load-memory.py [OPTIONS]
```

**Options:**
- `--directory DIR` - Memory directory to load
- `--format FORMAT` - Output format (json, python, text)
- `--output FILE` - Write loaded state to file

**Examples:**

**Example 1: Load and display**
```bash
python scripts/load-memory.py
```

Output:
```
Loading session memory from .atlas/memory

Loaded state:
  Current Task: Implement authorization middleware
  Current File: src/auth/middleware.py (line 45)
  Total Tasks: 25
  Completed: 12 (48%)
  Active Patterns: 8

Session state ready.
```

**Example 2: Load to JSON file**
```bash
python scripts/load-memory.py --format json --output /tmp/state.json
```

Output file `/tmp/state.json`:
```json
{
  "current_task": "Implement authorization middleware",
  "current_file": "src/auth/middleware.py",
  "current_line": 45,
  "tasks": {
    "total": 25,
    "completed": 12,
    "pending": 11,
    "blocked": 2
  },
  "patterns": 8
}
```

**When to use:**
- Session initialization
- After context compaction
- Resuming interrupted work

---

## save-memory.py

**Purpose:** Save current session state to memory files.

**Usage:**
```bash
python scripts/save-memory.py [OPTIONS]
```

**Options:**
- `--directory DIR` - Memory directory
- `--state FILE` - JSON file with session state
- `--backup` - Create backup before saving

**Examples:**

**Example 1: Save from current state**
```bash
python scripts/save-memory.py --backup
```

Output:
```
Creating backup... Done (backup.20251231-180000)
Saving session state to .atlas/memory

Updating activeContext.md... Done
Updating patterns.md... Done
Updating progress.md... Done

Session state saved successfully.
```

**Example 2: Save from JSON file**
```bash
python scripts/save-memory.py --state /tmp/state.json
```

**When to use:**
- Before context compaction
- After completing tasks
- Before session termination
- After major decisions

---

## archive-memory.py

**Purpose:** Archive old completed tasks and patterns.

**Usage:**
```bash
python scripts/archive-memory.py [OPTIONS]
```

**Options:**
- `--directory DIR` - Memory directory
- `--type TYPE` - What to archive (tasks, patterns, decisions, all)
- `--cutoff-days DAYS` - Age threshold (default: 30)
- `--dry-run` - Show what would be archived

**Examples:**

**Example 1: Archive old tasks**
```bash
python scripts/archive-memory.py --type tasks --cutoff-days 30
```

Output:
```
Analyzing completed tasks...
Found 78 completed tasks
45 tasks older than 30 days

Creating archive: archive/2025/completed-tasks-202512.md
Writing 45 tasks... Done
Removing from progress.md... Done

Archived: 45 tasks
Space saved: 123KB
```

**Example 2: Dry run**
```bash
python scripts/archive-memory.py --type all --dry-run
```

Output:
```
[DRY RUN] Would archive:
- 45 completed tasks (older than 30 days)
- 12 patterns (not referenced in 60 days)
- 8 decisions (older than 60 days)

Total space to save: ~185KB
No changes made (dry run mode).
```

**When to use:**
- Memory files exceed 150KB
- Slow session initialization
- Regular maintenance

---

## repair-memory.py

**Purpose:** Recover from corrupted or invalid memory files.

**Usage:**
```bash
python scripts/repair-memory.py [OPTIONS]
```

**Options:**
- `--directory DIR` - Memory directory
- `--file FILE` - Specific file to repair
- `--method METHOD` - Repair method (backup, reconstruct, manual)
- `--force` - Skip confirmation prompts

**Examples:**

**Example 1: Auto repair**
```bash
python scripts/repair-memory.py
```

Output:
```
Analyzing memory files...

activeContext.md: Corrupted (truncated)
patterns.md: OK
progress.md: OK

Attempting repair of activeContext.md...
Method: Restore from backup
Latest backup: backups/activeContext.md.backup.20251231-170000

Restoring... Done
Verifying... OK

Repair successful.
```

**Example 2: Specific file repair**
```bash
python scripts/repair-memory.py --file activeContext.md --method reconstruct
```

Output:
```
Repairing activeContext.md using reconstruction method...

Extracting from conversation history... Done
Reconstructing file... Done
Validating... OK

File repaired successfully.
WARNING: Some data may be incomplete. Review and update as needed.
```

**When to use:**
- Corrupted memory files
- After crash or interruption
- Failed memory operations

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Related:** [18-using-scripts.md](18-using-scripts.md) (Main index)
