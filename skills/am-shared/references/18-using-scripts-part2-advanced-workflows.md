# Using Memory Scripts - Part 2: Advanced Scripts & Workflows

## Table of Contents

1. [Advanced Scripts](#advanced-scripts)
   - [archive-memory.py](#archive-memorypy) - Archive old content
   - [repair-memory.py](#repair-memorypy) - Fix corrupted memory
2. [Common Workflows](#common-workflows)
   - [Daily Startup](#workflow-1-daily-startup)
   - [Before Compaction](#workflow-2-before-compaction)
   - [Weekly Maintenance](#workflow-3-weekly-maintenance)
   - [Emergency Recovery](#workflow-4-emergency-recovery)
3. [Integration Examples](#examples)
4. [Troubleshooting](#troubleshooting)

**See Also:** [Part 1: Basic Scripts](18-using-scripts-part1-basic-scripts.md)

---

## Advanced Scripts

### archive-memory.py

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

### repair-memory.py

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

## Common Workflows

### Workflow 1: Daily Startup

```bash
# 1. Validate memory
python scripts/validate-memory.py

# 2. Load into session
python scripts/load-memory.py

# 3. Begin work...
```

---

### Workflow 2: Before Compaction

```bash
# 1. Save current state
python scripts/save-memory.py --backup

# 2. Validate saved state
python scripts/validate-memory.py

# 3. Ready for compaction
```

---

### Workflow 3: Weekly Maintenance

```bash
# 1. Archive old content
python scripts/archive-memory.py --type all --cutoff-days 30

# 2. Validate after archival
python scripts/validate-memory.py --fix

# 3. Check file sizes
du -h .atlas/memory/*.md
```

---

### Workflow 4: Emergency Recovery

```bash
# 1. Assess damage
python scripts/validate-memory.py --verbose

# 2. Attempt repair
python scripts/repair-memory.py

# 3. If repair fails, reinitialize
python scripts/initialize-memory.py --force
```

---

## Examples

### Example: Integrating into Agent Workflow

```python
# In agent main loop

def initialize_session():
    """Load session memory at startup."""
    result = subprocess.run(
        ['python', 'scripts/load-memory.py', '--format', 'json'],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Error loading memory:", result.stderr)
        # Attempt repair
        repair_memory()
        return initialize_session()  # Retry

    state = json.loads(result.stdout)
    return state

def save_session():
    """Save session memory before shutdown."""
    state_json = json.dumps(current_state)

    with open('/tmp/state.json', 'w') as f:
        f.write(state_json)

    result = subprocess.run(
        ['python', 'scripts/save-memory.py', '--state', '/tmp/state.json', '--backup'],
        capture_output=True
    )

    if result.returncode != 0:
        print("Error saving memory:", result.stderr)
        return False

    return True
```

---

## Troubleshooting

### Issue: Script fails with "module not found"

**Cause:** Missing Python dependencies

**Solution:**
```bash
pip install -r requirements.txt
# Or for scripts specifically:
pip install markdown pyyaml
```

---

### Issue: Permission denied

**Cause:** Scripts not executable

**Solution:**
```bash
chmod +x scripts/*.py
# Or run with python explicitly:
python scripts/validate-memory.py
```

---

### Issue: Script reports errors but files look OK

**Cause:** Script validation rules may be too strict

**Solution:**
1. Review reported errors manually
2. Use `--verbose` to understand what failed
3. Fix actual issues or adjust validation rules

---

**Version:** 1.0
**Last Updated:** 2026-01-08
**Target Audience:** Atlas Orchestrator Agents
**Related:** [Part 1: Basic Scripts](18-using-scripts-part1-basic-scripts.md), SKILL.md (Implementation Scripts section)
