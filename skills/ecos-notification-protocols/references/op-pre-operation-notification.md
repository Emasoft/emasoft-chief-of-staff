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
- The `agent-messaging` skill is available
- The `ai-maestro-agents-management` skill is available
- Target agent(s) are registered and reachable
- Operation details are known (type, expected duration, impact)
- Acknowledgment timeout policy is understood (60 seconds for pre-operation ACK)

## Procedure

### Step 1: Identify Affected Agents

Determine which agents will be impacted by the operation.

Use the `ai-maestro-agents-management` skill to list all active agents. Filter by status "active" to build the affected agents list.

### Step 2: Compose Notification Message

Include these required elements:
- What operation will occur
- Why it is necessary
- Expected duration/downtime
- What the agent should do (save work, prepare)
- Request for acknowledgment

### Step 3: Send Notification

Use the `agent-messaging` skill to send the pre-operation notification:
- **Recipient**: the target agent session name
- **Subject**: `[Operation Type] Pending`
- **Priority**: `high`
- **Content**: type `pre-operation`, message: "I will [operation description]. This requires [impact description]. Please [action required] and reply with 'ok' when ready. I will wait up to 60 seconds." Include fields: `operation` (the operation type), `expected_downtime` (duration string), `requires_acknowledgment` (true).

### Step 4: Track Acknowledgments

Use the `agent-messaging` skill to periodically check for unread messages from the target agent. Poll every 5 seconds for up to 60 seconds. Look for a response containing "ok" or type `acknowledgment`.

### Step 5: Handle Timeout

If no acknowledgment after 60 seconds:

1. Use the `agent-messaging` skill to send a final notice (see Example 2)
2. Log the timeout occurrence
3. Proceed with operation

## Checklist

Copy this checklist and track your progress:

- [ ] Identified all affected agents
- [ ] Composed notification with all required elements
- [ ] Sent notification with high priority via `agent-messaging` skill
- [ ] Started acknowledgment tracking
- [ ] Sent reminders at 15s, 30s, 45s (if no response)
- [ ] Received acknowledgment OR handled timeout
- [ ] Logged notification outcome
- [ ] Ready to proceed with operation

## Examples

### Example 1: Skill Installation Notification

**Scenario:** Installing security-audit skill on code-impl-auth agent.

Use the `agent-messaging` skill to send:
- **Recipient**: `code-impl-auth`
- **Subject**: `Skill Installation Pending`
- **Priority**: `high`
- **Content**: type `pre-operation`, message: "I will install the security-audit skill on your agent. This requires hibernating and waking you. Please finish your current work and reply with 'ok' when ready. I will wait up to 60 seconds." Include `operation`: "skill-install", `skill_name`: "security-audit", `expected_downtime`: "30 seconds", `requires_acknowledgment`: true.

### Example 2: Timeout Final Notice

**Scenario:** Agent did not respond within 60 seconds.

Use the `agent-messaging` skill to send:
- **Recipient**: `code-impl-auth`
- **Subject**: `Proceeding Without Acknowledgment`
- **Priority**: `high`
- **Content**: type `timeout-notice`, message: "No response received after 60 seconds. Proceeding with skill installation now. You will be hibernated and woken shortly." Include `operation`: "skill-install", `timeout_occurred`: true.

### Example 3: System Maintenance Broadcast

**Scenario:** Notifying all agents about upcoming system maintenance.

For each agent in the team (`code-impl-auth`, `test-engineer-01`, `docs-writer`), use the `agent-messaging` skill to send:
- **Recipient**: the agent session name
- **Subject**: `System Maintenance in 5 Minutes`
- **Priority**: `high`
- **Content**: type `pre-operation`, message: "System maintenance will begin in 5 minutes. All agents will be hibernated. Please save your work and reply with 'ok' when ready." Include `operation`: "system-maintenance", `broadcast_id`: a unique broadcast ID, `expected_downtime`: "10 minutes", `requires_acknowledgment`: true.

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Message not delivered | Agent session not found | Use the `ai-maestro-agents-management` skill to verify the agent is registered |
| Agent does not respond | Agent busy or unresponsive | Send reminders at 15s, 30s, 45s; proceed after 60s timeout |
| Agent responds with "not ready" | Work in progress | Negotiate delay; ask when agent will be ready |
| Multiple agents timeout | Broadcast delivery issue | Use the `ai-maestro-agents-management` skill to check AI Maestro health; retry broadcast |
| Notification arrives too late | Network delay | Send notifications earlier; increase lead time |

## Related Operations

- [op-post-operation-notification.md](op-post-operation-notification.md) - Send after operation completes
- [op-acknowledgment-protocol.md](op-acknowledgment-protocol.md) - Detailed ACK handling
- [op-failure-notification.md](op-failure-notification.md) - Send if operation fails
- [pre-operation-notifications.md](pre-operation-notifications.md) - Complete reference documentation
