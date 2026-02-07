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

Use the `agent-messaging` skill to send the acknowledgment request:
- **Recipient**: the target agent session name
- **Subject**: `[Operation] Pending - Acknowledgment Required`
- **Priority**: `high`
- **Content**: type `pre-operation`, message: "I will [operation description]. Please finish your current work and reply with 'ok' when ready. I will wait up to 2 minutes." Include fields: `operation` (the operation type), `requires_acknowledgment` (true), `acknowledgment_timeout` (120), `acknowledgment_reminder_intervals` ([30, 60, 90]).

**Critical elements:**
1. Clear statement of what will happen
2. Explicit request for "ok" response
3. Statement of timeout duration
4. High priority to ensure visibility

### 3.3.2 Start timeout timer

**Purpose:** Begin tracking time for acknowledgment response.

After sending the request, start a 2-minute timer. Record the start time and monitor elapsed time. The timeout is 120 seconds by default.

### 3.3.3 Send reminders

**Purpose:** Remind agents who have not responded.

**Reminder schedule:**
- 30 seconds: First reminder (90 seconds remaining)
- 60 seconds: Second reminder (60 seconds remaining)
- 90 seconds: Final reminder (30 seconds remaining)

For each reminder, use the `agent-messaging` skill to send a reminder message:
- **Recipient**: the target agent session name
- **Subject**: `Reminder: Acknowledgment Required`
- **Priority**: `high`
- **Content**: type `reminder`, message: "Reminder: Please reply 'ok' when ready for the pending operation. [X] seconds remaining before I proceed." Include fields: `time_remaining` (remaining seconds), `reminder_number` (1, 2, or 3).

### 3.3.4 Process response

**Purpose:** Handle the agent's acknowledgment (or other response).

**Expected responses:**
1. `"ok"` - Agent is ready, proceed with operation
2. `"wait"` or `"not ready"` - Agent needs more time
3. `"cancel"` - Agent requests operation cancellation
4. Other message - Treat as information, still waiting

Use the `agent-messaging` skill to check for unread messages from the target agent. Look for messages with type `acknowledgment` and content containing "ok", "wait", or "cancel".

**Response handling logic:**
- If message contains "ok" or "ready": Proceed with operation
- If message contains "wait" or "not ready": Extend timeout by 1 minute (once only)
- If message contains "cancel" or "abort": Cancel operation and notify agent
- Other messages: Log the content and continue waiting

### 3.3.5 Proceed or timeout

**Purpose:** Either proceed with operation after acknowledgment, or handle timeout.

**On acknowledgment received:**
- Log that the agent acknowledged
- Proceed with the planned operation

**On timeout:**
1. Log the timeout with timestamp
2. Use the `agent-messaging` skill to send a timeout notice:
   - **Recipient**: the target agent session name
   - **Subject**: `Proceeding Without Acknowledgment`
   - **Priority**: `high`
   - **Content**: type `timeout-notice`, message: "No response received after 2 minutes. Proceeding with operation now." Include fields: `operation` (the operation type), `timeout_occurred` (true).
3. Log the timeout and proceed with the operation

---

## 3.4 Acknowledgment message format

**Standard acknowledgment request message fields:**

| Field | Required | Description |
|-------|----------|-------------|
| Recipient | Yes | Target agent session name |
| Subject | Yes | "[Operation] Pending - Acknowledgment Required" |
| Priority | Yes | `high` |
| Content type | Yes | `pre-operation` |
| Content message | Yes | Human-readable description with "ok" request |
| Content operation | Yes | Operation type: `skill-install`, `plugin-install`, `restart`, `maintenance` |
| Content requires_acknowledgment | Yes | `true` |
| Content acknowledgment_timeout | No | Timeout in seconds (default 120) |
| Content acknowledgment_reminder_intervals | No | Array of reminder times: [30, 60, 90] |
| Content acknowledgment_instructions | No | Object with `ready`, `need_time`, `cancel` instruction strings |

---

## 3.5 Reminder message format

**Standard reminder message fields:**

| Field | Required | Description |
|-------|----------|-------------|
| Recipient | Yes | Target agent session name |
| Subject | Yes | "Reminder: Acknowledgment Required" |
| Priority | Yes | `high` |
| Content type | Yes | `reminder` |
| Content message | Yes | "Reminder: Please reply 'ok' when ready. [X] seconds remaining." |
| Content original_operation | No | The operation type being acknowledged |
| Content time_remaining | Yes | Remaining seconds as string |
| Content reminder_number | Yes | 1, 2, or 3 |
| Content total_reminders | No | 3 |

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

**Expected response message from agent:**
The agent should use the `agent-messaging` skill to reply with:
- **Recipient**: `chief-of-staff` session name
- **Subject**: `RE: [Operation] Pending - Acknowledgment Required`
- **Content**: type `acknowledgment`, message: "ok", plus optional `ready` (true/false) and `notes` fields.

---

## 3.7 Timeout behavior

**What happens when timeout is reached:**

1. **Log the timeout**
   ```
   [2025-02-02T10:30:00Z] TIMEOUT: No acknowledgment from code-impl-auth after 120 seconds
   ```

2. **Send timeout notice to agent** using the `agent-messaging` skill:
   - **Recipient**: the target agent session name
   - **Subject**: `Proceeding Without Acknowledgment`
   - **Priority**: `high`
   - **Content**: type `timeout-notice`, message: "No response received after 2 minutes. Proceeding with operation now."

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

1. Use the `agent-messaging` skill to send the initial acknowledgment request:
   - **Recipient**: `code-impl-auth`
   - **Subject**: `Skill Installation Pending - Acknowledgment Required`
   - **Priority**: `high`
   - **Content**: type `pre-operation`, message: "I will install the security-audit skill. Please finish your current work and reply with 'ok' when ready. I will wait up to 2 minutes." Include `operation`: "skill-install", `requires_acknowledgment`: true, `acknowledgment_timeout`: 120.

2. Agent responds after 25 seconds with type `acknowledgment`, message: "ok".

3. Chief of Staff proceeds:
   - Log acknowledgment received
   - Use the `ai-maestro-agents-management` skill to hibernate the agent
   - Install the skill
   - Use the `ai-maestro-agents-management` skill to wake the agent

### Example 2: Acknowledgment with Reminders

1. Send initial acknowledgment request (same as Example 1).

2. No response by 30 seconds. Use the `agent-messaging` skill to send reminder 1:
   - **Recipient**: `code-impl-auth`
   - **Subject**: `Reminder: Acknowledgment Required`
   - **Priority**: `high`
   - **Content**: type `reminder`, message: "Reminder: Please reply 'ok' when ready for skill installation. 90 seconds remaining." Include `time_remaining`: "90 seconds", `reminder_number`: 1.

3. No response by 60 seconds. Send reminder 2 with 60 seconds remaining.

4. Agent responds at 75 seconds with message: "ok".

5. Proceed with operation.

### Example 3: Timeout and Proceed

1. Send initial acknowledgment request.
2. Send reminders at 30s, 60s, 90s.
3. No response after 120 seconds - timeout reached.
4. Use the `agent-messaging` skill to send timeout notice:
   - **Recipient**: `code-impl-auth`
   - **Subject**: `Proceeding Without Acknowledgment`
   - **Priority**: `high`
   - **Content**: type `timeout-notice`, message: "No response received after 2 minutes. Proceeding with skill installation now. You will be hibernated shortly." Include `operation`: "skill-install", `timeout_occurred`: true.
5. Proceed with operation anyway. Use the `ai-maestro-agents-management` skill to hibernate the agent.

### Example 4: Agent Requests Extension

1. Send initial acknowledgment request.
2. Agent responds at 45 seconds with message: "wait", notes: "Need 30 more seconds to save state".
3. Extend timeout by 60 seconds (new total: 135 seconds remaining from original start).
4. Use the `agent-messaging` skill to send extension confirmation:
   - **Recipient**: `code-impl-auth`
   - **Subject**: `Extension Granted`
   - **Priority**: `normal`
   - **Content**: type `extension-granted`, message: "Extension granted. You now have 135 seconds remaining. Please reply 'ok' when ready." Include `new_timeout`: "135 seconds", `extension_allowed_again`: false.
5. Continue waiting with new timeout.

---

## 3.9 Troubleshooting

### Issue: Agent never responds to acknowledgment requests

**Symptoms:** All acknowledgment requests timeout, reminders ignored.

**Resolution:**
1. Verify agent is online and not stuck
2. Check if agent has AI Maestro polling enabled
3. Use the `agent-messaging` skill to verify message is being delivered (check inbox)
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
4. Verify messaging skill is responding for reminder sends
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
