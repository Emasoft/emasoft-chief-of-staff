---
operation: acknowledgment-protocol
procedure: proc-notify-team-ready
workflow-instruction: Step 5 - Team Ready Notification
parent-skill: ecos-notification-protocols
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Acknowledgment Protocol

## When to Use

Trigger this operation when:
- Agent confirmation is required before proceeding
- Operations require agent readiness verification
- Coordinating multi-agent synchronized actions
- Disruptive operations need agent consent
- State-changing operations affect agent context

## Prerequisites

- AI Maestro messaging system is running
- The `agent-messaging` skill is available
- Target agent is active and reachable
- Timeout values are understood (see Standardized ACK Timeout Policy)
- Fallback behavior is defined for timeout scenarios

## Standardized ACK Timeout Policy

**CRITICAL:** Use these exact timeout values:

| ACK Type | Timeout | Reminders | Use Case |
|----------|---------|-----------|----------|
| Pre-operation ACK | **60 seconds** | 15s, 30s, 45s | Before disruptive operations |
| Approval request | **2 minutes** | 60s, 90s | Requesting manager approval |
| Emergency handoff ACK | **30 seconds** | 10s, 20s | Time-critical emergencies |
| Health check response | **30 seconds** | None | Verifying agent is alive |

## Procedure

### Step 1: Send Acknowledgment Request

Use the `agent-messaging` skill to send:
- **Recipient**: the target agent session name
- **Subject**: the request subject
- **Priority**: `high`
- **Content**: type `ack-request`, message: "[What needs acknowledgment]. Please reply with 'ok' when ready." Include `timeout_seconds`: 60, `requires_acknowledgment`: true.

### Step 2: Start Timeout Timer

Track elapsed time from request sent. Default timeout: 60 seconds. Reminder intervals: 15s, 30s, 45s.

### Step 3: Send Reminders

At each reminder interval, if no response, use the `agent-messaging` skill to send a reminder:
- **Recipient**: the target agent session name
- **Subject**: `Reminder: [Original Subject]`
- **Priority**: `high`
- **Content**: type `reminder`, message: "Reminder: Please reply 'ok' when ready. [X] seconds remaining." Include `original_subject`, `time_remaining`.

### Step 4: Process Response

Use the `agent-messaging` skill to check for unread messages from the target agent. Look for responses containing:
- `"ok"` - Agent is ready, proceed
- `"not ready"` - Agent needs more time, negotiate
- `"busy"` - Agent cannot respond now, may need escalation
- No response - Timeout behavior applies

### Step 5: Proceed or Handle Timeout

**If acknowledgment received:** Proceed with operation.

**If timeout occurs:**
1. Use the `agent-messaging` skill to send a final timeout notice:
   - **Recipient**: the target agent session name
   - **Subject**: `Proceeding Without Acknowledgment`
   - **Priority**: `high`
   - **Content**: type `timeout-notice`, message: "No response received within timeout. Proceeding with operation." Include `timeout_occurred`: true.
2. Log timeout event
3. Proceed with operation (for pre-operation ACK) or abort (for approval requests without autonomous mode)

## Checklist

Copy this checklist and track your progress:

- [ ] Sent acknowledgment request with clear instructions via `agent-messaging` skill
- [ ] Started timeout timer
- [ ] Sent reminder at 15 seconds (if no response)
- [ ] Sent reminder at 30 seconds (if no response)
- [ ] Sent reminder at 45 seconds (if no response)
- [ ] Processed response OR handled timeout at 60 seconds
- [ ] Logged acknowledgment outcome
- [ ] Proceeded with operation OR aborted based on policy

## Examples

### Example 1: Pre-Operation ACK Flow

**Scenario:** Getting acknowledgment before skill installation.

Use the `agent-messaging` skill to send:
- **Recipient**: `code-impl-auth`
- **Subject**: `Ready for Skill Installation?`
- **Priority**: `high`
- **Content**: type `ack-request`, message: "I am about to install the security-audit skill. This will hibernate and wake you. Please save your work and reply 'ok' when ready." Include `timeout_seconds`: 60, `requires_acknowledgment`: true.

Wait for response with reminders at 15s, 30s, 45s.

On "ok" response: Proceed with skill installation.

### Example 2: Approval Request ACK

**Scenario:** Requesting EAMA approval for expensive operation.

Use the `agent-messaging` skill to send (2 minute timeout):
- **Recipient**: `emasoft-assistant-manager-agent`
- **Subject**: `Approval Request: Full Project Rescan`
- **Priority**: `high`
- **Content**: type `approval-request`, message: "Requesting approval for full project skill rescan. Estimated time: 15 minutes. Estimated cost: significant token usage. Reply 'approved' to proceed or 'denied' with reason." Include `timeout_seconds`: 120, `operation`: "full-rescan", `requires_acknowledgment`: true.

### Example 3: Emergency Handoff ACK

**Scenario:** Emergency handoff with tight timeout.

Use the `agent-messaging` skill to send (30 second timeout):
- **Recipient**: `backup-coordinator`
- **Subject**: `URGENT: Emergency Handoff`
- **Priority**: `urgent`
- **Content**: type `emergency-ack`, message: "Chief of Staff is running out of context. Emergency handoff required. Reply 'ok' immediately to accept handoff." Include `timeout_seconds`: 30, `requires_acknowledgment`: true.

Send reminders at 10s and 20s. Proceed immediately after 30s regardless.

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| No response within timeout | Agent busy/offline/crashed | Proceed per timeout policy; log occurrence |
| Agent responds "not ready" | Work in progress | Ask when ready; reschedule if possible |
| Agent responds "busy" | Cannot handle request | Escalate to user or find alternative agent |
| Reminder delivery fails | Messaging issue | Use the `ai-maestro-agents-management` skill to check AI Maestro health; proceed with timeout |
| Agent acknowledges late | Response after timeout | Log late ACK; operation may already be in progress |
| Invalid response format | Agent misunderstood request | Clarify expectations; retry request |

## Related Operations

- [op-pre-operation-notification.md](op-pre-operation-notification.md) - Uses ACK protocol
- [op-post-operation-notification.md](op-post-operation-notification.md) - Verification is similar
- [op-failure-notification.md](op-failure-notification.md) - May follow timeout
- [acknowledgment-protocol.md](acknowledgment-protocol.md) - Complete reference documentation
