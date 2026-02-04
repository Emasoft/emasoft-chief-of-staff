# Approval Tracking Reference

## Contents

- 2.1 What is approval tracking - Understanding state management
- 2.2 Tracking data structure - Approval state format
- 2.3 Tracking procedure - Step-by-step tracking process
  - 2.3.1 Request registration - Recording new requests
  - 2.3.2 Status monitoring - Checking for responses
  - 2.3.3 Concurrent request handling - Managing multiple approvals
  - 2.3.4 Resolution recording - Updating on decision
- 2.4 State file format - Persistent tracking structure
- 2.5 Examples - Tracking scenarios
- 2.6 Troubleshooting - Tracking issues

---

## 2.1 What Is Approval Tracking

Approval tracking is the process of maintaining state for all pending, approved, rejected, and timed-out approval requests. ECOS must track every approval request from submission to resolution to ensure:

- No requests are lost or forgotten
- Responses are matched to the correct requests
- Escalation is triggered at appropriate times
- Complete audit trail is maintained
- Concurrent requests are handled correctly

**Tracking lifecycle:**

```
REQUEST SUBMITTED ──► PENDING ──► RESPONSE RECEIVED ──► RESOLVED
                        │                                  │
                        │                                  ▼
                        │                         APPROVED / REJECTED
                        │                         MODIFIED / DELAYED
                        │
                        ▼
                    ESCALATED (timeout)
                        │
                        ▼
                TIMEOUT_PROCEED / TIMEOUT_ABORT
```

---

## 2.2 Tracking Data Structure

Each approval request is tracked with the following data:

```yaml
request:
  # Identification
  request_id: "string - unique identifier"
  operation: "string - spawn|terminate|hibernate|wake|plugin_install"
  target: "string - agent name or plugin name"

  # Timing
  submitted_at: "ISO-8601 - when request was sent"
  last_reminder_at: "ISO-8601 | null - when last reminder was sent"
  timeout_at: "ISO-8601 - when timeout will occur"
  resolved_at: "ISO-8601 | null - when decision was received"

  # State
  status: "string - pending|escalated|resolved"
  escalation_count: "integer - number of reminders sent (0-3)"

  # Resolution
  decision: "string | null - approved|rejected|modified|delayed|timeout_proceed|timeout_abort"
  decided_by: "string | null - eama|autonomous|timeout"
  modifications: "object | null - any modifications to original request"
  notes: "string | null - decision notes"

  # Context
  justification: "string - original justification"
  details: "object - operation-specific details"
```

---

## 2.3 Tracking Procedure

### 2.3.1 Request Registration

**When:** Immediately after sending an approval request via AI Maestro.

**Steps:**

1. Create new tracking entry with status `pending`
2. Set `submitted_at` to current timestamp
3. Calculate `timeout_at` as submitted_at + 120 seconds
4. Set `escalation_count` to 0
5. Store in active requests collection
6. Write to state file

**Implementation:**

```python
def register_request(request_id, operation, target, details, justification):
    now = datetime.utcnow().isoformat() + "Z"
    timeout = (datetime.utcnow() + timedelta(seconds=120)).isoformat() + "Z"

    entry = {
        "request_id": request_id,
        "operation": operation,
        "target": target,
        "submitted_at": now,
        "last_reminder_at": None,
        "timeout_at": timeout,
        "resolved_at": None,
        "status": "pending",
        "escalation_count": 0,
        "decision": None,
        "decided_by": None,
        "modifications": None,
        "notes": None,
        "justification": justification,
        "details": details
    }

    active_requests[request_id] = entry
    save_state_file()
    return entry
```

### 2.3.2 Status Monitoring

**When:** Continuously while requests are pending.

**Monitoring loop:**

1. Check for incoming messages from EAMA
2. Match messages to pending requests by `request_id`
3. Check if any pending requests have exceeded escalation thresholds
4. Trigger escalation if needed

**Escalation thresholds:**
- 60 seconds: First reminder (escalation_count = 1)
- 90 seconds: Urgent notification (escalation_count = 2)
- 120 seconds: Final timeout (escalation_count = 3)

**Check for responses:**

```bash
# Poll for unread messages
curl -s "http://localhost:23000/api/messages?agent=ecos-chief-of-staff&action=list&status=unread" | \
  jq '.messages[] | select(.content.type == "approval_response")'
```

**Match response to request:**

```python
def check_for_responses():
    messages = fetch_unread_messages()

    for msg in messages:
        if msg.get("content", {}).get("type") == "approval_response":
            request_id = msg["content"]["request_id"]
            if request_id in active_requests:
                resolve_request(request_id, msg["content"])
                mark_message_read(msg["id"])
```

### 2.3.3 Concurrent Request Handling

ECOS may have multiple approval requests pending simultaneously. Each request is tracked independently.

**Concurrency rules:**

1. Each request has its own timeout timer
2. Escalations are sent per-request, not batched
3. Responses are matched by `request_id`, not by order
4. One request's timeout does not affect others

**Managing multiple requests:**

```python
def get_pending_requests():
    return [r for r in active_requests.values() if r["status"] == "pending"]

def check_all_timeouts():
    now = datetime.utcnow()

    for request in get_pending_requests():
        submitted = datetime.fromisoformat(request["submitted_at"].rstrip("Z"))
        elapsed = (now - submitted).total_seconds()

        if elapsed >= 120 and request["escalation_count"] < 3:
            trigger_final_timeout(request)
        elif elapsed >= 90 and request["escalation_count"] < 2:
            send_urgent_reminder(request)
        elif elapsed >= 60 and request["escalation_count"] < 1:
            send_first_reminder(request)
```

**Priority handling:**

When multiple requests are pending, process responses in this order:
1. Urgent priority requests
2. High priority requests
3. Normal priority requests
4. Oldest requests first within same priority

### 2.3.4 Resolution Recording

**When:** Upon receiving a response from EAMA or upon timeout.

**Steps:**

1. Update tracking entry status to `resolved`
2. Set `resolved_at` to current timestamp
3. Record decision, decided_by, modifications, and notes
4. Move from active requests to resolved requests
5. Write to audit trail
6. Update state file

**Implementation:**

```python
def resolve_request(request_id, response):
    if request_id not in active_requests:
        return  # Request not found

    request = active_requests[request_id]
    now = datetime.utcnow().isoformat() + "Z"

    request["status"] = "resolved"
    request["resolved_at"] = now
    request["decision"] = response.get("decision")
    request["decided_by"] = "eama"
    request["modifications"] = response.get("modifications")
    request["notes"] = response.get("notes")

    # Move to resolved
    resolved_requests[request_id] = request
    del active_requests[request_id]

    # Write audit trail
    write_audit_entry(request)
    save_state_file()

    return request
```

**Timeout resolution:**

```python
def resolve_timeout(request_id, action):
    request = active_requests[request_id]
    now = datetime.utcnow().isoformat() + "Z"

    request["status"] = "resolved"
    request["resolved_at"] = now
    request["decision"] = f"timeout_{action}"  # timeout_proceed or timeout_abort
    request["decided_by"] = "timeout"
    request["notes"] = f"Timed out after {request['escalation_count']} escalation attempts"

    resolved_requests[request_id] = request
    del active_requests[request_id]

    write_audit_entry(request)
    save_state_file()
```

---

## 2.4 State File Format

ECOS maintains approval tracking state in a YAML file.

**File location:** `docs_dev/state/ecos-approval-tracking.yaml`

**File structure:**

```yaml
# ECOS Approval Tracking State
# Last updated: {ISO-8601 timestamp}

metadata:
  version: "1.0"
  last_updated: "2025-02-02T10:30:00Z"
  total_requests: 47
  pending_count: 2
  resolved_count: 45

active_requests:
  spawn-req-2025-02-02-005:
    request_id: "spawn-req-2025-02-02-005"
    operation: "spawn"
    target: "backend-api-03"
    submitted_at: "2025-02-02T10:29:00Z"
    last_reminder_at: null
    timeout_at: "2025-02-02T10:31:00Z"
    resolved_at: null
    status: "pending"
    escalation_count: 0
    decision: null
    decided_by: null
    modifications: null
    notes: null
    justification: "Need additional API agent for parallel endpoint development"
    details:
      agent_name: "backend-api-03"
      agent_role: "backend-developer"
      task: "Implement user settings API endpoints"
      working_directory: "/Users/dev/project/api"
      expected_duration: "3 hours"
      resource_requirements: "standard"

  hibernate-req-2025-02-02-002:
    request_id: "hibernate-req-2025-02-02-002"
    operation: "hibernate"
    target: "test-runner-02"
    submitted_at: "2025-02-02T10:28:30Z"
    last_reminder_at: "2025-02-02T10:29:30Z"
    timeout_at: "2025-02-02T10:30:30Z"
    resolved_at: null
    status: "escalated"
    escalation_count: 1
    decision: null
    decided_by: null
    modifications: null
    notes: null
    justification: "Agent idle for 52 minutes"
    details:
      agent_name: "test-runner-02"
      idle_duration: "52 minutes"
      last_activity: "2025-02-02T09:36:00Z"
      expected_wake_trigger: "New test suite ready"

resolved_requests:
  # Last 10 resolved requests kept for reference
  spawn-req-2025-02-02-004:
    request_id: "spawn-req-2025-02-02-004"
    operation: "spawn"
    target: "frontend-dev-02"
    submitted_at: "2025-02-02T10:20:00Z"
    resolved_at: "2025-02-02T10:20:45Z"
    status: "resolved"
    escalation_count: 0
    decision: "approved"
    decided_by: "eama"
    notes: "Approved for dashboard work"
```

**State file operations:**

```python
import yaml
from pathlib import Path

STATE_FILE = Path("docs_dev/state/ecos-approval-tracking.yaml")

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, "r") as f:
            return yaml.safe_load(f)
    return {
        "metadata": {"version": "1.0", "total_requests": 0, "pending_count": 0, "resolved_count": 0},
        "active_requests": {},
        "resolved_requests": {}
    }

def save_state():
    state = {
        "metadata": {
            "version": "1.0",
            "last_updated": datetime.utcnow().isoformat() + "Z",
            "total_requests": len(active_requests) + len(resolved_requests),
            "pending_count": len(active_requests),
            "resolved_count": len(resolved_requests)
        },
        "active_requests": active_requests,
        "resolved_requests": dict(list(resolved_requests.items())[-10:])  # Keep last 10
    }

    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        yaml.dump(state, f, default_flow_style=False, sort_keys=False)
```

---

## 2.5 Examples

### Example 1: Tracking a New Spawn Request

```python
# Request sent
request_id = "spawn-req-2025-02-02-006"

# Register in tracking
entry = register_request(
    request_id=request_id,
    operation="spawn",
    target="docs-writer-01",
    details={
        "agent_name": "docs-writer-01",
        "agent_role": "documentation-writer",
        "task": "Generate API documentation",
        "working_directory": "/Users/dev/project/docs",
        "expected_duration": "2 hours",
        "resource_requirements": "low"
    },
    justification="API documentation required for release 2.0"
)

# State file updated with new entry
# Status: pending
# Timeout at: submitted_at + 120 seconds
```

### Example 2: Monitoring and Escalation

```python
# T+0: Request registered
# Status: pending, escalation_count: 0

# T+60: First timeout reached
check_all_timeouts()
# Sends reminder to EAMA
# Updates: last_reminder_at, escalation_count: 1, status: escalated

# T+90: Second timeout reached
check_all_timeouts()
# Sends urgent notification to EAMA
# Updates: last_reminder_at, escalation_count: 2

# T+120: Final timeout reached
check_all_timeouts()
# Determines proceed or abort based on operation type
# Updates: resolved_at, decision: timeout_proceed|timeout_abort, escalation_count: 3
```

### Example 3: Receiving and Processing Response

```python
# Response received from EAMA
response = {
    "type": "approval_response",
    "request_id": "spawn-req-2025-02-02-006",
    "decision": "approved",
    "decided_at": "2025-02-02T10:35:20Z",
    "modifications": None,
    "notes": "Approved. Start documentation work."
}

# Match to pending request
request = active_requests.get(response["request_id"])

if request:
    # Resolve the request
    resolve_request(response["request_id"], response)

    # Entry now in resolved_requests
    # decision: approved
    # decided_by: eama
    # status: resolved

    # Can now proceed with spawn operation
    proceed_with_operation(request)
```

### Example 4: Multiple Concurrent Requests

```python
# State with multiple pending requests
active_requests = {
    "spawn-req-2025-02-02-007": {
        "status": "pending",
        "operation": "spawn",
        "target": "agent-a",
        "submitted_at": "2025-02-02T10:40:00Z",
        "escalation_count": 0
    },
    "terminate-req-2025-02-02-003": {
        "status": "escalated",
        "operation": "terminate",
        "target": "agent-b",
        "submitted_at": "2025-02-02T10:38:00Z",
        "escalation_count": 2
    },
    "hibernate-req-2025-02-02-004": {
        "status": "pending",
        "operation": "hibernate",
        "target": "agent-c",
        "submitted_at": "2025-02-02T10:39:30Z",
        "escalation_count": 0
    }
}

# Response arrives for terminate request
response = {
    "request_id": "terminate-req-2025-02-02-003",
    "decision": "rejected",
    "notes": "Keep agent-b alive for now"
}

# Only terminate request is resolved
# Other two remain pending
resolve_request("terminate-req-2025-02-02-003", response)

# Now:
# active_requests has 2 entries (spawn and hibernate)
# resolved_requests has 1 entry (terminate)
```

---

## 2.6 Troubleshooting

### Issue: State file corruption

**Symptoms:**
- YAML parse error when loading state
- Missing or malformed entries
- Inconsistent counts

**Cause:** Concurrent writes, disk error, or invalid data written.

**Resolution:**
1. Keep backup of state file before each write
2. Validate YAML before saving
3. If corrupted, restore from backup or rebuild from audit trail

```python
def save_state_safe():
    backup_path = STATE_FILE.with_suffix(".yaml.bak")
    if STATE_FILE.exists():
        shutil.copy(STATE_FILE, backup_path)

    try:
        save_state()
        # Validate by reading back
        load_state()
    except Exception as e:
        # Restore from backup
        if backup_path.exists():
            shutil.copy(backup_path, STATE_FILE)
        raise e
```

### Issue: Request ID not found for response

**Symptoms:**
- Response received but no matching active request
- "Request not found" warning

**Cause:** Request already resolved (duplicate response) or state lost.

**Resolution:**
1. Check resolved_requests for the ID (duplicate response)
2. Check audit trail for historical record
3. If truly missing, log warning and discard response
4. Review state persistence for gaps

### Issue: Timeout not triggering

**Symptoms:**
- Request pending beyond 120 seconds
- No escalation sent

**Cause:** Monitoring loop not running or timestamp calculation error.

**Resolution:**
1. Verify monitoring loop is active
2. Check system time synchronization
3. Verify timeout_at calculation
4. Manually trigger timeout check

### Issue: Escalation count exceeds maximum

**Symptoms:**
- escalation_count > 3
- Continuous escalation messages

**Cause:** Timeout not properly resolving request.

**Resolution:**
1. Cap escalation_count at 3
2. Force resolve after escalation_count reaches 3
3. Check resolve_timeout function for bugs

### Issue: Memory growth from unresolved requests

**Symptoms:**
- active_requests grows indefinitely
- Memory usage increases over time

**Cause:** Requests never being resolved or moved to resolved.

**Resolution:**
1. Implement maximum pending request limit
2. Force-expire very old requests (> 1 hour)
3. Periodically clean up stale entries

```python
def cleanup_stale_requests():
    now = datetime.utcnow()
    max_age = timedelta(hours=1)

    for request_id, request in list(active_requests.items()):
        submitted = datetime.fromisoformat(request["submitted_at"].rstrip("Z"))
        if (now - submitted) > max_age:
            request["decision"] = "expired"
            request["decided_by"] = "cleanup"
            request["notes"] = "Force-expired after 1 hour"
            resolved_requests[request_id] = request
            del active_requests[request_id]

    save_state()
```

---

**Version:** 1.0
**Last Updated:** 2025-02-02
**Related:** [SKILL.md](../SKILL.md), [approval-request-procedure.md](approval-request-procedure.md), [approval-escalation.md](approval-escalation.md)
