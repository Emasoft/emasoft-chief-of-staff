---
name: ecos-notify-agents
description: "Notify agents before or after operations via AI Maestro messaging API"
argument-hint: "--agents <name1,name2,...> | --all --operation <type> --message <text> [--require-ack]"
allowed-tools: ["Bash", "Task"]
user-invocable: true
---

# Notify Agents Command

Send notifications to specific agents or all agents before or after operations via the AI Maestro messaging API.

## Usage

Parse the provided arguments and send notifications to agents using the `agent-messaging` skill.

## Messaging Integration

This command uses the `agent-messaging` skill to send notifications to agents.

For each target agent, send a notification message using the `agent-messaging` skill:
- **Recipient**: the target agent
- **Subject**: `[NOTIFICATION] <operation>`
- **Content**: the notification message with operation type
- **Type**: `notification`
- **Priority**: `normal`
- If `--require-ack` is set, include acknowledgment request in the message

**Verify**: confirm message delivery via the `agent-messaging` skill's sent messages feature.

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--agents <names>` | Yes* | Comma-separated list of agent names to notify |
| `--all` | Yes* | Notify all registered agents (alternative to --agents) |
| `--operation <type>` | Yes | Type of operation (e.g., `skill-install`, `restart`, `update`) |
| `--message <text>` | Yes | Notification message text |
| `--require-ack` | No | Wait for acknowledgment from each agent |

*One of `--agents` or `--all` is required.

## Operation Types

| Operation | Description | Typical Use |
|-----------|-------------|-------------|
| `skill-install` | Skill installation starting/complete | Before/after installing skills |
| `plugin-install` | Plugin installation starting/complete | Before/after installing plugins |
| `restart` | Agent restart required | When plugin changes require restart |
| `hibernate` | Mass hibernation event | End of day or maintenance |
| `wake` | Mass wake event | Start of day |
| `update` | System update notification | Software updates |
| `maintenance` | Maintenance window | System maintenance periods |
| `custom` | Custom notification | Any other notification |

## Examples

```bash
# Notify specific agents about skill installation
/ecos-notify-agents --agents helper-python,frontend-ui --operation skill-install --message "Installing new validation skill in 60 seconds"

# Notify all agents about system maintenance
/ecos-notify-agents --all --operation maintenance --message "System maintenance starting in 5 minutes"

# Notify with acknowledgment required
/ecos-notify-agents --agents data-processor --operation restart --message "Plugin update requires restart. Please finish current task." --require-ack

# Pre-operation notification
/ecos-notify-agents --agents helper-python --operation skill-install --message "Will install data-validation skill. Please save your work."

# Post-operation notification
/ecos-notify-agents --agents helper-python --operation skill-install --message "Skill installation complete. Please verify activation."
```

## Notification Flow

### Without Acknowledgment

```
1. Parse arguments
   |
2. Resolve agent list (--agents or --all)
   |
3. For each agent:
   |-- Send notification via API
   |-- Log delivery status
   |
4. Report summary
```

### With Acknowledgment (--require-ack)

```
1. Parse arguments
   |
2. Resolve agent list
   |
3. For each agent:
   |-- Send notification with requireAck=true
   |-- Wait for acknowledgment (up to 120s)
   |-- Send reminder at 30s intervals
   |
4. Report acknowledgments received
```

## Implementation

This command is implemented by:

1. **Resolving target agents**: if `--all` is specified, use the `ai-maestro-agents-management` skill to list all agents; otherwise use the explicit agent list
2. **Sending notifications**: for each target agent, send a message using the `agent-messaging` skill with the operation type and message content
3. **Polling for acknowledgments** (if `--require-ack`): use the `agent-messaging` skill to check for incoming acknowledgment messages from each agent

**Verify**: each target agent receives the notification. If `--require-ack`, confirm acknowledgments are received.

## Output Format

```
================================================================================
  NOTIFY AGENTS
================================================================================

  Operation: skill-install
  Message: Installing new validation skill in 60 seconds
  Require Ack: Yes

  Sending notifications...

  Agent                  | Status      | Ack
  -----------------------|-------------|-------
  helper-python          | Delivered   | Pending
  frontend-ui            | Delivered   | Pending
  data-processor         | Delivered   | Pending

  Waiting for acknowledgments (timeout: 120s)...

  Agent                  | Status      | Ack
  -----------------------|-------------|-------
  helper-python          | Delivered   | OK (15s)
  frontend-ui            | Delivered   | OK (42s)
  data-processor         | Delivered   | OK (89s)

================================================================================
  All agents acknowledged successfully
================================================================================
```

## Acknowledgment Protocol

When `--require-ack` is specified, agents should respond with:

```json
{
  "to": "<sender>",
  "subject": "RE: [NOTIFICATION] <operation>",
  "content": {
    "type": "ack",
    "operation": "<operation>",
    "status": "ready"
  }
}
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Agent not found" | Invalid agent name | Check with `/ecos-staff-status` |
| "API unreachable" | AI Maestro not running | Start AI Maestro server |
| "Timeout waiting for ack" | Agent didn't respond | Agent may be busy or offline |
| "Delivery failed" | Network or agent issue | Check agent status |

## Timeout Behavior

When `--require-ack` is specified:
- Default timeout: 120 seconds per agent
- Reminders sent every 30 seconds
- If timeout reached, notification logged as "timeout" but command continues
- Final report shows which agents timed out

## Related Commands

- `/ecos-wait-for-agent-ok` - Wait for single agent acknowledgment
- `/ecos-broadcast-notification` - Send broadcast with priority
- `/ecos-staff-status` - View all agents
- `/ecos-install-skill-notify` - Install skill with full notification protocol
