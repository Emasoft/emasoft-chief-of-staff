---
operation: maintain-teammate-awareness
procedure: proc-notify-team-ready
workflow-instruction: Step 5 - Team Ready Notification
parent-skill: ecos-team-coordination
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Maintain Teammate Awareness

## When to Use

Trigger this operation when:
- Starting a coordination session (initial team state discovery)
- Before assigning new tasks (verify agent availability)
- Reporting team status to user or manager
- Detecting potential issues (inactive agents, overloaded agents)
- Periodically during long operations (every 5-10 minutes)

## Prerequisites

- AI Maestro API is accessible at http://localhost:23000
- Team roster exists with expected agents
- Permission to query agent sessions
- Understanding of expected team composition

## Procedure

### Step 1: Poll AI Maestro for Active Sessions

```bash
# Get all active sessions
curl -s "http://localhost:23000/api/sessions" | jq '.sessions[] | {name: .name, status: .status, lastSeen: .lastSeen}'
```

### Step 2: Query Each Agent's Status

For agents that need detailed status:

```bash
# Send status request to specific agent
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "<agent-session-name>",
    "subject": "Status Check",
    "priority": "normal",
    "content": {
      "type": "status-request",
      "message": "Please report your current status: task, progress, blockers."
    }
  }'
```

### Step 3: Update Team Roster

Compile status information into team roster:
- Agent name
- Session status (active/inactive/hibernating)
- Current task (if known)
- Last seen timestamp
- Any reported blockers

### Step 4: Identify Inactive Agents

Compare expected team members against active sessions:

```bash
# Expected agents (example)
EXPECTED=("code-impl-auth" "test-engineer-01" "docs-writer" "chief-of-staff")

# Get active agents
ACTIVE=$(curl -s "http://localhost:23000/api/sessions" | jq -r '.sessions[].name')

# Find missing agents
for agent in "${EXPECTED[@]}"; do
  if ! echo "$ACTIVE" | grep -q "$agent"; then
    echo "MISSING: $agent"
  fi
done
```

### Step 5: Flag Issues

Document any anomalies:
- Agents that should be active but are not
- Agents that have not responded to status requests
- Agents with stale lastSeen timestamps (more than 5 minutes)
- Agents reporting blockers

## Checklist

Copy this checklist and track your progress:

- [ ] Polled AI Maestro for all active sessions
- [ ] Sent status requests to key agents
- [ ] Updated team roster with current information
- [ ] Identified any inactive or missing agents
- [ ] Flagged issues for follow-up
- [ ] Documented team state for reporting

## Examples

### Example: Initial Team State Discovery

**Scenario:** Chief of Staff starting a new coordination session.

```bash
# Step 1: Get all sessions
echo "=== Active Sessions ==="
curl -s "http://localhost:23000/api/sessions" | jq '.sessions[] | {name: .name, status: .status, lastSeen: .lastSeen}'

# Step 2: Check unread messages for any pending issues
echo "=== Unread Messages ==="
curl -s "http://localhost:23000/api/messages?agent=chief-of-staff&action=list&status=unread" | jq '.messages[] | {from: .from, subject: .subject, priority: .priority}'
```

**Expected Output:**
```json
{
  "name": "code-impl-auth",
  "status": "active",
  "lastSeen": "2025-02-05T10:30:00Z"
}
{
  "name": "test-engineer-01",
  "status": "active",
  "lastSeen": "2025-02-05T10:29:45Z"
}
```

### Example: Pre-Task Assignment Check

**Scenario:** Before assigning a task to code-impl-auth, verify availability.

```bash
# Check if agent is active
STATUS=$(curl -s "http://localhost:23000/api/sessions" | jq -r '.sessions[] | select(.name == "code-impl-auth") | .status')

if [ "$STATUS" == "active" ]; then
  echo "Agent is active, checking current workload..."

  # Send status request
  curl -X POST "http://localhost:23000/api/messages" \
    -H "Content-Type: application/json" \
    -d '{
      "to": "code-impl-auth",
      "subject": "Availability Check",
      "priority": "normal",
      "content": {
        "type": "status-request",
        "message": "Are you available for a new task? Please report current workload."
      }
    }'
else
  echo "WARNING: Agent is not active (status: $STATUS)"
fi
```

### Example: Team Status Report Generation

**Scenario:** Generate a summary for the user.

```bash
# Collect all agent statuses
echo "=== Team Status Report ==="
echo "Generated: $(date)"
echo ""

curl -s "http://localhost:23000/api/sessions" | jq -r '.sessions[] | "Agent: \(.name)\n  Status: \(.status)\n  Last Seen: \(.lastSeen)\n"'
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| AI Maestro API unreachable | Service not running | Run `curl -s "http://localhost:23000/api/health"` to diagnose; notify user if service is down |
| Agent shows stale lastSeen | Agent hibernated or crashed | Attempt to wake agent; if no response, flag for user attention |
| Status request times out | Agent busy or unresponsive | Wait 30 seconds, retry once; if still no response, mark as "unresponsive" |
| Team roster mismatch | New agents not registered | Update expected team list; query for newly registered sessions |
| Inconsistent status data | Cache or sync issue | Force refresh by re-querying all sessions; clear local roster cache |

## Related Operations

- [op-assign-agent-roles.md](op-assign-agent-roles.md) - Awareness informs role assignments
- [op-send-team-messages.md](op-send-team-messages.md) - Status requests use messaging
- [teammate-awareness.md](teammate-awareness.md) - Complete awareness reference documentation
