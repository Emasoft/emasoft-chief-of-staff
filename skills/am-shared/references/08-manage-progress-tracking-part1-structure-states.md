# Progress Tracking: Structure and States

## Table of Contents
1. [Progress Tracker Structure](#progress-tracker-structure)
2. [File Location](#file-location)
3. [Standard Structure Template](#standard-structure)
4. [Task States](#task-states)
5. [State Transitions](#state-transitions)

---

## Progress Tracker Structure

### File Location
`.session_memory/progress_tracker.md`

### Standard Structure

```markdown
# Progress Tracker

**Last Updated**: 2026-01-01 14:30 UTC
**Active Tasks**: 3
**Completed Tasks**: 12
**Blocked Tasks**: 1

---

## Active Tasks

- [ ] Task 1 - Brief description
  - **Priority**: High/Medium/Low
  - **Started**: 2026-01-01 10:00 UTC
  - **Estimated Completion**: 2026-01-01 16:00 UTC
  - **Dependencies**: None
  - **Progress**: 60%
  - **Status**: In progress

- [ ] Task 2 - Brief description
  - **Priority**: Medium
  - **Started**: 2026-01-01 11:00 UTC
  - **Dependencies**: Task 1
  - **Progress**: 20%
  - **Status**: Waiting for dependency

---

## Completed Tasks

- [x] Task 0 - Brief description
  - **Started**: 2026-01-01 08:00 UTC
  - **Completed**: 2026-01-01 10:00 UTC
  - **Duration**: 2 hours
  - **Outcome**: Successfully implemented
  - **Learnings**: Key insight 1, Key insight 2

---

## Blocked Tasks

- [ ] Task 3 - Brief description
  - **Priority**: High
  - **Blocked By**: Open question Q1
  - **Blocking Since**: 2026-01-01 12:00 UTC
  - **Impact**: Cannot proceed with Task 4

---

## Task Dependencies

```
Task 1 (active)
  └─> Task 2 (waiting)
      └─> Task 4 (planned)

Task 3 (blocked by Q1)
  └─> Task 5 (planned)
```

---

## Milestones

### Milestone 1: Authentication System
**Target**: 2026-01-05
**Progress**: 75%
**Tasks**:
- [x] OAuth setup
- [x] JWT implementation
- [ ] Role management
- [ ] Integration tests

---

## Future Tasks

- [ ] Task 6 - Brief description (Planned)
- [ ] Task 7 - Brief description (Planned)
```

---

## Task States

### State Definitions

| State | Checkbox | Meaning | Location |
|-------|----------|---------|----------|
| Active | `- [ ]` | Currently being worked on | Active Tasks |
| Completed | `- [x]` | Finished successfully | Completed Tasks |
| Blocked | `- [ ]` | Cannot proceed due to blocker | Blocked Tasks |
| Planned | `- [ ]` | Not yet started | Future Tasks |

### State Transitions

```
Planned → Active
  Trigger: Start working on task

Active → Completed
  Trigger: Task finished successfully

Active → Blocked
  Trigger: Hit blocker or dependency

Blocked → Active
  Trigger: Blocker resolved

Blocked → Completed
  Trigger: Blocker resolved and task finished
```

---

**Next**: See [Part 2: Task Management Procedures](./08-manage-progress-tracking-part2-task-management.md) for how to manage tasks through their lifecycle.
