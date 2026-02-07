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
- AI Maestro is running locally at `http://localhost:23000`
- `aimaestro-agent.sh` CLI is available in PATH
- State storage directory is writable (`~/.emasoft/agent-states/`)
- Team registry is accessible

## Procedure

### Step 1: Confirm Agent Is Idle

Verify the agent has no active work before hibernating:

```bash
# Send idle check
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "<agent-session-name>",
    "subject": "Idle Status Check",
    "priority": "normal",
    "content": {"type": "status-request", "message": "Are you currently working on any active tasks? Reply with IDLE if no active work."}
  }'
```

Wait for IDLE confirmation.

### Step 2: Send Hibernation Warning

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "<agent-session-name>",
    "subject": "Hibernation Notice",
    "priority": "high",
    "content": {"type": "hibernation-warning", "message": "You will be hibernated in 30 seconds. Please save any transient state."}
  }'
```

### Step 3: Request State Capture

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "<agent-session-name>",
    "subject": "State Capture Request",
    "priority": "high",
    "content": {"type": "request", "message": "Save your current state to ~/.emasoft/agent-states/<session-name>-hibernation.json"}
  }'
```

### Step 4: Execute Hibernation

```bash
aimaestro-agent.sh hibernate <agent-session-name>
```

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
- [ ] Send hibernation warning (30 second notice)
- [ ] Request state capture from agent
- [ ] Wait for state capture confirmation
- [ ] Execute hibernation command
- [ ] Verify agent status changed to "hibernated"
- [ ] Update team registry status
- [ ] Log hibernation event with timestamp
- [ ] Note expected wake time if scheduled

## Examples

### Example: Hibernating Idle Developer at End of Day

```bash
SESSION_NAME="dev-frontend-bob"

# Step 1: Check idle status
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "'"$SESSION_NAME"'",
    "subject": "Idle Status Check",
    "priority": "normal",
    "content": {"type": "status-request", "message": "Are you currently working on any active tasks?"}
  }'

# Wait for IDLE response...

# Step 2: Send warning
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "'"$SESSION_NAME"'",
    "subject": "Hibernation Notice",
    "priority": "high",
    "content": {"type": "hibernation-warning", "message": "End of day hibernation in 30 seconds."}
  }'

sleep 30

# Step 3: Hibernate
aimaestro-agent.sh hibernate $SESSION_NAME

# Step 4: Update registry
uv run python scripts/ecos_team_registry.py update-status \
  --name "$SESSION_NAME" \
  --status "hibernated" \
  --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Step 5: Log
uv run python scripts/ecos_team_registry.py log \
  --event "hibernation" \
  --agent "$SESSION_NAME" \
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
