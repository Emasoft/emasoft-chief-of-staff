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
- AI Maestro is running locally at `http://localhost:23000`
- `aimaestro-agent.sh` CLI is available in PATH
- Team registry is accessible

## Procedure

### Step 1: Verify Work Is Complete

Before terminating, confirm the agent has no pending work:

```bash
# Send status request
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "<agent-session-name>",
    "subject": "Pre-Termination Status Check",
    "priority": "high",
    "content": {"type": "status-request", "message": "Please confirm all tasks are complete before termination."}
  }'
```

Wait for confirmation response.

### Step 2: Save Final State (Optional but Recommended)

If state preservation is needed for audit or handoff:

```bash
# Request state dump
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "<agent-session-name>",
    "subject": "State Dump Request",
    "priority": "high",
    "content": {"type": "request", "message": "Please save your current state to ~/.emasoft/agent-states/<session-name>-final.json before termination."}
  }'
```

### Step 3: Send Termination Warning

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "<agent-session-name>",
    "subject": "Termination Notice",
    "priority": "urgent",
    "content": {"type": "hibernation-warning", "message": "You will be terminated in 60 seconds. Please complete any final cleanup."}
  }'
```

### Step 4: Execute Termination

```bash
# Graceful termination (recommended)
aimaestro-agent.sh delete <agent-session-name> --confirm

# Force termination (if graceful fails)
aimaestro-agent.sh delete <agent-session-name> --confirm --force
```

### Step 5: Update Team Registry

```bash
uv run python scripts/ecos_team_registry.py remove-agent \
  --name "<agent-session-name>"
```

### Step 6: Cleanup Resources

```bash
# Remove agent working directory (optional - keep for audit)
# rm -rf ~/agents/<agent-session-name>

# Remove agent from plugin cache (optional)
# rm -rf ~/agents/<agent-session-name>/.claude
```

### Step 7: Log Termination

Document the termination in the team registry log:

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
- [ ] Execute termination command with --confirm
- [ ] Verify agent status is "terminated" or session gone
- [ ] Update team registry to remove agent
- [ ] Log termination event
- [ ] Notify relevant teammates if needed

## Examples

### Example: Terminating a Completed Developer Agent

```bash
SESSION_NAME="dev-backend-alice"

# Step 1: Request status
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "'"$SESSION_NAME"'",
    "subject": "Pre-Termination Status Check",
    "priority": "high",
    "content": {"type": "status-request", "message": "Please confirm all tasks are complete."}
  }'

# Wait for response...

# Step 2: Send warning
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "'"$SESSION_NAME"'",
    "subject": "Termination Notice",
    "priority": "urgent",
    "content": {"type": "hibernation-warning", "message": "Termination in 60 seconds."}
  }'

# Wait 60 seconds...
sleep 60

# Step 3: Execute
aimaestro-agent.sh delete $SESSION_NAME --confirm

# Step 4: Update registry
uv run python scripts/ecos_team_registry.py remove-agent --name "$SESSION_NAME"

# Step 5: Log
uv run python scripts/ecos_team_registry.py log \
  --event "termination" \
  --agent "$SESSION_NAME" \
  --reason "Task completed - backend API implementation finished" \
  --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Agent not responding to status check | Agent hung or crashed | Proceed with forced termination using --force |
| Termination command fails | tmux session stuck | Kill tmux session manually: `tmux kill-session -t <name>` |
| Agent still appears in registry | Registry not updated | Manually remove entry or run remove-agent again |
| Work not complete | Premature termination request | Delay termination, assign work to another agent |
| Cannot find agent session | Wrong session name | Check `aimaestro-agent.sh list` for correct name |

## Related Operations

- [op-spawn-agent.md](op-spawn-agent.md) - Spawn new agent
- [op-hibernate-agent.md](op-hibernate-agent.md) - Hibernate instead of terminate
- [op-update-team-registry.md](op-update-team-registry.md) - Update registry
