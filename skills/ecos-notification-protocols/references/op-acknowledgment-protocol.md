---
operation: acknowledgment-protocol
procedure: proc-notify-team-ready
workflow-instruction: Step 5 - Team Ready Notification
parent-skill: ecos-notification-protocols
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Acknowledgment Protocol

## When to Use

Trigger this operation when:
- Agent confirmation is required before proceeding
- Operations require agent readiness verification
- Coordinating multi-agent synchronized actions
- Disruptive operations need agent consent
- State-changing operations affect agent context

## Prerequisites

- AI Maestro messaging system is running
- Target agent is active and reachable
- Timeout values are understood (see Standardized ACK Timeout Policy)
- Fallback behavior is defined for timeout scenarios

## Standardized ACK Timeout Policy

**CRITICAL:** Use these exact timeout values:

| ACK Type | Timeout | Reminders | Use Case |
|----------|---------|-----------|----------|
| Pre-operation ACK | **60 seconds** | 15s, 30s, 45s | Before disruptive operations |
| Approval request | **2 minutes** | 60s, 90s | Requesting manager approval |
| Emergency handoff ACK | **30 seconds** | 10s, 20s | Time-critical emergencies |
| Health check response | **30 seconds** | None | Verifying agent is alive |

## Procedure

### Step 1: Send Acknowledgment Request

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "<target-agent>",
    "subject": "<Request Subject>",
    "priority": "high",
    "content": {
      "type": "ack-request",
      "message": "<What needs acknowledgment>. Please reply with \"ok\" when ready.",
      "timeout_seconds": 60,
      "requires_acknowledgment": true
    }
  }'
```

### Step 2: Start Timeout Timer

Track elapsed time from request sent:

```bash
START_TIME=$(date +%s)
TIMEOUT=60  # seconds
REMINDER_INTERVALS=(15 30 45)
```

### Step 3: Send Reminders

At each reminder interval, if no response:

```bash
# At 15 seconds
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "<target-agent>",
    "subject": "Reminder: <Original Subject>",
    "priority": "high",
    "content": {
      "type": "reminder",
      "message": "Reminder: Please reply \"ok\" when ready. 45 seconds remaining.",
      "original_subject": "<Original Subject>",
      "time_remaining": "45 seconds"
    }
  }'

# At 30 seconds
# ... (time_remaining: 30 seconds)

# At 45 seconds
# ... (time_remaining: 15 seconds)
```

### Step 4: Process Response

Valid acknowledgment responses:
- `"ok"` - Agent is ready, proceed
- `"not ready"` - Agent needs more time, negotiate
- `"busy"` - Agent cannot respond now, may need escalation
- No response - Timeout behavior applies

```bash
# Check for response
RESPONSE=$(curl -s "http://localhost:23000/api/messages?agent=chief-of-staff&action=list&status=unread" | jq '.messages[] | select(.from == "<target-agent>")')

if echo "$RESPONSE" | grep -q '"ok"'; then
  echo "Acknowledgment received - proceeding"
elif echo "$RESPONSE" | grep -q '"not ready"'; then
  echo "Agent not ready - negotiating delay"
else
  echo "Unexpected response - evaluating"
fi
```

### Step 5: Proceed or Handle Timeout

**If acknowledgment received:** Proceed with operation.

**If timeout occurs:**
1. Send final notice
2. Log timeout event
3. Proceed with operation (for pre-operation ACK)
4. Or abort (for approval requests without autonomous mode)

```bash
# Final notice on timeout
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "<target-agent>",
    "subject": "Proceeding Without Acknowledgment",
    "priority": "high",
    "content": {
      "type": "timeout-notice",
      "message": "No response received within timeout. Proceeding with operation.",
      "timeout_occurred": true
    }
  }'
```

## Checklist

Copy this checklist and track your progress:

- [ ] Sent acknowledgment request with clear instructions
- [ ] Started timeout timer
- [ ] Sent reminder at 15 seconds (if no response)
- [ ] Sent reminder at 30 seconds (if no response)
- [ ] Sent reminder at 45 seconds (if no response)
- [ ] Processed response OR handled timeout at 60 seconds
- [ ] Logged acknowledgment outcome
- [ ] Proceeded with operation OR aborted based on policy

## Examples

### Example 1: Pre-Operation ACK Flow

**Scenario:** Getting acknowledgment before skill installation.

```bash
# Send ACK request
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "code-impl-auth",
    "subject": "Ready for Skill Installation?",
    "priority": "high",
    "content": {
      "type": "ack-request",
      "message": "I am about to install the security-audit skill. This will hibernate and wake you. Please save your work and reply \"ok\" when ready.",
      "timeout_seconds": 60,
      "requires_acknowledgment": true
    }
  }'

# Wait for response with reminders...

# On "ok" response:
echo "Proceeding with skill installation"
```

### Example 2: Approval Request ACK

**Scenario:** Requesting EAMA approval for expensive operation.

```bash
# Send approval request (2 minute timeout)
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "emasoft-assistant-manager-agent",
    "subject": "Approval Request: Full Project Rescan",
    "priority": "high",
    "content": {
      "type": "approval-request",
      "message": "Requesting approval for full project skill rescan. Estimated time: 15 minutes. Estimated cost: significant token usage. Reply \"approved\" to proceed or \"denied\" with reason.",
      "timeout_seconds": 120,
      "operation": "full-rescan",
      "requires_acknowledgment": true
    }
  }'
```

### Example 3: Emergency Handoff ACK

**Scenario:** Emergency handoff with tight timeout.

```bash
# Send emergency ACK request (30 second timeout)
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "backup-coordinator",
    "subject": "URGENT: Emergency Handoff",
    "priority": "urgent",
    "content": {
      "type": "emergency-ack",
      "message": "Chief of Staff is running out of context. Emergency handoff required. Reply \"ok\" immediately to accept handoff.",
      "timeout_seconds": 30,
      "requires_acknowledgment": true
    }
  }'

# Reminders at 10s and 20s
# Proceed immediately after 30s regardless
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| No response within timeout | Agent busy/offline/crashed | Proceed per timeout policy; log occurrence |
| Agent responds "not ready" | Work in progress | Ask when ready; reschedule if possible |
| Agent responds "busy" | Cannot handle request | Escalate to user or find alternative agent |
| Reminder delivery fails | Messaging issue | Check AI Maestro health; proceed with timeout |
| Agent acknowledges late | Response after timeout | Log late ACK; operation may already be in progress |
| Invalid response format | Agent misunderstood request | Clarify expectations; retry request |

## Related Operations

- [op-pre-operation-notification.md](op-pre-operation-notification.md) - Uses ACK protocol
- [op-post-operation-notification.md](op-post-operation-notification.md) - Verification is similar
- [op-failure-notification.md](op-failure-notification.md) - May follow timeout
- [acknowledgment-protocol.md](acknowledgment-protocol.md) - Complete reference documentation
