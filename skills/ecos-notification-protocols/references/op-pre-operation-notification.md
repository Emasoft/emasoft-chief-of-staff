---
operation: pre-operation-notification
procedure: proc-notify-team-ready
workflow-instruction: Step 5 - Team Ready Notification
parent-skill: ecos-notification-protocols
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Pre-Operation Notification

## When to Use

Trigger this operation BEFORE:
- Skill installation on an agent
- Plugin installation requiring agent restart
- Configuration changes affecting agent behavior
- System maintenance causing temporary disruption
- Any operation that will interrupt an agent's current work

## Prerequisites

- AI Maestro messaging system is running
- Target agent(s) are registered and reachable
- Operation details are known (type, expected duration, impact)
- Acknowledgment timeout policy is understood (60 seconds for pre-operation ACK)

## Procedure

### Step 1: Identify Affected Agents

Determine which agents will be impacted by the operation:

```bash
# List all agents that will be affected
# For skill installation: the target agent
# For system maintenance: all active agents
curl -s "http://localhost:23000/api/sessions" | jq '.sessions[] | select(.status == "active") | .name'
```

### Step 2: Compose Notification Message

Include these required elements:
- What operation will occur
- Why it is necessary
- Expected duration/downtime
- What the agent should do (save work, prepare)
- Request for acknowledgment

### Step 3: Send Notification via AI Maestro

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "<target-agent>",
    "subject": "<Operation Type> Pending",
    "priority": "high",
    "content": {
      "type": "pre-operation",
      "message": "I will <operation description>. This requires <impact description>. Please <action required> and reply with \"ok\" when ready. I will wait up to 60 seconds.",
      "operation": "<operation-type>",
      "expected_downtime": "<duration>",
      "requires_acknowledgment": true
    }
  }'
```

### Step 4: Track Acknowledgments

Monitor for agent response:

```bash
# Check for acknowledgment (run in loop with timeout)
START_TIME=$(date +%s)
TIMEOUT=60

while true; do
  RESPONSE=$(curl -s "http://localhost:23000/api/messages?agent=chief-of-staff&action=list&status=unread" | jq '.messages[] | select(.from == "<target-agent>")')

  if [ -n "$RESPONSE" ]; then
    echo "Acknowledgment received"
    break
  fi

  ELAPSED=$(($(date +%s) - START_TIME))
  if [ $ELAPSED -ge $TIMEOUT ]; then
    echo "Timeout - no acknowledgment"
    break
  fi

  sleep 5
done
```

### Step 5: Handle Timeout

If no acknowledgment after 60 seconds:

1. Send final notice (see Example 2)
2. Log the timeout occurrence
3. Proceed with operation

## Checklist

Copy this checklist and track your progress:

- [ ] Identified all affected agents
- [ ] Composed notification with all required elements
- [ ] Sent notification with high priority
- [ ] Started acknowledgment tracking
- [ ] Sent reminders at 15s, 30s, 45s (if no response)
- [ ] Received acknowledgment OR handled timeout
- [ ] Logged notification outcome
- [ ] Ready to proceed with operation

## Examples

### Example 1: Skill Installation Notification

**Scenario:** Installing security-audit skill on code-impl-auth agent.

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "code-impl-auth",
    "subject": "Skill Installation Pending",
    "priority": "high",
    "content": {
      "type": "pre-operation",
      "message": "I will install the security-audit skill on your agent. This requires hibernating and waking you. Please finish your current work and reply with \"ok\" when ready. I will wait up to 60 seconds.",
      "operation": "skill-install",
      "skill_name": "security-audit",
      "expected_downtime": "30 seconds",
      "requires_acknowledgment": true
    }
  }'
```

### Example 2: Timeout Final Notice

**Scenario:** Agent did not respond within 60 seconds.

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "code-impl-auth",
    "subject": "Proceeding Without Acknowledgment",
    "priority": "high",
    "content": {
      "type": "timeout-notice",
      "message": "No response received after 60 seconds. Proceeding with skill installation now. You will be hibernated and woken shortly.",
      "operation": "skill-install",
      "timeout_occurred": true
    }
  }'
```

### Example 3: System Maintenance Broadcast

**Scenario:** Notifying all agents about upcoming system maintenance.

```bash
AGENTS=("code-impl-auth" "test-engineer-01" "docs-writer")
BROADCAST_ID="maint-$(date +%Y%m%d%H%M%S)"

for agent in "${AGENTS[@]}"; do
  curl -X POST "http://localhost:23000/api/messages" \
    -H "Content-Type: application/json" \
    -d "{
      \"to\": \"$agent\",
      \"subject\": \"System Maintenance in 5 Minutes\",
      \"priority\": \"high\",
      \"content\": {
        \"type\": \"pre-operation\",
        \"message\": \"System maintenance will begin in 5 minutes. All agents will be hibernated. Please save your work and reply with 'ok' when ready.\",
        \"operation\": \"system-maintenance\",
        \"broadcast_id\": \"$BROADCAST_ID\",
        \"expected_downtime\": \"10 minutes\",
        \"requires_acknowledgment\": true
      }
    }"
done
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Message not delivered | Agent session not found | Verify agent is registered: `curl -s "http://localhost:23000/api/sessions"` |
| Agent does not respond | Agent busy or unresponsive | Send reminders at 15s, 30s, 45s; proceed after 60s timeout |
| Agent responds with "not ready" | Work in progress | Negotiate delay; ask when agent will be ready |
| Multiple agents timeout | Broadcast delivery issue | Check AI Maestro health; retry broadcast |
| Notification arrives too late | Network delay | Send notifications earlier; increase lead time |

## Related Operations

- [op-post-operation-notification.md](op-post-operation-notification.md) - Send after operation completes
- [op-acknowledgment-protocol.md](op-acknowledgment-protocol.md) - Detailed ACK handling
- [op-failure-notification.md](op-failure-notification.md) - Send if operation fails
- [pre-operation-notifications.md](pre-operation-notifications.md) - Complete reference documentation
