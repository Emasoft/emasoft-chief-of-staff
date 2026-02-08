---
procedure: support-skill
workflow-instruction: support
operation: emergency-handoff
parent-skill: ecos-failure-recovery
---

# Operation: Emergency Work Handoff

## Purpose

Transfer critical work immediately when deadlines cannot wait for the full agent replacement protocol.

## When To Use This Operation

- Critical deadline cannot wait for full replacement (30-120 min)
- Work must continue immediately regardless of replacement status
- High-priority tasks are blocked by agent failure

## Emergency vs Regular Handoff

| Aspect | Regular Handoff | Emergency Handoff |
|--------|-----------------|-------------------|
| Timing | After replacement ready | Immediately |
| Completeness | Full context | Minimum viable |
| Recipient | Replacement agent | Any available agent |
| Duration | Permanent | Temporary |

## Steps

### Step 1: Identify Critical Tasks

1. **Review failed agent's task queue**
   ```bash
   # Check progress tracking
   cat $CLAUDE_PROJECT_DIR/.ecos/agent-health/task-tracking.json | jq '.tasks[] | select(.agent == "FAILED_AGENT")'
   ```

2. **Identify tasks with critical deadlines**
   - Tasks due within 2 hours
   - Tasks blocking other agents
   - Tasks on critical path

3. **Document critical tasks**
   ```markdown
   ## Critical Tasks for Emergency Handoff
   1. TASK-001: [description] - Due: [time]
   2. TASK-002: [description] - Due: [time]
   ```

### Step 2: Notify Orchestrator

1. **Send urgent notification to EOA**
   > **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

   ```json
   {
     "from": "ecos-chief-of-staff",
     "to": "eoa-orchestrator",
     "subject": "URGENT: Emergency handoff required",
     "priority": "urgent",
     "content": {
       "type": "emergency-handoff-request",
       "message": "Agent [FAILED_AGENT] has failed. Critical tasks require immediate handoff.",
       "failed_agent": "FAILED_AGENT",
       "critical_tasks": ["TASK-001", "TASK-002"],
       "deadlines": {"TASK-001": "2 hours", "TASK-002": "4 hours"}
     }
   }
   ```

2. **Request available agent assignment**

### Step 3: Create Emergency Handoff Documentation

1. **Create minimal handoff document**
   ```markdown
   # Emergency Handoff: [FAILED_AGENT] -> [RECEIVING_AGENT]

   UUID: EH-[DATE]-[AGENT]-[SEQ]
   Type: emergency-handoff
   Created: [ISO8601]

   ## Critical Context
   - Task: [task description]
   - Deadline: [deadline]
   - Current state: [what was done]
   - Next step: [what needs to happen]

   ## Files
   - [list of relevant files]

   ## Blockers
   - [any known blockers]
   ```

2. **Save to emergency handoffs directory**
   ```bash
   mkdir -p $CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/emergency/
   # Save handoff document
   ```

### Step 4: Assign Work to Receiving Agent

1. **Wait for EOA to assign available agent**

2. **Send emergency handoff to receiving agent**
   > **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

   ```json
   {
     "from": "ecos-chief-of-staff",
     "to": "RECEIVING_AGENT",
     "subject": "URGENT: Emergency handoff - [TASK]",
     "priority": "urgent",
     "content": {
       "type": "emergency-handoff",
       "message": "You are receiving emergency work from failed agent [FAILED_AGENT].",
       "handoff_uuid": "EH-20250204-svgbbox-001",
       "handoff_document": "thoughts/shared/handoffs/emergency/EH-20250204-svgbbox-001.md",
       "deadline": "[deadline]"
     }
   }
   ```

3. **Confirm receipt and understanding**

### Step 5: Monitor Progress

1. **Track receiving agent's progress**
2. **Escalate if deadline at risk**
3. **Notify EAMA of emergency handoff status**

### Step 6: Post-Emergency Reconciliation

After deadline passes:
1. Determine if replacement agent ready
2. Transfer work back if appropriate
3. Document lessons learned
4. Update incident log

## Checklist

Copy this checklist and track your progress:

- [ ] Critical tasks identified
- [ ] Orchestrator (EOA) notified
- [ ] Emergency handoff documentation created
- [ ] Receiving agent assigned by EOA
- [ ] Emergency handoff sent to receiving agent
- [ ] Receiving agent acknowledged
- [ ] Work transfer verified
- [ ] Progress monitored
- [ ] Deadline met OR escalated
- [ ] Post-emergency reconciliation completed

## Handoff Validation

Before sending any emergency handoff, validate:

- [ ] UUID is unique
- [ ] Target agent exists and is alive
- [ ] All referenced files exist
- [ ] No placeholder [TBD] markers
- [ ] Deadline clearly specified

## Output

After completing this operation:
- Critical work transferred to available agent
- Deadline tracking active
- Regular replacement can proceed in parallel

## Related References

- [work-handoff-during-failure.md](work-handoff-during-failure.md) - Complete handoff procedures
- [agent-replacement-protocol.md](agent-replacement-protocol.md) - Full replacement protocol
- [examples.md](examples.md) - Emergency handoff examples
