---
procedure: support-skill
workflow-instruction: support
operation: replace-agent
parent-skill: ecos-failure-recovery
---

# Operation: Replace Agent


## Contents

- [Purpose](#purpose)
- [When To Use This Operation](#when-to-use-this-operation)
- [Critical Consideration](#critical-consideration)
- [Steps](#steps)
  - [Phase 1: Confirm Failure and Preserve Artifacts](#phase-1-confirm-failure-and-preserve-artifacts)
  - [Phase 2: Request Manager Approval](#phase-2-request-manager-approval)
  - [Phase 3: Create Replacement Agent](#phase-3-create-replacement-agent)
  - [Phase 4: Notify Orchestrator](#phase-4-notify-orchestrator)
  - [Phase 5: Send Handoff to New Agent](#phase-5-send-handoff-to-new-agent)
  - [Phase 6: Cleanup and Close Incident](#phase-6-cleanup-and-close-incident)
- [Checklist](#checklist)
- [Output](#output)
- [Related References](#related-references)
- [Next Operation](#next-operation)

## Purpose

Create a replacement agent when recovery fails or failure is terminal, ensuring work continuity and proper handoff.

## When To Use This Operation

- After recovery strategies have failed
- When failure is classified as TERMINAL
- When replacement is the only option for work continuity

## Critical Consideration

**The replacement agent has NO MEMORY of the old agent.**

The new agent does not know:
- What tasks were assigned
- What work was in progress
- The project context

Therefore:
- Orchestrator (EOA) must generate handoff documentation
- EOA must reassign tasks in GitHub Project kanban
- ECOS must send handoff docs to new agent

## Steps

### Phase 1: Confirm Failure and Preserve Artifacts

1. **Confirm agent is unrecoverable**
   Use the `ai-maestro-agents-management` skill to perform a final status check on the agent.

2. **Preserve work artifacts**
   - Save any accessible output files
   - Backup logs if available
   - Document last known state

3. **Record in incident log**
   ```json
   {
     "event": "terminal_failure_confirmed",
     "agent": "failed-agent-name",
     "timestamp": "ISO8601",
     "recovery_attempts": 3,
     "artifacts_preserved": ["list", "of", "files"]
   }
   ```

### Phase 2: Request Manager Approval

1. **Notify EAMA (Assistant Manager)**
   > **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

   ```json
   {
     "from": "ecos-chief-of-staff",
     "to": "eama-assistant-manager",
     "subject": "APPROVAL NEEDED: Replace agent [AGENT_NAME]",
     "priority": "urgent",
     "content": {
       "type": "replacement-request",
       "message": "Agent [AGENT_NAME] has failed terminally. Requesting approval to create replacement.",
       "failed_agent": "AGENT_NAME",
       "failure_type": "terminal",
       "recovery_attempts": 3,
       "impact": "Tasks X, Y, Z are blocked"
     }
   }
   ```

2. **Wait for approval** (max 15 minutes)

3. **If no response**: Send reminder, then escalate to user

### Phase 3: Create Replacement Agent

1. **Determine replacement agent type**
   - Same specialization as failed agent
   - Or reassign to available agent with similar skills

2. **Request agent creation**
   - Use appropriate agent creation method
   - Assign same role/specialization

3. **Verify new agent registration**
   Use the `ai-maestro-agents-management` skill to list agents and verify the new agent appears in the registry.

### Phase 4: Notify Orchestrator

1. **Send notification to EOA**
   > **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

   ```json
   {
     "from": "ecos-chief-of-staff",
     "to": "eoa-orchestrator",
     "subject": "Agent replaced - handoff needed",
     "priority": "high",
     "content": {
       "type": "replacement-notification",
       "message": "Agent [OLD_AGENT] has been replaced by [NEW_AGENT]. Please generate handoff documentation and reassign tasks.",
       "failed_agent": "OLD_AGENT_NAME",
       "replacement_agent": "NEW_AGENT_NAME",
       "affected_tasks": ["task-1", "task-2"]
     }
   }
   ```

2. **Wait for EOA to generate handoff documentation**

### Phase 5: Send Handoff to New Agent

1. **Receive handoff docs from EOA**

2. **Send handoff to new agent**
   > **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

   ```json
   {
     "from": "ecos-chief-of-staff",
     "to": "NEW_AGENT_NAME",
     "subject": "HANDOFF: Taking over from [OLD_AGENT]",
     "priority": "high",
     "content": {
       "type": "handoff",
       "message": "You are replacing [OLD_AGENT]. See attached handoff documentation.",
       "handoff_document_path": "thoughts/shared/handoffs/NEW_AGENT/current.md"
     }
   }
   ```

3. **Wait for acknowledgment from new agent**

### Phase 6: Cleanup and Close Incident

1. **Deregister failed agent** (if still registered)
2. **Update incident log with closure**
3. **Notify EAMA of completion**

## Checklist

Copy this checklist and track your progress:

- [ ] Terminal failure confirmed
- [ ] Artifacts preserved
- [ ] Manager (EAMA) notified
- [ ] Replacement approval received
- [ ] Replacement agent created
- [ ] Orchestrator (EOA) notified
- [ ] Handoff documentation received from EOA
- [ ] Handoff sent to new agent
- [ ] New agent acknowledged handoff
- [ ] Failed agent deregistered
- [ ] Incident closed
- [ ] EAMA notified of completion

## Output

After completing this operation:
- New agent operational and aware of assigned work
- Failed agent deregistered
- Incident documented and closed

## Related References

- [agent-replacement-protocol.md](agent-replacement-protocol.md) - Complete replacement workflow
- [work-handoff-during-failure.md](work-handoff-during-failure.md) - Handoff procedures
- [troubleshooting.md](troubleshooting.md) - Replacement issues

## Next Operation

- Normal monitoring resumes for new agent
- If deadline critical: [op-emergency-handoff.md](op-emergency-handoff.md)
