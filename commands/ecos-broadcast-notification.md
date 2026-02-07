---
name: ecos-broadcast-notification
description: "Send notification to multiple agents simultaneously with filtering by role or project"
argument-hint: "--agents <names> | --role <role> | --project <project> --subject <text> --message <text> [--priority normal|high|urgent]"
allowed-tools: ["Bash", "Task"]
user-invocable: true
---

# Broadcast Notification Command

Send a notification to multiple agents simultaneously with filtering options by agent names, role, or project assignment.

## Usage

```!
# Broadcast notification via AI Maestro API
# Arguments: $ARGUMENTS

# Filter options (choose one):
# --agents <name1,name2,...>  Specific agents
# --role <role>               All agents with role
# --project <project>         All agents assigned to project

# Required:
# --subject <text>            Notification subject
# --message <text>            Notification body

# Optional:
# --priority normal|high|urgent  Message priority (default: normal)
```

## Messaging Integration

This command uses the `agent-messaging` skill to broadcast notifications. It first queries the agent registry to resolve filter criteria, then sends messages to all matching agents using the `agent-messaging` skill.

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--agents <names>` | Yes* | Comma-separated list of agent names |
| `--role <role>` | Yes* | Filter by agent role (e.g., `helper`, `specialist`) |
| `--project <project>` | Yes* | Filter by project assignment |
| `--subject <text>` | Yes | Notification subject line |
| `--message <text>` | Yes | Notification message body |
| `--priority <level>` | No | Priority: `normal` (default), `high`, `urgent` |

*One of `--agents`, `--role`, or `--project` is required.

## Priority Levels

| Priority | Icon | Description | Agent Behavior |
|----------|------|-------------|----------------|
| `normal` | - | Standard notification | Process when convenient |
| `high` | ! | Important notification | Process before other tasks |
| `urgent` | !! | Critical notification | Process immediately, interrupt current work |

## Filter Options

### By Agent Names

```bash
/ecos-broadcast-notification --agents helper-python,frontend-ui,data-processor \
  --subject "Team Meeting" --message "Standup in 5 minutes"
```

### By Role

```bash
/ecos-broadcast-notification --role helper \
  --subject "Helper Agents" --message "New task assignment protocol active"
```

The command uses the `ai-maestro-agents-management` skill to query agents matching the role filter.

### By Project

```bash
/ecos-broadcast-notification --project skill-factory \
  --subject "Project Update" --message "New milestone requirements posted"
```

The command uses the `ai-maestro-agents-management` skill to query agents matching the project filter.

## Examples

```bash
# Normal priority broadcast to specific agents
/ecos-broadcast-notification --agents helper-python,frontend-ui \
  --subject "Daily Standup" --message "Please report your status"

# High priority broadcast by role
/ecos-broadcast-notification --role specialist \
  --subject "Code Review Needed" --message "PR #42 requires review by EOD" \
  --priority high

# Urgent broadcast to project team
/ecos-broadcast-notification --project production-api \
  --subject "URGENT: Production Issue" --message "API latency spike detected. Investigate immediately." \
  --priority urgent

# System-wide announcement
/ecos-broadcast-notification --role "*" \
  --subject "System Maintenance" --message "Scheduled maintenance tonight 22:00-23:00 UTC" \
  --priority high
```

## Implementation

This command is implemented by:

1. **Resolving target agents** using the `ai-maestro-agents-management` skill to list agents matching the filter criteria (by name, role, or project)
2. **Sending messages** to each resolved agent using the `agent-messaging` skill:
   - **Recipient**: each matching agent
   - **Subject**: the provided subject
   - **Content**: the provided message with type "broadcast"
   - **Priority**: the provided priority level
3. **Recording delivery status** for each agent

**Verify**: each target agent receives the broadcast message.

## Broadcast Flow

```
1. Parse filter arguments
   |
2. Query agent registry
   |
3. Apply filter (agents/role/project)
   |
4. For each matching agent:
   |-- Format message with priority
   |-- Send via API
   |-- Record delivery status
   |
5. Report broadcast summary
```

## Output Format

```
================================================================================
  BROADCAST NOTIFICATION
================================================================================

  Subject: Code Review Needed
  Priority: HIGH
  Message: PR #42 requires review by EOD

  Filter: --role specialist
  Resolved agents: 3

  Sending broadcast...

  Agent                  | Status
  -----------------------|------------
  code-reviewer-1        | Delivered
  code-reviewer-2        | Delivered
  qa-specialist          | Delivered

================================================================================
  Broadcast complete: 3/3 delivered
================================================================================
```

## Priority Display in Agent Inbox

When agents receive the notification:

**Normal Priority:**
```
[BROADCAST] Code Review Needed
```

**High Priority:**
```
[!] [BROADCAST] Code Review Needed
```

**Urgent Priority:**
```
[!!] [URGENT BROADCAST] Code Review Needed
```

## Role Wildcards

Special role values:
- `*` - All agents in registry
- `helper` - Helper agents
- `specialist` - Specialist agents
- `orchestrator` - Orchestrator agents
- `custom-role` - Any custom role defined in registry

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "No agents match filter" | Filter too restrictive | Check filter criteria |
| "Agent not found" | Agent offline or removed | Verify agent status |
| "API unreachable" | AI Maestro not running | Start AI Maestro server |
| "Invalid priority" | Wrong priority value | Use `normal`, `high`, or `urgent` |

## Delivery Tracking

The command tracks delivery status but does not wait for acknowledgments. For acknowledgment-required notifications, use:

```bash
# Use notify-agents with --require-ack for ack-required broadcasts
/ecos-notify-agents --all --operation custom --message "Message" --require-ack
```

## Related Commands

- `/ecos-notify-agents` - Notify with optional acknowledgment
- `/ecos-wait-for-agent-ok` - Wait for specific agent acknowledgment
- `/ecos-install-skill-notify` - Skill installation with notifications
- `/ecos-staff-status` - View all agents and their status
