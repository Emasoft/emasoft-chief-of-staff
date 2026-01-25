---
name: am-planning-status
description: "View Plan Phase progress - requirements completion, modules defined, exit criteria status"
argument-hint: "[--verbose]"
allowed-tools: ["Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/am_planning_status.py:*)"]
---

# Planning Status Command

View the current status of Plan Phase including requirements progress, module definitions, and exit criteria.

## Usage

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/am_planning_status.py" $ARGUMENTS
```

## What This Command Shows

1. **Phase Status**: Current phase state (drafting/reviewing/approved)
2. **Goal**: The locked user goal
3. **Requirements Progress**: Completion status of each requirement section
4. **Modules Defined**: List of modules with their status and acceptance criteria
5. **Exit Criteria**: Checklist of conditions required to transition

## Output Format

```
╔════════════════════════════════════════════════════════════════╗
║                    PLAN PHASE STATUS                           ║
╠════════════════════════════════════════════════════════════════╣
║ Plan ID: plan-20260108-143022                                  ║
║ Status: drafting                                               ║
║ Goal: Build user authentication with OAuth2                    ║
╠════════════════════════════════════════════════════════════════╣
║ REQUIREMENTS PROGRESS                                          ║
╠════════════════════════════════════════════════════════════════╣
║ [✓] Functional Requirements     - complete                     ║
║ [→] Non-Functional Requirements - in_progress                  ║
║ [ ] Architecture Design         - pending                      ║
╠════════════════════════════════════════════════════════════════╣
║ MODULES DEFINED (2)                                            ║
╠════════════════════════════════════════════════════════════════╣
║ 1. auth-core      - Core Authentication    [planned]           ║
║ 2. oauth-google   - Google OAuth2          [pending]           ║
╠════════════════════════════════════════════════════════════════╣
║ EXIT CRITERIA                                                  ║
╠════════════════════════════════════════════════════════════════╣
║ [ ] USER_REQUIREMENTS.md complete                              ║
║ [ ] All modules defined with acceptance criteria               ║
║ [ ] GitHub Issues created for all modules                      ║
║ [ ] User approved the plan                                     ║
╚════════════════════════════════════════════════════════════════╝
```

## Options

- `--verbose`: Show detailed acceptance criteria for each module

## When to Use

- After `/start-planning` to verify initialization
- During planning to track progress
- Before `/approve-plan` to verify all criteria met

## Related Commands

- `/start-planning` - Enter Plan Phase Mode
- `/add-requirement` - Add new requirement or module
- `/modify-requirement` - Change existing specifications
- `/approve-plan` - Transition to Orchestration Phase
