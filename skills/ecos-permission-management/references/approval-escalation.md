# Approval Escalation Reference

## Contents

- 3.1 What is approval escalation - Understanding timeout handling
- 3.2 Escalation triggers - When escalation occurs
  - 3.2.1 First timeout (60 seconds) - Reminder notification
  - 3.2.2 Second timeout (90 seconds) - Urgent notification
  - 3.2.3 Final timeout (120 seconds) - Proceed or abort decision
- 3.3 Escalation procedure - Step-by-step handling
  - 3.3.1 Reminder notification - First follow-up
  - 3.3.2 Urgent notification - Second follow-up
  - 3.3.3 Proceed decision - When to continue without approval
  - 3.3.4 Abort decision - When to cancel operation
  - 3.3.5 Audit logging - Recording escalation
- 3.4 Autonomous operation mode - Manager directive handling
- 3.5 Examples - Escalation scenarios
- 3.6 Troubleshooting - Escalation issues

---

## 3.1 What Is Approval Escalation

Approval escalation is the process of handling situations where EAMA (the Assistant Manager) does not respond to an approval request within the expected timeframe. ECOS cannot wait indefinitely for approval, as this would block critical operations and reduce system effectiveness.

**Escalation purpose:**
- Remind EAMA of pending approval requests
- Alert the user to urgent decisions needed
- Provide a clear path forward when approval is not received
- Maintain audit trail of all escalation attempts
- Balance responsiveness with proper authorization

**Escalation timeline:**

```
T+0s          T+60s           T+90s           T+120s
  │             │               │                │
  ▼             ▼               ▼                ▼
REQUEST     REMINDER        URGENT           TIMEOUT
SENT        SENT            SENT             REACHED
            │               │                │
            escalation=1    escalation=2     escalation=3
                                             │
                                             ▼
                                      PROCEED or ABORT
```

---

## 3.2 Escalation Triggers

### 3.2.1 First Timeout (60 Seconds) - Reminder Notification

**Trigger condition:** 60 seconds elapsed since request submission with no response.

**Action:** Send reminder notification to EAMA.

**Notification characteristics:**
- Priority: `high`
- Subject: `[REMINDER] Pending Approval: {operation} {target}`
- Content includes: original request reference, elapsed time, remaining time
- Updates escalation_count to 1

**Purpose:** Gentle reminder that may have been missed or is pending user attention.

### 3.2.2 Second Timeout (90 Seconds) - Urgent Notification

**Trigger condition:** 90 seconds elapsed since request submission with no response.

**Action:** Send urgent notification to EAMA.

**Notification characteristics:**
- Priority: `urgent`
- Subject: `[URGENT] Approval Required: {operation} {target} - Will proceed in 30s`
- Content includes: warning of impending timeout, action that will be taken
- Updates escalation_count to 2

**Purpose:** Escalate visibility and communicate consequence of non-response.

### 3.2.3 Final Timeout (120 Seconds) - Proceed or Abort Decision

**Trigger condition:** 120 seconds elapsed since request submission with no response.

**Action:** Determine whether to proceed without approval or abort the operation.

**Decision criteria:**

| Operation | Default Action | Rationale |
|-----------|---------------|-----------|
| spawn | PROCEED | Work blocked; user can terminate if unwanted |
| terminate | ABORT | Destructive; safer to keep agent running |
| hibernate | PROCEED | Non-destructive; can wake if needed |
| wake | PROCEED | Work blocked; user can hibernate if unwanted |
| plugin_install | ABORT | Security-sensitive; requires explicit approval |

**Updates:** escalation_count to 3, decision to `timeout_proceed` or `timeout_abort`

---

## 3.3 Escalation Procedure

### 3.3.1 Reminder Notification - First Follow-up

**When:** escalation_count is 0 and 60 seconds have elapsed.

**Steps:**

1. Compose reminder message
2. Send to EAMA via AI Maestro
3. Update request: last_reminder_at, escalation_count = 1, status = escalated
4. Log escalation event

**Message format:**

Use the `agent-messaging` skill to send:
- **Recipient**: `eama-assistant-manager`
- **Subject**: `[REMINDER] Pending Approval: {operation} {target}`
- **Priority**: `high`
- **Content**: type `approval_reminder`, message: "Reminder: approval request pending for 60 seconds". Include `request_id`, `original_request_time` (submitted_at), `elapsed_seconds`: 60, `timeout_in_seconds`: 60, `original_operation`, `original_target`, `original_justification`.

### 3.3.2 Urgent Notification - Second Follow-up

**When:** escalation_count is 1 and 90 seconds have elapsed.

**Steps:**

1. Determine action on timeout (proceed or abort)
2. Compose urgent message with warning
3. Send to EAMA via AI Maestro
4. Update request: last_reminder_at, escalation_count = 2
5. Log escalation event

**Message format:**

Use the `agent-messaging` skill to send:
- **Recipient**: `eama-assistant-manager`
- **Subject**: `[URGENT] Approval Required: {operation} {target} - Will {action} in 30s`
- **Priority**: `urgent`
- **Content**: type `approval_urgent`, message: "URGENT: Will {action} without approval in 30 seconds if no response". Include `request_id`, `original_request_time` (submitted_at), `elapsed_seconds`: 90, `timeout_in_seconds`: 30, `action_on_timeout` ("proceed" or "abort"), `original_operation`, `original_target`.

### 3.3.3 Proceed Decision - When to Continue Without Approval

**When:** Final timeout reached and operation is in proceed-allowed category.

**Proceed-allowed operations:**
- `spawn` - Creating agents is reversible (can terminate)
- `hibernate` - Suspending agents is reversible (can wake)
- `wake` - Waking agents is reversible (can hibernate)

**Steps:**

1. Log timeout decision with justification
2. Resolve request with decision = `timeout_proceed`
3. Execute the operation
4. Send post-operation notification to EAMA using the `agent-messaging` skill

**Post-operation notification:**

Use the `agent-messaging` skill to send:
- **Recipient**: `eama-assistant-manager`
- **Subject**: `[TIMEOUT PROCEED] Completed: {operation} {target}`
- **Priority**: `normal`
- **Content**: type `timeout_notification`, message: "Operation completed after approval timeout". Include `request_id`, `operation`, `target`, `executed_at` (ISO-8601 timestamp), `escalation_count`: 3, `notes`: "Proceeded after 3 notification attempts with no response. User can reverse if needed."

**Verify**: confirm message delivery via the `agent-messaging` skill's sent messages feature.

### 3.3.4 Abort Decision - When to Cancel Operation

**When:** Final timeout reached and operation is in abort-required category.

**Abort-required operations:**
- `terminate` - Permanent; cannot be undone
- `plugin_install` - Security-sensitive; requires explicit consent

**Steps:**

1. Log timeout decision with justification
2. Resolve request with decision = `timeout_abort`
3. Do NOT execute the operation
4. Send abort notification to EAMA using the `agent-messaging` skill

**Abort notification:**

Use the `agent-messaging` skill to send:
- **Recipient**: `eama-assistant-manager`
- **Subject**: `[TIMEOUT ABORT] Cancelled: {operation} {target}`
- **Priority**: `high`
- **Content**: type `timeout_notification`, message: "Operation cancelled due to approval timeout". Include `request_id`, `operation`, `target`, `cancelled_at` (ISO-8601 timestamp), `escalation_count`: 3, `notes`: "Aborted after 3 notification attempts with no response. Please respond to proceed."

### 3.3.5 Audit Logging - Recording Escalation

**Every escalation event must be logged:**

```yaml
# Escalation event log
escalation_events:
  - timestamp: "2025-02-02T10:31:00Z"
    request_id: "spawn-req-2025-02-02-005"
    escalation_level: 1
    action: "reminder_sent"
    message_id: "msg-abc123"

  - timestamp: "2025-02-02T10:31:30Z"
    request_id: "spawn-req-2025-02-02-005"
    escalation_level: 2
    action: "urgent_sent"
    message_id: "msg-def456"
    warning: "Will proceed in 30 seconds"

  - timestamp: "2025-02-02T10:32:00Z"
    request_id: "spawn-req-2025-02-02-005"
    escalation_level: 3
    action: "timeout_proceed"
    reason: "No response after 3 attempts"
    operation_executed: true
```

**Audit log location:** `docs_dev/audit/ecos-escalations-{date}.yaml`

---

## 3.4 Autonomous Operation Mode

The manager (via EAMA) may issue an autonomous operation directive that allows ECOS to perform certain operations without pre-approval.

**Autonomous directive format:**

```yaml
directive:
  type: "autonomous_operation"
  issued_by: "eama"
  issued_at: "2025-02-02T09:00:00Z"
  expires_at: "2025-02-02T18:00:00Z"
  scope:
    - spawn
    - hibernate
    - wake
  excluded:
    - terminate
    - plugin_install
  conditions:
    max_concurrent_agents: 10
    notify_after: true
```

**Handling autonomous mode:**

1. Check if current operation is within directive scope
2. Verify directive has not expired
3. Check any conditions (e.g., max concurrent agents)
4. If all checks pass: execute without pre-approval
5. Send post-operation notification to EAMA using the `agent-messaging` skill
6. Log with directive reference

**Post-operation notification (autonomous):**

Use the `agent-messaging` skill to send:
- **Recipient**: `eama-assistant-manager`
- **Subject**: `[AUTONOMOUS] {operation}: {target}`
- **Priority**: `normal`
- **Content**: type `autonomous_notification`, message: "Operation completed under autonomous directive". Include `operation`, `target`, `details` (operation-specific details), `directive_reference` (the directive ID), `completed_at` (ISO-8601 timestamp).

**Directive storage:**

Active directives are stored in state file:

```yaml
autonomous_directives:
  directive-2025-02-02-001:
    type: "autonomous_operation"
    issued_by: "eama"
    issued_at: "2025-02-02T09:00:00Z"
    expires_at: "2025-02-02T18:00:00Z"
    scope: ["spawn", "hibernate", "wake"]
    excluded: ["terminate", "plugin_install"]
    conditions:
      max_concurrent_agents: 10
      notify_after: true
    active: true
```

---

## 3.5 Examples

### Example 1: Complete Escalation Sequence (Proceed)

```python
# T+0: Spawn request submitted
request_id = "spawn-req-2025-02-02-007"
send_approval_request(request_id, "spawn", "metrics-agent-01")
# Status: pending, escalation_count: 0

# T+60: First timeout
send_reminder(request_id)
# Message: "[REMINDER] Pending Approval: spawn metrics-agent-01"
# Status: escalated, escalation_count: 1

# T+90: Second timeout
send_urgent(request_id, action_on_timeout="proceed")
# Message: "[URGENT] Approval Required: spawn metrics-agent-01 - Will proceed in 30s"
# escalation_count: 2

# T+120: Final timeout
timeout_decision = "proceed"  # spawn is proceed-allowed
resolve_timeout(request_id, timeout_decision)
# decision: timeout_proceed, escalation_count: 3

# Execute operation
spawn_agent("metrics-agent-01", config)

# Send notification
send_timeout_notification(request_id, "spawn", "metrics-agent-01", "proceed")
# Message: "[TIMEOUT PROCEED] Completed: spawn metrics-agent-01"

# Audit trail
{
    "request_id": "spawn-req-2025-02-02-007",
    "decision": "timeout_proceed",
    "decided_by": "timeout",
    "escalation_count": 3,
    "notes": "Proceeded after 3 notification attempts with no response"
}
```

### Example 2: Complete Escalation Sequence (Abort)

```python
# T+0: Plugin install request submitted
request_id = "plugin_install-req-2025-02-02-002"
send_approval_request(request_id, "plugin_install", "security-scanner")
# Status: pending, escalation_count: 0

# T+60: First timeout
send_reminder(request_id)
# escalation_count: 1

# T+90: Second timeout
send_urgent(request_id, action_on_timeout="abort")
# Message: "[URGENT] Approval Required: plugin_install security-scanner - Will abort in 30s"
# escalation_count: 2

# T+120: Final timeout
timeout_decision = "abort"  # plugin_install is abort-required
resolve_timeout(request_id, timeout_decision)
# decision: timeout_abort, escalation_count: 3

# DO NOT execute operation

# Send notification
send_timeout_notification(request_id, "plugin_install", "security-scanner", "abort")
# Message: "[TIMEOUT ABORT] Cancelled: plugin_install security-scanner"

# Audit trail
{
    "request_id": "plugin_install-req-2025-02-02-002",
    "decision": "timeout_abort",
    "decided_by": "timeout",
    "escalation_count": 3,
    "notes": "Aborted after 3 notification attempts with no response"
}
```

### Example 3: Response Received During Escalation

```python
# T+0: Request submitted
request_id = "terminate-req-2025-02-02-004"
# Status: pending

# T+60: First reminder sent
# escalation_count: 1

# T+75: Response received (before urgent)
response = {
    "request_id": "terminate-req-2025-02-02-004",
    "decision": "approved",
    "notes": "Confirmed. Terminate the agent."
}

# Process response
resolve_request(request_id, response)
# Status: resolved, decision: approved, decided_by: eama

# Escalation stops - no further timeouts
# Execute termination with approval
terminate_agent("failing-worker-01")
```

### Example 4: Autonomous Operation

```python
# Directive received from EAMA
directive = {
    "type": "autonomous_operation",
    "scope": ["spawn", "hibernate", "wake"],
    "expires_at": "2025-02-02T18:00:00Z"
}

# Later: ECOS needs to spawn an agent
operation = "spawn"
target = "quick-task-agent"

# Check directive
if operation in directive["scope"] and not directive_expired(directive):
    # Execute without approval
    spawn_agent(target, config)

    # Notify EAMA after
    send_autonomous_notification(operation, target, directive["id"])

    # Audit trail
    {
        "operation": "spawn",
        "target": "quick-task-agent",
        "decision": "autonomous",
        "decided_by": "autonomous",
        "directive_reference": "directive-2025-02-02-001"
    }
```

### Example 5: Directive Scope Check

```python
# Directive allows: spawn, hibernate, wake
# Directive excludes: terminate, plugin_install

# ECOS wants to terminate an agent
operation = "terminate"

if operation not in directive["scope"] or operation in directive["excluded"]:
    # Must request approval - cannot use autonomous mode
    send_approval_request(request_id, "terminate", "old-agent")
    # Normal approval flow proceeds
```

---

## 3.6 Troubleshooting

### Issue: EAMA is offline during escalation

**Symptoms:**
- Messages fail to send
- No acknowledgment of reminders

**Cause:** EAMA session not running or AI Maestro connectivity issue.

**Resolution:**
1. Check EAMA status in AI Maestro registry
2. If EAMA offline: log the condition, proceed with timeout decision
3. Queue notifications for when EAMA comes online
4. Consider alerting user through alternative channel if critical

### Issue: Urgent messages not being seen

**Symptoms:**
- Escalation completes without user seeing urgent message
- User reports not receiving notifications

**Cause:** EAMA may not be surfacing urgent messages to user.

**Resolution:**
1. Verify message was delivered (check AI Maestro logs)
2. Confirm EAMA is processing urgent priority correctly
3. Consider additional notification channels for urgent matters
4. Review EAMA's notification handling skill

### Issue: Premature timeout

**Symptoms:**
- Timeout occurs before 120 seconds
- User responds but ECOS already proceeded

**Cause:** Timer calculation error or system clock issue.

**Resolution:**
1. Verify system time is synchronized
2. Use monotonic time for interval calculations
3. Check that submitted_at is recorded correctly
4. Add buffer time (e.g., 125 seconds instead of 120)

### Issue: Timeout not proceeding when it should

**Symptoms:**
- Request stays pending beyond 120 seconds
- No timeout resolution

**Cause:** Monitoring loop not checking timeouts, or escalation_count not incrementing.

**Resolution:**
1. Verify monitoring loop is running
2. Check escalation_count is being updated
3. Verify timeout_at calculation
4. Manually trigger timeout check

### Issue: Autonomous directive not being honored

**Symptoms:**
- ECOS still requesting approval for directive-covered operations
- Operations blocked waiting for approval

**Cause:** Directive not loaded, expired, or scope check failing.

**Resolution:**
1. Verify directive is stored in state file
2. Check directive expiration timestamp
3. Verify operation is in scope array
4. Check for typos in operation names

### Issue: Duplicate escalation messages

**Symptoms:**
- Multiple reminders sent at same escalation level
- EAMA receives repeated notifications

**Cause:** escalation_count not being updated, or check running multiple times.

**Resolution:**
1. Verify escalation_count is persisted after update
2. Use locking to prevent concurrent escalation checks
3. Check for duplicate monitoring loop instances

```python
# Prevent duplicate escalations
def send_escalation_if_needed(request):
    with escalation_lock:
        if request["escalation_count"] >= get_required_level(request):
            return  # Already escalated to this level

        send_escalation(request)
        request["escalation_count"] += 1
        save_state()
```

---

**Version:** 1.0
**Last Updated:** 2025-02-02
**Related:** [SKILL.md](../SKILL.md), [approval-request-procedure.md](approval-request-procedure.md), [approval-tracking.md](approval-tracking.md)
