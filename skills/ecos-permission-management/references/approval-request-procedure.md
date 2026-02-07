# Approval Request Procedure Reference

## Contents

- 1.1 What is an approval request - Understanding the request format
- 1.2 When to request approval - Triggers for approval workflow
  - 1.2.1 Agent spawn triggers - New agent needed
  - 1.2.2 Agent terminate triggers - Agent work complete or failed
  - 1.2.3 Agent hibernate triggers - Resource optimization needed
  - 1.2.4 Agent wake triggers - Resuming work
  - 1.2.5 Plugin install triggers - New capability required
- 1.3 Approval request procedure - Step-by-step request process
  - 1.3.1 Operation identification - Determining request type
  - 1.3.2 Justification preparation - Explaining why
  - 1.3.3 Message composition - Formatting the request
  - 1.3.4 Transmission via `agent-messaging` skill - Sending to EAMA
  - 1.3.5 Response awaiting - Waiting with timeout
- 1.4 Request message format - Standard message structure
- 1.5 Examples - Approval request scenarios
- 1.6 Troubleshooting - Request failures and recovery

---

## 1.1 What Is an Approval Request

An approval request is a formal message sent from ECOS (Chief of Staff) to EAMA (Assistant Manager) asking for authorization to perform a privileged operation. The request contains all information EAMA needs to make an informed decision on behalf of the user.

**Approval requests are structured messages that include:**
- A unique request identifier for tracking
- The type of operation being requested
- Details specific to the operation
- A justification explaining why the operation is needed

**The request-response cycle:**
1. ECOS identifies an operation requiring approval
2. ECOS composes and sends an approval request to EAMA
3. EAMA receives the request and presents it to the user
4. The user makes a decision (approve, reject, or modify)
5. EAMA sends the decision back to ECOS
6. ECOS proceeds based on the decision

---

## 1.2 When to Request Approval

ECOS must request approval before executing any of the following operations:

### 1.2.1 Agent Spawn Triggers

Request spawn approval when:
- A new task requires a dedicated agent
- Parallel execution requires additional agents
- A specialized capability is needed that requires a new agent type
- The orchestrator (EOA) requests agent creation
- The architect (EAA) design calls for new agents

**Do NOT request approval for:**
- Querying agent registry (read-only)
- Checking agent status
- Listing existing agents

### 1.2.2 Agent Terminate Triggers

Request terminate approval when:
- An agent has completed its assigned task
- An agent has failed unrecoverably
- An agent is redundant (duplicate capability)
- The user requests agent termination via EAMA
- Resource constraints require agent reduction

**Do NOT request approval for:**
- Checking if an agent can be terminated (pre-flight check)
- Preparing termination (state save, cleanup planning)

### 1.2.3 Agent Hibernate Triggers

Request hibernate approval when:
- An agent has been idle beyond the threshold (default: 30 minutes)
- Resource pressure requires freeing capacity
- Scheduled maintenance window approaching
- End-of-day resource conservation

**Do NOT request approval for:**
- Checking agent idle time
- Preparing hibernation state snapshot

### 1.2.4 Agent Wake Triggers

Request wake approval when:
- New work arrives for a hibernated agent
- Priority task requires the agent's capability
- Scheduled wake time reached
- User requests agent wake via EAMA

**Do NOT request approval for:**
- Checking if an agent is hibernated
- Checking hibernated agent state availability

### 1.2.5 Plugin Install Triggers

Request plugin install approval when:
- A new capability is needed that requires a plugin
- A plugin update is available with security fixes
- The architect (EAA) design requires a specific plugin
- The user requests plugin installation via EAMA

**Do NOT request approval for:**
- Listing installed plugins
- Checking plugin availability in marketplace
- Validating plugin compatibility

---

## 1.3 Approval Request Procedure

Follow these steps to request approval from EAMA:

### 1.3.1 Operation Identification

**Step 1:** Determine the exact operation type.

Valid operation types:
- `spawn` - Creating a new agent
- `terminate` - Permanently stopping an agent
- `hibernate` - Suspending an agent
- `wake` - Resuming a hibernated agent
- `plugin_install` - Installing a Claude Code plugin

**Step 2:** Gather operation-specific details.

| Operation | Required Details |
|-----------|------------------|
| spawn | agent_name, agent_role, task, working_directory |
| terminate | agent_name, reason, final_report, pending_work |
| hibernate | agent_name, idle_duration, last_activity |
| wake | agent_name, reason, task_to_resume |
| plugin_install | plugin_name, version, source, capability |

### 1.3.2 Justification Preparation

**Step 3:** Write a clear justification for the operation.

A good justification answers:
- Why is this operation needed now?
- What will happen if the operation is not performed?
- What triggered this request?
- What references support this request? (design docs, user requests, etc.)

**Example justifications:**

```
spawn: "New authentication module required per design doc EAA-AUTH-001.
        Code implementer agent needed to execute implementation tasks."

terminate: "Agent has completed all assigned data processing tasks.
            1500 records processed. No pending work remains."

hibernate: "Agent has been idle for 45 minutes. No incoming tasks.
            Hibernating to conserve resources."

wake: "New batch of data arrived requiring processing.
       Agent data-processor-03 has the required context."

plugin_install: "Code review capability needed for PR #42.
                 Plugin eia-code-reviewer provides required functionality."
```

### 1.3.3 Message Composition

**Step 4:** Compose the approval request message.

The message must follow this structure:
- **From**: `ecos-chief-of-staff`
- **To**: `eama-assistant-manager`
- **Subject**: `[APPROVAL REQUEST] {Operation}: {Target}`
- **Priority**: `high` or `normal`
- **Content**: type `approval_request`, message: "Requesting approval to {operation} {target}". Include `request_id` (unique identifier), `operation` (operation type), `details` (operation-specific details object), `justification` (justification text).

**Request ID format:** `{operation}-req-{date}-{sequence}`

Examples:
- `spawn-req-2025-02-02-001`
- `terminate-req-2025-02-02-003`
- `plugin_install-req-2025-02-02-001`

**Priority guidelines:**
- `high` - For spawn and wake operations (blocking work)
- `normal` - For terminate and hibernate operations (cleanup)
- `urgent` - Only for escalation reminders (not initial request)

### 1.3.4 Transmission via `agent-messaging` skill

**Step 5:** Use the `agent-messaging` skill to send the composed approval request message to EAMA.

**Verify transmission:**
- Check the delivery confirmation from the skill
- Record the message ID returned
- Record transmission timestamp

**If transmission fails:**
- Retry up to 3 times with 5-second intervals
- If all retries fail, log error and notify user directly
- Do NOT proceed with operation without approval

### 1.3.5 Response Awaiting

**Step 6:** Wait for EAMA response with timeout handling.

Timeout schedule:
- T+0: Request sent
- T+60s: Send reminder notification
- T+90s: Send urgent notification
- T+120s: Timeout reached

**Check for response:**

Use the `agent-messaging` skill to check for unread messages addressed to `ecos-chief-of-staff`. Filter for messages containing the matching `request_id` (e.g., `spawn-req-2025-02-02-001`).

**Valid response decisions:**
- `approved` - Proceed with operation
- `rejected` - Do not proceed, log rejection
- `modified` - Proceed with modifications in response
- `delayed` - Wait for specified time, then re-request

---

## 1.4 Request Message Format

### Complete Request Schema

The approval request message sent via the `agent-messaging` skill must contain:

- **from**: string (required) - must be `ecos-chief-of-staff`
- **to**: string (required) - must be `eama-assistant-manager`
- **subject**: string (required) - `[APPROVAL REQUEST] {Operation}: {Target}`
- **priority**: string (required) - `high`, `normal`, or `urgent`
- **content**:
  - **type**: string (required) - must be `approval_request`
  - **message**: string (required) - human-readable summary
  - **request_id**: string (required) - unique identifier
  - **operation**: string (required) - `spawn`, `terminate`, `hibernate`, `wake`, or `plugin_install`
  - **details**: object (required) - operation-specific details
  - **justification**: string (required) - why this operation is needed

### Operation-Specific Details

**Spawn details:**
- `agent_name`: unique agent identifier
- `agent_role`: role/type of agent
- `task`: assigned task description
- `working_directory`: absolute path
- `expected_duration`: estimated time
- `resource_requirements`: standard, high, or low
- `tags`: optional metadata tags list

**Terminate details:**
- `agent_name`: agent to terminate
- `current_status`: running, idle, or error
- `reason`: task_complete, failed, redundant, or user_request
- `final_report`: summary of work done
- `pending_work`: none or description of incomplete work

**Hibernate details:**
- `agent_name`: agent to hibernate
- `idle_duration`: how long agent has been idle
- `last_activity`: ISO-8601 timestamp
- `expected_wake_trigger`: what will wake this agent

**Wake details:**
- `agent_name`: agent to wake
- `reason`: why waking is needed
- `task_to_resume`: task description
- `priority_level`: normal, high, or urgent

**Plugin install details:**
- `plugin_name`: plugin identifier
- `version`: specific version or "latest"
- `source`: marketplace name or local path
- `capability`: what capability this adds
- `security_implications`: any security notes

---

## 1.5 Examples

### Example: Spawn Request

Use the `agent-messaging` skill to send:
- **Recipient**: `eama-assistant-manager`
- **Subject**: `[APPROVAL REQUEST] Spawn: frontend-dev-02`
- **Priority**: `high`
- **Content**: type `approval_request`, message: "Requesting approval to spawn frontend development agent". Include `request_id`: "spawn-req-2025-02-02-004", `operation`: "spawn", `details`: { `agent_name`: "frontend-dev-02", `agent_role`: "frontend-developer", `task`: "Implement React components for dashboard", `working_directory`: "/Users/dev/project/frontend", `expected_duration`: "4 hours", `resource_requirements`: "standard", `tags`: ["react", "dashboard", "frontend"] }, `justification`: "Dashboard implementation requires dedicated frontend agent. Design doc EAA-DASH-003 specifies React component implementation."

### Example: Hibernate Request

Use the `agent-messaging` skill to send:
- **Recipient**: `eama-assistant-manager`
- **Subject**: `[APPROVAL REQUEST] Hibernate: api-tester-01`
- **Priority**: `normal`
- **Content**: type `approval_request`, message: "Requesting approval to hibernate idle testing agent". Include `request_id`: "hibernate-req-2025-02-02-001", `operation`: "hibernate", `details`: { `agent_name`: "api-tester-01", `idle_duration`: "47 minutes", `last_activity`: "2025-02-02T09:13:00Z", `expected_wake_trigger`: "New API endpoints ready for testing" }, `justification`: "Agent has been idle for 47 minutes with no pending tests. API development still in progress. Hibernating to conserve resources."

### Example: Plugin Install Request

Use the `agent-messaging` skill to send:
- **Recipient**: `eama-assistant-manager`
- **Subject**: `[APPROVAL REQUEST] Plugin Install: perfect-skill-suggester`
- **Priority**: `high`
- **Content**: type `approval_request`, message: "Requesting approval to install skill suggestion plugin". Include `request_id`: "plugin_install-req-2025-02-02-001", `operation`: "plugin_install", `details`: { `plugin_name`: "perfect-skill-suggester", `version`: "1.2.2", `source`: "emasoft-plugins", `capability`: "AI-analyzed skill activation based on task context", `security_implications`: "Runs hooks on prompt submission. No network access required." }, `justification`: "Skill activation currently manual. PSS automates skill matching to improve agent efficiency."

---

## 1.6 Troubleshooting

### Issue: Message send fails with connection error

**Symptoms:**
- Messaging skill reports delivery failure
- No confirmation returned

**Cause:** AI Maestro server may not be running.

**Resolution:**
1. Use the `ai-maestro-agents-management` skill to check system health
2. If AI Maestro is not running, start it
3. Retry the request
4. If still failing, notify user directly about the infrastructure issue

### Issue: EAMA returns "invalid request format" error

**Symptoms:**
- Error response about missing fields

**Cause:** Request message is missing required fields or has wrong format.

**Resolution:**
1. Verify all required fields are present (see Section 1.4)
2. Ensure content type is exactly `approval_request`
3. Verify `request_id` follows the required format
4. Resubmit with corrected format

### Issue: No response received within timeout

**Symptoms:**
- Request sent successfully
- No response after 120 seconds

**Cause:** EAMA may be offline, busy, or user is unavailable.

**Resolution:**
1. Use the `ai-maestro-agents-management` skill to verify EAMA is online
2. If EAMA offline, wait for it to come online or notify user
3. If EAMA online but no response, follow escalation procedure
4. See [approval-escalation.md](approval-escalation.md) for timeout handling

### Issue: Received unexpected response format

**Symptoms:**
- Response received but cannot parse
- Missing decision field

**Cause:** Response from EAMA does not match expected schema.

**Resolution:**
1. Log the raw response for debugging
2. Extract decision if present in any form
3. If completely unparseable, send clarification request to EAMA
4. Treat as "delayed" and re-request after 30 seconds

### Issue: Request ID collision

**Symptoms:**
- Same request ID used twice
- Confusion about which response belongs to which request

**Cause:** Request ID generation not unique.

**Resolution:**
1. Always use date and sequence number in request ID
2. Maintain a local sequence counter
3. If collision detected, regenerate with new sequence number
4. Consider adding timestamp milliseconds for uniqueness

---

**Version:** 1.0
**Last Updated:** 2025-02-02
**Related:** [SKILL.md](../SKILL.md), [approval-tracking.md](approval-tracking.md), [approval-escalation.md](approval-escalation.md)
