---
operation: wake-agent
procedure: proc-create-team
workflow-instruction: Step 4 - Team Creation
parent-skill: ecos-agent-lifecycle
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Wake Hibernated Agent

## When to Use

- New work available for a hibernated agent
- Start of work day (scheduled wake)
- Resource availability allows resuming agents
- Urgent task requires previously hibernated capability
- User explicitly requests agent wake

## Prerequisites

- Agent exists in team registry with status "hibernated"
- Hibernation state file exists at `~/.emasoft/agent-states/<session-name>-hibernation.json`
- AI Maestro is running locally
- The `ai-maestro-agents-management` skill is available
- The `agent-messaging` skill is available
- Sufficient resources available (check concurrent agent limit)

## Procedure

### Step 1: Verify Agent Is Hibernated

Check the agent's status in the team registry:

```bash
uv run python scripts/ecos_team_registry.py list \
  --filter-name "<agent-session-name>" \
  --show-status
```

Expected: status = "hibernated"

Verify the state file exists at `~/.emasoft/agent-states/<agent-session-name>-hibernation.json`.

### Step 2: Check Resource Availability

```bash
RUNNING_COUNT=$(uv run python scripts/ecos_team_registry.py list --filter-status running --count)
MAX_AGENTS=5

if [ "$RUNNING_COUNT" -ge "$MAX_AGENTS" ]; then
  echo "WARNING: At max capacity. Hibernate another agent first."
  exit 1
fi
```

### Step 3: Execute Wake Command

Use the `ai-maestro-agents-management` skill to wake the hibernated agent.

This resumes the suspended tmux session.

### Step 4: Verify Agent Is Responsive

Use the `ai-maestro-agents-management` skill to check the agent's status. Expected status: running.

Then use the `agent-messaging` skill to send a wake notification:
- **Recipient**: the target agent session name
- **Subject**: `Wake Confirmation`
- **Priority**: `high`
- **Content**: type `wake-notification`, informing the agent it has been woken from hibernation and asking it to confirm it is operational

**Verify**: confirm message delivery via the `agent-messaging` skill's sent messages feature.

Wait for confirmation response.

### Step 5: Restore State (If Needed)

If the agent needs context restoration, use the `agent-messaging` skill to send a state restoration request:
- **Recipient**: the target agent session name
- **Subject**: `State Restoration`
- **Priority**: `high`
- **Content**: type `request`, asking the agent to restore its state from `~/.emasoft/agent-states/<session-name>-hibernation.json`

**Verify**: confirm message delivery via the `agent-messaging` skill's sent messages feature.

### Step 6: Update Team Registry

```bash
uv run python scripts/ecos_team_registry.py update-status \
  --name "<agent-session-name>" \
  --status "running" \
  --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

### Step 7: Log Wake Event

```bash
uv run python scripts/ecos_team_registry.py log \
  --event "wake" \
  --agent "<agent-session-name>" \
  --reason "<wake reason>" \
  --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

## Checklist

Copy this checklist and track your progress:

- [ ] Verify agent is in "hibernated" status
- [ ] Verify hibernation state file exists
- [ ] Check resource availability (running agent count)
- [ ] Execute wake via `ai-maestro-agents-management` skill
- [ ] Verify agent status is "running"
- [ ] Send wake notification via `agent-messaging` skill
- [ ] Wait for agent confirmation response
- [ ] Request state restoration if needed
- [ ] Update team registry to "running"
- [ ] Log wake event with timestamp

## Examples

### Example: Waking Agent for Morning Work Session

For agent `dev-frontend-bob`:

1. Verify hibernated status:
   ```bash
   uv run python scripts/ecos_team_registry.py list --filter-name "dev-frontend-bob" --show-status
   # Output: dev-frontend-bob | hibernated | frontend | webapp
   ```
2. Check capacity:
   ```bash
   RUNNING=$(uv run python scripts/ecos_team_registry.py list --filter-status running --count)
   echo "Currently running: $RUNNING / 5"
   ```
3. Use the `ai-maestro-agents-management` skill to wake agent `dev-frontend-bob`
4. Use the `ai-maestro-agents-management` skill to verify status is "running"
5. Use the `agent-messaging` skill to send a wake notification:
   - **Recipient**: `dev-frontend-bob`
   - **Subject**: `Good Morning - Wake Notification`
   - **Priority**: `high`
   - **Content**: type `wake-notification`, message: "You have been woken for the morning work session. Please confirm operational and restore your previous context."
6. Update registry:
   ```bash
   uv run python scripts/ecos_team_registry.py update-status \
     --name "dev-frontend-bob" \
     --status "running" \
     --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
   ```
7. Log the event:
   ```bash
   uv run python scripts/ecos_team_registry.py log \
     --event "wake" \
     --agent "dev-frontend-bob" \
     --reason "Morning work session start" \
     --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
   ```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Agent not found in hibernated status | Agent was terminated or never hibernated | Spawn new agent instead |
| State file missing | Hibernation did not save state properly | Wake without state, agent starts fresh |
| Wake command fails | tmux session corrupted | Delete and respawn agent |
| Agent not responding after wake | Claude Code instance crashed | Use the `ai-maestro-agents-management` skill to restart the agent |
| Resource limit exceeded | Too many running agents | Hibernate another agent first |
| State restoration fails | Corrupt state file | Continue without state, log incident |

## Related Operations

- [op-hibernate-agent.md](op-hibernate-agent.md) - Hibernate agent
- [op-spawn-agent.md](op-spawn-agent.md) - Spawn new agent if wake fails
- [op-update-team-registry.md](op-update-team-registry.md) - Update registry
