---
procedure: support-skill
workflow-instruction: support
operation: route-task-blocker
parent-skill: ecos-failure-recovery
---

# Operation: Route Task Blocker

## Purpose

Determine how to handle task blocker escalations - resolve directly if within ECOS authority, or route to EAMA if user decision required.

## When To Use This Operation

- When receiving blocker escalation from EOA
- When work cannot proceed due to missing information or access
- When a decision requires user input

## Decision Tree

```
ECOS receives escalation from EOA
  |
  +-- Is it an agent failure? (crash, unresponsive, repeated failure)
  |     -> YES: Handle via failure recovery workflow (use other op-* files)
  |
  +-- Is it a task blocker that ECOS can resolve?
  |     +-- Agent reassignment needed -> Handle directly
  |     +-- Permission within ECOS authority -> Handle directly
  |
  +-- Is it a task blocker requiring user input?
        -> YES: Route to EAMA using blocker-escalation template
```

## Steps

### Step 1: Receive and Classify Escalation

1. **Receive escalation from EOA**
   - Note the escalation type
   - Note the task and blocker details

2. **Classify escalation type**
   - Agent failure: Use failure recovery workflow
   - Task blocker (ECOS can resolve): Handle directly
   - Task blocker (user decision needed): Route to EAMA

### Step 2A: Handle Directly (If ECOS Can Resolve)

If blocker is agent reassignment or permission within ECOS authority:

1. Take appropriate action
2. Notify EOA of resolution
3. Document resolution

### Step 2B: Route to EAMA (If User Decision Needed)

1. **Compose blocker-escalation message**
   > **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

   ```json
   {
     "from": "ecos-chief-of-staff",
     "to": "eama-assistant-manager",
     "subject": "BLOCKER: Task requires user decision",
     "priority": "high",
     "content": {
       "type": "blocker-escalation",
       "message": "A task is blocked and requires user input. EOA has escalated this after determining the blocker cannot be resolved by agents.",
       "task_uuid": "[task-uuid]",
       "issue_number": "[GitHub issue number of the blocked task]",
       "blocker_issue_number": "[GitHub issue number tracking the blocker problem]",
       "blocker_type": "user-decision",
       "blocker_description": "[What is blocking and why agents cannot resolve it]",
       "impact": "[Affected agents and tasks]",
       "options": ["[Options if available]"],
       "escalated_from": "eoa-[project-name]",
       "original_blocker_time": "[ISO8601 timestamp]"
     }
   }
   ```

2. **Send to EAMA via AI Maestro**

3. **Track the blocker in ECOS records**

### Step 3: Wait for Resolution

1. Monitor for EAMA response
2. When EAMA responds with user's decision, proceed to Step 4

### Step 4: Route Resolution Back to EOA

1. **Receive blocker-resolution from EAMA**
   - Verify it includes user's exact decision (RULE 14)

2. **Route to EOA**
   > **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

   ```json
   {
     "from": "ecos-chief-of-staff",
     "to": "eoa-orchestrator",
     "subject": "RESOLUTION: Blocker [issue_number] resolved",
     "priority": "high",
     "content": {
       "type": "blocker-resolution",
       "message": "User has provided decision for blocker.",
       "blocker_issue_number": "[GitHub issue number]",
       "resolution": "[User's exact decision]",
       "resolved_by": "user via EAMA"
     }
   }
   ```

3. **Verify EOA acknowledges receipt**

4. **Update ECOS records to mark blocker as resolved**

## Checklist: Routing a Task Blocker

- [ ] Receive escalation from EOA
- [ ] Determine escalation type: agent failure OR task blocker
- [ ] If agent failure: use failure recovery workflow (Phases 1-5)
- [ ] If task blocker that ECOS can resolve: handle directly
- [ ] If task blocker requiring user input: compose blocker-escalation message
- [ ] Include `blocker_issue_number` in the message
- [ ] Send escalation to EAMA via AI Maestro
- [ ] Track blocker in ECOS records
- [ ] When EAMA responds: route resolution back to EOA
- [ ] Verify EOA acknowledges receipt
- [ ] Update ECOS records

## Checklist: When EAMA Returns a Resolution

- [ ] Receive blocker-resolution message from EAMA
- [ ] Verify resolution includes user's exact decision
- [ ] Route resolution to EOA via AI Maestro
- [ ] Verify EOA acknowledges receipt
- [ ] Note: EOA will close blocker issue and notify agent
- [ ] Update ECOS records to mark blocker as resolved

## Output

After completing this operation:
- Blocker routed to appropriate party
- Resolution tracked back to EOA
- ECOS records updated

## Related References

- [troubleshooting.md](troubleshooting.md) - Common blocker issues
- [agent-replacement-protocol.md](agent-replacement-protocol.md) - If blocker requires replacement
