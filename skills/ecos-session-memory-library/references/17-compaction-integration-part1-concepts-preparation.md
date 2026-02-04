# Compaction Integration - Part 1: Concepts & Preparation

## Table of Contents

1. [Overview](#overview)
   - What is compaction integration
   - Why integration matters
2. [Understanding Context Compaction](#understanding-context-compaction)
   - What is context compaction
   - When compaction occurs
   - What happens during compaction
3. [Compaction Risks](#compaction-risks)
   - Risk 1: Memory Loss
   - Risk 2: Partial State Loss
   - Risk 3: Stale Memory
   - Risk 4: Failed Reload
4. [PROCEDURE 1: Prepare for Compaction](#procedure-1-prepare-for-compaction)
5. [PROCEDURE 2: Save State Before Compaction](#procedure-2-save-state-before-compaction)
6. [Compaction Triggers](#compaction-triggers)
   - Proactive compaction monitoring
   - Emergency save triggers

**Related:** [Part 2: Recovery & Verification](17-compaction-integration-part2-recovery-verification.md)

---

## Overview

### What Is Compaction Integration?

Compaction integration is the set of procedures that ensure session memory survives context window compaction. Context window compaction occurs when Claude's conversation context becomes too large and must be compressed or truncated. Without proper integration, memory can be lost during compaction.

### Why Integration Matters

**Without compaction integration:**
- Session memory lost when context is compacted
- Agent forgets current task after compaction
- Progress tracking is reset
- Patterns are forgotten
- Work must restart from beginning

**With compaction integration:**
- Session memory persists across compaction
- Agent resumes work seamlessly
- Progress is preserved
- Patterns are retained
- Minimal disruption to workflow

---

## Understanding Context Compaction

### What Is Context Compaction?

**Context window** is the total conversation history that Claude can see. It has a fixed token limit (e.g., 200,000 tokens). When this limit is approached, the context must be compacted.

**Compaction methods:**
1. **Truncation** - Remove oldest messages
2. **Summarization** - Summarize old messages
3. **Selective retention** - Keep important messages, remove others

### When Does Compaction Occur?

**Automatic triggers:**
- Context window reaches 70-80% of limit
- Long conversation with many messages
- Large code blocks or file contents in context
- Extensive tool outputs

**Manual triggers:**
- User explicitly requests context reset
- Starting new conversation
- Switching to different task requiring fresh context

### What Happens During Compaction?

**Conversation history:**
- Oldest messages removed or summarized
- Recent messages retained
- Tool outputs may be discarded
- Code blocks may be removed

**Session memory:**
- **WITHOUT integration:** Memory files mentioned in conversation but not persisted
- **WITH integration:** Memory files explicitly saved to disk and reloaded

---

## Compaction Risks

### Risk 1: Memory Loss

**Risk:** Session memory exists only in conversation context

**Impact:**
- After compaction, agent has no memory of current task
- Progress tracking is lost
- Patterns are forgotten

**Mitigation:** Save memory to disk BEFORE compaction

---

### Risk 2: Partial State Loss

**Risk:** Some memory persisted, some lost

**Impact:**
- activeContext.md saved but progress.md lost
- Inconsistent state after compaction
- Agent has conflicting information

**Mitigation:** Atomic save operation - all or nothing

---

### Risk 3: Stale Memory

**Risk:** Memory saved but not updated before compaction

**Impact:**
- Agent resumes with outdated information
- Recent work is not captured
- Decisions made after last save are lost

**Mitigation:** Update memory immediately before compaction

---

### Risk 4: Failed Reload

**Risk:** Memory saved but not reloaded after compaction

**Impact:**
- Memory exists on disk but agent doesn't load it
- Agent starts fresh despite having saved state
- Work is duplicated

**Mitigation:** Explicit reload procedure after compaction

---

## PROCEDURE 1: Prepare for Compaction

**When to use:**
- Context window reaches 70% utilization
- Before long-running operations
- When many large outputs are expected

**Steps:**

1. **Check context window utilization**
   ```python
   # Pseudo-code - actual implementation depends on environment
   current_tokens = get_current_context_tokens()
   max_tokens = get_max_context_tokens()
   utilization = (current_tokens / max_tokens) * 100

   if utilization >= 70:
       print(f"WARNING: Context at {utilization}% - compaction imminent")
       prepare_for_compaction()
   ```

2. **Identify critical state to preserve**
   - Current task
   - Recent decisions
   - Task progress
   - Active patterns
   - Open file and line number

3. **Check when memory was last saved**
   ```bash
   last_save=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" design/memory/activeContext.md)
   echo "Memory last saved: $last_save"

   # If last save > 5 minutes ago, update needed
   ```

4. **Estimate compaction timing**
   ```python
   # If context at 70%, estimate tokens until compaction
   remaining_tokens = max_tokens - current_tokens
   safety_margin = max_tokens * 0.1  # 10% safety buffer

   tokens_until_compaction = remaining_tokens - safety_margin

   # Estimate messages until compaction
   avg_tokens_per_message = 1000
   messages_until_compaction = tokens_until_compaction / avg_tokens_per_message

   print(f"Estimated messages until compaction: {messages_until_compaction}")
   ```

5. **Decide on proactive compaction**
   ```
   If messages_until_compaction < 10:
       - Inform user that compaction is imminent
       - Recommend saving current state
       - Suggest completing current subtask before continuing
   ```

6. **Set compaction readiness flag**
   ```markdown
   # In activeContext.md

   ## Session State
   **Compaction Ready:** Yes
   **Last Prepared:** 2025-12-31 17:00:00
   ```

---

## PROCEDURE 2: Save State Before Compaction

**When to use:**
- Context window reaches 75% utilization
- Immediately before known compaction trigger
- Before risky operations that might cause compaction

**Steps:**

1. **Update all memory files atomically**
   ```bash
   # Save all three files in quick succession
   update_active_context
   update_patterns
   update_progress

   # Timestamp must be same across all files
   timestamp=$(date -Iseconds)
   update_all_timestamps_to "$timestamp"
   ```

2. **Create pre-compaction checkpoint**
   ```bash
   checkpoint_dir="design/memory/checkpoints/pre-compaction-$(date +%Y%m%d-%H%M%S)"
   mkdir -p "$checkpoint_dir"

   cp design/memory/activeContext.md "$checkpoint_dir/"
   cp design/memory/patterns.md "$checkpoint_dir/"
   cp design/memory/progress.md "$checkpoint_dir/"
   cp design/memory/config-snapshot.md "$checkpoint_dir/" 2>/dev/null || true
   ```

3. **Verify all critical state is captured**
   ```python
   critical_state_checklist = {
       'current_task': check_current_task_saved(),
       'current_file': check_current_file_saved(),
       'recent_decisions': check_recent_decisions_saved(),
       'task_progress': check_task_progress_saved(),
       'active_patterns': check_active_patterns_saved()
   }

   all_saved = all(critical_state_checklist.values())

   if not all_saved:
       print("ERROR: Not all critical state saved:")
       for item, saved in critical_state_checklist.items():
           if not saved:
               print(f"  - {item}: NOT SAVED")
       return False
   ```

4. **Write compaction metadata**
   ```markdown
   # In activeContext.md

   ## Pre-Compaction State
   **Saved At:** 2025-12-31 17:05:00
   **Context Utilization:** 76%
   **Checkpoint:** checkpoints/pre-compaction-20251231-170500
   **Current Task:** [task name]
   **Current File:** [file path]
   **Current Line:** [line number]
   ```

5. **Flush all file writes to disk**
   ```bash
   # Ensure no buffered writes
   sync

   # Verify files are on disk
   ls -lh design/memory/*.md
   ```

6. **Create recovery instructions**
   ```markdown
   # In design/memory/RECOVERY.md

   # Post-Compaction Recovery

   If context was compacted, follow these steps:

   1. Load activeContext.md
   2. Load patterns.md
   3. Load progress.md
   4. Verify current task: [task name]
   5. Resume from file: [file path] line [line number]

   **Last Save:** 2025-12-31 17:05:00
   ```

---

## Compaction Triggers

### Proactive Compaction Monitoring

**Monitor context utilization:**
```python
def monitor_compaction_risk():
    utilization = get_context_utilization()

    if utilization >= 80:
        print("CRITICAL: Compaction imminent (<20% remaining)")
        trigger_emergency_save()
    elif utilization >= 70:
        print("WARNING: Compaction likely soon (<30% remaining)")
        recommend_save()
    elif utilization >= 60:
        print("INFO: Context usage elevated (>60%)")
        prepare_for_eventual_compaction()
```

**Trigger emergency save:**
```python
def trigger_emergency_save():
    print("Performing emergency memory save due to high context usage...")

    # Save all memory immediately
    save_all_memory_files()

    # Create checkpoint
    create_checkpoint('emergency')

    # Reduce context usage if possible
    # - Summarize old outputs
    # - Archive completed tasks
    # - Consolidate active context

    print("Emergency save complete. Compaction can occur safely.")
```

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Target Audience:** Chief of Staff Agents
**Related:** [Part 2: Recovery & Verification](17-compaction-integration-part2-recovery-verification.md)
