---
name: ecos-add-project
description: "Add a new project to Chief of Staff management"
argument-hint: "<REPO_URL> [--github-project BOARD_URL] [--id PROJECT_ID]"
allowed-tools: ["Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/ecos_add_project.py:*)"]
user-invocable: true
---

# Add Project to Management Command

Register a new project with the Chief of Staff for centralized management. This enables agent assignment, GitHub Project board integration, and cross-project coordination.

## Usage

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ecos_add_project.py" $ARGUMENTS
```

## What This Command Does

1. **Validates Repository URL**
   - Checks URL format (GitHub, GitLab, etc.)
   - Verifies repository accessibility via `gh` CLI
   - Extracts owner/repo information

2. **Configures GitHub Project Board** (if provided)
   - Validates board URL format
   - Verifies board exists and is accessible
   - Links board to project for issue tracking

3. **Generates Project ID**
   - Uses provided `--id` or auto-generates from repo name
   - Ensures uniqueness across managed projects
   - Creates kebab-case identifier

4. **Updates State File**
   - Adds project entry to `.claude/chief-of-staff-state.local.md`
   - Records timestamp and configuration
   - Initializes empty agent list

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `<REPO_URL>` | Yes | Full URL to the Git repository |

## Options

| Option | Description |
|--------|-------------|
| `--github-project BOARD_URL` | URL to GitHub Project board for issue tracking |
| `--id PROJECT_ID` | Custom project identifier (defaults to repo name) |

## Examples

### Basic Usage

```bash
/ecos-add-project https://github.com/Emasoft/svgbbox
```

Output:
```
Project added successfully.
  ID: svgbbox
  Repository: https://github.com/Emasoft/svgbbox
  GitHub Board: (none)

Next: Assign agents with /ecos-assign-project <session_name> svgbbox
```

### With GitHub Project Board

```bash
/ecos-add-project https://github.com/Emasoft/ai-maestro --github-project https://github.com/orgs/Emasoft/projects/8
```

Output:
```
Project added successfully.
  ID: ai-maestro
  Repository: https://github.com/Emasoft/ai-maestro
  GitHub Board: https://github.com/orgs/Emasoft/projects/8

Board verified: "AI Maestro Development" (3 open issues)

Next: Assign agents with /ecos-assign-project <session_name> ai-maestro
```

### With Custom ID

```bash
/ecos-add-project https://github.com/Emasoft/my-long-project-name --id myproj
```

Output:
```
Project added successfully.
  ID: myproj
  Repository: https://github.com/Emasoft/my-long-project-name
  GitHub Board: (none)

Next: Assign agents with /ecos-assign-project <session_name> myproj
```

## State File Update

After running this command, `.claude/chief-of-staff-state.local.md` is updated:

```markdown
## Managed Projects

### svgbbox
- **repo**: https://github.com/Emasoft/svgbbox
- **github_project**: (none)
- **agents**: (none)
- **added**: 2026-02-01T11:15:00Z
- **status**: active
```

## Validation Rules

| Rule | Description |
|------|-------------|
| Valid URL | Must be a valid Git repository URL |
| Unique ID | Project ID cannot conflict with existing projects |
| ID format | Must be kebab-case, 2-32 characters |
| Board access | GitHub board must be accessible via `gh` CLI |

## Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| "Invalid repository URL" | Malformed or unsupported URL | Use full HTTPS URL |
| "Repository not accessible" | Cannot reach repo via `gh` CLI | Check URL and auth |
| "Project ID already exists" | Duplicate ID | Use `--id` with unique name |
| "Invalid GitHub Project URL" | Board URL malformed | Use full project board URL |
| "Board not accessible" | Cannot access board via `gh` CLI | Check board permissions |
| "State file locked" | Another operation in progress | Wait and retry |

## Prerequisites

- `gh` CLI must be authenticated (`gh auth login`)
- Write access to `.claude/` directory
- State file must exist or be creatable

## Related Commands

- `/ecos-list-projects` - View all managed projects
- `/ecos-remove-project` - Remove a project from management
- `/ecos-assign-project` - Assign an agent to this project
