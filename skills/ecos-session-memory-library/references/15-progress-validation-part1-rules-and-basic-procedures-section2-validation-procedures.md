# Progress Validation - Section 2: Validation Procedures

## Table of Contents

1. [PROCEDURE 1: Validate Task Status](#procedure-1-validate-task-status)
2. [PROCEDURE 2: Validate Dependencies](#procedure-2-validate-dependencies)
3. [PROCEDURE 3: Validate Timestamps](#procedure-3-validate-timestamps)

**Parent document:** [Part 1: Rules and Basic Procedures](15-progress-validation-part1-rules-and-basic-procedures.md)

---

## PROCEDURE 1: Validate Task Status

**When to use:**
- After updating task status
- At session initialization
- Before context compaction

**Steps:**

1. **Extract all tasks from progress.md**
   ```bash
   # Extract todo tasks
   todo_tasks=$(sed -n '/## Todo List/,/## /p' design/memory/progress.md | grep '- \[')

   # Extract completed tasks
   completed_tasks=$(sed -n '/## Completed Tasks/,/## /p' design/memory/progress.md | grep '- \[x\]')

   # Extract blocked tasks
   blocked_tasks=$(sed -n '/## Blocked Tasks/,/## /p' design/memory/progress.md | grep '- \[!\]')
   ```

2. **Check for duplicate task names**
   ```python
   def check_duplicates(tasks):
       task_names = {}
       for task in tasks:
           name = extract_task_name(task)
           if name in task_names:
               print(f"ERROR: Duplicate task '{name}'")
               print(f"  First occurrence: {task_names[name]}")
               print(f"  Second occurrence: {task}")
               return False
           task_names[name] = task
       return True
   ```

3. **Check for contradictory statuses**
   ```python
   # Task marked both incomplete and complete
   for task in extract_all_tasks(progress_md):
       is_todo = task in todo_section
       is_complete = task in completed_section

       if is_todo and is_complete:
           print(f"ERROR: Task '{task}' is both pending and completed")
           return False
   ```

4. **Verify status markers are correct**
   ```python
   # Todo tasks should have [ ]
   for task in todo_section:
       if not task.startswith('- [ ]'):
           print(f"ERROR: Todo task has wrong marker: {task}")

   # Completed tasks should have [x]
   for task in completed_section:
       if not task.startswith('- [x]'):
           print(f"ERROR: Completed task has wrong marker: {task}")
   ```

5. **Report validation results**
   ```markdown
   ## Task Status Validation Report

   **Total Tasks:** 15
   **Todo:** 8
   **In Progress:** 2
   **Completed:** 4
   **Blocked:** 1

   **Validation Results:**
   - No duplicate tasks found
   - No contradictory statuses
   - All status markers correct
   - Found 1 issue: Task "Add tests" marked complete but no completion timestamp
   ```

---

## PROCEDURE 2: Validate Dependencies

**When to use:**
- After adding task dependencies
- After completing a task that unblocks others
- Before starting a blocked task

**Steps:**

1. **Extract dependency relationships**
   ```python
   def extract_dependencies(progress_md):
       deps = {}
       for task in extract_all_tasks(progress_md):
           task_name = extract_task_name(task)
           task_deps = extract_task_dependencies(task)
           deps[task_name] = task_deps
       return deps
   ```

2. **Check all dependencies exist**
   ```python
   task_names = set(deps.keys())

   for task, dependencies in deps.items():
       for dep in dependencies:
           if dep not in task_names:
               print(f"ERROR: Task '{task}' depends on non-existent task '{dep}'")
               return False
   ```

3. **Check for circular dependencies**
   ```python
   def has_cycle(deps):
       visited = set()
       recursion_stack = set()

       def visit(task):
           if task in recursion_stack:
               print(f"ERROR: Circular dependency detected at '{task}'")
               return True
           if task in visited:
               return False

           visited.add(task)
           recursion_stack.add(task)

           for dep in deps.get(task, []):
               if visit(dep):
                   return True

           recursion_stack.remove(task)
           return False

       for task in deps:
           if visit(task):
               return True
       return False
   ```

4. **Check blocked tasks have documented blockers**
   ```python
   blocked_tasks = extract_blocked_tasks(progress_md)

   for task in blocked_tasks:
       blocker = extract_blocker(task)
       if not blocker:
           print(f"ERROR: Blocked task '{task}' has no documented blocker")
           return False
   ```

5. **Check unblocked tasks are moved to todo**
   ```python
   for task in blocked_tasks:
       blocker = extract_blocker(task)
       blocker_status = get_task_status(blocker)

       if blocker_status == 'completed':
           print(f"WARNING: Task '{task}' is blocked by completed task '{blocker}'")
           print(f"  Should be moved to Todo List")
   ```

6. **Generate dependency graph**
   ```markdown
   ## Dependency Validation Report

   **Dependency Graph:**
   ```
   Task A
   +-- depends on Task B (exists, completed)
   +-- depends on Task C (exists, still pending)

   Task D
   +-- depends on Task A (exists, still pending)
   ```

   **Validation Results:**
   - All dependencies exist
   - No circular dependencies
   - All blocked tasks have documented blockers
   - 2 tasks can be unblocked (blockers completed)
   ```

---

## PROCEDURE 3: Validate Timestamps

**When to use:**
- After recording task completion
- After importing tasks from external source
- When timestamps seem incorrect

**Steps:**

1. **Extract all timestamps**
   ```python
   import re
   from datetime import datetime

   def extract_timestamps(progress_md):
       # Match ISO 8601 timestamps
       pattern = r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}'
       timestamps = re.findall(pattern, progress_md)
       return timestamps
   ```

2. **Validate timestamp format**
   ```python
   for ts in timestamps:
       try:
           dt = datetime.fromisoformat(ts.replace(' ', 'T'))
       except ValueError:
           print(f"ERROR: Invalid timestamp format: {ts}")
           return False
   ```

3. **Check chronological order for completed tasks**
   ```python
   completed = extract_completed_tasks_with_timestamps(progress_md)

   prev_time = None
   for task, timestamp in completed:
       current_time = datetime.fromisoformat(timestamp)

       if prev_time and current_time < prev_time:
           print(f"ERROR: Task '{task}' completed at {timestamp}")
           print(f"  But previous task completed at {prev_time}")
           print(f"  Completed tasks should be in chronological order")
           return False

       prev_time = current_time
   ```

4. **Check for future timestamps**
   ```python
   now = datetime.now()

   for task, timestamp in extract_all_tasks_with_timestamps(progress_md):
       task_time = datetime.fromisoformat(timestamp)

       if task_time > now:
           print(f"ERROR: Task '{task}' has future timestamp: {timestamp}")
           return False
   ```

5. **Check for unreasonably old timestamps**
   ```python
   from datetime import timedelta

   for task, timestamp in extract_all_tasks_with_timestamps(progress_md):
       task_time = datetime.fromisoformat(timestamp)
       age = now - task_time

       if age > timedelta(days=365):
           print(f"WARNING: Task '{task}' timestamp is over 1 year old: {timestamp}")
   ```

6. **Report validation results**
   ```markdown
   ## Timestamp Validation Report

   **Total Timestamps:** 25
   **Valid Format:** 25
   **Invalid Format:** 0

   **Ordering:**
   - Completed tasks in chronological order
   - No future timestamps
   - 2 tasks have timestamps over 6 months old (consider archiving)
   ```

---

**Version:** 1.0
**Last Updated:** 2026-01-08
**Target Audience:** Chief of Staff Agents
