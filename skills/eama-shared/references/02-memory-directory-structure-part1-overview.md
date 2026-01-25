# Memory Directory Structure - Part 1: Overview and Naming

## Table of Contents
1. [When you need to understand the purpose](#purpose)
2. [To see canonical structure](#canonical-structure)
3. [Understanding directory meanings](#directory-descriptions)
4. [Learning file naming rules](#file-naming-conventions)

**Related Documents:**
- [Part 2: Validation and Operations](./02-memory-directory-structure-part2-operations.md) - Validation scripts, repair procedures, examples, troubleshooting

---

## Purpose

This document defines the canonical directory structure for session memory. Understanding this structure is essential for:
- Proper file organization
- Automated memory management
- Recovery from failures
- Compaction safety
- Pattern discovery

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

## Directory Descriptions

### Root Level (.session_memory/)

**Purpose**: Contains active memory files that are frequently read and updated.

**Files**:
- `session_info.md`: Session metadata (start time, compaction count, environment info)
- `active_context.md`: Current working context (focus, decisions, open questions)
- `progress_tracker.md`: Task tracking (active, completed, blocked tasks)
- `pattern_index.md`: Pattern catalog with quick references

**Update Frequency**: Very high - these files change constantly during operation

**Size Management**: Keep lean - move historical data to snapshots

### active_context/ Directory

**Purpose**: Stores timestamped snapshots of active context for recovery and audit.

**Files**:
- `context_YYYYMMDD_HHMMSS.md`: Timestamped context snapshot
- `context_latest.md`: Symlink to most recent snapshot

**When Created**:
- Before major context updates
- Before compaction
- At user request
- On significant decision points

**Retention**: Keep last 10 snapshots, archive older ones

**Example Filename**: `context_20260101_143022.md`

### patterns/ Directory

**Purpose**: Stores categorized patterns discovered during work.

**Subdirectories**:
- `problem_solution/`: Problem-solution pairs
- `workflow/`: Effective workflow patterns
- `decision_logic/`: Decision trees and logic patterns
- `error_recovery/`: Error handling procedures
- `configuration/`: Configuration patterns

**File Naming**: `{category_prefix}_{number}_{brief_description}.md`
- `ps_`: Problem-Solution
- `wf_`: Workflow
- `dl_`: Decision-Logic
- `er_`: Error-Recovery
- `cfg_`: Configuration

**Examples**:
- `ps_001_git_auth_failure.md`
- `wf_002_parallel_testing.md`
- `dl_003_feature_approval_logic.md`

### progress/ Directory

**Purpose**: Stores timestamped snapshots of progress tracker for recovery.

**Files**:
- `progress_YYYYMMDD_HHMMSS.md`: Timestamped progress snapshot
- `progress_latest.md`: Symlink to most recent snapshot

**When Created**:
- After completing major tasks
- Before compaction
- At milestone points
- On user request

**Retention**: Keep last 10 snapshots, archive older ones

### snapshots/ Directory

**Purpose**: Full session snapshots combining all memory components.

**Structure**:
Each snapshot is a directory containing:
- `context.md`: Copy of active_context.md
- `progress.md`: Copy of progress_tracker.md
- `patterns.md`: Copy of pattern_index.md
- `metadata.txt`: Snapshot metadata (timestamp, trigger reason)

**When Created**:
- Before compaction (mandatory)
- At major milestones
- Before risky operations
- On explicit request

**Retention**: Keep last 5 full snapshots

### archived/ Directory

**Purpose**: Long-term storage for old snapshots and pre-compaction states.

**Structure**:
- `pre_compaction_N/`: State before Nth compaction
- `README.md`: Index of archived data with timestamps and reasons

**Content**:
Each archive contains copies of:
- `active_context.md`
- `progress_tracker.md`
- `pattern_index.md`
- `timestamp.txt`: When archived and why

**Retention**: Keep indefinitely unless manually cleaned

## File Naming Conventions

### Timestamp Format

Use ISO-8601 compatible format for consistency:
- Format: `YYYYMMDD_HHMMSS`
- Example: `20260101_143022` (January 1, 2026, 14:30:22)
- Always use UTC timezone

```bash
# Generate timestamp
timestamp=$(date -u +"%Y%m%d_%H%M%S")
```

### Pattern Files

Format: `{prefix}_{number}_{description}.md`

**Prefix Codes**:
- `ps`: Problem-Solution
- `wf`: Workflow
- `dl`: Decision-Logic
- `er`: Error-Recovery
- `cfg`: Configuration

**Number**: Zero-padded 3-digit sequential number (001, 002, ...)

**Description**: Brief kebab-case description (lowercase, hyphens)

**Examples**:
```
ps_001_git-auth-failure.md
wf_002_parallel-agent-spawning.md
dl_003_approve-feature-requests.md
er_004_context-overflow-recovery.md
cfg_005_eslint-configuration.md
```

### Snapshot Directories

Format: `snapshot_{timestamp}` or `pre_compaction_{count}`

**Examples**:
```
snapshot_20260101_143022/
snapshot_20260101_150000/
pre_compaction_1/
pre_compaction_2/
```

---

**Next**: See [Part 2: Validation and Operations](./02-memory-directory-structure-part2-operations.md) for validation scripts, repair procedures, examples, and troubleshooting.
