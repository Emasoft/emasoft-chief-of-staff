---
name: ecos-hibernate-agent
description: "Put a remote agent to sleep, preserving its state for later resumption using AI Maestro CLI"
argument-hint: "<AGENT_NAME>"
allowed-tools: ["Bash(aimaestro-agent.sh:*)"]
user-invocable: true
---

# Hibernate Agent Command

Put a remote agent to sleep, preserving its state for later resumption using the AI Maestro CLI.

## Usage

```!
aimaestro-agent.sh hibernate $ARGUMENTS
```

## AI Maestro CLI Integration

This command uses the **aimaestro-agent.sh** CLI tool for agent hibernation. The CLI:
1. Saves the agent state
2. Kills the tmux session (frees system resources)
3. Updates the agent registry status to `hibernated`
4. Agent can be woken later with full context preserved

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `AGENT_NAME` | Yes | Agent name or ID to hibernate |

## Examples

```bash
# Hibernate an agent
/ecos-hibernate-agent helper-python

# Hibernate multiple agents at end of day
/ecos-hibernate-agent frontend-ui
/ecos-hibernate-agent data-processor
```

## Hibernation vs Termination

| Aspect | Hibernate | Terminate |
|--------|-----------|-----------|
| State preserved | Yes | No |
| Can resume | Yes | No |
| Resource usage | Minimal (state file only) | None |
| Registry status | `hibernated` | Removed |
| Use case | Temporary pause | Permanent shutdown |

**Use hibernation when:**
- Agent not needed for a while but will be needed later
- Conserving system resources during low-activity periods
- Pausing work temporarily (e.g., end of day, lunch break)

## Hibernation Flow

```
1. aimaestro-agent.sh hibernate <agent>
   |
2. Agent state saved to storage
   |
3. tmux session terminated (resources freed)
   |
4. Registry updated: status = hibernated
   |
5. ✓ Agent hibernated successfully
```

## State Preservation

When hibernated, AI Maestro preserves:
- Agent configuration and metadata
- Working directory association
- Task description and tags
- Session context for resumption

## Output Format

```
═══════════════════════════════════════════════════════════════
  Hibernating Agent: helper-python
═══════════════════════════════════════════════════════════════

  ✓ Agent state saved
  ✓ tmux session terminated
  ✓ Registry updated: status = hibernated

═══════════════════════════════════════════════════════════════
  Agent 'helper-python' is now HIBERNATED

  Wake with: aimaestro-agent.sh wake helper-python
═══════════════════════════════════════════════════════════════
```

## View Hibernated Agents

```bash
# List all agents including hibernated
aimaestro-agent.sh list --status all

# List only hibernated agents
aimaestro-agent.sh list --status hibernated
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Agent not found" | Agent doesn't exist | Check name with `/ecos-staff-status` |
| "Agent is already hibernated" | State check failed | Agent already sleeping |
| "Agent is not online" | Cannot hibernate offline agent | Check agent status first |

## Related Commands

- `/ecos-staff-status` - View all remote agents
- `/ecos-wake-agent` - Wake a hibernated agent
- `/ecos-terminate-agent` - Permanently terminate an agent
- `/ecos-spawn-agent` - Create a new remote agent

## CLI Reference

Full documentation: `ai-maestro-agents-management` skill or run `aimaestro-agent.sh hibernate --help`
