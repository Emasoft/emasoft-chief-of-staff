---
name: ecos-configure-plugins
description: "Configure plugins for an agent's project by adding, removing, or managing plugin scope"
argument-hint: "<SESSION_NAME> --add PLUGIN [--remove PLUGIN] [--scope local|project]"
user-invocable: true
allowed-tools: ["Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/ecos_configure_plugins.py:*)"]
---

# Configure Plugins Command

Configure plugins for a specific agent session. Add or remove plugins and manage their scope (local or project).

## Usage

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ecos_configure_plugins.py" $ARGUMENTS
```

## What This Command Does

1. **Resolves Target Agent**
   - Resolves SESSION_NAME to agent identifier via AI Maestro API
   - Verifies agent exists and is accessible
   - Retrieves agent's project directory

2. **Manages Plugin Installation**
   - Adds plugins using `claude plugin install PLUGIN --scope SCOPE`
   - Removes plugins using `claude plugin uninstall PLUGIN`
   - Enables/disables plugins as needed

3. **Configures Plugin Scope**
   - `local`: Plugin active only for this agent (stored in .claude/settings.local.json)
   - `project`: Plugin shared across team (stored in .claude/settings.json)

4. **Reports Configuration Status**
   - Lists currently installed plugins
   - Shows plugin versions and scopes
   - Indicates which plugins are enabled/disabled

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `SESSION_NAME` | Yes | Target agent session name (e.g., `libs-svg-svgbbox`) |
| `--add PLUGIN` | No | Plugin name or path to add (can be repeated) |
| `--remove PLUGIN` | No | Plugin name to remove (can be repeated) |
| `--scope` | No | Installation scope: `local` (default) or `project` |
| `--list` | No | List currently installed plugins without making changes |
| `--enable PLUGIN` | No | Enable a disabled plugin |
| `--disable PLUGIN` | No | Disable a plugin without uninstalling |

## Examples

### Add a plugin to an agent

```bash
/ecos-configure-plugins libs-svg-svgbbox --add perfect-skill-suggester@emasoft-plugins
```

### Remove a plugin

```bash
/ecos-configure-plugins helper-agent-generic --remove old-plugin
```

### Add plugin with project scope

```bash
/ecos-configure-plugins orchestrator-master --add emasoft-architect-agent --scope project
```

### List installed plugins

```bash
/ecos-configure-plugins libs-svg-svgbbox --list
```

### Add and remove in one command

```bash
/ecos-configure-plugins helper-agent-generic --add new-plugin --remove deprecated-plugin
```

## Output Example

```
╔════════════════════════════════════════════════════════════════╗
║               PLUGIN CONFIGURATION REPORT                      ║
╠════════════════════════════════════════════════════════════════╣
║ Agent: libs-svg-svgbbox                                        ║
║ Project: /Users/user/Code/svg-bbox                             ║
╠════════════════════════════════════════════════════════════════╣
║ ACTIONS PERFORMED                                              ║
╠════════════════════════════════════════════════════════════════╣
║ [+] Added: perfect-skill-suggester@emasoft-plugins (local)     ║
║ [-] Removed: old-deprecated-plugin                             ║
╠════════════════════════════════════════════════════════════════╣
║ CURRENT PLUGINS                                                ║
╠════════════════════════════════════════════════════════════════╣
║ Plugin Name                  │ Version │ Scope   │ Status      ║
║─────────────────────────────────────────────────────────────── ║
║ perfect-skill-suggester      │ 1.2.3   │ local   │ enabled     ║
║ emasoft-architect-agent      │ 2.0.0   │ project │ enabled     ║
║ ai-maestro-messaging-hook    │ 1.0.0   │ user    │ enabled     ║
╠════════════════════════════════════════════════════════════════╣
║ NOTE: Agent must restart Claude Code to apply plugin changes   ║
╚════════════════════════════════════════════════════════════════╝
```

## Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| "Agent not found" | SESSION_NAME not registered in AI Maestro | Verify agent name with AI Maestro API |
| "Plugin not found" | Plugin name invalid or marketplace not added | Add marketplace first or check plugin name |
| "Permission denied" | Cannot write to agent's settings | Check file permissions |
| "Scope conflict" | Plugin already installed at different scope | Remove first, then reinstall at new scope |

## Prerequisites

- AI Maestro API must be running (`http://localhost:23000`)
- Target agent must be registered in AI Maestro
- For marketplace plugins: marketplace must be added first

## Notes

- **RESTART REQUIRED**: Plugin changes require Claude Code restart to take effect
- This command sends a notification to the target agent about plugin changes
- The `--scope project` setting affects the `.claude/settings.json` which is version-controlled

## Related Commands

- `/ecos-validate-skills` - Validate skills for an agent
- `/ecos-reindex-skills` - Trigger PSS reindex for an agent
- `/ecos-orchestration-status` - Check agent orchestration status
