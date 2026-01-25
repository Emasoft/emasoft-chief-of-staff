# Context Synchronization - Part 1: Foundations and Core Procedures

## Table of Contents

1. [Overview](#overview)
   - 1.1 [What Is Context Synchronization?](#what-is-context-synchronization)
   - 1.2 [Why Synchronization Matters](#why-synchronization-matters)
2. [Understanding Context Drift](#what-is-context-drift)
   - 2.1 [Definition](#definition)
   - 2.2 [Common Causes](#common-causes)
3. [Synchronization Points](#synchronization-points)
   - 3.1 [When to Synchronize](#when-to-synchronize)
4. [Core Synchronization Procedures](#synchronization-procedures)
   - 4.1 [Procedure 1: Detect Context Drift](#procedure-1-detect-context-drift)
   - 4.2 [Procedure 2: Sync After Task Completion](#procedure-2-sync-after-task-completion)
   - 4.3 [Procedure 3: Sync After File Switch](#procedure-3-sync-after-file-switch)
   - 4.4 [Procedure 4: Sync After Decision](#procedure-4-sync-after-decision)

**Related Documents:**
- [Part 2: Advanced Procedures and Troubleshooting](14-context-sync-part2-advanced.md) - Emergency resync, consistency checks, examples

---

## Overview

### What Is Context Synchronization?

Context synchronization is the process of ensuring that the session memory files (activeContext.md, patterns.md, progress.md) accurately reflect the current actual state of the agent's work. When memory becomes out of sync with reality, the agent may continue working on wrong tasks, reference outdated files, or make decisions based on stale information.

### Why Synchronization Matters

**Without synchronization:**
- Agent resumes wrong task after interruption
- References files that have been moved or deleted
- Makes decisions based on outdated assumptions
- Duplicates work already completed
- Ignores blockers that have been resolved

**With synchronization:**
- Memory always reflects current reality
- Agent can resume work correctly
- Decisions are based on accurate information
- No duplicate or contradictory work

---

## What Is Context Drift?

### Definition

**Context drift** occurs when the in-memory state of the agent diverges from the state recorded in session memory files.

### Common Causes

**Cause 1: Infrequent Updates**
- Memory updated only at session start/end
- Work happens but memory not written
- Long gaps between memory writes

**Cause 2: Failed Updates**
- Memory write failed due to error
- Update was interrupted mid-write
- Validation failed and update rolled back

**Cause 3: Manual Interventions**
- User manually edited files
- User changed task priorities
- User moved or deleted files agent was editing

**Cause 4: External Changes**
- Other agents modified shared files
- CI/CD pipeline made changes
- Automated tools reformatted code

**Cause 5: Missed Events**
- Task completed but progress.md not updated
- File switch happened but activeContext.md not updated
- Pattern discovered but patterns.md not updated

---

## Synchronization Points

### When to Synchronize

**Point 1: Task Transition**
- Trigger: Task status changes (started, completed, blocked, failed)
- Action: Update progress.md with new status
- Action: Update activeContext.md if switching tasks

**Point 2: File Navigation**
- Trigger: Agent switches to editing different file
- Action: Update activeContext.md with new file path
- Action: Update activeContext.md with new line number

**Point 3: Decision Made**
- Trigger: Agent makes architectural or implementation decision
- Action: Record decision in activeContext.md
- Action: Update patterns.md if decision reveals pattern

**Point 4: Blocker Encountered**
- Trigger: Task becomes blocked
- Action: Update progress.md with blocker details
- Action: Update activeContext.md with blocked state

**Point 5: Pattern Discovered**
- Trigger: Agent identifies code pattern or anti-pattern
- Action: Add pattern to patterns.md
- Action: Update activeContext.md to reference new pattern

**Point 6: Session Initialization**
- Trigger: Agent starts new session
- Action: Validate all memory files match reality
- Action: Update any stale information

**Point 7: Before Context Compaction**
- Trigger: Context window approaching limit
- Action: Full synchronization of all memory files
- Action: Ensure no pending updates are lost

---

## Synchronization Procedures

### PROCEDURE 1: Detect Context Drift

**When to use:**
- At session start
- After resuming from interruption
- When agent behavior seems wrong
- Before starting major tasks

**Steps:**

1. **Load current memory state**
   ```bash
   active_task=$(grep "**Current Task:**" .atlas/memory/activeContext.md | cut -d: -f2-)
   active_file=$(grep "**Current File:**" .atlas/memory/activeContext.md | cut -d: -f2-)
   ```

2. **Check if current task is still valid**
   - Is the task in progress.md marked as completed?
   - Is the task blocked but memory shows it as active?
   - Has the task been reassigned or cancelled?

3. **Check if current file still exists**
   ```bash
   if [ ! -f "$active_file" ]; then
     echo "DRIFT: Current file no longer exists"
   fi
   ```

4. **Check if current line is still valid**
   ```bash
   active_line=$(grep "**Current Line:**" .atlas/memory/activeContext.md | cut -d: -f2-)
   total_lines=$(wc -l < "$active_file")
   if [ "$active_line" -gt "$total_lines" ]; then
     echo "DRIFT: Current line beyond file end"
   fi
   ```

5. **Compare task status across files**
   - Is task marked "in progress" in activeContext.md?
   - Is same task marked "completed" in progress.md?
   - This is drift - needs synchronization

6. **Check for missing recent work**
   - Check last modified timestamp of memory files
   - Check last modified timestamp of working files
   - If working files modified after memory files, drift detected

7. **Report drift findings**
   ```markdown
   ## Context Drift Detected

   **Drift Type:** Task status mismatch
   **Current Memory State:** Working on authentication endpoint
   **Actual State:** Authentication endpoint completed 2 hours ago
   **Recommended Action:** Update activeContext.md to next task
   ```

**Drift detection checklist:**
- [ ] Current task is valid and not completed
- [ ] Current file exists and is editable
- [ ] Current line is within file bounds
- [ ] Task status is consistent across memory files
- [ ] Recent work is captured in memory
- [ ] No missing updates detected

---

### PROCEDURE 2: Sync After Task Completion

**When to use:**
- Immediately after completing a task
- Before switching to next task
- Before session termination

**Steps:**

1. **Update progress.md with completion**
   ```markdown
   ## Completed Tasks

   - [x] Implement authentication endpoint (completed 2025-12-31 10:45:00)
     - Added JWT token generation
     - Implemented login route
     - Added unit tests
   ```

2. **Remove from active tasks in progress.md**
   ```markdown
   ## Todo List

   ~~- [ ] Implement authentication endpoint~~ (moved to completed)
   - [ ] Implement authorization middleware
   - [ ] Add rate limiting
   ```

3. **Update dependencies in progress.md**
   ```markdown
   ## Todo List

   - [ ] Implement authorization middleware (blocker removed - auth endpoint complete)
   - [ ] Add rate limiting
   ```

4. **Update activeContext.md to next task**
   ```markdown
   ## Current Task
   Implement authorization middleware

   ## Previous Task (just completed)
   Implement authentication endpoint (completed 2025-12-31 10:45:00)
   ```

5. **Clear completion-specific context**
   - Remove references to completed task's files
   - Clear decisions specific to completed task
   - Update current file to next task's file

6. **Validate synchronization**
   - Task is in "Completed Tasks" section
   - Task is not in "Todo List" section
   - activeContext.md references next task
   - No contradictions between files

**Example synchronized state after completion:**

activeContext.md:
```markdown
## Current Task
Implement authorization middleware

## Previous Task
Implement authentication endpoint (completed 2025-12-31 10:45:00)
```

progress.md:
```markdown
## Todo List
- [ ] Implement authorization middleware
- [ ] Add rate limiting

## Completed Tasks
- [x] Implement authentication endpoint (completed 2025-12-31 10:45:00)
```

---

### PROCEDURE 3: Sync After File Switch

**When to use:**
- When opening a different file for editing
- When navigating between files during review
- When switching focus from one module to another

**Steps:**

1. **Record previous file state**
   ```markdown
   ## Recent File History
   - src/auth/routes.py (line 45, working on login endpoint)
   - src/auth/models.py (line 12, reviewed User model)
   ```

2. **Update current file in activeContext.md**
   ```markdown
   ## Current File
   src/auth/middleware.py

   ## Current Line
   1

   ## Current Focus
   Implementing authorization middleware
   ```

3. **Update recent decisions if file switch reveals new info**
   ```markdown
   ## Recent Decisions
   - Moving from routes.py to middleware.py
   - Need to extract auth logic from routes into middleware
   - Will use decorator pattern for authorization
   ```

4. **Update current task if file switch indicates task change**
   - If new file is for different task, update current task
   - If same task but different file, keep current task

5. **Verify file exists and is accessible**
   ```bash
   if [ ! -f "src/auth/middleware.py" ]; then
     echo "WARNING: New current file does not exist"
     echo "Creating file..."
     touch src/auth/middleware.py
   fi
   ```

6. **Write synchronized activeContext.md**
   ```bash
   # Atomic write to prevent corruption
   cat > .atlas/memory/activeContext.md.tmp << 'EOF'
   [updated content with new file]
   EOF
   mv .atlas/memory/activeContext.md.tmp .atlas/memory/activeContext.md
   ```

---

### PROCEDURE 4: Sync After Decision

**When to use:**
- Immediately after making architectural decision
- After choosing between implementation approaches
- After discovering important constraint or requirement

**Steps:**

1. **Record decision in activeContext.md**
   ```markdown
   ## Recent Decisions

   ### Decision: Use decorator pattern for authorization (2025-12-31 11:00:00)
   **Context:** Need reusable way to protect endpoints
   **Options Considered:**
   - Middleware for all routes
   - Decorator per endpoint (chosen)
   - Manual checks in each function

   **Rationale:** Decorators provide fine-grained control and are more explicit
   **Impact:** Will create @requires_auth and @requires_role decorators
   ```

2. **Update current task if decision changes direction**
   ```markdown
   ## Current Task
   Implement authorization decorators (updated from "middleware")
   ```

3. **Check if decision reveals pattern**
   - If decision is based on pattern, add to patterns.md
   - If decision establishes new pattern, add to patterns.md

   ```markdown
   # In patterns.md

   ## Code Patterns

   ### Pattern: Decorator-based Authorization
   **Discovered:** 2025-12-31 11:00:00
   **Context:** Authentication and authorization implementation

   **Pattern:**
   ```python
   @requires_auth
   @requires_role('admin')
   def admin_endpoint():
       ...
   ```

   **Benefits:** Clear, reusable, testable
   ```

4. **Update task list if decision adds new tasks**
   ```markdown
   ## Todo List
   - [ ] Implement @requires_auth decorator
   - [ ] Implement @requires_role decorator
   - [ ] Add decorator unit tests
   - [ ] Update endpoints to use decorators
   ```

5. **Validate consistency across files**
   - Decision in activeContext.md
   - Pattern in patterns.md (if applicable)
   - New tasks in progress.md (if applicable)
   - All files tell same story

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Target Audience:** Atlas Orchestrator Agents
**Related:** [Part 2: Advanced Procedures](14-context-sync-part2-advanced.md)
