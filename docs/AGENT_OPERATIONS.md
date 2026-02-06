# AGENT_OPERATIONS.md - ECOS Chief of Staff

**SINGLE SOURCE OF TRUTH** for ECOS (Emasoft Chief of Staff) agent operations.

---

## 1. Session Naming Convention

**Format**: `<role-prefix>-<descriptive>[-number]`

**ECOS prefix**: `ecos-`

**Examples**:
- `ecos-chief-of-staff-one`
- `ecos-project-alpha`
- `ecos-svgbbox-coordinator`

**Critical Rules**:
- Session name = AI Maestro registry identity (how agents message each other)
- Must be unique across all running agents
- Session name is passed to `aimaestro-agent.sh create` command
- Session name determines the tmux session name
- Session name must be valid for both tmux and AI Maestro (alphanumeric, hyphens, underscores only)

**Role Prefixes**:
| Role | Prefix | Example Session Name |
|------|--------|---------------------|
| Chief of Staff | `ecos-` | `ecos-chief-of-staff-one` |
| Orchestrator | `eoa-` | `eoa-svgbbox-orchestrator` |
| Architect | `eaa-` | `eaa-project-alpha-architect` |
| Integrator | `eia-` | `eia-feature-reviewer` |
| Manager | `eama-` | `eama-user-interface` |
| Programmer | (none) | `svgbbox-programmer-001` |

---

## 2. Plugin Paths

**Environment Variables**:
- `${CLAUDE_PLUGIN_ROOT}` - Set by Claude Code when plugin loaded via `--plugin-dir`
- `${CLAUDE_PROJECT_DIR}` - Working directory of the Claude Code session
- `${AIMAESTRO_API}` - AI Maestro API endpoint (default: `http://localhost:23000`)

**Path Resolution**:
```bash
# Current plugin (loaded by this agent)
${CLAUDE_PLUGIN_ROOT}
# Example: ~/agents/ecos-chief-of-staff-one/.claude/plugins/emasoft-chief-of-staff

# Sibling plugins (in same parent directory)
${CLAUDE_PLUGIN_ROOT}/../<plugin-name>
# Example: ~/agents/ecos-chief-of-staff-one/.claude/plugins/emasoft-orchestrator-agent

# Agent local plugins directory
~/agents/<session-name>/.claude/plugins/<plugin-name>/
```

**Plugin Sources**:
| Context | Plugin Source |
|---------|--------------|
| **Marketplace** | `~/.claude/plugins/cache/emasoft-plugins/<plugin-name>/<version>/` |
| **Agent Local** | `~/agents/<session-name>/.claude/plugins/<plugin-name>/` |

**CRITICAL**: ECOS installs plugins from the emasoft-plugins marketplace cache to the agent's local `.claude/plugins/` folder!

---

## 3. Agent Directory Structure (FLAT)

**Architecture**: FLAT (no nesting, all agents at same level)

```
~/agents/
├── ecos-chief-of-staff-one/
│   └── .claude/
│       └── plugins/
│           └── emasoft-chief-of-staff/
│               ├── .claude-plugin/
│               │   └── plugin.json
│               ├── agents/
│               ├── skills/
│               ├── commands/
│               └── hooks/
├── eoa-svgbbox-orchestrator/
│   └── .claude/
│       └── plugins/
│           └── emasoft-orchestrator-agent/
│               ├── .claude-plugin/
│               │   └── plugin.json
│               ├── agents/
│               ├── skills/
│               ├── commands/
│               └── hooks/
├── eaa-project-alpha-architect/
│   └── .claude/
│       └── plugins/
│           └── emasoft-architect-agent/
│               └── ...
├── eia-feature-reviewer/
│   └── .claude/
│       └── plugins/
│           └── emasoft-integrator-agent/
│               └── ...
├── svgbbox-programmer-001/
│   └── .claude/
│       └── plugins/
│           └── emasoft-programmer-agent/
│               └── ...
└── eama-user-interface/
    └── .claude/
        └── plugins/
            └── emasoft-assistant-manager-agent/
                └── ...
```

**Why FLAT?**:
- Each agent is an independent Claude Code session
- No parent-child relationship in file system
- Communication happens via AI Maestro messaging, not file system
- Easier to manage, monitor, and terminate individual agents

---

## 4. Spawn Procedure

### 4.1 Copy Plugin First

**CRITICAL**: Always copy plugin to agent's local directory before spawning!

```bash
# Define paths - Use marketplace cache as source
PLUGIN_NAME="<target-plugin>"
# Marketplace plugins installed via: claude plugin install <name>@emasoft-plugins
PLUGIN_SOURCE="$HOME/.claude/plugins/cache/emasoft-plugins/$PLUGIN_NAME"
# Use latest version from marketplace cache
PLUGIN_VERSION=$(ls -1 "$PLUGIN_SOURCE" | sort -V | tail -1)
PLUGIN_SOURCE="$PLUGIN_SOURCE/$PLUGIN_VERSION"

SESSION_NAME="<role-prefix>-<descriptive>"
PLUGIN_DEST="$HOME/agents/$SESSION_NAME/.claude/plugins/$PLUGIN_NAME"

# Create directory and copy from marketplace cache
mkdir -p "$(dirname "$PLUGIN_DEST")"
cp -r "$PLUGIN_SOURCE" "$PLUGIN_DEST"

# Verify copy succeeded
if [ -f "$PLUGIN_DEST/.claude-plugin/plugin.json" ]; then
  echo "Plugin copied successfully"
else
  echo "ERROR: Plugin copy failed!"
  exit 1
fi
```

### 4.2 Spawn Command

```bash
SESSION_NAME="<role-prefix>-<descriptive>"
WORKING_DIR="$HOME/agents/$SESSION_NAME"
PLUGIN_PATH="$WORKING_DIR/.claude/plugins/<target-plugin>"
AGENT_NAME="<prefix>-<role>-main-agent"

aimaestro-agent.sh create "$SESSION_NAME" \
  --dir "$WORKING_DIR" \
  --task "Task description here" \
  -- --dangerously-skip-permissions \
     --chrome \
     --add-dir /tmp \
     --plugin-dir "$PLUGIN_PATH" \
     --agent "$AGENT_NAME"
```

**Flags Explained**:
- `--dir` - Agent's working directory
- `--task` - Initial task prompt for the agent
- `--` - Separator between aimaestro-agent.sh flags and Claude Code flags
- `--dangerously-skip-permissions` - Auto-approve file operations
- `--chrome` - Enable Chrome DevTools MCP
- `--add-dir /tmp` - Add /tmp to accessible directories
- `--plugin-dir` - Path to plugin to load
- `--agent` - Agent definition file to use

### 4.3 Role to Plugin/Agent Mapping

| Role | Plugin | --agent Flag | Prefix |
|------|--------|--------------|--------|
| Chief of Staff | `emasoft-chief-of-staff` | `ecos-chief-of-staff-main-agent` | `ecos-` |
| Orchestrator | `emasoft-orchestrator-agent` | `eoa-orchestrator-main-agent` | `eoa-` |
| Architect | `emasoft-architect-agent` | `eaa-architect-main-agent` | `eaa-` |
| Integrator | `emasoft-integrator-agent` | `eia-integrator-main-agent` | `eia-` |
| Manager | `emasoft-assistant-manager-agent` | `eama-assistant-manager-main-agent` | `eama-` |
| Programmer | `emasoft-programmer-agent` | `epa-programmer-main-agent` | (none) |

### 4.4 Example: Spawn Orchestrator

```bash
# Step 1: Define session name
SESSION_NAME="eoa-svgbbox-orchestrator"

# Step 2: Install plugin from marketplace cache
# Prerequisite: claude plugin install emasoft-orchestrator-agent@emasoft-plugins
PLUGIN_NAME="emasoft-orchestrator-agent"
MARKETPLACE_CACHE="$HOME/.claude/plugins/cache/emasoft-plugins/$PLUGIN_NAME"
PLUGIN_VERSION=$(ls -1 "$MARKETPLACE_CACHE" | sort -V | tail -1)
PLUGIN_SOURCE="$MARKETPLACE_CACHE/$PLUGIN_VERSION"
PLUGIN_DEST="$HOME/agents/$SESSION_NAME/.claude/plugins/$PLUGIN_NAME"
mkdir -p "$(dirname "$PLUGIN_DEST")"
cp -r "$PLUGIN_SOURCE" "$PLUGIN_DEST"

# Step 3: Spawn agent
aimaestro-agent.sh create "$SESSION_NAME" \
  --dir "$HOME/agents/$SESSION_NAME" \
  --task "Orchestrate development of svgbbox library features" \
  -- --dangerously-skip-permissions \
     --chrome \
     --add-dir /tmp \
     --plugin-dir "$PLUGIN_DEST" \
     --agent eoa-orchestrator-main-agent
```

### 4.5 Example: Spawn Programmer

```bash
# Step 1: Define session name (Programmers use project-based naming)
SESSION_NAME="svgbbox-programmer-001"

# Step 2: Install plugin from marketplace cache
PLUGIN_NAME="emasoft-programmer-agent"
MARKETPLACE_CACHE="$HOME/.claude/plugins/cache/emasoft-plugins/$PLUGIN_NAME"
PLUGIN_VERSION=$(ls -1 "$MARKETPLACE_CACHE" | sort -V | tail -1)
PLUGIN_SOURCE="$MARKETPLACE_CACHE/$PLUGIN_VERSION"
PLUGIN_DEST="$HOME/agents/$SESSION_NAME/.claude/plugins/$PLUGIN_NAME"
mkdir -p "$(dirname "$PLUGIN_DEST")"
cp -r "$PLUGIN_SOURCE" "$PLUGIN_DEST"

# Step 3: Spawn agent
aimaestro-agent.sh create "$SESSION_NAME" \
  --dir "$HOME/agents/$SESSION_NAME" \
  --task "Implement authentication module for svgbbox library" \
  -- --dangerously-skip-permissions \
     --chrome \
     --add-dir /tmp \
     --plugin-dir "$PLUGIN_DEST" \
     --agent epa-programmer-main-agent
```

---

## 5. Wake Procedure (Hibernated Agent)

**When to use**: Agent was hibernated (tmux session exists but detached)

```bash
aimaestro-agent.sh wake <session-name>
```

**What happens**:
- `aimaestro-agent.sh` internally adds `--continue` flag to Claude Code
- Reattaches to existing tmux session
- Claude Code resumes from last state
- Agent reconnects to AI Maestro

**Example**:
```bash
aimaestro-agent.sh wake eoa-svgbbox-orchestrator
```

**Verification**:
```bash
# Check if session is running
tmux list-sessions | grep <session-name>

# Check AI Maestro registration
curl -s "$AIMAESTRO_API/api/agents" | jq '.agents[] | select(.session_name == "<session-name>")'
```

---

## 6. Hibernate Procedure

**When to use**: Temporarily pause agent, preserve state

```bash
aimaestro-agent.sh hibernate <session-name>
```

**What happens**:
- Detaches from tmux session (session continues running)
- Agent remains registered in AI Maestro
- Can be woken later with `wake` command

**Example**:
```bash
aimaestro-agent.sh hibernate eoa-svgbbox-orchestrator
```

**Difference from Terminate**:
| Action | Tmux Session | AI Maestro | State |
|--------|--------------|------------|-------|
| **Hibernate** | Detached | Registered | Preserved |
| **Terminate** | Killed | Unregistered | Lost |

---

## 7. Terminate Procedure

**When to use**: Permanently stop agent, clean up resources

```bash
aimaestro-agent.sh delete <session-name> --confirm
```

**Flags**:
- `--confirm` - Required to prevent accidental termination
- `--force` - Forcefully kill tmux session (use if graceful stop fails)

**What happens**:
- Claude Code session stopped
- Tmux session killed
- Agent unregistered from AI Maestro
- Working directory preserved (not deleted)

**Example**:
```bash
# Normal termination
aimaestro-agent.sh delete eoa-svgbbox-orchestrator --confirm

# Forceful termination (if stuck)
aimaestro-agent.sh delete eoa-svgbbox-orchestrator --confirm --force
```

**Cleanup (optional)**:
```bash
# Remove working directory
rm -rf ~/agents/eoa-svgbbox-orchestrator
```

**CRITICAL**: Always terminate agents when work is complete to avoid:
- Resource leaks (CPU, memory)
- AI Maestro registry clutter
- Orphaned tmux sessions

---

## 8. Plugin Mutual Exclusivity

**CRITICAL RULE**: Each Claude Code instance can only have ONE role plugin loaded at a time!

**Why?**:
- Plugin hooks can conflict (duplicate PreToolUse, PostToolUse, etc.)
- Skill namespaces can collide
- Command namespaces can collide
- Agent definitions can conflict

**Implications**:
- ❌ CANNOT load `emasoft-chief-of-staff` + `emasoft-orchestrator-agent` in same session
- ❌ CANNOT reference skills from other plugins (e.g., EIA skill in EOA session)
- ✅ MUST spawn separate agent with correct plugin for cross-role operations
- ✅ MUST use AI Maestro messaging for cross-plugin communication

**Self-Contained Plugins**:
Each plugin must include:
- All skills needed for that role
- All commands for that role
- All agents for that role
- All hooks for that role

**Cross-Plugin Communication**: AI Maestro messages ONLY!

**Example Violations**:
```bash
# WRONG: Load two role plugins
claude --plugin-dir ~/plugins/emasoft-chief-of-staff \
       --plugin-dir ~/plugins/emasoft-orchestrator-agent

# WRONG: Reference other plugin's skill
/learn eoa-two-phase-orchestration  # eoa- skill in ecos- session

# WRONG: Use other plugin's command
/eoa-initiate  # eoa- command in ecos- session
```

**Correct Approach**:
```bash
# RIGHT: One plugin per session
claude --plugin-dir ~/plugins/emasoft-chief-of-staff

# RIGHT: Spawn separate agent for other role
aimaestro-agent.sh create eoa-orchestrator-one \
  --plugin-dir ~/plugins/emasoft-orchestrator-agent

# RIGHT: Use AI Maestro for cross-role communication
curl -X POST "$AIMAESTRO_API/api/messages" \
  -d '{"from": "ecos-one", "to": "eoa-orchestrator-one", ...}'
```

---

## 9. AI Maestro Messaging

### 9.1 Send Message

```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "<sender-session-name>",
    "to": "<receiver-session-name>",
    "subject": "Subject",
    "priority": "normal|high|urgent",
    "content": {"type": "request|response|notification", "message": "..."}
  }'
```

**Priority Levels**:
| Priority | Use Case | Example |
|----------|----------|---------|
| `normal` | Regular updates, progress reports | "Task completed successfully" |
| `high` | Action required, important info | "Need input on architecture decision" |
| `urgent` | Blocking issue, immediate attention | "Critical bug found in production" |

**Content Types**:
| Type | Use Case | Example |
|------|----------|---------|
| `request` | Ask agent to do something | "Please review PR #42" |
| `response` | Reply to a request | "PR #42 approved" |
| `notification` | Inform about event | "Tests completed, 3 failures" |

### 9.2 Check Inbox

```bash
curl -s "$AIMAESTRO_API/api/messages?agent=<session-name>&action=list&status=unread" \
  | jq '.messages[].content.message'
```

### 9.3 Mark Message Read

```bash
curl -X POST "$AIMAESTRO_API/api/messages/<message-id>/read"
```

### 9.4 Message Workflow Example

```bash
# ECOS sends task to Orchestrator
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff-one",
    "to": "eoa-svgbbox-orchestrator",
    "subject": "Implement Feature X",
    "priority": "high",
    "content": {
      "type": "request",
      "message": "Please implement feature X with the following requirements: ..."
    }
  }'

# Orchestrator acknowledges
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eoa-svgbbox-orchestrator",
    "to": "ecos-chief-of-staff-one",
    "subject": "Re: Implement Feature X",
    "priority": "normal",
    "content": {
      "type": "response",
      "message": "Acknowledged. Starting implementation. ETA: 2 hours."
    }
  }'

# Orchestrator completes task
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eoa-svgbbox-orchestrator",
    "to": "ecos-chief-of-staff-one",
    "subject": "Re: Implement Feature X",
    "priority": "normal",
    "content": {
      "type": "notification",
      "message": "Feature X implementation complete. PR #42 ready for review."
    }
  }'
```

---

## 10. Skill References

### 10.1 Correct Format

**Reference skills by folder name only**:
```markdown
See skill: **ecos-agent-lifecycle**
```

**In commands/agents, use just the skill name**:
```yaml
skills:
  - ecos-agent-lifecycle
  - ecos-task-delegation
```

### 10.2 NEVER Use Paths

❌ **WRONG**:
```markdown
See skill: ../skills/ecos-agent-lifecycle/SKILL.md
See skill: ${CLAUDE_PLUGIN_ROOT}/skills/ecos-agent-lifecycle/SKILL.md
See skill: /full/path/to/skills/ecos-agent-lifecycle/SKILL.md
```

### 10.3 NEVER Reference Other Plugins' Skills

❌ **WRONG** (in ECOS session):
```yaml
skills:
  - eoa-two-phase-orchestration  # This is EOA skill, not ECOS!
  - eaa-architecture-design  # This is EAA skill, not ECOS!
```

✅ **CORRECT** (in ECOS session):
```yaml
skills:
  - ecos-agent-lifecycle  # ECOS skill
  - ecos-task-delegation  # ECOS skill
```

### 10.4 Skill Discovery

Claude Code resolves skill names using:
1. Plugin's `skills/` directory
2. Skill folder names (not SKILL.md content)
3. Skill frontmatter `name` field (optional)

**Example**: If skill is at `skills/ecos-agent-lifecycle/`, reference as `ecos-agent-lifecycle`.

---

## 11. ECOS-Specific Responsibilities

### 11.1 Creation

**ECOS is created by EAMA (Manager) only!**

- User interacts with EAMA (Manager) first
- EAMA assesses if task requires orchestration
- EAMA spawns ECOS for complex multi-agent coordination

### 11.2 Agent Creation Authority

**ECOS creates**:
1. **Orchestrator** (`eoa-`) - Coordinates task execution
2. **Architect** (`eaa-`) - Designs system architecture
3. **Integrator** (`eia-`) - Reviews code, runs quality gates

**ECOS does NOT create**:
- Manager (`eama-`) - Only user creates Manager
- Other ECOS instances - Only Manager creates ECOS

### 11.3 Session Naming Responsibility

**ECOS chooses unique session names** for all agents it creates!

**Naming Strategy**:
```bash
# Format: <role-prefix>-<project>-<role>[-number]
# Examples:
eoa-svgbbox-orchestrator
eaa-svgbbox-architect
eia-svgbbox-integrator

# If multiple needed:
eoa-svgbbox-orchestrator-1
eoa-svgbbox-orchestrator-2
```

**Uniqueness Check**:
```bash
# Before spawning, check if name exists
curl -s "$AIMAESTRO_API/api/agents" | jq -r '.agents[].session_name' | grep "^${SESSION_NAME}$"
# If output is empty, name is unique
```

### 11.4 Lifecycle Management

**ECOS monitors agent health**:
```bash
# Heartbeat check (every 5 minutes)
curl -s "$AIMAESTRO_API/api/agents/<session-name>/status"

# Check message backlog
curl -s "$AIMAESTRO_API/api/messages?agent=<session-name>&status=unread" | jq '.count'

# Check last activity
curl -s "$AIMAESTRO_API/api/agents/<session-name>/last-activity"
```

**ECOS hibernates idle agents**:
```bash
# If agent idle > 30 minutes with no pending tasks
aimaestro-agent.sh hibernate <session-name>
```

**ECOS terminates completed agents**:
```bash
# After work is done and verified
aimaestro-agent.sh delete <session-name> --confirm
```

### 11.5 Task Delegation Flow

```
User Request
     ↓
   EAMA (Manager)
     ↓ (spawns if complex)
   ECOS (Chief of Staff)
     ↓
     ├─→ EOA (Orchestrator) ─→ Implementation agents
     ├─→ EAA (Architect) ─→ Design agents
     └─→ EIA (Integrator) ─→ Review agents
```

**ECOS coordination responsibilities**:
1. Assess task complexity and requirements
2. Choose which agents to spawn (Orchestrator, Architect, Integrator)
3. Assign unique session names
4. Copy plugins to agent directories
5. Spawn agents with appropriate flags
6. Send initial task prompts via AI Maestro
7. Monitor agent progress and health
8. Coordinate cross-agent communication
9. Hibernate idle agents
10. Terminate completed agents
11. Report final results back to EAMA

---

## 12. Troubleshooting

### 12.1 Agent Won't Spawn

**Symptom**: `aimaestro-agent.sh create` fails

**Check**:
```bash
# 1. Session name already exists?
tmux list-sessions | grep <session-name>

# 2. AI Maestro running?
curl -s "$AIMAESTRO_API/api/agents" | jq .

# 3. Plugin exists at path?
ls -la ~/agents/<session-name>/.claude/plugins/<plugin-name>/.claude-plugin/plugin.json

# 4. Claude Code binary accessible?
which claude
```

### 12.2 Agent Can't Find Skills

**Symptom**: Skill reference fails

**Check**:
```bash
# 1. Skill exists in plugin?
ls -la ~/agents/<session-name>/.claude/plugins/<plugin-name>/skills/

# 2. Skill folder name matches reference?
# Reference: ecos-agent-lifecycle
# Folder: skills/ecos-agent-lifecycle/

# 3. SKILL.md exists?
cat ~/agents/<session-name>/.claude/plugins/<plugin-name>/skills/ecos-agent-lifecycle/SKILL.md
```

**Fix**: Use skill folder name only, no paths!

### 12.3 Cross-Plugin Skill References Fail

**Symptom**: Agent in ECOS session tries to use EOA skill

**Why**: Plugin mutual exclusivity - can't reference other plugin's skills

**Fix**: Spawn separate agent with correct plugin!

```bash
# WRONG: Try to use EOA skill in ECOS session
/learn eoa-two-phase-orchestration  # Fails!

# RIGHT: Spawn EOA agent, send task via AI Maestro
aimaestro-agent.sh create eoa-temp-orchestrator ...
curl -X POST "$AIMAESTRO_API/api/messages" -d '{"to": "eoa-temp-orchestrator", ...}'
```

### 12.4 Plugin Hooks Conflict

**Symptom**: Duplicate PreToolUse hooks error

**Cause**: Two plugins with same hook loaded (violates mutual exclusivity)

**Check**:
```bash
# How many --plugin-dir flags?
ps aux | grep "claude.*--plugin-dir" | grep <session-name>
```

**Fix**: Only load ONE role plugin per agent!

### 12.5 AI Maestro Messages Not Received

**Symptom**: Agent doesn't receive messages

**Check**:
```bash
# 1. Agent registered?
curl -s "$AIMAESTRO_API/api/agents" | jq '.agents[] | select(.session_name == "<session-name>")'

# 2. Messages in inbox?
curl -s "$AIMAESTRO_API/api/messages?agent=<session-name>&action=list&status=unread"

# 3. Message poll hook working?
# Check plugin's hooks/hooks.json for UserPromptSubmit hook
```

**Fix**: Ensure AI Maestro hook is loaded (check plugin's hooks.json)

---

## 13. Quick Reference Commands

```bash
# Spawn agent
aimaestro-agent.sh create <session> --dir ~/agents/<session> --task "..." -- --plugin-dir ~/agents/<session>/.claude/plugins/<plugin> --agent <agent-name>

# Wake hibernated agent
aimaestro-agent.sh wake <session>

# Hibernate agent
aimaestro-agent.sh hibernate <session>

# Terminate agent
aimaestro-agent.sh delete <session> --confirm

# Send message
curl -X POST "$AIMAESTRO_API/api/messages" -H "Content-Type: application/json" -d '{"from":"<from>","to":"<to>","subject":"...","priority":"normal","content":{"type":"request","message":"..."}}'

# Check inbox
curl -s "$AIMAESTRO_API/api/messages?agent=<session>&action=list&status=unread" | jq .

# List agents
curl -s "$AIMAESTRO_API/api/agents" | jq '.agents[] | {session: .session_name, status: .status}'

# Check agent status
curl -s "$AIMAESTRO_API/api/agents/<session>/status" | jq .
```

---

**END OF DOCUMENT**
