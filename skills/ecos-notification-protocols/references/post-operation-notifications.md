# Post-Operation Notifications Reference

## Table of Contents

- 2.1 What are post-operation notifications - Understanding confirmation messages
- 2.2 When to send post-operation notifications - Confirmation triggers
  - 2.2.1 Skill installation complete - Skill is now active
  - 2.2.2 Agent restart complete - Agent is back online
  - 2.2.3 Configuration applied - Settings now active
  - 2.2.4 Maintenance complete - Normal operations resume
- 2.3 Post-operation notification procedure - Step-by-step process
  - 2.3.1 Confirm operation success - Verify completion
  - 2.3.2 Compose confirmation - What to tell agents
  - 2.3.3 Send notification - Using AI Maestro API
  - 2.3.4 Request verification - Ask agent to confirm
  - 2.3.5 Log outcome - Record the result
- 2.4 Verification request format - Asking agents to confirm
- 2.5 Examples - Post-operation scenarios
- 2.6 Troubleshooting - Verification issues

---

## 2.1 What are post-operation notifications

Post-operation notifications are confirmation messages sent to agents after completing operations that affected them. The purpose is to:

1. Inform agents that the operation completed successfully
2. Provide details about what was changed or installed
3. Request verification that changes are visible to the agent
4. Allow agents to resume their work
5. Document the operation outcome

Post-operation notifications complete the notification protocol flow. They are sent after successful operations to close the loop with affected agents.

---

## 2.2 When to send post-operation notifications

### 2.2.1 Skill installation complete

**Trigger:** Skill installation has finished and agent has been woken.

**What to communicate:**
- Skill name and version installed
- Confirmation agent is back online
- How to verify skill is active
- How to use the new skill

**Notification required:** Yes, with verification request.

**Message content should include:**
- Name of skill installed
- Instruction to verify skill availability
- Request for confirmation response

### 2.2.2 Agent restart complete

**Trigger:** Agent has been restarted (for plugin installation or other reason).

**What to communicate:**
- Agent is back online
- What was installed or changed
- Any context that was lost
- Next steps for the agent

**Notification required:** Yes.

**Message content should include:**
- Confirmation agent is running
- Summary of changes made
- Any action items for agent

### 2.2.3 Configuration applied

**Trigger:** Configuration change has taken effect.

**What to communicate:**
- What configuration changed
- New behavior to expect
- Any actions required by agent

**Notification required:** Yes.

**Message content should include:**
- Configuration key that changed
- Old and new values
- Impact on agent behavior

### 2.2.4 Maintenance complete

**Trigger:** Scheduled or emergency maintenance has finished.

**What to communicate:**
- Maintenance is complete
- All systems normal
- Agents may resume work

**Notification required:** Yes (broadcast).

**Message content should include:**
- Confirmation maintenance complete
- Any issues encountered
- All-clear to resume operations

---

## 2.3 Post-operation notification procedure

### 2.3.1 Confirm operation success

**Purpose:** Verify the operation completed before notifying agents.

**Verification steps:**
1. Check operation exit code or status
2. Verify expected changes are present
3. Confirm agent is online (if restarted)
4. Validate skill or plugin is loaded (if installed)

**Example verification:**
```bash
# Verify skill installation
aimaestro-agent.sh show code-impl-auth | grep -q "security-audit"
if [ $? -eq 0 ]; then
  echo "Skill installation verified"
  OPERATION_SUCCESS=true
else
  echo "Skill installation NOT verified"
  OPERATION_SUCCESS=false
fi
```

### 2.3.2 Compose confirmation

**Purpose:** Create a clear confirmation message for the agent.

**Required elements:**
1. Subject line indicating operation complete
2. Confirmation of success
3. Summary of what was done
4. Verification request (if applicable)
5. Next steps for agent

**Template:**
```json
{
  "subject": "[Operation Type] Complete",
  "priority": "normal",
  "content": {
    "type": "post-operation",
    "message": "The [operation] has been completed successfully. [Summary of changes]. Please [verification request].",
    "operation": "[operation-type]",
    "status": "success",
    "verification_requested": true
  }
}
```

### 2.3.3 Send notification

**Purpose:** Deliver the confirmation via AI Maestro API.

**API call:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "[agent-name]",
    "subject": "[Operation Type] Complete",
    "priority": "normal",
    "content": {
      "type": "post-operation",
      "message": "[Confirmation message]",
      "operation": "[operation-type]",
      "status": "success",
      "operation_details": {
        "completed_at": "[timestamp]",
        "changes": ["[change1]", "[change2]"]
      },
      "verification_requested": true
    }
  }'
```

### 2.3.4 Request verification

**Purpose:** Ask the agent to confirm the changes are visible and working.

**Verification request format:**
```json
{
  "content": {
    "verification_requested": true,
    "verification_instructions": "Please check your available skills and confirm you can see security-audit in the list.",
    "expected_verification": "Agent confirms skill is visible"
  }
}
```

**Why request verification:**
1. Confirms agent received the notification
2. Validates operation truly succeeded from agent perspective
3. Catches issues that server-side checks might miss
4. Creates audit trail of confirmed completions

### 2.3.5 Log outcome

**Purpose:** Record the operation result for tracking and auditing.

**Log entry format:**
```json
{
  "timestamp": "2025-02-02T10:30:00Z",
  "operation": "skill-install",
  "target_agent": "code-impl-auth",
  "operation_details": {
    "skill_name": "security-audit",
    "skill_version": "1.0.0"
  },
  "pre_notification_sent": "2025-02-02T10:28:00Z",
  "acknowledgment_received": "2025-02-02T10:28:45Z",
  "operation_completed": "2025-02-02T10:29:15Z",
  "post_notification_sent": "2025-02-02T10:30:00Z",
  "verification_received": "2025-02-02T10:30:30Z",
  "status": "success"
}
```

---

## 2.4 Verification request format

**Standard verification request structure:**

```json
{
  "to": "agent-session-name",
  "subject": "[Operation Type] Complete - Verification Requested",
  "priority": "normal",
  "content": {
    "type": "post-operation",
    "message": "The [operation] has completed. Please verify and confirm.",
    "operation": "skill-install|plugin-install|config-change|maintenance",
    "status": "success",
    "operation_details": {
      "skill_name": "skill-name (if applicable)",
      "completed_at": "2025-02-02T10:30:00Z"
    },
    "verification_requested": true,
    "verification_instructions": "Step-by-step instructions for agent to verify",
    "verification_response_format": {
      "type": "verification-response",
      "verified": true,
      "verification_notes": "What agent observed"
    }
  }
}
```

**Verification instructions by operation type:**

| Operation | Verification Instructions |
|-----------|--------------------------|
| skill-install | "Check your available skills list and confirm [skill-name] appears" |
| plugin-install | "Verify plugin commands are available by running /help" |
| config-change | "Confirm your behavior reflects the new [setting]" |
| maintenance | "Verify all services are responding normally" |

---

## 2.5 Examples

### Example 1: Skill Installation Complete

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "code-impl-auth",
    "subject": "Skill Installation Complete",
    "priority": "normal",
    "content": {
      "type": "post-operation",
      "message": "The security-audit skill has been installed successfully. You are now back online. Please verify the skill is active by checking your available skills list. Reply with confirmation once verified.",
      "operation": "skill-install",
      "status": "success",
      "operation_details": {
        "skill_name": "security-audit",
        "skill_version": "1.0.0",
        "completed_at": "2025-02-02T10:30:00Z",
        "downtime_actual": "28 seconds"
      },
      "verification_requested": true,
      "verification_instructions": "Check your available skills list and confirm security-audit appears. You can test it by asking about security best practices."
    }
  }'
```

### Example 2: Plugin Installation Complete (Context Lost)

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "test-engineer-01",
    "subject": "Plugin Installation Complete",
    "priority": "normal",
    "content": {
      "type": "post-operation",
      "message": "The test-framework-integration plugin has been installed. You have been restarted and your previous context was not preserved. Please reload any necessary context and verify the plugin is active. Reply when ready to continue.",
      "operation": "plugin-install",
      "status": "success",
      "operation_details": {
        "plugin_name": "test-framework-integration",
        "plugin_version": "2.1.0",
        "completed_at": "2025-02-02T10:30:00Z",
        "context_preserved": false
      },
      "verification_requested": true,
      "verification_instructions": "Run /help and verify test-framework commands are available. Your previous context was not preserved - please reload your task context.",
      "next_steps": [
        "Reload task context if needed",
        "Verify plugin commands available",
        "Resume previous work"
      ]
    }
  }'
```

### Example 3: Configuration Change Applied

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "devops-ci",
    "subject": "Configuration Change Applied",
    "priority": "normal",
    "content": {
      "type": "post-operation",
      "message": "Your deployment timeout configuration has been updated from 300 seconds to 600 seconds. This change is now active. No restart required. Verify by checking your deployment behavior on next run.",
      "operation": "config-change",
      "status": "success",
      "operation_details": {
        "config_key": "deployment.timeout",
        "old_value": "300",
        "new_value": "600",
        "applied_at": "2025-02-02T10:30:00Z",
        "restart_required": false
      },
      "verification_requested": false
    }
  }'
```

### Example 4: Broadcast Maintenance Complete

```bash
AGENTS=("code-impl-auth" "test-engineer-01" "docs-writer" "devops-ci")
BROADCAST_ID="maint-20250202103000"

for agent in "${AGENTS[@]}"; do
  curl -X POST "http://localhost:23000/api/messages" \
    -H "Content-Type: application/json" \
    -d "{
      \"to\": \"$agent\",
      \"subject\": \"System Maintenance Complete\",
      \"priority\": \"normal\",
      \"content\": {
        \"type\": \"post-operation\",
        \"message\": \"System maintenance is complete. All services are operational. You may resume normal work. Database migrations completed successfully.\",
        \"operation\": \"maintenance\",
        \"status\": \"success\",
        \"operation_details\": {
          \"maintenance_type\": \"database-migration\",
          \"completed_at\": \"2025-02-02T10:30:00Z\",
          \"actual_duration\": \"8 minutes\",
          \"issues_encountered\": \"none\"
        },
        \"broadcast_id\": \"$BROADCAST_ID\",
        \"verification_requested\": false
      }
    }"
done
```

---

## 2.6 Troubleshooting

### Issue: Agent does not receive post-operation notification

**Symptoms:** Agent unaware operation completed, continues waiting.

**Resolution:**
1. Verify agent is online after operation
2. Check AI Maestro message delivery logs
3. Confirm agent session name is correct
4. Resend notification if delivery failed
5. Check agent inbox directly

### Issue: Agent cannot verify operation

**Symptoms:** Agent reports skill/plugin not visible despite successful install.

**Resolution:**
1. Verify operation truly completed (check logs)
2. Agent may need to refresh (restart Claude Code)
3. Check if skill/plugin has activation requirements
4. Review installation logs for partial failures
5. Consider reinstallation if verification fails

### Issue: Verification response not received

**Symptoms:** Post-operation sent, verification requested, no response.

**Resolution:**
1. Agent may be busy - give time to respond
2. Send a follow-up asking for verification status
3. Check if original message was delivered
4. Agent may have verified but not responded - check their work
5. Do not block on verification if operation is confirmed server-side

### Issue: Broadcast notification incomplete

**Symptoms:** Some agents received confirmation, others did not.

**Resolution:**
1. Check which agents received vs missed
2. Verify all agent names were correct
3. Resend to agents that missed notification
4. Check for network or API issues during broadcast
5. Consider sequential sends if parallel fails
