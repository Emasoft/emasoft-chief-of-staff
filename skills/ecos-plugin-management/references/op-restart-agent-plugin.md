---
operation: restart-agent-plugin
procedure: proc-create-team
workflow-instruction: Step 4 - Team Creation
parent-skill: ecos-plugin-management
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Restart Agent After Plugin Changes


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [For Local Agent (Self)](#for-local-agent-self)
  - [For Remote Agents](#for-remote-agents)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Restarting Self After Plugin Install](#example-restarting-self-after-plugin-install)
  - [Example: Restarting Remote Agent](#example-restarting-remote-agent)
  - [Example: Batch Restart Multiple Agents](#example-batch-restart-multiple-agents)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

- After installing a plugin locally (self-install)
- When plugin changes are not taking effect
- After plugin update or version change
- When hooks stop firing unexpectedly
- To apply plugin configuration changes

## Prerequisites

- Agent session is accessible
- The `ai-maestro-agents-management` skill is available (for remote agents)
- Claude Code CLI available (for local agent)

## Procedure

### For Local Agent (Self)

Claude Code caches plugin state in memory. You MUST exit and relaunch.

1. Save any important state
2. Exit the current Claude Code session
3. Relaunch Claude Code (optionally with `--plugin-dir /path/to/my-plugin` for specific plugin loading)

### For Remote Agents

#### Step 1: Send Pre-Restart Warning

Use the `agent-messaging` skill to send a message:
- **Recipient**: the target agent session name
- **Subject**: `Restart Warning`
- **Priority**: `urgent`
- **Content**: type `hibernation-warning`, informing the agent it will restart in 30 seconds for plugin changes and should save current state

#### Step 2: Wait for Acknowledgment

Wait 30 seconds for the agent to save state.

#### Step 3: Execute Restart

Use the `ai-maestro-agents-management` skill to restart the target agent.

For slow systems, use a longer wait time option if available.

#### Step 4: Verify Agent Resumed

Use the `ai-maestro-agents-management` skill to check the agent's status. Expected status: running.

Then use the `agent-messaging` skill to send a confirmation request:
- **Recipient**: the target agent session name
- **Subject**: `Restart Complete`
- **Priority**: `high`
- **Content**: type `status-request`, asking the agent to confirm it is operational and new plugins are loaded

#### Step 5: Update Registry Status

Update the team registry log with the restart event:

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
- [ ] Execute restart via `ai-maestro-agents-management` skill
- [ ] Wait for agent to come back online
- [ ] Verify status is "running"
- [ ] Send confirmation request
- [ ] Log restart event in registry

## Examples

### Example: Restarting Self After Plugin Install

1. Install the plugin (e.g., via `claude plugin install my-plugin@marketplace`)
2. Save your work
3. Exit Claude Code
4. Relaunch Claude Code
5. Run `/hooks` to verify new hooks from the plugin are loaded

### Example: Restarting Remote Agent

For agent `dev-backend-alice`:

1. Use the `agent-messaging` skill to send a restart warning:
   - **Recipient**: `dev-backend-alice`
   - **Subject**: `Restart in 30s`
   - **Priority**: `urgent`
   - **Content**: type `hibernation-warning`, message: "Restarting for plugin update."
2. Wait 30 seconds
3. Use the `ai-maestro-agents-management` skill to restart agent `dev-backend-alice`
4. Wait for restart to complete
5. Use the `ai-maestro-agents-management` skill to check the agent's status (expected: running)
6. Use the `agent-messaging` skill to send a confirmation request:
   - **Recipient**: `dev-backend-alice`
   - **Subject**: `Restart Complete`
   - **Priority**: `high`
   - **Content**: type `status-request`, asking the agent to confirm new plugins loaded

### Example: Batch Restart Multiple Agents

For agents `dev-backend-alice` and `dev-frontend-bob`:

1. Use the `agent-messaging` skill to send restart warnings to each agent:
   - **Priority**: `urgent`
   - **Content**: type `hibernation-warning`, message: "Batch restart for plugin updates in 30s."
2. Wait 30 seconds
3. Use the `ai-maestro-agents-management` skill to restart each agent
4. Wait for all agents to come back online
5. Use the `ai-maestro-agents-management` skill to check each agent's status

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Agent not responding after restart | Restart failed | Check tmux session, retry restart via the skill |
| Status not "running" | Claude Code crashed | Check logs, try force restart via the skill |
| Old plugins still loaded | Cache issue | Clear plugin cache before restart |
| New hooks not appearing | Plugin not properly installed | Verify plugin installation before restart |
| Restart hangs | Long-running task interrupted | Use force option if available |
| Agent lost context | Normal behavior | Send context restoration message |

## Related Operations

- [op-install-plugin-marketplace.md](op-install-plugin-marketplace.md) - Install before restart
- [op-install-plugin-remote.md](op-install-plugin-remote.md) - Remote install (auto-restarts)
- [op-validate-plugin.md](op-validate-plugin.md) - Validate before restart
