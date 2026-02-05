# aimaestro-agent.sh CLI Reference

Complete command-line interface reference for managing Claude Code agent lifecycles.

## Contents

- 1.0 Quick Command Reference
- 2.0 Spawning new agents with aimaestro-agent.sh create
  - 2.1 Basic spawn syntax and required Claude Code arguments
  - 2.2 Spawn with task description and tags
  - 2.3 Spawn using an existing directory (--force-folder)
  - 2.4 Platform-specific temporary directory configuration
  - 2.5 Post-spawn plugin installation workflow
- 3.0 Terminating agents with aimaestro-agent.sh delete
  - 3.1 Graceful termination with confirmation requirement
  - 3.2 When to terminate vs. hibernate
- 4.0 Hibernating agents with aimaestro-agent.sh hibernate
  - 4.1 Saving agent state and freeing resources
  - 4.2 Hibernate workflow and state persistence
- 5.0 Waking hibernated agents with aimaestro-agent.sh wake
  - 5.1 Restoring agent state and resuming operation
  - 5.2 Wake with automatic session attachment
- 6.0 Restarting agents after plugin changes with aimaestro-agent.sh restart
  - 6.1 Hibernate-wake cycle for plugin/marketplace updates
  - 6.2 Restart limitations (cannot restart self)
- 7.0 Updating agent properties with aimaestro-agent.sh update
  - 7.1 Modifying task descriptions
  - 7.2 Updating tag collections
  - 7.3 Adding and removing individual tags
- 8.0 Listing and filtering agents with aimaestro-agent.sh list
  - 8.1 Filtering by agent state (online/offline/hibernated)
  - 8.2 Listing all agents regardless of state
- 9.0 Inspecting agent details with aimaestro-agent.sh show
  - 9.1 Viewing detailed agent information
  - 9.2 JSON output format for scripting
- 10.0 Agent state management and monitoring
  - 10.1 Understanding agent states (online/offline/hibernated)
  - 10.2 Health check procedures for unresponsive agents
  - 10.3 Recovery workflows for offline agents
- 11.0 Error handling and troubleshooting
  - 11.1 Common spawn errors and recovery
  - 11.2 Common lifecycle operation errors and recovery
  - 11.3 Plugin installation errors and recovery
- 12.0 Common workflows
  - 12.1 Complete agent spawn and configuration workflow
  - 12.2 Batch hibernation for resource management
  - 12.3 Mass plugin installation across agent fleet
  - 12.4 Agent recovery from unresponsive state

---

## 1.0 Quick Command Reference

| Command | Purpose |
|---------|---------|
| `aimaestro-agent.sh create <name> --dir <path>` | Create new agent |
| `aimaestro-agent.sh delete <name> --confirm` | Terminate agent |
| `aimaestro-agent.sh hibernate <name>` | Save state and suspend |
| `aimaestro-agent.sh wake <name>` | Restore state and resume |
| `aimaestro-agent.sh restart <name>` | Hibernate + wake (for plugin changes) |
| `aimaestro-agent.sh list` | List all agents |
| `aimaestro-agent.sh show <name>` | Show agent details |
| `aimaestro-agent.sh update <name>` | Update agent properties |
| `aimaestro-agent.sh plugin marketplace add <agent> <marketplace>` | Add marketplace to agent |
| `aimaestro-agent.sh plugin install <agent> <plugin>` | Install plugin on agent |
| `aimaestro-agent.sh plugin list <agent>` | List agent's installed plugins |

---

## 2.0 Spawning new agents with aimaestro-agent.sh create

### 2.1 Basic spawn syntax and required Claude Code arguments

The `create` command spawns a new Claude Code agent instance in a tmux session. All arguments after `--` are passed directly to Claude Code.

**Basic syntax:**
```bash
aimaestro-agent.sh create <name> --dir <path> \
  -- <claude-code-arguments>
```

**Required Claude Code arguments (ALWAYS pass after `--`):**

| Argument | Purpose |
|----------|---------|
| `continue` | Resume previous session context |
| `--dangerously-skip-permissions` | Skip permission dialogs for automation |
| `--chrome` | Enable Chrome DevTools integration |
| `--add-dir <TEMP>` | Add temp directory access |

**Minimal working example:**
```bash
aimaestro-agent.sh create my-agent --dir ~/projects/my-agent \
  -- continue --dangerously-skip-permissions --chrome --add-dir /tmp
```

**What the CLI does automatically:**
1. Creates the directory (or validates if using --force-folder)
2. Initializes a git repository
3. Creates CLAUDE.md template from default or custom template
4. Registers agent in AI Maestro registry
5. Creates tmux session with the agent name
6. Launches Claude Code with the specified arguments

### 2.2 Spawn with task description and tags

Add metadata to your agents for better organization and discoverability:

```bash
aimaestro-agent.sh create <name> \
  --dir <path> \
  --task "Description of work" \
  --tags "role,project,team" \
  -- continue --dangerously-skip-permissions --chrome --add-dir /tmp
```

**Example:**
```bash
aimaestro-agent.sh create code-reviewer-auth \
  --dir ~/projects/auth-review \
  --task "Review authentication module code" \
  --tags "reviewer,auth,security" \
  -- continue --dangerously-skip-permissions --chrome --add-dir /tmp
```

**Task and tags usage:**
- **task**: Human-readable description shown in `list` and `show` commands
- **tags**: Comma-separated labels for filtering and categorization
- Both can be updated later with `aimaestro-agent.sh update`

### 2.3 Spawn using an existing directory (--force-folder)

If you want to spawn an agent in an existing directory (e.g., a pre-configured project folder):

```bash
aimaestro-agent.sh create <name> \
  --dir <existing-path> \
  --force-folder \
  -- continue --dangerously-skip-permissions --chrome --add-dir /tmp
```

**Example:**
```bash
aimaestro-agent.sh create docs-writer \
  --dir ~/projects/documentation \
  --force-folder \
  -- continue --dangerously-skip-permissions --chrome --add-dir /tmp
```

**When to use --force-folder:**
- Directory already exists
- Directory contains project files you want the agent to access
- You've pre-configured CLAUDE.md or other setup files

**Without --force-folder**, the CLI will error if the directory already exists.

### 2.4 Platform-specific temporary directory configuration

The `--add-dir <TEMP>` argument grants Claude Code access to the system's temporary directory.

**Platform-specific temp directories:**

| Platform | Path | Example |
|----------|------|---------|
| macOS | `/tmp` | `--add-dir /tmp` |
| Linux | `/tmp` | `--add-dir /tmp` |
| Windows | `%TEMP%` or full path | `--add-dir %TEMP%` or `--add-dir C:\Users\<user>\AppData\Local\Temp` |

**macOS/Linux example:**
```bash
aimaestro-agent.sh create my-agent --dir ~/projects/my-agent \
  -- continue --dangerously-skip-permissions --chrome --add-dir /tmp
```

**Windows example:**
```bash
aimaestro-agent.sh create my-agent --dir C:\projects\my-agent \
  -- continue --dangerously-skip-permissions --chrome --add-dir %TEMP%
```

### 2.5 Post-spawn plugin installation workflow

After spawning an agent, install plugins using the CLI's plugin management commands.

**Step 1: Add marketplace to the agent**
```bash
aimaestro-agent.sh plugin marketplace add <agent> <marketplace-url>
```

**Step 2: Install plugin on the agent**
```bash
aimaestro-agent.sh plugin install <agent> <plugin-name>
```

**Complete example:**
```bash
# Spawn agent
aimaestro-agent.sh create code-reviewer \
  --dir ~/projects/review \
  --tags "reviewer" \
  -- continue --dangerously-skip-permissions --chrome --add-dir /tmp

# Add Emasoft marketplace
aimaestro-agent.sh plugin marketplace add code-reviewer github:Emasoft/emasoft-plugins

# Install Chief of Staff plugin
aimaestro-agent.sh plugin install code-reviewer emasoft-chief-of-staff

# Verify installation
aimaestro-agent.sh plugin list code-reviewer
```

**Important notes:**
- Each plugin command automatically restarts the target agent (hibernate + wake)
- You cannot modify plugins on your own session (the current agent)
- Marketplace URL format: `github:Owner/repo` or full HTTPS URL

---

## 3.0 Terminating agents with aimaestro-agent.sh delete

### 3.1 Graceful termination with confirmation requirement

The `delete` command permanently terminates an agent and removes it from the registry.

**Syntax:**
```bash
aimaestro-agent.sh delete <name> --confirm
```

**The --confirm flag is REQUIRED** to prevent accidental deletions.

**Example:**
```bash
aimaestro-agent.sh delete test-agent-01 --confirm
```

**What happens during deletion:**
1. Kills the tmux session (if running)
2. Removes agent from AI Maestro registry
3. **Does NOT delete the working directory** (your project files are safe)

### 3.2 When to terminate vs. hibernate

| Use Case | Action | Reason |
|----------|--------|--------|
| Agent no longer needed | `delete --confirm` | Frees registry and session resources |
| Temporary pause (hours/days) | `hibernate` | Preserves state, can resume later |
| Short break (minutes) | Leave running | No action needed |
| Unresponsive/corrupted | `delete --confirm` then recreate | Clean slate recovery |

**IMPORTANT**: Termination is permanent. The agent cannot be restored from the registry. Consider hibernating first if you might need the agent again.

---

## 4.0 Hibernating agents with aimaestro-agent.sh hibernate

### 4.1 Saving agent state and freeing resources

The `hibernate` command suspends an agent while preserving its state.

**Syntax:**
```bash
aimaestro-agent.sh hibernate <name>
```

**Example:**
```bash
aimaestro-agent.sh hibernate docs-writer
```

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

**Example workflow:**
```bash
# Before hibernating, ensure work is committed
tmux send-keys -t docs-writer "git status" C-m
tmux send-keys -t docs-writer "git add . && git commit -m 'Hibernate checkpoint'" C-m

# Hibernate the agent
aimaestro-agent.sh hibernate docs-writer
```

---

## 5.0 Waking hibernated agents with aimaestro-agent.sh wake

### 5.1 Restoring agent state and resuming operation

The `wake` command resumes a hibernated agent.

**Syntax:**
```bash
aimaestro-agent.sh wake <name>
```

**Example:**
```bash
aimaestro-agent.sh wake docs-writer
```

**What happens during wake:**
1. Creates new tmux session with agent name
2. Changes to working directory
3. Launches Claude Code with original arguments
4. Updates registry status to `online`

### 5.2 Wake with automatic session attachment

You can wake an agent and immediately attach to its tmux session:

**Syntax:**
```bash
aimaestro-agent.sh wake <name> --attach
```

**Example:**
```bash
aimaestro-agent.sh wake docs-writer --attach
```

This is useful when you want to interact with the agent immediately after waking it.

**To detach from the session later:**
- Press `Ctrl+B`, then `D` (standard tmux detach)

---

## 6.0 Restarting agents after plugin changes with aimaestro-agent.sh restart

### 6.1 Hibernate-wake cycle for plugin/marketplace updates

The `restart` command performs a hibernate-wake cycle, which is required after plugin or marketplace changes.

**Syntax:**
```bash
aimaestro-agent.sh restart <name>
```

**Example:**
```bash
# After installing a plugin
aimaestro-agent.sh plugin install code-reviewer emasoft-chief-of-staff

# No manual restart needed - plugin commands auto-restart

# But if you manually edited plugin files
aimaestro-agent.sh restart code-reviewer
```

**With custom wait time:**
```bash
# Wait 5 seconds between hibernate and wake
aimaestro-agent.sh restart code-reviewer --wait 5
```

**What restart does:**
1. Hibernates the agent (saves state, kills session)
2. Waits (default 2 seconds, customizable with --wait)
3. Wakes the agent (recreates session, launches Claude Code)

**Why restart is needed:**
- Claude Code loads plugins on startup only
- Plugin/marketplace changes require a full restart to take effect
- Restart is faster than manual hibernate + wake

### 6.2 Restart limitations (cannot restart self)

**You cannot restart the current agent** (the one executing the command).

**Example of the error:**
```bash
# If executed from code-reviewer agent
aimaestro-agent.sh restart code-reviewer

# Output: ERROR: Cannot restart current session
```

**Workaround:**
1. Exit Claude Code manually
2. Relaunch with `aimaestro-agent.sh wake code-reviewer`

**Or from another agent:**
```bash
# From orchestrator-master, restart code-reviewer
aimaestro-agent.sh restart code-reviewer
```

---

## 7.0 Updating agent properties with aimaestro-agent.sh update

### 7.1 Modifying task descriptions

Change the task description displayed in `list` and `show` commands:

**Syntax:**
```bash
aimaestro-agent.sh update <name> --task "New task description"
```

**Example:**
```bash
aimaestro-agent.sh update code-reviewer --task "Review authentication and authorization modules"
```

### 7.2 Updating tag collections

Replace the entire tag collection:

**Syntax:**
```bash
aimaestro-agent.sh update <name> --tags "tag1,tag2,tag3"
```

**Example:**
```bash
aimaestro-agent.sh update code-reviewer --tags "reviewer,security,auth,critical"
```

**Note**: This replaces ALL existing tags.

### 7.3 Adding and removing individual tags

Add a single tag without replacing existing tags:

**Syntax:**
```bash
aimaestro-agent.sh update <name> --add-tag "new-tag"
```

**Example:**
```bash
aimaestro-agent.sh update code-reviewer --add-tag "priority"
```

Remove a single tag:

**Syntax:**
```bash
aimaestro-agent.sh update <name> --remove-tag "old-tag"
```

**Example:**
```bash
aimaestro-agent.sh update code-reviewer --remove-tag "deprecated"
```

---

## 8.0 Listing and filtering agents with aimaestro-agent.sh list

### 8.1 Filtering by agent state (online/offline/hibernated)

**List all agents:**
```bash
aimaestro-agent.sh list --status all
```

**List online agents only:**
```bash
aimaestro-agent.sh list --status online
```

**List offline agents only:**
```bash
aimaestro-agent.sh list --status offline
```

**List hibernated agents only:**
```bash
aimaestro-agent.sh list --status hibernated
```

### 8.2 Listing all agents regardless of state

**Default (shows all):**
```bash
aimaestro-agent.sh list
```

**Output format:**
```
NAME                STATUS      TASK
code-reviewer       online      Review authentication module
docs-writer         hibernated  Write API documentation
test-runner-001     offline     Run integration tests
```

**Get just agent names (for scripting):**
```bash
aimaestro-agent.sh list --status online --format names
```

**Output:**
```
code-reviewer
orchestrator-master
```

---

## 9.0 Inspecting agent details with aimaestro-agent.sh show

### 9.1 Viewing detailed agent information

**Syntax:**
```bash
aimaestro-agent.sh show <name>
```

**Example:**
```bash
aimaestro-agent.sh show code-reviewer
```

**Example output:**
```
Agent: code-reviewer
Status: online
Directory: /Users/dev/projects/auth-review
Task: Review authentication module code
Tags: reviewer, auth, security
Plugins: emasoft-chief-of-staff
Marketplaces: github:Emasoft/emasoft-plugins
Created: 2026-02-01 14:30:00
Last updated: 2026-02-05 09:15:00
```

### 9.2 JSON output format for scripting

**Syntax:**
```bash
aimaestro-agent.sh show <name> --format json
```

**Example:**
```bash
aimaestro-agent.sh show code-reviewer --format json | jq .
```

**Example JSON output:**
```json
{
  "name": "code-reviewer",
  "status": "online",
  "directory": "/Users/dev/projects/auth-review",
  "task": "Review authentication module code",
  "tags": ["reviewer", "auth", "security"],
  "plugins": ["emasoft-chief-of-staff"],
  "marketplaces": ["github:Emasoft/emasoft-plugins"],
  "created": "2026-02-01T14:30:00Z",
  "updated": "2026-02-05T09:15:00Z"
}
```

**Use with jq for status checks:**
```bash
# Check if agent is online (exit code based)
aimaestro-agent.sh show code-reviewer --format json | jq -e '.status == "online"'
```

---

## 10.0 Agent state management and monitoring

### 10.1 Understanding agent states (online/offline/hibernated)

| State | Description | tmux Session | Registry Entry |
|-------|-------------|--------------|----------------|
| **online** | Running in tmux session | Exists | status = online |
| **offline** | Session not running | Does not exist | status = offline |
| **hibernated** | Explicitly suspended | Does not exist | status = hibernated |

**State transitions:**
- `create` → online
- `hibernate` → hibernated
- `wake` → online (from hibernated)
- `delete` → (removed from registry)
- Session crash → offline (automatic)

### 10.2 Health check procedures for unresponsive agents

**Step 1: Check agent status**
```bash
aimaestro-agent.sh show <agent-name>
```

**Step 2: Interpret status**

| Status | Likely Cause | Next Action |
|--------|--------------|-------------|
| online | Agent running but not responding | Check tmux session, inspect logs |
| offline | Session crashed | Try wake command |
| hibernated | Intentionally suspended | Wake to resume |

**Step 3: Check tmux session directly**
```bash
tmux list-sessions | grep <agent-name>
```

**Step 4: Inspect Claude Code logs (if session exists)**
```bash
tmux capture-pane -t <agent-name> -p | tail -50
```

### 10.3 Recovery workflows for offline agents

**If agent is offline:**

**Option 1: Try waking**
```bash
aimaestro-agent.sh wake <agent-name>
```

**Option 2: Check if actually hibernated**
```bash
aimaestro-agent.sh show <agent-name> | grep hibernated
```

If hibernated, use wake. If offline due to crash:

**Option 3: Delete and recreate**
```bash
# Save directory path first
dir=$(aimaestro-agent.sh show <agent-name> --format json | jq -r .directory)

# Delete
aimaestro-agent.sh delete <agent-name> --confirm

# Recreate with same configuration
aimaestro-agent.sh create <agent-name> \
  --dir "$dir" \
  --force-folder \
  --task "Original task" \
  --tags "original,tags" \
  -- continue --dangerously-skip-permissions --chrome --add-dir /tmp
```

---

## 11.0 Error handling and troubleshooting

### 11.1 Common spawn errors and recovery

| Error | Cause | Solution |
|-------|-------|----------|
| "Directory exists" | Path already exists | Use `--force-folder` flag |
| "Agent name exists" | Name already in registry | Choose different name or delete first: `aimaestro-agent.sh delete <name> --confirm` |
| "tmux session exists" | Orphaned tmux session | Kill session manually: `tmux kill-session -t <name>` |
| "Claude Code not found" | Binary not in PATH | Install Claude Code or add to PATH |

**Example recovery (directory exists):**
```bash
# Original command fails
aimaestro-agent.sh create my-agent --dir ~/existing-project

# ERROR: Directory exists

# Solution: use --force-folder
aimaestro-agent.sh create my-agent --dir ~/existing-project --force-folder
```

### 11.2 Common lifecycle operation errors and recovery

| Error | Cause | Solution |
|-------|-------|----------|
| "Agent not found" | Not in registry | Already deleted or typo in name |
| "Agent not online" (hibernate) | Already stopped | No action needed, already hibernated/offline |
| "Agent not hibernated" (wake) | Agent is online or offline | Check status first: `aimaestro-agent.sh show <name>` |
| "Cannot restart self" (restart) | Trying to restart current agent | Exit and relaunch Claude Code manually |

**Example recovery (wake fails):**
```bash
# Wake command fails
aimaestro-agent.sh wake my-agent

# ERROR: Agent not hibernated

# Check actual status
aimaestro-agent.sh show my-agent

# If online: no action needed
# If offline: agent crashed, recreate or check logs
```

### 11.3 Plugin installation errors and recovery

| Error | Cause | Solution |
|-------|-------|----------|
| "Marketplace not found" | Marketplace not added to agent | Add marketplace first: `aimaestro-agent.sh plugin marketplace add <agent> <url>` |
| "Plugin not found" | Plugin doesn't exist in marketplace | Check marketplace contents, verify plugin name |
| "Cannot modify self" | Trying to install plugin on current agent | Use different agent or exit and manually install |

**Example recovery (marketplace not found):**
```bash
# Install fails
aimaestro-agent.sh plugin install my-agent emasoft-chief-of-staff

# ERROR: Marketplace not found

# Solution: add marketplace first
aimaestro-agent.sh plugin marketplace add my-agent github:Emasoft/emasoft-plugins

# Now install plugin
aimaestro-agent.sh plugin install my-agent emasoft-chief-of-staff
```

---

## 12.0 Common workflows

### 12.1 Complete agent spawn and configuration workflow

**Full workflow from spawn to ready:**

```bash
# Step 1: Spawn agent
aimaestro-agent.sh create code-reviewer-auth \
  --dir ~/projects/auth-review \
  --task "Review authentication module code" \
  --tags "reviewer,auth,security" \
  -- continue --dangerously-skip-permissions --chrome --add-dir /tmp

# Step 2: Add marketplace (auto-restarts agent)
aimaestro-agent.sh plugin marketplace add code-reviewer-auth github:Emasoft/emasoft-plugins

# Step 3: Install plugin (auto-restarts agent)
aimaestro-agent.sh plugin install code-reviewer-auth emasoft-chief-of-staff

# Step 4: Verify configuration
aimaestro-agent.sh show code-reviewer-auth

# Step 5: Check plugin installation
aimaestro-agent.sh plugin list code-reviewer-auth

# Agent is now fully configured and ready
```

### 12.2 Batch hibernation for resource management

**Hibernate all online agents except critical ones:**

```bash
# Get list of online agents
agents=$(aimaestro-agent.sh list --status online --format names)

# Define critical agents to keep running
critical="orchestrator-master monitoring-agent"

# Hibernate all non-critical agents
for agent in $agents; do
  if ! echo "$critical" | grep -q "$agent"; then
    echo "Hibernating $agent..."
    aimaestro-agent.sh hibernate "$agent"
  fi
done

# Verify
aimaestro-agent.sh list --status hibernated
```

**Wake all hibernated agents:**

```bash
# Get hibernated agents
hibernated=$(aimaestro-agent.sh list --status hibernated --format names)

# Wake each
for agent in $hibernated; do
  echo "Waking $agent..."
  aimaestro-agent.sh wake "$agent"
done

# Verify
aimaestro-agent.sh list --status online
```

### 12.3 Mass plugin installation across agent fleet

**Install plugin on all online agents:**

```bash
# Get list of online agents
agents=$(aimaestro-agent.sh list --status online --format names)

# Add marketplace to each (ignore if already exists)
for agent in $agents; do
  aimaestro-agent.sh plugin marketplace add "$agent" github:Emasoft/emasoft-plugins 2>/dev/null || true
done

# Install plugin on each (auto-restarts)
for agent in $agents; do
  echo "Installing on $agent..."
  aimaestro-agent.sh plugin install "$agent" emasoft-chief-of-staff
done

# Verify installation
for agent in $agents; do
  echo "--- $agent ---"
  aimaestro-agent.sh plugin list "$agent" | grep chief-of-staff
done
```

### 12.4 Agent recovery from unresponsive state

**Complete recovery procedure:**

```bash
# Step 1: Check agent status
agent_name="test-runner-003"
aimaestro-agent.sh show "$agent_name"

# Step 2: If offline, try waking
if aimaestro-agent.sh show "$agent_name" --format json | jq -e '.status == "offline"'; then
  echo "Agent is offline, attempting wake..."
  aimaestro-agent.sh wake "$agent_name"
fi

# Step 3: If wake fails, delete and recreate
if ! aimaestro-agent.sh show "$agent_name" --format json | jq -e '.status == "online"'; then
  echo "Wake failed, recreating agent..."

  # Save configuration
  dir=$(aimaestro-agent.sh show "$agent_name" --format json | jq -r .directory)
  task=$(aimaestro-agent.sh show "$agent_name" --format json | jq -r .task)
  tags=$(aimaestro-agent.sh show "$agent_name" --format json | jq -r '.tags | join(",")')

  # Delete
  aimaestro-agent.sh delete "$agent_name" --confirm

  # Recreate
  aimaestro-agent.sh create "$agent_name" \
    --dir "$dir" \
    --force-folder \
    --task "$task" \
    --tags "$tags" \
    -- continue --dangerously-skip-permissions --chrome --add-dir /tmp

  # Reinstall plugins
  aimaestro-agent.sh plugin marketplace add "$agent_name" github:Emasoft/emasoft-plugins
  aimaestro-agent.sh plugin install "$agent_name" emasoft-chief-of-staff
fi

# Step 4: Verify recovery
aimaestro-agent.sh show "$agent_name"
```

---

## Exit Codes

All `aimaestro-agent.sh` commands use standard exit codes:

| Code | Meaning | Example |
|------|---------|---------|
| 0 | Success | Command completed successfully |
| 1 | General error | Invalid arguments, command failed |
| 2 | Agent not found | Agent doesn't exist in registry |
| 3 | Permission denied | Cannot modify current agent |
| 4 | State conflict | Cannot wake online agent, cannot hibernate offline agent |

**Use in scripts:**
```bash
if aimaestro-agent.sh show my-agent &>/dev/null; then
  echo "Agent exists"
else
  echo "Agent not found"
fi
```
