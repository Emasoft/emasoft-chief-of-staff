---
operation: deliver-role-briefing
procedure: proc-create-team
workflow-instruction: Step 4 - Team Creation
parent-skill: ecos-onboarding
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Deliver Role Briefing


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Retrieve Role Definition](#step-1-retrieve-role-definition)
  - [Step 2: Compose Role Briefing Message](#step-2-compose-role-briefing-message)
  - [Step 3: Send Role Briefing](#step-3-send-role-briefing)
  - [Step 4: Handle Questions](#step-4-handle-questions)
  - [Step 5: Confirm Understanding](#step-5-confirm-understanding)
  - [Step 6: Log Role Assignment](#step-6-log-role-assignment)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Developer Role Briefing](#example-developer-role-briefing)
  - [Example: Orchestrator Role Briefing](#example-orchestrator-role-briefing)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

- After initial onboarding checklist
- When agent role changes
- When role responsibilities are updated
- When agent requests role clarification
- During team restructuring

## Prerequisites

- Agent is onboarded (basic checklist complete)
- Role definition document exists
- The `agent-messaging` skill is available
- Reporting structure is defined

## Procedure

### Step 1: Retrieve Role Definition

Get the role definition for the agent's assigned role:

```bash
# Check available role definitions
ls /path/to/plugin/docs/roles/

# Read specific role definition
cat /path/to/plugin/docs/roles/<role-name>.md
```

### Step 2: Compose Role Briefing Message

Structure the briefing with these sections:
1. Assigned role name
2. Key responsibilities
3. Reporting structure
4. Performance expectations
5. Available resources

### Step 3: Send Role Briefing

Use the `agent-messaging` skill to send:
- **Recipient**: the target agent session name
- **Subject**: `Role Briefing: [Role Name]`
- **Priority**: `high`
- **Content**: type `role-assignment`, message: A structured briefing containing: the assigned role and project name, numbered responsibilities, reporting structure (report to, coordinate with, escalate to), expectations, and available resources. End with "Please confirm you understand these responsibilities."

### Step 4: Handle Questions

If the agent asks clarifying questions, use the `agent-messaging` skill to reply:
- **Recipient**: the agent session name
- **Subject**: `RE: Role Clarification`
- **Priority**: `normal`
- **Content**: type `request`, message: the answer to the specific question.

### Step 5: Confirm Understanding

Use the `agent-messaging` skill to send:
- **Recipient**: the agent session name
- **Subject**: `Role Understanding Confirmation`
- **Priority**: `high`
- **Content**: type `request`, message: "Please summarize your understanding of your role in 2-3 sentences to confirm you have understood the briefing correctly."

### Step 6: Log Role Assignment

```bash
uv run python scripts/ecos_team_registry.py update-role \
  --name "<agent-session-name>" \
  --role "<role-name>" \
  --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

uv run python scripts/ecos_team_registry.py log \
  --event "role-briefing" \
  --agent "<agent-session-name>" \
  --reason "Assigned as <role> on <project>" \
  --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

## Checklist

Copy this checklist and track your progress:

- [ ] Retrieve role definition document
- [ ] Compose role briefing with all sections
- [ ] Send role briefing message via `agent-messaging` skill
- [ ] Wait for initial acknowledgment
- [ ] Answer any clarifying questions
- [ ] Request understanding confirmation
- [ ] Verify agent summary is accurate
- [ ] Correct any misunderstandings
- [ ] Log role assignment in registry

## Examples

### Example: Developer Role Briefing

Use the `agent-messaging` skill to send:
- **Recipient**: `dev-backend-alice`
- **Subject**: `Role Briefing: Developer`
- **Priority**: `high`
- **Content**: type `role-assignment`, message: "Role Briefing: Developer. You are assigned as a Developer on the backend-api project. Responsibilities: (1) Implement features from the backlog, (2) Write unit tests for all new code, (3) Update documentation for your changes, (4) Participate in code reviews when requested, (5) Report blockers promptly. Reporting Structure: Report to eoa-backend-orchestrator for task assignments, coordinate with dev-backend-bob as peer developer, escalate to ecos-chief-of-staff for blockers and resource issues. Expectations: Acknowledge task assignments promptly, provide regular status updates, request clarification if requirements unclear, follow project coding conventions (see CLAUDE.md), complete tasks within estimated timeframes. Resources: CLAUDE.md (project instructions), docs/API.md (API specifications), tests/ (existing test examples), .github/ (CI/CD configuration). Please confirm you understand these responsibilities."

### Example: Orchestrator Role Briefing

Use the `agent-messaging` skill to send:
- **Recipient**: `eoa-webapp-orchestrator`
- **Subject**: `Role Briefing: Orchestrator`
- **Priority**: `high`
- **Content**: type `role-assignment`, message: "Role Briefing: Orchestrator. You are the Orchestrator for the webapp project team. Responsibilities: (1) Receive work from EAMA and break into tasks, (2) Assign tasks to team developers, (3) Track task progress and blockers, (4) Coordinate parallel work streams, (5) Report completion to EAMA. Reporting Structure: Report to eama-assistant-manager for work assignments, manage dev-frontend-bob and dev-backend-charlie as developers, coordinate with eia-webapp-integrator for code reviews, escalate to ecos-chief-of-staff for team issues. Expectations: Maintain clear task backlog, ensure developers are not blocked, provide daily progress summaries, identify risks early and escalate, do NOT do implementation work yourself. Resources: Team registry at .emasoft/team-registry.json, project backlog at docs/BACKLOG.md, GitHub Issues for task tracking. Please confirm you understand these responsibilities."

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Agent claims role unclear | Briefing too generic | Provide more specific examples |
| Agent confused about reporting | Structure not explicit | Draw clear reporting diagram |
| Agent asks about tasks not in role | Role boundary confusion | Clarify what is NOT their responsibility |
| Agent doesn't acknowledge | Overwhelmed or confused | Break briefing into smaller messages |
| Understanding summary incorrect | Misunderstood briefing | Correct specific misunderstandings, re-brief |

## Related Operations

- [op-execute-onboarding-checklist.md](op-execute-onboarding-checklist.md) - Full onboarding first
- [op-conduct-project-handoff.md](op-conduct-project-handoff.md) - Project-specific context
- [op-validate-handoff.md](op-validate-handoff.md) - Validate handoff documents
