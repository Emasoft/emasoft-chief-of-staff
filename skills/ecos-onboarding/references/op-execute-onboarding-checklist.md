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
- AI Maestro is running locally
- The `agent-messaging` skill is available
- Project documentation is available
- Team registry is accessible
- Role definition documents exist

## Procedure

### Step 1: Initiate Onboarding Session

Use the `agent-messaging` skill to send the onboarding initiation message:
- **Recipient**: the target agent session name
- **Subject**: `Welcome - Onboarding Session Starting`
- **Priority**: `high`
- **Content**: type `request`, message: "Welcome to the team. I am the Chief of Staff and will conduct your onboarding. Please confirm you are ready to begin."

Wait for confirmation response.

### Step 2: Verify Agent Identity

Use the `agent-messaging` skill to request identity confirmation:
- **Recipient**: the target agent session name
- **Subject**: `Identity Verification`
- **Priority**: `high`
- **Content**: type `request`, message: "Please confirm your session name, assigned role, and the plugin you are running."

### Step 3: Work Through Core Checklist

Send each checklist item using the `agent-messaging` skill and await acknowledgment:

**Item 1: Team Introduction**

Use the `agent-messaging` skill:
- **Recipient**: the target agent session name
- **Subject**: `Onboarding 1/6: Team Introduction`
- **Priority**: `normal`
- **Content**: type `team-notification`, message listing team members with their roles and identifying the orchestrator. Ask the agent to acknowledge when understood.

**Item 2: Communication Channels**

Use the `agent-messaging` skill to explain how to use AI Maestro messaging, how to check inbox using the `agent-messaging` skill, and how to send messages.

**Item 3: Working Directory**

Use the `agent-messaging` skill to explain the agent's working directory and project structure.

**Item 4: Key Resources**

Use the `agent-messaging` skill to share locations of CLAUDE.md, project docs, and relevant files.

**Item 5: Reporting Structure**

Use the `agent-messaging` skill to explain who to report to and escalation paths.

**Item 6: Initial Task Assignment**

Use the `agent-messaging` skill to inform of first task or to await orchestrator assignment.

### Step 4: Confirm Completion

Use the `agent-messaging` skill to request final confirmation:
- **Recipient**: the target agent session name
- **Subject**: `Onboarding Complete`
- **Priority**: `high`
- **Content**: type `request`, message: "Onboarding checklist complete. Please confirm you understand: (1) your team, (2) communication channels, (3) your working directory, (4) key resources, (5) reporting structure, (6) your initial assignment."

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

- [ ] Send onboarding initiation message via `agent-messaging` skill
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

For agent `dev-backend-alice` on project `backend-api` with role `developer`:

1. **Initiate**: Use the `agent-messaging` skill to send welcome message:
   - **Recipient**: `dev-backend-alice`
   - **Subject**: `Welcome - Onboarding Starting`
   - **Priority**: `high`
   - **Content**: type `request`, message: "Welcome to the backend-api team. Ready to begin onboarding?"
2. Wait for response
3. **Team intro**: Use the `agent-messaging` skill:
   - **Recipient**: `dev-backend-alice`
   - **Subject**: `Onboarding 1/6: Your Team`
   - **Priority**: `normal`
   - **Content**: type `team-notification`, message: "Team members: dev-backend-bob (developer), eia-api-reviewer (integrator). Orchestrator: eoa-backend-orchestrator. Acknowledge."
4. **Communication**: Use the `agent-messaging` skill:
   - **Recipient**: `dev-backend-alice`
   - **Subject**: `Onboarding 2/6: Communication`
   - **Priority**: `normal`
   - **Content**: type `request`, message: "Use AI Maestro for all team communication. Use the `agent-messaging` skill to check your inbox and send messages. Acknowledge."
5. **Working directory**: Use the `agent-messaging` skill:
   - **Recipient**: `dev-backend-alice`
   - **Subject**: `Onboarding 3/6: Working Directory`
   - **Priority**: `normal`
   - **Content**: type `request`, message: "Your working directory is ~/agents/dev-backend-alice/. Project code is in ~/projects/backend-api/. Acknowledge."
6. **Resources**: Use the `agent-messaging` skill:
   - **Recipient**: `dev-backend-alice`
   - **Subject**: `Onboarding 4/6: Key Resources`
   - **Priority**: `normal`
   - **Content**: type `request`, message: "Key files: CLAUDE.md (project instructions), docs/API.md (API specs), tests/ (test directory). Acknowledge."
7. **Reporting**: Use the `agent-messaging` skill:
   - **Recipient**: `dev-backend-alice`
   - **Subject**: `Onboarding 5/6: Reporting`
   - **Priority**: `normal`
   - **Content**: type `request`, message: "Report task progress to eoa-backend-orchestrator. Escalate blockers to ecos-chief-of-staff. Acknowledge."
8. **Initial assignment**: Use the `agent-messaging` skill:
   - **Recipient**: `dev-backend-alice`
   - **Subject**: `Onboarding 6/6: Initial Assignment`
   - **Priority**: `normal`
   - **Content**: type `request`, message: "Await task assignment from eoa-backend-orchestrator. They will contact you shortly. Acknowledge."
9. **Completion**: Use the `agent-messaging` skill:
   - **Recipient**: `dev-backend-alice`
   - **Subject**: `Onboarding Complete`
   - **Priority**: `high`
   - **Content**: type `request`, message: "Onboarding complete. Confirm understanding of all 6 items."
10. **Log**: Record onboarding completion in team registry:
    ```bash
    uv run python scripts/ecos_team_registry.py log \
      --event "onboarding-complete" \
      --agent "dev-backend-alice" \
      --reason "Initial onboarding for developer on backend-api" \
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
