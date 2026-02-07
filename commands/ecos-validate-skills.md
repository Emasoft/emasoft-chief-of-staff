---
name: ecos-validate-skills
description: "Validate skills for an agent using skills-ref validator"
argument-hint: "<SESSION_NAME> [--skill SKILL_NAME] [--fix]"
user-invocable: true
allowed-tools: ["Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/ecos_validate_skills.py:*)"]
---

# Validate Skills Command

Validate agent skills using the `skills-ref` validator. Can validate all skills for an agent or a specific skill by name.

## Usage

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ecos_validate_skills.py" $ARGUMENTS
```

## What This Command Does

1. **Resolves Target Agent**
   - Resolves SESSION_NAME to agent identifier via AI Maestro API
   - Retrieves agent's project directory and installed plugins
   - Locates all skill directories across all plugins

2. **Validates Skills Structure**
   - Uses `skills-ref validate` for OpenSpec compliance
   - Checks SKILL.md existence and format
   - Validates YAML frontmatter fields
   - Verifies reference documents are accessible

3. **Checks Skill-Specific Requirements**
   - TOC presence in SKILL.md
   - Progressive disclosure structure
   - Reference file accessibility
   - Script validation (if scripts/ directory exists)

4. **Reports Validation Results**
   - Lists all skills with pass/fail status
   - Details specific validation errors
   - Suggests fixes for common issues

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `SESSION_NAME` | Yes | Target agent session name (e.g., `libs-svg-svgbbox`) |
| `--skill SKILL_NAME` | No | Validate only this specific skill |
| `--fix` | No | Attempt automatic fixes for common issues |
| `--verbose` | No | Show detailed validation output |
| `--json` | No | Output results as JSON |

## Examples

### Validate all skills for an agent

```bash
/ecos-validate-skills libs-svg-svgbbox
```

### Validate a specific skill

```bash
/ecos-validate-skills orchestrator-master --skill eaa-architecture-review
```

### Validate with auto-fix

```bash
/ecos-validate-skills helper-agent-generic --fix
```

### Get JSON output for automation

```bash
/ecos-validate-skills libs-svg-svgbbox --json
```

## Output Example

```
╔════════════════════════════════════════════════════════════════╗
║                  SKILL VALIDATION REPORT                       ║
╠════════════════════════════════════════════════════════════════╣
║ Agent: orchestrator-master                                     ║
║ Project: /Users/user/Code/MAESTRO                              ║
║ Plugins Scanned: 3                                             ║
║ Skills Found: 12                                               ║
╠════════════════════════════════════════════════════════════════╣
║ VALIDATION RESULTS                                             ║
╠════════════════════════════════════════════════════════════════╣
║ Skill Name                   │ Plugin              │ Status    ║
║─────────────────────────────────────────────────────────────── ║
║ eama-role-routing            │ emasoft-assistant-m │ PASS      ║
║ eia-tdd-workflow             │ emasoft-integrator- │ PASS      ║
║ eoa-worktree-management      │ emasoft-orchestrato │ FAIL      ║
║ pss-activation-rules         │ perfect-skill-sugg  │ PASS      ║
║ ecos-session-memory-library  │ emasoft-chief-of-s  │ PASS      ║
╠════════════════════════════════════════════════════════════════╣
║ ERRORS (1)                                                     ║
╠════════════════════════════════════════════════════════════════╣
║ eoa-worktree-management:                                       ║
║   - Missing TOC in SKILL.md                                    ║
║   - Reference file not found: references/worktree-setup.md     ║
╠════════════════════════════════════════════════════════════════╣
║ SUMMARY                                                        ║
╠════════════════════════════════════════════════════════════════╣
║ Total: 12 | Passed: 11 | Failed: 1 | Warnings: 0               ║
╚════════════════════════════════════════════════════════════════╝
```

## Validation Checks

The validator performs these checks:

| Check | Description | Severity |
|-------|-------------|----------|
| SKILL.md exists | Main skill file must exist | Error |
| Valid frontmatter | YAML frontmatter must parse correctly | Error |
| Required fields | `name`, `description` must be present | Error |
| TOC present | Table of contents for progressive disclosure | Warning |
| References valid | All referenced files must exist | Error |
| Scripts executable | Scripts in scripts/ must be executable | Warning |
| No circular refs | Reference chain must not loop | Error |

## Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| "Agent not found" | SESSION_NAME not registered | Check agent name |
| "No plugins found" | Agent has no plugins installed | Install plugins first |
| "Skill not found" | Specified skill name doesn't exist | Check skill name |
| "skills-ref not installed" | Validator tool missing | Install with `pip install skills-ref` |

## Prerequisites

- AI Maestro must be running (use `ai-maestro-agents-management` skill to verify)
- Target agent must be registered in AI Maestro
- `skills-ref` must be installed (`pip install skills-ref`)

## Notes

- This command validates skill structure, not skill content quality
- Claude Code-specific fields (`context`, `agent`, `user-invocable`) may show as warnings in `skills-ref` output but are valid for Claude Code plugins
- Use `--fix` to attempt automatic repairs (adds missing TOC, fixes permissions)

## Related Commands

- `/ecos-configure-plugins` - Configure plugins for an agent
- `/ecos-reindex-skills` - Trigger PSS reindex after skill changes
- `/ecos-orchestration-status` - Check agent orchestration status
