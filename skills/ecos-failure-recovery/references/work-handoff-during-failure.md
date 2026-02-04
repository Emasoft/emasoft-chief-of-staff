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

Immediately notify EOA when initiating emergency handoff:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eoa-orchestrator",
    "subject": "[EMERGENCY] Agent failure - work handoff required",
    "priority": "urgent",
    "content": {
      "type": "emergency-handoff-request",
      "message": "Agent libs-svg-svgbbox has failed. Critical task task-001 has deadline in 90 minutes. Requesting emergency handoff to available agent.",
      "failed_agent": "libs-svg-svgbbox",
      "failure_type": "terminal",
      "recovery_estimate": "60+ minutes",
      "critical_tasks": [
        {
          "task_id": "task-001",
          "title": "Implement bounding box calculation",
          "deadline": "2025-01-15T12:00:00Z",
          "time_remaining": "90 minutes",
          "estimated_work_remaining": "45 minutes",
          "can_be_completed_by_other": true
        }
      ],
      "non_critical_tasks": [
        {
          "task_id": "task-002",
          "title": "Add unit tests for SVG parsing",
          "deadline": "2025-01-17T17:00:00Z",
          "time_remaining": "2 days",
          "can_wait_for_replacement": true
        }
      ],
      "action_requested": "reassign_critical_tasks",
      "suggested_recipient": "any_available_agent_with_svg_capability"
    }
  }'
```

### 5.3.3 Notification to Manager

Notify EAMA about the emergency handoff:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eama-assistant-manager",
    "subject": "[ALERT] Emergency work handoff initiated",
    "priority": "urgent",
    "content": {
      "type": "emergency-handoff-notification",
      "message": "Due to agent failure and imminent deadline, I am initiating emergency handoff of critical tasks. Non-critical tasks will be held for replacement agent.",
      "failed_agent": "libs-svg-svgbbox",
      "tasks_being_reassigned": ["task-001"],
      "tasks_being_held": ["task-002"],
      "reason": "task-001 deadline in 90 minutes, recovery estimate 60+ minutes",
      "awaiting_approval": false,
      "notification_only": true
    }
  }'
```

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
```bash
# Check AI Maestro for agent's last progress report
curl -s "http://localhost:23000/api/messages?agent=libs-svg-svgbbox&action=sent&limit=5" | jq '.messages[].content'
```

---

## 5.5 Reassigning Work During Failure

### 5.5.1 Temporary Reassignment to Other Agents

When reassigning to another agent:

1. **Identify capable agents** - agents with relevant skills/context
2. **Check agent availability** - are they overloaded?
3. **Request reassignment from EOA**

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eoa-orchestrator",
    "subject": "[REQUEST] Temporary task reassignment",
    "priority": "urgent",
    "content": {
      "type": "task-reassignment-request",
      "message": "Please temporarily reassign task-001 to an available agent.",
      "task_id": "task-001",
      "from_agent": "libs-svg-svgbbox (failed)",
      "suggested_agents": [
        "apps-svgplayer-development",
        "utils-media-smartmediamanager"
      ],
      "reassignment_type": "temporary",
      "return_to_replacement": true,
      "handoff_document": "thoughts/shared/handoffs/emergency/task-001-emergency-20250115.md"
    }
  }'
```

### 5.5.2 Holding Tasks for Replacement Agent

Non-critical tasks should be held, not reassigned:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eoa-orchestrator",
    "subject": "[INFO] Tasks being held for replacement agent",
    "priority": "normal",
    "content": {
      "type": "task-hold-notification",
      "message": "The following tasks are being held for the replacement agent. No action required now.",
      "failed_agent": "libs-svg-svgbbox",
      "tasks_on_hold": [
        {
          "task_id": "task-002",
          "title": "Add unit tests for SVG parsing",
          "reason": "Not deadline-critical, can wait"
        }
      ],
      "will_be_assigned_to": "libs-svg-svgbbox replacement agent",
      "estimated_replacement_time": "60 minutes"
    }
  }'
```

### 5.5.3 Splitting Tasks Across Multiple Agents

If a task is large, it may be split:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eoa-orchestrator",
    "subject": "[REQUEST] Split task for parallel work",
    "priority": "urgent",
    "content": {
      "type": "task-split-request",
      "message": "Task task-001 is too large for one agent to complete before deadline. Requesting split across multiple agents.",
      "original_task": "task-001",
      "proposed_split": [
        {
          "subtask_id": "task-001a",
          "title": "Implement bounding box for rectangles",
          "estimated_time": "20 minutes",
          "suggested_agent": "agent-a"
        },
        {
          "subtask_id": "task-001b",
          "title": "Implement bounding box for circles",
          "estimated_time": "25 minutes",
          "suggested_agent": "agent-b"
        }
      ],
      "coordination_required": "Merge results into single module after completion"
    }
  }'
```

---

## 5.6 Emergency Handoff Message Formats

### 5.6.1 Handoff Request to Orchestrator

Complete format for requesting EOA to coordinate emergency handoff:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eoa-orchestrator",
    "subject": "[EMERGENCY HANDOFF] Immediate coordination required",
    "priority": "urgent",
    "content": {
      "type": "emergency-handoff-coordination",
      "message": "EMERGENCY: Agent failure requires immediate work reassignment to meet deadlines.",
      "situation": {
        "failed_agent": "libs-svg-svgbbox",
        "failure_type": "terminal",
        "failure_time": "2025-01-15T10:00:00Z",
        "recovery_status": "replacement in progress, ETA 60 minutes"
      },
      "critical_tasks": [
        {
          "task_id": "task-001",
          "deadline": "2025-01-15T12:00:00Z",
          "status": "60% complete",
          "handoff_doc": "thoughts/shared/handoffs/emergency/task-001-emergency.md"
        }
      ],
      "requested_actions": [
        "Identify available agent for task-001",
        "Update GitHub Project to reassign task-001",
        "Send task-001 handoff to receiving agent",
        "Monitor progress until deadline"
      ],
      "ecos_will_handle": [
        "Continue agent replacement process",
        "Notify when replacement agent is ready",
        "Reconcile work after deadline passes"
      ]
    }
  }'
```

### 5.6.2 Task Reassignment Notification

Notification to receiving agent about emergency assignment:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "RECEIVING_AGENT_NAME",
    "subject": "[EMERGENCY ASSIGNMENT] Critical task reassigned to you",
    "priority": "urgent",
    "content": {
      "type": "emergency-task-assignment",
      "message": "CRITICAL: You are receiving an emergency task reassignment due to another agent failure. This task has an imminent deadline.",
      "task": {
        "task_id": "task-001",
        "title": "Implement bounding box calculation",
        "deadline": "2025-01-15T12:00:00Z",
        "time_remaining": "90 minutes",
        "current_status": "60% complete",
        "estimated_work_remaining": "45 minutes"
      },
      "handoff_document": "thoughts/shared/handoffs/emergency/task-001-emergency.md",
      "instructions": [
        "1. STOP your current work immediately",
        "2. Read the handoff document NOW",
        "3. Clone/pull the repository if needed",
        "4. Checkout branch: feature/bounding-box",
        "5. Review last commit: abc123",
        "6. Continue from where the previous agent stopped",
        "7. Complete before deadline: 2025-01-15T12:00:00Z"
      ],
      "support": "Contact ECOS or EOA immediately if you have questions or blockers",
      "acknowledgment_required": true,
      "acknowledge_by": "2025-01-15T10:35:00Z"
    }
  }'
```

### 5.6.3 Receiving Agent Instructions

Detailed instructions for the receiving agent:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "RECEIVING_AGENT_NAME",
    "subject": "[INSTRUCTIONS] How to proceed with emergency task",
    "priority": "high",
    "content": {
      "type": "emergency-task-instructions",
      "message": "Follow these detailed instructions for the emergency task.",
      "setup_steps": [
        {
          "step": 1,
          "action": "Ensure you have the repository cloned",
          "command": "git clone https://github.com/ORG/REPO.git (if not already)"
        },
        {
          "step": 2,
          "action": "Fetch latest changes",
          "command": "git fetch origin"
        },
        {
          "step": 3,
          "action": "Checkout the working branch",
          "command": "git checkout feature/bounding-box"
        },
        {
          "step": 4,
          "action": "Pull latest changes",
          "command": "git pull origin feature/bounding-box"
        },
        {
          "step": 5,
          "action": "Review the last commit",
          "command": "git show HEAD"
        }
      ],
      "work_guidelines": [
        "Build on existing work - do not start from scratch",
        "Match the coding style already in use",
        "If unsure about approach, ask before implementing",
        "Commit frequently with clear messages",
        "Test before marking complete"
      ],
      "completion_criteria": [
        "All acceptance criteria from handoff doc met",
        "Tests pass",
        "Code committed and pushed",
        "PR created (if required) or merged to main"
      ],
      "reporting": {
        "report_progress_to": "ecos-chief-of-staff",
        "report_blockers_to": "eoa-orchestrator",
        "report_completion_to": ["ecos-chief-of-staff", "eoa-orchestrator"]
      }
    }
  }'
```

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

If both agents made progress, merge carefully:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eoa-orchestrator",
    "subject": "[RECONCILIATION] Work merge required",
    "priority": "normal",
    "content": {
      "type": "work-reconciliation-request",
      "message": "Emergency handoff resulted in overlapping work. Please coordinate merge.",
      "task_id": "task-001",
      "work_sources": [
        {
          "agent": "libs-svg-svgbbox (failed)",
          "commit_range": "abc123..def456",
          "files": ["src/bbox.py"]
        },
        {
          "agent": "apps-svgplayer-development (receiving)",
          "commit_range": "ghi789..jkl012",
          "files": ["src/bbox.py", "tests/test_bbox.py"]
        }
      ],
      "recommended_action": "Keep receiving agent work, it includes failed agent changes plus completion",
      "needs_review": true
    }
  }'
```

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
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eoa-orchestrator",
    "subject": "[UPDATE] Task status after emergency handoff",
    "priority": "normal",
    "content": {
      "type": "task-status-update",
      "message": "Please update GitHub Project with final task status after emergency handoff.",
      "task_id": "task-001",
      "new_status": "completed",
      "completed_by": "apps-svgplayer-development",
      "notes": "Completed via emergency handoff from libs-svg-svgbbox (failed)",
      "pr_url": "https://github.com/ORG/REPO/pull/456"
    }
  }'
```

**3. Notify manager of resolution:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eama-assistant-manager",
    "subject": "[RESOLVED] Emergency handoff completed successfully",
    "priority": "normal",
    "content": {
      "type": "emergency-handoff-resolution",
      "message": "Emergency handoff for task-001 completed successfully. Deadline was met.",
      "summary": {
        "original_agent": "libs-svg-svgbbox",
        "receiving_agent": "apps-svgplayer-development",
        "task_id": "task-001",
        "deadline": "2025-01-15T12:00:00Z",
        "completed_at": "2025-01-15T11:45:00Z",
        "outcome": "success - deadline met with 15 minutes to spare"
      },
      "replacement_status": "libs-svg-svgbbox replacement still in progress, ETA 15 minutes"
    }
  }'
```

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

## Emergency Handoff Template (Complete)

Use this complete curl template for emergency handoffs. All fields are required:

```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "TARGET_AGENT",
    "subject": "[EMERGENCY HANDOFF] Agent Failure - Work Transfer",
    "priority": "urgent",
    "content": {
      "type": "emergency_handoff",
      "message": "Agent <NAME> has failed. Critical work handoff required.",
      "failed_agent": "<AGENT_NAME>",
      "failure_reason": "<REASON>",
      "failure_type": "<transient|recoverable|terminal>",
      "failure_time": "<ISO_TIMESTAMP>",
      "active_tasks": ["<TASK_1>", "<TASK_2>"],
      "critical_tasks": [
        {
          "task_id": "<TASK_ID>",
          "title": "<TASK_TITLE>",
          "deadline": "<ISO_TIMESTAMP>",
          "time_remaining": "<DURATION>",
          "status_percent": <0-100>,
          "branch": "<GIT_BRANCH>",
          "last_commit": "<COMMIT_HASH>"
        }
      ],
      "state_file": "<PATH_TO_STATE>",
      "handoff_document": "<PATH_TO_HANDOFF_DOC>",
      "priority_actions": ["<ACTION_1>", "<ACTION_2>"],
      "deadline_impact": "<IMPACT_DESCRIPTION>",
      "recovery_estimate": "<DURATION>",
      "acknowledgment_required": true,
      "acknowledge_by": "<ISO_TIMESTAMP>"
    }
  }'
```

**Example with filled values:**

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "apps-svgplayer-development",
    "subject": "[EMERGENCY HANDOFF] Agent Failure - Work Transfer",
    "priority": "urgent",
    "content": {
      "type": "emergency_handoff",
      "message": "Agent libs-svg-svgbbox has failed. Critical work handoff required.",
      "failed_agent": "libs-svg-svgbbox",
      "failure_reason": "Terminal crash - host system disk corruption detected",
      "failure_type": "terminal",
      "failure_time": "2025-02-04T10:00:00Z",
      "active_tasks": ["task-001", "task-002"],
      "critical_tasks": [
        {
          "task_id": "task-001",
          "title": "Implement bounding box calculation",
          "deadline": "2025-02-04T12:00:00Z",
          "time_remaining": "90 minutes",
          "status_percent": 60,
          "branch": "feature/bounding-box",
          "last_commit": "abc123def"
        }
      ],
      "state_file": "/path/to/project/.ecos/agent-health/libs-svg-svgbbox-state.json",
      "handoff_document": "thoughts/shared/handoffs/emergency/task-001-emergency-20250204.md",
      "priority_actions": [
        "1. Read handoff document immediately",
        "2. Checkout branch feature/bounding-box",
        "3. Continue from line 145 in src/bbox.py"
      ],
      "deadline_impact": "CRITICAL - Customer demo at 12:30, feature must be complete",
      "recovery_estimate": "60+ minutes (replacement agent creation)",
      "acknowledgment_required": true,
      "acknowledge_by": "2025-02-04T10:35:00Z"
    }
  }'
```

**Required fields reference:**

| Field | Type | Description |
|-------|------|-------------|
| `to` | string | Target agent session name |
| `subject` | string | Must start with `[EMERGENCY HANDOFF]` |
| `priority` | string | Must be `urgent` |
| `content.type` | string | Must be `emergency_handoff` |
| `content.failed_agent` | string | Name of the failed agent |
| `content.failure_reason` | string | Human-readable failure explanation |
| `content.failure_type` | string | One of: `transient`, `recoverable`, `terminal` |
| `content.failure_time` | string | ISO-8601 timestamp of failure detection |
| `content.active_tasks` | array | List of all task IDs assigned to failed agent |
| `content.critical_tasks` | array | Detailed objects for deadline-critical tasks |
| `content.state_file` | string | Path to preserved agent state (if available) |
| `content.handoff_document` | string | Path to emergency handoff markdown |
| `content.priority_actions` | array | Ordered list of immediate actions |
| `content.deadline_impact` | string | Business impact of missing deadline |
| `content.acknowledgment_required` | boolean | Must be `true` for emergency handoffs |
| `content.acknowledge_by` | string | ISO-8601 timestamp for ACK deadline |
