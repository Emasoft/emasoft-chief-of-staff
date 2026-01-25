# Context Synchronization - Part 2: Advanced Procedures and Troubleshooting

## Table of Contents

1. [Emergency Full Resync](#procedure-5-emergency-full-resync)
   - 1.1 [When to Use Emergency Resync](#when-to-use)
   - 1.2 [Step-by-Step Procedure](#steps)
2. [Consistency Checks](#consistency-checks)
   - 2.1 [Check 1: Task Status Consistency](#check-1-task-status-consistency)
   - 2.2 [Check 2: File Path Validity](#check-2-file-path-validity)
   - 2.3 [Check 3: Decision Recency](#check-3-decision-recency)
   - 2.4 [Check 4: Pattern Relevance](#check-4-pattern-relevance)
3. [Synchronization Examples](#examples)
   - 3.1 [Example 1: Syncing After Unexpected Task Completion](#example-1-syncing-after-unexpected-task-completion)
   - 3.2 [Example 2: Syncing After File Moved](#example-2-syncing-after-file-moved)
   - 3.3 [Example 3: Syncing After Decision Changes Direction](#example-3-syncing-after-decision-changes-direction)
4. [Troubleshooting](#troubleshooting)
   - 4.1 [Cannot Determine Actual State](#issue-sync-detects-drift-but-cannot-determine-actual-state)
   - 4.2 [Frequent Drift Detected](#issue-frequent-drift-detected)
   - 4.3 [Sync Creates New Inconsistencies](#issue-sync-creates-new-inconsistencies)

**Related Documents:**
- [Part 1: Foundations and Core Procedures](14-context-sync-part1-foundations.md) - Overview, drift detection, basic sync procedures

---

## PROCEDURE 5: Emergency Full Resync

### When to use:
- Severe context drift detected
- Agent is clearly working on wrong thing
- Memory state is completely inconsistent
- After major manual intervention

### Steps:

1. **Stop all current work**
   - Do not proceed with any tasks
   - Do not make any file changes
   - Focus entirely on synchronization

2. **Snapshot current actual state**
   ```bash
   # What file is actually being edited?
   actual_file=$(git diff --name-only HEAD)

   # What tasks are actually complete?
   actual_completed=$(git log --oneline --since="1 day ago")

   # What is current branch?
   actual_branch=$(git branch --show-current)
   ```

3. **Snapshot current memory state**
   ```bash
   memory_task=$(grep "**Current Task:**" .atlas/memory/activeContext.md)
   memory_file=$(grep "**Current File:**" .atlas/memory/activeContext.md)
   memory_progress=$(grep -A 20 "## Todo List" .atlas/memory/progress.md)
   ```

4. **Compare and identify discrepancies**
   ```markdown
   ## Synchronization Report

   **Actual File:** src/auth/middleware.py
   **Memory File:** src/auth/routes.py
   **Discrepancy:** Files do not match

   **Actual Task:** Authorization decorators
   **Memory Task:** Login endpoint
   **Discrepancy:** Tasks do not match (login is complete)
   ```

5. **Ask user to confirm actual state**
   ```
   Agent: I've detected major context drift. Can you confirm:
   - Are you currently working on: authorization decorators?
   - In file: src/auth/middleware.py?
   - Have you completed: login endpoint implementation?
   ```

6. **Rewrite all memory files based on confirmed state**

   activeContext.md:
   ```markdown
   # Active Context

   **Last Updated:** 2025-12-31 11:15:00
   **Sync Note:** Emergency full resync performed

   ## Current Task
   Implement authorization decorators (user confirmed)

   ## Current File
   src/auth/middleware.py (user confirmed)

   ## Recent Decisions
   [reconstructed from user confirmation]
   ```

   progress.md:
   ```markdown
   # Progress

   **Last Updated:** 2025-12-31 11:15:00
   **Sync Note:** Emergency full resync performed

   ## Todo List
   [rebuilt from user confirmation]

   ## Completed Tasks
   - [x] Login endpoint implementation (user confirmed complete)
   [other confirmed completions]
   ```

7. **Validate resynchronized state**
   - Run PROCEDURE 1 to check for drift
   - Should show no drift
   - Memory should match reality

8. **Document resync event**
   ```markdown
   ## Sync History

   ### Emergency Resync (2025-12-31 11:15:00)
   **Reason:** Severe context drift - working on wrong task
   **Method:** User confirmation + full rewrite
   **Outcome:** Successfully resynchronized
   ```

---

## Consistency Checks

### Check 1: Task Status Consistency

**What to check:**
- Task in activeContext.md should exist in progress.md
- Task should have same status in both files
- If task is "current" in activeContext.md, it should be "in progress" in progress.md

**How to check:**
```bash
# Extract current task
current=$(grep "**Current Task:**" .atlas/memory/activeContext.md | cut -d: -f2-)

# Check if in progress.md todo list
if ! grep -q "$current" .atlas/memory/progress.md; then
  echo "INCONSISTENCY: Current task not in progress.md"
fi

# Check if in completed list
if grep -A 100 "## Completed Tasks" .atlas/memory/progress.md | grep -q "$current"; then
  echo "INCONSISTENCY: Current task is marked complete"
fi
```

---

### Check 2: File Path Validity

**What to check:**
- Current file path in activeContext.md should exist
- File should be in expected directory structure
- File should be editable (not read-only)

**How to check:**
```bash
active_file=$(grep "**Current File:**" .atlas/memory/activeContext.md | cut -d: -f2- | tr -d ' ')

if [ ! -f "$active_file" ]; then
  echo "INCONSISTENCY: Current file does not exist"
elif [ ! -w "$active_file" ]; then
  echo "INCONSISTENCY: Current file is not writable"
fi
```

---

### Check 3: Decision Recency

**What to check:**
- Recent decisions should be actually recent (within last session)
- Old decisions should be moved to archive
- Decisions should be relevant to current task

**How to check:**
```python
from datetime import datetime, timedelta

# Extract decision timestamps
decisions = extract_decisions_from(activeContext)

# Check each decision
for decision in decisions:
    decision_time = datetime.fromisoformat(decision.timestamp)
    if datetime.now() - decision_time > timedelta(days=7):
        print(f"INCONSISTENCY: Decision '{decision.title}' is over 7 days old")
```

---

### Check 4: Pattern Relevance

**What to check:**
- Patterns in patterns.md should be relevant to current project
- Patterns should be referenced by current work
- Patterns should not contradict each other

**How to check:**
```bash
# Check if patterns are used
for pattern in $(grep "^### Pattern:" .atlas/memory/patterns.md); do
  pattern_name=${pattern#*: }
  if ! grep -r "$pattern_name" src/; then
    echo "INCONSISTENCY: Pattern '$pattern_name' not used in codebase"
  fi
done
```

---

## Examples

### Example 1: Syncing After Unexpected Task Completion

**Scenario:** User manually completed task while agent was idle

**Before sync:**
```markdown
# activeContext.md
## Current Task
Implement login endpoint

# progress.md
## Todo List
- [ ] Implement login endpoint
```

**Reality:**
```bash
$ git log -1 --oneline
abc123f Add login endpoint implementation
```

**Sync procedure:**
1. Detect drift - task is complete but memory shows in progress
2. Ask user to confirm: "I see the login endpoint was completed. Should I move to the next task?"
3. Update progress.md to mark task complete
4. Update activeContext.md to next task
5. Validate sync

**After sync:**
```markdown
# activeContext.md
## Current Task
Implement authorization middleware

## Previous Task
Implement login endpoint (completed by user 2025-12-31 10:00:00)

# progress.md
## Todo List
- [ ] Implement authorization middleware

## Completed Tasks
- [x] Implement login endpoint (completed 2025-12-31 10:00:00)
```

---

### Example 2: Syncing After File Moved

**Scenario:** File was moved to different directory

**Before sync:**
```markdown
# activeContext.md
## Current File
src/auth/routes.py
```

**Reality:**
```bash
$ ls src/auth/routes.py
ls: cannot access 'src/auth/routes.py': No such file exists

$ git log --follow src/api/auth/routes.py
# Shows file was moved
```

**Sync procedure:**
1. Detect drift - current file does not exist
2. Check git history for file move
3. Update activeContext.md with new path
4. Verify new path is correct

**After sync:**
```markdown
# activeContext.md
## Current File
src/api/auth/routes.py (moved from src/auth/routes.py)

## Recent Events
- File relocated in project restructure (2025-12-31 09:00:00)
```

---

### Example 3: Syncing After Decision Changes Direction

**Scenario:** Decision made that changes current task

**Before sync:**
```markdown
# activeContext.md
## Current Task
Implement session-based authentication

# progress.md
## Todo List
- [ ] Implement session storage
- [ ] Implement session middleware
```

**Decision made:**
```markdown
# activeContext.md (updated)
## Recent Decisions

### Decision: Use JWT instead of sessions (2025-12-31 11:30:00)
**Rationale:** Stateless auth better for API-first architecture
```

**Sync procedure:**
1. Decision invalidates current task approach
2. Update current task to reflect new direction
3. Update progress.md to replace session tasks with JWT tasks
4. Document decision impact

**After sync:**
```markdown
# activeContext.md
## Current Task
Implement JWT-based authentication (changed from session-based)

## Recent Decisions
### Decision: Use JWT instead of sessions (2025-12-31 11:30:00)

# progress.md
## Todo List
- [ ] Implement JWT token generation
- [ ] Implement JWT validation middleware
- [ ] Add token refresh logic

## Cancelled Tasks
- [-] Implement session storage (cancelled due to JWT decision)
- [-] Implement session middleware (cancelled due to JWT decision)
```

---

## Troubleshooting

### Issue: Sync detects drift but cannot determine actual state

**Symptoms:**
- Memory state and actual state both seem plausible
- Cannot determine which is correct
- No clear evidence either way

**Solution:**
1. Ask user to confirm actual state
2. Do not make assumptions
3. Use user confirmation as source of truth
4. Document sync was based on user input

---

### Issue: Frequent drift detected

**Symptoms:**
- Every sync operation finds drift
- Drift appears shortly after sync
- Memory constantly out of sync

**Cause:** Updates not happening frequently enough

**Solution:**
1. Increase sync frequency
2. Update memory after every significant event
3. Implement automatic sync triggers
4. Review and fix update procedures

---

### Issue: Sync creates new inconsistencies

**Symptoms:**
- After sync, files are more inconsistent than before
- Sync operation introduced new errors
- Multiple syncs make things worse

**Cause:** Sync logic is incorrect or incomplete

**Solution:**
1. Stop automatic syncs
2. Perform manual review of memory files
3. Use PROCEDURE 5 (emergency full resync)
4. Get user confirmation before each change
5. Fix sync procedures before resuming automatic sync

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Target Audience:** Atlas Orchestrator Agents
**Related:** [Part 1: Foundations and Core Procedures](14-context-sync-part1-foundations.md), SKILL.md (Phase 2: Session Execution)
