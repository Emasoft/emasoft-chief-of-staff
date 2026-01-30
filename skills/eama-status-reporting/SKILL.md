---
name: eama-status-reporting
description: Use when generating status reports showing progress across all roles (Architect, Orchestrator, Integrator)
context: fork
agent: eama-report-generator
user-invocable: true
triggers:
  - when user asks for status
  - when generating progress reports
  - when summarizing work across roles
---

# Status Reporting Skill

## Overview

Generate comprehensive status reports showing progress across all roles (Architect, Orchestrator, Integrator).

## Prerequisites

- AI Maestro messaging system must be running for role queries
- GitHub CLI (`gh`) must be installed for issue/PR status
- Session memory files must be accessible
- `docs_dev/reports/` directory must exist

## Instructions

1. Determine the type of report needed (quick status, progress, handoff summary, blocker)
2. Query each role via AI Maestro for their current status
3. Query GitHub for issue and PR status using `gh` CLI
4. Read session memory files for context
5. Compile all information into unified report format
6. Save report to `docs_dev/reports/status-{date}.md`
7. Present formatted report to user

## Report Types

| Type | Frequency | Content |
|------|-----------|---------|
| Quick Status | On demand | Current state summary |
| Progress Report | Daily/Weekly | Work completed, in progress, blocked |
| Handoff Summary | On transition | What was handed to whom |
| Blocker Report | As needed | What's blocking progress |

## Report Generation Workflow

1. Query each role via AI Maestro for current status
2. Query GitHub for issue/PR status
3. Read session memory files
4. Compile into unified report
5. Format for user consumption

## Report Sections

### Quick Status Format
- Current active task
- % complete estimate
- Next milestone
- Blockers (if any)

### Progress Report Format
- Period covered
- Tasks completed (with evidence)
- Tasks in progress (with estimates)
- Tasks blocked (with reasons)
- Tasks added (new scope)
- Risks identified

## Output Location

Reports saved to: `docs_dev/reports/status-{date}.md`

## Examples

### Example 1: Quick Status Report

```markdown
## Quick Status - 2025-01-30

**Current Active Task**: Implementing user authentication
**% Complete**: 65%
**Next Milestone**: Complete login endpoint by EOD
**Blockers**: None
```

### Example 2: Progress Report

```markdown
## Progress Report - Week of 2025-01-27

### Period Covered
2025-01-27 to 2025-01-30

### Tasks Completed
- [EAA] Auth system design approved (PR #45)
- [EOA] Login endpoint implemented (5 files)
- [EIA] Code review completed, 2 issues fixed

### Tasks In Progress
- [EOA] Logout endpoint (ETA: 2025-01-31)
- [EAA] Session management design (ETA: 2025-02-01)

### Tasks Blocked
- [EOA] Password reset - blocked by email service config

### Risks Identified
- Email service integration may delay password reset feature
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Role query timeout | Agent not responding | Mark as "status unknown" and continue |
| GitHub API failure | Auth or rate limit | Use cached data, note staleness |
| Memory file not found | Not initialized | Report "no session data available" |
| Report directory missing | First report | Create `docs_dev/reports/` automatically |

## Resources

- [eama-role-routing SKILL](../eama-role-routing/SKILL.md) - Role status queries
- [eama-approval-workflows SKILL](../eama-approval-workflows/SKILL.md) - Approval status
- [eama-shared SKILL](../eama-shared/SKILL.md) - Session memory access
