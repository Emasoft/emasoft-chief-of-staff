# Permission Management Examples

## Table of Contents (Use-Case Oriented)

- 1. Requesting Approval to Spawn an Agent - When you need to create a new agent
- 2. Requesting Approval to Terminate an Agent - When you need to stop an agent
- 3. Handling Approval Timeout - When EAMA does not respond in time
- 4. Operating in Autonomous Mode - When operating under autonomous directive

---

## 1. Requesting Approval to Spawn an Agent

**Use this example when:** You need to create a new agent instance and must request approval from EAMA.

### Request Message

Use the `agent-messaging` skill to send:
- **Recipient**: `eama-assistant-manager`
- **Subject**: `[APPROVAL REQUEST] Spawn Agent: code-impl-auth`
- **Priority**: `high`
- **Content**: type `approval_request`, message: "Requesting approval to spawn new agent". Include `request_id`: "spawn-req-2025-02-02-001", `operation`: "spawn", `details`: { `agent_name`: "code-impl-auth", `agent_role`: "code-implementer", `task`: "Implement user authentication module", `working_directory`: "{baseDir}/auth", `expected_duration`: "2 hours", `resource_requirements`: "standard" }, `justification`: "New authentication module required per design doc EAA-AUTH-001".

### Expected Response (Approval)

EAMA replies with type `approval_response`, `request_id`: "spawn-req-2025-02-02-001", `decision`: "approved", `decided_at`: timestamp, `notes`: "Approved. Proceed with spawn."

### Key Points

- Use `priority: "high"` for spawn requests as they typically block work
- Include all required `details` fields
- Reference relevant design documents in `justification`
- Use consistent `request_id` format for tracking

---

## 2. Requesting Approval to Terminate an Agent

**Use this example when:** An agent has completed its work and you need approval to terminate it.

### Request Message

Use the `agent-messaging` skill to send:
- **Recipient**: `eama-assistant-manager`
- **Subject**: `[APPROVAL REQUEST] Terminate Agent: data-processor-03`
- **Priority**: `normal`
- **Content**: type `approval_request`, message: "Requesting approval to terminate agent". Include `request_id`: "term-req-2025-02-02-002", `operation`: "terminate", `details`: { `agent_name`: "data-processor-03", `current_status`: "idle", `reason`: "task_complete", `final_report`: "Processed 1500 records. All tasks complete.", `pending_work`: "none" }, `justification`: "Agent has completed all assigned data processing tasks".

### Expected Response (Rejection with Alternative)

EAMA replies with type `approval_response`, `request_id`: "term-req-2025-02-02-002", `decision`: "rejected", `notes`: "Hibernate instead. We may need this agent for batch 2."

### Key Points

- Use `priority: "normal"` for terminate requests as they are less urgent
- Include `final_report` summarizing agent work
- Be prepared for EAMA to suggest alternatives (hibernate instead of terminate)
- Follow EAMA's guidance in the response

---

## 3. Handling Approval Timeout

**Use this example when:** EAMA does not respond to your approval request within the timeout period.

### Timeline

| Time | Event | Action |
|------|-------|--------|
| T+0 | Initial request sent | Wait for response |
| T+60s | First timeout | Send reminder |
| T+90s | Second timeout | Send urgent notification |
| T+120s | Final timeout | Proceed or abort |

### Reminder Notification (T+60 seconds)

Use the `agent-messaging` skill to send:
- **Recipient**: `eama-assistant-manager`
- **Subject**: `[REMINDER] Pending Approval: Spawn code-impl-auth`
- **Priority**: `high`
- **Content**: type `approval_reminder`, message: "Reminder: approval request pending for 60 seconds". Include `request_id`: "spawn-req-2025-02-02-001", `original_request_time`: "2025-02-02T10:00:00Z", `timeout_in_seconds`: 60.

### Urgent Notification (T+90 seconds)

Use the `agent-messaging` skill to send:
- **Recipient**: `eama-assistant-manager`
- **Subject**: `[URGENT] Approval Required: Spawn code-impl-auth - Will proceed in 30s`
- **Priority**: `urgent`
- **Content**: type `approval_urgent`, message: "URGENT: Will proceed without approval in 30 seconds". Include `request_id`: "spawn-req-2025-02-02-001", `original_request_time`: "2025-02-02T10:00:00Z", `timeout_in_seconds`: 30, `action_on_timeout`: "proceed".

### Audit Trail Entry (T+120 seconds - No Response)

```json
{
  "timestamp": "2025-02-02T10:02:00Z",
  "operation": "spawn",
  "target": "code-impl-auth",
  "request_id": "spawn-req-2025-02-02-001",
  "decision": "timeout_proceed",
  "decided_by": "timeout",
  "escalation_count": 3,
  "notes": "Proceeded after 3 notification attempts with no response"
}
```

### Key Points

- Always send reminder at 60 seconds
- Always send urgent at 90 seconds
- Include `action_on_timeout` in urgent message
- Log `escalation_count` in audit trail
- Use `timeout_proceed` or `timeout_abort` as decision value

---

## 4. Operating in Autonomous Mode

**Use this example when:** The user has granted an autonomous directive and you can proceed without pre-approval.

### Prerequisite

ECOS must have received an autonomous directive from EAMA:

```
"Operate autonomously for agent management until 18:00"
```

### Post-Operation Notification

After executing under autonomous directive, use the `agent-messaging` skill to send:
- **Recipient**: `eama-assistant-manager`
- **Subject**: `[AUTONOMOUS] Agent Spawned: test-runner-04`
- **Priority**: `normal`
- **Content**: type `autonomous_notification`, message: "Agent spawned under autonomous directive". Include `operation`: "spawn", `details`: { `agent_name`: "test-runner-04", `agent_role`: "test-engineer", `task`: "Run integration tests for auth module" }, `directive_reference`: "autonomous-directive-2025-02-02-001", `completed_at`: "2025-02-02T14:30:00Z".

### Audit Trail Entry

```json
{
  "timestamp": "2025-02-02T14:30:00Z",
  "operation": "spawn",
  "target": "test-runner-04",
  "decision": "autonomous",
  "decided_by": "autonomous",
  "directive_reference": "autonomous-directive-2025-02-02-001"
}
```

### Key Points

- Use `type: "autonomous_notification"` (not `approval_request`)
- Include `directive_reference` to link to the authorizing directive
- Still send notification even though no approval was required
- Use `decided_by: "autonomous"` in audit trail
- Always log with `decision: "autonomous"`

---

**Version:** 1.0
**Last Updated:** 2025-02-03
