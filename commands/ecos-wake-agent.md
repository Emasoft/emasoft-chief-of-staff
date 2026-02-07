---
name: ecos-wake-agent
description: "Wake a hibernated agent, restoring its previous state using AI Maestro CLI"
argument-hint: "<AGENT_NAME> [--attach]"
allowed-tools: ["Bash(aimaestro-agent.sh:*)", "Task"]
user-invocable: true
---

# Wake Agent Command

Wake a hibernated agent, restoring its previous state using the AI Maestro CLI.

## Usage

Use the `ai-maestro-agents-management` skill to wake the agent with the provided arguments.

## What This Command Does

This command wakes a hibernated agent session. The operation:
1. Retrieves agent state from storage
2. Creates a new tmux session
3. Launches Claude Code with restored context
4. Updates the agent registry status to `online`

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `AGENT_NAME` | Yes | Agent name or ID to wake |
| `--attach` | No | Attach to the tmux session after waking |

## Required Claude Code Arguments

**Note**: When waking agents, the standard Claude Code arguments should be passed automatically. If the agent doesn't start correctly, ensure these arguments are configured:

| Argument | Purpose |
|----------|---------|
| `continue` | Resume previous session context |
| `--dangerously-skip-permissions` | Skip permission dialogs for automation |
| `--chrome` | Enable Chrome DevTools integration |
| `--add-dir <TEMP_DIR>` | Add temp directory access |

**Platform-specific temp directories:**
- **macOS/Linux**: `/tmp`
- **Windows**: `%TEMP%` or `C:\Users\<user>\AppData\Local\Temp`

## Examples

```bash
# Wake a hibernated agent
/ecos-wake-agent helper-python

# Wake and immediately attach to the session
/ecos-wake-agent helper-python --attach

# Wake multiple agents at start of day
/ecos-wake-agent frontend-ui
/ecos-wake-agent data-processor
```

## Wake Flow

```
1. Wake command issued for <agent>
   |
2. Agent state retrieved from storage
   |
3. tmux session created
   |
4. Claude Code launched in session
   |
5. Registry updated: status = online
   |
6. Agent is now ONLINE
   |
7. (Optional) Attach to session with --attach
```

## State Restoration

When woken, the agent:
- Resumes in its configured working directory
- Retains task description and tags
- Is ready to receive new instructions
- Can continue previous work context

## Output Format

```
═══════════════════════════════════════════════════════════════
  Waking Agent: helper-python
═══════════════════════════════════════════════════════════════

  ✓ Agent state retrieved
  ✓ tmux session created: helper-python
  ✓ Claude Code launched
  ✓ Registry updated: status = online

═══════════════════════════════════════════════════════════════
  Agent 'helper-python' is now ONLINE

  Attach with: tmux attach -t helper-python
═══════════════════════════════════════════════════════════════
```

## When to Use Wake vs Spawn

| Scenario | Use Wake | Use Spawn |
|----------|----------|-----------|
| Resume hibernated agent | ✓ | |
| Create brand new agent | | ✓ |
| Agent was terminated | | ✓ |
| After end-of-day hibernate | ✓ | |
| Different project/role needed | | ✓ |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Agent not found" | Agent doesn't exist | Check name with `/ecos-staff-status` |
| "Agent is not hibernated" | Agent is online or offline | Check current status |
| "Failed to create session" | tmux issue | Check tmux is running |

## Restart Agent (After Plugin Install)

After installing plugins or marketplaces, use the `ai-maestro-agents-management` skill to restart the agent. A restart is equivalent to hibernate followed by wake, which auto-applies plugin changes.

## Related Commands

- `/ecos-staff-status` - View all remote agents
- `/ecos-hibernate-agent` - Put an agent to sleep
- `/ecos-spawn-agent` - Create a new remote agent
- `/ecos-terminate-agent` - Permanently terminate an agent

## CLI Reference

Full documentation: `ai-maestro-agents-management` skill
