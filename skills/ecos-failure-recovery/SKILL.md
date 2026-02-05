---
name: ecos-failure-recovery
description: Use when recovering from agent failures or coordinating agent replacements. Trigger with failure events.
license: Apache-2.0
compatibility: Requires AI Maestro installed.
context: fork
agent: ecos-main
---

# ECOS Failure Recovery Skill

## Overview

This skill teaches the Emasoft Chief of Staff (ECOS) how to detect, classify, and recover from agent failures in a multi-agent system coordinated via AI Maestro messaging.

**When to use this skill:**
- When monitoring remote agent health
- When an agent becomes unresponsive
- When an agent crashes or terminates unexpectedly
- When work must be transferred due to agent failure
- When a replacement agent must be created and onboarded

## Prerequisites

Before using this skill, ensure:
1. AI Maestro is running locally
2. Agent registry is accessible
3. Recovery scripts are available in scripts/

## Instructions

1. Detect the failure using heartbeat monitoring, message delivery status, or task completion timeouts
2. Classify the failure as transient, recoverable, or terminal using the classification criteria
3. Apply the appropriate recovery strategy based on failure type
4. If recovery fails or failure is terminal, initiate agent replacement protocol
5. For critical deadlines, use emergency handoff to transfer work immediately
6. Document all incidents in the incident log and notify EAMA of outcomes

### Checklist

Copy this checklist and track your progress:

```markdown
## ECOS Failure Response Checklist

Agent: _______________
Failure detected: _______________

### Detection
- [ ] Heartbeat status checked
- [ ] AI Maestro agent status queried
- [ ] Message delivery verified
- [ ] Task progress reviewed

### Classification
- [ ] Failure type determined: [ ] Transient [ ] Recoverable [ ] Terminal
- [ ] Evidence documented
- [ ] Incident logged

### Response (choose path)

#### If Transient:
- [ ] Waited for auto-recovery (< 5 min)
- [ ] Verified agent responsive
- [ ] Resumed normal monitoring

#### If Recoverable:
- [ ] Manager notified
- [ ] Recovery strategy selected
- [ ] Recovery attempted
- [ ] Recovery verified OR escalated to replacement

#### If Terminal:
- [ ] Manager notified
- [ ] Replacement approval requested
- [ ] Artifacts preserved
- [ ] Replacement agent created
- [ ] Orchestrator notified
- [ ] Handoff documentation sent
- [ ] New agent acknowledged
- [ ] Incident closed

### Emergency Handoff (if deadline critical):
- [ ] Critical tasks identified
- [ ] Orchestrator notified
- [ ] Receiving agent assigned
- [ ] Handoff documentation created
- [ ] Work transferred
- [ ] Deadline met OR escalated
```

## Output

| Recovery Type | Output |
|---------------|--------|
| Agent restart | Agent back online, state restored |
| Communication | Message queue cleared, connection restored |
| State | Corrupted state replaced with backup |

## Quick Reference: Failure Response Workflow

```
DETECT --> CLASSIFY --> RESPOND
   |           |           |
   v           v           v
Heartbeat    Transient?    Wait & Retry
timeout?     --> Yes -->   (auto-recover)
   |              |
Message          No
delivery         |
failed?          v
   |         Recoverable?
Agent        --> Yes -->   Restart / Wake
offline?          |        (intervention needed)
                  |
                  No
                  |
                  v
              Terminal -->  Replace Agent
                           (full protocol)
```

## Procedures Summary

| Phase | Action | Reference Document |
|-------|--------|-------------------|
| 1 | Detect failure | [failure-detection.md](references/failure-detection.md) |
| 2 | Classify severity | [failure-classification.md](references/failure-classification.md) |
| 3 | Attempt recovery | [recovery-strategies.md](references/recovery-strategies.md) |
| 4 | Replace if terminal | [agent-replacement-protocol.md](references/agent-replacement-protocol.md) |
| 5 | Emergency handoff | [work-handoff-during-failure.md](references/work-handoff-during-failure.md) |

---

## Phase 1: Failure Detection

Before responding to a failure, ECOS must first detect that a failure has occurred.

**Read [references/failure-detection.md](references/failure-detection.md) for:**
- 1.1-1.2 Overview and when to use
- 1.3 Heartbeat monitoring via AI Maestro
- 1.4 Message delivery failure detection
- 1.5 Task completion timeout detection
- 1.6 Agent status API queries
- 1.7 Decision flowchart

| Mechanism | Signal | Response Time |
|-----------|--------|---------------|
| Heartbeat timeout | Missed pings | 30-60 seconds |
| Message delivery failure | API error | Immediate |
| Message acknowledgment timeout | No ACK | 5-15 minutes |
| Task completion timeout | Stalled progress | Variable |

---

## Phase 2: Failure Classification

Once detected, classify severity to determine response.

**Read [references/failure-classification.md](references/failure-classification.md) for:**
- 2.1-2.2 Overview and categories
- 2.3 Transient failures (auto-recover < 5 min)
- 2.4 Recoverable failures (intervention needed)
- 2.5 Terminal failures (replacement required)
- 2.6-2.8 Decision matrix and escalation

| Category | Severity | Recovery | Example |
|----------|----------|----------|---------|
| **Transient** | Low | Automatic (< 5 min) | Network hiccup, API rate limit |
| **Recoverable** | Medium | With intervention | Session hibernated, out of memory |
| **Terminal** | High | Replacement required | Host crash, disk corruption |

---

## Phase 3: Recovery Strategies

For transient and recoverable failures, attempt recovery before escalating.

**Read [references/recovery-strategies.md](references/recovery-strategies.md) for:**
- 3.1-3.2 Overview and strategy selection
- 3.3 Wait and Retry (transient)
- 3.4 Restart Agent (soft/hard procedures)
- 3.5 Hibernate-Wake Cycle
- 3.6 Resource Adjustment
- 3.7-3.8 When to replace and flowchart

| Strategy | When to Use | Time to Recover |
|----------|-------------|-----------------|
| Wait and Retry | Transient failures | 1-5 minutes |
| Restart | Hung/crashed agent | 5-15 minutes |
| Hibernate-Wake | Idle/suspended session | 2-5 minutes |
| Resource Adjustment | Memory/disk exhaustion | 15-60 minutes |
| Replace | All above failed | 30-120 minutes |

---

## Phase 4: Agent Replacement Protocol

When recovery fails or failure is terminal, create a replacement agent.

**Read [references/agent-replacement-protocol.md](references/agent-replacement-protocol.md) for:**
- 4.1-4.2 Overview
- 4.3 Phase 1: Failure confirmation and artifact preservation
- 4.4 Phase 2: Manager notification and approval
- 4.5 Phase 3: Creating replacement agent
- 4.6 Phase 4: Orchestrator notification
- 4.7 Phase 5: Work handoff to new agent
- 4.8-4.9 Cleanup and complete checklist

### Replacement Protocol Summary

```
ECOS detects terminal failure
         |
         v
ECOS notifies EAMA (manager) --> EAMA approves
         |
         v
ECOS coordinates new agent creation
         |
         v
ECOS notifies EOA (orchestrator) to:
  - Generate handoff document
  - Update GitHub Project kanban
         |
         v
ECOS sends handoff docs to new agent
         |
         v
New agent acknowledges and begins work
```

### Key Consideration: Memory Loss

**CRITICAL**: The replacement agent has NO MEMORY of the old agent.

The new agent does not know what tasks were assigned, what work was in progress, or the project context. Therefore:
- Orchestrator (EOA) must generate handoff documentation
- EOA must reassign tasks in GitHub Project kanban
- ECOS must send handoff docs to new agent

**ROLE BOUNDARY**: ECOS creates agents and sends context. EOA owns task assignment.

---

## Phase 5: Emergency Work Handoff

When critical work cannot wait for full replacement protocol.

**Read [references/work-handoff-during-failure.md](references/work-handoff-during-failure.md) for:**
- 5.1-5.2 Overview and when to use
- 5.3 Triggering emergency handoff
- 5.4 Creating emergency handoff documentation
- 5.5 Reassigning work during failure
- 5.6 Emergency handoff message formats
- 5.7 Post-failure work reconciliation

| Aspect | Regular Handoff | Emergency Handoff |
|--------|-----------------|-------------------|
| Timing | After replacement ready | Immediately |
| Completeness | Full context | Minimum viable |
| Recipient | Replacement agent | Any available agent |
| Duration | Permanent | Temporary |

---

## Task Blockers vs Agent Failures

ECOS handles TWO types of escalations differently:

### Agent Failures (ECOS resolves directly)

An agent failure occurs when an agent crashes, becomes unresponsive, or repeatedly fails. ECOS handles this by:
1. Detecting the failure (heartbeat, message timeout, task timeout)
2. Attempting recovery (wake, restart)
3. If unrecoverable: replacing the agent and handing off work
4. Notifying EAMA of the emergency handoff (notification only, no approval needed)

### Task Blockers (ECOS routes to EAMA for user decision)

A task blocker occurs when work cannot proceed due to missing information, access, or a decision that only the user can make. When ECOS receives a task blocker escalation from EOA:

1. Determine if ECOS can resolve the blocker:
   - Agent reassignment needed → ECOS handles directly
   - Permission or access issue within ECOS authority → ECOS handles directly
   - User decision or input needed → Route to EAMA
2. If routing to EAMA, use this template:

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

3. Track the blocker in ECOS records
4. When EAMA responds with user's decision, route it back to EOA

### Decision Tree

```
ECOS receives escalation
  │
  ├─ Is it an agent failure? (crash, unresponsive, repeated failure)
  │   └─ YES → Handle via failure recovery workflow (this skill)
  │
  ├─ Is it a task blocker that ECOS can resolve?
  │   ├─ Agent reassignment → Handle directly
  │   └─ Permission within authority → Handle directly
  │
  └─ Is it a task blocker requiring user input?
      └─ YES → Route to EAMA using blocker-escalation template above
```

---

## File Locations

| Data | Location |
|------|----------|
| Heartbeat configuration | `$CLAUDE_PROJECT_DIR/.ecos/agent-health/heartbeat-config.json` |
| Task tracking | `$CLAUDE_PROJECT_DIR/.ecos/agent-health/task-tracking.json` |
| Incident log | `$CLAUDE_PROJECT_DIR/.ecos/agent-health/incident-log.jsonl` |
| Recovery log | `$CLAUDE_PROJECT_DIR/.ecos/agent-health/recovery-log.jsonl` |
| Handoff documents | `$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/AGENT_NAME/` |
| Emergency handoffs | `$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/emergency/` |

---

## Manager Notification Priorities

| Situation | Priority | Message Type |
|-----------|----------|--------------|
| Transient failure (pattern) | `normal` | `escalation` |
| Recoverable failure detected | `high` | `failure-report` |
| Recovery attempt failed | `high` | `failure-report` |
| Terminal failure detected | `urgent` | `replacement-request` |
| Emergency handoff initiated | `urgent` | `emergency-handoff-notification` |
| Replacement complete | `normal` | `replacement-complete` |

---

## Troubleshooting

Common issues when recovering from agent failures.

**Read [references/troubleshooting.md](references/troubleshooting.md) for:**
- Agent shows online but unresponsive -> Verify hooks and send status inquiry
- Cannot determine failure type -> Default to recoverable, attempt strategies in order
- Manager does not respond -> Wait 15 min, send reminder, escalate to user if needed
- New replacement agent fails to register -> Verify AI Maestro health and hooks
- Emergency handoff deadline missed -> Document, notify stakeholders, conduct post-mortem

## Handoff Validation Checklist

Before sending any handoff document (regular or emergency), validate using this checklist:

```markdown
### Handoff Validation Checklist

Before sending handoff:
- [ ] All required fields present (from/to/type/UUID/task)
- [ ] UUID is unique (check existing handoffs: `ls $CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/`)
- [ ] Target agent exists and is alive (`curl -s "http://localhost:23000/api/agents" | jq -r '.agents[].name'`)
- [ ] All referenced files exist (`test -f <path> && echo "EXISTS" || echo "MISSING"`)
- [ ] No placeholder [TBD] markers (`grep -r "\[TBD\]" handoff.md`)
- [ ] Document is valid markdown (no broken links, proper formatting)
- [ ] Acceptance criteria clearly defined
- [ ] Current state accurately reflects reality
- [ ] Contact information for questions provided
```

**Required fields for failure recovery handoffs:**

| Field | Description | Example |
|-------|-------------|---------|
| `from` | Sending agent name | `ecos-chief-of-staff` |
| `to` | Target agent name | `replacement-agent-001` |
| `type` | Handoff type | `emergency-handoff`, `replacement-handoff` |
| `UUID` | Unique handoff identifier | `EH-20250204-svgbbox-001` |
| `task` | Task being handed off | `Implement bounding box calculation` |
| `failed_agent` | Name of failed agent | `libs-svg-svgbbox` |
| `failure_reason` | Why agent failed | `Terminal crash - disk corruption` |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Agent unresponsive | Network issue or crash | Send ping, wait 30s, then classify |
| Recovery failed | State corrupted | Escalate to terminal, request replacement |
| Handoff rejected | Target agent busy | Queue handoff, retry in 5 minutes |
| AI Maestro unavailable | Server down | Use fallback file-based communication |

## Examples

Recovery scenarios with step-by-step commands.

**Read [references/examples.md](references/examples.md) for:**
- Agent crash recovery (recoverable -> restart -> verify)
- Terminal failure with replacement (3 crashes -> replace -> handoff)
- Transient network failure (wait -> auto-recover)
- Emergency handoff with deadline (immediate reassignment)
- Quick command reference (heartbeat, status, restart, approval, handoff)

## Resources

- [references/failure-detection.md](references/failure-detection.md) - Detection procedures
- [references/failure-classification.md](references/failure-classification.md) - Classification criteria
- [references/recovery-strategies.md](references/recovery-strategies.md) - Recovery steps
- [references/recovery-operations.md](references/recovery-operations.md) - Recovery operations procedures
- [references/agent-replacement-protocol.md](references/agent-replacement-protocol.md) - Replacement workflow
- [references/work-handoff-during-failure.md](references/work-handoff-during-failure.md) - Work transfer procedures
- [references/troubleshooting.md](references/troubleshooting.md) - Common issues and solutions
- [references/examples.md](references/examples.md) - Complete recovery examples
