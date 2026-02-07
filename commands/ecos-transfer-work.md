---
name: ecos-transfer-work
description: "Transfer work from one agent to another by sending handoff documentation via AI Maestro messaging"
argument-hint: "--from <AGENT> --to <AGENT> --handoff-file <PATH> [--priority urgent|high|normal]"
allowed-tools: ["Bash", "Task", "Read"]
user-invocable: true
---

# Transfer Work Command

Transfer work context from one agent to another by sending handoff documentation via AI Maestro messaging. This is a lightweight work transfer that does not terminate or replace the source agent.

**IMPORTANT: Role Boundaries**
- ECOS sends the handoff documentation to the target agent
- EOA handles the actual task reassignment in the GitHub Project kanban
- Always use `--notify-orchestrator` so EOA can update task assignments

## Usage

```!
# Read the handoff file and send it to the target agent via AI Maestro API
```

## Work Transfer Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    WORK TRANSFER FLOW                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐│
│  │  FROM Agent  │────>│  Handoff Doc │────>│   TO Agent   ││
│  │  (source)    │     │  (context)   │     │  (target)    ││
│  └──────────────┘     └──────────────┘     └──────────────┘│
│                                                             │
│  The handoff document contains:                             │
│  - Task description and current state                       │
│  - Code context and file locations                          │
│  - Pending items and blockers                               │
│  - Instructions for continuation                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--from <agent>` | Yes | Source agent transferring work |
| `--to <agent>` | Yes | Target agent receiving work |
| `--handoff-file <path>` | Yes | Path to handoff documentation file |
| `--priority <level>` | No | Message priority: `urgent`, `high`, `normal` (default: high) |
| `--notify-orchestrator` | No | Also notify EOA about the transfer |
| `--summary <text>` | No | Brief summary to include in message |

## Examples

```bash
# Basic work transfer
/ecos-transfer-work \
  --from helper-backend \
  --to helper-backend-v2 \
  --handoff-file ~/handoffs/backend-transfer.md

# Urgent transfer with notification
/ecos-transfer-work \
  --from crashed-agent \
  --to replacement-agent \
  --handoff-file /tmp/handoff-20240115.md \
  --priority urgent \
  --notify-orchestrator

# Transfer with summary
/ecos-transfer-work \
  --from old-tester \
  --to new-tester \
  --handoff-file ~/docs/test-handoff.md \
  --summary "API endpoint tests 50% complete, focus on /users endpoints"
```

## Handoff File Format

The handoff file should be a Markdown document with the following structure:

```markdown
# Work Handoff: [Task Name]

## Source Agent
- **Agent**: helper-backend
- **Project**: myapp-api
- **Transfer Date**: 2024-01-15

## Task Overview
Brief description of the task being transferred.

## Current State
- Progress: 60% complete
- Last commit: abc1234
- Branch: feature/user-auth

## Completed Work
- [x] Database schema design
- [x] User model implementation
- [x] Basic CRUD endpoints

## Pending Work
- [ ] Authentication middleware
- [ ] Password hashing
- [ ] Session management

## Key Files
- `src/models/user.py` - User model
- `src/routes/auth.py` - Auth endpoints (in progress)
- `tests/test_auth.py` - Test file (partially written)

## Context & Notes
- Using bcrypt for password hashing
- JWT tokens for session management
- Reference: docs/auth-spec.md

## Blockers
- None currently

## Instructions for Continuation
1. Review src/routes/auth.py for current state
2. Complete the login endpoint
3. Run tests with `pytest tests/test_auth.py`
```

## Execution Workflow

### Step 1: Validate Arguments

Use the `ai-maestro-agents-management` skill to:
- Check that the source agent exists (show agent details)
- Check that the target agent exists and is online (health check)

**Verify**: both agents are valid and the target is online.

### Step 2: Read Handoff File

Read the handoff file contents to include in the transfer message.

### Step 3: Send Transfer Message

Send the handoff to the target agent using the `agent-messaging` skill:
- **Recipient**: the target agent
- **Subject**: `[WORK TRANSFER] Task handoff from <source-agent>`
- **Content**: handoff document with source agent name, handoff file path, summary, and instructions
- **Type**: `handoff`
- **Priority**: `high`

**Verify**: target agent receives the handoff message.

### Step 4: Notify Orchestrator (if requested)

If `--notify-orchestrator` is set, send a notification to EOA using the `agent-messaging` skill:
- **Recipient**: `eoa-orchestrator`
- **Subject**: `[TRANSFER NOTIFICATION] Work transferred: <from> -> <to>`
- **Content**: notification about the work transfer with both agent names
- **Priority**: `normal`

**Verify**: EOA receives the transfer notification.

## Output Format

```
═══════════════════════════════════════════════════════════════
  Work Transfer: helper-backend -> helper-backend-v2
═══════════════════════════════════════════════════════════════

  From Agent:     helper-backend
  To Agent:       helper-backend-v2
  Handoff File:   /Users/dev/handoffs/backend-transfer.md
  Priority:       high

  Steps:
    ✓ Source agent validated
    ✓ Target agent validated (status: online)
    ✓ Handoff file read (2.4 KB)
    ✓ Transfer message sent (msg-id: abc123)
    ✓ Orchestrator notified

═══════════════════════════════════════════════════════════════
  TRANSFER COMPLETE
  Message ID: abc123
═══════════════════════════════════════════════════════════════
```

## JSON Output

Use `--format json` for structured output:

```json
{
  "status": "success",
  "transfer": {
    "from": "helper-backend",
    "to": "helper-backend-v2",
    "handoff_file": "/Users/dev/handoffs/backend-transfer.md",
    "priority": "high",
    "message_id": "abc123",
    "timestamp": "2024-01-15T10:30:00Z"
  },
  "notifications": {
    "target_agent": true,
    "orchestrator": true
  }
}
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Source agent not found" | Invalid from agent | Check agent name with `/ecos-staff-status` |
| "Target agent not found" | Invalid to agent | Check agent name with `/ecos-staff-status` |
| "Target agent offline" | Agent not running | Wake agent with `/ecos-wake-agent` first |
| "Handoff file not found" | Invalid path | Verify file path exists |
| "Message send failed" | AI Maestro error | Check API is running |

## Use Cases

| Scenario | When to Use |
|----------|-------------|
| **Load Balancing** | Transfer part of work to less busy agent |
| **Specialization** | Move task to agent with specific expertise |
| **Shift Handoff** | End-of-day handoff to overnight agent |
| **Partial Recovery** | Transfer work before terminating degraded agent |
| **Collaboration** | Share context between collaborating agents |

## Related Commands

- `/ecos-replace-agent` - Full replacement workflow (includes transfer)
- `/ecos-spawn-agent` - Create new agent to receive work
- `/ecos-staff-status` - Check agent availability before transfer
- `/ecos-health-check` - Verify target agent health

## CLI Reference

Full documentation: `ai-maestro-agents-management` skill
