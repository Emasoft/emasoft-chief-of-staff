# Using Memory Scripts

## Overview

Memory scripts are Python automation tools in the `scripts/` subdirectory that help manage session memory operations. They provide command-line interfaces for common memory tasks and can be used manually or integrated into agent workflows.

**Benefits:**
- Consistent memory operations
- Automated validation
- Error handling built-in
- Batch operations support
- Standardized output formats

---

## Table of Contents

This document is split into parts for efficient loading. Read the section relevant to your current task.

### Part 1: Initialize and Validate Scripts

**File:** [18-using-scripts-part1-initialize-validate.md](18-using-scripts-part1-initialize-validate.md)

**Contents:**
- 1.1 Overview - What are memory scripts and why use them
- 1.2 Available Scripts - Full inventory table of all scripts
- 1.3 initialize-memory.py - Creating new memory structure
  - 1.3.1 Basic initialization for new projects
  - 1.3.2 Force reinitialize after corruption
  - 1.3.3 Custom directory initialization
- 1.4 validate-memory.py - Checking memory integrity
  - 1.4.1 Basic validation workflow
  - 1.4.2 Auto-fix validation issues
  - 1.4.3 Verbose validation for debugging

**When to read:** Starting new projects, setting up memory, validating after manual edits

---

### Part 2: Load, Save, Archive, and Repair Scripts

**File:** [18-using-scripts-part2-load-save-archive-repair.md](18-using-scripts-part2-load-save-archive-repair.md)

**Contents:**
- 2.1 load-memory.py - Loading session state
  - 2.1.1 Load and display current state
  - 2.1.2 Export state to JSON file
- 2.2 save-memory.py - Persisting session state
  - 2.2.1 Save with automatic backup
  - 2.2.2 Save from external JSON file
- 2.3 archive-memory.py - Archiving old content
  - 2.3.1 Archive completed tasks by age
  - 2.3.2 Dry run to preview archival
- 2.4 repair-memory.py - Recovering from corruption
  - 2.4.1 Automatic repair from backups
  - 2.4.2 Reconstruct from conversation history

**When to read:** Session initialization, compaction prep, maintenance, recovery

---

### Part 3: Workflows, Examples, and Troubleshooting

**File:** [18-using-scripts-part3-workflows-examples.md](18-using-scripts-part3-workflows-examples.md)

**Contents:**
- 3.1 Common Workflows
  - 3.1.1 Daily Startup workflow
  - 3.1.2 Before Compaction workflow
  - 3.1.3 Weekly Maintenance workflow
  - 3.1.4 Emergency Recovery workflow
- 3.2 Implementation Examples
  - 3.2.1 Python integration for agent workflows
- 3.3 Troubleshooting
  - 3.3.1 Module not found errors
  - 3.3.2 Permission denied issues
  - 3.3.3 False positive validation errors

**When to read:** Daily operations, integrating scripts into agents, fixing issues

---

## Quick Reference: Script Inventory

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `initialize-memory.py` | Create new memory structure | New project setup |
| `validate-memory.py` | Check memory integrity | After manual edits, before compaction |
| `load-memory.py` | Load memory into session | Session start, after compaction |
| `save-memory.py` | Persist memory to disk | Before compaction, after major tasks |
| `archive-memory.py` | Archive old content | Weekly maintenance |
| `repair-memory.py` | Fix corrupted memory | After crashes, corruption |

---

## Quick Reference: Common Commands

```bash
# Daily startup
python scripts/validate-memory.py
python scripts/load-memory.py

# Before compaction
python scripts/save-memory.py --backup
python scripts/validate-memory.py

# Weekly maintenance
python scripts/archive-memory.py --type all --cutoff-days 30
python scripts/validate-memory.py --fix

# Emergency recovery
python scripts/validate-memory.py --verbose
python scripts/repair-memory.py
```

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Target Audience:** Atlas Orchestrator Agents
**Related:** SKILL.md (Implementation Scripts section)
