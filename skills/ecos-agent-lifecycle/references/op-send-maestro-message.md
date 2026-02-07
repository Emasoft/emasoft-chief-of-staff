---
operation: send-maestro-message
procedure: proc-create-team
workflow-instruction: Step 4 - Team Creation
parent-skill: ecos-agent-lifecycle
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Send AI Maestro Message

## When to Use

- Communicating with remote agents
- Sending role or project assignments
- Requesting status updates from agents
- Broadcasting notifications to team
- Sending warnings (hibernation, termination)
- Coordinating between agents

## Prerequisites

- AI Maestro is running locally at `http://localhost:23000`
- Target agent is registered in AI Maestro
- Network connectivity to localhost

## Procedure

### Step 1: Determine Message Type

Select appropriate message type:

| Type | Purpose |
|------|---------|
| `role-assignment` | Assign role to agent |
| `project-assignment` | Assign project to agent |
| `task-delegation` | Delegate specific task |
| `status-request` | Request status update |
| `status-report` | Report status back |
| `team-notification` | Notify about teammates |
| `hibernation-warning` | Warn of pending hibernation |
| `wake-notification` | Notify agent woken |
| `registry-update` | Team registry changed |
| `request` | Generic request |

### Step 2: Determine Priority

| Priority | Use Case |
|----------|----------|
| `normal` | Routine communication |
| `high` | Important but not urgent |
| `urgent` | Requires immediate attention |

### Step 3: Compose Message Content

The `content` field must be a JSON object with `type` and `message`:

```json
{
  "type": "<message-type>",
  "message": "<human-readable message text>"
}
```

### Step 4: Send Message

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "<target-agent-name>",
    "subject": "<brief subject line>",
    "priority": "<normal|high|urgent>",
    "content": {
      "type": "<message-type>",
      "message": "<detailed message text>"
    }
  }'
```

### Step 5: Verify Delivery (Optional)

```bash
# Check if message was delivered
curl -s "http://localhost:23000/api/messages?agent=<target-agent>&action=list&status=unread" | jq '.'
```

### Step 6: Wait for Response (If Expected)

For messages expecting a response, poll your inbox:

```bash
# Check for responses
curl -s "http://localhost:23000/api/messages?agent=ecos-chief-of-staff&action=list&status=unread" | jq '.messages[].content.message'
```

## Checklist

Copy this checklist and track your progress:

- [ ] Determine appropriate message type
- [ ] Select priority level
- [ ] Compose clear message content
- [ ] Verify target agent name is correct
- [ ] Send message via curl
- [ ] Check for delivery confirmation
- [ ] Wait for response if expected
- [ ] Log message exchange if significant

## Examples

### Example: Role Assignment Message

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "dev-api-charlie",
    "subject": "Role Assignment - API Developer",
    "priority": "high",
    "content": {
      "type": "role-assignment",
      "message": "You are assigned as API Developer on the backend-api project. Your responsibilities include implementing endpoints, writing tests, and maintaining API documentation. Please acknowledge this assignment."
    }
  }'
```

### Example: Status Request Message

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eoa-webapp-orchestrator",
    "subject": "Status Request - Sprint Progress",
    "priority": "normal",
    "content": {
      "type": "status-request",
      "message": "Please provide current sprint progress including: completed tasks, in-progress work, blocked items, and estimated completion."
    }
  }'
```

### Example: Hibernation Warning Message

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "dev-frontend-bob",
    "subject": "Hibernation Warning - 60 Seconds",
    "priority": "urgent",
    "content": {
      "type": "hibernation-warning",
      "message": "You will be hibernated in 60 seconds due to idle timeout. Please save any transient state and acknowledge."
    }
  }'
```

### Example: Team Broadcast Message

```bash
# Get all running agents
AGENTS=$(uv run python scripts/ecos_team_registry.py list --filter-status running --names-only)

# Send to each
for AGENT in $AGENTS; do
  curl -X POST "http://localhost:23000/api/messages" \
    -H "Content-Type: application/json" \
    -d '{
      "from": "ecos-chief-of-staff",
      "to": "'"$AGENT"'",
      "subject": "Team Announcement",
      "priority": "normal",
      "content": {
        "type": "team-notification",
        "message": "Sprint planning meeting in 30 minutes. Please prepare your status updates."
      }
    }'
done
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Connection refused | AI Maestro not running | Start AI Maestro with `aimaestro start` |
| Agent not found | Wrong agent name or not registered | Check agent name with `aimaestro-agent.sh list` |
| Invalid JSON | Malformed content field | Ensure content is valid JSON object |
| Message not delivered | Agent session dead | Check agent status, respawn if needed |
| No response received | Agent not processing messages | Send ping, check if agent is responsive |
| Rate limit exceeded | Too many messages | Slow down message frequency, batch if possible |

## Related Operations

- [op-spawn-agent.md](op-spawn-agent.md) - Send welcome message after spawn
- [op-terminate-agent.md](op-terminate-agent.md) - Send termination warning
- [op-hibernate-agent.md](op-hibernate-agent.md) - Send hibernation warning
- [op-wake-agent.md](op-wake-agent.md) - Send wake notification
