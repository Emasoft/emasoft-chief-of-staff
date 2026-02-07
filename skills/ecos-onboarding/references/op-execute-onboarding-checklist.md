---
operation: execute-onboarding-checklist
procedure: proc-create-team
workflow-instruction: Step 4 - Team Creation
parent-skill: ecos-onboarding
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Execute Onboarding Checklist

## When to Use

- New agent joins the team
- Agent reassigned to different project
- Agent returns from long hibernation
- Agent role significantly changes
- Starting a new work session after extended break

## Prerequisites

- Agent to be onboarded is created and running
- AI Maestro is running locally at `http://localhost:23000`
- Project documentation is available
- Team registry is accessible
- Role definition documents exist

## Procedure

### Step 1: Initiate Onboarding Session

Send onboarding initiation message to the agent:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "<agent-session-name>",
    "subject": "Welcome - Onboarding Session Starting",
    "priority": "high",
    "content": {
      "type": "request",
      "message": "Welcome to the team. I am the Chief of Staff and will conduct your onboarding. Please confirm you are ready to begin."
    }
  }'
```

Wait for confirmation response.

### Step 2: Verify Agent Identity

Confirm you are communicating with the correct agent:

```bash
# Request identity confirmation
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "<agent-session-name>",
    "subject": "Identity Verification",
    "priority": "high",
    "content": {
      "type": "request",
      "message": "Please confirm your session name, assigned role, and the plugin you are running."
    }
  }'
```

### Step 3: Work Through Core Checklist

Send each checklist item and await acknowledgment:

**Item 1: Team Introduction**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "<agent-session-name>",
    "subject": "Onboarding 1/6: Team Introduction",
    "priority": "normal",
    "content": {
      "type": "team-notification",
      "message": "Your team members are: [list teammates with roles]. The orchestrator is [orchestrator-name]. Acknowledge when understood."
    }
  }'
```

**Item 2: Communication Channels**
```bash
# Explain AI Maestro messaging, how to check inbox, how to send messages
```

**Item 3: Working Directory**
```bash
# Explain agent working directory, project structure
```

**Item 4: Key Resources**
```bash
# Share CLAUDE.md location, project docs, relevant files
```

**Item 5: Reporting Structure**
```bash
# Explain who to report to, escalation paths
```

**Item 6: Initial Task Assignment**
```bash
# Inform of first task or to await orchestrator assignment
```

### Step 4: Confirm Completion

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "<agent-session-name>",
    "subject": "Onboarding Complete",
    "priority": "high",
    "content": {
      "type": "request",
      "message": "Onboarding checklist complete. Please confirm you understand: (1) your team, (2) communication channels, (3) your working directory, (4) key resources, (5) reporting structure, (6) your initial assignment."
    }
  }'
```

### Step 5: Document Onboarding

Log the onboarding completion:

```bash
uv run python scripts/ecos_team_registry.py log \
  --event "onboarding-complete" \
  --agent "<agent-session-name>" \
  --reason "Initial onboarding for [role] on [project]" \
  --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

## Checklist

Copy this checklist and track your progress:

- [ ] Send onboarding initiation message
- [ ] Receive ready confirmation from agent
- [ ] Verify agent identity
- [ ] Send team introduction
- [ ] Explain communication channels
- [ ] Explain working directory structure
- [ ] Share key resources and documentation
- [ ] Explain reporting structure
- [ ] Provide initial task assignment info
- [ ] Receive completion confirmation
- [ ] Log onboarding in registry

## Examples

### Example: Complete Onboarding for New Developer

```bash
AGENT="dev-backend-alice"
PROJECT="backend-api"
ROLE="developer"

# Step 1: Initiate
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "'"$AGENT"'",
    "subject": "Welcome - Onboarding Starting",
    "priority": "high",
    "content": {"type": "request", "message": "Welcome to '"$PROJECT"' team. Ready to begin onboarding?"}
  }'

# Wait for response...

# Step 2: Team intro
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "'"$AGENT"'",
    "subject": "Onboarding 1/6: Your Team",
    "priority": "normal",
    "content": {"type": "team-notification", "message": "Team members: dev-backend-bob (developer), eia-api-reviewer (integrator). Orchestrator: eoa-backend-orchestrator. Acknowledge."}
  }'

# Step 3: Communication
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "'"$AGENT"'",
    "subject": "Onboarding 2/6: Communication",
    "priority": "normal",
    "content": {"type": "request", "message": "Use AI Maestro for all team communication. Check inbox with: curl -s \"http://localhost:23000/api/messages?agent='"$AGENT"'&action=list&status=unread\". Acknowledge."}
  }'

# Step 4: Working directory
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "'"$AGENT"'",
    "subject": "Onboarding 3/6: Working Directory",
    "priority": "normal",
    "content": {"type": "request", "message": "Your working directory is ~/agents/'"$AGENT"'/. Project code is in ~/projects/'"$PROJECT"'/. Acknowledge."}
  }'

# Step 5: Resources
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "'"$AGENT"'",
    "subject": "Onboarding 4/6: Key Resources",
    "priority": "normal",
    "content": {"type": "request", "message": "Key files: CLAUDE.md (project instructions), docs/API.md (API specs), tests/ (test directory). Acknowledge."}
  }'

# Step 6: Reporting
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "'"$AGENT"'",
    "subject": "Onboarding 5/6: Reporting",
    "priority": "normal",
    "content": {"type": "request", "message": "Report task progress to eoa-backend-orchestrator. Escalate blockers to ecos-chief-of-staff. Acknowledge."}
  }'

# Step 7: Initial assignment
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "'"$AGENT"'",
    "subject": "Onboarding 6/6: Initial Assignment",
    "priority": "normal",
    "content": {"type": "request", "message": "Await task assignment from eoa-backend-orchestrator. They will contact you shortly. Acknowledge."}
  }'

# Step 8: Completion confirmation
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "'"$AGENT"'",
    "subject": "Onboarding Complete",
    "priority": "high",
    "content": {"type": "request", "message": "Onboarding complete. Confirm understanding of all 6 items."}
  }'

# Step 9: Log completion
uv run python scripts/ecos_team_registry.py log \
  --event "onboarding-complete" \
  --agent "$AGENT" \
  --reason "Initial onboarding for $ROLE on $PROJECT" \
  --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Agent not responding | Session inactive or crashed | Check agent status, restart if needed |
| Agent claims not ready | Agent busy with prior task | Wait or reschedule onboarding |
| Identity verification fails | Wrong agent session | Verify session name matches registry |
| Agent doesn't acknowledge items | Communication issue | Retry, check AI Maestro status |
| Onboarding incomplete | Agent confused or overloaded | Break into smaller steps, provide examples |

## Related Operations

- [op-deliver-role-briefing.md](op-deliver-role-briefing.md) - Detailed role briefing
- [op-conduct-project-handoff.md](op-conduct-project-handoff.md) - Project-specific handoff
- [op-validate-handoff.md](op-validate-handoff.md) - Validate handoff documents
