# Progress Validation - Section 1: Validation Rules

## Table of Contents

1. [Rule 1: Task Status Integrity](#rule-1-task-status-integrity)
2. [Rule 2: Dependency Validity](#rule-2-dependency-validity)
3. [Rule 3: Timestamp Ordering](#rule-3-timestamp-ordering)
4. [Rule 4: Progress Consistency](#rule-4-progress-consistency)
5. [Rule 5: Completeness Requirements](#rule-5-completeness-requirements)

**Parent document:** [Part 1: Rules and Basic Procedures](15-progress-validation-part1-rules-and-basic-procedures.md)

---

## Rule 1: Task Status Integrity

**Rule:** A task can be in exactly one state at a time.

**Valid states:**
- Pending (in Todo List, not started)
- In Progress (actively being worked on)
- Completed (in Completed Tasks)
- Blocked (in Blocked Tasks with blocker documented)
- Cancelled (in Cancelled Tasks with reason)

**Invalid:**
- Task appears in both Todo List and Completed Tasks
- Task appears in multiple sections
- Task has contradictory status markers

**Validation check:**
```python
def validate_task_status(progress_md):
    tasks = extract_all_tasks(progress_md)
    task_names = {}

    for task in tasks:
        if task.name in task_names:
            print(f"ERROR: Task '{task.name}' appears in multiple states:")
            print(f"  - {task_names[task.name]}")
            print(f"  - {task.status}")
            return False
        task_names[task.name] = task.status

    return True
```

---

## Rule 2: Dependency Validity

**Rule:** All task dependencies must reference existing tasks.

**Valid:**
- Task A depends on Task B, and Task B exists in progress.md
- Task dependencies form a directed acyclic graph (no cycles)
- Blocked tasks have documented blockers

**Invalid:**
- Task A depends on Task B, but Task B does not exist
- Task A depends on Task B, Task B depends on Task A (cycle)
- Task is marked as blocked but no blocker documented

**Validation check:**
```python
def validate_dependencies(progress_md):
    tasks = extract_all_tasks(progress_md)
    task_names = set(task.name for task in tasks)

    for task in tasks:
        for dependency in task.dependencies:
            if dependency not in task_names:
                print(f"ERROR: Task '{task.name}' depends on non-existent task '{dependency}'")
                return False

    # Check for cycles
    if has_circular_dependency(tasks):
        print("ERROR: Circular dependency detected")
        return False

    return True
```

---

## Rule 3: Timestamp Ordering

**Rule:** Timestamps must be in chronological order.

**Valid:**
- Task created_at < completed_at
- Tasks completed in chronological order in Completed Tasks section
- Timestamps are valid ISO 8601 format

**Invalid:**
- Task completed_at < created_at (completed before created)
- Tasks in Completed Tasks are out of chronological order
- Timestamp format is invalid or unparseable

**Validation check:**
```python
from datetime import datetime

def validate_timestamps(progress_md):
    tasks = extract_completed_tasks(progress_md)

    prev_timestamp = None
    for task in tasks:
        # Validate format
        try:
            completed = datetime.fromisoformat(task.completed_at)
        except ValueError:
            print(f"ERROR: Task '{task.name}' has invalid timestamp: {task.completed_at}")
            return False

        # Validate ordering
        if prev_timestamp and completed < prev_timestamp:
            print(f"ERROR: Task '{task.name}' completed before previous task")
            return False

        prev_timestamp = completed

    return True
```

---

## Rule 4: Progress Consistency

**Rule:** Overall progress must be consistent with individual task states.

**Valid:**
- Total tasks = pending + in_progress + completed + blocked + cancelled
- Percentage complete = (completed / total) * 100
- Blocked count matches number of tasks with blockers

**Invalid:**
- Numbers don't add up
- Percentage complete doesn't match actual completion ratio
- Claimed progress contradicts task states

**Validation check:**
```python
def validate_progress_consistency(progress_md):
    counts = count_tasks_by_status(progress_md)

    total = counts['pending'] + counts['in_progress'] + counts['completed'] + counts['blocked'] + counts['cancelled']

    if counts['total'] != total:
        print(f"ERROR: Total tasks ({counts['total']}) != sum of states ({total})")
        return False

    expected_pct = (counts['completed'] / total) * 100
    if abs(counts['progress_pct'] - expected_pct) > 1.0:
        print(f"ERROR: Progress percentage ({counts['progress_pct']}%) != calculated ({expected_pct}%)")
        return False

    return True
```

---

## Rule 5: Completeness Requirements

**Rule:** Completed tasks must have all required information.

**Required for completed tasks:**
- Task name
- Completion timestamp (valid ISO 8601)
- Brief completion note (what was done)

**Required for blocked tasks:**
- Task name
- Blocker description
- Blocking timestamp

**Required for cancelled tasks:**
- Task name
- Cancellation reason
- Cancellation timestamp

**Validation check:**
```python
def validate_completeness(progress_md):
    completed = extract_completed_tasks(progress_md)

    for task in completed:
        if not task.name:
            print("ERROR: Completed task has no name")
            return False
        if not task.completed_at:
            print(f"ERROR: Task '{task.name}' has no completion timestamp")
            return False
        if not task.completion_note:
            print(f"ERROR: Task '{task.name}' has no completion note")
            return False

    return True
```

---

**Version:** 1.0
**Last Updated:** 2026-01-08
**Target Audience:** Chief of Staff Agents
