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
- AI Maestro is running locally at `http://localhost:23000`
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

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "<agent-session-name>",
    "subject": "Project Handoff: <Project Name>",
    "priority": "high",
    "content": {
      "type": "project-assignment",
      "message": "# Project Handoff: <Project Name>\n\n## Project Overview\n<Brief description of project purpose and goals>\n\n## Current State\n- Feature A: COMPLETE\n- Feature B: IN PROGRESS (60%)\n- Feature C: NOT STARTED\n\n## Key Files\n- src/main.py - Entry point\n- src/core/ - Core logic\n- tests/ - Test directory\n- CLAUDE.md - Project instructions\n\n## Conventions\n- Use async/await for I/O\n- All functions need docstrings\n- Tests required for new code\n\n## Active Context\nCurrent work focus: <specific task>\nNext step: <immediate next action>\n\n## Contact\nQuestions: ecos-chief-of-staff\nTask issues: <orchestrator>\n\nPlease confirm receipt and ask any clarifying questions."
    }
  }'
```

### Step 5: Verify Comprehension

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "<agent-session-name>",
    "subject": "Project Handoff Verification",
    "priority": "high",
    "content": {
      "type": "request",
      "message": "To verify handoff completion, please answer: (1) What is the project purpose? (2) What is the current state of Feature B? (3) Where would you find the project coding conventions?"
    }
  }'
```

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
- [ ] Send handoff message
- [ ] Wait for receipt confirmation
- [ ] Ask verification questions
- [ ] Confirm agent comprehension
- [ ] Log handoff completion

## Examples

### Example: API Project Handoff

```bash
AGENT="dev-api-charlie"
PROJECT="backend-api"

# Compose handoff
HANDOFF=$(cat << 'EOF'
# Project Handoff: Backend API

## Project Overview
We are building a RESTful API for the main application. The API provides authentication, user management, and data CRUD operations.

Current sprint: Sprint 5 (2 weeks remaining)

## Current State
- Authentication endpoints: COMPLETE
- User CRUD endpoints: IN PROGRESS (80%)
- Data endpoints: NOT STARTED
- Documentation: PARTIAL

## Key Files
- src/api/auth.py - Authentication handlers
- src/api/users.py - User CRUD handlers (your focus)
- src/models/ - Database models
- tests/api/ - API tests
- CLAUDE.md - Project instructions
- docs/API.md - API specification

## Conventions
- Use FastAPI for all endpoints
- All endpoints return JSON
- Error responses use standard format: {"error": "message", "code": 123}
- Tests required for all new endpoints
- Use async/await for database operations

## Active Context
Current work: User update endpoint (PUT /users/{id})
Location: src/api/users.py line 145
Next step: Implement validation for user update fields
Blocked by: Nothing

## Contact
- Questions about project: ecos-chief-of-staff
- Task assignments: eoa-backend-orchestrator
- Code reviews: eia-api-integrator

Please confirm receipt and understanding.
EOF
)

# Send handoff
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "'"$AGENT"'",
    "subject": "Project Handoff: '"$PROJECT"'",
    "priority": "high",
    "content": {
      "type": "project-assignment",
      "message": "'"$(echo "$HANDOFF" | sed 's/"/\\"/g' | tr '\n' ' ')"'"
    }
  }'
```

### Example: Emergency Mid-Project Handoff

```bash
# Urgent handoff when replacing agent
OUTGOING="dev-old-agent"
INCOMING="dev-new-agent"
PROJECT="critical-fix"

# Get state from outgoing agent (if possible)
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "'"$OUTGOING"'",
    "subject": "Urgent: State Dump Required",
    "priority": "urgent",
    "content": {"type": "request", "message": "Emergency handoff needed. Please save your current state to ~/.emasoft/agent-states/'"$OUTGOING"'-emergency.json immediately."}
  }'

# Wait briefly for state dump...
sleep 30

# Handoff to incoming with emergency context
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "'"$INCOMING"'",
    "subject": "EMERGENCY Handoff: '"$PROJECT"'",
    "priority": "urgent",
    "content": {
      "type": "project-assignment",
      "message": "Emergency handoff. Previous agent state at ~/.emasoft/agent-states/'"$OUTGOING"'-emergency.json. Review and continue the critical fix. Report status immediately upon starting."
    }
  }'
```

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
