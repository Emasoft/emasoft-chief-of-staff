---
operation: restart-agent-plugin
procedure: proc-create-team
workflow-instruction: Step 4 - Team Creation
parent-skill: ecos-plugin-management
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Restart Agent After Plugin Changes

## When to Use

- After installing a plugin locally (self-install)
- When plugin changes are not taking effect
- After plugin update or version change
- When hooks stop firing unexpectedly
- To apply plugin configuration changes

## Prerequisites

- Agent session is accessible
- `aimaestro-agent.sh` CLI available (for remote agents)
- Claude Code CLI available (for local agent)

## Procedure

### For Local Agent (Self)

Claude Code caches plugin state in memory. You MUST exit and relaunch.

```bash
# Step 1: Exit current session
exit

# Step 2: Relaunch Claude Code
claude

# Or with specific plugin
claude --plugin-dir /path/to/my-plugin
```

### For Remote Agents

Use aimaestro-agent.sh for remote restarts.

#### Step 1: Send Pre-Restart Warning

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "<agent-session-name>",
    "subject": "Restart Warning",
    "priority": "urgent",
    "content": {
      "type": "hibernation-warning",
      "message": "Agent will restart in 30 seconds for plugin changes. Please save current state."
    }
  }'
```

#### Step 2: Wait for Acknowledgment

```bash
sleep 30
```

#### Step 3: Execute Restart

```bash
# Standard restart
aimaestro-agent.sh restart <agent-session-name>

# With longer wait time (slow systems)
aimaestro-agent.sh restart <agent-session-name> --wait 5
```

#### Step 4: Verify Agent Resumed

```bash
# Check status
aimaestro-agent.sh status <agent-session-name>
# Expected: running

# Send confirmation request
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "<agent-session-name>",
    "subject": "Restart Complete",
    "priority": "high",
    "content": {
      "type": "status-request",
      "message": "Restart complete. Please confirm you are operational and new plugins are loaded."
    }
  }'
```

#### Step 5: Update Registry Status

```bash
uv run python scripts/ecos_team_registry.py log \
  --event "restart" \
  --agent "<agent-session-name>" \
  --reason "Plugin changes applied" \
  --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

## Checklist

Copy this checklist and track your progress:

**For Local Agent:**
- [ ] Save any important state
- [ ] Exit Claude Code session
- [ ] Relaunch Claude Code with correct flags
- [ ] Verify hooks are registered
- [ ] Test plugin functionality

**For Remote Agent:**
- [ ] Send restart warning message
- [ ] Wait for acknowledgment (or timeout)
- [ ] Execute restart command
- [ ] Wait for agent to come back online
- [ ] Verify status is "running"
- [ ] Send confirmation request
- [ ] Log restart event in registry

## Examples

### Example: Restarting Self After Plugin Install

```bash
# You just ran: claude plugin install my-plugin@marketplace
# Now you must restart

# Save your work, then:
exit

# Relaunch
claude

# Verify new plugin loaded
/hooks
# Should show new hooks from my-plugin
```

### Example: Restarting Remote Agent

```bash
SESSION_NAME="dev-backend-alice"

# Warning
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "'"$SESSION_NAME"'",
    "subject": "Restart in 30s",
    "priority": "urgent",
    "content": {"type": "hibernation-warning", "message": "Restarting for plugin update."}
  }'

# Wait
sleep 30

# Restart
aimaestro-agent.sh restart $SESSION_NAME

# Wait for restart
sleep 5

# Verify
aimaestro-agent.sh status $SESSION_NAME
# Output: running

# Confirm
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "'"$SESSION_NAME"'",
    "subject": "Restart Complete",
    "priority": "high",
    "content": {"type": "status-request", "message": "Please confirm new plugins loaded."}
  }'
```

### Example: Batch Restart Multiple Agents

```bash
AGENTS="dev-backend-alice dev-frontend-bob"

# Send warnings
for AGENT in $AGENTS; do
  curl -X POST "http://localhost:23000/api/messages" \
    -H "Content-Type: application/json" \
    -d '{
      "from": "ecos-chief-of-staff",
      "to": "'"$AGENT"'",
      "subject": "Batch Restart",
      "priority": "urgent",
      "content": {"type": "hibernation-warning", "message": "Batch restart for plugin updates in 30s."}
    }'
done

# Wait
sleep 30

# Restart all
for AGENT in $AGENTS; do
  aimaestro-agent.sh restart $AGENT
  echo "Restarted $AGENT"
done

# Wait for all to come back
sleep 10

# Verify all
for AGENT in $AGENTS; do
  STATUS=$(aimaestro-agent.sh status $AGENT)
  echo "$AGENT: $STATUS"
done
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Agent not responding after restart | Restart failed | Check tmux session, retry restart |
| Status not "running" | Claude Code crashed | Check logs, try `aimaestro-agent.sh restart --force` |
| Old plugins still loaded | Cache issue | Clear plugin cache before restart |
| New hooks not appearing | Plugin not properly installed | Verify plugin installation before restart |
| Restart hangs | Long-running task interrupted | Use `--force` flag if needed |
| Agent lost context | Normal behavior | Send context restoration message |

## Related Operations

- [op-install-plugin-marketplace.md](op-install-plugin-marketplace.md) - Install before restart
- [op-install-plugin-remote.md](op-install-plugin-remote.md) - Remote install (auto-restarts)
- [op-validate-plugin.md](op-validate-plugin.md) - Validate before restart
