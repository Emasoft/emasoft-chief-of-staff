# Agent Lifecycle Operations Reference

Complete reference for managing Claude Code agent lifecycles using the `ai-maestro-agents-management` skill.

## Contents

- 1.0 Quick Operations Reference
- 2.0 Creating new agents
  - 2.1 Basic creation with required Claude Code arguments
  - 2.2 Creation with task description and tags
  - 2.3 Creation using an existing directory
  - 2.4 Platform-specific temporary directory configuration
  - 2.5 Post-creation plugin installation workflow
- 3.0 Terminating agents
  - 3.1 Graceful termination with confirmation
  - 3.2 When to terminate vs. hibernate
- 4.0 Hibernating agents
  - 4.1 Saving agent state and freeing resources
  - 4.2 Hibernate workflow and state persistence
- 5.0 Waking hibernated agents
  - 5.1 Restoring agent state and resuming operation
  - 5.2 Wake with automatic session attachment
- 6.0 Restarting agents after plugin changes
  - 6.1 Hibernate-wake cycle for plugin/marketplace updates
  - 6.2 Restart limitations (cannot restart self)
- 7.0 Updating agent properties
  - 7.1 Modifying task descriptions
  - 7.2 Updating tag collections
  - 7.3 Adding and removing individual tags
- 8.0 Listing and filtering agents
  - 8.1 Filtering by agent state (online/offline/hibernated)
  - 8.2 Listing all agents regardless of state
- 9.0 Inspecting agent details
  - 9.1 Viewing detailed agent information
  - 9.2 JSON output format for scripting
- 10.0 Agent state management and monitoring
  - 10.1 Understanding agent states (online/offline/hibernated)
  - 10.2 Health check procedures for unresponsive agents
  - 10.3 Recovery workflows for offline agents
- 11.0 Error handling and troubleshooting
  - 11.1 Common creation errors and recovery
  - 11.2 Common lifecycle operation errors and recovery
  - 11.3 Plugin installation errors and recovery
- 12.0 Common workflows
  - 12.1 Complete agent creation and configuration workflow
  - 12.2 Batch hibernation for resource management
  - 12.3 Mass plugin installation across agent fleet
  - 12.4 Agent recovery from unresponsive state

---

## 1.0 Quick Operations Reference

All operations below are performed using the `ai-maestro-agents-management` skill.

| Operation | Description |
|-----------|-------------|
| Create agent | Create a new agent with a name, working directory, and Claude Code arguments |
| Terminate agent | Permanently remove an agent (requires confirmation) |
| Hibernate agent | Save state and suspend an agent |
| Wake agent | Restore state and resume a hibernated agent |
| Restart agent | Hibernate + wake cycle (for plugin changes) |
| List agents | List all agents, optionally filtered by status |
| Show agent | Display detailed agent information |
| Update agent | Modify agent task description or tags |
| Add marketplace | Register a plugin marketplace on an agent |
| Install plugin | Install a plugin from a marketplace on an agent |
| List plugins | List plugins installed on an agent |

---

## 2.0 Creating new agents

### 2.1 Basic creation with required Claude Code arguments

Use the `ai-maestro-agents-management` skill to create a new agent. Provide:

- **Name**: unique identifier for the agent
- **Directory**: working directory path for the agent
- **Claude Code arguments**: the following arguments must always be included:

| Argument | Purpose |
|----------|---------|
| `continue` | Resume previous session context |
| `--dangerously-skip-permissions` | Skip permission dialogs for automation |
| `--chrome` | Enable Chrome DevTools integration |
| `--add-dir <TEMP>` | Add temp directory access |

**What happens automatically during creation:**
1. Creates the directory (or validates if using existing directory)
2. Initializes a git repository
3. Creates CLAUDE.md template from default or custom template
4. Registers agent in AI Maestro registry
5. Creates tmux session with the agent name
6. Launches Claude Code with the specified arguments

**Verify**: the new agent appears in the agent list with "online" status.

### 2.2 Creation with task description and tags

When creating an agent, you can include metadata for organization and discoverability:

- **Task**: human-readable description of the agent's work (shown in list and show operations)
- **Tags**: comma-separated labels for filtering and categorization

Both can be updated later using the update operation.

### 2.3 Creation using an existing directory

If you want to create an agent in an existing directory (e.g., a pre-configured project folder), specify that the existing directory should be used (force-folder option).

**When to use this:**
- Directory already exists
- Directory contains project files you want the agent to access
- You have pre-configured CLAUDE.md or other setup files

**Without force-folder**, the creation will error if the directory already exists.

### 2.4 Platform-specific temporary directory configuration

The `--add-dir <TEMP>` argument grants Claude Code access to the system's temporary directory.

**Platform-specific temp directories:**

| Platform | Path |
|----------|------|
| macOS | `/tmp` |
| Linux | `/tmp` |
| Windows | `%TEMP%` or `C:\Users\<user>\AppData\Local\Temp` |

### 2.5 Post-creation plugin installation workflow

After creating an agent, install plugins using the `ai-maestro-agents-management` skill:

1. **Add marketplace** to the agent (specify the marketplace URL)
2. **Install plugin** on the agent (specify the plugin name)
3. **Verify** using the list plugins operation

**Important notes:**
- Each plugin operation automatically restarts the target agent (hibernate + wake)
- You cannot modify plugins on your own session (the current agent)
- Marketplace URL format: `github:Owner/repo` or full HTTPS URL

---

## 3.0 Terminating agents

### 3.1 Graceful termination with confirmation

Use the `ai-maestro-agents-management` skill to terminate an agent. Confirmation is required to prevent accidental deletions.

**What happens during termination:**
1. Kills the tmux session (if running)
2. Removes agent from AI Maestro registry
3. **Does NOT delete the working directory** (project files are safe)

### 3.2 When to terminate vs. hibernate

| Use Case | Action | Reason |
|----------|--------|--------|
| Agent no longer needed | Terminate | Frees registry and session resources |
| Temporary pause (hours/days) | Hibernate | Preserves state, can resume later |
| Short break (minutes) | Leave running | No action needed |
| Unresponsive/corrupted | Terminate then recreate | Clean slate recovery |

**IMPORTANT**: Termination is permanent. The agent cannot be restored from the registry. Consider hibernating first if you might need the agent again.

---

## 4.0 Hibernating agents

### 4.1 Saving agent state and freeing resources

Use the `ai-maestro-agents-management` skill to hibernate an agent.

### 4.2 Hibernate workflow and state persistence

**What happens during hibernation:**
1. Agent state is saved to registry
2. Tmux session is terminated (kills Claude Code process)
3. Registry status updated to `hibernated`
4. System resources (CPU, memory) are freed

**What is preserved:**
- Agent name
- Working directory path
- Task description
- Tags
- Installed plugins and marketplaces
- Claude Code configuration

**What is NOT preserved:**
- Conversation history (Claude Code limitation)
- In-memory state
- Unsaved file changes (commit before hibernating!)

**Before hibernating**, ensure work is committed (use `git add . && git commit` in the agent's tmux session).

---

## 5.0 Waking hibernated agents

### 5.1 Restoring agent state and resuming operation

Use the `ai-maestro-agents-management` skill to wake a hibernated agent.

**What happens during wake:**
1. Creates new tmux session with agent name
2. Changes to working directory
3. Launches Claude Code with original arguments
4. Updates registry status to `online`

### 5.2 Wake with automatic session attachment

You can wake an agent and immediately attach to its tmux session by specifying the attach option.

This is useful when you want to interact with the agent immediately after waking it.

**To detach from the session later:**
- Press `Ctrl+B`, then `D` (standard tmux detach)

---

## 6.0 Restarting agents after plugin changes

### 6.1 Hibernate-wake cycle for plugin/marketplace updates

Use the `ai-maestro-agents-management` skill to restart an agent. This performs a hibernate-wake cycle, which is required after plugin or marketplace changes.

You can optionally specify a custom wait time between hibernate and wake (default 2 seconds).

**Why restart is needed:**
- Claude Code loads plugins on startup only
- Plugin/marketplace changes require a full restart to take effect
- Restart is faster than manual hibernate + wake

### 6.2 Restart limitations (cannot restart self)

**You cannot restart the current agent** (the one executing the command).

**Workaround:**
1. Exit Claude Code manually
2. Use the `ai-maestro-agents-management` skill to wake your own agent from another agent

**Or from another agent:** use the skill to restart the target agent.

---

## 7.0 Updating agent properties

### 7.1 Modifying task descriptions

Use the `ai-maestro-agents-management` skill to update an agent's task description (shown in list and show operations).

### 7.2 Updating tag collections

Use the skill to replace the entire tag collection on an agent (comma-separated labels).

**Note**: This replaces ALL existing tags.

### 7.3 Adding and removing individual tags

Use the skill to add a single tag without replacing existing tags, or to remove a single tag.

---

## 8.0 Listing and filtering agents

### 8.1 Filtering by agent state (online/offline/hibernated)

Use the `ai-maestro-agents-management` skill to list agents, optionally filtering by status:
- **online**: currently running agents
- **offline**: crashed or stopped agents
- **hibernated**: explicitly suspended agents
- **all**: all agents regardless of state

### 8.2 Listing all agents regardless of state

The default list operation shows all agents. Output includes name, status, and task for each agent.

You can also request just agent names (for scripting purposes).

---

## 9.0 Inspecting agent details

### 9.1 Viewing detailed agent information

Use the `ai-maestro-agents-management` skill to show detailed information about a specific agent, including:
- Name and status
- Working directory
- Task description
- Tags
- Installed plugins and marketplaces
- Creation and last update timestamps

### 9.2 JSON output format for scripting

You can request the agent details in JSON format for programmatic use.

---

## 10.0 Agent state management and monitoring

### 10.1 Understanding agent states (online/offline/hibernated)

| State | Description | tmux Session | Registry Entry |
|-------|-------------|--------------|----------------|
| **online** | Running in tmux session | Exists | status = online |
| **offline** | Session not running | Does not exist | status = offline |
| **hibernated** | Explicitly suspended | Does not exist | status = hibernated |

**State transitions:**
- Create -> online
- Hibernate -> hibernated
- Wake -> online (from hibernated)
- Terminate -> (removed from registry)
- Session crash -> offline (automatic)

### 10.2 Health check procedures for unresponsive agents

**Step 1:** Use the `ai-maestro-agents-management` skill to show agent details and check status.

**Step 2: Interpret status**

| Status | Likely Cause | Next Action |
|--------|--------------|-------------|
| online | Agent running but not responding | Check tmux session, inspect logs |
| offline | Session crashed | Try wake operation |
| hibernated | Intentionally suspended | Wake to resume |

**Step 3:** Check tmux session directly: `tmux list-sessions | grep <agent-name>`

**Step 4:** Inspect Claude Code logs (if session exists): `tmux capture-pane -t <agent-name> -p | tail -50`

### 10.3 Recovery workflows for offline agents

**If agent is offline:**

1. **Try waking**: Use the `ai-maestro-agents-management` skill to wake the agent
2. **Check if actually hibernated**: Use the skill to show agent details and check for hibernated status
3. **If wake fails, delete and recreate**:
   - Save the agent's directory path and configuration using the show operation
   - Use the skill to terminate the agent (with confirmation)
   - Use the skill to create a new agent with the same name, directory (force-folder), task, and tags
   - Reinstall plugins using the skill

---

## 11.0 Error handling and troubleshooting

### 11.1 Common creation errors and recovery

| Error | Cause | Solution |
|-------|-------|----------|
| "Directory exists" | Path already exists | Use the force-folder option |
| "Agent name exists" | Name already in registry | Choose different name or terminate first |
| "tmux session exists" | Orphaned tmux session | Kill session manually: `tmux kill-session -t <name>` |
| "Claude Code not found" | Binary not in PATH | Install Claude Code or add to PATH |

### 11.2 Common lifecycle operation errors and recovery

| Error | Cause | Solution |
|-------|-------|----------|
| "Agent not found" | Not in registry | Already deleted or typo in name |
| "Agent not online" (hibernate) | Already stopped | No action needed, already hibernated/offline |
| "Agent not hibernated" (wake) | Agent is online or offline | Check status first using the show operation |
| "Cannot restart self" (restart) | Trying to restart current agent | Exit and relaunch Claude Code manually |

### 11.3 Plugin installation errors and recovery

| Error | Cause | Solution |
|-------|-------|----------|
| "Marketplace not found" | Marketplace not added to agent | Add marketplace first using the skill |
| "Plugin not found" | Plugin does not exist in marketplace | Check marketplace contents, verify plugin name |
| "Cannot modify self" | Trying to install plugin on current agent | Use different agent or exit and manually install |

---

## 12.0 Common workflows

### 12.1 Complete agent creation and configuration workflow

**Full workflow from creation to ready:**

1. **Create agent**: Use the `ai-maestro-agents-management` skill to create the agent with name, directory, task, and tags
2. **Add marketplace**: Use the skill to add the Emasoft marketplace to the agent (auto-restarts agent)
3. **Install plugin**: Use the skill to install the required plugin on the agent (auto-restarts agent)
4. **Verify configuration**: Use the skill to show agent details
5. **Check plugin installation**: Use the skill to list plugins on the agent

**Verify**: agent is online with the correct plugins installed.

### 12.2 Batch hibernation for resource management

**Hibernate all online agents except critical ones:**

1. Use the `ai-maestro-agents-management` skill to list online agents
2. Define critical agents to keep running (e.g., orchestrator, monitoring)
3. For each non-critical agent, use the skill to hibernate it
4. Use the skill to list hibernated agents to verify

**Wake all hibernated agents:**

1. Use the skill to list hibernated agents
2. For each hibernated agent, use the skill to wake it
3. Use the skill to list online agents to verify

### 12.3 Mass plugin installation across agent fleet

**Install plugin on all online agents:**

1. Use the `ai-maestro-agents-management` skill to list online agents
2. For each agent, use the skill to add the marketplace (if not already added)
3. For each agent, use the skill to install the plugin (auto-restarts)
4. For each agent, use the skill to list plugins and verify installation

### 12.4 Agent recovery from unresponsive state

**Complete recovery procedure:**

1. Use the `ai-maestro-agents-management` skill to show agent status
2. If offline, use the skill to try waking the agent
3. If wake fails, save configuration (directory, task, tags) from the show operation
4. Use the skill to terminate the agent (with confirmation)
5. Use the skill to create a new agent with the same configuration (force-folder)
6. Use the skill to add marketplace and install plugins
7. Use the skill to show agent details and verify recovery

---

## Exit Codes

All agent lifecycle operations use standard exit codes:

| Code | Meaning |
|------|---------|
| 0 | Success - command completed successfully |
| 1 | General error - invalid arguments or command failed |
| 2 | Agent not found - agent does not exist in registry |
| 3 | Permission denied - cannot modify current agent |
| 4 | State conflict - cannot wake online agent, cannot hibernate offline agent |
