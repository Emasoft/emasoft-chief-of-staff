# Using Memory Scripts: Initialize and Validate

## Table of Contents

1. [Overview](#overview)
2. [Available Scripts](#available-scripts)
3. [initialize-memory.py](#initialize-memorypy)
4. [validate-memory.py](#validate-memorypy)

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

## initialize-memory.py

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

## validate-memory.py

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

**Version:** 1.0
**Last Updated:** 2026-01-01
**Related:** [18-using-scripts.md](18-using-scripts.md) (Main index)
