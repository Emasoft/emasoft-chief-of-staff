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

- AI Maestro messaging system is running at http://localhost:23000
- Recipient agents are registered with valid session names
- Message content and priority are determined
- For broadcasts: list of target agents is available

## Procedure

### Step 1: Identify Recipients

Determine who needs to receive the message:

```bash
# List all active agents
curl -s "http://localhost:23000/api/sessions" | jq '.sessions[] | .name'

# Or get agents by role
curl -s "http://localhost:23000/api/sessions" | jq '.sessions[] | select(.metadata.role == "developer") | .name'
```

### Step 2: Compose Message with Priority

Select appropriate priority level:
- **urgent**: Immediate attention required (emergencies, blockers)
- **high**: Important, should be read soon (role assignments, operation warnings)
- **normal**: Standard updates (status reports, announcements)
- **low**: Informational (FYI, optional reading)

### Step 3: Send via AI Maestro API

**For targeted message (single recipient):**

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "<recipient-session-name>",
    "subject": "<Message Subject>",
    "priority": "<urgent|high|normal|low>",
    "content": {
      "type": "<message-type>",
      "message": "<Your message content>"
    }
  }'
```

**For broadcast message (multiple recipients):**

```bash
curl -X POST "http://localhost:23000/api/messages/broadcast" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "<Broadcast Subject>",
    "priority": "<priority>",
    "content": {
      "type": "announcement",
      "message": "<Your broadcast message>"
    }
  }'
```

### Step 4: Confirm Delivery

```bash
# Check message was sent successfully (returns message ID)
# The API returns the message ID on success

# For important messages, request read receipt
curl -s "http://localhost:23000/api/messages/<message-id>/status"
```

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
- [ ] Sent message via AI Maestro API
- [ ] Verified delivery confirmation received
- [ ] Logged message in coordination state

## Examples

### Example: Broadcasting Sprint Start

**Scenario:** Sprint 5 is starting, all team members need to be informed.

```bash
curl -X POST "http://localhost:23000/api/messages/broadcast" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Sprint 5 Starting Now",
    "priority": "high",
    "content": {
      "type": "announcement",
      "message": "Sprint 5 has officially started. Duration: 2 weeks. Focus: Authentication module refactor. Check your inbox for individual task assignments."
    }
  }'
```

### Example: Targeted Instruction to Developer

**Scenario:** Code-impl-auth needs to pause work for an upcoming operation.

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "code-impl-auth",
    "subject": "Pause Work: Incoming Skill Installation",
    "priority": "high",
    "content": {
      "type": "instruction",
      "message": "Please pause your current work and save state. A skill installation will begin in 2 minutes. Reply with ok when ready."
    }
  }'
```

### Example: Multi-Recipient Status Request

**Scenario:** Need status from all developers before standup.

```bash
DEVELOPERS=("code-impl-auth" "code-impl-core" "code-impl-api")

for dev in "${DEVELOPERS[@]}"; do
  curl -X POST "http://localhost:23000/api/messages" \
    -H "Content-Type: application/json" \
    -d "{
      \"to\": \"$dev\",
      \"subject\": \"Status Request: Pre-Standup\",
      \"priority\": \"normal\",
      \"content\": {
        \"type\": \"request\",
        \"message\": \"Please provide your current status for standup. Include: current task, blockers, expected completion.\"
      }
    }"
done
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Message not delivered | Recipient session not found | Verify session name with `curl -s "http://localhost:23000/api/sessions"` |
| API returns error | AI Maestro not running | Check AI Maestro status: `curl -s "http://localhost:23000/api/health"` |
| Invalid JSON | Malformed message content | Validate JSON before sending: `echo '<json>' | jq .` |
| Broadcast fails partially | Some agents offline | Check delivery status, resend to failed recipients individually |
| Priority not respected | Agent inbox overwhelmed | Use urgent priority for critical messages; follow up directly |

## Related Operations

- [op-assign-agent-roles.md](op-assign-agent-roles.md) - Role assignment uses targeted messages
- [op-maintain-teammate-awareness.md](op-maintain-teammate-awareness.md) - Status polling sends request messages
- [team-messaging.md](team-messaging.md) - Complete messaging reference documentation
