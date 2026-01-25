---
name: ao-session-memory
description: Critical persistence mechanism for Atlas orchestrator agent enabling continuity across multiple interactions, surviving context window compaction, and graceful recovery from interruptions. Structured data storage system consisting of three coordinated documents stored in .atlas/memory/ directory - activeContext.md (current working state), patterns.md (learned patterns and heuristics), and progress.md (task tracking and completion state). Includes config snapshot integration for configuration drift detection and conflict resolution.
license: Apache-2.0
compatibility: Requires file system access to .atlas/memory/ directory, Markdown parsing capabilities, and understanding of session lifecycle (initialization, execution, termination).
metadata:
  author: Anthropic
  version: 1.0.0
context: fork
---

# Atlas Orchestrator Session Memory Skill

## Overview

Session memory is a critical persistence mechanism for the Atlas orchestrator agent. It enables the agent to maintain continuity across multiple interactions, survive context window compaction, and recover gracefully from interruptions. This skill teaches you how to implement, manage, and troubleshoot session memory in Atlas orchestrator.

## What Is Session Memory?

Session memory is a structured data storage system that persists an agent's working state across multiple conversations and context window compressions. Unlike conversation history (which can be lost when context is compacted), session memory is explicitly saved to disk and reloaded at each session start.

**Key characteristics:**
- **Persistent**: Survives conversation context limits
- **Structured**: Organized into three specialized documents
- **Recoverable**: Can be restored if the agent is interrupted
- **Compaction-safe**: Not affected by context window management

## Session Memory Components

Session memory consists of three coordinated documents stored in the `.atlas/memory/` directory:

### 1. **activeContext.md** - Current Working State
Captures the immediate context needed to continue work:
- Current task being executed
- Active file being edited and its line number
- Open dialog states or interactive prompts
- Recent decisions and their rationale
- Pending operations waiting for completion

### 2. **patterns.md** - Learned Patterns and Heuristics
Records patterns discovered during the session:
- Code patterns and anti-patterns identified
- Architecture insights and recommendations
- Recurring issues and their solutions
- Project-specific conventions learned
- Performance characteristics observed

### 3. **progress.md** - Task Tracking and Completion State
Maintains the complete task execution state:
- Master todo list with task status
- Dependencies between tasks
- Completed tasks with timestamps
- Failed tasks with error details
- Critical milestones reached
- Blocked tasks and their blockers

## How Session Memory Works

### Phase 1: Session Initialization (Load)

**Order of operations:**
1. Check if `.atlas/memory/` directory exists
2. Load `activeContext.md` if present
3. Load `patterns.md` if present
4. Load `progress.md` if present
5. Verify all loaded data is valid and consistent
6. Report session state to the user

**When to initialize:** At session start, when resuming work, after context compaction, or when recovering from interruptions.

### Phase 2: Session Execution (Update)

**During work, memory is updated:**
1. After completing each logical step
2. When discovering new patterns
3. When task status changes
4. When making architectural decisions
5. When encountering blockers

### Phase 3: Session Termination (Save)

**Order of operations:**
1. Ensure all updates have been written to disk
2. Verify the memory files are not corrupted
3. Check that all critical state is captured
4. Confirm the session can be resumed from this point

## Core Procedures

### PROCEDURE 1: Initialize Session Memory

**Steps:** Check directory exists, read all three memory files, validate Markdown syntax, report loaded state.

**Related documentation:**

#### Initializing Session Memory ([references/01-initialize-session-memory.md](references/01-initialize-session-memory.md))
- Understanding purpose → Purpose section
- When to initialize → When To Initialize section
- How to perform initialization → Initialization Procedure section
- Directory structure → Directory Structure section
- Initial files to create → Initial Files section
- How to verify → Verification Steps section
- Implementation examples → Examples section
- Issues → Troubleshooting section

#### Memory Directory Structure ([references/02-memory-directory-structure.md](references/02-memory-directory-structure.md))
- Canonical structure → Canonical Structure section
- Directory meanings → Directory Descriptions section
- File naming rules → File Naming Conventions section
- Structure validation → Structure Validation section

#### Memory Validation ([references/04-memory-validation.md](references/04-memory-validation.md))
- Validation levels → Validation Levels section
- Validation procedures → Validation Procedures section
- Validation scripts → Validation Scripts section
- Validation checklist → Validation Checklist section

### PROCEDURE 2: Update Active Context

**When to use:** When shifting focus, changing current line, entering/exiting dialogs, or making decisions.

**Steps:** Identify change, open activeContext.md, update relevant section with timestamp, write immediately.

**Related documentation:**

#### Managing Active Context ([references/03-manage-active-context.md](references/03-manage-active-context.md))
- What active context is → What Is Active Context section
- Context update triggers → Context Update Triggers section
- Update procedures → Update Procedures section
- Context snapshots → Context Snapshot Creation section
- Context pruning → Context Pruning section

#### Context Update Patterns ([references/06-context-update-patterns.md](references/06-context-update-patterns.md))
- Update patterns overview → Update Patterns Overview section
- Task switching → Pattern 1 Task Switch Update section
- Recording decisions → Pattern 2 Decision Recording Update section
- Adding questions → Pattern 3 Question Addition Update section
- Milestone updates → Pattern 4 Progress Milestone Update section
- Pre-compaction updates → Pattern 5 Pre Compaction Update section

### PROCEDURE 3: Record Discovered Patterns

**When to use:** After identifying recurring patterns, anti-patterns, conventions, or effective solutions.

**Steps:** Identify pattern, open patterns.md, add with description/examples, categorize, add date and context.

**Related documentation:**

#### Recording Patterns ([references/05-record-patterns.md](references/05-record-patterns.md))
- What patterns are → What Are Patterns section
- Pattern categories → Pattern Categories section
- When to record → When To Record Patterns section
- Recording procedure → Pattern Recording Procedure section
- File structure → Pattern File Structure section
- Index management → Pattern Index Management section

#### Pattern Categories ([references/07-pattern-categories.md](references/07-pattern-categories.md))
- Category definitions → Category Definitions section
- Problem-solution patterns → Problem Solution Patterns section
- Workflow patterns → Workflow Patterns section
- Decision-logic patterns → Decision Logic Patterns section
- Error-recovery patterns → Error Recovery Patterns section
- Configuration patterns → Configuration Patterns section
- Choosing categories → Choosing The Right Category section

### PROCEDURE 4: Update Task Progress

**When to use:** When task completes, status changes, task becomes blocked, or dependencies resolve.

**Steps:** Identify changed task, open progress.md, update status with timestamp, document blockers if any, update dependent tasks.

**Related documentation:**

#### Managing Progress Tracking ([references/08-manage-progress-tracking.md](references/08-manage-progress-tracking.md))
- Tracker structure → Progress Tracker Structure section
- Task states → Task States section
- Task management → Task Management Procedures section
- Dependencies → Dependency Management section
- Progress snapshots → Progress Snapshots section

#### Task Dependencies ([references/09-task-dependencies.md](references/09-task-dependencies.md))
- Dependency types → Dependency Types section
- Dependency notation → Dependency Notation section
- Dependency management → Dependency Management section
- Critical path → Critical Path Analysis section
- Validation → Dependency Validation section

### PROCEDURE 5: Recover Session After Interruption

**When to use:** After unexpected termination, manual interruption, or long breaks.

**Steps:** Load all memory files, read activeContext.md for work state, read progress.md for task state, ask user to confirm resumption.

**Related documentation:**

#### Interruption Recovery ([references/10-recovery-procedures.md](references/10-recovery-procedures.md))
- Recovery scenarios → Recovery Scenarios section
- Failed compaction recovery → Recovery From Failed Compaction section
- Corrupted memory recovery → Recovery From Corrupted Memory section
- Lost context recovery → Recovery From Lost Context section
- Snapshot failure recovery → Recovery From Snapshot Failure section
- Emergency recovery → Emergency Recovery section

### PROCEDURE 6: Prepare for Context Compaction

**When to use:** When context usage exceeds 70%, before long-running operations, or proactively.

**Steps:** Ensure all three memory files are fully updated, run validation, write to disk, confirm ready.

**Related documentation:**

#### Compaction Safety ([references/11-compaction-safety.md](references/11-compaction-safety.md))
- Compaction risks → Compaction Risks section
- Pre-compaction safety checks → Pre Compaction Safety Checks section
- Safe compaction procedure → Safe Compaction Procedure section
- Post-compaction verification → Post Compaction Verification section
- Rollback procedure → Rollback Procedure section

#### Pre-compaction Checklist ([references/12-pre-compaction-checklist.md](references/12-pre-compaction-checklist.md))
- Master checklist → Master Checklist section
- Preparation phase → Preparation Phase section
- Backup phase → Backup Phase section
- Validation phase → Validation Phase section
- Final verification → Final Verification section
- Go/no-go decision → Gono Go Decision section

## Config Snapshot Integration

Session memory captures configuration state at session start to detect drift, maintain consistency, enable conflict resolution, and support audit trails.

**Config snapshot location:** `.atlas/memory/config-snapshot.md`

This file is separate from authoritative configs in `.atlas/config/` and serves as a point-in-time capture.

### PROCEDURE 7: Capture Config Snapshot at Session Start

**When to use:** During session initialization, after loading core memory files, before any work begins.

**Steps:** Read all config files from `.atlas/config/`, create snapshot with timestamp and session ID, copy config content and metadata, save snapshot, record in activeContext.md.

**Related documentation:**

#### Config Snapshot Creation ([references/19-config-snapshot-creation.md](references/19-config-snapshot-creation.md))
- What is a config snapshot → What Is A Config Snapshot section
- Why snapshots matter → Why Snapshots Matter section
- Creating initial snapshot → Procedure 1 Create Initial Snapshot section
- Updating snapshot → Procedure 2 Update Snapshot section
- Validating snapshot → Procedure 3 Validate Snapshot section
- Snapshot structure → Snapshot Structure section
- Implementation examples → Examples section
- Issues → Troubleshooting section

### PROCEDURE 8: Detect Config Changes During Session

**When to use:** Periodically during long sessions (every 30 minutes), after config change notifications, before major tasks, when unexpected behavior occurs.

**Steps:** Read current and snapshot configs, compare timestamps, perform content comparison if timestamps differ, identify changed sections, log in activeContext.md, trigger conflict resolution if critical.

**Related documentation:**

#### Config Change Detection ([references/20-config-change-detection.md](references/20-config-change-detection.md))
- Detection methods → Detection Methods section
- Timestamp-based detection → Procedure 1 Timestamp Based Detection section
- Content-based detection → Procedure 2 Content Based Detection section
- Notification handling → Procedure 3 Change Notification Handling section
- Periodic drift checking → Procedure 4 Periodic Drift Check section
- Change classification → Change Classification section
- Implementation examples → Examples section
- Issues → Troubleshooting section

### PROCEDURE 9: Handle Config Version Conflicts

**When to use:** When change detection reveals critical differences, high-priority notifications arrive, current work becomes incompatible, or orchestrator requests resolution.

**Conflict types:**
- **Type A (Non-Breaking):** Formatting, documentation - adopt immediately
- **Type B (Breaking-Future):** Major versions - complete task, then adopt
- **Type C (Breaking-Immediate):** Security patches - pause, adopt, restart
- **Type D (Irreconcilable):** Contradictory requirements - stop, escalate

**Related documentation:**

#### Config Conflict Resolution ([references/21-config-conflict-resolution.md](references/21-config-conflict-resolution.md))
- Conflict types → Conflict Types section
- Resolution strategies → Resolution Strategies section
- Non-breaking resolution → Procedure 1 Resolve Non Breaking Changes section
- Future breaking resolution → Procedure 2 Resolve Breaking Changes Future section
- Immediate breaking resolution → Procedure 3 Resolve Breaking Changes Immediate section
- Irreconcilable resolution → Procedure 4 Resolve Irreconcilable Conflicts section
- Decision trees → Decision Trees section
- Implementation examples → Examples section
- Issues → Troubleshooting section

## Task Checklist

- [ ] Understand session memory purpose and components
- [ ] Learn Phase 1: Initialize session memory at start
- [ ] Learn Phase 2: Update memory during work
- [ ] Learn Phase 3: Save memory before exit
- [ ] Practice PROCEDURE 1: Initialize session memory
- [ ] Practice PROCEDURE 2: Update active context
- [ ] Practice PROCEDURE 3: Record discovered patterns
- [ ] Practice PROCEDURE 4: Update task progress
- [ ] Practice PROCEDURE 5: Recover after interruption
- [ ] Practice PROCEDURE 6: Prepare for context compaction
- [ ] Practice PROCEDURE 7-9: Config snapshot integration
- [ ] Test memory persistence across sessions
- [ ] Test memory recovery after interruptions
- [ ] Test compaction safety

## Troubleshooting

### Issue: Memory files are corrupted or have invalid Markdown

**Symptoms:** Files cannot be parsed, missing sections, syntax errors.

#### Memory File Recovery ([references/13-file-recovery.md](references/13-file-recovery.md))
- Corruption types → Types Of Memory File Corruption section
- Recovery procedures → Recovery Procedures section
- Prevention strategies → Prevention Strategies section

### Issue: Active context becomes out of sync with actual state

**Symptoms:** Agent continues wrong task, references outdated locations, old decisions referenced.

#### Context Synchronization ([references/14-context-sync.md](references/14-context-sync.md))
- Context drift → What Is Context Drift section
- Synchronization points → Synchronization Points section
- Synchronization procedures → Synchronization Procedures section
- Consistency checks → Consistency Checks section

### Issue: Progress tracking becomes inconsistent

**Symptoms:** Tasks marked complete but work not done, dependencies resolved but blocked, timestamps out of order.

#### Progress Validation ([references/15-progress-validation.md](references/15-progress-validation.md))
- Validation rules → Validation Rules section
- Validation procedures → Validation Procedures section
- Common errors → Common Validation Errors section
- Automated validation → Automated Validation section

### Issue: Memory files grow too large

**Symptoms:** Slow initialization, noticeably slow operations, files are hundreds of KB.

#### Memory Archival ([references/16-memory-archival.md](references/16-memory-archival.md))
- When to archive → When To Archive section
- What to archive → What To Archive section
- Archival procedures → Archival Procedures section
- Archive organization → Archive Organization section

### Issue: Session memory does not survive context compaction

**Symptoms:** Memory files exist but not reloaded, progress lost, patterns forgotten.

#### Compaction Integration ([references/17-compaction-integration.md](references/17-compaction-integration.md))
- Understanding compaction → Understanding Context Compaction section
- Compaction risks → Compaction Risks section
- Integration procedures → Integration Procedures section
- Compaction triggers → Compaction Triggers section

## Implementation Scripts

The `scripts/` subdirectory includes automation helpers:

- **`initialize-memory.py`** - Create new session memory structure
- **`validate-memory.py`** - Check memory files for consistency
- **`load-memory.py`** - Load memory into session state
- **`save-memory.py`** - Persist memory to disk
- **`archive-memory.py`** - Archive old completed tasks
- **`repair-memory.py`** - Recover from corruption

#### Using Memory Scripts ([references/18-using-scripts.md](references/18-using-scripts.md))
- Available scripts → Available Scripts section
- Script usage guide → Script Usage Guide section
- Common workflows → Common Workflows section
- Implementation examples → Examples section

## Key Takeaways

1. **Session memory is separate from conversation history** - It persists even when context is compacted
2. **Three coordinated documents work together** - activeContext, patterns, and progress must be kept in sync
3. **Memory must be loaded at session start and saved at session end** - This is not automatic
4. **Frequent updates prevent data loss** - Do not wait until session end to save important changes
5. **Validation ensures consistency** - Check memory integrity regularly
6. **Config snapshots detect drift** - Capture config at session start and compare periodically

## Next Steps

### 1. Read Initializing Session Memory
See [references/01-initialize-session-memory.md](references/01-initialize-session-memory.md) for complete initialization procedures.

### 2. Read Memory Directory Structure
See [references/02-memory-directory-structure.md](references/02-memory-directory-structure.md) for canonical directory layout.

### 3. Implement Python Scripts
Implement the Python scripts from the `scripts/` directory in your project.

### 4. Integrate Memory into Agent Lifecycle
- Load memory at initialization
- Update during execution
- Save before exit

---

**Version:** 1.0
**Last Updated:** 2025-12-29
**Target Audience:** Atlas Orchestrator Agents
**Difficulty Level:** Intermediate
