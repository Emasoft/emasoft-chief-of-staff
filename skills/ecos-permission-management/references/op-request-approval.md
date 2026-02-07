---
name: op-request-approval
description: Operation procedure for requesting approval from EAMA before executing privileged operations.
workflow-instruction: "support"
procedure: "support-skill"
---

# Operation: Request Approval

## Purpose

Request approval from the Assistant Manager (EAMA) before executing privileged operations such as agent spawn, terminate, hibernate, wake, or plugin install.

## When to Use

- Before spawning a new agent
- Before terminating an agent
- Before hibernating an agent
- Before waking a hibernated agent
- Before installing a Claude Code plugin

## Prerequisites

- AI Maestro messaging system running
- EAMA online and responsive
- Clear justification for the operation

## Procedure

### Step 1: Identify Operation Type

| Operation | Type Code | Required Justification |
|-----------|-----------|------------------------|
| Spawn agent | `spawn` | Why new agent needed, task assignment |
| Terminate agent | `terminate` | Why termination needed, work status |
| Hibernate agent | `hibernate` | Why suspend, expected wake time |
| Wake agent | `wake` | Why resume, task to perform |
| Install plugin | `plugin_install` | What plugin, why needed |

### Step 2: Generate Request ID

```bash
REQUEST_ID=$(uuidgen | tr '[:upper:]' '[:lower:]')
echo "Request ID: $REQUEST_ID"
```

### Step 3: Compose Approval Request

```bash
OPERATION_TYPE="spawn"  # or terminate, hibernate, wake, plugin_install
TARGET="implementer-2"  # agent name or plugin name
JUSTIFICATION="High priority issue #42 requires dedicated agent for parallel work"

REQUEST_BODY=$(cat <<EOF
{
  "to": "eama-main",
  "subject": "[APPROVAL REQUIRED] $OPERATION_TYPE: $TARGET",
  "priority": "high",
  "content": {
    "type": "approval-request",
    "message": "ECOS requests approval for operation: $OPERATION_TYPE",
    "request_id": "$REQUEST_ID",
    "operation": "$OPERATION_TYPE",
    "target": "$TARGET",
    "justification": "$JUSTIFICATION",
    "requested_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "options": ["approve", "reject", "modify"]
  }
}
EOF
)
```

### Step 4: Send Request via AI Maestro

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d "$REQUEST_BODY"
```

### Step 5: Register Pending Approval

```bash
# Add to pending approvals file
PENDING_FILE="docs_dev/pending-approvals.json"
jq '.pending["'"$REQUEST_ID"'"] = {
  "operation": "'"$OPERATION_TYPE"'",
  "target": "'"$TARGET"'",
  "requested_at": "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'",
  "status": "pending"
}' $PENDING_FILE > temp.json && mv temp.json $PENDING_FILE
```

### Step 6: Await Response

Poll for response or wait for AI Maestro callback:

```bash
# Check for response (poll every 10 seconds)
TIMEOUT=120  # 2 minutes
ELAPSED=0

while [ $ELAPSED -lt $TIMEOUT ]; do
  # Check inbox for approval response
  RESPONSE=$(curl -s "http://localhost:23000/api/messages?agent=ecos-main&action=list&status=unread" | \
    jq -r '.messages[] | select(.content.request_id == "'"$REQUEST_ID"'")')

  if [ -n "$RESPONSE" ]; then
    DECISION=$(echo $RESPONSE | jq -r '.content.decision')
    echo "Decision received: $DECISION"
    break
  fi

  sleep 10
  ELAPSED=$((ELAPSED + 10))
done
```

### Step 7: Handle Decision

```bash
case "$DECISION" in
  "approved")
    echo "Proceeding with $OPERATION_TYPE on $TARGET"
    # Execute operation
    ;;
  "rejected")
    echo "Operation rejected: $(echo $RESPONSE | jq -r '.content.reason')"
    # Abort operation
    ;;
  "modified")
    echo "Operation modified: $(echo $RESPONSE | jq -r '.content.modifications')"
    # Apply modifications and proceed
    ;;
  *)
    echo "No response within timeout"
    # Handle timeout (see escalation procedure)
    ;;
esac
```

## Example

**Scenario:** Request approval to spawn agent `implementer-2` for issue #42.

```bash
# Generate request ID
REQUEST_ID=$(uuidgen | tr '[:upper:]' '[:lower:]')

# Send request
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "eama-main",
    "subject": "[APPROVAL REQUIRED] spawn: implementer-2",
    "priority": "high",
    "content": {
      "type": "approval-request",
      "message": "ECOS requests approval to spawn new agent",
      "request_id": "'"$REQUEST_ID"'",
      "operation": "spawn",
      "target": "implementer-2",
      "justification": "High priority issue #42 requires dedicated agent for parallel work on API component.",
      "requested_at": "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'",
      "task_assignment": "Issue #42 - API endpoints for user authentication",
      "options": ["approve", "reject", "modify"]
    }
  }'

# Wait for response
echo "Waiting for EAMA approval..."
```

## Request Message Format

```json
{
  "type": "approval-request",
  "message": "Human-readable summary",
  "request_id": "uuid",
  "operation": "spawn|terminate|hibernate|wake|plugin_install",
  "target": "agent_name or plugin_name",
  "justification": "Why this operation is needed",
  "requested_at": "ISO-8601 timestamp",
  "options": ["approve", "reject", "modify"],
  "context": {
    "issue_number": 42,
    "priority": "high"
  }
}
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| AI Maestro unreachable | Service down | Log and retry; if critical, request human fallback |
| EAMA offline | No manager available | Escalate per timeout procedure |
| Invalid request format | Missing required fields | Fix format and resend |
| Duplicate request | Same request sent twice | Use existing request ID |

## Notes

- Never proceed without approval (except in autonomous mode)
- Always include clear justification
- Track all requests in pending file for audit
- Set appropriate priority based on urgency
