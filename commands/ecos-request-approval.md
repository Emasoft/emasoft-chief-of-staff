---
name: ecos-request-approval
description: "Request approval from manager (EAMA) for agent operations via AI Maestro"
argument-hint: "--type <TYPE> --agent <NAME> --reason <TEXT> [--urgent] [--timeout <SECONDS>]"
allowed-tools: ["Bash(aimaestro-agent.sh:*)", "Task", "Read"]
user-invocable: true
---

# Request Approval Command

Request approval from the Assistant Manager (EAMA) for sensitive agent operations. Sends an approval request via AI Maestro messaging and optionally waits for response.

## Usage

Send an approval request to EAMA using the `agent-messaging` skill:
- **Recipient**: `emasoft-assistant-manager-agent` (EAMA)
- **Subject**: `[APPROVAL REQUEST] <type>: <agent-name>`
- **Content**: structured approval request with request ID, operation type, agent name, reason, and timestamp
- **Priority**: `high` (or `urgent` if `--urgent` flag is set)

**Verify**: confirm the approval request message was delivered to EAMA.

## Operations Requiring Approval

| Operation Type | Description | Risk Level |
|----------------|-------------|------------|
| `spawn` | Create a new remote agent | Medium |
| `terminate` | Permanently delete an agent | High |
| `hibernate` | Put agent into hibernation | Low |
| `wake` | Wake a hibernated agent | Low |
| `install` | Install plugin on agent | Medium |
| `replace` | Replace agent with new instance | High |
| `modify-config` | Change agent configuration | Medium |

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--type <TYPE>` | **Yes** | Operation type (spawn, terminate, hibernate, wake, install, replace) |
| `--agent <NAME>` | **Yes** | Target agent name |
| `--reason <TEXT>` | **Yes** | Justification for the operation |
| `--urgent` | No | Mark as urgent priority (default: high) |
| `--timeout <SECONDS>` | No | Wait for response (default: 0, no wait) |
| `--metadata <JSON>` | No | Additional context as JSON string |

## Request ID Generation

Each request gets a unique ID for tracking:

```bash
REQUEST_ID="ECOS-$(date +%Y%m%d%H%M%S)-$(openssl rand -hex 4)"
```

Example: `ECOS-20250202150000-a1b2c3d4`

## Examples

```bash
# Request approval to spawn a new agent
/ecos-request-approval --type spawn --agent helper-tester \
  --reason "Need additional agent for parallel test execution"

# Request approval to terminate an agent (high risk)
/ecos-request-approval --type terminate --agent old-worker --urgent \
  --reason "Agent has critical bug and cannot recover"

# Request approval to install a plugin
/ecos-request-approval --type install --agent helper-python \
  --reason "Agent needs emasoft-integrator plugin for CI/CD tasks" \
  --metadata '{"plugin": "emasoft-integrator-agent"}'

# Request with wait for response
/ecos-request-approval --type hibernate --agent helper-docs \
  --reason "Pausing documentation work until API is finalized" \
  --timeout 60
```

## Request Message Format

The approval request is sent as a structured AI Maestro message:

```json
{
  "from": "emasoft-chief-of-staff",
  "to": "emasoft-assistant-manager-agent",
  "subject": "[APPROVAL REQUEST] terminate: helper-python",
  "priority": "high",
  "content": {
    "type": "approval_request",
    "request_id": "ECOS-20250202150000-a1b2c3d4",
    "operation_type": "terminate",
    "agent_name": "helper-python",
    "reason": "Agent has critical bug and cannot recover",
    "timestamp": "2025-02-02T15:00:00Z",
    "metadata": {}
  }
}
```

## Response Format

EAMA responds with an approval decision:

```json
{
  "type": "approval_response",
  "request_id": "ECOS-20250202150000-a1b2c3d4",
  "decision": "approved",
  "conditions": [],
  "notes": "Proceed with termination. Ensure work is backed up first.",
  "timestamp": "2025-02-02T15:02:30Z"
}
```

Decision values: `approved`, `rejected`, `deferred`, `needs_more_info`

## Output Format

```
=======================================================================
  APPROVAL REQUEST SUBMITTED
=======================================================================

  Request ID:    ECOS-20250202150000-a1b2c3d4
  Operation:     terminate
  Target Agent:  helper-python
  Priority:      high

  Reason: Agent has critical bug and cannot recover

  Status: PENDING - Awaiting EAMA response

=======================================================================
  Use /ecos-check-approval-status --request-id ECOS-20250202150000-a1b2c3d4
  to check the status of this request.
=======================================================================
```

## Tracking Approvals

Approval requests are logged to:

```
~/.aimaestro/approvals/pending/ECOS-20250202150000-a1b2c3d4.json
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "AI Maestro not responding" | API unreachable | Check if AI Maestro is running |
| "EAMA not available" | Manager agent offline | Wait or contact user |
| "Invalid operation type" | Unknown type | Use valid type from list |
| "Missing required argument" | Incomplete command | Provide all required args |

## Pre-Approval Guidelines

Before requesting approval:

1. **Verify necessity** - Is approval actually required for this operation?
2. **Gather context** - Include relevant details in reason
3. **Check prerequisites** - Ensure target agent exists and is accessible
4. **Assess urgency** - Only use `--urgent` for time-sensitive situations

## Related Commands

- `/ecos-check-approval-status` - Check status of pending approvals
- `/ecos-wait-for-approval` - Wait for approval with timeout
- `/ecos-notify-manager` - Send notification to manager
- `/ecos-staff-status` - View all agents
