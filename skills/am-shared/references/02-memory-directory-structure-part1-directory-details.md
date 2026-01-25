# Memory Directory Structure - Part 1: Directory Details

## Table of Contents
- 1.1 [Root Level (.session_memory/)](#11-root-level-session_memory)
- 1.2 [active_context/ Directory](#12-active_context-directory)
- 1.3 [patterns/ Directory](#13-patterns-directory)
- 1.4 [progress/ Directory](#14-progress-directory)
- 1.5 [snapshots/ Directory](#15-snapshots-directory)
- 1.6 [archived/ Directory](#16-archived-directory)

---

## 1.1 Root Level (.session_memory/)

**Purpose**: Contains active memory files that are frequently read and updated.

**Files**:
- `session_info.md`: Session metadata (start time, compaction count, environment info)
- `active_context.md`: Current working context (focus, decisions, open questions)
- `progress_tracker.md`: Task tracking (active, completed, blocked tasks)
- `pattern_index.md`: Pattern catalog with quick references

**Update Frequency**: Very high - these files change constantly during operation

**Size Management**: Keep lean - move historical data to snapshots

---

## 1.2 active_context/ Directory

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

---

## 1.3 patterns/ Directory

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

---

## 1.4 progress/ Directory

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

---

## 1.5 snapshots/ Directory

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

---

## 1.6 archived/ Directory

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
