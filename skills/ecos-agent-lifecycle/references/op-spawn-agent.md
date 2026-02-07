---
operation: spawn-agent
procedure: proc-create-team
workflow-instruction: Step 4 - Team Creation
parent-skill: ecos-agent-lifecycle
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Spawn New Agent

## When to Use

- A new task requires an agent instance
- Scaling up for parallel work
- Specialized capability is needed that existing agents do not provide
- User requests creating a new team member

## Prerequisites

- AI Maestro is running locally
- The `ai-maestro-agents-management` skill is available
- The `agent-messaging` skill is available
- tmux is installed for session management
- Team registry location is writable (`.emasoft/team-registry.json`)
- Plugin for the agent role is installed in marketplace cache

## Procedure

### Step 1: Determine Agent Type and Session Name

Select the appropriate agent type based on the task requirements. ECOS chooses the unique session name.

**Session naming format:** `<role-prefix>-<project>-<descriptive>`

| Role | Prefix | Plugin | Main Agent |
|------|--------|--------|------------|
| Orchestrator | eoa | emasoft-orchestrator-agent | eoa-orchestrator-main-agent |
| Architect | eaa | emasoft-architect-agent | eaa-architect-main-agent |
| Integrator | eia | emasoft-integrator-agent | eia-integrator-main-agent |
| Programmer | (none) | emasoft-programmer-agent | epa-programmer-main-agent |

**Example session names:**
- `eoa-svgbbox-orchestrator`
- `eaa-webapp-architect`
- `eia-api-integrator`
- `svgbbox-programmer-001` (Programmer uses project-based naming)

### Step 2: Setup Plugin for Agent

Copy the plugin from the **emasoft-plugins marketplace cache** to the agent's local folder:
- **Source**: `$HOME/.claude/plugins/cache/emasoft-plugins/<plugin-name>/<latest-version>/`
- **Destination**: `$HOME/agents/<session-name>/.claude/plugins/<plugin-name>/`

Create the destination directory and copy the plugin files.

### Step 3: Create Agent Instance

Use the `ai-maestro-agents-management` skill to create a new agent:
- **Name**: the chosen session name
- **Directory**: `~/agents/<session-name>/` (FLAT structure)
- **Task**: description of the agent's purpose
- **Program args**: include `--dangerously-skip-permissions`, `--chrome`, `--add-dir /tmp`, `--plugin-dir` pointing to the copied plugin, and `--agent <prefix>-<role>-main-agent`

**Important flags:**
- `--dir`: Working directory for the agent (FLAT structure: `~/agents/<session-name>/`)
- `--task`: Description of the agent's purpose
- `--plugin-dir`: Path to the COPIED plugin in agent's local folder
- `--agent`: The main agent prompt to inject

### Step 4: Verify Initialization

Use the `ai-maestro-agents-management` skill to check the agent's status. Expected status: running.

### Step 5: Register in Team Registry

```bash
uv run python scripts/ecos_team_registry.py add-agent \
  --name "<session-name>" \
  --role "<role>" \
  --project "<project>" \
  --status "running"
```

### Step 6: Send Welcome Message

Use the `agent-messaging` skill to send a welcome message:
- **Recipient**: the new agent session name
- **Subject**: `Welcome - Agent Created`
- **Priority**: `high`
- **Content**: type `team-notification`, informing the agent it has been created and registered, and is awaiting role assignment from the orchestrator

## Checklist

Copy this checklist and track your progress:

- [ ] Determine agent type based on task requirements
- [ ] Choose unique session name following naming convention
- [ ] Verify plugin exists in marketplace cache
- [ ] Copy plugin to agent's local folder
- [ ] Create agent via `ai-maestro-agents-management` skill
- [ ] Verify agent status is "running"
- [ ] Register agent in team registry
- [ ] Send welcome message via `agent-messaging` skill
- [ ] Confirm agent acknowledgment received

## Examples

### Example: Creating an Orchestrator for svgbbox Project

1. Set variables: session name `eoa-svgbbox-orchestrator`, plugin `emasoft-orchestrator-agent`
2. Copy plugin from marketplace cache (`$HOME/.claude/plugins/cache/emasoft-plugins/emasoft-orchestrator-agent/<latest-version>/`) to `$HOME/agents/eoa-svgbbox-orchestrator/.claude/plugins/emasoft-orchestrator-agent/`
3. Use the `ai-maestro-agents-management` skill to create a new agent:
   - **Name**: `eoa-svgbbox-orchestrator`
   - **Directory**: `~/agents/eoa-svgbbox-orchestrator`
   - **Task**: `Orchestrate tasks for svgbbox-library-team`
   - **Program args**: include `--dangerously-skip-permissions`, `--chrome`, `--add-dir /tmp`, `--plugin-dir ~/agents/eoa-svgbbox-orchestrator/.claude/plugins/emasoft-orchestrator-agent`, `--agent eoa-orchestrator-main-agent`
4. Use the `ai-maestro-agents-management` skill to verify status is "running"
5. Register in team registry:
   ```bash
   uv run python scripts/ecos_team_registry.py add-agent \
     --name "eoa-svgbbox-orchestrator" \
     --role "orchestrator" \
     --project "svgbbox" \
     --status "running"
   ```

### Example: Creating a Programmer for svgbbox Project

1. Set variables: session name `svgbbox-programmer-001`, plugin `emasoft-programmer-agent` (Programmers use project-based naming)
2. Copy plugin from marketplace cache to `$HOME/agents/svgbbox-programmer-001/.claude/plugins/emasoft-programmer-agent/`
3. Use the `ai-maestro-agents-management` skill to create a new agent:
   - **Name**: `svgbbox-programmer-001`
   - **Directory**: `~/agents/svgbbox-programmer-001`
   - **Task**: `Implement authentication module for svgbbox`
   - **Program args**: include `--dangerously-skip-permissions`, `--chrome`, `--add-dir /tmp`, `--plugin-dir ~/agents/svgbbox-programmer-001/.claude/plugins/emasoft-programmer-agent`, `--agent epa-programmer-main-agent`
4. Use the `ai-maestro-agents-management` skill to verify status is "running"
5. Register in team registry:
   ```bash
   uv run python scripts/ecos_team_registry.py add-agent \
     --name "svgbbox-programmer-001" \
     --role "programmer" \
     --project "svgbbox" \
     --status "running"
   ```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Plugin not found in cache | Plugin not installed from marketplace | Install the plugin from the marketplace first |
| Session name already exists | Name collision | Choose a different unique session name |
| tmux session creation failed | tmux not installed or permission issue | Install tmux or check permissions |
| Agent status not "running" | Initialization failed | Check agent logs, retry with debug options |
| AI Maestro unreachable | Service not running | Start AI Maestro service |

## Related Operations

- [op-terminate-agent.md](op-terminate-agent.md) - Terminate agent when work complete
- [op-hibernate-agent.md](op-hibernate-agent.md) - Hibernate idle agent
- [op-update-team-registry.md](op-update-team-registry.md) - Update registry after operations
