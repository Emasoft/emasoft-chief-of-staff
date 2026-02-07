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

- The `ai-maestro-agents-management` skill is available
- Target agent is running and registered in AI Maestro
- Marketplace is accessible (for marketplace installs)
- AI Maestro is running locally

## Procedure

### Step 1: Verify Target Agent Exists

Use the `ai-maestro-agents-management` skill to list available agents and check the target agent's status.

**Verify**: the target agent exists and is in a running or hibernated state.

### Step 2: Add Marketplace to Remote Agent (If Needed)

Use the `ai-maestro-agents-management` skill to add a marketplace to the target agent (e.g., `github:Emasoft/emasoft-plugins`).

**Note**: This auto-restarts the agent.

### Step 3: Install Plugin

Use the `ai-maestro-agents-management` skill to install the plugin on the target agent.

**Note**: Remote installs automatically trigger agent restart.

### Step 4: Verify Installation

Use the `ai-maestro-agents-management` skill to list plugins on the target agent and verify the new plugin appears.

### Step 5: Send Notification (Optional)

Use the `agent-messaging` skill to notify the target agent:
- **Recipient**: the target agent session name
- **Subject**: `Plugin Installed`
- **Priority**: `normal`
- **Content**: type `team-notification`, informing the agent that the plugin has been installed and new capabilities are available

**Verify**: confirm message delivery.

## Checklist

Copy this checklist and track your progress:

- [ ] Verify target agent exists and is accessible
- [ ] Check agent status (running/hibernated)
- [ ] Add marketplace if not already registered
- [ ] Execute plugin install
- [ ] Wait for automatic agent restart
- [ ] Verify plugin appears in list
- [ ] Send notification to agent
- [ ] Test new capabilities work

## Examples

### Example: Installing Plugin on Multiple Agents

For each target agent (`dev-backend-alice`, `dev-frontend-bob`, `dev-api-charlie`):

1. Use the `ai-maestro-agents-management` skill to install the plugin on the agent (auto-restarts)
2. Wait for restart to complete
3. Use the skill to list plugins on the agent and verify installation
4. Use the `agent-messaging` skill to notify the agent about the update

### Example: Remote Marketplace Management

Use the `ai-maestro-agents-management` skill for all marketplace operations on a remote agent:
- **List marketplaces** on the agent
- **Add marketplace** to the agent
- **Update marketplace cache** on the agent
- **Remove marketplace** from the agent

### Example: Remote Plugin Operations

Use the `ai-maestro-agents-management` skill for all plugin operations on a remote agent:
- **List all plugins** installed on the agent
- **Enable** a disabled plugin
- **Disable** a plugin without uninstalling
- **Uninstall** a plugin
- **Clean plugin cache** to fix corruption (preview first, then execute)
- **Reinstall** a corrupted plugin

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Agent not found | Wrong session name | Use the skill to list agents and find the correct name |
| Agent not responding | Session crashed | Use the skill to restart the agent |
| Marketplace add fails | Network issue | Check connectivity, retry |
| Plugin install fails | Plugin not in marketplace | Verify plugin name, update marketplace cache |
| Auto-restart fails | Claude Code issue | Use the skill to manually restart the agent |
| Plugin not appearing | Cache issue | Use the skill to clean plugin cache, then reinstall |

## Related Operations

- [op-install-plugin-marketplace.md](op-install-plugin-marketplace.md) - Local marketplace install
- [op-restart-agent-plugin.md](op-restart-agent-plugin.md) - Restart agent after changes
- [op-validate-plugin.md](op-validate-plugin.md) - Validate before install
