---
name: ecos-spawn-agent
description: "Create and launch a new remote agent in a tmux session using AI Maestro CLI"
argument-hint: "<AGENT_NAME> --dir <PATH> [--task <DESCRIPTION>] [--tags <TAGS>] [--no-session]"
allowed-tools: ["Bash(aimaestro-agent.sh:*)", "Task"]
user-invocable: true
---

# Spawn Agent Command

Create and launch a new remote agent in a dedicated tmux session using the AI Maestro CLI.

## Usage

Use the `ai-maestro-agents-management` skill to create a new agent with the provided arguments.

## What This Command Does

This command creates a new agent session. The operation:
1. Creates the project folder at the specified path
2. Initializes a git repository in the folder
3. Creates a CLAUDE.md template
4. Registers the agent in the agent registry
5. Creates a tmux session and launches Claude Code

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `AGENT_NAME` | Yes | Agent name (alphanumeric, hyphens, underscores only) |
| `--dir <path>` | **Yes** | Working directory path for the agent (REQUIRED) |
| `--task <description>` | No | Task description for the agent |
| `--tags <tag1,tag2>` | No | Comma-separated tags (e.g., `implementer,python,api`) |
| `--no-session` | No | Create agent without tmux session |
| `--force-folder` | No | Use existing folder if it exists |
| `-- <args>` | No | Additional arguments passed to Claude Code |

## Required Claude Code Arguments

**IMPORTANT**: When spawning agents, always include the standard Claude Code flags as program arguments:

| Argument | Purpose |
|----------|---------|
| `continue` | Resume previous session context |
| `--dangerously-skip-permissions` | Skip permission dialogs for automation |
| `--chrome` | Enable Chrome DevTools integration |
| `--add-dir <TEMP_DIR>` | Add temp directory access |

**Platform-specific temp directories:**
- **macOS/Linux**: `/tmp`
- **Windows**: `%TEMP%` or `C:\Users\<user>\AppData\Local\Temp`

## Examples

```bash
# Create a Python implementer agent (macOS/Linux)
/ecos-spawn-agent helper-python --dir ~/projects/myapp \
  --task "Implement user authentication module" \
  --tags "implementer,python,auth"

# Create a tester agent for a specific project
/ecos-spawn-agent helper-tester --dir ~/projects/myapp-tests \
  --task "Write and run unit tests for API endpoints" \
  --tags "tester,pytest"

# Create agent in existing folder
/ecos-spawn-agent helper-docs --dir ~/projects/existing-project \
  --force-folder \
  --task "Generate API documentation" \
  --tags "documenter"
```

## Output Format

```
═══════════════════════════════════════════════════════════════
  Creating Agent: helper-python
═══════════════════════════════════════════════════════════════

  ✓ Directory created: /Users/dev/projects/myapp
  ✓ Git repository initialized
  ✓ CLAUDE.md template created
  ✓ Agent registered in AI Maestro
  ✓ tmux session created: helper-python
  ✓ Claude Code launched

═══════════════════════════════════════════════════════════════
  Agent 'helper-python' is now ONLINE
═══════════════════════════════════════════════════════════════
```

## Post-Spawn Plugin Installation

After spawning, install plugins for the agent using the `ai-maestro-agents-management` skill:
- **Operation**: install plugin on agent
- **Agent**: the newly spawned agent name
- **Plugin**: the plugin to install (e.g., `emasoft-chief-of-staff`)
- **Marketplace**: add marketplace first if needed (e.g., `github:Emasoft/emasoft-plugins`)

**Verify**: plugin appears in the agent's plugin list after restart.

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Agent name already exists" | Duplicate name | Use a different name or delete existing agent first |
| "--dir is required" | Missing directory flag | Always specify `--dir <path>` |
| "Directory already exists" | Folder exists | Use `--force-folder` to use existing folder |
| "Failed to create directory" | Permission issue | Check write permissions on parent directory |

## Related Commands

- `/ecos-staff-status` - View all remote agents
- `/ecos-terminate-agent` - Terminate a remote agent
- `/ecos-hibernate-agent` - Put an agent to sleep
- `/ecos-wake-agent` - Wake a hibernated agent

## CLI Reference

Full documentation: `ai-maestro-agents-management` skill
