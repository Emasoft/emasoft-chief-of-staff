# Failure Notifications Reference

## Table of Contents

- 4.1 What are failure notifications - Understanding error messages
- 4.2 When to send failure notifications - Failure triggers
  - 4.2.1 Installation failures - Skill or plugin not installed
  - 4.2.2 Restart failures - Agent did not come back online
  - 4.2.3 Configuration failures - Settings not applied
  - 4.2.4 Timeout failures - Operation did not complete in time
- 4.3 Failure notification procedure - Step-by-step process
  - 4.3.1 Capture error details - What went wrong
  - 4.3.2 Compose failure message - What to tell agents
  - 4.3.3 Send notification - Using the `agent-messaging` skill
  - 4.3.4 Provide recovery guidance - How to proceed
  - 4.3.5 Log failure - Record for analysis
- 4.4 Failure message format - Standard error structure
- 4.5 Error severity levels - Critical, error, warning
- 4.6 Recovery guidance patterns - Common recovery steps
- 4.7 Examples - Failure scenarios
- 4.8 Troubleshooting - Notification delivery during failures

---

## 4.1 What are failure notifications

Failure notifications are error messages sent to agents when operations do not complete successfully. The purpose is to:

1. Inform agents that an expected operation failed
2. Provide details about what went wrong
3. Give agents guidance on what to do next
4. Maintain transparency about system state
5. Enable agents to adjust their work accordingly

Failure notifications are critical for maintaining agent trust and coordination. Agents that were waiting for an operation should not be left wondering what happened.

**Failure notification flow:**
```
Operation        Failure           Notification        Recovery
   |               |                    |                |
   +--- Start ---> |                    |                |
   |               |                    |                |
   |           <-- Fail                 |                |
   |               |                    |                |
   |               +-- Capture error -->|                |
   |               |                    |                |
   |               |   <-- Compose --   |                |
   |               |                    |                |
   |               |   --- Send ------> |                |
   |               |                    |                |
   |               |                    +-- Agent aware  |
   |               |                    |                |
   |               +-- Log failure ---> |                |
   |               |                    |                |
   |               |                    +-- Guidance --> |
```

---

## 4.2 When to send failure notifications

### 4.2.1 Installation failures

**Trigger:** Skill or plugin installation did not complete successfully.

**Common causes:**
- Invalid skill package structure
- Missing required files (SKILL.md)
- Permission errors
- Disk space issues
- Network failures (for remote skills)
- Version conflicts

**What to communicate:**
- Installation failed
- Specific error encountered
- Skill/plugin that failed
- Agent can continue previous work
- When retry will be attempted

**Example error:**
```
Installation of security-audit skill failed.
Error: SKILL_VALIDATION_FAILED - Missing SKILL.md file
```

### 4.2.2 Restart failures

**Trigger:** Agent restart did not complete, agent is not online.

**Common causes:**
- Process failed to start
- Configuration error
- Resource exhaustion
- Dependency missing
- Port conflicts

**What to communicate:**
- Agent restart failed
- Agent is currently offline
- Error details
- Manual intervention may be needed
- Alternative actions being taken

**Example error:**
```
Agent restart failed for code-impl-auth.
Error: PROCESS_START_FAILED - Claude Code process exited immediately
```

### 4.2.3 Configuration failures

**Trigger:** Configuration change did not apply.

**Common causes:**
- Invalid configuration value
- Validation error
- Permission denied
- Configuration file locked
- Schema mismatch

**What to communicate:**
- Configuration change failed
- Current settings unchanged
- Specific error
- Agent can continue with current config

**Example error:**
```
Configuration change failed for deployment.timeout.
Error: VALIDATION_FAILED - Value must be between 60 and 3600
```

### 4.2.4 Timeout failures

**Trigger:** Operation did not complete within expected time.

**Common causes:**
- Network latency
- Resource contention
- Large payload
- Service unavailable
- Deadlock

**What to communicate:**
- Operation timed out
- Partial completion state
- Whether operation will be retried
- Agent state is uncertain

**Example error:**
```
Skill installation timed out after 300 seconds.
State: Unknown - hibernation completed, installation status uncertain
```

---

## 4.3 Failure notification procedure

### 4.3.1 Capture error details

**Purpose:** Collect comprehensive error information for the notification.

**Details to capture:**
```json
{
  "error_code": "SKILL_VALIDATION_FAILED",
  "error_message": "Missing required SKILL.md file",
  "operation": "skill-install",
  "target_agent": "code-impl-auth",
  "timestamp": "2025-02-02T10:30:00Z",
  "stack_trace": "...",
  "operation_context": {
    "skill_name": "security-audit",
    "skill_path": "/path/to/skill"
  }
}
```

**Capture implementation:**
```bash
capture_error() {
  local EXIT_CODE=$1
  local OPERATION=$2
  local AGENT=$3

  ERROR_DETAILS=$(cat <<EOF
{
  "error_code": "$(get_error_code $EXIT_CODE)",
  "error_message": "$(get_error_message $EXIT_CODE)",
  "operation": "$OPERATION",
  "target_agent": "$AGENT",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "exit_code": $EXIT_CODE
}
EOF
)
  echo "$ERROR_DETAILS"
}
```

### 4.3.2 Compose failure message

**Purpose:** Create a clear, actionable failure notification.

**Required elements:**
1. Clear statement that operation failed
2. Specific error code and message
3. Impact on agent
4. Recovery guidance
5. Next steps from Chief of Staff

**Template:**
```json
{
  "subject": "[Operation] Failed",
  "priority": "high",
  "content": {
    "type": "failure",
    "message": "The [operation] has failed. Error: [error_message]. You can [recovery guidance]. I will [next steps].",
    "operation": "[operation-type]",
    "status": "failed",
    "error_code": "[error_code]",
    "error_details": "[detailed error]",
    "recovery_action": "[what will happen next]"
  }
}
```

### 4.3.3 Send notification

**Purpose:** Deliver the failure notification using the `agent-messaging` skill.

Use the `agent-messaging` skill to send:
- **Recipient**: the affected agent session name
- **Subject**: `[Operation] Failed`
- **Priority**: `high`
- **Content**: type `failure`, message: "The [operation] has failed. Error: [error_message]. [recovery_guidance]." Include `operation`, `status`: "failed", `error_code`, `error_details`, `recovery_action`.

**Verify**: confirm message delivery via the `agent-messaging` skill's sent messages feature.

### 4.3.4 Provide recovery guidance

**Purpose:** Tell the agent what to do after the failure.

**Recovery guidance patterns:**

| Failure Type | Guidance |
|--------------|----------|
| Installation failed | "You can continue your previous work. I will fix the package and retry." |
| Restart failed | "I am investigating the issue. You may need to be manually restarted." |
| Config failed | "Current settings remain active. I will attempt with corrected values." |
| Timeout | "State is uncertain. Please verify your current status when you resume." |

**Include specific next steps:**
```json
{
  "recovery_guidance": {
    "immediate_action": "Continue your previous work",
    "chief_of_staff_action": "Will fix skill package and retry in 5 minutes",
    "agent_action_if_needed": "None required",
    "escalation": "If issues persist, user will be notified"
  }
}
```

### 4.3.5 Log failure

**Purpose:** Record the failure for analysis and auditing.

**Failure log entry:**
```json
{
  "timestamp": "2025-02-02T10:30:00Z",
  "event_type": "operation_failure",
  "operation": "skill-install",
  "target_agent": "code-impl-auth",
  "error": {
    "code": "SKILL_VALIDATION_FAILED",
    "message": "Missing required SKILL.md file",
    "details": "File not found at expected path"
  },
  "notification_sent": true,
  "notification_message_id": "msg-12345",
  "recovery_action_planned": "Fix skill package and retry",
  "retry_scheduled": "2025-02-02T10:35:00Z"
}
```

**Log file location:**
```bash
LOG_FILE="/var/log/chief-of-staff/operations.log"
echo "$LOG_ENTRY" >> $LOG_FILE
```

---

## 4.4 Failure message format

**Standard failure notification structure:**

> **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

```json
{
  "to": "agent-session-name",
  "subject": "[Operation] Failed",
  "priority": "high",
  "content": {
    "type": "failure",
    "message": "Human-readable summary of failure and recovery",
    "operation": "skill-install|plugin-install|restart|config-change",
    "status": "failed",
    "error_code": "ERROR_CODE_HERE",
    "error_details": "Detailed error message",
    "error_context": {
      "skill_name": "security-audit (if applicable)",
      "attempted_at": "2025-02-02T10:30:00Z",
      "duration": "15 seconds"
    },
    "severity": "critical|error|warning",
    "recovery_action": "What Chief of Staff will do next",
    "agent_action": "What agent should do (usually nothing)",
    "retry_planned": true,
    "retry_time": "2025-02-02T10:35:00Z"
  }
}
```

**Field descriptions:**

| Field | Required | Description |
|-------|----------|-------------|
| `content.type` | Yes | Always "failure" |
| `content.error_code` | Yes | Machine-readable error identifier |
| `content.error_details` | Yes | Human-readable error description |
| `content.severity` | Yes | Error severity level |
| `content.recovery_action` | Yes | What happens next |
| `content.agent_action` | No | What agent should do |
| `content.retry_planned` | No | Whether retry will be attempted |
| `content.retry_time` | No | When retry will occur |

---

## 4.5 Error severity levels

| Severity | Meaning | Agent Impact | Example |
|----------|---------|--------------|---------|
| `critical` | Major system failure | Agent cannot function | Database connection lost |
| `error` | Operation failed | Agent work interrupted | Skill install failed |
| `warning` | Issue but recoverable | Agent may be affected | Config validation warning |

**Severity determination rules:**
1. `critical` - Agent is offline or system is broken
2. `error` - Specific operation failed but agent is functional
3. `warning` - Issue occurred but operation partially succeeded

**Priority mapping:**
- `critical` severity -> `critical` priority notification
- `error` severity -> `high` priority notification
- `warning` severity -> `normal` priority notification

---

## 4.6 Recovery guidance patterns

**Pattern 1: Retry will be attempted**
```
"You can continue your previous work. I will retry this operation in [X] minutes after fixing the issue."
```

**Pattern 2: Manual intervention needed**
```
"This failure requires manual intervention. I have notified the user. Please wait for further instructions."
```

**Pattern 3: Agent should take action**
```
"Please [specific action] and then notify me when complete so I can retry the operation."
```

**Pattern 4: State uncertain**
```
"The operation state is uncertain due to the failure. Please verify your current status and report any issues."
```

**Pattern 5: No action needed**
```
"No action required from you. Your current configuration remains unchanged. This is informational only."
```

**Recovery guidance by failure type:**

| Failure Type | Typical Guidance |
|--------------|------------------|
| Skill validation failed | "Package will be fixed and reinstalled" |
| Agent restart failed | "Manual restart may be required" |
| Network timeout | "Retry scheduled when network stable" |
| Permission denied | "User will be asked to grant permissions" |
| Resource exhaustion | "Waiting for resources to free up" |
| Version conflict | "Conflicting component will be updated" |

---

## 4.7 Examples

### Example 1: Skill Installation Failure

Use the `agent-messaging` skill to send:
- **Recipient**: `code-impl-auth`
- **Subject**: `Skill Installation Failed`
- **Priority**: `high`
- **Content**: type `failure`, message: "Failed to install security-audit skill. Error: Skill package validation failed - SKILL.md file is missing from the package. You can continue your previous work. I will fix the skill package and retry installation in 5 minutes." Include `operation`: "skill-install", `status`: "failed", `error_code`: "SKILL_VALIDATION_FAILED", `error_details`: "Missing required SKILL.md file at /skills/security-audit/SKILL.md", `error_context`: { `skill_name`: "security-audit", `skill_path`: "/path/to/skills/security-audit", `validation_step`: "file_structure_check" }, `severity`: "error", `recovery_action`: "Skill package will be fixed and installation will be retried", `agent_action`: "Continue your previous work - no action required", `retry_planned`: true, `retry_time`: "2025-02-02T10:35:00Z".

### Example 2: Agent Restart Failure

Use the `agent-messaging` skill to send:
- **Recipient**: `orchestrator-master`
- **Subject**: `Agent Restart Failed`
- **Priority**: `critical`
- **Content**: type `failure`, message: "Failed to restart agent code-impl-auth after plugin installation. Error: Claude Code process exited with code 1 immediately after start. The agent is currently OFFLINE. Manual intervention may be required." Include `operation`: "agent-restart", `status`: "failed", `error_code`: "PROCESS_START_FAILED", `error_details`: "Claude Code process exited with code 1. Stderr: Configuration file corrupted.", `error_context`: { `agent_name`: "code-impl-auth", `restart_reason`: "plugin-install", `exit_code`: 1, `attempts`: 3 }, `severity`: "critical", `recovery_action`: "Investigating configuration. User has been notified.", `agent_action`: "Agent is offline - no action possible from agent", `retry_planned`: false, `manual_intervention_required`: true.

### Example 3: Configuration Change Failure

Use the `agent-messaging` skill to send:
- **Recipient**: `devops-ci`
- **Subject**: `Configuration Change Failed`
- **Priority**: `high`
- **Content**: type `failure`, message: "Failed to update deployment.timeout configuration. Error: Value 5000 exceeds maximum allowed value of 3600. Your current configuration remains unchanged (timeout=300). I will retry with a valid value." Include `operation`: "config-change", `status`: "failed", `error_code`: "VALIDATION_FAILED", `error_details`: "Value 5000 exceeds maximum allowed (3600) for deployment.timeout", `error_context`: { `config_key`: "deployment.timeout", `attempted_value`: "5000", `current_value`: "300", `valid_range`: "60-3600" }, `severity`: "error", `recovery_action`: "Will retry with value 3600 (maximum allowed)", `agent_action`: "No action required - current settings remain active", `retry_planned`: true, `retry_time`: "2025-02-02T10:31:00Z".

### Example 4: Operation Timeout Failure

Use the `agent-messaging` skill to send:
- **Recipient**: `code-impl-auth`
- **Subject**: `Operation Timeout`
- **Priority**: `high`
- **Content**: type `failure`, message: "Skill installation operation timed out after 300 seconds. The operation state is uncertain - hibernation completed but installation status is unknown. Please verify your current status when you fully resume. I will check skill availability and retry if needed." Include `operation`: "skill-install", `status`: "failed", `error_code`: "OPERATION_TIMEOUT", `error_details`: "Operation exceeded 300 second timeout. Last known state: agent hibernated, skill copy in progress.", `error_context`: { `skill_name`: "security-audit", `timeout_seconds`: 300, `last_known_state`: "skill_copy_in_progress" }, `severity`: "error", `recovery_action`: "Checking operation state and will verify skill availability", `agent_action`: "Please verify your skill list and report if security-audit is present", `state_uncertain`: true, `retry_planned`: true, `retry_time`: "2025-02-02T10:35:00Z".

---

## 4.8 Troubleshooting

### Issue: Failure notification not delivered

**Symptoms:** Agent unaware of failure, waiting for operation that already failed.

**Resolution:**
1. Verify AI Maestro is running during failure
2. Check if failure occurred before notification code ran
3. Ensure notification is in finally/cleanup block
4. Verify agent session name is correct
5. Retry notification delivery manually

**Prevention:**
```bash
# Always wrap operations with failure notification
perform_operation() {
  local RESULT
  RESULT=$(run_operation "$@") || {
    send_failure_notification "$AGENT" "$OPERATION" "$?" "$RESULT"
    return 1
  }
  return 0
}
```

### Issue: Failure notification too vague

**Symptoms:** Agent cannot understand what failed or what to do.

**Resolution:**
1. Include specific error code and message
2. Add error context (what was being attempted)
3. Provide explicit recovery guidance
4. Include next steps from both parties

**Good failure message elements:**
- What operation failed
- Specific error that occurred
- What agent should do (usually "continue previous work")
- What Chief of Staff will do next
- When retry will occur (if applicable)

### Issue: Multiple failure notifications for same failure

**Symptoms:** Agent receives duplicate failure messages.

**Resolution:**
1. Implement idempotent notification sending
2. Track sent notifications by operation_id
3. Check if notification already sent before sending
4. Use message deduplication in AI Maestro

### Issue: Agent panics after failure notification

**Symptoms:** Agent overreacts to failure, abandons work unnecessarily.

**Resolution:**
1. Use clear, calm language in notifications
2. Explicitly state "You can continue your previous work"
3. Distinguish between critical and non-critical failures
4. Provide reassurance when appropriate
5. Avoid alarming language unless truly critical

### Issue: Failure notification during system outage

**Symptoms:** Cannot send notification because AI Maestro is also down.

**Resolution:**
1. Queue failed notifications for later delivery
2. Log failure locally when messaging unavailable
3. Send delayed notification when system recovers
4. Consider fallback notification method
5. Agent will learn of failure on next interaction
