---
name: ecos-terminate-agent
description: "Terminate a remote agent and clean up its session using AI Maestro CLI"
argument-hint: "<AGENT_NAME> --confirm [--keep-folder]"
allowed-tools: ["Bash", "Task"]
user-invocable: true
---

# Terminate Agent Command

Terminate a remote agent and clean up its tmux session using the AI Maestro CLI.

## Usage

Use the `ai-maestro-agents-management` skill to terminate (delete) the agent with the provided arguments.

## What This Command Does

This command terminates an agent session. The operation:
1. Validates the agent exists
2. Kills the tmux session if running
3. Removes the agent from the agent registry
4. (Future: Optionally preserves project folder)

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `AGENT_NAME` | Yes | Agent name or ID to terminate |
| `--confirm` | **Yes** | Required confirmation flag (non-interactive) |
| `--keep-folder` | No | Don't delete the project folder (reserved for future API support) |
| `--keep-data` | No | Don't delete agent data in registry (reserved for future API support) |

## Examples

```bash
# Terminate an agent (requires --confirm)
/ecos-terminate-agent helper-python --confirm

# Terminate but keep project folder (when API supports it)
/ecos-terminate-agent old-project --confirm --keep-folder
```

## Termination vs Hibernation

| Aspect | Terminate | Hibernate |
|--------|-----------|-----------|
| State preserved | No | Yes |
| Can resume | No | Yes |
| Resource usage | None | Minimal |
| Registry entry | Removed | Updated to hibernated |
| Use case | Permanent shutdown | Temporary pause |

**IMPORTANT**: Use `/ecos-hibernate-agent` instead if you may need the agent again later!

## Termination Flow

```
1. Validate agent exists in registry
   |
2. Kill tmux session if running
   |
3. Remove agent from AI Maestro registry
   |
4. (Future: Delete or preserve project folder)
   |
5. ✓ Agent terminated
```

## Output Format

```
═══════════════════════════════════════════════════════════════
  Deleting Agent: helper-python
═══════════════════════════════════════════════════════════════

  ✓ Agent validated: helper-python
  ✓ tmux session killed
  ✓ Agent removed from registry

═══════════════════════════════════════════════════════════════
  Agent 'helper-python' has been DELETED
═══════════════════════════════════════════════════════════════
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Agent not found" | Agent doesn't exist | Check name with `/ecos-staff-status` |
| "Missing --confirm flag" | Safety check | Add `--confirm` to command |
| "Agent is hibernated" | Cannot delete hibernated | Wake agent first, then delete |

## Pre-Termination Checklist

Before terminating an agent:

1. **Verify work is complete** - Check agent has no pending tasks
2. **Backup important state** - Use the `ai-maestro-agents-management` skill to export agent state if needed
3. **Consider hibernating** - If you might need the agent again. Use the `ai-maestro-agents-management` skill to export agent state if needed.

## Related Commands

- `/ecos-staff-status` - View all remote agents
- `/ecos-spawn-agent` - Create a new remote agent
- `/ecos-hibernate-agent` - Put an agent to sleep (preserves state)
- `/ecos-wake-agent` - Wake a hibernated agent

## CLI Reference

Full documentation: `ai-maestro-agents-management` skill
