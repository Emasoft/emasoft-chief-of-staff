# Acknowledgment Protocol Reference

## Table of Contents

- 3.1 What is the acknowledgment protocol - Understanding coordination
- 3.2 When to require acknowledgments - Acknowledgment triggers
  - 3.2.1 Disruptive operations - Agent will be interrupted
  - 3.2.2 State-changing operations - Agent context affected
  - 3.2.3 Multi-agent coordination - Synchronized actions needed
- 3.3 Acknowledgment procedure - Step-by-step process
  - 3.3.1 Send acknowledgment request - Ask for "ok"
  - 3.3.2 Start timeout timer - 2 minute maximum wait
  - 3.3.3 Send reminders - At 30s, 60s, 90s intervals
  - 3.3.4 Process response - Handle "ok" or other responses
  - 3.3.5 Proceed or timeout - Continue or handle no response
- 3.4 Acknowledgment message format - Standard request structure
- 3.5 Reminder message format - Standard reminder structure
- 3.6 Response handling - What agents can send back
- 3.7 Timeout behavior - What happens without response
- 3.8 Examples - Acknowledgment scenarios
- 3.9 Troubleshooting - Acknowledgment issues

---

## 3.1 What is the acknowledgment protocol

The acknowledgment protocol is a coordination mechanism where the Chief of Staff requests confirmation from an agent before proceeding with an operation. The protocol ensures:

1. Agents have time to prepare for operations
2. Agents can finish current work before interruption
3. Operations do not surprise agents mid-task
4. There is an audit trail of agent readiness
5. Timeouts prevent indefinite waiting

The acknowledgment protocol is the core of coordination between Chief of Staff and other agents. It transforms one-way commands into a handshake pattern.

**Protocol overview:**
```
Chief of Staff                    Agent
      |                              |
      |  --- Pre-op notification --> |
      |        (request "ok")        |
      |                              |
      |  <-- Wait for response --    |
      |                              |
      |  --- Reminder (30s) ------>  |
      |                              |
      |  --- Reminder (60s) ------>  |
      |                              |
      |  --- Reminder (90s) ------>  |
      |                              |
      |  <-- "ok" acknowledgment --- |
      |                              |
      |  --- Proceed with op ----->  |
      |                              |
```

---

## 3.2 When to require acknowledgments

### 3.2.1 Disruptive operations

**Trigger:** Operations that will interrupt the agent's current work.

**Examples:**
- Skill installation (hibernation required)
- Plugin installation (restart required)
- Agent restart
- System maintenance

**Why acknowledgment needed:**
- Agent may be in middle of critical task
- Agent needs time to save state
- Interruption could cause data loss

**Acknowledgment behavior:**
- Required: Yes
- Timeout: 2 minutes
- On timeout: Proceed with warning

### 3.2.2 State-changing operations

**Trigger:** Operations that will modify agent state or context.

**Examples:**
- Configuration changes affecting behavior
- Permission changes
- Skill activation/deactivation
- Context modifications

**Why acknowledgment needed:**
- Agent should be aware of state changes
- Agent may need to adjust behavior
- Unexpected changes could confuse agent

**Acknowledgment behavior:**
- Required: Recommended
- Timeout: 2 minutes
- On timeout: Proceed with notification

### 3.2.3 Multi-agent coordination

**Trigger:** Operations requiring multiple agents to synchronize.

**Examples:**
- Rolling deployments
- Synchronized testing
- Coordinated releases
- Multi-agent task handoffs

**Why acknowledgment needed:**
- All agents must be ready simultaneously
- Operations depend on agent synchronization
- Partial completion could cause failures

**Acknowledgment behavior:**
- Required: Yes, from all participating agents
- Timeout: 2 minutes per agent
- On timeout: May abort or proceed based on quorum

---

## 3.3 Acknowledgment procedure

### 3.3.1 Send acknowledgment request

**Purpose:** Request the agent's readiness confirmation.

**Request format:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "agent-name",
    "subject": "[Operation] Pending - Acknowledgment Required",
    "priority": "high",
    "content": {
      "type": "pre-operation",
      "message": "I will [operation description]. Please finish your current work and reply with \"ok\" when ready. I will wait up to 2 minutes.",
      "operation": "[operation-type]",
      "requires_acknowledgment": true,
      "acknowledgment_timeout": 120,
      "acknowledgment_reminder_intervals": [30, 60, 90]
    }
  }'
```

**Critical elements:**
1. Clear statement of what will happen
2. Explicit request for "ok" response
3. Statement of timeout duration
4. High priority to ensure visibility

### 3.3.2 Start timeout timer

**Purpose:** Begin tracking time for acknowledgment response.

**Timer implementation:**
```bash
#!/bin/bash
# Start acknowledgment wait

AGENT="code-impl-auth"
TIMEOUT=120  # 2 minutes
REMINDER_INTERVALS=(30 60 90)
START_TIME=$(date +%s)

# Record start
echo "[$(date)] Started waiting for acknowledgment from $AGENT"

# Function to check if timeout exceeded
check_timeout() {
  CURRENT=$(date +%s)
  ELAPSED=$((CURRENT - START_TIME))
  if [ $ELAPSED -ge $TIMEOUT ]; then
    return 0  # True - timed out
  fi
  return 1  # False - still waiting
}
```

### 3.3.3 Send reminders

**Purpose:** Remind agents who have not responded.

**Reminder schedule:**
- 30 seconds: First reminder (90 seconds remaining)
- 60 seconds: Second reminder (60 seconds remaining)
- 90 seconds: Final reminder (30 seconds remaining)

**Reminder implementation:**
```bash
REMINDER_SENT=(false false false)
REMINDER_INTERVALS=(30 60 90)

while ! check_timeout; do
  CURRENT=$(date +%s)
  ELAPSED=$((CURRENT - START_TIME))

  # Check if time to send reminders
  for i in 0 1 2; do
    if [ $ELAPSED -ge ${REMINDER_INTERVALS[$i]} ] && [ "${REMINDER_SENT[$i]}" = "false" ]; then
      REMAINING=$((TIMEOUT - ELAPSED))
      send_reminder $AGENT $REMAINING
      REMINDER_SENT[$i]=true
    fi
  done

  # Check for acknowledgment
  if check_acknowledgment $AGENT; then
    echo "[$(date)] Acknowledgment received from $AGENT"
    break
  fi

  sleep 5
done
```

**Reminder message:**
```bash
send_reminder() {
  AGENT=$1
  REMAINING=$2

  curl -X POST "http://localhost:23000/api/messages" \
    -H "Content-Type: application/json" \
    -d "{
      \"to\": \"$AGENT\",
      \"subject\": \"Reminder: Acknowledgment Required\",
      \"priority\": \"high\",
      \"content\": {
        \"type\": \"reminder\",
        \"message\": \"Reminder: Please reply 'ok' when ready for the pending operation. $REMAINING seconds remaining before I proceed.\",
        \"time_remaining\": \"$REMAINING seconds\",
        \"reminder_number\": $((${#REMINDER_SENT[@]} + 1))
      }
    }"
}
```

### 3.3.4 Process response

**Purpose:** Handle the agent's acknowledgment (or other response).

**Expected responses:**
1. `"ok"` - Agent is ready, proceed with operation
2. `"wait"` or `"not ready"` - Agent needs more time
3. `"cancel"` - Agent requests operation cancellation
4. Other message - Treat as information, still waiting

**Response handling:**
```bash
check_acknowledgment() {
  AGENT=$1

  # Query for unread messages from this agent
  RESPONSE=$(curl -s "http://localhost:23000/api/messages?agent=chief-of-staff&action=list&status=unread")

  # Look for acknowledgment message
  ACK_MSG=$(echo $RESPONSE | jq -r ".messages[] | select(.from == \"$AGENT\")")

  if [ -z "$ACK_MSG" ]; then
    return 1  # No message
  fi

  # Check message content
  MSG_TYPE=$(echo $ACK_MSG | jq -r '.content.type')
  MSG_TEXT=$(echo $ACK_MSG | jq -r '.content.message' | tr '[:upper:]' '[:lower:]')

  # Handle different responses
  case "$MSG_TEXT" in
    *"ok"*)
      echo "Agent $AGENT acknowledged - ready to proceed"
      return 0
      ;;
    *"wait"*|*"not ready"*)
      echo "Agent $AGENT requested more time"
      # Optionally extend timeout
      return 1
      ;;
    *"cancel"*)
      echo "Agent $AGENT requested cancellation"
      # Handle cancellation
      return 2
      ;;
    *)
      echo "Agent $AGENT sent: $MSG_TEXT"
      # Unknown response - continue waiting
      return 1
      ;;
  esac
}
```

### 3.3.5 Proceed or timeout

**Purpose:** Either proceed with operation after acknowledgment, or handle timeout.

**On acknowledgment received:**
```bash
if [ $ACK_RESULT -eq 0 ]; then
  echo "[$(date)] Proceeding with operation - agent acknowledged"
  perform_operation $AGENT $OPERATION
fi
```

**On timeout:**
```bash
if check_timeout; then
  echo "[$(date)] WARNING: Timeout - no acknowledgment from $AGENT after $TIMEOUT seconds"

  # Send timeout notice
  curl -X POST "http://localhost:23000/api/messages" \
    -H "Content-Type: application/json" \
    -d "{
      \"to\": \"$AGENT\",
      \"subject\": \"Proceeding Without Acknowledgment\",
      \"priority\": \"high\",
      \"content\": {
        \"type\": \"timeout-notice\",
        \"message\": \"No response received after 2 minutes. Proceeding with operation now.\",
        \"operation\": \"$OPERATION\",
        \"timeout_occurred\": true
      }
    }"

  # Log timeout and proceed
  log_timeout $AGENT $OPERATION
  perform_operation $AGENT $OPERATION
fi
```

---

## 3.4 Acknowledgment message format

**Standard acknowledgment request:**

```json
{
  "to": "agent-session-name",
  "subject": "[Operation] Pending - Acknowledgment Required",
  "priority": "high",
  "content": {
    "type": "pre-operation",
    "message": "I will [operation]. Please finish your current work and reply with 'ok' when ready. I will wait up to 2 minutes.",
    "operation": "skill-install|plugin-install|restart|maintenance",
    "requires_acknowledgment": true,
    "acknowledgment_timeout": 120,
    "acknowledgment_reminder_intervals": [30, 60, 90],
    "acknowledgment_instructions": {
      "ready": "Reply with 'ok' to proceed",
      "need_time": "Reply with 'wait' for more time (up to 1 additional minute)",
      "cancel": "Reply with 'cancel' to abort the operation"
    }
  }
}
```

---

## 3.5 Reminder message format

**Standard reminder:**

```json
{
  "to": "agent-session-name",
  "subject": "Reminder: Acknowledgment Required",
  "priority": "high",
  "content": {
    "type": "reminder",
    "message": "Reminder: Please reply 'ok' when ready for the pending [operation]. [X] seconds remaining before I proceed.",
    "original_operation": "[operation-type]",
    "time_remaining": "[seconds] seconds",
    "reminder_number": 1,
    "total_reminders": 3
  }
}
```

**Reminder escalation:**

| Reminder | Time | Message Tone | Remaining |
|----------|------|--------------|-----------|
| 1 | 30s | Gentle reminder | 90 seconds |
| 2 | 60s | Firm reminder | 60 seconds |
| 3 | 90s | Final notice | 30 seconds |

---

## 3.6 Response handling

**Valid agent responses:**

| Response | Meaning | Chief of Staff Action |
|----------|---------|----------------------|
| `"ok"` | Ready to proceed | Proceed with operation |
| `"OK"` | Ready (case insensitive) | Proceed with operation |
| `"ready"` | Ready to proceed | Proceed with operation |
| `"wait"` | Need more time | Extend timeout by 1 minute (once only) |
| `"not ready"` | Need more time | Extend timeout by 1 minute (once only) |
| `"cancel"` | Abort operation | Cancel operation, notify agent |
| `"abort"` | Abort operation | Cancel operation, notify agent |
| Other | Information | Log message, continue waiting |

**Response message format (from agent):**

```json
{
  "from": "agent-session-name",
  "to": "chief-of-staff",
  "subject": "RE: [Operation] Pending - Acknowledgment Required",
  "content": {
    "type": "acknowledgment",
    "message": "ok",
    "ready": true,
    "notes": "Finished saving current work, ready for operation"
  }
}
```

---

## 3.7 Timeout behavior

**What happens when timeout is reached:**

1. **Log the timeout**
   ```
   [2025-02-02T10:30:00Z] TIMEOUT: No acknowledgment from code-impl-auth after 120 seconds
   ```

2. **Send timeout notice to agent**
   ```json
   {
     "type": "timeout-notice",
     "message": "No response received after 2 minutes. Proceeding with operation now."
   }
   ```

3. **Proceed with operation anyway**
   - Operation is performed
   - Agent state may be lost
   - Post-operation notification still sent

4. **Record timeout in operation log**
   ```json
   {
     "operation": "skill-install",
     "agent": "code-impl-auth",
     "acknowledgment_received": false,
     "timeout_occurred": true,
     "proceeded_anyway": true
   }
   ```

**Timeout configuration:**

| Setting | Default | Description |
|---------|---------|-------------|
| `acknowledgment_timeout` | 120 seconds | Maximum wait time |
| `reminder_intervals` | [30, 60, 90] | When to send reminders |
| `extension_allowed` | true | Can agent request more time |
| `max_extension` | 60 seconds | Maximum additional time |
| `proceed_on_timeout` | true | Continue if no response |

---

## 3.8 Examples

### Example 1: Successful Acknowledgment Flow

```bash
# 1. Send initial request
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "code-impl-auth",
    "subject": "Skill Installation Pending - Acknowledgment Required",
    "priority": "high",
    "content": {
      "type": "pre-operation",
      "message": "I will install the security-audit skill. Please finish your current work and reply with \"ok\" when ready. I will wait up to 2 minutes.",
      "operation": "skill-install",
      "requires_acknowledgment": true,
      "acknowledgment_timeout": 120
    }
  }'

# 2. Agent responds after 25 seconds
# Response from agent:
# {
#   "from": "code-impl-auth",
#   "content": {"type": "acknowledgment", "message": "ok"}
# }

# 3. Chief of Staff proceeds
echo "[$(date)] Acknowledgment received - proceeding with skill installation"
aimaestro-agent.sh hibernate code-impl-auth
# ... install skill ...
aimaestro-agent.sh wake code-impl-auth
```

### Example 2: Acknowledgment with Reminders

```bash
# 1. Send initial request
# ... (same as above)

# 2. No response by 30 seconds - send reminder 1
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "code-impl-auth",
    "subject": "Reminder: Acknowledgment Required",
    "priority": "high",
    "content": {
      "type": "reminder",
      "message": "Reminder: Please reply \"ok\" when ready for skill installation. 90 seconds remaining.",
      "time_remaining": "90 seconds",
      "reminder_number": 1
    }
  }'

# 3. No response by 60 seconds - send reminder 2
# ... similar to above with 60 seconds remaining

# 4. Agent responds at 75 seconds
# Response: {"message": "ok"}

# 5. Proceed with operation
echo "[$(date)] Acknowledgment received after 2 reminders - proceeding"
```

### Example 3: Timeout and Proceed

```bash
# 1. Send initial request
# ...

# 2. Send reminders at 30s, 60s, 90s
# ...

# 3. No response after 120 seconds - timeout
echo "[$(date)] WARNING: Timeout reached - no acknowledgment"

# 4. Send timeout notice
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "code-impl-auth",
    "subject": "Proceeding Without Acknowledgment",
    "priority": "high",
    "content": {
      "type": "timeout-notice",
      "message": "No response received after 2 minutes. Proceeding with skill installation now. You will be hibernated shortly.",
      "operation": "skill-install",
      "timeout_occurred": true
    }
  }'

# 5. Proceed anyway
aimaestro-agent.sh hibernate code-impl-auth
```

### Example 4: Agent Requests Extension

```bash
# 1. Send initial request
# ...

# 2. Agent responds at 45 seconds with "wait"
# Response: {"message": "wait", "notes": "Need 30 more seconds to save state"}

# 3. Extend timeout
NEW_TIMEOUT=$((TIMEOUT + 60))  # Add 1 minute
echo "[$(date)] Agent requested extension - new timeout: $NEW_TIMEOUT seconds"

# 4. Send extension acknowledgment
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "code-impl-auth",
    "subject": "Extension Granted",
    "priority": "normal",
    "content": {
      "type": "extension-granted",
      "message": "Extension granted. You now have 135 seconds remaining. Please reply \"ok\" when ready.",
      "new_timeout": "135 seconds",
      "extension_allowed_again": false
    }
  }'

# 5. Continue waiting with new timeout
```

---

## 3.9 Troubleshooting

### Issue: Agent never responds to acknowledgment requests

**Symptoms:** All acknowledgment requests timeout, reminders ignored.

**Resolution:**
1. Verify agent is online and not stuck
2. Check if agent has AI Maestro polling enabled
3. Verify message is being delivered (check inbox)
4. Agent may be in a blocking operation
5. Consider agent restart if consistently unresponsive

### Issue: Acknowledgment received but not recognized

**Symptoms:** Agent says they responded, system shows timeout.

**Resolution:**
1. Check response message format - must contain "ok"
2. Verify from field matches expected agent name
3. Check for typos in response message
4. Review message timestamp ordering
5. Check if response went to wrong recipient

### Issue: Reminders not being sent

**Symptoms:** Agent only receives initial request, no reminders.

**Resolution:**
1. Verify reminder timer is running
2. Check reminder interval configuration
3. Ensure loop is not exiting early
4. Verify API is responding for reminder sends
5. Check logs for reminder send errors

### Issue: Timeout too short for agent task

**Symptoms:** Agent cannot finish work in 2 minutes.

**Resolution:**
1. Agent should respond with "wait" to request extension
2. Consider longer default timeout for specific operations
3. Agent should checkpoint work more frequently
4. Consider breaking large operations into smaller ones
5. Use pre-notification before the acknowledgment request

### Issue: Multi-agent acknowledgment tracking fails

**Symptoms:** Lost track of which agents acknowledged.

**Resolution:**
1. Use broadcast_id to correlate responses
2. Maintain explicit list of expected vs received acknowledgments
3. Log each acknowledgment with agent name
4. Consider using operation_id in messages
5. Implement acknowledgment tracking data structure
