---
operation: terminate-agent
procedure: proc-create-team
workflow-instruction: Step 4 - Team Creation
parent-skill: ecos-agent-lifecycle
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Terminate Agent

## When to Use

- Agent task is complete and no further work expected
- Agent is no longer needed for the project
- Cleanup operations during project closure
- User explicitly requests agent termination
- Unrecoverable error condition requires agent replacement

## Prerequisites

- Agent exists and is registered in team registry
- AI Maestro is running locally
- The `ai-maestro-agents-management` skill is available
- The `agent-messaging` skill is available
- Team registry is accessible

## Procedure

### Step 1: Verify Work Is Complete

Before terminating, confirm the agent has no pending work.

Use the `agent-messaging` skill to send a status request:
- **Recipient**: the target agent session name
- **Subject**: `Pre-Termination Status Check`
- **Priority**: `high`
- **Content**: type `status-request`, asking the agent to confirm all tasks are complete before termination

Wait for confirmation response.

### Step 2: Save Final State (Optional but Recommended)

If state preservation is needed for audit or handoff:

Use the `agent-messaging` skill to request a state dump:
- **Recipient**: the target agent session name
- **Subject**: `State Dump Request`
- **Priority**: `high`
- **Content**: type `request`, asking the agent to save its current state to `~/.emasoft/agent-states/<session-name>-final.json` before termination

### Step 3: Send Termination Warning

Use the `agent-messaging` skill to send a termination notice:
- **Recipient**: the target agent session name
- **Subject**: `Termination Notice`
- **Priority**: `urgent`
- **Content**: type `hibernation-warning`, informing the agent it will be terminated in 60 seconds and should complete any final cleanup

### Step 4: Execute Termination

Use the `ai-maestro-agents-management` skill to terminate the agent with confirmation.

If graceful termination fails, use the force option if available.

### Step 5: Update Team Registry

```bash
uv run python scripts/ecos_team_registry.py remove-agent \
  --name "<agent-session-name>"
```

### Step 6: Cleanup Resources

Optionally remove the agent's working directory and local plugin cache. Keep the directory if audit trail is needed.

### Step 7: Log Termination

```bash
uv run python scripts/ecos_team_registry.py log \
  --event "termination" \
  --agent "<agent-session-name>" \
  --reason "<termination reason>" \
  --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

## Checklist

Copy this checklist and track your progress:

- [ ] Verify agent has no pending work
- [ ] Request status confirmation from agent
- [ ] Save final state if needed
- [ ] Send termination warning (60 second notice)
- [ ] Wait for agent acknowledgment or timeout
- [ ] Execute termination via `ai-maestro-agents-management` skill with confirmation
- [ ] Verify agent status is "terminated" or session gone
- [ ] Update team registry to remove agent
- [ ] Log termination event
- [ ] Notify relevant teammates if needed

## Examples

### Example: Terminating a Completed Developer Agent

For agent `dev-backend-alice`:

1. Use the `agent-messaging` skill to send a pre-termination status check:
   - **Recipient**: `dev-backend-alice`
   - **Subject**: `Pre-Termination Status Check`
   - **Priority**: `high`
   - **Content**: type `status-request`, message: "Please confirm all tasks are complete."
2. Wait for response confirming work is done
3. Use the `agent-messaging` skill to send a termination warning:
   - **Recipient**: `dev-backend-alice`
   - **Subject**: `Termination Notice`
   - **Priority**: `urgent`
   - **Content**: type `hibernation-warning`, message: "Termination in 60 seconds."
4. Wait 60 seconds
5. Use the `ai-maestro-agents-management` skill to terminate agent `dev-backend-alice` with confirmation
6. Update registry:
   ```bash
   uv run python scripts/ecos_team_registry.py remove-agent --name "dev-backend-alice"
   ```
7. Log the event:
   ```bash
   uv run python scripts/ecos_team_registry.py log \
     --event "termination" \
     --agent "dev-backend-alice" \
     --reason "Task completed - backend API implementation finished" \
     --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
   ```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Agent not responding to status check | Agent hung or crashed | Proceed with forced termination |
| Termination command fails | tmux session stuck | Kill tmux session manually: `tmux kill-session -t <name>` |
| Agent still appears in registry | Registry not updated | Manually remove entry or run remove-agent again |
| Work not complete | Premature termination request | Delay termination, assign work to another agent |
| Cannot find agent session | Wrong session name | Use the `ai-maestro-agents-management` skill to list agents for correct name |

## Related Operations

- [op-spawn-agent.md](op-spawn-agent.md) - Spawn new agent
- [op-hibernate-agent.md](op-hibernate-agent.md) - Hibernate instead of terminate
- [op-update-team-registry.md](op-update-team-registry.md) - Update registry
