---
operation: post-operation-notification
procedure: proc-notify-team-ready
workflow-instruction: Step 5 - Team Ready Notification
parent-skill: ecos-notification-protocols
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Post-Operation Notification


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Confirm Operation Completed](#step-1-confirm-operation-completed)
  - [Step 2: Compose Success Message](#step-2-compose-success-message)
  - [Step 3: Send Confirmation](#step-3-send-confirmation)
  - [Step 4: Request Verification](#step-4-request-verification)
  - [Step 5: Log Outcome](#step-5-log-outcome)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example 1: Skill Installation Complete](#example-1-skill-installation-complete)
  - [Example 2: Agent Restart Complete](#example-2-agent-restart-complete)
  - [Example 3: System Maintenance Complete Broadcast](#example-3-system-maintenance-complete-broadcast)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

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
- The `agent-messaging` skill is available
- The `ai-maestro-agents-management` skill is available

## Procedure

### Step 1: Confirm Operation Completed

Verify the operation succeeded before notifying.

Use the `ai-maestro-agents-management` skill to check the target agent's status:
- For skill installation: verify the skill is registered on the agent
- For agent restart: verify the agent session is active and status shows "running"
- For configuration changes: verify the change took effect

### Step 2: Compose Success Message

Include these elements:
- Confirmation that operation completed
- What was changed/installed/updated
- Request for agent to verify
- Any next steps or actions needed

### Step 3: Send Confirmation

Use the `agent-messaging` skill to send:
- **Recipient**: the target agent session name
- **Subject**: `[Operation Type] Complete`
- **Priority**: `normal`
- **Content**: type `post-operation`, message: "The [operation] has been completed. [details]. Please verify [what to verify] and reply with confirmation." Include `operation` (the operation type), `status`: "success", `verification_requested`: true.

### Step 4: Request Verification

Use the `agent-messaging` skill to check for unread messages from the target agent. Wait up to 30 seconds (per health check timeout). Look for a response containing a verification confirmation from the target agent.

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
- [ ] Sent post-operation notification via `agent-messaging` skill
- [ ] Received verification from agent (or noted pending)
- [ ] Logged operation outcome
- [ ] Documented any issues encountered

## Examples

### Example 1: Skill Installation Complete

**Scenario:** security-audit skill was installed on code-impl-auth.

Use the `agent-messaging` skill to send:
- **Recipient**: `code-impl-auth`
- **Subject**: `Skill Installation Complete`
- **Priority**: `normal`
- **Content**: type `post-operation`, message: "The security-audit skill has been installed. Please verify the skill is active by checking your available skills list. Reply with confirmation that you can see and use the new skill." Include `operation`: "skill-install", `skill_name`: "security-audit", `status`: "success", `verification_requested`: true.

**Expected Verification Response:**

The agent should reply with a message of type `verification`, confirming "security-audit skill is active and functional", with `verified`: true.

### Example 2: Agent Restart Complete

**Scenario:** test-engineer-01 was restarted for plugin update.

Use the `agent-messaging` skill to send:
- **Recipient**: `test-engineer-01`
- **Subject**: `Restart Complete`
- **Priority**: `normal`
- **Content**: type `post-operation`, message: "Your agent has been restarted with the updated plugin configuration. Please verify you can access the new testing tools and reply with confirmation." Include `operation`: "agent-restart", `status`: "success", `verification_requested`: true.

### Example 3: System Maintenance Complete Broadcast

**Scenario:** System maintenance finished, all agents back online.

For each agent in the team (`code-impl-auth`, `test-engineer-01`, `docs-writer`), use the `agent-messaging` skill to send:
- **Recipient**: the agent session name
- **Subject**: `System Maintenance Complete`
- **Priority**: `normal`
- **Content**: type `post-operation`, message: "System maintenance is complete. All systems are operational. You may resume normal work. Please report any issues you encounter." Include `operation`: "system-maintenance", `status`: "success", `verification_requested`: false.

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
