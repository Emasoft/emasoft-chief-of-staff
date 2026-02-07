---
operation: send-team-messages
procedure: proc-notify-team-ready
workflow-instruction: Step 5 - Team Ready Notification
parent-skill: ecos-team-coordination
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Send Team Messages

## When to Use

Trigger this operation when:
- Broadcasting updates to all team members
- Sending targeted instructions to specific agents
- Facilitating inter-agent communication
- Announcing team-wide events (sprint start, maintenance, etc.)
- Coordinating multi-agent operations

## Prerequisites

- AI Maestro messaging system is running
- The `agent-messaging` skill is available
- The `ai-maestro-agents-management` skill is available
- Recipient agents are registered with valid session names
- Message content and priority are determined
- For broadcasts: list of target agents is available

## Procedure

### Step 1: Identify Recipients

Determine who needs to receive the message.

Use the `ai-maestro-agents-management` skill to list all active agents. Filter by role or status as needed to build the recipient list.

For role-based targeting:
- Review the agent list and filter by role metadata (e.g., all agents with role "developer")
- Note each agent's session name for targeted messaging

### Step 2: Compose Message with Priority

Select appropriate priority level:
- **urgent**: Immediate attention required (emergencies, blockers)
- **high**: Important, should be read soon (role assignments, operation warnings)
- **normal**: Standard updates (status reports, announcements)
- **low**: Informational (FYI, optional reading)

### Step 3: Send Message

**For targeted message (single recipient):**

Use the `agent-messaging` skill to send a message:
- **Recipient**: the target agent session name
- **Subject**: descriptive subject line
- **Priority**: appropriate priority level
- **Content**: type matching the message purpose (e.g., `instruction`, `announcement`, `request`), message with the actual content

**For broadcast message (all team members):**

Use the `agent-messaging` skill to broadcast a message to all active sessions:
- **Subject**: descriptive broadcast subject
- **Priority**: appropriate priority level
- **Content**: type `announcement`, message with the broadcast content

**For multi-recipient message (specific group):**

For each target agent in the group, use the `agent-messaging` skill to send an individual message with the same content.

### Step 4: Confirm Delivery

Use the `agent-messaging` skill to check message status by message ID. For important messages, verify delivery was successful.

### Step 5: Log in Coordination State

Record the message in coordination log:
- Timestamp
- Recipients
- Subject
- Priority
- Message type
- Delivery status

## Checklist

Copy this checklist and track your progress:

- [ ] Identified all recipients for the message
- [ ] Determined appropriate message priority
- [ ] Composed clear, actionable message content
- [ ] Sent message via `agent-messaging` skill
- [ ] Verified delivery confirmation received
- [ ] Logged message in coordination state

## Examples

### Example: Broadcasting Sprint Start

**Scenario:** Sprint 5 is starting, all team members need to be informed.

Use the `agent-messaging` skill to broadcast:
- **Subject**: `Sprint 5 Starting Now`
- **Priority**: `high`
- **Content**: type `announcement`, message: "Sprint 5 has officially started. Duration: 2 weeks. Focus: Authentication module refactor. Check your inbox for individual task assignments."

### Example: Targeted Instruction to Developer

**Scenario:** Agent `code-impl-auth` needs to pause work for an upcoming operation.

Use the `agent-messaging` skill to send a message:
- **Recipient**: `code-impl-auth`
- **Subject**: `Pause Work: Incoming Skill Installation`
- **Priority**: `high`
- **Content**: type `instruction`, message: "Please pause your current work and save state. A skill installation will begin in 2 minutes. Reply with ok when ready."

### Example: Multi-Recipient Status Request

**Scenario:** Need status from all developers before standup.

For each developer agent (`code-impl-auth`, `code-impl-core`, `code-impl-api`), use the `agent-messaging` skill to send:
- **Recipient**: the developer agent session name
- **Subject**: `Status Request: Pre-Standup`
- **Priority**: `normal`
- **Content**: type `request`, message: "Please provide your current status for standup. Include: current task, blockers, expected completion."

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Message not delivered | Recipient session not found | Use the `ai-maestro-agents-management` skill to list agents and verify session name |
| Messaging unavailable | AI Maestro not running | Use the `ai-maestro-agents-management` skill to check service health |
| Invalid message format | Malformed message content | Verify content includes required `type` and `message` fields |
| Broadcast fails partially | Some agents offline | Check delivery status, resend to failed recipients individually |
| Priority not respected | Agent inbox overwhelmed | Use urgent priority for critical messages; follow up directly |

## Related Operations

- [op-assign-agent-roles.md](op-assign-agent-roles.md) - Role assignment uses targeted messages
- [op-maintain-teammate-awareness.md](op-maintain-teammate-awareness.md) - Status polling sends request messages
- [team-messaging.md](team-messaging.md) - Complete messaging reference documentation
