# Detecting Config Changes - Part 2: Advanced Procedures and Classification

## Table of Contents

1. [Advanced Detection Procedures](#advanced-detection-procedures)
   - [PROCEDURE 3: Change Notification Handling](#procedure-3-change-notification-handling)
   - [PROCEDURE 4: Periodic Drift Check](#procedure-4-periodic-drift-check)
2. [Change Classification](#change-classification)
   - [MINOR Changes](#minor-changes)
   - [MODERATE Changes](#moderate-changes)
   - [MAJOR Changes](#major-changes)
   - [CRITICAL Changes](#critical-changes)
3. [Examples](#examples)
   - [Example 1: Detecting Toolchain Update](#example-1-detecting-toolchain-update)
   - [Example 2: Handling Change Notification](#example-2-handling-change-notification)
4. [Troubleshooting](#troubleshooting)
   - [Issue: False positive - timestamp changed but content unchanged](#issue-false-positive---timestamp-changed-but-content-unchanged)
   - [Issue: Change detected but notification not received](#issue-change-detected-but-notification-not-received)

**Related documents:**
- [Part 1: Methods and Basic Detection](./20-config-change-detection-part1-methods.md)

---

## Advanced Detection Procedures

### PROCEDURE 3: Change Notification Handling

**When to use:**
- Orchestrator sends config change notification
- Immediate response needed
- Config update is urgent

**Steps:**

1. **Receive notification message**
   ```json
   {
     "from": "orchestrator-master",
     "subject": "Config Update: toolchain.md",
     "priority": "high",
     "content": {
       "type": "config-update",
       "config_files": ["toolchain.md"],
       "change_type": "minor",
       "reason": "Python 3.12 security patch required",
       "breaking": true,
       "action": "adopt"
     }
   }
   ```

2. **Parse notification**
   ```python
   notification = receive_message()

   if notification.content.type == 'config-update':
       config_files = notification.content.config_files
       change_type = notification.content.change_type
       is_breaking = notification.content.breaking
       recommended_action = notification.content.action
   ```

3. **Validate notification against actual changes**
   ```python
   # Check if configs actually changed
   for config in config_files:
       actual_change = detect_config_change(config)

       if not actual_change:
           print(f"WARNING: Notification claims {config} changed but no change detected")
   ```

4. **Log notification**
   ```markdown
   ## Config Change Notifications

   ### Notification Received: 2025-12-31 14:40:00
   **From:** orchestrator-master
   **Priority:** High
   **Configs:** toolchain.md
   **Change Type:** Minor
   **Breaking:** Yes
   **Recommended Action:** Adopt
   **Reason:** Python 3.12 security patch required
   ```

5. **Trigger appropriate response**
   ```python
   if recommended_action == 'adopt':
       # Immediately trigger config conflict resolution
       handle_config_conflict(config_files, 'adopt-immediately')
   elif recommended_action == 'after-task':
       # Schedule adoption after current task
       schedule_config_adoption(config_files, 'after-task')
   else:
       # Manual review needed
       request_user_decision(config_files)
   ```

---

### PROCEDURE 4: Periodic Drift Check

**When to use:**
- During long-running sessions
- No notification system available
- Proactive drift detection

**Steps:**

1. **Define check schedule**
   ```python
   # Check every 30 minutes during active session
   CHECK_INTERVAL = timedelta(minutes=30)
   last_check = datetime.now()
   ```

2. **Perform scheduled check**
   ```python
   def periodic_drift_check():
       global last_check

       now = datetime.now()
       if now - last_check < CHECK_INTERVAL:
           return  # Too soon

       # Run timestamp-based detection
       changes = detect_config_changes_timestamp()

       if changes:
           print(f"Drift detected in: {', '.join(changes)}")
           # Run content-based detection for details
           for config in changes:
               analyze_config_changes(config)

       last_check = now
   ```

3. **Integrate into agent main loop**
   ```python
   while agent_running:
       # Regular work
       perform_task()

       # Periodic checks
       periodic_drift_check()

       # Continue work
   ```

4. **Log drift checks**
   ```markdown
   ## Config Drift Checks

   ### Check: 2025-12-31 14:00:00
   **Result:** No changes detected

   ### Check: 2025-12-31 14:30:00
   **Result:** Change detected in toolchain.md
   **Action:** Analyzed changes, triggered conflict resolution
   ```

---

## Change Classification

### MINOR Changes

**Examples:**
- Documentation updates
- Formatting improvements
- Comment additions
- Minor version bumps (patch releases)

**Action:** Can adopt immediately with minimal impact

---

### MODERATE Changes

**Examples:**
- Minor version updates (3.11 to 3.12)
- New optional dependencies
- Standard clarifications
- Process improvements

**Action:** Adopt after current task completion

---

### MAJOR Changes

**Examples:**
- Breaking API changes
- Major version updates (Python 2 to 3)
- Incompatible standards
- Architectural shifts

**Action:** Pause work, review impact, decide with user

---

### CRITICAL Changes

**Examples:**
- Security patches
- Urgent bug fixes
- Emergency standards updates

**Action:** Adopt immediately, restart affected work

---

## Examples

### Example 1: Detecting Toolchain Update

**Periodic check detects change:**
```python
# During 14:30 scheduled check
changes = detect_config_changes_timestamp()
# Returns: ['toolchain']

# Analyze changes
diff = analyze_config_changes('toolchain')
# Shows: Python 3.11.7 → 3.12.1
```

**Output:**
```
Config Change Detected (14:30:00)
==================================

Config: toolchain.md
Method: Timestamp comparison + content diff

Changes:
- Python version: 3.11.7 → 3.12.1
- Added: Type checking with mypy

Classification: MODERATE
Recommendation: Adopt after current task
```

---

### Example 2: Handling Change Notification

**Notification received:**
```json
{
  "from": "orchestrator-master",
  "subject": "URGENT: Security update required",
  "priority": "critical",
  "content": {
    "type": "config-update",
    "config_files": ["toolchain.md"],
    "change_type": "critical",
    "reason": "CVE-2025-12345 requires Python 3.12.2",
    "breaking": true,
    "action": "adopt-immediately"
  }
}
```

**Response:**
```
CRITICAL CONFIG UPDATE RECEIVED
================================

Pausing current work...
Saving progress... Done

Analyzing change:
- Current: Python 3.12.1
- Required: Python 3.12.2
- Reason: Security CVE-2025-12345

Adopting new config immediately...
Updating config snapshot... Done

Resuming work with Python 3.12.2
```

---

## Troubleshooting

### Issue: False positive - timestamp changed but content unchanged

**Cause:** Timestamp updated manually or by script

**Solution:**
```python
# Always verify with content comparison
if timestamp_indicates_change:
    content_changed = compare_content_hash(snapshot, current)
    if not content_changed:
        print("False positive: timestamp changed but content identical")
        # Ignore change
```

---

### Issue: Change detected but notification not received

**Cause:** Notification system failure or delay

**Solution:**
1. Proceed with detected change
2. Log missing notification
3. Report to orchestrator
4. Don't wait for notification

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Target Audience:** Atlas Orchestrator Agents
**Related:** SKILL.md (PROCEDURE 8: Detect Config Changes During Session)
