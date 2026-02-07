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

- AI Maestro is running locally
- The `agent-messaging` skill is available
- Target agent is registered in AI Maestro

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

The content must include:
- **type**: the message type from Step 1
- **message**: human-readable message text

Additional fields may be included as needed.

### Step 4: Send Message

Use the `agent-messaging` skill to send a message:
- **Recipient**: the target agent session name
- **Subject**: a brief, descriptive subject line
- **Priority**: `normal`, `high`, or `urgent`
- **Content**: structured object with `type` and `message` fields

### Step 5: Verify Delivery (Optional)

Use the `agent-messaging` skill to check the message status or list unread messages for the target agent.

### Step 6: Wait for Response (If Expected)

For messages expecting a response, use the `agent-messaging` skill to poll your inbox for unread messages.

## Checklist

Copy this checklist and track your progress:

- [ ] Determine appropriate message type
- [ ] Select priority level
- [ ] Compose clear message content
- [ ] Verify target agent name is correct
- [ ] Send message via `agent-messaging` skill
- [ ] Check for delivery confirmation
- [ ] Wait for response if expected
- [ ] Log message exchange if significant

## Examples

### Example: Role Assignment Message

Use the `agent-messaging` skill to send a role assignment:
- **Recipient**: `dev-api-charlie`
- **Subject**: `Role Assignment - API Developer`
- **Priority**: `high`
- **Content**: type `role-assignment`, message: "You are assigned as API Developer on the backend-api project. Your responsibilities include implementing endpoints, writing tests, and maintaining API documentation. Please acknowledge this assignment."

### Example: Status Request Message

Use the `agent-messaging` skill to request status:
- **Recipient**: `eoa-webapp-orchestrator`
- **Subject**: `Status Request - Sprint Progress`
- **Priority**: `normal`
- **Content**: type `status-request`, message: "Please provide current sprint progress including: completed tasks, in-progress work, blocked items, and estimated completion."

### Example: Hibernation Warning Message

Use the `agent-messaging` skill to send a hibernation warning:
- **Recipient**: `dev-frontend-bob`
- **Subject**: `Hibernation Warning - 60 Seconds`
- **Priority**: `urgent`
- **Content**: type `hibernation-warning`, message: "You will be hibernated in 60 seconds due to idle timeout. Please save any transient state and acknowledge."

### Example: Team Broadcast Message

To broadcast to all running agents:

1. Get all running agent names from the team registry:
   ```bash
   AGENTS=$(uv run python scripts/ecos_team_registry.py list --filter-status running --names-only)
   ```
2. For each agent, use the `agent-messaging` skill to send a team notification:
   - **Recipient**: the agent session name
   - **Subject**: `Team Announcement`
   - **Priority**: `normal`
   - **Content**: type `team-notification`, message: "Sprint planning meeting in 30 minutes. Please prepare your status updates."

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Connection refused | AI Maestro not running | Start AI Maestro service |
| Agent not found | Wrong agent name or not registered | Use the `ai-maestro-agents-management` skill to list agents for correct name |
| Invalid content format | Malformed content field | Ensure content is a valid object with `type` and `message` fields |
| Message not delivered | Agent session dead | Check agent status, respawn if needed |
| No response received | Agent not processing messages | Send ping, check if agent is responsive |
| Rate limit exceeded | Too many messages | Slow down message frequency, batch if possible |

## Related Operations

- [op-spawn-agent.md](op-spawn-agent.md) - Send welcome message after spawn
- [op-terminate-agent.md](op-terminate-agent.md) - Send termination warning
- [op-hibernate-agent.md](op-hibernate-agent.md) - Send hibernation warning
- [op-wake-agent.md](op-wake-agent.md) - Send wake notification
