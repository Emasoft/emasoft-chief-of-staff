# Task Completion Checklist (Chief of Staff Agent)

## Before Reporting Task Complete

## Table of Contents

1. [Before Reporting Task Complete](#before-reporting-task-complete)
   - 1.1 [Acceptance Criteria Met](#1-acceptance-criteria-met)
   - 1.2 [Quality Gates Passed](#2-quality-gates-passed)
   - 1.3 [Memory Management Verification](#3-memory-management-verification)
   - 1.4 [Documentation Updated](#4-documentation-updated)
   - 1.5 [Handoff Prepared](#5-handoff-prepared)
   - 1.6 [GitHub Updated (if applicable)](#6-github-updated-if-applicable)
   - 1.7 [Session Memory Updated](#7-session-memory-updated)
2. [Verification Loop](#verification-loop)

---


STOP and verify ALL of the following:

### 1. Acceptance Criteria Met
- [ ] ALL acceptance criteria from task definition satisfied
- [ ] Evidence documented for each criterion
- [ ] No "partial" or "mostly" completions
- [ ] Memory state consistent and validated

### 2. Quality Gates Passed
- [ ] Linting passed (ruff check, eslint)
- [ ] Type checking passed (mypy, pyright)
- [ ] Tests pass (pytest, jest)
- [ ] No regressions introduced
- [ ] Memory validation scripts pass

### 3. Memory Management Verification
- [ ] Session memory files are consistent
- [ ] activeContext.md reflects current state accurately
- [ ] progress.md has all task entries
- [ ] patterns.md captures new learnings
- [ ] No orphaned or stale memory entries
- [ ] Pre-compaction backup created (if applicable)
- [ ] Config snapshots current

### 4. Documentation Updated
- [ ] Code comments explain WHY (not just what)
- [ ] README updated if behavior changed
- [ ] CHANGELOG entry added (if applicable)
- [ ] Memory structure documentation current

### 5. Handoff Prepared
- [ ] Handoff document written to docs_dev/handoffs/
- [ ] Next steps clearly defined
- [ ] AI Maestro message queued
- [ ] Context state documented for session resumption

### 6. GitHub Updated (if applicable)
- [ ] PR created/updated with description
- [ ] Issue comments added with progress
- [ ] Labels updated to reflect status
- [ ] Projects board item moved

### 7. Session Memory Updated
- [ ] activeContext.md reflects completed work
- [ ] progress.md has completion entry
- [ ] patterns.md captures any new learnings
- [ ] Timestamps are current and accurate

## Verification Loop

Before marking complete, ask yourself:

1. "If I was a different agent reading this, would I know what was done?"
2. "Is there any ambiguity about what 'done' means?"
3. "Did I actually test this, or am I assuming it works?"
4. "Are there edge cases I didn't handle?"
5. "If this session ends now, can the next session resume seamlessly?"
6. "Is the memory state recoverable if something goes wrong?"

If ANY answer is uncertain, the task is NOT complete. Continue work.

## Common Traps (Memory Manager-Specific)

| Trap | Reality |
|------|---------|
| "File saved" | Does NOT equal "content correct" |
| "Memory updated" | Does NOT equal "memory consistent" |
| "Backup created" | Does NOT equal "backup verified" |
| "Context written" | Does NOT equal "context complete" |
| "Timestamps updated" | Does NOT equal "timestamps accurate" |
| "Tests compile" | Does NOT equal "tests pass" |
| "Should work" | Does NOT equal "verified working" |
| "Almost done" | Does NOT equal "done" |

## Completion Report Format

When reporting completion:

```yaml
status: COMPLETE
task_id: <uuid>
summary: <1-2 sentences>
evidence:
  - <what proves it's done>
  - <validation script output>
  - <memory state verification>
files_changed:
  - <path:lines>
memory_state:
  activeContext: <last_updated timestamp>
  progress: <task_count, completed_count>
  patterns: <new_patterns_added>
  backup_location: <path if applicable>
next_steps: <what happens next>
handoff: <path to handoff doc>
session_resumption:
  - read: <files needed to resume>
  - context: <key state to restore>
```

## Pre-Completion Checklist for Memory Managers

Before declaring ANY memory task complete:

1. **Validate file integrity** - Run validation scripts
2. **Check timestamps** - Are all timestamps current and consistent?
3. **Verify cross-references** - Do files reference each other correctly?
4. **Test recovery** - Can the session be resumed from memory state?
5. **Create backups** - Before any destructive operation
6. **Document state** - Clear picture of current memory contents
7. **Prepare handoff** - Include exact files to read on resume

## Memory-Specific Verification

### File Consistency
- [ ] All required memory files exist
- [ ] File formats are valid (YAML, JSON, Markdown)
- [ ] No syntax errors in structured files
- [ ] Cross-file references resolve correctly
- [ ] No duplicate or conflicting entries

### Session State
- [ ] activeContext.md reflects true current state
- [ ] In-progress tasks have accurate status
- [ ] Completed tasks are marked and dated
- [ ] Blocked tasks have documented reasons
- [ ] Dependencies are correctly linked

### Backup and Recovery
- [ ] Pre-compaction backups exist (if compaction happened)
- [ ] Config snapshots are current
- [ ] Recovery procedure documented
- [ ] Archive location documented

### Handoff Readiness
- [ ] Next agent can understand state by reading memory
- [ ] No implicit knowledge required
- [ ] All context is explicit and documented
- [ ] Resume instructions are clear

## When to Escalate vs Complete

| Situation | Action |
|-----------|--------|
| All criteria met, verified | Mark COMPLETE |
| 1+ criteria unmet but fixable | Continue work, do NOT mark complete |
| Memory corruption detected | Mark BLOCKED, initiate recovery |
| Inconsistent state | Mark BLOCKED, reconcile before proceeding |
| Missing required files | Mark BLOCKED, recreate or recover |
| Compaction needed | Mark WAITING, prepare then compact |
