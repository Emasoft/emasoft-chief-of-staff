---
name: ecos-remove-project
description: "Remove a project from Chief of Staff management"
argument-hint: "<PROJECT_ID> [--force]"
allowed-tools: ["Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/ecos_remove_project.py:*)"]
user-invocable: true
---

# Remove Project from Management Command

Unregister a project from Chief of Staff management. This removes the project from tracking but does not affect the actual repository or GitHub board.

## Usage

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ecos_remove_project.py" $ARGUMENTS
```

## What This Command Does

1. **Validates Project Exists**
   - Looks up project by ID in state file
   - Confirms project is currently managed

2. **Checks for Active Agents**
   - Verifies no agents are currently assigned
   - If agents assigned, blocks removal unless `--force`
   - Lists assigned agents if blocking

3. **Sends Unassignment Notifications** (if --force)
   - Notifies all assigned agents via AI Maestro
   - Agents receive project removal notification
   - Clears agent assignments in state

4. **Updates State File**
   - Removes project entry from `.claude/chief-of-staff-state.local.md`
   - Preserves other project configurations
   - Records removal in activity log

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `<PROJECT_ID>` | Yes | Project identifier to remove |

## Options

| Option | Description |
|--------|-------------|
| `--force` | Remove even if agents are assigned (sends unassignment notifications) |

## Examples

### Remove Unassigned Project

```bash
/ecos-remove-project oldproject
```

Output:
```
Project removed successfully.
  ID: oldproject
  Repository: https://github.com/Emasoft/oldproject

Project is no longer managed by Chief of Staff.
```

### Attempt to Remove With Assigned Agents

```bash
/ecos-remove-project svgbbox
```

Output:
```
ERROR: Cannot remove project with assigned agents.

Project: svgbbox
Assigned agents:
  - libs-svg-svgbbox
  - helper-agent-generic

Options:
  1. Reassign agents to different project first
  2. Use --force to remove and notify agents
```

### Force Remove With Agents

```bash
/ecos-remove-project svgbbox --force
```

Output:
```
WARNING: Force removing project with assigned agents.

Sending unassignment notifications...
  - libs-svg-svgbbox: notified
  - helper-agent-generic: notified

Project removed successfully.
  ID: svgbbox
  Repository: https://github.com/Emasoft/svgbbox
  Agents notified: 2

Project is no longer managed by Chief of Staff.
Assigned agents have been notified of removal.
```

## Agent Notification Format

When `--force` is used, agents receive this AI Maestro message:

> **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

```json
{
  "to": "libs-svg-svgbbox",
  "subject": "[PROJECT REMOVED] svgbbox",
  "priority": "high",
  "content": {
    "type": "notification",
    "message": "Project 'svgbbox' has been removed from Chief of Staff management. You are no longer assigned to this project. Please await new assignment or contact orchestrator for instructions."
  }
}
```

## Safety Checks

| Check | Behavior |
|-------|----------|
| Project exists | Fails if project ID not found |
| Agents assigned | Blocks removal unless `--force` |
| Active operations | Warns if project has pending tasks |
| State file writable | Ensures state can be updated |

## Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| "Project not found" | Invalid project ID | Check ID with `/ecos-list-projects` |
| "Agents still assigned" | Active agent assignments | Reassign agents or use `--force` |
| "State file not found" | Missing state file | Initialize with `/ecos-init` |
| "State file locked" | Another operation in progress | Wait and retry |
| "AI Maestro unreachable" | Cannot send notifications | Check AI Maestro service |

## State File Update

After removal, the project section is deleted from `.claude/chief-of-staff-state.local.md`:

Before:
```markdown
## Managed Projects

### svgbbox
- **repo**: https://github.com/Emasoft/svgbbox
- **agents**: libs-svg-svgbbox
- **added**: 2026-01-15T09:00:00Z

### maestro
- **repo**: https://github.com/Emasoft/ai-maestro
- **agents**: orchestrator-master
- **added**: 2026-01-10T14:30:00Z
```

After `/ecos-remove-project svgbbox`:
```markdown
## Managed Projects

### maestro
- **repo**: https://github.com/Emasoft/ai-maestro
- **agents**: orchestrator-master
- **added**: 2026-01-10T14:30:00Z
```

## Related Commands

- `/ecos-list-projects` - View all managed projects
- `/ecos-add-project` - Add a new project to management
- `/ecos-assign-project` - Assign an agent to a project
