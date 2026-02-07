---
operation: post-operation-notification
procedure: proc-notify-team-ready
workflow-instruction: Step 5 - Team Ready Notification
parent-skill: ecos-notification-protocols
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Post-Operation Notification

## When to Use

Trigger this operation AFTER:
- Skill installation completes successfully
- Agent restart completes
- Configuration changes are applied
- System maintenance ends
- Any disruptive operation finishes successfully

## Prerequisites

- Operation completed successfully
- Agent is back online (for restart/hibernation operations)
- Verification criteria are defined
- AI Maestro messaging is available

## Procedure

### Step 1: Confirm Operation Completed

Verify the operation succeeded before notifying:

```bash
# For skill installation - verify skill is registered
# For agent restart - verify agent session is active
curl -s "http://localhost:23000/api/sessions" | jq '.sessions[] | select(.name == "<agent>") | .status'
```

### Step 2: Compose Success Message

Include these elements:
- Confirmation that operation completed
- What was changed/installed/updated
- Request for agent to verify
- Any next steps or actions needed

### Step 3: Send Confirmation via AI Maestro

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "<target-agent>",
    "subject": "<Operation Type> Complete",
    "priority": "normal",
    "content": {
      "type": "post-operation",
      "message": "The <operation> has been completed. <details>. Please verify <what to verify> and reply with confirmation.",
      "operation": "<operation-type>",
      "status": "success",
      "verification_requested": true
    }
  }'
```

### Step 4: Request Verification

Ask the agent to confirm the operation had the intended effect:

```bash
# Wait for verification response (up to 30 seconds per health check timeout)
curl -s "http://localhost:23000/api/messages?agent=chief-of-staff&action=list&status=unread" | jq '.messages[] | select(.from == "<target-agent>")'
```

### Step 5: Log Outcome

Record the operation completion:
- Operation type
- Target agent
- Completion timestamp
- Verification status (confirmed/pending/failed)

## Checklist

Copy this checklist and track your progress:

- [ ] Verified operation completed successfully
- [ ] Composed confirmation message with verification request
- [ ] Sent post-operation notification
- [ ] Received verification from agent (or noted pending)
- [ ] Logged operation outcome
- [ ] Documented any issues encountered

## Examples

### Example 1: Skill Installation Complete

**Scenario:** security-audit skill was installed on code-impl-auth.

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "code-impl-auth",
    "subject": "Skill Installation Complete",
    "priority": "normal",
    "content": {
      "type": "post-operation",
      "message": "The security-audit skill has been installed. Please verify the skill is active by checking your available skills list. Reply with confirmation that you can see and use the new skill.",
      "operation": "skill-install",
      "skill_name": "security-audit",
      "status": "success",
      "verification_requested": true
    }
  }'
```

**Expected Verification Response:**
```json
{
  "from": "code-impl-auth",
  "subject": "RE: Skill Installation Complete",
  "content": {
    "type": "verification",
    "message": "Confirmed. security-audit skill is active and functional.",
    "verified": true
  }
}
```

### Example 2: Agent Restart Complete

**Scenario:** test-engineer-01 was restarted for plugin update.

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "test-engineer-01",
    "subject": "Restart Complete",
    "priority": "normal",
    "content": {
      "type": "post-operation",
      "message": "Your agent has been restarted with the updated plugin configuration. Please verify you can access the new testing tools and reply with confirmation.",
      "operation": "agent-restart",
      "status": "success",
      "verification_requested": true
    }
  }'
```

### Example 3: System Maintenance Complete Broadcast

**Scenario:** System maintenance finished, all agents back online.

```bash
AGENTS=("code-impl-auth" "test-engineer-01" "docs-writer")

for agent in "${AGENTS[@]}"; do
  curl -X POST "http://localhost:23000/api/messages" \
    -H "Content-Type: application/json" \
    -d "{
      \"to\": \"$agent\",
      \"subject\": \"System Maintenance Complete\",
      \"priority\": \"normal\",
      \"content\": {
        \"type\": \"post-operation\",
        \"message\": \"System maintenance is complete. All systems are operational. You may resume normal work. Please report any issues you encounter.\",
        \"operation\": \"system-maintenance\",
        \"status\": \"success\",
        \"verification_requested\": false
      }
    }"
done
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Agent does not verify | Agent distracted or verification unclear | Send specific verification request; clarify what to check |
| Verification fails | Operation did not have intended effect | Log issue; may need to retry operation or investigate |
| Agent reports issues | Side effects from operation | Document issues; may need rollback or fix |
| Post-op message not delivered | Agent still offline | Wait for agent to come online; retry message |
| Wrong verification received | Agent misunderstood request | Resend with clearer instructions |

## Related Operations

- [op-pre-operation-notification.md](op-pre-operation-notification.md) - Send before operation
- [op-failure-notification.md](op-failure-notification.md) - Send if operation fails instead
- [op-acknowledgment-protocol.md](op-acknowledgment-protocol.md) - Verification uses similar protocol
- [post-operation-notifications.md](post-operation-notifications.md) - Complete reference documentation
