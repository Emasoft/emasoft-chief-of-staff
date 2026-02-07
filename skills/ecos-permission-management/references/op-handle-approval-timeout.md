---
name: op-handle-approval-timeout
description: Operation procedure for handling approval request timeouts and escalation.
workflow-instruction: "support"
procedure: "support-skill"
---

# Operation: Handle Approval Timeout

## Purpose

Handle situations where approval requests do not receive timely responses, including sending reminders, escalating urgency, and making proceed/abort decisions.

## When to Use

- When approval request has been pending for >60 seconds
- When urgent escalation needed at >90 seconds
- When maximum timeout (120 seconds) reached
- When operating in autonomous mode

## Prerequisites

- Pending approval request with known request ID
- AI Maestro messaging system
- Tracking file at `docs_dev/pending-approvals.json`
- Audit log at `docs_dev/audit/`

## Procedure

### Step 1: Check Request Age

```bash
REQUEST_ID="$1"
PENDING_FILE="docs_dev/pending-approvals.json"

REQUESTED_AT=$(jq -r '.pending["'"$REQUEST_ID"'"].requested_at' $PENDING_FILE)
AGE_SECONDS=$(( $(date +%s) - $(date -d "$REQUESTED_AT" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%SZ" "$REQUESTED_AT" +%s) ))

echo "Request age: $AGE_SECONDS seconds"
```

### Step 2: Send Reminder at 60 Seconds

```bash
if [ $AGE_SECONDS -ge 60 ] && [ $AGE_SECONDS -lt 90 ]; then
  REMINDER_SENT=$(jq -r '.pending["'"$REQUEST_ID"'"].reminder_sent' $PENDING_FILE)

  if [ "$REMINDER_SENT" != "true" ]; then
    # Send reminder
    curl -X POST "http://localhost:23000/api/messages" \
      -H "Content-Type: application/json" \
      -d '{
        "to": "eama-main",
        "subject": "[REMINDER] Approval pending: '"$REQUEST_ID"'",
        "priority": "high",
        "content": {
          "type": "approval-reminder",
          "message": "Approval request pending for 60+ seconds. Please respond.",
          "request_id": "'"$REQUEST_ID"'",
          "original_operation": "'"$(jq -r '.pending["'"$REQUEST_ID"'"].operation' $PENDING_FILE)"'",
          "target": "'"$(jq -r '.pending["'"$REQUEST_ID"'"].target' $PENDING_FILE)"'"
        }
      }'

    # Mark reminder sent
    jq '.pending["'"$REQUEST_ID"'"].reminder_sent = true' $PENDING_FILE > temp.json && mv temp.json $PENDING_FILE

    echo "Reminder sent for $REQUEST_ID"
  fi
fi
```

### Step 3: Send Urgent Notification at 90 Seconds

```bash
if [ $AGE_SECONDS -ge 90 ] && [ $AGE_SECONDS -lt 120 ]; then
  URGENT_SENT=$(jq -r '.pending["'"$REQUEST_ID"'"].urgent_sent' $PENDING_FILE)

  if [ "$URGENT_SENT" != "true" ]; then
    # Send urgent notification
    curl -X POST "http://localhost:23000/api/messages" \
      -H "Content-Type: application/json" \
      -d '{
        "to": "eama-main",
        "subject": "[URGENT] Approval timeout imminent: '"$REQUEST_ID"'",
        "priority": "urgent",
        "content": {
          "type": "approval-urgent",
          "message": "URGENT: Approval will timeout in 30 seconds. Respond immediately or operation will be aborted.",
          "request_id": "'"$REQUEST_ID"'",
          "timeout_at": "'"$(date -u -d '+30 seconds' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v+30S +%Y-%m-%dT%H:%M:%SZ)"'"
        }
      }'

    # Mark urgent sent
    jq '.pending["'"$REQUEST_ID"'"].urgent_sent = true' $PENDING_FILE > temp.json && mv temp.json $PENDING_FILE

    echo "Urgent notification sent for $REQUEST_ID"
  fi
fi
```

### Step 4: Handle Timeout at 120 Seconds

```bash
if [ $AGE_SECONDS -ge 120 ]; then
  OPERATION=$(jq -r '.pending["'"$REQUEST_ID"'"].operation' $PENDING_FILE)
  TARGET=$(jq -r '.pending["'"$REQUEST_ID"'"].target' $PENDING_FILE)

  # Determine default action based on operation type
  case "$OPERATION" in
    "spawn"|"wake")
      # Safe to proceed - creates resources
      ACTION="proceed"
      ;;
    "terminate"|"hibernate"|"plugin_install")
      # Destructive - abort by default
      ACTION="abort"
      ;;
  esac

  echo "Timeout reached. Default action: $ACTION"

  # Update tracking
  jq '.pending["'"$REQUEST_ID"'"].status = "timeout_'"$ACTION"'"' $PENDING_FILE > temp.json && mv temp.json $PENDING_FILE

  # Log to audit
  AUDIT_FILE="docs_dev/audit/ecos-approvals-$(date +%Y-%m-%d).yaml"
  cat >> $AUDIT_FILE <<EOF
- timestamp: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  operation: "$OPERATION"
  target: "$TARGET"
  request_id: "$REQUEST_ID"
  decision: "timeout_$ACTION"
  decided_by: "timeout"
  escalation_count: 2
EOF

  # Notify about timeout
  curl -X POST "http://localhost:23000/api/messages" \
    -H "Content-Type: application/json" \
    -d '{
      "to": "eama-main",
      "subject": "[TIMEOUT] Approval auto-'"$ACTION"': '"$REQUEST_ID"'",
      "priority": "high",
      "content": {
        "type": "approval-timeout",
        "message": "Approval request timed out after 120 seconds. Action: '"$ACTION"'.",
        "request_id": "'"$REQUEST_ID"'",
        "operation": "'"$OPERATION"'",
        "target": "'"$TARGET"'",
        "action_taken": "'"$ACTION"'"
      }
    }'

  # Execute or abort based on decision
  if [ "$ACTION" = "proceed" ]; then
    echo "Executing $OPERATION on $TARGET (timeout proceed)"
    # Execute the operation
  else
    echo "Aborting $OPERATION on $TARGET (timeout abort)"
    # Clean up any partial state
  fi
fi
```

## Example

**Scenario:** Approval request for spawning `implementer-2` times out.

```bash
REQUEST_ID="abc-123"
PENDING_FILE="docs_dev/pending-approvals.json"

# Current state: request submitted 100 seconds ago
# Reminder sent at 60s, urgent sent at 90s

# At 120 seconds:
OPERATION="spawn"
TARGET="implementer-2"
ACTION="proceed"  # spawn is safe to proceed

# Log timeout
echo "- timestamp: \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
  operation: \"$OPERATION\"
  target: \"$TARGET\"
  request_id: \"$REQUEST_ID\"
  decision: \"timeout_proceed\"
  decided_by: \"timeout\"
  escalation_count: 2" >> docs_dev/audit/ecos-approvals-$(date +%Y-%m-%d).yaml

# Notify EAMA
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "eama-main",
    "subject": "[TIMEOUT] Approval auto-proceed: abc-123",
    "priority": "high",
    "content": {
      "type": "approval-timeout",
      "message": "Spawn request for implementer-2 timed out. Proceeding with spawn.",
      "request_id": "abc-123",
      "action_taken": "proceed"
    }
  }'

# Execute spawn
echo "Spawning implementer-2..."
```

## Escalation Timeline

| Time | Event | Action |
|------|-------|--------|
| 0s | Request submitted | Wait for response |
| 60s | Reminder threshold | Send reminder to EAMA |
| 90s | Urgent threshold | Send urgent notification |
| 120s | Timeout | Auto-proceed or auto-abort |

## Default Timeout Actions

| Operation | Default Action | Rationale |
|-----------|----------------|-----------|
| spawn | proceed | Creates resource, easily terminated if wrong |
| wake | proceed | Resumes existing resource |
| terminate | abort | Destructive, prefer manual approval |
| hibernate | abort | Affects running agent |
| plugin_install | abort | Could introduce security risks |

## Autonomous Mode

When operating under autonomous directive:

```bash
# Skip approval entirely, but notify after
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "eama-main",
    "subject": "[AUTONOMOUS] Executed: spawn implementer-2",
    "priority": "normal",
    "content": {
      "type": "autonomous-notification",
      "message": "Operating in autonomous mode. Spawned implementer-2 for issue #42.",
      "operation": "spawn",
      "target": "implementer-2",
      "executed_at": "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"
    }
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Time calculation fails | Date format issues | Use consistent ISO-8601 format |
| Audit write fails | Permission or path | Ensure docs_dev/audit/ exists |
| AI Maestro down | Service unavailable | Log locally, retry later |
| Multiple timeouts racing | Concurrent requests | Process sequentially |

## Notes

- Always log timeout decisions to audit trail
- Prefer abort for destructive operations
- Document autonomous mode usage
- Review timeout decisions in regular audits
