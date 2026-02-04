# Using Memory Scripts - Part 1: Basic Scripts

## Table of Contents

1. [Overview](#overview)
   - What Are Memory Scripts?
   - Why Use Scripts?
2. [Available Scripts](#available-scripts)
3. [Basic Script Usage](#script-usage-guide)
   - [initialize-memory.py](#initialize-memorypy) - Create new memory structure
   - [validate-memory.py](#validate-memorypy) - Check memory integrity
   - [load-memory.py](#load-memorypy) - Load memory into session
   - [save-memory.py](#save-memorypy) - Persist memory to disk

**See Also:** [Part 2: Advanced Scripts & Workflows](18-using-scripts-part2-advanced-workflows.md)

---

## Overview

### What Are Memory Scripts?

Memory scripts are Python automation tools in the `scripts/` subdirectory that help manage session memory operations. They provide command-line interfaces for common memory tasks and can be used manually or integrated into agent workflows.

### Why Use Scripts?

**Benefits:**
- Consistent memory operations
- Automated validation
- Error handling built-in
- Batch operations support
- Standardized output formats

---

## Available Scripts

### Script Inventory

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| `initialize-memory.py` | Create new memory structure | None | Memory files created |
| `validate-memory.py` | Check memory integrity | Memory files | Validation report |
| `load-memory.py` | Load memory into session | Memory files | Session state object |
| `save-memory.py` | Persist memory to disk | Session state | Updated memory files |
| `archive-memory.py` | Archive old content | Memory files | Archive files |
| `repair-memory.py` | Fix corrupted memory | Corrupted files | Repaired files |

---

## Script Usage Guide

### initialize-memory.py

**Purpose:** Create new session memory structure with template files.

**Usage:**
```bash
python scripts/initialize-memory.py [OPTIONS]
```

**Options:**
- `--directory DIR` - Target directory (default: `.chief-of-staff/memory`)
- `--force` - Overwrite existing files
- `--template TEMPLATE` - Template to use (default: standard)

**Examples:**

**Example 1: Basic initialization**
```bash
python scripts/initialize-memory.py
```

Output:
```
Creating memory directory: .chief-of-staff/memory
Creating activeContext.md... Done
Creating patterns.md... Done
Creating progress.md... Done
Creating backups directory... Done

Memory structure initialized successfully.
```

**Example 2: Force reinitialize**
```bash
python scripts/initialize-memory.py --force
```

Output:
```
WARNING: --force specified, will overwrite existing files
Backing up existing files to backups/
Creating new memory files... Done
```

**Example 3: Custom directory**
```bash
python scripts/initialize-memory.py --directory /custom/path
```

**When to use:**
- Starting new project
- After corrupting all memory files
- Setting up test environment

---

### validate-memory.py

**Purpose:** Validate memory files for correctness and consistency.

**Usage:**
```bash
python scripts/validate-memory.py [OPTIONS]
```

**Options:**
- `--directory DIR` - Memory directory to validate
- `--fix` - Attempt automatic fixes
- `--verbose` - Show detailed validation info
- `--report FILE` - Write validation report to file

**Examples:**

**Example 1: Basic validation**
```bash
python scripts/validate-memory.py
```

Output:
```
Validating session memory in .chief-of-staff/memory

Checking activeContext.md...
  ✓ File exists
  ✓ Valid Markdown syntax
  ✓ Required sections present
  ✓ Timestamps valid

Checking patterns.md...
  ✓ File exists
  ✓ Valid Markdown syntax
  ✓ Pattern format correct

Checking progress.md...
  ✓ File exists
  ✓ Valid Markdown syntax
  ✗ Task "Implement auth" in both Todo and Completed sections

Validation failed: 1 error found
```

**Example 2: Validation with auto-fix**
```bash
python scripts/validate-memory.py --fix
```

Output:
```
Validating and fixing issues...

Issue: Task "Implement auth" in multiple sections
Fix: Removing from Todo section (task is completed)
✓ Fixed

All issues resolved. Memory is now valid.
```

**Example 3: Verbose validation**
```bash
python scripts/validate-memory.py --verbose
```

**When to use:**
- After manual memory edits
- Before context compaction
- During troubleshooting
- Regular maintenance checks

---

### load-memory.py

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
Loading session memory from .chief-of-staff/memory

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

### save-memory.py

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
Saving session state to .chief-of-staff/memory

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

**Version:** 1.0
**Last Updated:** 2026-01-08
**Target Audience:** Chief of Staff Agents
**Related:** [Part 2: Advanced Scripts & Workflows](18-using-scripts-part2-advanced-workflows.md)
