---
name: ecos-wait-for-agent-ok
description: "Wait for an agent to acknowledge readiness with polling and reminders"
argument-hint: "--agent <name> [--timeout <seconds>] [--remind-interval <seconds>]"
allowed-tools: ["Bash(curl:*)", "Read"]
user-invocable: true
---

# Wait For Agent OK Command

Wait for an agent to acknowledge readiness by polling the AI Maestro messaging API. Sends periodic reminders until acknowledgment received or timeout.

## Usage

```!
# Poll for agent acknowledgment via AI Maestro API
# Arguments: $ARGUMENTS

AGENT=""
TIMEOUT=120
REMIND_INTERVAL=30

# Parse arguments and poll for "ok" message from agent
```

## AI Maestro API Integration

This command polls the AI Maestro messaging API waiting for an acknowledgment message from a specific agent.

**Poll Endpoint**: `http://localhost:23000/api/messages?agent=<self>&action=list&status=unread`

**Expected Acknowledgment Format**:
```json
{
  "from": "<agent_name>",
  "content": {
    "type": "ack",
    "status": "ready"
  }
}
```

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--agent <name>` | Yes | - | Agent name to wait for |
| `--timeout <seconds>` | No | 120 | Maximum wait time in seconds |
| `--remind-interval <seconds>` | No | 30 | Interval between reminder messages |

## Examples

```bash
# Wait for agent with default settings (120s timeout, 30s reminders)
/ecos-wait-for-agent-ok --agent helper-python

# Wait with custom timeout
/ecos-wait-for-agent-ok --agent data-processor --timeout 300

# Wait with shorter reminder interval
/ecos-wait-for-agent-ok --agent frontend-ui --timeout 180 --remind-interval 15

# Quick wait with no reminders (set interval > timeout)
/ecos-wait-for-agent-ok --agent helper-python --timeout 60 --remind-interval 120
```

## Wait Flow

```
1. Initial request sent (from calling command or prior notification)
   |
2. Start polling loop
   |
3. Every <remind-interval> seconds:
   |-- Check for acknowledgment message
   |-- If found: exit success
   |-- If not found: send reminder
   |
4. Continue until:
   |-- Acknowledgment received -> SUCCESS
   |-- Timeout reached -> WARNING (proceed anyway)
```

## Implementation

Execute the following polling logic:

```bash
#!/bin/bash
# Polling script for agent acknowledgment

AGENT="$1"
TIMEOUT="${2:-120}"
REMIND_INTERVAL="${3:-30}"
SELF_AGENT="${SESSION_NAME:-orchestrator}"
API_BASE="http://localhost:23000"

start_time=$(date +%s)
last_remind=0

echo "Waiting for acknowledgment from: $AGENT"
echo "Timeout: ${TIMEOUT}s | Remind interval: ${REMIND_INTERVAL}s"

while true; do
  current_time=$(date +%s)
  elapsed=$((current_time - start_time))

  # Check timeout
  if [ $elapsed -ge $TIMEOUT ]; then
    echo "[WARNING] Timeout reached waiting for $AGENT"
    echo "[WARNING] Proceeding without acknowledgment"
    exit 0  # Exit success but with warning
  fi

  # Poll for acknowledgment
  ack=$(curl -s "${API_BASE}/api/messages?agent=${SELF_AGENT}&action=list&status=unread" | \
    jq -r ".messages[] | select(.from == \"$AGENT\" and .content.type == \"ack\") | .content.status")

  if [ "$ack" = "ready" ]; then
    echo "[SUCCESS] Agent $AGENT acknowledged: ready"
    # Mark message as read
    exit 0
  fi

  # Send reminder if interval elapsed
  time_since_remind=$((current_time - last_remind))
  if [ $time_since_remind -ge $REMIND_INTERVAL ]; then
    echo "[REMINDER] Sending reminder to $AGENT..."
    curl -s -X POST "${API_BASE}/api/messages" \
      -H "Content-Type: application/json" \
      -d "{
        \"to\": \"$AGENT\",
        \"subject\": \"[REMINDER] Waiting for your acknowledgment\",
        \"priority\": \"high\",
        \"content\": {
          \"type\": \"reminder\",
          \"message\": \"Please acknowledge when ready. Waiting for ${elapsed}s of ${TIMEOUT}s.\"
        }
      }"
    last_remind=$current_time
  fi

  # Wait before next poll
  sleep 5
done
```

## Output Format

### Success Case

```
================================================================================
  WAITING FOR AGENT OK
================================================================================

  Agent: helper-python
  Timeout: 120 seconds
  Remind interval: 30 seconds

  [00:00] Polling for acknowledgment...
  [00:05] No response yet
  [00:10] No response yet
  [00:15] No response yet
  [00:20] No response yet
  [00:25] No response yet
  [00:30] Sending reminder to helper-python...
  [00:35] No response yet
  [00:40] No response yet
  [00:42] Acknowledgment received!

================================================================================
  Agent 'helper-python' acknowledged: READY
  Wait time: 42 seconds
================================================================================
```

### Timeout Case

```
================================================================================
  WAITING FOR AGENT OK
================================================================================

  Agent: helper-python
  Timeout: 120 seconds
  Remind interval: 30 seconds

  [00:00] Polling for acknowledgment...
  [00:30] Sending reminder to helper-python...
  [00:60] Sending reminder to helper-python...
  [00:90] Sending reminder to helper-python...
  [02:00] TIMEOUT REACHED

================================================================================
  [WARNING] Agent 'helper-python' did not acknowledge within 120s

  Proceeding with operation anyway.
  The agent may be busy or temporarily unavailable.
================================================================================
```

## Acknowledgment Message Format

Agents should respond with this message format:

```json
{
  "to": "<orchestrator-session>",
  "subject": "ACK: Ready",
  "content": {
    "type": "ack",
    "status": "ready",
    "message": "Work saved, ready for operation"
  }
}
```

## Typical Usage Pattern

```bash
# 1. Notify agent about upcoming operation
/ecos-notify-agents --agents helper-python --operation skill-install --message "Saving work? Let me know when ready."

# 2. Wait for agent to acknowledge
/ecos-wait-for-agent-ok --agent helper-python --timeout 120

# 3. Proceed with operation (skill install, restart, etc.)
aimaestro-agent.sh plugin install helper-python my-skill@marketplace
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Agent not found" | Invalid agent name | Check with `/ecos-staff-status` |
| "API unreachable" | AI Maestro not running | Start AI Maestro server |
| "Timeout" | Agent didn't respond | Proceed with warning or abort |

## Timeout Behavior

When timeout is reached:
- Command exits with success (exit code 0)
- Warning message displayed
- Calling workflow should decide whether to proceed or abort
- Log entry created for tracking

**Rationale**: The orchestrator decides policy. This command provides information about whether ack was received, but doesn't block critical operations.

## Related Commands

- `/ecos-notify-agents` - Send notifications with optional ack
- `/ecos-broadcast-notification` - Broadcast to multiple agents
- `/ecos-install-skill-notify` - Full skill installation workflow
- `/ecos-staff-status` - Check agent status
