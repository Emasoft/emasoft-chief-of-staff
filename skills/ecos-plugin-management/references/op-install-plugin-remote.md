---
operation: install-plugin-remote
procedure: proc-create-team
workflow-instruction: Step 4 - Team Creation
parent-skill: ecos-plugin-management
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Install Plugin on Remote Agent

## When to Use

- Adding plugins to agents running in other tmux sessions
- Deploying new capabilities to existing team members
- Updating plugins across multiple agents
- Setting up new agents with required plugins

## Prerequisites

- `aimaestro-agent.sh` CLI is available in PATH
- Target agent is running and registered in AI Maestro
- Marketplace is accessible (for marketplace installs)
- AI Maestro is running locally at `http://localhost:23000`

## Procedure

### Step 1: Verify Target Agent Exists

```bash
# List available agents
aimaestro-agent.sh list

# Check target agent status
aimaestro-agent.sh status <agent-session-name>
# Expected: running or hibernated
```

### Step 2: Add Marketplace to Remote Agent (If Needed)

```bash
# Add marketplace (auto-restarts agent)
aimaestro-agent.sh plugin marketplace add <agent-session-name> github:Emasoft/emasoft-plugins
```

### Step 3: Install Plugin

```bash
# Install plugin from marketplace (auto-restarts agent)
aimaestro-agent.sh plugin install <agent-session-name> <plugin-name>

# Example
aimaestro-agent.sh plugin install dev-backend-alice perfect-skill-suggester
```

**Note**: Remote installs automatically trigger agent restart.

### Step 4: Verify Installation

```bash
# List plugins on remote agent
aimaestro-agent.sh plugin list <agent-session-name>

# Check specific plugin
aimaestro-agent.sh plugin list <agent-session-name> | grep <plugin-name>
```

### Step 5: Send Notification (Optional)

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "<agent-session-name>",
    "subject": "Plugin Installed",
    "priority": "normal",
    "content": {
      "type": "team-notification",
      "message": "Plugin <plugin-name> has been installed. New capabilities are now available."
    }
  }'
```

## Checklist

Copy this checklist and track your progress:

- [ ] Verify target agent exists and is accessible
- [ ] Check agent status (running/hibernated)
- [ ] Add marketplace if not already registered
- [ ] Execute plugin install command
- [ ] Wait for automatic agent restart
- [ ] Verify plugin appears in list
- [ ] Send notification to agent
- [ ] Test new capabilities work

## Examples

### Example: Installing Plugin on Multiple Agents

```bash
# List of agents to update
AGENTS="dev-backend-alice dev-frontend-bob dev-api-charlie"
PLUGIN="perfect-skill-suggester"

for AGENT in $AGENTS; do
  echo "Installing $PLUGIN on $AGENT..."

  # Install (auto-restarts)
  aimaestro-agent.sh plugin install $AGENT $PLUGIN

  # Wait for restart to complete
  sleep 5

  # Verify
  aimaestro-agent.sh plugin list $AGENT | grep $PLUGIN

  # Notify
  curl -X POST "http://localhost:23000/api/messages" \
    -H "Content-Type: application/json" \
    -d '{
      "from": "ecos-chief-of-staff",
      "to": "'"$AGENT"'",
      "subject": "Plugin Update",
      "priority": "normal",
      "content": {"type": "team-notification", "message": "Plugin '"$PLUGIN"' installed."}
    }'
done
```

### Example: Remote Marketplace Management

```bash
SESSION_NAME="dev-backend-alice"

# List marketplaces on remote agent
aimaestro-agent.sh plugin marketplace list $SESSION_NAME

# Add marketplace
aimaestro-agent.sh plugin marketplace add $SESSION_NAME github:Emasoft/emasoft-plugins

# Update marketplace cache
aimaestro-agent.sh plugin marketplace update $SESSION_NAME

# Remove marketplace
aimaestro-agent.sh plugin marketplace remove $SESSION_NAME old-marketplace
```

### Example: Remote Plugin Operations

```bash
SESSION_NAME="dev-backend-alice"

# List all plugins
aimaestro-agent.sh plugin list $SESSION_NAME

# Enable a disabled plugin
aimaestro-agent.sh plugin enable $SESSION_NAME my-plugin

# Disable a plugin
aimaestro-agent.sh plugin disable $SESSION_NAME my-plugin

# Uninstall a plugin
aimaestro-agent.sh plugin uninstall $SESSION_NAME old-plugin

# Clean plugin cache (fix corruption)
aimaestro-agent.sh plugin clean $SESSION_NAME --dry-run  # Preview
aimaestro-agent.sh plugin clean $SESSION_NAME            # Execute

# Reinstall (fix corrupted install)
aimaestro-agent.sh plugin reinstall $SESSION_NAME my-plugin
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Agent not found | Wrong session name | Check `aimaestro-agent.sh list` for correct name |
| Agent not responding | Session crashed | Restart with `aimaestro-agent.sh restart <name>` |
| Marketplace add fails | Network issue | Check connectivity, retry |
| Plugin install fails | Plugin not in marketplace | Verify plugin name, update marketplace cache |
| Auto-restart fails | Claude Code issue | Manual restart: `aimaestro-agent.sh restart <name>` |
| Plugin not appearing | Cache issue | Run `aimaestro-agent.sh plugin clean <name>` then reinstall |

## Related Operations

- [op-install-plugin-marketplace.md](op-install-plugin-marketplace.md) - Local marketplace install
- [op-restart-agent-plugin.md](op-restart-agent-plugin.md) - Restart agent after changes
- [op-validate-plugin.md](op-validate-plugin.md) - Validate before install
