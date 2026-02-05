# Approval Workflow Engine

Complete reference for the ECOS approval workflow system, covering request submission, decision processing, timeout handling, and escalation procedures.

## Contents (Use-Case-Oriented)

- [1. Submitting an approval request for an operation](#1-submitting-an-approval-request-for-an-operation)
  - [1.1 Approval request template and required fields](#11-approval-request-template-and-required-fields)
  - [1.2 Generating unique request IDs](#12-generating-unique-request-ids)
  - [1.3 Calculating timeout timestamps](#13-calculating-timeout-timestamps)
  - [1.4 Checking autonomous mode before requesting](#14-checking-autonomous-mode-before-requesting)
  - [1.5 Validating request completeness](#15-validating-request-completeness)
- [2. Understanding approval types and their policies](#2-understanding-approval-types-and-their-policies)
  - [2.1 Complete list of approval types](#21-complete-list-of-approval-types)
  - [2.2 Default timeouts by type](#22-default-timeouts-by-type)
  - [2.3 Auto-reject vs escalate policies](#23-auto-reject-vs-escalate-policies)
- [3. Tracking approval request status lifecycle](#3-tracking-approval-request-status-lifecycle)
  - [3.1 Status definitions and transitions](#31-status-definitions-and-transitions)
  - [3.2 Pending approvals file structure](#32-pending-approvals-file-structure)
  - [3.3 Moving requests from pending to history](#33-moving-requests-from-pending-to-history)
- [4. Forwarding requests to manager via EAMA](#4-forwarding-requests-to-manager-via-eama)
  - [4.1 AI Maestro message format for approval requests](#41-ai-maestro-message-format-for-approval-requests)
  - [4.2 Setting priority levels](#42-setting-priority-levels)
  - [4.3 Formatting human-readable request summaries](#43-formatting-human-readable-request-summaries)
- [5. Handling escalation timeline and reminders](#5-handling-escalation-timeline-and-reminders)
  - [5.1 Escalation timeline stages (0s, 30s, 60s, 90s, 120s)](#51-escalation-timeline-stages-0s-30s-60s-90s-120s)
  - [5.2 Sending reminder messages at intervals](#52-sending-reminder-messages-at-intervals)
  - [5.3 Tracking reminder count and elapsed time](#53-tracking-reminder-count-and-elapsed-time)
- [6. Processing timeout conditions](#6-processing-timeout-conditions)
  - [6.1 Timeout policy decision tree by type](#61-timeout-policy-decision-tree-by-type)
  - [6.2 Auto-rejecting non-critical requests](#62-auto-rejecting-non-critical-requests)
  - [6.3 Escalating critical operations with extended timeout](#63-escalating-critical-operations-with-extended-timeout)
  - [6.4 Final auto-reject after extended timeout expires](#64-final-auto-reject-after-extended-timeout-expires)
- [7. Receiving and processing approval decisions](#7-receiving-and-processing-approval-decisions)
  - [7.1 Decision message format from EAMA](#71-decision-message-format-from-eama)
  - [7.2 Validating decision matches pending request](#72-validating-decision-matches-pending-request)
  - [7.3 Decision types: approved, rejected, revision_needed](#73-decision-types-approved-rejected-revision_needed)
  - [7.4 Updating status and logging decision](#74-updating-status-and-logging-decision)
- [8. Executing approved operations](#8-executing-approved-operations)
  - [8.1 Transitioning status to executing](#81-transitioning-status-to-executing)
  - [8.2 Delegating execution to appropriate ECOS agent](#82-delegating-execution-to-appropriate-ecos-agent)
  - [8.3 Monitoring execution progress](#83-monitoring-execution-progress)
  - [8.4 Handling execution success](#84-handling-execution-success)
  - [8.5 Handling execution failure](#85-handling-execution-failure)
- [9. Executing rollback procedures after failures](#9-executing-rollback-procedures-after-failures)
  - [9.1 Initiating rollback from request rollback_plan](#91-initiating-rollback-from-request-rollback_plan)
  - [9.2 Automated vs manual rollback steps](#92-automated-vs-manual-rollback-steps)
  - [9.3 Logging rollback progress](#93-logging-rollback-progress)
  - [9.4 Escalating rollback failures immediately](#94-escalating-rollback-failures-immediately)
- [10. Using autonomous mode for pre-approved operations](#10-using-autonomous-mode-for-pre-approved-operations)
  - [10.1 Autonomous mode configuration structure](#101-autonomous-mode-configuration-structure)
  - [10.2 Per-operation permission rules](#102-per-operation-permission-rules)
  - [10.3 Rate limiting (max per hour counters)](#103-rate-limiting-max-per-hour-counters)
  - [10.4 Checking and incrementing counters](#104-checking-and-incrementing-counters)
  - [10.5 Autonomous mode grant and revocation](#105-autonomous-mode-grant-and-revocation)
- [11. Maintaining audit trail logs](#11-maintaining-audit-trail-logs)
  - [11.1 Log entry format and event types](#111-log-entry-format-and-event-types)
  - [11.2 Recording submissions, decisions, executions, rollbacks](#112-recording-submissions-decisions-executions-rollbacks)
  - [11.3 Audit trail file location and structure](#113-audit-trail-file-location-and-structure)
- [12. Handling error conditions](#12-handling-error-conditions)
  - [12.1 Invalid request format errors](#121-invalid-request-format-errors)
  - [12.2 Missing rollback plan errors](#122-missing-rollback-plan-errors)
  - [12.3 EAMA unreachable retry logic](#123-eama-unreachable-retry-logic)
  - [12.4 Duplicate request ID handling](#124-duplicate-request-id-handling)

---

## 1. Submitting an approval request for an operation

### 1.1 Approval request template and required fields

All approval requests MUST follow this exact JSON structure:

```json
{
  "request_id": "AR-<timestamp>-<random>",
  "type": "<approval_type>",
  "requester": "<agent_session_name>",
  "operation": {
    "action": "<action_description>",
    "target": "<target_resource>",
    "parameters": {}
  },
  "justification": "<why_this_operation_is_needed>",
  "impact": {
    "scope": "local|project|global",
    "affected_agents": ["<agent1>", "<agent2>"],
    "affected_resources": ["<resource1>", "<resource2>"],
    "risk_level": "low|medium|high|critical"
  },
  "rollback_plan": {
    "steps": ["<step1>", "<step2>"],
    "automated": true|false,
    "estimated_time_seconds": <number>
  },
  "priority": "normal|high|urgent",
  "submitted_at": "<ISO_timestamp>",
  "timeout_at": "<ISO_timestamp>",
  "status": "pending|approved|rejected|revision_needed|timeout|executing|completed|failed|rolled_back"
}
```

**Required fields** (request rejected if missing):
- `request_id` (unique identifier)
- `type` (valid approval type code)
- `requester` (requesting agent session name)
- `operation` (complete operation details)
- `justification` (why operation is needed)
- `impact` (scope, affected resources, risk level)
- `rollback_plan` (MANDATORY - cannot be empty)
- `priority` (normal/high/urgent)
- `submitted_at` (ISO timestamp)
- `timeout_at` (ISO timestamp)
- `status` (initial: "pending")

### 1.2 Generating unique request IDs

Request IDs follow the format: `AR-<unix_timestamp>-<random_hex>`

```bash
# Generate unique request ID
request_id="AR-$(date +%s)-$(openssl rand -hex 3)"

# Example output: AR-1706795200-f3a2b1
```

### 1.3 Calculating timeout timestamps

Default timeout for all approval types: **120 seconds** from submission.

```bash
# macOS
timeout_at=$(date -u -v+120S +"%Y-%m-%dT%H:%M:%SZ")

# Linux
timeout_at=$(date -u -d "+120 seconds" +"%Y-%m-%dT%H:%M:%SZ")
```

### 1.4 Checking autonomous mode before requesting

Before submitting an approval request, check if autonomous mode allows direct execution:

```bash
autonomous_file="$CLAUDE_PROJECT_DIR/thoughts/shared/autonomous-mode.json"

if [[ -f "$autonomous_file" ]]; then
  enabled=$(jq -r '.enabled' "$autonomous_file")
  operation_type="agent_spawn"  # Replace with actual type
  allowed=$(jq -r ".permissions.${operation_type}.allowed" "$autonomous_file")
  max=$(jq -r ".permissions.${operation_type}.max_per_hour" "$autonomous_file")
  current=$(jq -r ".permissions.${operation_type}.current_hour_count" "$autonomous_file")

  if [[ "$enabled" == "true" && "$allowed" == "true" && "$current" -lt "$max" ]]; then
    # Execute autonomously, increment counter, log to audit trail
    echo "Autonomous execution allowed"
  else
    # Submit approval request
    echo "Approval required"
  fi
fi
```

### 1.5 Validating request completeness

Before submission, validate:

1. **All required fields present** - check each field exists
2. **Rollback plan not empty** - `rollback_plan.steps` array has at least 1 step
3. **Valid approval type** - type matches one of the defined approval types
4. **Valid priority** - one of: normal, high, urgent
5. **Valid risk level** - one of: low, medium, high, critical
6. **Valid scope** - one of: local, project, global

**If validation fails**: Return error to requester immediately, do NOT submit to manager.

---

## 2. Understanding approval types and their policies

### 2.1 Complete list of approval types

| Type | Code | Description |
|------|------|-------------|
| Agent Spawn | `agent_spawn` | Creating new Claude Code agent instances |
| Agent Terminate | `agent_terminate` | Terminating existing agents |
| Agent Replace | `agent_replace` | Replacing failed agents with new ones |
| Plugin Install | `plugin_install` | Installing plugins or skills on agents |
| Critical Operation | `critical_operation` | Any operation marked as critical (custom) |

### 2.2 Default timeouts by type

**All approval types have the same default timeout: 120 seconds**

This timeout is consistent to simplify timeout handling logic.

### 2.3 Auto-reject vs escalate policies

| Type | Timeout Action | Description |
|------|----------------|-------------|
| `agent_spawn` | Auto-reject | No escalation, immediate rejection at 120s |
| `agent_terminate` | Auto-reject | No escalation, immediate rejection at 120s |
| `agent_replace` | Auto-reject | No escalation, immediate rejection at 120s |
| `plugin_install` | Auto-reject | No escalation, immediate rejection at 120s |
| `critical_operation` | Escalate | Priority elevated to URGENT, timeout extended +60s, then auto-reject |

**Critical Operations Escalation**: The only type that gets special treatment at timeout.

---

## 3. Tracking approval request status lifecycle

### 3.1 Status definitions and transitions

```
pending --> approved --> executing --> completed
   |            |           |
   |            |           +--> failed --> rolled_back
   |            |
   |            +--> revision_needed --> pending
   |
   +--> rejected
   |
   +--> timeout (auto-reject or escalate)
```

| Status | Description |
|--------|-------------|
| `pending` | Awaiting manager decision (initial state) |
| `approved` | Manager approved, ready for execution |
| `rejected` | Manager rejected with reason (terminal state) |
| `revision_needed` | Manager requested changes, returns to pending after revision |
| `timeout` | Request timed out without decision (terminal state) |
| `executing` | Operation currently being executed |
| `completed` | Operation completed successfully (terminal state) |
| `failed` | Operation failed during execution |
| `rolled_back` | Rollback executed after failure (terminal state) |

**Terminal states**: rejected, timeout, completed, rolled_back (no further transitions)

### 3.2 Pending approvals file structure

**Location**: `$CLAUDE_PROJECT_DIR/thoughts/shared/pending-approvals.json`

```json
{
  "pending": [
    {
      "request_id": "AR-1706795200-abc123",
      "type": "agent_spawn",
      "requester": "ecos-lifecycle-manager",
      "submitted_at": "2026-02-01T12:00:00Z",
      "timeout_at": "2026-02-01T12:02:00Z",
      "last_reminder_at": null,
      "reminder_count": 0
    }
  ],
  "history": []
}
```

**Fields**:
- `pending`: Array of currently pending approval requests (awaiting decision)
- `history`: Array of completed requests (moved here after decision or timeout)

### 3.3 Moving requests from pending to history

When a request receives a decision or times out:

1. **Remove from `pending` array**
2. **Add to `history` array** with final status
3. **Update file atomically** (write temp file, then rename)

```bash
# Example: Move request to history
jq --arg rid "AR-1706795200-abc123" \
   --arg status "approved" \
   '.history += [(.pending[] | select(.request_id == $rid) | . + {status: $status})] | .pending |= map(select(.request_id != $rid))' \
   pending-approvals.json > pending-approvals.json.tmp && \
   mv pending-approvals.json.tmp pending-approvals.json
```

---

## 4. Forwarding requests to manager via EAMA

### 4.1 AI Maestro message format for approval requests

Send approval requests to EAMA using AI Maestro messaging:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'${SESSION_NAME}'",
    "to": "eama-main",
    "subject": "APPROVAL REQUIRED: <operation_type>",
    "priority": "<normal|high|urgent>",
    "content": {
      "type": "approval_request",
      "message": "<formatted_request_summary>",
      "request_id": "<request_id>",
      "timeout_seconds": 120
    }
  }'
```

**Required fields**:
- `from`: Your session name (ecos-approval-coordinator)
- `to`: "eama-main" (EAMA's session name)
- `subject`: "APPROVAL REQUIRED: <type>"
- `priority`: normal/high/urgent (matches request priority)
- `content.type`: "approval_request" (message type)
- `content.message`: Human-readable summary
- `content.request_id`: Unique request ID for tracking
- `content.timeout_seconds`: 120 (standard timeout)

### 4.2 Setting priority levels

| Priority | When to Use |
|----------|-------------|
| `normal` | Standard operations, low/medium risk |
| `high` | Operations affecting multiple agents or resources |
| `urgent` | Critical operations or escalated timeout requests |

### 4.3 Formatting human-readable request summaries

Manager sees the `content.message` field. Format it clearly:

```
Request to spawn agent worker-dev-auth-001 for auth module development.

Requester: ecos-lifecycle-manager
Risk: low
Scope: local
Affected agents: none
Rollback: Terminate agent, remove from registry

Justification: Team needs additional developer for auth module tasks.
```

**Structure**:
1. **One-line summary** of the operation
2. **Key details**: Requester, risk, scope, affected resources
3. **Rollback plan summary**
4. **Justification** (why this operation is needed)

---

## 5. Handling escalation timeline and reminders

### 5.1 Escalation timeline stages (0s, 30s, 60s, 90s, 120s)

All approval requests follow this escalation timeline:

| Time Elapsed | Action |
|--------------|--------|
| 0s | Submit request to manager via EAMA |
| 30s | Send first reminder if no response |
| 60s | Send second reminder (elevated urgency) |
| 90s | Send final warning |
| 120s | Timeout - execute timeout policy |

### 5.2 Sending reminder messages at intervals

Reminder message format:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'${SESSION_NAME}'",
    "to": "eama-main",
    "subject": "REMINDER: Approval pending - <request_id>",
    "priority": "high",
    "content": {
      "type": "approval_reminder",
      "message": "<reminder_message>",
      "request_id": "<request_id>",
      "elapsed_seconds": <elapsed>,
      "remaining_seconds": <remaining>
    }
  }'
```

**Reminder content examples**:

- **30s reminder**: "Approval request AR-xxx pending for 30 seconds. 90 seconds remaining."
- **60s reminder**: "ELEVATED: Approval request AR-xxx pending for 60 seconds. 60 seconds remaining."
- **90s reminder**: "FINAL WARNING: Approval request AR-xxx pending for 90 seconds. 30 seconds remaining. Auto-reject in 30s."

### 5.3 Tracking reminder count and elapsed time

Update `pending-approvals.json` after each reminder:

```json
{
  "request_id": "AR-1706795200-abc123",
  "last_reminder_at": "2026-02-01T12:00:30Z",
  "reminder_count": 1
}
```

**Fields to update**:
- `last_reminder_at`: ISO timestamp of last reminder sent
- `reminder_count`: Increment by 1 each time

---

## 6. Processing timeout conditions

### 6.1 Timeout policy decision tree by type

At 120 seconds elapsed:

```
Is type "critical_operation"?
  ├─ YES → Escalate (see 6.3)
  └─ NO → Auto-reject (see 6.2)
```

### 6.2 Auto-rejecting non-critical requests

For types: `agent_spawn`, `agent_terminate`, `agent_replace`, `plugin_install`

**Procedure**:
1. Update status to "timeout" in pending-approvals.json
2. Move request to history
3. Log timeout to audit trail
4. Notify requester via AI Maestro:
   ```
   Request AR-xxx TIMED OUT - auto-rejected.
   Reason: No manager response within 120 seconds.
   Resubmit if still needed.
   ```

### 6.3 Escalating critical operations with extended timeout

For type: `critical_operation`

**Procedure**:
1. Elevate priority to URGENT
2. Extend timeout by 60 seconds
3. Send escalation message to EAMA:
   ```bash
   curl -X POST "http://localhost:23000/api/messages" \
     -H "Content-Type: application/json" \
     -d '{
       "from": "'${SESSION_NAME}'",
       "to": "eama-main",
       "subject": "URGENT ESCALATION: critical_operation timeout",
       "priority": "urgent",
       "content": {
         "type": "approval_escalation",
         "message": "CRITICAL: Approval request AR-xxx has TIMED OUT.\n\nOriginal request: <operation>\nRequester: <agent>\nRisk: CRITICAL\n\nThis request requires immediate attention. Extended timeout: 60 seconds.\n\nApprove or Reject IMMEDIATELY.",
         "request_id": "<request_id>",
         "timeout_seconds": 60
       }
     }'
   ```
4. Log escalation to audit trail
5. Wait additional 60 seconds
6. If still no response → proceed to 6.4

### 6.4 Final auto-reject after extended timeout expires

If critical operation receives no response after extended timeout:

1. Update status to "timeout"
2. Move to history
3. Log final auto-reject
4. Notify requester:
   ```
   CRITICAL request AR-xxx TIMED OUT - auto-rejected.
   Extended timeout expired (180s total).
   Operation NOT executed.
   ```

---

## 7. Receiving and processing approval decisions

### 7.1 Decision message format from EAMA

Check for approval decision messages:

```bash
curl -s "http://localhost:23000/api/messages?agent=${SESSION_NAME}&action=list&status=unread" | \
  jq '.messages[] | select(.content.type == "approval_decision")'
```

Expected decision format:

```json
{
  "type": "approval_decision",
  "request_id": "AR-1706795200-abc123",
  "decision": "approved|rejected|revision_needed",
  "reason": "<decision_reason>",
  "feedback": "<optional_feedback_for_revision>",
  "decided_by": "manager",
  "decided_at": "2026-02-01T12:01:30Z"
}
```

### 7.2 Validating decision matches pending request

Before processing decision:

1. **Check request_id exists in pending list**
2. **Verify decision is valid value** (approved/rejected/revision_needed)
3. **Confirm decided_by is "manager"**

If validation fails: Log error, notify EAMA of invalid decision message.

### 7.3 Decision types: approved, rejected, revision_needed

| Decision | Action |
|----------|--------|
| `approved` | Proceed to execution (see section 8) |
| `rejected` | Cancel operation, notify requester with reason, move to history |
| `revision_needed` | Return to requester with feedback, keep status as pending |

**Rejected**: Terminal state, operation will NOT be executed.

**Revision needed**: Requester can modify request and resubmit (with same or new request_id).

### 7.4 Updating status and logging decision

For approved decision:
```bash
# Update status to "approved"
jq --arg rid "AR-xxx" '.pending |= map(if .request_id == $rid then . + {status: "approved"} else . end)' pending-approvals.json

# Log to audit trail
echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] [AR-xxx] [DECIDE] decision=approved by=manager reason=\"Team needs additional developer\"" >> approval-audit.log
```

---

## 8. Executing approved operations

### 8.1 Transitioning status to executing

After approval received:

```bash
# Update status to "executing"
jq --arg rid "AR-xxx" '.pending |= map(if .request_id == $rid then . + {status: "executing"} else . end)' pending-approvals.json
```

### 8.2 Delegating execution to appropriate ECOS agent

Based on operation type, delegate to the right agent:

| Operation Type | Delegate To |
|----------------|-------------|
| `agent_spawn` | ecos-lifecycle-manager |
| `agent_terminate` | ecos-lifecycle-manager |
| `agent_replace` | ecos-lifecycle-manager |
| `plugin_install` | ecos-lifecycle-manager |
| `critical_operation` | Agent specified in request |

Send execution command via AI Maestro message.

### 8.3 Monitoring execution progress

Poll for execution completion message from delegated agent:

```bash
# Check for completion message
curl -s "http://localhost:23000/api/messages?agent=${SESSION_NAME}&action=list&status=unread" | \
  jq '.messages[] | select(.content.type == "execution_result" and .content.request_id == "AR-xxx")'
```

Expected result format:

```json
{
  "type": "execution_result",
  "request_id": "AR-xxx",
  "result": "success|failure",
  "error": "<error_message_if_failed>",
  "duration_ms": 6000
}
```

### 8.4 Handling execution success

On success:

1. Update status to "completed"
2. Move to history
3. Log completion to audit trail:
   ```
   [2026-02-01T12:00:52Z] [AR-xxx] [EXEC_DONE] result=success duration=6000ms
   ```
4. Notify requester:
   ```
   Request AR-xxx APPROVED and EXECUTED successfully.
   Operation completed in 6000ms.
   ```

### 8.5 Handling execution failure

On failure:

1. Update status to "failed"
2. Log failure to audit trail:
   ```
   [2026-02-01T13:00:10Z] [AR-xxx] [EXEC_DONE] result=failure duration=2000ms error="Directory already exists"
   ```
3. Initiate rollback (see section 9)

---

## 9. Executing rollback procedures after failures

### 9.1 Initiating rollback from request rollback_plan

When approved operation fails, retrieve rollback_plan from original request:

```json
{
  "rollback_plan": {
    "steps": [
      "Remove partial agent registration from AI Maestro",
      "Clean up any created tmux session",
      "Update registry to remove agent entry"
    ],
    "automated": true,
    "estimated_time_seconds": 10
  }
}
```

### 9.2 Automated vs manual rollback steps

**If `automated: true`**:
- Execute rollback steps programmatically
- Log each step execution

**If `automated: false`**:
- Notify requester with rollback steps
- Request manual execution
- Wait for confirmation

### 9.3 Logging rollback progress

Log rollback initiation:
```
[2026-02-01T13:00:11Z] [AR-xxx] [ROLLBACK_START] reason="Execution failed: Directory already exists"
```

Log each rollback step:
```
[2026-02-01T13:00:12Z] [AR-xxx] [ROLLBACK_STEP] step=1 action="Remove AI Maestro registration" result=success
[2026-02-01T13:00:13Z] [AR-xxx] [ROLLBACK_STEP] step=2 action="Clean up tmux session" result=success
```

Log rollback completion:
```
[2026-02-01T13:00:14Z] [AR-xxx] [ROLLBACK_DONE] result=success
```

### 9.4 Escalating rollback failures immediately

**If rollback fails**:

1. Update status to "failed" with `rollback_failed: true` flag
2. Log rollback failure:
   ```
   [2026-02-01T13:00:15Z] [AR-xxx] [ROLLBACK_DONE] result=failure error="Cannot remove tmux session: permission denied"
   ```
3. **ESCALATE IMMEDIATELY** to manager via EAMA with URGENT priority:
   ```
   CRITICAL: Rollback FAILED for request AR-xxx

   Operation: <operation>
   Execution error: <execution_error>
   Rollback error: <rollback_error>

   MANUAL INTERVENTION REQUIRED
   ```

---

## 10. Using autonomous mode for pre-approved operations

### 10.1 Autonomous mode configuration structure

**Location**: `$CLAUDE_PROJECT_DIR/thoughts/shared/autonomous-mode.json`

```json
{
  "enabled": true,
  "granted_at": "2026-02-01T10:00:00Z",
  "granted_by": "manager",
  "expires_at": null,
  "permissions": {
    "agent_spawn": {
      "allowed": true,
      "max_per_hour": 10,
      "current_hour_count": 2
    },
    "agent_terminate": {
      "allowed": true,
      "max_per_hour": 5,
      "current_hour_count": 0
    },
    "agent_replace": {
      "allowed": true,
      "max_per_hour": 5,
      "current_hour_count": 1
    },
    "plugin_install": {
      "allowed": false
    },
    "critical_operation": {
      "allowed": false
    }
  }
}
```

### 10.2 Per-operation permission rules

Each operation type has independent permission settings:

| Field | Type | Description |
|-------|------|-------------|
| `allowed` | boolean | Whether autonomous execution is permitted |
| `max_per_hour` | integer | Maximum operations allowed per hour (optional) |
| `current_hour_count` | integer | Current count for this hour (resets hourly) |

**If `allowed: false`**: Approval request REQUIRED, even if autonomous mode is enabled globally.

### 10.3 Rate limiting (max per hour counters)

**Hourly reset**: Counters reset at the top of each hour (XX:00:00).

**Enforcement logic**:
```bash
if [[ "$current_hour_count" -ge "$max_per_hour" ]]; then
  # Rate limit exceeded, require approval
fi
```

### 10.4 Checking and incrementing counters

Before autonomous execution:

```bash
autonomous_file="$CLAUDE_PROJECT_DIR/thoughts/shared/autonomous-mode.json"
operation_type="agent_spawn"

# Check if allowed and under limit
enabled=$(jq -r '.enabled' "$autonomous_file")
allowed=$(jq -r ".permissions.${operation_type}.allowed" "$autonomous_file")
max=$(jq -r ".permissions.${operation_type}.max_per_hour" "$autonomous_file")
current=$(jq -r ".permissions.${operation_type}.current_hour_count" "$autonomous_file")

if [[ "$enabled" == "true" && "$allowed" == "true" && "$current" -lt "$max" ]]; then
  # Execute autonomously

  # Increment counter
  jq ".permissions.${operation_type}.current_hour_count += 1" "$autonomous_file" > tmp && mv tmp "$autonomous_file"

  # Log autonomous execution
  echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] [AUTONOMOUS] type=${operation_type} count=$((current+1))/${max}" >> approval-audit.log
else
  # Request approval
fi
```

### 10.5 Autonomous mode grant and revocation

**Granting autonomous mode**:

Manager sends message via EAMA:
```json
{
  "type": "autonomous_mode_grant",
  "permissions": {
    "agent_spawn": {"allowed": true, "max_per_hour": 10},
    "agent_terminate": {"allowed": true, "max_per_hour": 5}
  }
}
```

**Revoking autonomous mode**:

Manager sends message via EAMA:
```json
{
  "type": "autonomous_mode_revoke"
}
```

Set `enabled: false` and log revocation:
```
[2026-02-01T15:00:00Z] [AUTONOMOUS_MODE] [REVOKED] by=manager
```

---

## 11. Maintaining audit trail logs

### 11.1 Log entry format and event types

**Location**: `$CLAUDE_PROJECT_DIR/thoughts/shared/approval-audit.log`

**Format**: `[<ISO_timestamp>] [<request_id>] [<event_type>] <details>`

| Event | Format |
|-------|--------|
| Request submitted | `[SUBMIT] type=<type> requester=<agent> operation=<op>` |
| Reminder sent | `[REMIND] count=<n> elapsed=<s>s remaining=<s>s` |
| Decision received | `[DECIDE] decision=<dec> by=<who> reason=<reason>` |
| Execution started | `[EXEC_START] operation=<op>` |
| Execution completed | `[EXEC_DONE] result=<success|failure> duration=<ms>ms` |
| Rollback initiated | `[ROLLBACK_START] reason=<reason>` |
| Rollback completed | `[ROLLBACK_DONE] result=<success|failure>` |
| Timeout | `[TIMEOUT] action=<auto_reject|escalate>` |
| Autonomous execution | `[AUTONOMOUS] type=<type> operation=<op> count=<n>/<max>` |

### 11.2 Recording submissions, decisions, executions, rollbacks

**Example complete audit trail for a successful approval**:

```
[2026-02-01T12:00:00Z] [AR-1706795200-abc123] [SUBMIT] type=agent_spawn requester=ecos-lifecycle-manager operation="Create worker-dev-001"
[2026-02-01T12:00:30Z] [AR-1706795200-abc123] [REMIND] count=1 elapsed=30s remaining=90s
[2026-02-01T12:00:45Z] [AR-1706795200-abc123] [DECIDE] decision=approved by=manager reason="Team needs additional developer"
[2026-02-01T12:00:46Z] [AR-1706795200-abc123] [EXEC_START] operation="Create worker-dev-001"
[2026-02-01T12:00:52Z] [AR-1706795200-abc123] [EXEC_DONE] result=success duration=6000ms
```

**Example with rollback**:

```
[2026-02-01T13:00:00Z] [AR-1706795200-xyz789] [SUBMIT] type=agent_spawn requester=ecos-lifecycle-manager operation="Create worker-dev-002"
[2026-02-01T13:00:08Z] [AR-1706795200-xyz789] [DECIDE] decision=approved by=manager reason="Additional developer"
[2026-02-01T13:00:09Z] [AR-1706795200-xyz789] [EXEC_START] operation="Create worker-dev-002"
[2026-02-01T13:00:10Z] [AR-1706795200-xyz789] [EXEC_DONE] result=failure duration=2000ms error="Directory already exists"
[2026-02-01T13:00:11Z] [AR-1706795200-xyz789] [ROLLBACK_START] reason="Execution failed: Directory already exists"
[2026-02-01T13:00:12Z] [AR-1706795200-xyz789] [ROLLBACK_DONE] result=success
```

### 11.3 Audit trail file location and structure

**Location**: `$CLAUDE_PROJECT_DIR/thoughts/shared/approval-audit.log`

**Format**: Append-only log file (do NOT overwrite, always append)

**Rotation**: Consider rotating logs daily or weekly if file grows large (>10MB).

---

## 12. Handling error conditions

### 12.1 Invalid request format errors

**Detection**: Missing required fields or invalid values

**Action**:
1. Do NOT submit to manager
2. Return error to requester:
   ```
   ERROR: Invalid approval request
   Missing fields: [rollback_plan]
   Fix and resubmit.
   ```
3. Log error (optional):
   ```
   [2026-02-01T12:00:00Z] [ERROR] Invalid request from ecos-lifecycle-manager: missing rollback_plan
   ```

### 12.2 Missing rollback plan errors

**CRITICAL**: Rollback plan is MANDATORY for ALL approval requests.

**Detection**: `rollback_plan` field missing or `rollback_plan.steps` array empty

**Action**:
1. Reject request immediately
2. Return error:
   ```
   ERROR: Rollback plan is REQUIRED for all approval requests.
   Provide rollback_plan with at least 1 step.
   ```
3. Do NOT submit to manager

### 12.3 EAMA unreachable retry logic

**Detection**: AI Maestro API returns connection error or timeout when sending message

**Retry logic**:
1. Retry 3 times with 5-second delay between attempts
2. If all retries fail:
   - Queue message for later retry
   - Log error:
     ```
     [2026-02-01T12:00:00Z] [AR-xxx] [ERROR] EAMA unreachable after 3 retries, queued for retry
     ```
   - Notify requester of delay

### 12.4 Duplicate request ID handling

**Detection**: Request ID already exists in pending or history

**Action**:
1. Reject duplicate
2. Generate new request ID:
   ```bash
   new_request_id="AR-$(date +%s)-$(openssl rand -hex 3)"
   ```
3. Return to requester:
   ```
   ERROR: Duplicate request ID AR-xxx
   Regenerated as AR-yyy, resubmit with new ID
   ```

---

## Summary

This approval workflow engine provides:

✅ **Complete request lifecycle** - From submission to execution to rollback
✅ **Escalation timeline** - 0s → 30s → 60s → 90s → 120s with reminders
✅ **Timeout policies** - Auto-reject for standard ops, escalate for critical ops
✅ **Autonomous mode** - Pre-approved operations with rate limiting
✅ **Rollback procedures** - Automated rollback on execution failure
✅ **Audit trail** - Complete log of all approval activities
✅ **Error handling** - Validation, retry logic, duplicate detection

All ECOS agents requesting approvals MUST follow these procedures exactly.
