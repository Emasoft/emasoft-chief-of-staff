---
name: ecos-spawn-agent
description: "Create and launch a new remote agent in a tmux session using AI Maestro CLI"
argument-hint: "<AGENT_NAME> --dir <PATH> [--task <DESCRIPTION>] [--tags <TAGS>] [--no-session]"
allowed-tools: ["Bash(aimaestro-agent.sh:*)"]
user-invocable: true
---

# Spawn Agent Command

Create and launch a new remote agent in a dedicated tmux session using the AI Maestro CLI.

## Usage

```!
aimaestro-agent.sh create $ARGUMENTS
```

## AI Maestro CLI Integration

This command uses the **aimaestro-agent.sh** CLI tool for agent lifecycle management. The CLI:
1. Creates the project folder at the specified path
2. Initializes a git repository in the folder
3. Creates a CLAUDE.md template
4. Registers the agent in AI Maestro
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

**IMPORTANT**: Always pass these arguments after `--` when spawning agents:

```bash
-- continue --dangerously-skip-permissions --chrome --add-dir <TEMP_DIR>
```

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
  --tags "implementer,python,auth" \
  -- continue --dangerously-skip-permissions --chrome --add-dir /tmp

# Create a tester agent for a specific project
/ecos-spawn-agent helper-tester --dir ~/projects/myapp-tests \
  --task "Write and run unit tests for API endpoints" \
  --tags "tester,pytest" \
  -- continue --dangerously-skip-permissions --chrome --add-dir /tmp

# Create agent in existing folder
/ecos-spawn-agent helper-docs --dir ~/projects/existing-project \
  --force-folder \
  --task "Generate API documentation" \
  --tags "documenter" \
  -- continue --dangerously-skip-permissions --chrome --add-dir /tmp

# Windows example
/ecos-spawn-agent helper-win --dir C:\projects\myapp \
  --task "Build Windows application" \
  --tags "implementer,windows" \
  -- continue --dangerously-skip-permissions --chrome --add-dir %TEMP%
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

After spawning, install plugins for the agent:

```bash
# Install a plugin on the new agent (auto-restarts the agent)
aimaestro-agent.sh plugin install helper-python emasoft-chief-of-staff

# Add a marketplace first if needed
aimaestro-agent.sh plugin marketplace add helper-python github:Emasoft/emasoft-plugins
```

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

Full documentation: `ai-maestro-agents-management` skill or run `aimaestro-agent.sh --help`
