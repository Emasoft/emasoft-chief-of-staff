---
name: ecos-session-memory-library
description: Use when managing session memory persistence across multiple interactions, surviving context window compaction, and recovering from interruptions. Trigger with shared configuration or pattern lookups.
license: Apache-2.0
compatibility: Requires file system access to design/memory/ directory, Markdown parsing capabilities, and understanding of session lifecycle (initialization, execution, termination). Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ecos-main
---

# Emasoft Chief of Staff Session Memory Skill

## Overview

Session memory is a critical persistence mechanism for the Chief of Staff agent. It enables the agent to maintain continuity across multiple interactions, survive context window compaction, and recover gracefully from interruptions. This skill teaches you how to implement, manage, and troubleshoot session memory in Chief of Staff.

## Prerequisites

Before using this skill, ensure:
1. Shared reference files are accessible
2. Pattern definitions are current
3. Configuration templates are available

## Instructions

1. Identify the shared resource needed
2. Locate in references directory
3. Apply pattern or configuration
4. Document usage

## Output

| Resource Type | Output |
|---------------|--------|
| Pattern | Pattern definition and usage example |
| Configuration | Config template with filled values |
| Reference | Reference content for context |

## Session Memory Fundamentals

Session memory persists agent state across conversations and context compaction. It uses three coordinated documents in `design/memory/`: **activeContext.md** (current work), **patterns.md** (learned patterns), and **progress.md** (task tracking).

For complete details, see [references/00-session-memory-fundamentals.md](references/00-session-memory-fundamentals.md):
- What Is Session Memory - Core persistence mechanism
- Key Characteristics - Persistent, structured, recoverable, compaction-safe
- Session Memory Components - The three documents and their contents

## Session Memory Lifecycle

Session memory follows three phases: **Load** (at session start), **Update** (during work), and **Save** (before exit).

For complete details, see [references/00-session-memory-lifecycle.md](references/00-session-memory-lifecycle.md):
- Phase 1: Session Initialization (Load) - Order of operations, when to initialize
- Phase 2: Session Execution (Update) - When to update memory
- Phase 3: Session Termination (Save) - Order of operations for clean exit

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

**Config snapshot location:** `design/memory/config-snapshot.md`

This file is separate from authoritative configs in `design/config/` (OPTIONAL: If EOA (Emasoft Orchestrator Agent) plugin is installed) and serves as a point-in-time capture.

### PROCEDURE 7: Capture Config Snapshot at Session Start

**When to use:** During session initialization, after loading core memory files, before any work begins.

**Steps:** Read all config files from `design/config/` (OPTIONAL: If EOA (Emasoft Orchestrator Agent) plugin is installed), create snapshot with timestamp and session ID, copy config content and metadata, save snapshot, record in activeContext.md.

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

Copy this checklist and track your progress:

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

## Examples

### Example 1: Initialize Session Memory

```bash
# Input: New session, no memory files
python3 scripts/initialize-memory.py --project-dir ./design/memory

# Output: Creates design/memory/{activeContext.md, patterns.md, progress.md}
```

### Example 2: Update Active Context

```markdown
# Input: Switching tasks
## Current Focus
- **Active Task:** fix-bug-123
- **Previous Task:** implement-auth (paused)
- **Timestamp:** 2026-02-03T14:30:00Z
# Output: activeContext.md updated
```

### Example 3: Record Discovered Pattern

```markdown
# Input: Found error handling pattern
## Pattern: Fail-Fast Error Propagation
**Category:** Error Recovery | **Discovered:** 2026-02-03
**Problem:** Silent failures causing cascading issues
**Solution:** Let errors propagate, handle at boundary layers only
# Output: Pattern added to patterns.md
```

For more examples, see [references/00-session-memory-examples.md](references/00-session-memory-examples.md)

## Error Handling

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

## Chief of Staff Integrations

The Chief of Staff agent requires additional integrations beyond session memory for team coordination.

### AI Maestro Integration

AI Maestro is the inter-agent messaging system that enables the Chief of Staff to coordinate with other agents.

**Related documentation:**

#### AI Maestro Integration ([references/ai-maestro-integration.md](references/ai-maestro-integration.md))
- What is AI Maestro → What Is AI Maestro section
- Core API endpoints → Core API Endpoints section
- Session management → Session Management section
- Message operations → Message Operations section
- Broadcast operations → Broadcast Operations section
- Health and status → Health And Status section
- Examples → Integration Examples section
- Issues → Troubleshooting section

### State File Format

The Chief of Staff uses specialized state files for team coordination, performance tracking, and alerts.

**Related documentation:**

#### State File Format ([references/state-file-format.md](references/state-file-format.md))
- State file overview → Overview Of State Files section
- Chief of Staff state file → Chief Of Staff State File section
- Team roster file → Team Roster File section
- Coordination log file → Coordination Log File section
- Performance data files → Performance Data Files section
- Alert state file → Alert State File section
- State file operations → State File Operations section
- Issues → Troubleshooting section

### Error Handling

The Chief of Staff follows a fail-fast approach to error handling with explicit recovery procedures.

**Related documentation:**

#### Error Handling ([references/error-handling.md](references/error-handling.md))
- Error handling philosophy → Error Handling Philosophy section
- Error categories → Error Categories section
- Communication errors → Communication Errors section
- Coordination errors → Coordination Errors section
- Resource errors → Resource Errors section
- State management errors → State Management Errors section
- Error logging and reporting → Error Logging And Reporting section
- Recovery procedures → Recovery Procedures section

## Key Takeaways

1. **Session memory is separate from conversation history** - It persists even when context is compacted
2. **Three coordinated documents work together** - activeContext, patterns, and progress must be kept in sync
3. **Memory must be loaded at session start and saved at session end** - This is not automatic
4. **Frequent updates prevent data loss** - Do not wait until session end to save important changes
5. **Validation ensures consistency** - Check memory integrity regularly
6. **Config snapshots detect drift** - Capture config at session start and compare periodically
7. **AI Maestro enables team coordination** - Use it for all inter-agent communication
8. **State files persist coordination state** - Keep roster, logs, and alerts current
9. **Errors should fail fast** - No silent failures or workarounds

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

## Resources

### Session Memory
- [Initialize Session Memory](references/01-initialize-session-memory.md)
- [Memory Directory Structure](references/02-memory-directory-structure.md)
- [Manage Active Context](references/03-manage-active-context.md)
- [Memory Validation](references/04-memory-validation.md)
- [Record Patterns](references/05-record-patterns.md)
- [Using Memory Scripts](references/18-using-scripts.md)

### Chief of Staff Coordination
- [AI Maestro Integration](references/ai-maestro-integration.md)
- [State File Format](references/state-file-format.md)
- [Error Handling](references/error-handling.md)

---

**Version:** 1.0.0
**Last Updated:** 2025-02-01
**Target Audience:** Emasoft Chief of Staff Agent
**Difficulty Level:** Intermediate
