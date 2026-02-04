---
name: ecos-assign-project
description: "Assign an agent to a managed project and send onboarding message"
argument-hint: "<SESSION_NAME> <PROJECT_ID>"
allowed-tools: ["Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/ecos_assign_project.py:*)"]
user-invocable: true
---

# Assign Agent to Project Command

Assign a Claude Code agent session to a managed project. This updates project tracking and sends an onboarding message to the agent via AI Maestro with project context and initial instructions.

## Usage

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ecos_assign_project.py" $ARGUMENTS
```

## What This Command Does

1. **Validates Inputs**
   - Checks session name format (domain-subdomain-name)
   - Verifies project ID exists in managed projects
   - Checks agent is not already assigned to this project

2. **Queries Agent Status**
   - Pings agent via AI Maestro to verify it is online
   - Gets agent's current assignment (if any)
   - Warns if agent is assigned to different project

3. **Updates State File**
   - Adds agent to project's agent list
   - Records assignment timestamp
   - Updates `.claude/chief-of-staff-state.local.md`

4. **Sends Onboarding Message**
   - Sends project context via AI Maestro
   - Includes repository URL, GitHub board, current issues
   - Provides initial task instructions if available

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `<SESSION_NAME>` | Yes | Full session name of the agent (e.g., `libs-svg-svgbbox`) |
| `<PROJECT_ID>` | Yes | Project identifier from managed projects |

## Examples

### Basic Assignment

```bash
/ecos-assign-project libs-svg-svgbbox svgbbox
```

Output:
```
Agent assignment successful.
  Agent: libs-svg-svgbbox
  Project: svgbbox
  Repository: https://github.com/Emasoft/svgbbox

Onboarding message sent via AI Maestro.
Agent will receive project context and instructions.
```

### Assign to Project With GitHub Board

```bash
/ecos-assign-project orchestrator-master maestro
```

Output:
```
Agent assignment successful.
  Agent: orchestrator-master
  Project: maestro
  Repository: https://github.com/Emasoft/ai-maestro
  GitHub Board: https://github.com/orgs/Emasoft/projects/8
  Open Issues: 5

Onboarding message sent via AI Maestro.
Agent will receive project context, board status, and priority issues.
```

### Attempt Duplicate Assignment

```bash
/ecos-assign-project libs-svg-svgbbox svgbbox
```

Output:
```
WARNING: Agent already assigned to this project.
  Agent: libs-svg-svgbbox
  Project: svgbbox
  Assigned: 2026-02-01T10:30:00Z

No changes made. Use /ecos-list-projects to view assignments.
```

## Onboarding Message Format

The assigned agent receives this AI Maestro message:

```json
{
  "to": "libs-svg-svgbbox",
  "subject": "[TEAM ASSIGNMENT] svgbbox",
  "priority": "high",
  "content": {
    "type": "team-assignment",
    "message": "You have been assigned to the team for project 'svgbbox'.\n\nProject Details:\n- Repository: https://github.com/Emasoft/svgbbox\n- GitHub Board: https://github.com/orgs/Emasoft/projects/12\n\nPlease acknowledge receipt. The project Orchestrator (EOA) will assign specific tasks to you.\n\nIMPORTANT: ECOS assigns you to teams. EOA assigns you tasks."
  }
}
```

## State File Update

After assignment, `.claude/chief-of-staff-state.local.md` is updated:

Before:
```markdown
### svgbbox
- **repo**: https://github.com/Emasoft/svgbbox
- **github_project**: https://github.com/orgs/Emasoft/projects/12
- **agents**: (none)
- **added**: 2026-01-15T09:00:00Z
```

After:
```markdown
### svgbbox
- **repo**: https://github.com/Emasoft/svgbbox
- **github_project**: https://github.com/orgs/Emasoft/projects/12
- **agents**: libs-svg-svgbbox
- **added**: 2026-01-15T09:00:00Z
- **last_assignment**: 2026-02-01T11:30:00Z
```

## Session Name Format

Agent session names follow the domain hierarchy format:

| Format | Example | Meaning |
|--------|---------|---------|
| `domain-subdomain-name` | `libs-svg-svgbbox` | Library / SVG / svgbbox project |
| `apps-project-role` | `apps-maestro-dev` | Application / Maestro / developer role |
| `utils-category-name` | `utils-media-encoder` | Utility / Media / encoder tool |
| `orchestrator-type` | `orchestrator-master` | Orchestrator / master instance |

**IMPORTANT**: Always use the FULL session name, not aliases.

## Validation Rules

| Rule | Description |
|------|-------------|
| Session format | Must match `domain-subdomain-name` pattern |
| Project exists | Project ID must be in managed projects |
| No duplicate | Agent cannot be assigned to same project twice |
| Agent reachable | Warning if AI Maestro cannot reach agent |

## Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| "Invalid session name" | Malformed session name | Use full domain-subdomain-name format |
| "Project not found" | Invalid project ID | Check ID with `/ecos-list-projects` |
| "Agent already assigned" | Duplicate assignment | Assignment already exists |
| "AI Maestro unreachable" | Cannot send message | Check AI Maestro service |
| "Agent offline" | Agent not responding | Warning only, assignment proceeds |
| "State file locked" | Another operation in progress | Wait and retry |

## Agent Status Response

The assigned agent should acknowledge with:

```json
{
  "to": "orchestrator-master",
  "subject": "RE: [PROJECT ASSIGNMENT] svgbbox",
  "priority": "normal",
  "content": {
    "type": "acknowledgment",
    "message": "Assignment received. Beginning work on issue #42."
  }
}
```

## Related Commands

- `/ecos-list-projects` - View all projects and assignments
- `/ecos-add-project` - Add a new project to management
- `/ecos-remove-project` - Remove a project (requires unassigning agents first)
