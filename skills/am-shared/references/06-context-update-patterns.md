# Context Update Patterns

## Table of Contents
1. [When you need to understand the purpose](#purpose)
2. [Understanding update patterns overview](#update-patterns-overview)
3. [When switching tasks](#pattern-1-task-switch-update) - See [Part 1](06-context-update-patterns-part1-task-decision.md)
4. [When recording decisions](#pattern-2-decision-recording-update) - See [Part 1](06-context-update-patterns-part1-task-decision.md)
5. [When adding questions](#pattern-3-question-addition-update) - See [Part 2](06-context-update-patterns-part2-question-milestone.md)
6. [When reaching milestones](#pattern-4-progress-milestone-update) - See [Part 2](06-context-update-patterns-part2-question-milestone.md)
7. [When preparing before compaction](#pattern-5-pre-compaction-update) - See [Part 3](06-context-update-patterns-part3-precompaction.md)
8. [For implementation examples](#examples) - See [Part 4](06-context-update-patterns-part4-examples-troubleshooting.md)
9. [If issues occur](#troubleshooting) - See [Part 4](06-context-update-patterns-part4-examples-troubleshooting.md)

---

## Purpose

Context update patterns provide standardized workflows for common context modification scenarios. Using these patterns ensures:
- Consistent context structure
- Complete information capture
- Proper snapshot creation
- Index maintenance
- Recovery capability

---

## Update Patterns Overview

| Pattern | When to Use | Snapshot Required | Index Update |
|---------|-------------|-------------------|--------------|
| Task Switch | Changing primary focus | Yes | No |
| Decision Recording | Making important decision | No | No |
| Question Addition | Adding blocker/question | No | No |
| Progress Milestone | Completing major task | Yes | Maybe |
| Pre-Compaction | Before compaction | Yes (mandatory) | Yes |

---

## Part Files

This document serves as an index to the detailed pattern documentation:

### [Part 1: Task Switch and Decision Recording](06-context-update-patterns-part1-task-decision.md)

**Contents:**
- Pattern 1: Task Switch Update
  - When to use task switch pattern
  - Step-by-step procedure for switching tasks
  - Creating context snapshots before switching
  - Archiving old focus to Recent Decisions
  - Updating Current Focus section
  - Complete task_switch.sh example script
- Pattern 2: Decision Recording Update
  - When to use decision recording pattern
  - Documenting decisions with rationale
  - Recording alternatives considered
  - Updating affected sections
  - Complete record_decision.sh example script

### [Part 2: Question Addition and Progress Milestone](06-context-update-patterns-part2-question-milestone.md)

**Contents:**
- Pattern 3: Question Addition Update
  - When to use question addition pattern
  - Adding to Open Questions section
  - Marking blocked tasks in progress tracker
  - Complete add_question.sh example script
- Pattern 4: Progress Milestone Update
  - When to use progress milestone pattern
  - Creating context and progress snapshots
  - Updating progress tracker with completed tasks
  - Recording milestones in active context
  - Recording reusable patterns
  - Complete milestone_update.sh example script

### [Part 3: Pre-Compaction Update](06-context-update-patterns-part3-precompaction.md)

**Contents:**
- Pattern 5: Pre-Compaction Update (Mandatory)
  - When to use (always before compaction)
  - Step 1: Creating full snapshot
  - Step 2: Validating memory structure
  - Step 3: Creating pre-compaction archive
  - Step 4: Updating session info
  - Step 5: Final pre-compaction checklist
  - Complete prepare_for_compaction.sh example script

### [Part 4: Examples and Troubleshooting](06-context-update-patterns-part4-examples-troubleshooting.md)

**Contents:**
- Combined Examples
  - Example 1: Task switch with decision recording
  - Example 2: Milestone with pattern recording
- Troubleshooting
  - Problem: Forgot to create snapshot before update
  - Problem: Context update interrupted
  - Problem: Multiple updates needed simultaneously
  - Problem: Pre-compaction validation fails

---

## Quick Reference

### Pattern 1: Task Switch Update

**When to use**: Starting new task, switching focus, completing task, priority change

**Key steps**:
1. Create context snapshot
2. Archive old focus to Recent Decisions
3. Update Current Focus with new task
4. Update timestamp

**See**: [Part 1 - Task Switch and Decision Recording](06-context-update-patterns-part1-task-decision.md)

### Pattern 2: Decision Recording Update

**When to use**: Technical decisions, choosing between alternatives, establishing precedent

**Key steps**:
1. Document decision with rationale and alternatives
2. Update affected sections
3. Update timestamp

**See**: [Part 1 - Task Switch and Decision Recording](06-context-update-patterns-part1-task-decision.md)

### Pattern 3: Question Addition Update

**When to use**: Encountering blockers, needing external input, unclear requirements

**Key steps**:
1. Add to Open Questions section
2. Mark blocked tasks in progress tracker
3. Update timestamp

**See**: [Part 2 - Question Addition and Progress Milestone](06-context-update-patterns-part2-question-milestone.md)

### Pattern 4: Progress Milestone Update

**When to use**: Completing major task, reaching milestone, finishing sprint

**Key steps**:
1. Create context and progress snapshots
2. Update progress tracker
3. Update active context with milestone
4. Record pattern if reusable

**See**: [Part 2 - Question Addition and Progress Milestone](06-context-update-patterns-part2-question-milestone.md)

### Pattern 5: Pre-Compaction Update

**When to use**: MANDATORY before every compaction

**Key steps**:
1. Create full snapshot
2. Validate memory structure
3. Create pre-compaction archive
4. Update session info
5. Complete final checklist

**See**: [Part 3 - Pre-Compaction Update](06-context-update-patterns-part3-precompaction.md)

---

## Troubleshooting Quick Links

| Problem | Solution Location |
|---------|-------------------|
| Forgot to create snapshot | [Part 4](06-context-update-patterns-part4-examples-troubleshooting.md#problem-forgot-to-create-snapshot-before-update) |
| Context update interrupted | [Part 4](06-context-update-patterns-part4-examples-troubleshooting.md#problem-context-update-interrupted) |
| Multiple updates needed | [Part 4](06-context-update-patterns-part4-examples-troubleshooting.md#problem-multiple-updates-needed-simultaneously) |
| Pre-compaction validation fails | [Part 4](06-context-update-patterns-part4-examples-troubleshooting.md#problem-pre-compaction-validation-fails) |
