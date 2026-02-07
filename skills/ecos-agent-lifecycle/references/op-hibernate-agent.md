---
operation: hibernate-agent
procedure: proc-create-team
workflow-instruction: Step 4 - Team Creation
parent-skill: ecos-agent-lifecycle
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Hibernate Agent

## When to Use

- Agent is idle but may be needed later
- Conserving system resources during low-activity periods
- Scheduled pause (end of work day, weekends)
- Resource pressure requires reducing active agents
- Agent idle timeout threshold exceeded (default: 30 min)

## Prerequisites

- Agent exists and is in "running" state
- AI Maestro is running locally
- The `ai-maestro-agents-management` skill is available
- The `agent-messaging` skill is available
- State storage directory is writable (`~/.emasoft/agent-states/`)
- Team registry is accessible

## Procedure

### Step 1: Confirm Agent Is Idle

Verify the agent has no active work before hibernating.

Use the `agent-messaging` skill to send an idle check:
- **Recipient**: the target agent session name
- **Subject**: `Idle Status Check`
- **Priority**: `normal`
- **Content**: type `status-request`, asking the agent if it is currently working on any active tasks (reply with IDLE if no active work)

**Verify**: confirm message delivery via the `agent-messaging` skill's sent messages feature.

Wait for IDLE confirmation.

### Step 2: Send Hibernation Warning

Use the `agent-messaging` skill to send a hibernation notice:
- **Recipient**: the target agent session name
- **Subject**: `Hibernation Notice`
- **Priority**: `high`
- **Content**: type `hibernation-warning`, informing the agent it will be hibernated in 30 seconds and should save any transient state

**Verify**: confirm message delivery via the `agent-messaging` skill's sent messages feature.

### Step 3: Request State Capture

Use the `agent-messaging` skill to request state capture:
- **Recipient**: the target agent session name
- **Subject**: `State Capture Request`
- **Priority**: `high`
- **Content**: type `request`, asking the agent to save its current state to `~/.emasoft/agent-states/<session-name>-hibernation.json`

**Verify**: confirm message delivery via the `agent-messaging` skill's sent messages feature.

### Step 4: Execute Hibernation

Use the `ai-maestro-agents-management` skill to hibernate the agent.

This suspends the tmux session while preserving state.

### Step 5: Update Team Registry

```bash
uv run python scripts/ecos_team_registry.py update-status \
  --name "<agent-session-name>" \
  --status "hibernated" \
  --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

### Step 6: Log Hibernation Event

```bash
uv run python scripts/ecos_team_registry.py log \
  --event "hibernation" \
  --agent "<agent-session-name>" \
  --reason "<hibernation reason>" \
  --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

## Checklist

Copy this checklist and track your progress:

- [ ] Verify agent is idle (no active tasks)
- [ ] Send hibernation warning (30 second notice) via `agent-messaging` skill
- [ ] Request state capture from agent via `agent-messaging` skill
- [ ] Wait for state capture confirmation
- [ ] Execute hibernation via `ai-maestro-agents-management` skill
- [ ] Verify agent status changed to "hibernated"
- [ ] Update team registry status
- [ ] Log hibernation event with timestamp
- [ ] Note expected wake time if scheduled

## Examples

### Example: Hibernating Idle Developer at End of Day

For agent `dev-frontend-bob`:

1. Use the `agent-messaging` skill to check idle status:
   - **Recipient**: `dev-frontend-bob`
   - **Subject**: `Idle Status Check`
   - **Priority**: `normal`
   - **Content**: type `status-request`, message: "Are you currently working on any active tasks?"
2. Wait for IDLE response
3. Use the `agent-messaging` skill to send hibernation warning:
   - **Recipient**: `dev-frontend-bob`
   - **Subject**: `Hibernation Notice`
   - **Priority**: `high`
   - **Content**: type `hibernation-warning`, message: "End of day hibernation in 30 seconds."
4. Wait 30 seconds
5. Use the `ai-maestro-agents-management` skill to hibernate agent `dev-frontend-bob`
6. Update registry:
   ```bash
   uv run python scripts/ecos_team_registry.py update-status \
     --name "dev-frontend-bob" \
     --status "hibernated" \
     --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
   ```
7. Log the event:
   ```bash
   uv run python scripts/ecos_team_registry.py log \
     --event "hibernation" \
     --agent "dev-frontend-bob" \
     --reason "End of day - scheduled hibernation" \
     --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
   ```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Agent reports active work | Premature hibernation attempt | Wait for task completion or reassign task first |
| State capture failed | Storage full or permissions | Free space or fix permissions on ~/.emasoft/agent-states/ |
| Hibernation command fails | tmux session issue | Check tmux status, try manual session suspend |
| Agent not responding | Agent crashed or hung | Force hibernation, check logs for errors |
| Registry update fails | Registry locked or corrupt | Retry, or manually edit team-registry.json |

## Related Operations

- [op-wake-agent.md](op-wake-agent.md) - Wake hibernated agent
- [op-terminate-agent.md](op-terminate-agent.md) - Terminate instead of hibernate
- [op-update-team-registry.md](op-update-team-registry.md) - Update registry
