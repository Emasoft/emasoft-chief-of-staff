---
name: ecos-notify-manager
description: "Notify the Assistant Manager (EAMA) about issues, status updates, or alerts via AI Maestro"
argument-hint: "--subject <TEXT> --message <TEXT> [--priority <PRIORITY>] [--type <TYPE>]"
allowed-tools: ["Bash(aimaestro-agent.sh:*)", "Task"]
user-invocable: true
---

# Notify Manager Command

Send notifications to the Assistant Manager (EAMA) about issues, status updates, alerts, or other important information via AI Maestro messaging.

## Usage

Send a message to the Assistant Manager (EAMA) using the `agent-messaging` skill:
- **Recipient**: `emasoft-assistant-manager-agent` (EAMA)
- **Subject**: the provided subject
- **Content**: structured message with type, message body, timestamp, and optional metadata
- **Priority**: the provided priority level

**Verify**: confirm message delivery to EAMA.

## Notification Types

| Type | Description | Default Priority |
|------|-------------|------------------|
| `status_update` | Regular progress update | normal |
| `issue_report` | Problem requiring attention | high |
| `alert` | Urgent situation | urgent |
| `completion` | Task or operation completed | normal |
| `request_info` | Need information from manager | normal |
| `escalation` | Issue beyond ECOS authority | high |
| `health_check` | Agent/system health status | normal |
| `resource_alert` | Resource constraint warning | high |

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--subject <TEXT>` | **Yes** | Brief subject line (max 100 chars) |
| `--message <TEXT>` | **Yes** | Full message content |
| `--priority <PRIORITY>` | No | Priority: normal, high, urgent (default: normal) |
| `--type <TYPE>` | No | Notification type (default: status_update) |
| `--agent <NAME>` | No | Related agent name (for context) |
| `--metadata <JSON>` | No | Additional structured data as JSON |
| `--require-ack` | No | Request acknowledgment from EAMA |

## Priority Levels

| Priority | Description | When to Use |
|----------|-------------|-------------|
| `normal` | Standard notification | Regular updates, completions |
| `high` | Important notification | Issues, escalations, resource alerts |
| `urgent` | Critical notification | Immediate attention needed, blockers |

## Examples

```bash
# Status update (routine)
/ecos-notify-manager --subject "Daily Status Update" \
  --message "All 5 agents operational. 3 tasks completed, 2 in progress." \
  --type status_update

# Issue report (important)
/ecos-notify-manager --subject "Agent helper-python unresponsive" \
  --message "Agent helper-python has not responded to heartbeat for 10 minutes. Last known state: executing pytest. Recommend investigation." \
  --type issue_report \
  --priority high \
  --agent helper-python

# Urgent alert
/ecos-notify-manager --subject "CRITICAL: Resource exhaustion imminent" \
  --message "System memory usage at 95%. 3 agents may crash if trend continues. Immediate action required: hibernate non-critical agents." \
  --type alert \
  --priority urgent

# Task completion
/ecos-notify-manager --subject "Agent deployment complete" \
  --message "Successfully spawned 3 new agents for the API project. All agents online and accepting tasks." \
  --type completion \
  --metadata '{"agents_spawned": ["api-worker-1", "api-worker-2", "api-tester"]}'

# Escalation
/ecos-notify-manager --subject "Permission escalation needed" \
  --message "Agent helper-devops needs access to production credentials. This is beyond ECOS authority. Requesting manager decision." \
  --type escalation \
  --priority high \
  --require-ack

# Request information
/ecos-notify-manager --subject "Clarification needed on task priority" \
  --message "Multiple urgent tasks received. Need guidance on execution order: (1) security patch, (2) feature deployment, (3) database migration." \
  --type request_info \
  --require-ack
```

## Message Content Structure

Notifications to EAMA include the following content fields:
- **type**: the notification type (e.g., `issue_report`, `status_update`, `alert`)
- **message**: the full notification message
- **timestamp**: UTC timestamp of the notification
- **related_agent**: (optional) name of the related agent
- **require_ack**: whether acknowledgment is requested
- **metadata**: (optional) additional structured data

## Output Format

```
=======================================================================
  NOTIFICATION SENT TO EAMA
=======================================================================

  Timestamp: 2025-02-02 15:30:00 UTC
  Message ID: msg-20250202153000-b2c3d4e5

  To:       emasoft-assistant-manager-agent (EAMA)
  Subject:  Agent helper-python unresponsive
  Priority: HIGH
  Type:     issue_report

  Message:
  Agent helper-python has not responded to heartbeat for 10 minutes.
  Last known state: executing pytest. Recommend investigation.

  ACK Required: No

=======================================================================
  Notification delivered successfully.
=======================================================================
```

## Acknowledgment Request

When `--require-ack` is used, EAMA is expected to respond:

```json
{
  "type": "notification_ack",
  "original_message_id": "msg-20250202153000-b2c3d4e5",
  "acknowledged": true,
  "notes": "Received. Will investigate helper-python.",
  "timestamp": "2025-02-02T15:32:00Z"
}
```

Check for acknowledgment with:
```bash
/ecos-check-approval-status --request-id msg-20250202153000-b2c3d4e5
```

## Best Practices

### DO:
- Keep subjects brief and descriptive
- Include actionable information in messages
- Use appropriate priority levels
- Include relevant agent names with `--agent`
- Add structured data with `--metadata` for complex reports

### DON'T:
- Use `urgent` priority for non-critical updates
- Send duplicate notifications
- Include sensitive credentials in messages
- Send overly verbose messages (summarize instead)

## Rate Limiting

To avoid flooding EAMA:
- Status updates: Max 1 per hour per topic
- Issue reports: Max 3 per hour for same issue
- Alerts: No limit (but must be genuine)

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "AI Maestro not responding" | API unreachable | Check if AI Maestro is running |
| "EAMA not available" | Manager agent offline | Queue message or retry later |
| "Subject too long" | Exceeds 100 chars | Shorten subject line |
| "Invalid priority" | Unknown priority value | Use: normal, high, urgent |
| "Invalid type" | Unknown notification type | Use valid type from list |

## Message Queue

If EAMA is offline, messages are queued:
- Location: `~/.aimaestro/outbox/`
- Auto-retry: Every 5 minutes
- Expiry: 24 hours (configurable)

## Related Commands

- `/ecos-request-approval` - Request operation approval
- `/ecos-check-approval-status` - Check approval/notification status
- `/ecos-staff-status` - View all agent status
- `/ecos-resource-report` - Generate resource utilization report
