---
operation: conduct-project-handoff
procedure: proc-create-team
workflow-instruction: Step 4 - Team Creation
parent-skill: ecos-onboarding
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Conduct Project Handoff

## When to Use

- Onboarding agent to specific project work
- Transferring work between agents
- Bringing backup agents up to speed
- Agent returning from hibernation needs context
- Mid-project agent replacement

## Prerequisites

- Agent has completed onboarding checklist
- Agent has received role briefing
- Project documentation is current
- The `agent-messaging` skill is available
- Current project state is known

## Procedure

### Step 1: Gather Project State

Collect current project information:

```bash
# Project overview
cat ~/projects/<project>/README.md

# Current sprint/backlog
cat ~/projects/<project>/docs/BACKLOG.md

# Active work
cat ~/projects/<project>/docs/CURRENT_TASK.md

# Recent changes
cd ~/projects/<project> && git log --oneline -10
```

### Step 2: Compose Project Handoff Document

Create a structured handoff document with:
1. Project overview
2. Current state
3. Key files
4. Conventions
5. Active context

### Step 3: Validate Handoff Document

Before sending, validate the handoff:

```bash
# Use validation script
python scripts/ecos_validate_handoff.py --file /tmp/handoff.md

# Manual checks:
# - All referenced files exist
# - No [TBD] placeholders
# - Current state is accurate
# - Contact info provided
```

### Step 4: Send Project Handoff

Use the `agent-messaging` skill to send:
- **Recipient**: the target agent session name
- **Subject**: `Project Handoff: [Project Name]`
- **Priority**: `high`
- **Content**: type `project-assignment`, message: A structured handoff document containing: Project Overview (description, purpose, goals), Current State (feature status per feature), Key Files (paths and purposes), Conventions (coding standards), Active Context (current work focus and next steps), Contact information (who to ask for questions, task issues, escalation). End with "Please confirm receipt and ask any clarifying questions."

### Step 5: Verify Comprehension

Use the `agent-messaging` skill to send:
- **Recipient**: the target agent session name
- **Subject**: `Project Handoff Verification`
- **Priority**: `high`
- **Content**: type `request`, message: "To verify handoff completion, please answer: (1) What is the project purpose? (2) What is the current state of Feature B? (3) Where would you find the project coding conventions?"

### Step 6: Log Handoff

```bash
uv run python scripts/ecos_team_registry.py log \
  --event "project-handoff" \
  --agent "<agent-session-name>" \
  --reason "Handoff for <project> - <role>" \
  --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

## Checklist

Copy this checklist and track your progress:

- [ ] Gather current project state
- [ ] Document project overview
- [ ] Document current progress on features
- [ ] List key files with purposes
- [ ] Document coding conventions
- [ ] Note active context and next steps
- [ ] Validate handoff document (no placeholders)
- [ ] Verify all referenced files exist
- [ ] Send handoff message via `agent-messaging` skill
- [ ] Wait for receipt confirmation
- [ ] Ask verification questions
- [ ] Confirm agent comprehension
- [ ] Log handoff completion

## Examples

### Example: API Project Handoff

Use the `agent-messaging` skill to send:
- **Recipient**: `dev-api-charlie`
- **Subject**: `Project Handoff: Backend API`
- **Priority**: `high`
- **Content**: type `project-assignment`, message: "Project Handoff: Backend API. Project Overview: We are building a RESTful API for the main application providing authentication, user management, and data CRUD operations. Current sprint: Sprint 5 (2 weeks remaining). Current State: Authentication endpoints COMPLETE, User CRUD endpoints IN PROGRESS (80%), Data endpoints NOT STARTED, Documentation PARTIAL. Key Files: src/api/auth.py (Authentication handlers), src/api/users.py (User CRUD handlers - your focus), src/models/ (Database models), tests/api/ (API tests), CLAUDE.md (Project instructions), docs/API.md (API specification). Conventions: Use FastAPI for all endpoints, all endpoints return JSON, error responses use standard format, tests required for all new endpoints, use async/await for database operations. Active Context: Current work is User update endpoint (PUT /users/{id}) at src/api/users.py line 145, next step is implementing validation for user update fields, not blocked by anything. Contact: Questions about project to ecos-chief-of-staff, task assignments from eoa-backend-orchestrator, code reviews by eia-api-integrator. Please confirm receipt and understanding."

### Example: Emergency Mid-Project Handoff

**Step 1:** Request state dump from outgoing agent using the `agent-messaging` skill:
- **Recipient**: the outgoing agent session name
- **Subject**: `Urgent: State Dump Required`
- **Priority**: `urgent`
- **Content**: type `request`, message: "Emergency handoff needed. Please save your current state to ~/.emasoft/agent-states/[agent-name]-emergency.json immediately."

**Step 2:** Wait briefly for state dump (30 seconds).

**Step 3:** Send handoff to incoming agent using the `agent-messaging` skill:
- **Recipient**: the incoming agent session name
- **Subject**: `EMERGENCY Handoff: [Project Name]`
- **Priority**: `urgent`
- **Content**: type `project-assignment`, message: "Emergency handoff. Previous agent state at ~/.emasoft/agent-states/[outgoing-agent]-emergency.json. Review and continue the critical fix. Report status immediately upon starting."

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Agent asks repeated questions | Handoff incomplete | Send supplementary information |
| Agent makes errors from missing context | Key info not in handoff | Update handoff, re-send missing details |
| Agent cannot find referenced files | Paths incorrect | Verify and correct file paths |
| Verification answers wrong | Agent misunderstood | Clarify specific points, re-verify |
| Agent overwhelmed | Too much info at once | Break handoff into stages |

## Related Operations

- [op-execute-onboarding-checklist.md](op-execute-onboarding-checklist.md) - Basic onboarding first
- [op-deliver-role-briefing.md](op-deliver-role-briefing.md) - Role context
- [op-validate-handoff.md](op-validate-handoff.md) - Validate before sending
