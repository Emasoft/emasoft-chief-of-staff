# Memory Directory Structure

## Table of Contents

1. [Purpose](#purpose)
2. [Canonical Structure](#canonical-structure)
3. [Directory Descriptions](#directory-descriptions) → [Part 1: Directory Details](./02-memory-directory-structure-part1-directory-details.md)
4. [File Naming Conventions](#file-naming-conventions) → [Part 2: Naming and Validation](./02-memory-directory-structure-part2-naming-validation.md)
5. [Structure Validation](#structure-validation) → [Part 2: Naming and Validation](./02-memory-directory-structure-part2-naming-validation.md)
6. [Examples](#examples) → [Part 3: Examples and Troubleshooting](./02-memory-directory-structure-part3-examples-troubleshooting.md)
7. [Troubleshooting](#troubleshooting) → [Part 3: Examples and Troubleshooting](./02-memory-directory-structure-part3-examples-troubleshooting.md)

---

## Purpose

This document defines the canonical directory structure for session memory. Understanding this structure is essential for:
- Proper file organization
- Automated memory management
- Recovery from failures
- Compaction safety
- Pattern discovery

---

## Canonical Structure

```
.session_memory/
│
├── session_info.md              # Session metadata and statistics
├── active_context.md            # Current working context
├── progress_tracker.md          # Task progress tracking
├── pattern_index.md             # Catalog of recorded patterns
│
├── active_context/              # Context snapshots directory
│   ├── context_YYYYMMDD_HHMMSS.md
│   └── context_latest.md -> context_YYYYMMDD_HHMMSS.md
│
├── patterns/                    # Recorded patterns directory
│   ├── problem_solution/
│   │   ├── ps_001_description.md
│   │   └── ps_002_description.md
│   ├── workflow/
│   │   ├── wf_001_description.md
│   │   └── wf_002_description.md
│   ├── decision_logic/
│   │   └── dl_001_description.md
│   ├── error_recovery/
│   │   └── er_001_description.md
│   └── configuration/
│       └── cfg_001_description.md
│
├── progress/                    # Progress snapshots directory
│   ├── progress_YYYYMMDD_HHMMSS.md
│   └── progress_latest.md -> progress_YYYYMMDD_HHMMSS.md
│
├── snapshots/                   # Full session snapshots
│   ├── snapshot_YYYYMMDD_HHMMSS/
│   │   ├── context.md
│   │   ├── progress.md
│   │   └── patterns.md
│   └── snapshot_latest -> snapshot_YYYYMMDD_HHMMSS/
│
└── archived/                    # Archived data (post-compaction)
    ├── pre_compaction_N/
    │   ├── active_context.md
    │   ├── progress_tracker.md
    │   └── timestamp.txt
    └── README.md                # Archive index
```

---

## Directory Descriptions

For detailed descriptions of each directory and its purpose, see:
→ **[Part 1: Directory Details](./02-memory-directory-structure-part1-directory-details.md)**

Contents:
- 1.1 Root Level (.session_memory/) - purpose, files, update frequency
- 1.2 active_context/ Directory - snapshots, retention policy
- 1.3 patterns/ Directory - categorization, file naming prefixes
- 1.4 progress/ Directory - progress snapshots
- 1.5 snapshots/ Directory - full session snapshots
- 1.6 archived/ Directory - long-term storage

---

## File Naming Conventions

For timestamp formats, pattern file naming, and snapshot directory naming, see:
→ **[Part 2: Naming and Validation](./02-memory-directory-structure-part2-naming-validation.md)**

Contents:
- 2.1 Timestamp Format - ISO-8601 compatible format
- 2.2 Pattern Files - prefix codes, numbering, descriptions
- 2.3 Snapshot Directories - naming conventions

---

## Structure Validation

For validation and repair scripts, see:
→ **[Part 2: Naming and Validation](./02-memory-directory-structure-part2-naming-validation.md)**

Contents:
- 2.4 Validation Script - validate_structure.sh
- 2.5 Repair Damaged Structure - repair_structure.sh

---

## Examples

For implementation examples, see:
→ **[Part 3: Examples and Troubleshooting](./02-memory-directory-structure-part3-examples-troubleshooting.md)**

Contents:
- 3.1 Create Complete Structure from Scratch
- 3.2 Verify Structure Integrity
- 3.3 Create Snapshot with Proper Structure

---

## Troubleshooting

For common problems and solutions, see:
→ **[Part 3: Examples and Troubleshooting](./02-memory-directory-structure-part3-examples-troubleshooting.md)**

Contents:
- 3.4 Pattern Category Directories Missing
- 3.5 Symlinks Broken
- 3.6 Excessive Disk Usage
- 3.7 Cannot Determine Structure Version
- 3.8 File Permissions Prevent Access
