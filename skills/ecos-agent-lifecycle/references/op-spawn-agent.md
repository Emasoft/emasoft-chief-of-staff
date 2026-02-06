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

- AI Maestro is running locally at `http://localhost:23000`
- `aimaestro-agent.sh` CLI is available in PATH
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

Copy the plugin from marketplace cache to agent's local folder:

```bash
# Variables
SESSION_NAME="<chosen-session-name>"
PLUGIN_NAME="<plugin-name>"
MARKETPLACE_CACHE="$HOME/.claude/plugins/cache/emasoft-plugins/$PLUGIN_NAME"
PLUGIN_VERSION=$(ls -1 "$MARKETPLACE_CACHE" | sort -V | tail -1)
PLUGIN_SOURCE="$MARKETPLACE_CACHE/$PLUGIN_VERSION"
PLUGIN_DEST="$HOME/agents/$SESSION_NAME/.claude/plugins/$PLUGIN_NAME"

# Create destination and copy
mkdir -p "$(dirname "$PLUGIN_DEST")"
cp -r "$PLUGIN_SOURCE" "$PLUGIN_DEST"
```

### Step 3: Create Agent Instance

Use aimaestro-agent.sh to create the agent:

```bash
aimaestro-agent.sh create $SESSION_NAME \
  --dir ~/agents/$SESSION_NAME \
  --task "<task description>" \
  -- --dangerously-skip-permissions --chrome --add-dir /tmp \
  --plugin-dir ~/agents/$SESSION_NAME/.claude/plugins/$PLUGIN_NAME \
  --agent <prefix>-<role>-main-agent
```

**Important flags:**
- `--dir`: Working directory for the agent (FLAT structure: `~/agents/<session-name>/`)
- `--task`: Description of the agent's purpose
- `--plugin-dir`: Path to the COPIED plugin in agent's local folder
- `--agent`: The main agent prompt to inject

### Step 4: Verify Initialization

```bash
# Check agent status
aimaestro-agent.sh status $SESSION_NAME

# Expected output: "running"
```

### Step 5: Register in Team Registry

```bash
uv run python scripts/ecos_team_registry.py add-agent \
  --name "$SESSION_NAME" \
  --role "<role>" \
  --project "<project>" \
  --status "running"
```

### Step 6: Send Welcome Message

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "'"$SESSION_NAME"'",
    "subject": "Welcome - Agent Created",
    "priority": "high",
    "content": {"type": "team-notification", "message": "You have been created and registered. Awaiting role assignment from orchestrator."}
  }'
```

## Checklist

Copy this checklist and track your progress:

- [ ] Determine agent type based on task requirements
- [ ] Choose unique session name following naming convention
- [ ] Verify plugin exists in marketplace cache
- [ ] Copy plugin to agent's local folder
- [ ] Execute aimaestro-agent.sh create command
- [ ] Verify agent status is "running"
- [ ] Register agent in team registry
- [ ] Send welcome message via AI Maestro
- [ ] Confirm agent acknowledgment received

## Examples

### Example: Creating an Orchestrator for svgbbox Project

```bash
# Step 1: Set variables
SESSION_NAME="eoa-svgbbox-orchestrator"
PLUGIN_NAME="emasoft-orchestrator-agent"

# Step 2: Setup plugin
MARKETPLACE_CACHE="$HOME/.claude/plugins/cache/emasoft-plugins/$PLUGIN_NAME"
PLUGIN_VERSION=$(ls -1 "$MARKETPLACE_CACHE" | sort -V | tail -1)
mkdir -p "$HOME/agents/$SESSION_NAME/.claude/plugins"
cp -r "$MARKETPLACE_CACHE/$PLUGIN_VERSION" "$HOME/agents/$SESSION_NAME/.claude/plugins/$PLUGIN_NAME"

# Step 3: Create agent
aimaestro-agent.sh create $SESSION_NAME \
  --dir ~/agents/$SESSION_NAME \
  --task "Orchestrate tasks for svgbbox-library-team" \
  -- --dangerously-skip-permissions --chrome --add-dir /tmp \
  --plugin-dir ~/agents/$SESSION_NAME/.claude/plugins/$PLUGIN_NAME \
  --agent eoa-orchestrator-main-agent

# Step 4: Verify
aimaestro-agent.sh status $SESSION_NAME
# Expected: running

# Step 5: Register
uv run python scripts/ecos_team_registry.py add-agent \
  --name "$SESSION_NAME" \
  --role "orchestrator" \
  --project "svgbbox" \
  --status "running"
```

### Example: Creating a Programmer for svgbbox Project

```bash
# Step 1: Set variables (Programmers use project-based naming)
SESSION_NAME="svgbbox-programmer-001"
PLUGIN_NAME="emasoft-programmer-agent"

# Step 2: Setup plugin
MARKETPLACE_CACHE="$HOME/.claude/plugins/cache/emasoft-plugins/$PLUGIN_NAME"
PLUGIN_VERSION=$(ls -1 "$MARKETPLACE_CACHE" | sort -V | tail -1)
mkdir -p "$HOME/agents/$SESSION_NAME/.claude/plugins"
cp -r "$MARKETPLACE_CACHE/$PLUGIN_VERSION" "$HOME/agents/$SESSION_NAME/.claude/plugins/$PLUGIN_NAME"

# Step 3: Create agent
aimaestro-agent.sh create $SESSION_NAME \
  --dir ~/agents/$SESSION_NAME \
  --task "Implement authentication module for svgbbox" \
  -- --dangerously-skip-permissions --chrome --add-dir /tmp \
  --plugin-dir ~/agents/$SESSION_NAME/.claude/plugins/$PLUGIN_NAME \
  --agent epa-programmer-main-agent

# Step 4: Verify
aimaestro-agent.sh status $SESSION_NAME
# Expected: running

# Step 5: Register
uv run python scripts/ecos_team_registry.py add-agent \
  --name "$SESSION_NAME" \
  --role "programmer" \
  --project "svgbbox" \
  --status "running"
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Plugin not found in cache | Plugin not installed from marketplace | Run `claude plugin install <plugin>@emasoft-plugins` first |
| Session name already exists | Name collision | Choose a different unique session name |
| tmux session creation failed | tmux not installed or permission issue | Install tmux or check permissions |
| Agent status not "running" | Initialization failed | Check agent logs, retry with --debug flag |
| AI Maestro unreachable | Service not running | Start AI Maestro with `aimaestro start` |

## Related Operations

- [op-terminate-agent.md](op-terminate-agent.md) - Terminate agent when work complete
- [op-hibernate-agent.md](op-hibernate-agent.md) - Hibernate idle agent
- [op-update-team-registry.md](op-update-team-registry.md) - Update registry after operations
