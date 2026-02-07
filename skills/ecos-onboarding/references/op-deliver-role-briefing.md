---
operation: deliver-role-briefing
procedure: proc-create-team
workflow-instruction: Step 4 - Team Creation
parent-skill: ecos-onboarding
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Deliver Role Briefing

## When to Use

- After initial onboarding checklist
- When agent role changes
- When role responsibilities are updated
- When agent requests role clarification
- During team restructuring

## Prerequisites

- Agent is onboarded (basic checklist complete)
- Role definition document exists
- AI Maestro is running locally at `http://localhost:23000`
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

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "<agent-session-name>",
    "subject": "Role Briefing: <Role Name>",
    "priority": "high",
    "content": {
      "type": "role-assignment",
      "message": "# Role Briefing: <Role Name>\n\n## Your Assigned Role\nYou are assigned as a **<Role>** on the <Project> project.\n\n## Responsibilities\n1. <Responsibility 1>\n2. <Responsibility 2>\n3. <Responsibility 3>\n\n## Reporting Structure\n- Report to: <supervisor>\n- Coordinate with: <teammates>\n- Escalate to: <escalation contact>\n\n## Expectations\n- <Expectation 1>\n- <Expectation 2>\n\n## Resources\n- <Resource 1>\n- <Resource 2>\n\nPlease confirm you understand these responsibilities."
    }
  }'
```

### Step 4: Handle Questions

If agent asks clarifying questions:

```bash
# Answer questions directly
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "<agent-session-name>",
    "subject": "RE: Role Clarification",
    "priority": "normal",
    "content": {
      "type": "request",
      "message": "<Answer to specific question>"
    }
  }'
```

### Step 5: Confirm Understanding

Request agent to acknowledge role understanding:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "<agent-session-name>",
    "subject": "Role Understanding Confirmation",
    "priority": "high",
    "content": {
      "type": "request",
      "message": "Please summarize your understanding of your role in 2-3 sentences to confirm you have understood the briefing correctly."
    }
  }'
```

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
- [ ] Send role briefing message
- [ ] Wait for initial acknowledgment
- [ ] Answer any clarifying questions
- [ ] Request understanding confirmation
- [ ] Verify agent summary is accurate
- [ ] Correct any misunderstandings
- [ ] Log role assignment in registry

## Examples

### Example: Developer Role Briefing

```bash
AGENT="dev-backend-alice"
PROJECT="backend-api"

curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "'"$AGENT"'",
    "subject": "Role Briefing: Developer",
    "priority": "high",
    "content": {
      "type": "role-assignment",
      "message": "# Role Briefing: Developer\n\n## Your Assigned Role\nYou are assigned as a **Developer** on the '"$PROJECT"' project.\n\n## Responsibilities\n1. Implement features from the backlog\n2. Write unit tests for all new code\n3. Update documentation for your changes\n4. Participate in code reviews when requested\n5. Report blockers promptly\n\n## Reporting Structure\n- **Report to:** eoa-backend-orchestrator (task assignments)\n- **Coordinate with:** dev-backend-bob (peer developer)\n- **Escalate to:** ecos-chief-of-staff (blockers, resource issues)\n\n## Expectations\n- Acknowledge task assignments promptly\n- Provide regular status updates during active work\n- Request clarification if requirements are unclear\n- Follow project coding conventions (see CLAUDE.md)\n- Complete tasks within estimated timeframes\n\n## Resources\n- CLAUDE.md - Project instructions and conventions\n- docs/API.md - API specifications\n- tests/ - Existing test examples\n- .github/ - CI/CD configuration\n\nPlease confirm you understand these responsibilities."
    }
  }'
```

### Example: Orchestrator Role Briefing

```bash
AGENT="eoa-webapp-orchestrator"
PROJECT="webapp"

curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "'"$AGENT"'",
    "subject": "Role Briefing: Orchestrator",
    "priority": "high",
    "content": {
      "type": "role-assignment",
      "message": "# Role Briefing: Orchestrator\n\n## Your Assigned Role\nYou are the **Orchestrator** for the '"$PROJECT"' project team.\n\n## Responsibilities\n1. Receive work from EAMA and break into tasks\n2. Assign tasks to team developers\n3. Track task progress and blockers\n4. Coordinate parallel work streams\n5. Report completion to EAMA\n\n## Reporting Structure\n- **Report to:** eama-assistant-manager (work assignments)\n- **Manage:** dev-frontend-bob, dev-backend-charlie (developers)\n- **Coordinate with:** eia-webapp-integrator (code reviews)\n- **Escalate to:** ecos-chief-of-staff (team issues)\n\n## Expectations\n- Maintain clear task backlog\n- Ensure developers are not blocked\n- Provide daily progress summaries\n- Identify risks early and escalate\n- Do NOT do implementation work yourself\n\n## Resources\n- Team registry at .emasoft/team-registry.json\n- Project backlog at docs/BACKLOG.md\n- GitHub Issues for task tracking\n\nPlease confirm you understand these responsibilities."
    }
  }'
```

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
