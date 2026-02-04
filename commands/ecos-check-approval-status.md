---
name: ecos-check-approval-status
description: "Check status of pending approval requests from EAMA"
argument-hint: "[--request-id <ID>] [--all] [--status <STATUS>] [--since <HOURS>]"
allowed-tools: ["Bash(curl:*)", "Bash(aimaestro:*)", "Bash(jq:*)", "Read"]
user-invocable: true
---

# Check Approval Status Command

Check the status of pending, approved, or rejected approval requests from the Assistant Manager (EAMA).

## Usage

```bash
# Check specific request
curl -s "http://localhost:23000/api/messages?agent=$ECOS_SESSION_NAME&action=list" | \
  jq '.messages[] | select(.content.request_id == "'$REQUEST_ID'")'

# List all pending approvals
ls -la ~/.aimaestro/approvals/pending/

# Check for responses from EAMA
curl -s "http://localhost:23000/api/messages?agent=$ECOS_SESSION_NAME&action=list&status=unread" | \
  jq '.messages[] | select(.content.type == "approval_response")'
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--request-id <ID>` | No | Check specific request by ID |
| `--all` | No | Show all requests (pending, approved, rejected) |
| `--status <STATUS>` | No | Filter by status (pending, approved, rejected, deferred) |
| `--since <HOURS>` | No | Show requests from last N hours (default: 24) |
| `--format <FORMAT>` | No | Output format: table, json (default: table) |

## Request Status Values

| Status | Description |
|--------|-------------|
| `pending` | Awaiting manager decision |
| `approved` | Manager approved the operation |
| `rejected` | Manager denied the operation |
| `deferred` | Decision postponed, needs more info |
| `expired` | Request timed out without response |
| `completed` | Approved and operation executed |
| `cancelled` | Request was cancelled |

## Examples

```bash
# Check a specific request
/ecos-check-approval-status --request-id ECOS-20250202150000-a1b2c3d4

# List all pending approvals
/ecos-check-approval-status --status pending

# Show all requests from last 48 hours
/ecos-check-approval-status --all --since 48

# Get JSON output for scripting
/ecos-check-approval-status --all --format json
```

## Output Format (Table)

```
=======================================================================
  APPROVAL REQUEST STATUS
=======================================================================

  Request ID: ECOS-20250202150000-a1b2c3d4

  +------------------+--------------------------------------------+
  | Field            | Value                                      |
  +------------------+--------------------------------------------+
  | Operation        | terminate                                  |
  | Target Agent     | helper-python                              |
  | Status           | APPROVED                                   |
  | Requested        | 2025-02-02 15:00:00 UTC                   |
  | Response Time    | 2025-02-02 15:02:30 UTC                   |
  | Decision By      | EAMA (emasoft-assistant-manager-agent)    |
  +------------------+--------------------------------------------+

  Reason: Agent has critical bug and cannot recover

  Manager Notes: Proceed with termination. Ensure work is backed up.

  Conditions:
    1. Verify no pending commits
    2. Export agent state before termination

=======================================================================
```

## Output Format (All Pending)

```
=======================================================================
  PENDING APPROVAL REQUESTS
=======================================================================

  +-----+---------------------------+------------+---------------+----------+
  | #   | Request ID                | Operation  | Target Agent  | Priority |
  +-----+---------------------------+------------+---------------+----------+
  | 1   | ECOS-20250202150000-a1b2  | terminate  | helper-python | high     |
  | 2   | ECOS-20250202143000-c3d4  | spawn      | helper-tester | normal   |
  | 3   | ECOS-20250202120000-e5f6  | install    | helper-docs   | normal   |
  +-----+---------------------------+------------+---------------+----------+

  Total Pending: 3
  Oldest Request: 3 hours ago

=======================================================================
```

## Output Format (JSON)

```json
{
  "requests": [
    {
      "request_id": "ECOS-20250202150000-a1b2c3d4",
      "operation_type": "terminate",
      "agent_name": "helper-python",
      "status": "approved",
      "priority": "high",
      "reason": "Agent has critical bug and cannot recover",
      "requested_at": "2025-02-02T15:00:00Z",
      "responded_at": "2025-02-02T15:02:30Z",
      "decision": "approved",
      "conditions": ["Verify no pending commits", "Export agent state"],
      "notes": "Proceed with termination. Ensure work is backed up."
    }
  ],
  "summary": {
    "total": 5,
    "pending": 2,
    "approved": 2,
    "rejected": 1
  }
}
```

## Approval Storage Locations

| Status | Location |
|--------|----------|
| Pending | `~/.aimaestro/approvals/pending/` |
| Approved | `~/.aimaestro/approvals/approved/` |
| Rejected | `~/.aimaestro/approvals/rejected/` |
| Expired | `~/.aimaestro/approvals/expired/` |

## Checking via AI Maestro Messages

The command also checks AI Maestro messages for responses:

```bash
# Check for unread approval responses
curl -s "http://localhost:23000/api/messages?agent=emasoft-chief-of-staff&action=list&status=unread" | \
  jq '[.messages[] | select(.content.type == "approval_response")]'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Request not found" | Invalid ID | Verify request ID spelling |
| "No pending requests" | Queue empty | All requests have been processed |
| "AI Maestro not responding" | API down | Check if AI Maestro is running |
| "Cannot read approval files" | Permission issue | Check ~/.aimaestro/approvals/ permissions |

## Interpreting Status

### Approved
The operation can proceed. Check `conditions` field for any requirements before execution.

### Rejected
The operation was denied. Check `notes` field for reason. You may need to:
- Provide additional justification
- Wait for different circumstances
- Request alternative operation

### Deferred
Manager needs more information. Check `notes` for what is needed and submit a follow-up via `/ecos-notify-manager`.

### Expired
Request timed out without response. You can:
- Resubmit with `/ecos-request-approval`
- Check if EAMA is online
- Contact user for manual approval

## Related Commands

- `/ecos-request-approval` - Submit new approval request
- `/ecos-wait-for-approval` - Wait for approval response
- `/ecos-notify-manager` - Send notification to manager
