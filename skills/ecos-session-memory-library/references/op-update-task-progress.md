---
procedure: support-skill
workflow-instruction: support
operation: update-task-progress
parent-skill: ecos-session-memory-library
---

# Operation: Update Task Progress


## Contents

- [Purpose](#purpose)
- [When To Use This Operation](#when-to-use-this-operation)
- [Task States](#task-states)
- [Steps](#steps)
  - [Step 1: Identify Changed Task](#step-1-identify-changed-task)
  - [Step 2: Open progress.md](#step-2-open-progressmd)
  - [Step 3: Update Task Status](#step-3-update-task-status)
- [Completed Tasks](#completed-tasks)
- [Blocked Tasks](#blocked-tasks)
- [Active Tasks](#active-tasks)
  - [Step 4: Document Blockers (if any)](#step-4-document-blockers-if-any)
  - [Step 5: Update Dependencies](#step-5-update-dependencies)
- [Active Tasks](#active-tasks)
  - [Step 6: Update Timestamp](#step-6-update-timestamp)
- [Checklist](#checklist)
- [Progress File Structure](#progress-file-structure)
- [Active Tasks](#active-tasks)
- [Completed Tasks](#completed-tasks)
- [Blocked Tasks](#blocked-tasks)
- [Paused Tasks](#paused-tasks)
- [Output](#output)
- [Related References](#related-references)
- [Next Operation](#next-operation)

## Purpose

Track task status changes, completions, blockers, and dependencies in progress.md.

## When To Use This Operation

- When a task completes
- When task status changes
- When a task becomes blocked
- When dependencies resolve
- When new tasks are assigned

## Task States

| State | Symbol | Description |
|-------|--------|-------------|
| Active | `[ ]` | In progress |
| Completed | `[x]` | Done |
| Blocked | `[B]` | Waiting on something |
| Paused | `[P]` | Temporarily stopped |

## Steps

### Step 1: Identify Changed Task

Determine which task needs updating:
- Task ID
- New status
- Reason for change

### Step 2: Open progress.md

```bash
PROGRESS_FILE="$CLAUDE_PROJECT_DIR/design/memory/progress.md"
```

### Step 3: Update Task Status

**Mark Task Complete:**
```markdown
## Completed Tasks
- [x] TASK-041: Implement login endpoint
  - Completed: 2025-02-05T14:00:00Z
  - Duration: 3.5 hours
  - Notes: Passed code review first attempt
```

**Mark Task Blocked:**
```markdown
## Blocked Tasks
- [B] TASK-042: Implement logout endpoint
  - Blocked: 2025-02-05T15:00:00Z
  - Blocker: Waiting for auth token format decision
  - Blocked by: Design review pending
  - Impact: Cannot proceed until resolved
```

**Add New Task:**
```markdown
## Active Tasks
- [ ] TASK-043: Implement password reset
  - Assigned: 2025-02-05T15:30:00Z
  - Estimate: 4 hours
  - Dependencies: TASK-042 (logout)
```

### Step 4: Document Blockers (if any)

If task is blocked, include:
- What is blocking
- Who/what can unblock
- Impact on other tasks
- Escalation if needed

### Step 5: Update Dependencies

If a dependency resolves:
```markdown
## Active Tasks
- [ ] TASK-043: Implement password reset
  - Dependencies: ~~TASK-042~~ (resolved)
  - Can now proceed: Yes
```

### Step 6: Update Timestamp

```markdown
# Task Progress

Last Updated: 2025-02-05T15:30:00Z
```

## Checklist

Copy this checklist and track your progress:

- [ ] Task identified
- [ ] New status determined
- [ ] Progress file updated
- [ ] Timestamp added to change
- [ ] Blockers documented (if blocked)
- [ ] Dependencies updated (if relevant)
- [ ] File timestamp updated

## Progress File Structure

```markdown
# Task Progress

Last Updated: [ISO8601]

## Active Tasks
- [ ] TASK-001: [description]
  - Assigned: [timestamp]
  - Estimate: [hours]
  - Progress: [percentage or description]

## Completed Tasks
- [x] TASK-000: [description]
  - Completed: [timestamp]
  - Duration: [actual hours]
  - Notes: [any notes]

## Blocked Tasks
- [B] TASK-002: [description]
  - Blocked: [timestamp]
  - Blocker: [what is blocking]
  - Impact: [what is affected]

## Paused Tasks
- [P] TASK-003: [description]
  - Paused: [timestamp]
  - Reason: [why paused]
  - Resume: [when to resume]
```

## Output

After completing this operation:
- Task status updated in progress.md
- Blockers documented
- Dependencies tracked
- Ready for reporting

## Related References

- [08-manage-progress-tracking.md](08-manage-progress-tracking.md) - Complete progress tracking guide
- [09-task-dependencies.md](09-task-dependencies.md) - Dependency management

## Next Operation

Related operations:
- [op-update-active-context.md](op-update-active-context.md) - Update context if task changed
- [op-prepare-context-compaction.md](op-prepare-context-compaction.md) - Before compaction
