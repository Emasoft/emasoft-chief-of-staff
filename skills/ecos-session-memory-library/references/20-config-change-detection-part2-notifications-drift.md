# Config Change Detection: Notifications and Periodic Drift Checks

**Parent Document:** [20-config-change-detection.md](./20-config-change-detection.md)

---

## Table of Contents

1. [PROCEDURE 3: Change Notification Handling](#procedure-3-change-notification-handling)
2. [PROCEDURE 4: Periodic Drift Check](#procedure-4-periodic-drift-check)

---

## PROCEDURE 3: Change Notification Handling

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

## PROCEDURE 4: Periodic Drift Check

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

**Version:** 1.0
**Last Updated:** 2026-01-01
**Related:** [20-config-change-detection.md](./20-config-change-detection.md)
