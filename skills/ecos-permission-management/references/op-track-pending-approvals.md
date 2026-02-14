---
name: op-track-pending-approvals
description: Operation procedure for tracking multiple pending approval requests.
workflow-instruction: "support"
procedure: "support-skill"
---

# Operation: Track Pending Approvals


## Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Initialize Tracking File](#step-1-initialize-tracking-file)
  - [Step 2: Register New Request](#step-2-register-new-request)
  - [Step 3: Check Pending Requests Status](#step-3-check-pending-requests-status)
  - [Step 4: Poll for Responses](#step-4-poll-for-responses)
  - [Step 5: Check for Timeouts](#step-5-check-for-timeouts)
  - [Step 6: Update Tracking on Resolution](#step-6-update-tracking-on-resolution)
  - [Step 7: Generate Status Report](#step-7-generate-status-report)
- [Example](#example)
- [Tracking State Schema](#tracking-state-schema)
- [Error Handling](#error-handling)
- [Notes](#notes)

## Purpose

Maintain tracking of all outstanding approval requests to manage multiple concurrent operations and ensure timely responses.

## When to Use

- When managing multiple approval requests simultaneously
- When checking status of pending operations
- When generating status reports
- When handling escalation timing

## Prerequisites

- Pending approvals tracking file at `docs_dev/pending-approvals.json`
- Request IDs from submitted approval requests
- AI Maestro for checking responses

## Procedure

### Step 1: Initialize Tracking File

```bash
PENDING_FILE="docs_dev/pending-approvals.json"
mkdir -p docs_dev

if [ ! -f "$PENDING_FILE" ]; then
  echo '{"pending": {}, "resolved": []}' > $PENDING_FILE
fi
```

### Step 2: Register New Request

When submitting a new approval request:

```bash
REQUEST_ID="$1"
OPERATION="$2"
TARGET="$3"

jq '.pending["'"$REQUEST_ID"'"] = {
  "operation": "'"$OPERATION"'",
  "target": "'"$TARGET"'",
  "requested_at": "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'",
  "status": "pending",
  "reminder_sent": false,
  "urgent_sent": false
}' $PENDING_FILE > temp.json && mv temp.json $PENDING_FILE
```

### Step 3: Check Pending Requests Status

```bash
# List all pending requests
jq '.pending | to_entries[] | {
  id: .key,
  operation: .value.operation,
  target: .value.target,
  requested_at: .value.requested_at,
  age_seconds: (now - (.value.requested_at | fromdateiso8601))
}' $PENDING_FILE
```

### Step 4: Poll for Responses

```bash
# Get all pending request IDs
PENDING_IDS=$(jq -r '.pending | keys[]' $PENDING_FILE)

for REQUEST_ID in $PENDING_IDS; do
  # Check AI Maestro inbox for response
  # Use the agent-messaging skill to check for unread messages matching the request ID
  RESPONSE=$(check_messages_for_request_id "$REQUEST_ID" "approval-response")

  if [ -n "$RESPONSE" ]; then
    DECISION=$(echo $RESPONSE | jq -r '.content.decision')
    echo "Response received for $REQUEST_ID: $DECISION"

    # Update tracking
    jq '.pending["'"$REQUEST_ID"'"].status = "'"$DECISION"'"' $PENDING_FILE > temp.json && mv temp.json $PENDING_FILE
  fi
done
```

### Step 5: Check for Timeouts

```bash
# Find requests older than 60 seconds without reminder
NEEDS_REMINDER=$(jq -r '.pending | to_entries[] | select(
  (now - (.value.requested_at | fromdateiso8601)) > 60 and
  .value.reminder_sent == false and
  .value.status == "pending"
) | .key' $PENDING_FILE)

# Find requests older than 90 seconds without urgent
NEEDS_URGENT=$(jq -r '.pending | to_entries[] | select(
  (now - (.value.requested_at | fromdateiso8601)) > 90 and
  .value.urgent_sent == false and
  .value.status == "pending"
) | .key' $PENDING_FILE)

echo "Needs reminder: $NEEDS_REMINDER"
echo "Needs urgent: $NEEDS_URGENT"
```

### Step 6: Update Tracking on Resolution

When approval is received:

```bash
REQUEST_ID="$1"
DECISION="$2"
DECIDED_BY="$3"

# Move from pending to resolved
RESOLVED_ENTRY=$(jq '.pending["'"$REQUEST_ID"'"] + {
  "decision": "'"$DECISION"'",
  "decided_at": "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'",
  "decided_by": "'"$DECIDED_BY"'"
}' $PENDING_FILE)

jq 'del(.pending["'"$REQUEST_ID"'"]) | .resolved += ['"$RESOLVED_ENTRY"']' $PENDING_FILE > temp.json && mv temp.json $PENDING_FILE
```

### Step 7: Generate Status Report

```bash
# Count pending by type
echo "=== Pending Approvals Status ==="
jq -r '.pending | group_by(.operation) | map({
  operation: .[0].operation,
  count: length,
  oldest_seconds: (now - ([.[].requested_at | fromdateiso8601] | min))
}) | .[]' $PENDING_FILE

# Recent resolutions
echo "=== Recent Resolutions ==="
jq -r '.resolved | sort_by(.decided_at) | reverse | .[0:5] | .[] | "\(.operation) \(.target): \(.decision)"' $PENDING_FILE
```

## Example

**Scenario:** Track multiple pending approvals for spawn, terminate, and plugin install.

```bash
# Initialize
PENDING_FILE="docs_dev/pending-approvals.json"

# Current state after multiple requests
cat $PENDING_FILE
# {
#   "pending": {
#     "abc-123": {
#       "operation": "spawn",
#       "target": "implementer-2",
#       "requested_at": "2025-02-05T10:00:00Z",
#       "status": "pending"
#     },
#     "def-456": {
#       "operation": "terminate",
#       "target": "test-runner-1",
#       "requested_at": "2025-02-05T10:01:00Z",
#       "status": "pending"
#     }
#   },
#   "resolved": []
# }

# Check for aged requests needing escalation
jq '.pending | to_entries[] | select(
  (now - (.value.requested_at | fromdateiso8601)) > 60
) | {id: .key, operation: .value.operation, age: (now - (.value.requested_at | fromdateiso8601))}' $PENDING_FILE
```

## Tracking State Schema

```json
{
  "pending": {
    "<request_id>": {
      "operation": "spawn|terminate|hibernate|wake|plugin_install",
      "target": "agent_name or plugin_name",
      "requested_at": "ISO-8601",
      "status": "pending|approved|rejected|modified|timeout",
      "reminder_sent": false,
      "urgent_sent": false
    }
  },
  "resolved": [
    {
      "operation": "spawn",
      "target": "implementer-1",
      "requested_at": "ISO-8601",
      "decision": "approved",
      "decided_at": "ISO-8601",
      "decided_by": "eama"
    }
  ]
}
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| File not found | First run or deleted | Initialize empty tracking file |
| JSON parse error | Corrupted file | Restore from backup or reinitialize |
| Request ID not found | Already resolved or never registered | Check resolved list |
| Concurrent updates | Multiple writers | Use file locking or atomic updates |

## Notes

- Keep resolved list bounded (e.g., last 100 entries)
- Archive old resolved entries to audit log
- Use request IDs consistently across all operations
- Clean up stale pending entries (>1 hour without resolution)
