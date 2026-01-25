# Compaction Integration - Part 2: Recovery & Verification

## Table of Contents

1. [PROCEDURE 3: Reload After Compaction](#procedure-3-reload-after-compaction)
2. [PROCEDURE 4: Verify Post-Compaction State](#procedure-4-verify-post-compaction-state)
3. [PROCEDURE 5: Recover from Compaction Issues](#procedure-5-recover-from-compaction-issues)
   - Minor recovery from checkpoint
   - Major recovery from archive
   - Critical recovery from user input
4. [Examples](#examples)
   - Example 1: Proactive compaction preparation
   - Example 2: Recovery from compaction issue
5. [Troubleshooting](#troubleshooting)
   - Memory not reloaded after compaction
   - Frequent compactions disrupting work

**Related:** [Part 1: Concepts & Preparation](17-compaction-integration-part1-concepts-preparation.md)

---

## PROCEDURE 3: Reload After Compaction

**When to use:**
- After context compaction occurred
- When starting new session after compaction
- When agent seems to have forgotten recent work

**Steps:**

1. **Detect that compaction occurred**
   ```python
   # Indicators of compaction:
   # - Conversation history is shorter than expected
   # - Recent messages are missing
   # - Context token count is low despite recent activity

   def detect_compaction():
       # Check if recovery file exists
       if file_exists('.atlas/memory/RECOVERY.md'):
           recovery_time = get_file_timestamp('.atlas/memory/RECOVERY.md')
           current_time = datetime.now()

           # If recovery file is recent, compaction likely occurred
           if current_time - recovery_time < timedelta(minutes=10):
               return True

       return False
   ```

2. **Load all memory files**
   ```python
   active_context = load_file('.atlas/memory/activeContext.md')
   patterns = load_file('.atlas/memory/patterns.md')
   progress = load_file('.atlas/memory/progress.md')
   ```

3. **Validate loaded memory**
   ```python
   # Check files are not empty
   if not active_context or not patterns or not progress:
       print("ERROR: One or more memory files are empty")
       attempt_recovery_from_checkpoint()
       return False

   # Check files are not corrupted
   validate_markdown(active_context)
   validate_markdown(patterns)
   validate_markdown(progress)
   ```

4. **Reconstruct session state from memory**
   ```python
   session_state = {
       'current_task': extract_current_task(active_context),
       'current_file': extract_current_file(active_context),
       'current_line': extract_current_line(active_context),
       'recent_decisions': extract_recent_decisions(active_context),
       'todo_list': extract_todo_list(progress),
       'active_patterns': extract_active_patterns(patterns)
   }
   ```

5. **Verify state is complete**
   ```python
   required_fields = ['current_task', 'current_file', 'current_line']

   for field in required_fields:
       if not session_state[field]:
           print(f"WARNING: Missing required field: {field}")
           # Attempt recovery or ask user
   ```

6. **Resume from saved state**
   ```
   Agent: I've reloaded session memory after context compaction.

   **Resumed State:**
   - Current Task: Implement authorization middleware
   - Current File: src/auth/middleware.py (line 45)
   - Progress: 12/25 tasks completed (48%)

   Continuing work on authorization middleware...
   ```

7. **Update recovery metadata**
   ```markdown
   # In activeContext.md

   ## Post-Compaction Recovery
   **Compaction Detected:** 2025-12-31 17:10:00
   **Recovery Completed:** 2025-12-31 17:10:15
   **State Restored:** Complete
   **Resumed Task:** Implement authorization middleware
   ```

---

## PROCEDURE 4: Verify Post-Compaction State

**When to use:**
- After reloading memory post-compaction
- To ensure no data was lost
- Before resuming work

**Steps:**

1. **Compare pre and post-compaction state**
   ```python
   # Load pre-compaction checkpoint
   checkpoint = load_latest_checkpoint()

   # Compare current state
   state_comparison = {
       'current_task': compare(checkpoint.current_task, session_state.current_task),
       'current_file': compare(checkpoint.current_file, session_state.current_file),
       'task_count': compare(checkpoint.task_count, len(session_state.todo_list))
   }

   mismatches = [k for k, v in state_comparison.items() if not v]
   if mismatches:
       print(f"WARNING: State mismatches detected: {mismatches}")
   ```

2. **Check for missing information**
   ```python
   # Decisions made between last save and compaction
   last_save_time = extract_last_save_time(checkpoint)
   compaction_time = extract_compaction_time()

   lost_time_window = compaction_time - last_save_time

   if lost_time_window > timedelta(minutes=5):
       print(f"WARNING: {lost_time_window} of work may be missing")
       print("Last save:", last_save_time)
       print("Compaction:", compaction_time)
   ```

3. **Validate file references**
   ```python
   current_file = session_state.current_file

   if not os.path.exists(current_file):
       print(f"ERROR: Current file does not exist: {current_file}")
       # File may have been moved or deleted
       # Need to find it or ask user
   ```

4. **Check task consistency**
   ```python
   # Current task should exist in progress.md
   current_task = session_state.current_task
   todo_list = session_state.todo_list

   if current_task not in [task.name for task in todo_list]:
       print(f"WARNING: Current task '{current_task}' not in todo list")
       # May have been completed or removed
   ```

5. **Report verification results**
   ```markdown
   ## Post-Compaction Verification

   **Verification Time:** 2025-12-31 17:10:30

   **State Integrity:**
   - All memory files loaded successfully
   - Current task matches pre-compaction state
   - Current file exists and is accessible
   - Task progress matches checkpoint
   - WARNING: 3 minutes of work between last save and compaction
   - WARNING: May need to review recent decisions

   **Recommendation:** Review last 3 minutes of work before continuing
   ```

6. **Prompt user if issues found**
   ```
   Agent: Post-compaction verification found minor issues:
   - 3 minutes elapsed between last save and compaction
   - Recent decisions may need review

   Can you confirm the current task is still: Implement authorization middleware?
   And you were editing: src/auth/middleware.py at line 45?
   ```

---

## PROCEDURE 5: Recover from Compaction Issues

**When to use:**
- Verification detects problems
- Memory files are corrupted
- State is inconsistent after compaction

**Steps:**

1. **Assess severity of issue**
   ```python
   severity = assess_compaction_issues()

   if severity == 'MINOR':
       # Missing recent work but core state intact
       use_minor_recovery()
   elif severity == 'MAJOR':
       # Corrupted files or major state loss
       use_major_recovery()
   elif severity == 'CRITICAL':
       # Complete memory loss
       use_critical_recovery()
   ```

2. **Minor Recovery: Restore from recent checkpoint**
   ```bash
   # Find most recent pre-compaction checkpoint
   latest_checkpoint=$(ls -t .atlas/memory/checkpoints/pre-compaction-* | head -1)

   # Restore files
   cp "$latest_checkpoint/activeContext.md" .atlas/memory/
   cp "$latest_checkpoint/patterns.md" .atlas/memory/
   cp "$latest_checkpoint/progress.md" .atlas/memory/
   ```

3. **Major Recovery: Restore from archive**
   ```bash
   # If checkpoints are also corrupted, restore from archive
   latest_snapshot=$(ls -t .atlas/memory/snapshots/*.tar.gz | head -1)

   # Extract snapshot
   restore_dir="/tmp/memory-restore"
   tar xzf "$latest_snapshot" -C "$restore_dir"

   # Restore files
   cp "$restore_dir/*/activeContext.md" .atlas/memory/
   cp "$restore_dir/*/patterns.md" .atlas/memory/
   cp "$restore_dir/*/progress.md" .atlas/memory/
   ```

4. **Critical Recovery: Reconstruct from user input**
   ```
   Agent: I've detected critical memory loss after compaction and no valid backups were found.

   I need to reconstruct session state. Can you help with these questions:

   1. What task were you working on?
   2. What file were you editing?
   3. What is the current status of the project?
   4. What tasks have been completed recently?

   I'll use your answers to rebuild the session memory.
   ```

5. **Rebuild memory from user input**
   ```python
   user_input = collect_user_responses()

   # Create new activeContext.md
   new_active_context = f"""
   # Active Context

   **Last Updated:** {datetime.now().isoformat()}
   **Recovery Note:** Rebuilt after compaction issue

   ## Current Task
   {user_input.current_task}

   ## Current File
   {user_input.current_file}

   ## Recovery Note
   Session memory was rebuilt from user input due to compaction issues.
   Historical data before {datetime.now().isoformat()} may be incomplete.
   """

   write_file('.atlas/memory/activeContext.md', new_active_context)
   ```

6. **Document recovery event**
   ```markdown
   # In activeContext.md

   ## Recovery History
   **Event:** Compaction recovery
   **Date:** 2025-12-31 17:15:00
   **Severity:** Major
   **Recovery Method:** Restored from checkpoint
   **Data Loss:** ~5 minutes of work
   **Action Taken:** Verified state with user
   ```

---

## Examples

### Example 1: Proactive Compaction Preparation

**Scenario:** Context at 72%, preparing for compaction

**Preparation:**
```
Agent: Context window is at 72% utilization. Compaction may occur soon.
       Saving current state...

[PROCEDURE 2: Save State Before Compaction]

Saved state:
- activeContext.md (updated)
- patterns.md (updated)
- progress.md (updated)
- Checkpoint created: checkpoints/pre-compaction-20251231-170500

Current state preserved. Can safely continue work.
```

**After compaction:**
```
Agent: Context compaction detected. Reloading session memory...

[PROCEDURE 3: Reload After Compaction]

State restored:
- Current Task: Implement authorization middleware
- Current File: src/auth/middleware.py (line 45)
- Progress: 12/25 tasks (48%)

Resuming work on authorization middleware...
```

---

### Example 2: Recovery from Compaction Issue

**Scenario:** Compaction occurred, memory files corrupted

**Detection:**
```
Agent: Loading session memory...
       ERROR: activeContext.md appears corrupted (invalid format)

[PROCEDURE 5: Recover from Compaction Issues]

Attempting recovery from checkpoint...
Latest checkpoint: checkpoints/pre-compaction-20251231-170500
Restoring files... Done

Verification:
- Files restored successfully
- Current task: Implement authorization middleware
- WARNING: Last 3 minutes of work may be lost

Can you confirm you were working on authorization middleware in src/auth/middleware.py?
```

**User confirms:**
```
User: Yes, that's correct. I was at line 45.

Agent: Thank you. Session memory restored successfully.
       Resuming from src/auth/middleware.py line 45.
```

---

## Troubleshooting

### Issue: Memory not reloaded after compaction

**Symptoms:**
- Agent behaves as if starting fresh
- No memory of previous work
- Memory files exist but not loaded

**Solution:**
1. Manually trigger reload (PROCEDURE 3)
2. Verify memory files are valid
3. Check for load errors in logs
4. Implement automatic reload on session start

---

### Issue: Frequent compactions disrupting work

**Symptoms:**
- Compaction occurs every few minutes
- Constant save/reload cycles
- Productivity impacted

**Solution:**
1. Reduce context usage:
   - Archive old completed tasks
   - Consolidate active context
   - Limit tool output verbosity
2. Increase save frequency
3. Use smaller code blocks
4. Split work into smaller sessions

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Target Audience:** Atlas Orchestrator Agents
**Related:** [Part 1: Concepts & Preparation](17-compaction-integration-part1-concepts-preparation.md), SKILL.md (PROCEDURE 6: Prepare for Context Compaction)
