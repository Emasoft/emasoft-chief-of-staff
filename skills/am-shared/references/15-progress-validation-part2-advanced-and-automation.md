# Progress Validation - Part 2: Advanced Validation and Automation

## Table of Contents

1. [Advanced validation procedures](#advanced-validation-procedures)
   - 1.1 [Validating consistency](#procedure-4-validate-consistency)
   - 1.2 [Validating completeness](#procedure-5-validate-completeness)
2. [Common validation errors](#common-validation-errors)
   - 2.1 [Task in Multiple States](#error-1-task-in-multiple-states)
   - 2.2 [Non-existent Dependency](#error-2-non-existent-dependency)
   - 2.3 [Timestamp Out of Order](#error-3-timestamp-out-of-order)
   - 2.4 [Missing Completion Timestamp](#error-4-missing-completion-timestamp)
3. [Automated validation](#automated-validation)
   - 3.1 [Validation Script](#validation-script)
   - 3.2 [Script Usage](#usage)
4. [For implementation examples](#examples)
   - 4.1 [Validating After Task Completion](#example-1-validating-after-task-completion)
5. [If issues occur](#troubleshooting)
   - 5.1 [Script reports errors but file looks correct](#issue-validation-script-reports-errors-but-file-looks-correct)
   - 5.2 [Many validation errors after importing tasks](#issue-many-validation-errors-after-importing-tasks)

**Related files:**
- [Part 1: Rules and Basic Procedures](15-progress-validation-part1-rules-and-basic-procedures.md) - Overview, validation rules, basic procedures

---

## Advanced Validation Procedures

### PROCEDURE 4: Validate Consistency

**When to use:**
- After major progress updates
- Before reporting status to user or orchestrator
- At session termination

**Steps:**

1. **Count tasks by status**
   ```python
   counts = {
       'pending': count_tasks_in_section(progress_md, 'Todo List'),
       'in_progress': count_tasks_in_section(progress_md, 'In Progress'),
       'completed': count_tasks_in_section(progress_md, 'Completed Tasks'),
       'blocked': count_tasks_in_section(progress_md, 'Blocked Tasks'),
       'cancelled': count_tasks_in_section(progress_md, 'Cancelled Tasks')
   }
   ```

2. **Verify total matches sum**
   ```python
   total = sum(counts.values())
   claimed_total = extract_total_from_summary(progress_md)

   if total != claimed_total:
       print(f"ERROR: Claimed total ({claimed_total}) != actual total ({total})")
       return False
   ```

3. **Verify percentage matches completion ratio**
   ```python
   completed = counts['completed']
   total = sum(counts.values())
   calculated_pct = (completed / total) * 100

   claimed_pct = extract_progress_percentage(progress_md)

   if abs(calculated_pct - claimed_pct) > 1.0:
       print(f"ERROR: Claimed progress ({claimed_pct}%) != calculated ({calculated_pct}%)")
       return False
   ```

4. **Cross-check with activeContext.md**
   ```python
   current_task_in_active = extract_current_task(activeContext_md)
   tasks_in_progress = extract_tasks_in_section(progress_md, 'In Progress')

   if current_task_in_active not in tasks_in_progress:
       print(f"WARNING: Current task in activeContext.md not marked 'In Progress' in progress.md")
   ```

5. **Check for orphaned references**
   ```python
   # Tasks mentioned in notes but not in any section
   all_tasks = extract_all_task_names(progress_md)
   mentioned_tasks = extract_task_mentions_in_notes(progress_md)

   for mentioned in mentioned_tasks:
       if mentioned not in all_tasks:
           print(f"WARNING: Task '{mentioned}' mentioned but not in any section")
   ```

6. **Report consistency check results**
   ```markdown
   ## Consistency Validation Report

   **Task Counts:**
   - Pending: 8
   - In Progress: 2
   - Completed: 4
   - Blocked: 1
   - Cancelled: 0
   - **Total: 15** (matches claimed total)

   **Progress:**
   - Calculated: 26.67% (4/15 completed)
   - Claimed: 27%
   - **Difference: 0.33%** (within tolerance)

   **Cross-references:**
   - Current task in activeContext.md matches In Progress section
   - No orphaned task references

   **Overall:** All consistency checks passed
   ```

---

### PROCEDURE 5: Validate Completeness

**When to use:**
- After completing a task
- Before marking a task as complete
- When reviewing progress history

**Steps:**

1. **Check completed tasks have all required fields**
   ```python
   for task in extract_completed_tasks(progress_md):
       # Required: task name
       if not task.name:
           print("ERROR: Completed task has no name")
           return False

       # Required: completion timestamp
       if not task.completed_at:
           print(f"ERROR: Task '{task.name}' has no completion timestamp")
           return False

       # Required: completion note
       if not task.completion_note:
           print(f"ERROR: Task '{task.name}' has no completion note")
           return False
   ```

2. **Check blocked tasks have blocker documentation**
   ```python
   for task in extract_blocked_tasks(progress_md):
       # Required: blocker description
       if not task.blocker:
           print(f"ERROR: Blocked task '{task.name}' has no blocker")
           return False

       # Required: blocking timestamp
       if not task.blocked_at:
           print(f"ERROR: Blocked task '{task.name}' has no blocking timestamp")
           return False
   ```

3. **Check cancelled tasks have cancellation reason**
   ```python
   for task in extract_cancelled_tasks(progress_md):
       # Required: cancellation reason
       if not task.cancellation_reason:
           print(f"ERROR: Cancelled task '{task.name}' has no cancellation reason")
           return False

       # Required: cancellation timestamp
       if not task.cancelled_at:
           print(f"ERROR: Cancelled task '{task.name}' has no cancellation timestamp")
           return False
   ```

4. **Check pending tasks have clear descriptions**
   ```python
   for task in extract_pending_tasks(progress_md):
       # Required: task description (not just name)
       if len(task.description) < 10:
           print(f"WARNING: Task '{task.name}' has very short description")
   ```

5. **Report completeness validation results**
   ```markdown
   ## Completeness Validation Report

   **Completed Tasks (4):**
   - All have names
   - All have completion timestamps
   - All have completion notes

   **Blocked Tasks (1):**
   - All have blocker documentation
   - All have blocking timestamps

   **Cancelled Tasks (0):**
   - N/A

   **Pending Tasks (8):**
   - 2 tasks have short descriptions (consider expanding)

   **Overall:** All required fields present
   ```

---

## Common Validation Errors

### Error 1: Task in Multiple States

**Example:**
```markdown
## Todo List
- [ ] Implement authentication

## Completed Tasks
- [x] Implement authentication (completed 2025-12-31)
```

**Fix:**
Remove task from one section (usually the Todo List if it's completed).

---

### Error 2: Non-existent Dependency

**Example:**
```markdown
## Todo List
- [ ] Add unit tests (depends on: Implement feature XYZ)

# But "Implement feature XYZ" is not in progress.md
```

**Fix:**
Either add the missing dependency task or remove the dependency reference.

---

### Error 3: Timestamp Out of Order

**Example:**
```markdown
## Completed Tasks
- [x] Task A (completed 2025-12-31 15:00:00)
- [x] Task B (completed 2025-12-31 14:00:00)  # Earlier than Task A
```

**Fix:**
Reorder tasks chronologically or correct the timestamps.

---

### Error 4: Missing Completion Timestamp

**Example:**
```markdown
## Completed Tasks
- [x] Implement login endpoint
```

**Fix:**
Add timestamp:
```markdown
- [x] Implement login endpoint (completed 2025-12-31 14:30:00)
```

---

## Automated Validation

### Validation Script

```python
#!/usr/bin/env python3
"""Automated validation of progress.md"""

from datetime import datetime
import re
import sys

def validate_progress(progress_file):
    with open(progress_file) as f:
        content = f.read()

    errors = []

    # Validate task status
    if not validate_task_status(content):
        errors.append("Task status validation failed")

    # Validate dependencies
    if not validate_dependencies(content):
        errors.append("Dependency validation failed")

    # Validate timestamps
    if not validate_timestamps(content):
        errors.append("Timestamp validation failed")

    # Validate consistency
    if not validate_consistency(content):
        errors.append("Consistency validation failed")

    # Validate completeness
    if not validate_completeness(content):
        errors.append("Completeness validation failed")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("All validation checks passed")
        return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: validate_progress.py <progress.md>")
        sys.exit(1)

    success = validate_progress(sys.argv[1])
    sys.exit(0 if success else 1)
```

### Usage

```bash
python scripts/validate_progress.py .atlas/memory/progress.md
```

---

## Examples

### Example 1: Validating After Task Completion

**Scenario:** Just completed "Implement login endpoint" task

**Validation steps:**
```bash
# 1. Check task moved to completed section
grep -A 5 "## Completed Tasks" .atlas/memory/progress.md | grep "Implement login"

# 2. Check task has completion timestamp
grep "Implement login.*completed.*2025" .atlas/memory/progress.md

# 3. Check task removed from todo section
! grep -A 100 "## Todo List" .atlas/memory/progress.md | grep -v "^#" | grep "Implement login"

# 4. Check dependent tasks are unblocked
python scripts/validate_progress.py .atlas/memory/progress.md
```

**Expected output:**
```
Task found in Completed Tasks section
Task has valid completion timestamp
Task not in Todo List section
No validation errors
2 dependent tasks can now proceed
```

---

## Troubleshooting

### Issue: Validation script reports errors but file looks correct

**Cause:** Script may have bugs or outdated validation logic

**Solution:**
1. Manually review the reported errors
2. Check if errors are false positives
3. Update validation script if needed
4. Report script issues for fixing

---

### Issue: Many validation errors after importing tasks

**Cause:** Imported tasks may not follow validation rules

**Solution:**
1. Run validation to identify all errors
2. Fix errors systematically one by one
3. Re-run validation after each fix
4. Update import process to prevent future errors

---

**Version:** 1.0
**Last Updated:** 2026-01-08
**Target Audience:** Atlas Orchestrator Agents
**Related:** SKILL.md (PROCEDURE 4: Update Task Progress), [Part 1: Rules and Basic Procedures](15-progress-validation-part1-rules-and-basic-procedures.md)
