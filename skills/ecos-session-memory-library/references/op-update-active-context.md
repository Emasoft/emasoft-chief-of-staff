---
procedure: support-skill
workflow-instruction: support
operation: update-active-context
parent-skill: ecos-session-memory-library
---

# Operation: Update Active Context


## Contents

- [Purpose](#purpose)
- [When To Use This Operation](#when-to-use-this-operation)
- [Update Triggers](#update-triggers)
- [Steps](#steps)
  - [Step 1: Identify What Changed](#step-1-identify-what-changed)
  - [Step 2: Open activeContext.md](#step-2-open-activecontextmd)
  - [Step 3: Update Relevant Section](#step-3-update-relevant-section)
- [Current Focus](#current-focus)
- [Recent Decisions](#recent-decisions)
- [Open Questions](#open-questions)
- [Session Notes](#session-notes)
  - [Step 4: Write Changes Immediately](#step-4-write-changes-immediately)
  - [Step 5: Update Timestamp](#step-5-update-timestamp)
- [Checklist](#checklist)
- [Update Patterns](#update-patterns)
  - [Pattern 1: Task Switch](#pattern-1-task-switch)
- [Current Focus](#current-focus)
  - [Pattern 2: Decision Recording](#pattern-2-decision-recording)
- [Recent Decisions](#recent-decisions)
  - [Pattern 3: Pre-Compaction Update](#pattern-3-pre-compaction-update)
- [Output](#output)
- [Related References](#related-references)
- [Next Operation](#next-operation)

## Purpose

Keep activeContext.md current with the agent's focus, decisions, and work state.

## When To Use This Operation

- When shifting focus to a new task
- When making significant decisions
- When entering or exiting dialogs
- Before context compaction
- At regular intervals during long operations

## Update Triggers

| Trigger | Update Section | Priority |
|---------|----------------|----------|
| Task switch | Current Focus | High |
| Decision made | Recent Decisions | High |
| Question arises | Open Questions | Medium |
| Note to remember | Session Notes | Medium |
| Approaching compaction | All sections | High |

## Steps

### Step 1: Identify What Changed

Determine which section needs updating:
- Current Focus: Active task, working location
- Open Questions: Unanswered questions
- Recent Decisions: Choices made
- Session Notes: Important information

### Step 2: Open activeContext.md

```bash
CONTEXT_FILE="$CLAUDE_PROJECT_DIR/design/memory/activeContext.md"
```

### Step 3: Update Relevant Section

**Task Switch Update:**
```markdown
## Current Focus
- **Active Task:** TASK-042 (Implement logout endpoint)
- **Previous Task:** TASK-041 (paused - waiting for review)
- **Working On:** Writing endpoint handler
- **Timestamp:** 2025-02-05T14:30:00Z
```

**Decision Recording Update:**
```markdown
## Recent Decisions
- [2025-02-05T14:30:00Z] Decided to use JWT tokens for session management
  - Reason: Better scalability, stateless
  - Alternative considered: Server-side sessions
```

**Question Addition Update:**
```markdown
## Open Questions
- [ ] Should logout invalidate all sessions or just current?
- [ ] What is the token expiry policy?
```

**Session Note Update:**
```markdown
## Session Notes
- User prefers explicit error messages over generic ones
- Project uses UTC timestamps everywhere
```

### Step 4: Write Changes Immediately

Do not batch updates. Write to disk after each change:

```bash
# After editing, verify file was written
ls -la "$CONTEXT_FILE"
```

### Step 5: Update Timestamp

Always update the "Last Updated" timestamp at the top:

```markdown
# Active Context

Last Updated: 2025-02-05T14:30:00Z
Session ID: session-20250205-1
```

## Checklist

Copy this checklist and track your progress:

- [ ] Change identified
- [ ] Appropriate section selected
- [ ] Update written with timestamp
- [ ] File saved to disk
- [ ] Last Updated timestamp refreshed

## Update Patterns

### Pattern 1: Task Switch

```markdown
## Current Focus
- **Active Task:** [new-task-id] ([description])
- **Previous Task:** [old-task-id] ([status: paused/completed])
- **Timestamp:** [ISO8601]
```

### Pattern 2: Decision Recording

```markdown
## Recent Decisions
- [ISO8601] [Decision statement]
  - Reason: [why this choice]
  - Alternative: [what was not chosen]
```

### Pattern 3: Pre-Compaction Update

Before compaction, ensure all sections are current:
- Current Focus reflects actual state
- All recent decisions documented
- Open questions listed
- Session notes captured

## Output

After completing this operation:
- activeContext.md reflects current state
- Changes persisted to disk
- Ready to survive context compaction

## Related References

- [03-manage-active-context.md](03-manage-active-context.md) - Complete context management guide
- [06-context-update-patterns.md](06-context-update-patterns.md) - Update pattern details

## Next Operation

Related operations:
- [op-record-discovered-pattern.md](op-record-discovered-pattern.md) - When patterns found
- [op-update-task-progress.md](op-update-task-progress.md) - When task status changes
