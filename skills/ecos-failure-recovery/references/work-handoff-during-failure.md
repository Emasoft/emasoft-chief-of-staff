# Work Handoff During Agent Failure

## Table of Contents

- 5.1 When to use this document
- 5.2 Overview of emergency handoff
- 5.3 Triggering emergency handoff
  - 5.3.1 When to initiate emergency handoff
  - 5.3.2 Notification to orchestrator
  - 5.3.3 Notification to manager
- 5.4 Creating emergency handoff documentation
  - 5.4.1 Required handoff content
  - 5.4.2 Handoff document template
  - 5.4.3 Extracting information from failed agent
- 5.5 Reassigning work during failure
  - 5.5.1 Temporary reassignment to other agents
  - 5.5.2 Holding tasks for replacement agent
  - 5.5.3 Splitting tasks across multiple agents
- 5.6 Emergency handoff message formats
  - 5.6.1 Handoff request to orchestrator
  - 5.6.2 Task reassignment notification
  - 5.6.3 Receiving agent instructions
- 5.7 Post-failure work reconciliation
  - 5.7.1 Identifying duplicate work
  - 5.7.2 Merging partial progress
  - 5.7.3 Updating task status

---

## 5.1 When to Use This Document

Use this document when:
- An agent has failed and work must be transferred IMMEDIATELY
- There is not enough time to wait for full replacement protocol
- Critical deadlines require work to continue without delay
- You need to reassign tasks to other agents during recovery

**IMPORTANT**: This document covers EMERGENCY handoff during active failure. For planned replacement handoff, see `references/agent-replacement-protocol.md` Phase 5.

---

## 5.2 Overview of Emergency Handoff

Emergency handoff differs from replacement handoff in urgency and completeness:

| Aspect | Replacement Handoff | Emergency Handoff |
|--------|---------------------|-------------------|
| Timing | After new agent created | Immediately upon failure detection |
| Completeness | Full context transfer | Minimum viable information |
| Recipient | New replacement agent | Available agents or queue |
| Goal | Resume all work | Prevent deadline failures |
| Duration | Permanent assignment | Temporary until recovery/replacement |

**Emergency handoff principle**: Get critical work moving immediately, even with incomplete information. Perfection is the enemy of progress in emergencies.

---

## 5.3 Triggering Emergency Handoff

### 5.3.1 When to Initiate Emergency Handoff

Initiate emergency handoff when ALL of the following are true:

1. **Agent has failed** (classified as recoverable or terminal)
2. **Critical work is blocked** (deadline within 24 hours or blocking other agents)
3. **Recovery will take too long** (estimated recovery > time to deadline)

**Decision matrix:**

| Failure Type | Time to Deadline | Initiate Emergency Handoff? |
|--------------|------------------|----------------------------|
| Transient | Any | No - wait for recovery |
| Recoverable | > 2 hours | No - attempt recovery first |
| Recoverable | < 2 hours | Yes - cannot wait |
| Terminal | > 4 hours | Maybe - depends on replacement time |
| Terminal | < 4 hours | Yes - definitely |

### 5.3.2 Notification to Orchestrator

Immediately notify EOA when initiating emergency handoff.

Use the `agent-messaging` skill to send the handoff request:
- **Recipient**: `eoa-orchestrator`
- **Subject**: `[EMERGENCY] Agent failure - work handoff required`
- **Priority**: `urgent`
- **Content**: type `emergency-handoff-request`, including:
  - Message explaining the failure and deadline urgency
  - Failed agent name
  - Failure type (terminal, recoverable)
  - Recovery time estimate
  - Critical tasks list (each with task ID, title, deadline, time remaining, estimated work remaining, and whether it can be completed by another agent)
  - Non-critical tasks list (each with task ID, title, deadline, whether it can wait for replacement)
  - Action requested: "reassign_critical_tasks"
  - Suggested recipient agent (if known)

**Verify**: confirm message delivery via the `agent-messaging` skill's sent messages feature.

### 5.3.3 Notification to Manager

Notify EAMA about the emergency handoff.

Use the `agent-messaging` skill to send notification:
- **Recipient**: `eama-assistant-manager`
- **Subject**: `[ALERT] Emergency work handoff initiated`
- **Priority**: `urgent`
- **Content**: type `emergency-handoff-notification`, including:
  - Message explaining the reason for emergency handoff
  - Failed agent name
  - Tasks being reassigned (list of task IDs)
  - Tasks being held for replacement (list of task IDs)
  - Reason for the decision
  - This is a notification only (not awaiting approval)

**Verify**: confirm message delivery via the `agent-messaging` skill's sent messages feature.

---

## 5.4 Creating Emergency Handoff Documentation

### 5.4.1 Required Handoff Content

Emergency handoff documentation is MINIMAL but must include:

| Required | Content | Why |
|----------|---------|-----|
| YES | Task ID and title | Identification |
| YES | Current status (% complete) | Where to start |
| YES | Acceptance criteria | What "done" looks like |
| YES | Key files/locations | Where to find the work |
| YES | Immediate next steps | What to do first |
| NO | Full history | Takes too long to compile |
| NO | All context | Receiving agent will ask if needed |

### 5.4.2 Handoff Document Template

```markdown
# EMERGENCY HANDOFF - [TASK_ID]

**URGENT**: This is an emergency handoff due to agent failure.
**Original Agent**: [FAILED_AGENT_NAME]
**Handoff Time**: [ISO_TIMESTAMP]
**Deadline**: [DEADLINE_TIMESTAMP]

## Task Summary
- **Task ID**: [TASK_ID]
- **Title**: [TASK_TITLE]
- **Status**: [% complete] complete
- **Priority**: CRITICAL

## Acceptance Criteria
[What must be true for this task to be considered complete]

## Current State
- **Last commit**: [COMMIT_HASH] "[COMMIT_MESSAGE]"
- **Branch**: [BRANCH_NAME]
- **Key files modified**:
  - `path/to/file1.py` - [brief description of changes]
  - `path/to/file2.py` - [brief description of changes]

## Immediate Next Steps
1. [First thing to do]
2. [Second thing to do]
3. [Third thing to do]

## Known Issues / Blockers
- [Any known issues]
- [Any blockers]

## Contact for Questions
- Ask ECOS (ecos-chief-of-staff) for clarification
- Check GitHub issue: [ISSUE_URL]

## DO NOT
- Do not rewrite existing work - build on what exists
- Do not change the approach without discussing first
```

### 5.4.3 Extracting Information from Failed Agent

If ECOS has any historical data about the failed agent's work, use it:

**From task tracking:**
```bash
jq --arg task "task-001" '.tasks[] | select(.task_id == $task)' \
  $CLAUDE_PROJECT_DIR/.ecos/agent-health/task-tracking.json
```

**From git history:**
```bash
# Get recent commits by the failed agent's work
git log --oneline --author="libs-svg-svgbbox" -10

# Get files changed in recent commits
git diff --name-only HEAD~5..HEAD
```

**From previous messages:**

Use the `agent-messaging` skill to list recent messages sent by the failed agent (limit to last 5 messages).

---

## 5.5 Reassigning Work During Failure

### 5.5.1 Temporary Reassignment to Other Agents

When reassigning to another agent:

1. **Identify capable agents** - agents with relevant skills/context
2. **Check agent availability** - are they overloaded?
3. **Request reassignment from EOA**

Use the `agent-messaging` skill to request reassignment:
- **Recipient**: `eoa-orchestrator`
- **Subject**: `[REQUEST] Temporary task reassignment`
- **Priority**: `urgent`
- **Content**: type `task-reassignment-request`, including:
  - Message requesting temporary reassignment
  - Task ID
  - From agent (failed)
  - Suggested receiving agents
  - Reassignment type: "temporary"
  - Flag: return to replacement agent when available
  - Handoff document path

### 5.5.2 Holding Tasks for Replacement Agent

Non-critical tasks should be held, not reassigned.

Use the `agent-messaging` skill to notify the orchestrator:
- **Recipient**: `eoa-orchestrator`
- **Subject**: `[INFO] Tasks being held for replacement agent`
- **Priority**: `normal`
- **Content**: type `task-hold-notification`, including:
  - Message explaining tasks are on hold
  - Failed agent name
  - Tasks on hold (each with task ID, title, and reason for holding)
  - Will be assigned to replacement agent
  - Estimated replacement time

### 5.5.3 Splitting Tasks Across Multiple Agents

If a task is large, it may be split.

Use the `agent-messaging` skill to request a task split:
- **Recipient**: `eoa-orchestrator`
- **Subject**: `[REQUEST] Split task for parallel work`
- **Priority**: `urgent`
- **Content**: type `task-split-request`, including:
  - Message explaining the split request
  - Original task ID
  - Proposed split (each subtask with ID, title, estimated time, suggested agent)
  - Coordination requirements for merging results

---

## 5.6 Emergency Handoff Message Formats

### 5.6.1 Handoff Request to Orchestrator

Use the `agent-messaging` skill to request EOA to coordinate emergency handoff:
- **Recipient**: `eoa-orchestrator`
- **Subject**: `[EMERGENCY HANDOFF] Immediate coordination required`
- **Priority**: `urgent`
- **Content**: type `emergency-handoff-coordination`, including:
  - Message: "EMERGENCY: Agent failure requires immediate work reassignment to meet deadlines."
  - Situation details (failed agent, failure type, failure time, recovery status)
  - Critical tasks list (each with task ID, deadline, status percent, handoff document path)
  - Requested actions (identify available agent, update GitHub Project, send handoff, monitor progress)
  - What ECOS will handle (continue replacement, notify when ready, reconcile work)

### 5.6.2 Task Reassignment Notification

Use the `agent-messaging` skill to notify the receiving agent:
- **Recipient**: the receiving agent session name
- **Subject**: `[EMERGENCY ASSIGNMENT] Critical task reassigned to you`
- **Priority**: `urgent`
- **Content**: type `emergency-task-assignment`, including:
  - Message: "CRITICAL: You are receiving an emergency task reassignment due to another agent failure. This task has an imminent deadline."
  - Task details (ID, title, deadline, time remaining, current status, estimated work remaining)
  - Handoff document path
  - Step-by-step instructions (stop current work, read handoff doc, clone/pull repo, checkout branch, review last commit, continue work, complete before deadline)
  - Support contact information
  - Acknowledgment required with deadline

### 5.6.3 Receiving Agent Instructions

Use the `agent-messaging` skill to send detailed instructions:
- **Recipient**: the receiving agent session name
- **Subject**: `[INSTRUCTIONS] How to proceed with emergency task`
- **Priority**: `high`
- **Content**: type `emergency-task-instructions`, including:
  - Setup steps (clone repo, fetch changes, checkout branch, pull, review last commit)
  - Work guidelines (build on existing work, match coding style, ask before changing approach, commit frequently, test before marking complete)
  - Completion criteria (acceptance criteria met, tests pass, code committed and pushed, PR created or merged)
  - Reporting structure (progress to ECOS, blockers to EOA, completion to both)

**Verify**: confirm message delivery via the `agent-messaging` skill's sent messages feature.

---

## 5.7 Post-Failure Work Reconciliation

### 5.7.1 Identifying Duplicate Work

After emergency handoff, there may be duplicate work if:
- Failed agent partially committed work before failure
- Receiving agent redid some work unnecessarily
- Multiple agents worked on split tasks with overlap

**Detection:**
```bash
# Compare commits from both agents
git log --oneline --author="failed-agent" feature/bounding-box
git log --oneline --author="receiving-agent" feature/bounding-box

# Check for overlapping file changes
git diff failed-agent-last-commit..receiving-agent-first-commit --name-only
```

### 5.7.2 Merging Partial Progress

If both agents made progress, request EOA to coordinate the merge.

Use the `agent-messaging` skill to request reconciliation:
- **Recipient**: `eoa-orchestrator`
- **Subject**: `[RECONCILIATION] Work merge required`
- **Priority**: `normal`
- **Content**: type `work-reconciliation-request`, including:
  - Message: "Emergency handoff resulted in overlapping work. Please coordinate merge."
  - Task ID
  - Work sources (each with agent name, commit range, files affected)
  - Recommended action
  - Needs review flag

### 5.7.3 Updating Task Status

After reconciliation, update all tracking systems:

**1. Update ECOS task tracking:**
```bash
jq --arg task "task-001" --arg status "completed" '
  .tasks[] |
  select(.task_id == $task) |
  .status = $status |
  .completed_by = "apps-svgplayer-development (emergency handoff)" |
  .completed_at = (now | strftime("%Y-%m-%dT%H:%M:%SZ"))
' $CLAUDE_PROJECT_DIR/.ecos/agent-health/task-tracking.json > temp.json && mv temp.json $CLAUDE_PROJECT_DIR/.ecos/agent-health/task-tracking.json
```

**2. Request GitHub Project update from EOA:**

Use the `agent-messaging` skill to request update:
- **Recipient**: `eoa-orchestrator`
- **Subject**: `[UPDATE] Task status after emergency handoff`
- **Priority**: `normal`
- **Content**: type `task-status-update`, including task ID, new status, completed by agent, notes about the emergency handoff, and PR URL

**3. Notify manager of resolution:**

Use the `agent-messaging` skill to report resolution:
- **Recipient**: `eama-assistant-manager`
- **Subject**: `[RESOLVED] Emergency handoff completed successfully`
- **Priority**: `normal`
- **Content**: type `emergency-handoff-resolution`, including summary with original agent, receiving agent, task ID, deadline, completion time, outcome, and replacement status

---

## Troubleshooting

### No agents available for emergency handoff

**Symptom**: All potential receiving agents are busy or overloaded.

**Solution**:
1. Check if any agent can deprioritize their current work
2. Request manager approval for overtime/parallel work
3. As last resort, notify user that deadline may be missed
4. Document the situation for post-mortem

### Receiving agent cannot access repository

**Symptom**: Agent reports git clone/pull failures.

**Solution**:
1. Verify repository URL is correct
2. Check agent has necessary credentials: `gh auth status`
3. Provide alternative access (manual file transfer if desperate)
4. Consider different receiving agent with existing repo access

### Receiving agent's work conflicts with recovered agent

**Symptom**: After failed agent is recovered/replaced, work conflicts exist.

**Solution**:
1. Decide which work is "canonical" (usually the completed work)
2. Have EOA coordinate merge or rebase
3. Update both agents about the resolution
4. Ensure only one agent continues on the task going forward

### Deadline passed despite emergency handoff

**Symptom**: Emergency handoff initiated but deadline still missed.

**Solution**:
1. Document the timeline and bottlenecks
2. Notify stakeholders immediately
3. Complete the work as soon as possible
4. Conduct post-mortem to improve response time
5. Consider earlier escalation thresholds for future

---

## Emergency Handoff Message Template (Complete)

Use the `agent-messaging` skill to send the complete emergency handoff message:
- **Recipient**: the target agent session name
- **Subject**: `[EMERGENCY HANDOFF] Agent Failure - Work Transfer`
- **Priority**: `urgent`
- **Content**: type `emergency_handoff`, including all required fields:

**Required fields reference:**

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Must be `emergency_handoff` |
| `message` | string | Human-readable description of the failure |
| `failed_agent` | string | Name of the failed agent |
| `failure_reason` | string | Human-readable failure explanation |
| `failure_type` | string | One of: `transient`, `recoverable`, `terminal` |
| `failure_time` | string | ISO-8601 timestamp of failure detection |
| `active_tasks` | array | List of all task IDs assigned to failed agent |
| `critical_tasks` | array | Detailed objects for deadline-critical tasks (each with task_id, title, deadline, time_remaining, status_percent, branch, last_commit) |
| `state_file` | string | Path to preserved agent state (if available) |
| `handoff_document` | string | Path to emergency handoff markdown |
| `priority_actions` | array | Ordered list of immediate actions |
| `deadline_impact` | string | Business impact of missing deadline |
| `acknowledgment_required` | boolean | Must be `true` for emergency handoffs |
| `acknowledge_by` | string | ISO-8601 timestamp for ACK deadline |

**Verify**: confirm message delivery via the `agent-messaging` skill's sent messages feature.
