---
operation: failure-notification
procedure: proc-notify-team-ready
workflow-instruction: Step 5 - Team Ready Notification
parent-skill: ecos-notification-protocols
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Failure Notification

## When to Use

Trigger this operation when:
- Skill installation fails
- Agent restart fails
- Configuration change fails
- Operation times out without completing
- Any error occurs during a notified operation
- Recovery from failure is needed

## Prerequisites

- Error details are captured (error code, message, stack trace if available)
- Affected agent(s) are identified
- Recovery guidance is prepared
- AI Maestro messaging is available

## Procedure

### Step 1: Capture Error Details

Document what went wrong:

```bash
# Capture error from failed operation
ERROR_CODE="<error-code>"
ERROR_MESSAGE="<what went wrong>"
ERROR_DETAILS="<additional diagnostic information>"
OPERATION_TYPE="<skill-install|agent-restart|config-change|etc>"
```

### Step 2: Compose Failure Message

Include these required elements:
- Clear statement that operation failed
- What the operation was attempting
- Error code and brief error description
- Impact on the agent (can they continue work?)
- Recovery guidance (what happens next)

### Step 3: Send Failure Notification

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "<affected-agent>",
    "subject": "<Operation Type> Failed",
    "priority": "high",
    "content": {
      "type": "failure",
      "message": "Failed to <operation description>. Error: <error message>. You can <what agent can do>. I will <recovery action>.",
      "operation": "<operation-type>",
      "status": "failed",
      "error_code": "<ERROR_CODE>",
      "error_details": "<ERROR_DETAILS>",
      "recovery_action": "<what will happen next>"
    }
  }'
```

### Step 4: Provide Recovery Guidance

Common recovery patterns:
- **Retry:** "I will retry the operation in 5 minutes"
- **Manual intervention:** "User intervention required to fix the issue"
- **Alternative approach:** "I will try an alternative installation method"
- **Rollback:** "Rolling back to previous state"

### Step 5: Log Failure

Record the failure for analysis:
- Timestamp
- Operation attempted
- Error code and details
- Agent affected
- Recovery action taken

## Checklist

Copy this checklist and track your progress:

- [ ] Captured complete error details
- [ ] Composed failure message with all required elements
- [ ] Included clear recovery guidance
- [ ] Sent failure notification via AI Maestro
- [ ] Logged failure for analysis
- [ ] Initiated recovery action (if automated)
- [ ] Escalated to user (if manual intervention needed)

## Examples

### Example 1: Skill Installation Failure

**Scenario:** security-audit skill installation failed due to validation error.

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "code-impl-auth",
    "subject": "Skill Installation Failed",
    "priority": "high",
    "content": {
      "type": "failure",
      "message": "Failed to install security-audit skill. Error: Skill validation failed - missing required SKILL.md file. You can continue your previous work normally. I will fix the skill package and retry installation.",
      "operation": "skill-install",
      "skill_name": "security-audit",
      "status": "failed",
      "error_code": "SKILL_VALIDATION_FAILED",
      "error_details": "Missing required SKILL.md file in skill directory",
      "recovery_action": "Skill package will be fixed and installation retried"
    }
  }'
```

### Example 2: Agent Restart Failure

**Scenario:** Agent did not come back online after restart.

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "Agent Restart Failed: test-engineer-01",
    "priority": "urgent",
    "content": {
      "type": "failure",
      "message": "Failed to restart test-engineer-01. Error: Agent did not come online within 2 minute timeout. The agent session may need manual recovery. I am escalating to user for intervention.",
      "operation": "agent-restart",
      "target_agent": "test-engineer-01",
      "status": "failed",
      "error_code": "RESTART_TIMEOUT",
      "error_details": "Agent session not detected after wake command",
      "recovery_action": "Escalating to user for manual intervention"
    }
  }'
```

### Example 3: Configuration Change Failure

**Scenario:** Settings update did not apply correctly.

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "code-impl-auth",
    "subject": "Configuration Update Failed",
    "priority": "high",
    "content": {
      "type": "failure",
      "message": "Failed to apply new logging configuration. Error: Permission denied when writing to config file. Your current configuration remains unchanged. I will request elevated permissions and retry.",
      "operation": "config-change",
      "config_type": "logging",
      "status": "failed",
      "error_code": "PERMISSION_DENIED",
      "error_details": "Cannot write to /etc/claude/logging.conf - permission denied",
      "recovery_action": "Requesting elevated permissions, will retry"
    }
  }'
```

### Example 4: Timeout Failure Notification

**Scenario:** Operation did not complete within expected time.

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "code-impl-auth",
    "subject": "Operation Timed Out",
    "priority": "high",
    "content": {
      "type": "failure",
      "message": "The skill indexing operation timed out after 10 minutes. The partial results have been discarded. You may continue your work. I will investigate the timeout cause and attempt a more targeted reindex.",
      "operation": "skill-reindex",
      "status": "failed",
      "error_code": "OPERATION_TIMEOUT",
      "error_details": "Skill indexing exceeded 10 minute timeout limit",
      "recovery_action": "Will attempt targeted reindex of changed skills only"
    }
  }'
```

## Error Severity Levels

Use appropriate severity in notifications:

| Severity | When to Use | Example |
|----------|-------------|---------|
| **critical** | System is unusable, immediate action needed | AI Maestro down, all agents unreachable |
| **error** | Operation failed, impact is significant | Skill installation failed, agent restart failed |
| **warning** | Issue detected, operation may still work | Partial failure, degraded performance |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Failure notification not delivered | Affected agent is offline | Log locally; send when agent comes online; notify user |
| Recovery action fails | Secondary failure | Escalate to user; do not retry indefinitely |
| Multiple agents affected | Cascading failure | Send individual notifications; coordinate recovery |
| Agent confused by error | Unclear error message | Provide specific, actionable guidance in follow-up |
| Duplicate failure notifications | Retry logic sending multiple | Track sent notifications; deduplicate by operation ID |

## Related Operations

- [op-pre-operation-notification.md](op-pre-operation-notification.md) - Precedes failed operation
- [op-post-operation-notification.md](op-post-operation-notification.md) - Alternative if operation succeeds
- [op-acknowledgment-protocol.md](op-acknowledgment-protocol.md) - Timeout may trigger failure
- [failure-notifications.md](failure-notifications.md) - Complete reference documentation
