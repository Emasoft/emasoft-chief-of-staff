---
operation: configure-local-plugin
procedure: proc-create-team
workflow-instruction: Step 4 - Team Creation
parent-skill: ecos-plugin-management
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Configure Local Plugin Directory

## When to Use

- Developing a new plugin locally
- Testing plugin changes before publishing
- Using plugins not in any marketplace
- Loading multiple plugins simultaneously during development

## Prerequisites

- Plugin source directory exists with correct structure
- Write permissions to plugin directory
- Claude Code CLI available

## Procedure

### Step 1: Verify Plugin Directory Structure

Ensure the plugin has the correct structure:

```
my-plugin/
├── .claude-plugin/           # Metadata directory
│   └── plugin.json          # REQUIRED: plugin manifest
├── commands/                 # Slash commands (at ROOT!)
│   └── my-command.md
├── agents/                   # Agent definitions (at ROOT!)
│   └── my-agent.md
├── skills/                   # Agent skills (at ROOT!)
│   └── my-skill/
│       └── SKILL.md
├── hooks/                    # Hook configurations (at ROOT!)
│   └── hooks.json
├── scripts/                  # Hook and utility scripts
│   └── my-hook.py
└── README.md
```

**CRITICAL**: Components go at ROOT level, NOT inside `.claude-plugin/`!

### Step 2: Verify plugin.json Manifest

Check `.claude-plugin/plugin.json` has required fields:

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What this plugin does",
  "author": {"name": "Author", "email": "email@example.com"},
  "agents": [
    "./agents/my-agent.md"
  ]
}
```

**Note**: `agents` must be an array of `.md` file paths, not a directory.

### Step 3: Make Scripts Executable

```bash
chmod +x /path/to/my-plugin/scripts/*.sh
chmod +x /path/to/my-plugin/scripts/*.py
```

### Step 4: Launch Claude Code with --plugin-dir

```bash
# Single local plugin
claude --plugin-dir /path/to/my-plugin

# Multiple local plugins
claude --plugin-dir /path/to/plugin-a --plugin-dir /path/to/plugin-b
```

### Step 5: Verify Plugin Loaded

```bash
# Check hooks are registered
/hooks

# Check commands are available
/<plugin-command>

# Debug if needed
claude --debug
```

## Checklist

Copy this checklist and track your progress:

- [ ] Verify .claude-plugin/plugin.json exists
- [ ] Verify plugin.json has required fields
- [ ] Verify components are at ROOT (not in .claude-plugin/)
- [ ] Verify agents field is array of .md paths
- [ ] Make all scripts executable
- [ ] Launch with --plugin-dir flag
- [ ] Verify hooks are registered
- [ ] Verify commands are available
- [ ] Test basic functionality

## Examples

### Example: Setting Up Local Development Plugin

```bash
# Check structure
ls -la /path/to/my-plugin/
# Should show: .claude-plugin/, commands/, agents/, hooks/, scripts/

# Check manifest
cat /path/to/my-plugin/.claude-plugin/plugin.json
# Should show valid JSON with name, version, etc.

# Make scripts executable
chmod +x /path/to/my-plugin/scripts/*.sh

# Launch
claude --plugin-dir /path/to/my-plugin

# Verify
/hooks
# Should list hooks from my-plugin
```

### Example: Loading Multiple Development Plugins

```bash
# Launch with two plugins
claude \
  --plugin-dir /Users/dev/projects/plugin-alpha \
  --plugin-dir /Users/dev/projects/plugin-beta

# Verify both loaded
/hooks
# Should show hooks from both plugins
```

### Example: Copying Plugin for Agent

When spawning an agent with a local plugin:

```bash
SESSION_NAME="eoa-test-orchestrator"
PLUGIN_SOURCE="/Users/dev/projects/emasoft-orchestrator-agent"
PLUGIN_DEST="$HOME/agents/$SESSION_NAME/.claude/plugins/emasoft-orchestrator-agent"

# Create destination
mkdir -p "$(dirname "$PLUGIN_DEST")"

# Copy plugin
cp -r "$PLUGIN_SOURCE" "$PLUGIN_DEST"

# Spawn agent with copied plugin
# Use the ai-maestro-agents-management skill to create the agent
# with the specified session name, working directory, task, and plugin directory
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Plugin not loading | Wrong path to --plugin-dir | Use absolute path, verify directory exists |
| plugin.json not found | Missing or wrong location | Must be at `.claude-plugin/plugin.json` |
| Commands not available | Components in wrong directory | Move to ROOT, not inside .claude-plugin/ |
| Hooks not firing | Scripts not executable | Run `chmod +x` on all scripts |
| Manifest invalid | JSON syntax error | Validate JSON with `jq . plugin.json` |
| Agents not found | agents field is directory not array | Change to array of .md file paths |
| Duplicate hook error | Same hook defined multiple times | Check hooks.json for duplicates |

## Related Operations

- [op-install-plugin-marketplace.md](op-install-plugin-marketplace.md) - Marketplace install
- [op-validate-plugin.md](op-validate-plugin.md) - Validate structure
- [op-restart-agent-plugin.md](op-restart-agent-plugin.md) - Restart after changes
