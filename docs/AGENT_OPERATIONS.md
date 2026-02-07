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
- Session name is used when creating an agent via the `ai-maestro-agents-management` skill
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
- `${AIMAESTRO_API}` - AI Maestro API endpoint (configured automatically by AI Maestro)

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

The plugin must be copied from the marketplace cache to the agent's local `.claude/plugins/` directory:
- **Source**: `$HOME/.claude/plugins/cache/emasoft-plugins/<plugin-name>/<latest-version>/`
- **Destination**: `$HOME/agents/<session-name>/.claude/plugins/<plugin-name>/`

**Verify**: the copied plugin contains `.claude-plugin/plugin.json`.

### 4.2 Spawn Command

Use the `ai-maestro-agents-management` skill to create a new agent:
- **Name**: `<role-prefix>-<descriptive>` (the session name)
- **Directory**: `$HOME/agents/<session-name>` (the working directory)
- **Task**: task description for the agent
- **Program args**: include standard Claude Code flags plus `--plugin-dir` and `--agent`

**Required parameters**:
| Parameter | Purpose |
|-----------|---------|
| Name | Session name (also AI Maestro registry identity) |
| Directory | Agent's working directory |
| Task | Initial task prompt |
| `--dangerously-skip-permissions` | Auto-approve file operations |
| `--chrome` | Enable Chrome DevTools MCP |
| `--add-dir /tmp` | Add /tmp to accessible directories |
| `--plugin-dir` | Path to the plugin to load |
| `--agent` | Agent definition file to use |

**Verify**: the new agent appears in the agent list with "online" status.

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

1. Copy `emasoft-orchestrator-agent` plugin from marketplace cache to `$HOME/agents/eoa-svgbbox-orchestrator/.claude/plugins/emasoft-orchestrator-agent/`
2. Use the `ai-maestro-agents-management` skill to create a new agent:
   - **Name**: `eoa-svgbbox-orchestrator`
   - **Directory**: `$HOME/agents/eoa-svgbbox-orchestrator`
   - **Task**: "Orchestrate development of svgbbox library features"
   - **Plugin**: `emasoft-orchestrator-agent`
   - **Agent**: `eoa-orchestrator-main-agent`

**Verify**: agent `eoa-svgbbox-orchestrator` appears online in the agent list.

### 4.5 Example: Spawn Programmer

1. Copy `emasoft-programmer-agent` plugin from marketplace cache to `$HOME/agents/svgbbox-programmer-001/.claude/plugins/emasoft-programmer-agent/`
2. Use the `ai-maestro-agents-management` skill to create a new agent:
   - **Name**: `svgbbox-programmer-001` (Programmers use project-based naming)
   - **Directory**: `$HOME/agents/svgbbox-programmer-001`
   - **Task**: "Implement authentication module for svgbbox library"
   - **Plugin**: `emasoft-programmer-agent`
   - **Agent**: `epa-programmer-main-agent`

**Verify**: agent `svgbbox-programmer-001` appears online in the agent list.

---

## 5. Wake Procedure (Hibernated Agent)

**When to use**: Agent was hibernated (tmux session exists but detached)

Use the `ai-maestro-agents-management` skill to wake the agent:
- **Name**: the session name of the hibernated agent

**What happens**:
- The `--continue` flag is internally added to Claude Code
- Reattaches to existing tmux session
- Claude Code resumes from last state
- Agent reconnects to the agent registry

**Verify**: agent status shows "online" in the agent list, and tmux session is running.

---

## 6. Hibernate Procedure

**When to use**: Temporarily pause agent, preserve state

Use the `ai-maestro-agents-management` skill to hibernate the agent:
- **Name**: the session name of the agent to hibernate

**What happens**:
- Detaches from tmux session (session continues running)
- Agent remains registered in the agent registry
- Can be woken later

**Difference from Terminate**:
| Action | Tmux Session | Registry | State |
|--------|--------------|----------|-------|
| **Hibernate** | Detached | Registered | Preserved |
| **Terminate** | Killed | Unregistered | Lost |

---

## 7. Terminate Procedure

**When to use**: Permanently stop agent, clean up resources

Use the `ai-maestro-agents-management` skill to terminate (delete) the agent:
- **Name**: the session name of the agent to terminate
- **Confirm**: required to prevent accidental termination
- **Force**: optional, forcefully kill tmux session if graceful stop fails

**What happens**:
- Claude Code session stopped
- Tmux session killed
- Agent unregistered from the agent registry
- Working directory preserved (not deleted)

**CRITICAL**: Always terminate agents when work is complete to avoid:
- Resource leaks (CPU, memory)
- Agent registry clutter
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
- **One plugin per session**: Load only ONE role plugin when launching Claude Code
- **Spawn separate agent for other role**: Use the `ai-maestro-agents-management` skill to create a new agent with its own role plugin
- **Cross-role communication**: Use the `agent-messaging` skill to send messages between agents

---

## 9. Inter-Agent Messaging

All messaging operations use the `agent-messaging` skill. Never use explicit API calls or command-line tools directly.

### 9.1 Send Message

Use the `agent-messaging` skill to send a message:
- **Recipient**: the target agent session name
- **Subject**: descriptive subject line
- **Content**: structured message with type and body
- **Priority**: `normal`, `high`, or `urgent`
- **Type**: `request`, `response`, or `notification`

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

Use the `agent-messaging` skill to check for unread messages.

### 9.3 Mark Message Read

Use the `agent-messaging` skill to mark a message as read.

### 9.4 Message Workflow Example

1. **ECOS sends task to Orchestrator** using the `agent-messaging` skill:
   - **Recipient**: `eoa-svgbbox-orchestrator`
   - **Subject**: "Implement Feature X"
   - **Content**: request with feature requirements
   - **Priority**: `high`

2. **Orchestrator acknowledges** using the `agent-messaging` skill:
   - **Recipient**: `ecos-chief-of-staff-one`
   - **Subject**: "Re: Implement Feature X"
   - **Content**: response acknowledging and providing ETA
   - **Priority**: `normal`

3. **Orchestrator reports completion** using the `agent-messaging` skill:
   - **Recipient**: `ecos-chief-of-staff-one`
   - **Subject**: "Re: Implement Feature X"
   - **Content**: notification that implementation is complete with PR reference
   - **Priority**: `normal`

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
4. **Programmer** (`epa-`) - Implements code tasks

**ECOS does NOT create**:
- Manager (`eama-`) - Only user creates Manager
- Other ECOS instances - Only Manager creates ECOS

**Implementer Category**: "Implementer" is an umbrella term for all agents that produce concrete deliverables. The Programmer is the first implementer role. Future implementer roles (each with its own plugin) may include: Documenter, 2D Artist, 3D Artist, Video Maker, Sound FX Artist, Music Maker, UI Designer, Copywriter, Interactive Storytelling, Marketing, App Store Optimization, SEO, and Financial agents.

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

**Uniqueness Check**: Before spawning, use the `ai-maestro-agents-management` skill to list all agents and verify the chosen session name is not already in use. If the name exists, append a number suffix.

### 11.4 Lifecycle Management

**ECOS monitors agent health**: Use the `ai-maestro-agents-management` skill to check agent status, heartbeat timestamps, message backlog, and last activity time (every 5 minutes).

**ECOS hibernates idle agents**: If an agent has been idle for more than 30 minutes with no pending tasks, use the `ai-maestro-agents-management` skill to hibernate it.

**ECOS terminates completed agents**: After work is done and verified, use the `ai-maestro-agents-management` skill to terminate the agent (with confirmation).

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

**Symptom**: Agent creation fails

**Check**:
1. Session name already exists? Check with `tmux list-sessions`
2. Agent registry running? Use the `ai-maestro-agents-management` skill to list agents
3. Plugin exists at path? Check `~/agents/<session-name>/.claude/plugins/<plugin-name>/.claude-plugin/plugin.json`
4. Claude Code binary accessible? Check with `which claude`

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

**Fix**: Spawn a separate agent with the correct plugin using the `ai-maestro-agents-management` skill, then send the task via the `agent-messaging` skill.

### 12.4 Plugin Hooks Conflict

**Symptom**: Duplicate PreToolUse hooks error

**Cause**: Two plugins with same hook loaded (violates mutual exclusivity)

**Check**:
```bash
# How many --plugin-dir flags?
ps aux | grep "claude.*--plugin-dir" | grep <session-name>
```

**Fix**: Only load ONE role plugin per agent!

### 12.5 Messages Not Received

**Symptom**: Agent doesn't receive messages

**Check**:
1. Agent registered? Use the `ai-maestro-agents-management` skill to verify agent exists
2. Messages in inbox? Use the `agent-messaging` skill to check for unread messages
3. Message poll hook working? Check plugin's `hooks/hooks.json` for UserPromptSubmit hook

**Fix**: Ensure the messaging hook is loaded (check plugin's hooks.json)

---

## 13. Quick Reference

All operations below use intent-based skill references:

| Operation | Skill | Intent |
|-----------|-------|--------|
| **Spawn agent** | `ai-maestro-agents-management` | Create a new agent with name, directory, task, and plugin |
| **Wake agent** | `ai-maestro-agents-management` | Wake a hibernated agent by name |
| **Hibernate agent** | `ai-maestro-agents-management` | Hibernate an agent by name |
| **Terminate agent** | `ai-maestro-agents-management` | Delete an agent by name (with confirmation) |
| **List agents** | `ai-maestro-agents-management` | List all registered agents with status |
| **Check agent health** | `ai-maestro-agents-management` | Check health status for an agent |
| **Send message** | `agent-messaging` | Send message to a recipient with subject, content, and priority |
| **Check inbox** | `agent-messaging` | Check for unread messages |
| **Mark read** | `agent-messaging` | Mark a message as read |

---

**END OF DOCUMENT**
