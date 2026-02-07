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
- AI Maestro is running locally at `http://localhost:23000`
- `aimaestro-agent.sh` CLI is available in PATH
- Sufficient resources available (check concurrent agent limit)

## Procedure

### Step 1: Verify Agent Is Hibernated

```bash
# Check agent status in registry
uv run python scripts/ecos_team_registry.py list \
  --filter-name "<agent-session-name>" \
  --show-status

# Expected: status = "hibernated"

# Verify state file exists
ls -la ~/.emasoft/agent-states/<agent-session-name>-hibernation.json
```

### Step 2: Check Resource Availability

```bash
# Count currently running agents
RUNNING_COUNT=$(uv run python scripts/ecos_team_registry.py list --filter-status running --count)
MAX_AGENTS=5

if [ "$RUNNING_COUNT" -ge "$MAX_AGENTS" ]; then
  echo "WARNING: At max capacity. Hibernate another agent first."
  exit 1
fi
```

### Step 3: Execute Wake Command

```bash
aimaestro-agent.sh wake <agent-session-name>
```

This resumes the suspended tmux session.

### Step 4: Verify Agent Is Responsive

```bash
# Check status
aimaestro-agent.sh status <agent-session-name>
# Expected: running

# Send ping message
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "<agent-session-name>",
    "subject": "Wake Confirmation",
    "priority": "high",
    "content": {"type": "wake-notification", "message": "You have been woken from hibernation. Please confirm you are operational."}
  }'
```

Wait for confirmation response.

### Step 5: Restore State (If Needed)

If agent needs context restoration:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "<agent-session-name>",
    "subject": "State Restoration",
    "priority": "high",
    "content": {"type": "request", "message": "Restore your state from ~/.emasoft/agent-states/<session-name>-hibernation.json"}
  }'
```

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
- [ ] Execute wake command
- [ ] Verify agent status is "running"
- [ ] Send wake notification message
- [ ] Wait for agent confirmation response
- [ ] Request state restoration if needed
- [ ] Update team registry to "running"
- [ ] Log wake event with timestamp

## Examples

### Example: Waking Agent for Morning Work Session

```bash
SESSION_NAME="dev-frontend-bob"

# Step 1: Verify hibernated
uv run python scripts/ecos_team_registry.py list --filter-name "$SESSION_NAME" --show-status
# Output: dev-frontend-bob | hibernated | frontend | webapp

# Step 2: Check capacity
RUNNING=$(uv run python scripts/ecos_team_registry.py list --filter-status running --count)
echo "Currently running: $RUNNING / 5"

# Step 3: Wake
aimaestro-agent.sh wake $SESSION_NAME

# Step 4: Verify running
aimaestro-agent.sh status $SESSION_NAME
# Output: running

# Step 5: Send notification
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "'"$SESSION_NAME"'",
    "subject": "Good Morning - Wake Notification",
    "priority": "high",
    "content": {"type": "wake-notification", "message": "You have been woken for the morning work session. Please confirm operational and restore your previous context."}
  }'

# Step 6: Update registry
uv run python scripts/ecos_team_registry.py update-status \
  --name "$SESSION_NAME" \
  --status "running" \
  --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Step 7: Log
uv run python scripts/ecos_team_registry.py log \
  --event "wake" \
  --agent "$SESSION_NAME" \
  --reason "Morning work session start" \
  --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Agent not found in hibernated status | Agent was terminated or never hibernated | Spawn new agent instead |
| State file missing | Hibernation did not save state properly | Wake without state, agent starts fresh |
| Wake command fails | tmux session corrupted | Delete and respawn agent |
| Agent not responding after wake | Claude Code instance crashed | Restart agent with `aimaestro-agent.sh restart <name>` |
| Resource limit exceeded | Too many running agents | Hibernate another agent first |
| State restoration fails | Corrupt state file | Continue without state, log incident |

## Related Operations

- [op-hibernate-agent.md](op-hibernate-agent.md) - Hibernate agent
- [op-spawn-agent.md](op-spawn-agent.md) - Spawn new agent if wake fails
- [op-update-team-registry.md](op-update-team-registry.md) - Update registry
