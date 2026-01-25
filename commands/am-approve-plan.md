---
name: ao-approve-plan
description: "Approve the plan and transition from Plan Phase to Orchestration Phase"
argument-hint: "[--skip-issues]"
allowed-tools: ["Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/atlas_approve_plan.py:*)"]
---

# Approve Plan Command

Mark the plan as approved and transition from Plan Phase to Orchestration Phase. This is the critical transition point that creates GitHub Issues and enables implementation.

## Usage

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/atlas_approve_plan.py" $ARGUMENTS
```

## What This Command Does

1. **Validates Plan Completeness**
   - Checks all requirement sections are complete
   - Verifies all modules have acceptance criteria
   - Confirms USER_REQUIREMENTS.md exists

2. **Creates GitHub Issues** (unless `--skip-issues`)
   - One issue per module with:
     - Module specs from plan
     - Acceptance criteria
     - Priority labels
   - Adds all issues to GitHub Project board

3. **Updates State Files**
   - Marks plan phase as complete
   - Creates orchestration phase state file
   - Links modules to GitHub issue numbers

4. **Outputs Transition Summary**
   - Lists created issues with URLs
   - Shows next steps for orchestration

## Prerequisites

Before running this command:
- [ ] USER_REQUIREMENTS.md must be complete
- [ ] All modules must have acceptance criteria defined
- [ ] All requirement sections must have `complete` status

Use `/planning-status` to verify all criteria are met.

## Options

| Option | Description |
|--------|-------------|
| `--skip-issues` | Skip GitHub Issue creation (for offline work) |

## Transition Flow

```
Plan Phase State File (.claude/orchestrator-plan-phase.local.md)
    |
    | /approve-plan validates and updates
    v
plan_phase_complete: true
    |
    | Creates GitHub Issues for all modules
    v
Orchestration Phase State File (.claude/orchestrator-exec-phase.local.md)
    |
    | Ready for /start-orchestration
    v
Orchestration Phase begins
```

## GitHub Issue Creation

For each module in the plan, creates an issue:

```markdown
# Module: [module_name]

## Description
[From plan specifications]

## Acceptance Criteria
- [ ] [criterion 1]
- [ ] [criterion 2]
- [ ] [criterion 3]

## Priority
[priority_label]

## Related
- Plan ID: [plan_id]
- Requirements: USER_REQUIREMENTS.md
```

Labels applied:
- `module`
- `priority-[level]`
- `status-todo`

## Output Example

```
╔════════════════════════════════════════════════════════════════╗
║                    PLAN APPROVED                               ║
╠════════════════════════════════════════════════════════════════╣
║ Plan ID: plan-20260108-143022                                  ║
║ Goal: Build user authentication with OAuth2                    ║
╠════════════════════════════════════════════════════════════════╣
║ GITHUB ISSUES CREATED                                          ║
╠════════════════════════════════════════════════════════════════╣
║ #42 - Core Authentication (auth-core)        [priority-high]   ║
║ #43 - Google OAuth2 (oauth-google)           [priority-medium] ║
║ #44 - Two-Factor Auth (auth-2fa)             [priority-low]    ║
╠════════════════════════════════════════════════════════════════╣
║ NEXT STEPS                                                     ║
╠════════════════════════════════════════════════════════════════╣
║ 1. Run /start-orchestration to begin implementation            ║
║ 2. Register remote agents with /register-agent                 ║
║ 3. Assign modules with /assign-module                          ║
╚════════════════════════════════════════════════════════════════╝
```

## Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| "Requirements incomplete" | Requirement sections not complete | Mark all sections complete |
| "Module missing criteria" | Module has no acceptance criteria | Add criteria with `/modify-requirement` |
| "USER_REQUIREMENTS.md not found" | File doesn't exist | Create the requirements document |
| "Not in Plan Phase" | No plan phase state file | Run `/start-planning` first |

## Related Commands

- `/planning-status` - Verify prerequisites
- `/start-orchestration` - Begin Orchestration Phase
- `/register-agent` - Register remote agents for implementation
