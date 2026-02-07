---
name: ecos-recovery-workflow
description: "Execute recovery workflow for a failed or unhealthy agent with restart, hibernate-wake, or replace actions"
argument-hint: "--agent <NAME> --action [restart|hibernate-wake|replace] [--timeout <SECONDS>]"
allowed-tools: ["Bash(aimaestro-agent.sh:*)", "Task"]
user-invocable: true
---

# Recovery Workflow Command

Execute a recovery workflow for a failed, unresponsive, or degraded agent. Supports multiple recovery strategies based on the severity of the issue.

## Usage

```!
# Execute the specified recovery action for the agent
```

## Recovery Actions Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    RECOVERY STRATEGIES                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  RESTART (Level 1 - Mild Issues)                            │
│  └─> For: Temporary hangs, minor memory issues              │
│  └─> Action: Restart tmux session and Claude Code           │
│  └─> Risk: Low - preserves session context                  │
│                                                             │
│  HIBERNATE-WAKE (Level 2 - Moderate Issues)                 │
│  └─> For: Memory exhaustion, context corruption             │
│  └─> Action: Hibernate agent, then wake with fresh session  │
│  └─> Risk: Medium - clears session but preserves agent      │
│                                                             │
│  REPLACE (Level 3 - Severe Issues)                          │
│  └─> For: Unrecoverable failures, persistent crashes        │
│  └─> Action: Full agent replacement via /ecos-replace-agent │
│  └─> Risk: High - creates new agent, transfers work         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--agent <name>` | Yes | Name of the agent to recover |
| `--action <action>` | Yes | Recovery action: `restart`, `hibernate-wake`, `replace` |
| `--timeout <seconds>` | No | Wait timeout for recovery (default: 60) |
| `--verify` | No | Perform health check after recovery |
| `--force` | No | Force recovery even if agent appears healthy |
| `--new-name <name>` | No | New agent name (required for replace action) |
| `--reason <text>` | No | Reason for recovery (logged and reported) |

## Examples

```bash
# Simple restart for temporarily hung agent
/ecos-recovery-workflow --agent helper-backend --action restart

# Hibernate-wake for memory issues
/ecos-recovery-workflow --agent helper-backend --action hibernate-wake --verify

# Full replacement for unrecoverable failure
/ecos-recovery-workflow --agent helper-backend --action replace \
  --new-name helper-backend-v2 \
  --reason "Persistent context corruption"

# Force recovery with custom timeout
/ecos-recovery-workflow --agent slow-agent --action restart \
  --force --timeout 120 --verify
```

## Recovery Workflows in Detail

### Action: restart

**When to use**: Agent is unresponsive but likely recoverable. Session may be hung or experiencing temporary issues.

**Workflow**:
```
1. Check current agent status
2. Send SIGTERM to Claude Code process (graceful stop)
3. Wait for process to exit (up to timeout)
4. Restart tmux session with Claude Code
5. Verify agent is responsive (if --verify)
```

**Operations**: Use the `ai-maestro-agents-management` skill to:
1. Restart the agent's tmux session
2. Wait for the agent to come online (timeout: 60s)
3. Verify health (if `--verify`)

**Verify**: agent status shows "online" and health check reports "HEALTHY".

### Action: hibernate-wake

**When to use**: Agent has memory exhaustion, context corruption, or needs a fresh start while preserving registration.

**Workflow**:
```
1. Check current agent status
2. Hibernate the agent (saves state, stops session)
3. Wait for hibernate to complete
4. Wake the agent (fresh session)
5. Wait for agent to come online
6. Verify agent is responsive (if --verify)
```

**Operations**: Use the `ai-maestro-agents-management` skill to:
1. Hibernate the agent
2. Wait briefly for hibernation to complete
3. Wake the agent
4. Wait for the agent to come online (timeout: 60s)
5. Verify health (if `--verify`)

**Verify**: agent status shows "online" and health check reports "HEALTHY".

### Action: replace

**When to use**: Agent has unrecoverable failure, persistent crashes, or corruption that cannot be fixed with restart/hibernate.

**Workflow**:
```
1. Gather information about failed agent
2. Trigger /ecos-replace-agent workflow:
   - Request approval from EAMA
   - Create new agent
   - Generate handoff
   - Update kanban
   - Transfer work
   - Verify new agent
3. Optionally terminate old agent
```

**Triggers Task Tool**:
```
The replace action spawns a Task to execute /ecos-replace-agent
with parameters derived from the failed agent's metadata.
```

## Output Format

### Restart Output

```
═══════════════════════════════════════════════════════════════
  Recovery Workflow: helper-backend
  Action: RESTART
═══════════════════════════════════════════════════════════════

  Step 1: Check Current Status
    Agent Status:     unresponsive
    Last Heartbeat:   5 minutes ago
    Session:          helper-backend (exists)

  Step 2: Stop Agent
    ✓ Sent SIGTERM to process 12345
    ✓ Process terminated gracefully

  Step 3: Restart Session
    ✓ tmux session restarted
    ✓ Claude Code launched

  Step 4: Wait for Online
    ✓ Agent online after 8 seconds

  Step 5: Verify Health
    ✓ Health check: HEALTHY
    ✓ Response time: 45ms

═══════════════════════════════════════════════════════════════
  RECOVERY COMPLETE
  Agent 'helper-backend' is now operational
═══════════════════════════════════════════════════════════════
```

### Hibernate-Wake Output

```
═══════════════════════════════════════════════════════════════
  Recovery Workflow: helper-backend
  Action: HIBERNATE-WAKE
═══════════════════════════════════════════════════════════════

  Step 1: Check Current Status
    Agent Status:     degraded
    Last Heartbeat:   90 seconds ago
    Memory Usage:     95% (critical)

  Step 2: Hibernate Agent
    ✓ Session state saved
    ✓ tmux session detached
    ✓ Agent status: hibernated

  Step 3: Wake Agent
    ✓ Fresh tmux session created
    ✓ Claude Code launched with clean context

  Step 4: Wait for Online
    ✓ Agent online after 12 seconds

  Step 5: Verify Health
    ✓ Health check: HEALTHY
    ✓ Memory Usage: 12% (normal)
    ✓ Response time: 38ms

═══════════════════════════════════════════════════════════════
  RECOVERY COMPLETE
  Agent 'helper-backend' has been refreshed
═══════════════════════════════════════════════════════════════
```

### Replace Output

```
═══════════════════════════════════════════════════════════════
  Recovery Workflow: helper-backend
  Action: REPLACE
═══════════════════════════════════════════════════════════════

  Step 1: Gather Failed Agent Info
    Agent:           helper-backend
    Project:         myapp-api
    Role:            implementer
    Working Dir:     /Users/dev/projects/myapp

  Step 2: Trigger Replacement Workflow
    ✓ Spawning /ecos-replace-agent task

    Parameters:
      --failed-agent:  helper-backend
      --new-name:      helper-backend-v2
      --role:          implementer
      --project:       myapp-api
      --dir:           /Users/dev/projects/myapp
      --reason:        Persistent context corruption

  Step 3: Replacement Status
    ✓ Approval received
    ✓ New agent created
    ✓ Handoff generated
    ✓ Kanban updated
    ✓ Work transferred
    ✓ New agent verified

═══════════════════════════════════════════════════════════════
  RECOVERY COMPLETE
  Agent replaced: helper-backend -> helper-backend-v2
═══════════════════════════════════════════════════════════════
```

## Decision Guide: Which Action to Use

| Symptom | Recommended Action |
|---------|-------------------|
| Agent hangs occasionally | `restart` |
| High response latency | `restart` |
| Memory usage > 80% | `hibernate-wake` |
| Context seems corrupted | `hibernate-wake` |
| Repeated crashes after restart | `hibernate-wake` |
| Repeated crashes after hibernate-wake | `replace` |
| Data corruption in outputs | `replace` |
| Agent produces incorrect results | `replace` |
| Hardware/network issues | `restart` then escalate |

## Automated Recovery Escalation

For automated recovery, use escalation pattern:

```bash
# Try restart first
/ecos-recovery-workflow --agent helper-backend --action restart --verify

# If still unhealthy after restart, try hibernate-wake
# (Automated via ecos-recovery-monitor agent)

# If still unhealthy after hibernate-wake, trigger replace
# (Requires manual approval unless --skip-approval)
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Agent not found" | Invalid agent name | Check with `/ecos-staff-status` |
| "Restart failed" | Process won't terminate | Try `hibernate-wake` or `replace` |
| "Hibernate failed" | Session lock issue | Force restart tmux manually |
| "Wake timeout" | Agent won't start | Check logs, try `replace` |
| "Replace requires --new-name" | Missing argument | Provide `--new-name` for replace action |

## Related Commands

- `/ecos-health-check` - Check agent health before recovery
- `/ecos-replace-agent` - Full replacement workflow
- `/ecos-terminate-agent` - Terminate agent after replacement
- `/ecos-hibernate-agent` - Manual hibernate
- `/ecos-wake-agent` - Manual wake
- `/ecos-staff-status` - View all agent statuses

## CLI Reference

Full documentation: `ai-maestro-agents-management` skill
