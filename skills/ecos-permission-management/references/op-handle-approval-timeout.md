---
name: op-handle-approval-timeout
description: Operation procedure for handling approval request timeouts and escalation.
workflow-instruction: "support"
procedure: "support-skill"
---

# Operation: Handle Approval Timeout


## Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Check Request Age](#step-1-check-request-age)
  - [Step 2: Send Reminder at 60 Seconds](#step-2-send-reminder-at-60-seconds)
  - [Step 3: Send Urgent Notification at 90 Seconds](#step-3-send-urgent-notification-at-90-seconds)
  - [Step 4: Handle Timeout at 120 Seconds](#step-4-handle-timeout-at-120-seconds)
- [Example](#example)
- [Escalation Timeline](#escalation-timeline)
- [Default Timeout Actions](#default-timeout-actions)
- [Autonomous Mode](#autonomous-mode)
- [Error Handling](#error-handling)
- [Notes](#notes)

## Purpose

Handle situations where approval requests do not receive timely responses, including sending reminders, escalating urgency, and making proceed/abort decisions.

## When to Use

- When approval request has been pending for >60 seconds
- When urgent escalation needed at >90 seconds
- When maximum timeout (120 seconds) reached
- When operating in autonomous mode

## Prerequisites

- Pending approval request with known request ID
- The `agent-messaging` skill is available
- Tracking file at `docs_dev/pending-approvals.json`
- Audit log at `docs_dev/audit/`

## Procedure

### Step 1: Check Request Age

Read the pending approvals tracking file (`docs_dev/pending-approvals.json`). Look up the request by its `REQUEST_ID`. Calculate the elapsed time since `requested_at` timestamp.

### Step 2: Send Reminder at 60 Seconds

If the request age is between 60 and 90 seconds, and no reminder has been sent yet:

Use the `agent-messaging` skill to send:
- **Recipient**: `eama-assistant-manager`
- **Subject**: `[REMINDER] Approval pending: [REQUEST_ID]`
- **Priority**: `high`
- **Content**: type `approval-reminder`, message: "Approval request pending for 60+ seconds. Please respond." Include `request_id`, `original_operation` (from the pending record), `target` (from the pending record).

Then update the tracking file to mark `reminder_sent` as true for this request.

### Step 3: Send Urgent Notification at 90 Seconds

If the request age is between 90 and 120 seconds, and no urgent notification has been sent yet:

Use the `agent-messaging` skill to send:
- **Recipient**: `eama-assistant-manager`
- **Subject**: `[URGENT] Approval timeout imminent: [REQUEST_ID]`
- **Priority**: `urgent`
- **Content**: type `approval-urgent`, message: "URGENT: Approval will timeout in 30 seconds. Respond immediately or operation will be aborted." Include `request_id`, `timeout_at` (the calculated timeout timestamp).

Then update the tracking file to mark `urgent_sent` as true for this request.

### Step 4: Handle Timeout at 120 Seconds

If the request age reaches 120 seconds or more:

**Determine default action based on operation type:**

| Operation | Default Action | Rationale |
|-----------|----------------|-----------|
| spawn | proceed | Creates resource, easily terminated if wrong |
| wake | proceed | Resumes existing resource |
| terminate | abort | Destructive, prefer manual approval |
| hibernate | abort | Affects running agent |
| plugin_install | abort | Could introduce security risks |

**Execute the timeout action:**

1. Update the tracking file status to `timeout_proceed` or `timeout_abort`
2. Write an audit log entry to `docs_dev/audit/ecos-approvals-[DATE].yaml` with: timestamp, operation, target, request_id, decision, decided_by: "timeout", escalation_count: 2
3. Use the `agent-messaging` skill to notify EAMA:
   - **Recipient**: `eama-assistant-manager`
   - **Subject**: `[TIMEOUT] Approval auto-[proceed/abort]: [REQUEST_ID]`
   - **Priority**: `high`
   - **Content**: type `approval-timeout`, message: "Approval request timed out after 120 seconds. Action: [proceed/abort]." Include `request_id`, `operation`, `target`, `action_taken`.
4. If action is "proceed", execute the operation. If action is "abort", clean up any partial state.

## Example

**Scenario:** Approval request for spawning `implementer-2` times out.

- Request ID: `abc-123`
- Operation: `spawn`
- Target: `implementer-2`
- Default action for spawn: `proceed`

At 60 seconds: Use the `agent-messaging` skill to send a reminder to `eama-assistant-manager` with subject "[REMINDER] Approval pending: abc-123", priority `high`.

At 90 seconds: Use the `agent-messaging` skill to send an urgent notice to `eama-assistant-manager` with subject "[URGENT] Approval timeout imminent: abc-123", priority `urgent`.

At 120 seconds: Log timeout to audit trail, then use the `agent-messaging` skill to send timeout notification to `eama-assistant-manager` with subject "[TIMEOUT] Approval auto-proceed: abc-123". Then proceed with spawning `implementer-2`.

## Escalation Timeline

| Time | Event | Action |
|------|-------|--------|
| 0s | Request submitted | Wait for response |
| 60s | Reminder threshold | Send reminder to EAMA |
| 90s | Urgent threshold | Send urgent notification |
| 120s | Timeout | Auto-proceed or auto-abort |

## Default Timeout Actions

| Operation | Default Action | Rationale |
|-----------|----------------|-----------|
| spawn | proceed | Creates resource, easily terminated if wrong |
| wake | proceed | Resumes existing resource |
| terminate | abort | Destructive, prefer manual approval |
| hibernate | abort | Affects running agent |
| plugin_install | abort | Could introduce security risks |

## Autonomous Mode

When operating under autonomous directive, skip the approval wait entirely. After executing the operation, use the `agent-messaging` skill to notify EAMA:
- **Recipient**: `eama-assistant-manager`
- **Subject**: `[AUTONOMOUS] Executed: [operation] [target]`
- **Priority**: `normal`
- **Content**: type `autonomous-notification`, message: "Operating in autonomous mode. [Operation] [target] for [reason]." Include `operation`, `target`, `executed_at` (ISO timestamp).

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Time calculation fails | Date format issues | Use consistent ISO-8601 format |
| Audit write fails | Permission or path | Ensure docs_dev/audit/ exists |
| Messaging unavailable | Service unavailable | Log locally, retry later |
| Multiple timeouts racing | Concurrent requests | Process sequentially |

## Notes

- Always log timeout decisions to audit trail
- Prefer abort for destructive operations
- Document autonomous mode usage
- Review timeout decisions in regular audits
