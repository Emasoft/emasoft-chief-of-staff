---
procedure: support-skill
workflow-instruction: support
operation: recover-session
parent-skill: ecos-session-memory-library
---

# Operation: Recover Session After Interruption


## Contents

- [Purpose](#purpose)
- [When To Use This Operation](#when-to-use-this-operation)
- [Steps](#steps)
  - [Step 1: Load All Memory Files](#step-1-load-all-memory-files)
  - [Step 2: Read activeContext.md for Work State](#step-2-read-activecontextmd-for-work-state)
- [Recovery: Current State](#recovery-current-state)
  - [Step 3: Read progress.md for Task State](#step-3-read-progressmd-for-task-state)
- [Recovery: Task State](#recovery-task-state)
  - [Step 4: Validate Memory Consistency](#step-4-validate-memory-consistency)
- [Recovery: Validation](#recovery-validation)
  - [Step 5: Ask User to Confirm Resumption](#step-5-ask-user-to-confirm-resumption)
- [Session Recovery Summary](#session-recovery-summary)
  - [State to Resume](#state-to-resume)
  - [Shall I resume from this state?](#shall-i-resume-from-this-state)
  - [Step 6: Update Session Start](#step-6-update-session-start)
- [Session Notes](#session-notes)
- [Recovery Scenarios](#recovery-scenarios)
  - [Scenario 1: Clean Resume (< 24 hours)](#scenario-1-clean-resume-24-hours)
  - [Scenario 2: Long Gap (> 24 hours)](#scenario-2-long-gap-24-hours)
  - [Scenario 3: Corrupted Files](#scenario-3-corrupted-files)
- [Checklist](#checklist)
- [Output](#output)
- [Related References](#related-references)
- [Next Operation](#next-operation)

## Purpose

Restore session state after unexpected termination, manual interruption, or long breaks.

## When To Use This Operation

- After unexpected termination
- After manual interruption (Ctrl+C)
- After long breaks (hours or days)
- After context compaction
- When resuming work after any gap

## Steps

### Step 1: Load All Memory Files

```bash
MEMORY_DIR="$CLAUDE_PROJECT_DIR/design/memory"

# Check files exist
ls -la "$MEMORY_DIR"/*.md

# Read each file
cat "$MEMORY_DIR/activeContext.md"
cat "$MEMORY_DIR/patterns.md"
cat "$MEMORY_DIR/progress.md"
```

### Step 2: Read activeContext.md for Work State

Extract current state:

```markdown
## Recovery: Current State

From activeContext.md:
- Active Task: [task from file]
- Working On: [description]
- Open Questions: [list]
- Recent Decisions: [list]
```

### Step 3: Read progress.md for Task State

Extract task status:

```markdown
## Recovery: Task State

Active Tasks: [count]
- [list of active tasks]

Blocked Tasks: [count]
- [list and blockers]

Recently Completed: [last few]
```

### Step 4: Validate Memory Consistency

Check for issues:
- activeContext references tasks that exist in progress.md
- No stale data (timestamps reasonable)
- No corrupted sections

```markdown
## Recovery: Validation

- Context-Progress alignment: [OK/ISSUE]
- Timestamps valid: [OK/ISSUE]
- File integrity: [OK/ISSUE]
```

### Step 5: Ask User to Confirm Resumption

Present state and ask for confirmation:

```markdown
## Session Recovery Summary

Last session: [timestamp from activeContext]
Time since last activity: [calculated]

### State to Resume
- Active task: [task]
- Progress: [description]
- Open questions: [count]

### Shall I resume from this state?
1. Yes, continue where I left off
2. No, let me review the state first
3. Start fresh (discard memory)
```

### Step 6: Update Session Start

Once confirmed, update activeContext:

```markdown
## Session Notes
- Resumed session at [ISO8601]
- Previous session ended: [timestamp]
- Gap duration: [hours/days]
```

## Recovery Scenarios

### Scenario 1: Clean Resume (< 24 hours)

1. Load files
2. Verify state
3. Brief summary
4. Continue work

### Scenario 2: Long Gap (> 24 hours)

1. Load files
2. Full state review
3. Check for stale blockers
4. Verify tasks still relevant
5. Update context before continuing

### Scenario 3: Corrupted Files

1. Detect corruption
2. Attempt repair from backups
3. If no backup, recreate structure
4. Document lost information
5. Notify user

## Checklist

Copy this checklist and track your progress:

- [ ] Memory directory located
- [ ] activeContext.md loaded
- [ ] patterns.md loaded
- [ ] progress.md loaded
- [ ] Current state extracted
- [ ] Task state extracted
- [ ] Consistency validated
- [ ] User confirmation requested
- [ ] Session start updated
- [ ] Ready to resume work

## Output

After completing this operation:
- Session state restored
- User aware of current state
- Ready to continue work

## Related References

- [10-recovery-procedures.md](10-recovery-procedures.md) - Complete recovery guide
- [13-file-recovery.md](13-file-recovery.md) - Corrupted file recovery
- [14-context-sync.md](14-context-sync.md) - Context synchronization

## Next Operation

After recovery: [op-update-active-context.md](op-update-active-context.md) to record session resume
