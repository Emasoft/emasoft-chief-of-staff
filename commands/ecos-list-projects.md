---
name: ecos-list-projects
description: "List all managed projects with their GitHub boards and assigned agents"
argument-hint: "[--verbose]"
allowed-tools: ["Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/ecos_list_projects.py:*)"]
user-invocable: true
---

# List Managed Projects Command

Display all projects currently managed by the Chief of Staff, including their repository URLs, GitHub Project boards, and assigned agent counts.

## Usage

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ecos_list_projects.py" $ARGUMENTS
```

## What This Command Does

1. **Reads State File**
   - Loads `.claude/chief-of-staff-state.local.md`
   - Parses the `## Managed Projects` section
   - Extracts project metadata

2. **Gathers Project Information**
   - Project ID (user-defined or auto-generated)
   - Repository URL
   - GitHub Project board URL (if configured)
   - Count of agents assigned to each project

3. **Displays Formatted Table**
   - Shows all projects in a readable table format
   - Includes status indicators
   - Shows agent assignment counts

## Options

| Option | Description |
|--------|-------------|
| `--verbose` | Show additional details: agent names, last activity, issue counts |

## Output Example

### Standard Output

```
+============+================================+==========================+========+
| Project ID | Repository                     | GitHub Board             | Agents |
+============+================================+==========================+========+
| svgbbox    | github.com/Emasoft/svgbbox     | Board #12                | 2      |
| maestro    | github.com/Emasoft/ai-maestro  | Board #8                 | 3      |
| skills     | github.com/Emasoft/skills-ref  | (none)                   | 1      |
+============+================================+==========================+========+
Total: 3 projects, 6 agents assigned
```

### Verbose Output

```
+============+================================+==========================+========+
| Project ID | Repository                     | GitHub Board             | Agents |
+============+================================+==========================+========+
| svgbbox    | github.com/Emasoft/svgbbox     | Board #12                | 2      |
|            | Agents: libs-svg-svgbbox, helper-agent-generic           |
|            | Last Activity: 2026-02-01T10:30:00Z                      |
|            | Open Issues: 5 | Closed: 12                              |
+------------+--------------------------------+--------------------------+--------+
| maestro    | github.com/Emasoft/ai-maestro  | Board #8                 | 3      |
|            | Agents: orchestrator-master, apps-maestro-dev, generic   |
|            | Last Activity: 2026-02-01T11:00:00Z                      |
|            | Open Issues: 3 | Closed: 28                              |
+------------+--------------------------------+--------------------------+--------+
| skills     | github.com/Emasoft/skills-ref  | (none)                   | 1      |
|            | Agents: claude-skills-factory                            |
|            | Last Activity: 2026-01-31T15:45:00Z                      |
|            | Open Issues: 0 | Closed: 4                               |
+============+================================+==========================+========+
Total: 3 projects, 6 agents assigned
```

## State File Format

The command reads from `.claude/chief-of-staff-state.local.md`:

```markdown
## Managed Projects

### svgbbox
- **repo**: https://github.com/Emasoft/svgbbox
- **github_project**: https://github.com/orgs/Emasoft/projects/12
- **agents**: libs-svg-svgbbox, helper-agent-generic
- **added**: 2026-01-15T09:00:00Z

### maestro
- **repo**: https://github.com/Emasoft/ai-maestro
- **github_project**: https://github.com/orgs/Emasoft/projects/8
- **agents**: orchestrator-master, apps-maestro-dev, generic
- **added**: 2026-01-10T14:30:00Z
```

## Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| "State file not found" | `.claude/chief-of-staff-state.local.md` missing | Initialize with `/ecos-init` or create file |
| "No projects configured" | No projects in state file | Add projects with `/ecos-add-project` |
| "Parse error" | Malformed state file | Check state file syntax |

## Related Commands

- `/ecos-add-project` - Add a new project to management
- `/ecos-remove-project` - Remove a project from management
- `/ecos-assign-project` - Assign an agent to a project
