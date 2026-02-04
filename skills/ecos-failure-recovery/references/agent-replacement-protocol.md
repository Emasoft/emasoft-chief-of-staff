# Agent Replacement Protocol

## Table of Contents

- 4.1 When to use this document
- 4.2 Overview of the replacement protocol
- 4.3 Phase 1: Failure confirmation and artifact preservation
  - 4.3.1 Confirming agent cannot be recovered
  - 4.3.2 Identifying recoverable artifacts
  - 4.3.3 Preserving git commits and logs
- 4.4 Phase 2: Manager notification and approval
  - 4.4.1 Composing the replacement request
  - 4.4.2 Required information for approval
  - 4.4.3 Handling approval response
  - 4.4.4 Handling rejection response
- 4.5 Phase 3: Creating the replacement agent
  - 4.5.1 Selecting the host for the new agent
  - 4.5.2 Creating a new local folder
  - 4.5.3 Cloning the git repository
  - 4.5.4 Starting the new Claude Code session
  - 4.5.5 Registering with AI Maestro
- 4.6 Phase 4: Orchestrator notification
  - 4.6.1 Notifying orchestrator about replacement
  - 4.6.2 Requesting handoff document generation
  - 4.6.3 Requesting GitHub Project update
- 4.7 Phase 5: Work handoff to new agent
  - 4.7.1 Sending handoff documentation
  - 4.7.2 Sending task assignments
  - 4.7.3 Awaiting acknowledgment
  - 4.7.4 Verifying new agent understanding
- 4.8 Phase 6: Cleanup and closure
  - 4.8.1 Updating incident log
  - 4.8.2 Notifying manager of completion
  - 4.8.3 Archiving old agent records
- 4.9 Complete replacement workflow checklist

---

## 4.1 When to Use This Document

Use this document when:
- An agent has been classified as a **terminal failure** per `references/failure-classification.md`
- All recovery strategies have been exhausted per `references/recovery-strategies.md`
- Manager (EAMA) has approved agent replacement
- You need to create a new agent to take over the failed agent's work

**CRITICAL**: The replacement agent has NO MEMORY of the old agent. All context, in-progress work, and task understanding must be explicitly transferred through documentation.

---

## 4.2 Overview of the Replacement Protocol

The replacement protocol consists of six phases executed in sequence:

```
Phase 1: Failure Confirmation ──► Phase 2: Manager Approval ──► Phase 3: Create Agent
                                                                        │
                                                                        ▼
Phase 6: Cleanup ◄── Phase 5: Work Handoff ◄── Phase 4: Orchestrator Notification
```

| Phase | Owner | Duration | Key Output |
|-------|-------|----------|------------|
| 1. Failure Confirmation | ECOS | 5-10 min | Artifact inventory |
| 2. Manager Approval | EAMA | 5-30 min | Approval decision |
| 3. Create Agent | ECOS + User | 10-30 min | New agent online |
| 4. Orchestrator Notification | ECOS → EOA | 5-10 min | Handoff docs, kanban update |
| 5. Work Handoff | ECOS → New Agent | 10-20 min | Agent acknowledgment |
| 6. Cleanup | ECOS | 5 min | Incident closed |

**Total estimated time**: 40-110 minutes depending on complexity and response times.

---

## 4.3 Phase 1: Failure Confirmation and Artifact Preservation

### 4.3.1 Confirming Agent Cannot Be Recovered

Before proceeding with replacement, ECOS must document that recovery is impossible:

**Confirmation checklist:**

```markdown
## Recovery Exhaustion Confirmation

Agent: [AGENT_SESSION_NAME]
Failure detected: [ISO_TIMESTAMP]
Classification: TERMINAL

### Recovery Attempts

| Strategy | Attempted | Result | Notes |
|----------|-----------|--------|-------|
| Wait and Retry | Yes/No | Failed/N/A | [details] |
| Soft Restart | Yes/No | Failed/N/A | [details] |
| Hard Restart | Yes/No | Failed/N/A | [details] |
| Hibernate-Wake | Yes/No | Failed/N/A | [details] |
| Resource Adjustment | Yes/No | Failed/N/A | [details] |

### Terminal Failure Evidence

- [ ] Agent process confirmed dead
- [ ] Host unreachable OR working directory corrupted
- [ ] 3+ consecutive recovery failures
- [ ] State unrecoverable (context lost, credentials invalid, etc.)

Confirmed by: ECOS
Confirmation timestamp: [ISO_TIMESTAMP]
```

### 4.3.2 Identifying Recoverable Artifacts

Even when the agent cannot be recovered, some work products may be salvageable:

**Artifact categories:**

| Artifact Type | Location | Recovery Method |
|---------------|----------|-----------------|
| Git commits | Remote repository | Clone from origin |
| Local uncommitted changes | Agent's working directory | May be lost if disk corrupted |
| Log files | `/var/log/` or project `logs/` | Copy if host accessible |
| Conversation history | Claude session | Lost if session terminated |
| Task tracking files | `$CLAUDE_PROJECT_DIR/.ecos/` | Copy if accessible |
| Handoff documents | `thoughts/shared/handoffs/` | Likely preserved in git |

### 4.3.3 Preserving Git Commits and Logs

**Step 1: Check last known commit from the failed agent**

If ECOS has SSH access to the host:

```bash
# Attempt to get git status from failed agent's directory
ssh USER@HOST "cd /path/to/agent/project && git log -1 --oneline" 2>/dev/null
```

**Step 2: Document the last known state**

```bash
# Create artifact inventory
cat > $CLAUDE_PROJECT_DIR/.ecos/agent-health/artifacts-AGENT_NAME.md << 'EOF'
# Artifact Inventory for Failed Agent

Agent: AGENT_SESSION_NAME
Failure timestamp: ISO_TIMESTAMP
Host: HOSTNAME

## Git State
- Last known commit: abc123 "Commit message"
- Branch: feature/my-feature
- Remote: origin/feature/my-feature (pushed: yes/no)
- Uncommitted changes: unknown/none/description

## Logs Preserved
- /var/log/agent-AGENT_NAME.log - copied to /archive/
- $PROJECT/.ecos/task-tracking.json - copied to /archive/

## Lost Artifacts
- In-progress file edits (not committed)
- Current task context
- Conversation history

EOF
```

---

## 4.4 Phase 2: Manager Notification and Approval

### 4.4.1 Composing the Replacement Request

ECOS must request approval from the manager (EAMA) before creating a replacement agent:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eama-assistant-manager",
    "subject": "[APPROVAL REQUIRED] Agent replacement request",
    "priority": "urgent",
    "content": {
      "type": "replacement-approval-request",
      "message": "Agent libs-svg-svgbbox has experienced a terminal failure and requires replacement. All recovery attempts have failed. Requesting approval to proceed with replacement protocol.",
      "agent": "libs-svg-svgbbox",
      "failure_summary": {
        "failure_type": "terminal",
        "failure_cause": "host_machine_crash",
        "detected_at": "2025-01-15T10:00:00Z",
        "recovery_attempts": 3,
        "last_recovery_attempt": "2025-01-15T10:45:00Z"
      },
      "impact_assessment": {
        "tasks_affected": ["task-001", "task-002"],
        "estimated_work_lost": "2 hours of uncommitted changes",
        "downstream_dependencies": ["Integration depends on task-001 completion"]
      },
      "replacement_plan": {
        "new_agent_name": "libs-svg-svgbbox-v2",
        "target_host": "workstation-1",
        "estimated_time_to_operational": "30 minutes",
        "handoff_required_from": "eoa-orchestrator"
      },
      "artifacts_preserved": [
        "Git commits up to abc123",
        "Task tracking logs"
      ],
      "artifacts_lost": [
        "Uncommitted file changes",
        "Current session context"
      ],
      "awaiting_approval": true,
      "response_requested_by": "2025-01-15T11:30:00Z"
    }
  }'
```

### 4.4.2 Required Information for Approval

The manager needs the following to make an informed decision:

| Information | Why Needed |
|-------------|------------|
| Agent name and role | Context about what was being done |
| Failure cause | Understanding what went wrong |
| Recovery attempts | Confidence that replacement is necessary |
| Impact assessment | Understanding of consequences |
| Work lost | Planning for redo effort |
| Replacement plan | Feasibility check |
| Artifacts preserved | What can be recovered |

### 4.4.3 Handling Approval Response

When manager approves, the response will include any additional instructions:

```json
{
  "type": "replacement-approval",
  "decision": "approved",
  "message": "Replacement approved. Proceed with the plan.",
  "additional_instructions": [
    "Use the same session name (libs-svg-svgbbox) to maintain continuity",
    "Prioritize task-001 for the replacement agent"
  ],
  "approved_by": "eama-assistant-manager",
  "approved_at": "2025-01-15T11:00:00Z"
}
```

**Upon approval:**
1. Log the approval
2. Proceed to Phase 3

```bash
echo "{\"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"agent\": \"AGENT_NAME\", \"action\": \"replacement_approved\", \"approved_by\": \"eama-assistant-manager\"}" >> $CLAUDE_PROJECT_DIR/.ecos/agent-health/recovery-log.jsonl
```

### 4.4.4 Handling Rejection Response

The manager may reject the replacement request:

```json
{
  "type": "replacement-approval",
  "decision": "rejected",
  "message": "Replacement not approved at this time.",
  "reason": "The host machine is being repaired. Wait 2 hours and retry recovery.",
  "alternative_action": "wait_and_retry_in_2_hours",
  "rejected_by": "eama-assistant-manager",
  "rejected_at": "2025-01-15T11:00:00Z"
}
```

**Upon rejection:**
1. Log the rejection
2. Follow the alternative action specified
3. Reschedule replacement request if appropriate

---

## 4.5 Phase 3: Creating the Replacement Agent

### 4.5.1 Selecting the Host for the New Agent

The replacement agent should run on a stable host. Considerations:

| Factor | Recommendation |
|--------|----------------|
| Same host as failed agent | Only if failure was software, not hardware |
| Different host | Preferred if hardware failure suspected |
| Resource availability | Ensure sufficient CPU/memory/disk |
| Network connectivity | Must be able to reach AI Maestro and git remotes |

### 4.5.2 Creating a New Local Folder

The replacement agent needs a fresh working directory. **The new agent will NOT inherit the old agent's local files.**

**Request user to create the folder:**

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "USER_OR_ADMIN",
    "subject": "[USER ACTION REQUIRED] Create folder for replacement agent",
    "priority": "high",
    "content": {
      "type": "user-action-required",
      "message": "Please create a new working directory for the replacement agent.",
      "instructions": [
        "1. SSH to the target host: ssh USER@workstation-1",
        "2. Create new directory: mkdir -p ~/agents/libs-svg-svgbbox-v2",
        "3. Navigate to it: cd ~/agents/libs-svg-svgbbox-v2",
        "4. Confirm the directory is empty and writable"
      ],
      "expected_result": "Empty directory at ~/agents/libs-svg-svgbbox-v2",
      "notify_when_complete": true
    }
  }'
```

### 4.5.3 Cloning the Git Repository

The new agent must clone the project repository to access code and history:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "USER_OR_ADMIN",
    "subject": "[USER ACTION REQUIRED] Clone repository for replacement agent",
    "priority": "high",
    "content": {
      "type": "user-action-required",
      "message": "Please clone the project repository into the new agent folder.",
      "instructions": [
        "1. Navigate to the agent directory: cd ~/agents/libs-svg-svgbbox-v2",
        "2. Clone the repository: git clone https://github.com/ORG/REPO.git .",
        "3. Checkout the appropriate branch: git checkout feature/my-feature",
        "4. Verify clone: git log -3 --oneline"
      ],
      "repository": "https://github.com/ORG/REPO.git",
      "branch": "feature/my-feature",
      "expected_result": "Repository cloned with full history"
    }
  }'
```

### 4.5.4 Starting the New Claude Code Session

Launch a new Claude Code session for the replacement agent:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "USER_OR_ADMIN",
    "subject": "[USER ACTION REQUIRED] Start Claude Code session for replacement agent",
    "priority": "high",
    "content": {
      "type": "user-action-required",
      "message": "Please start a new Claude Code session for the replacement agent.",
      "instructions": [
        "1. Open a new terminal (or tmux session): tmux new -s libs-svg-svgbbox",
        "2. Navigate to the agent directory: cd ~/agents/libs-svg-svgbbox-v2",
        "3. Start Claude Code: claude",
        "4. The new agent should register with AI Maestro automatically",
        "5. Verify registration by checking: curl http://localhost:23000/api/agents/libs-svg-svgbbox/status"
      ],
      "session_name": "libs-svg-svgbbox",
      "working_directory": "~/agents/libs-svg-svgbbox-v2"
    }
  }'
```

### 4.5.5 Registering with AI Maestro

The new agent should automatically register when it starts (via AI Maestro hooks). Verify registration:

```bash
# Check agent registration
RESPONSE=$(curl -s "http://localhost:23000/api/agents/libs-svg-svgbbox/status")

# Verify status is "online"
echo "$RESPONSE" | jq -e '.status == "online"' && echo "Agent registered successfully"
```

If registration fails, troubleshoot:
1. Check agent has AI Maestro hooks enabled
2. Check AI Maestro server is running
3. Check agent's session name matches expected

---

## 4.6 Phase 4: Orchestrator Notification

### 4.6.1 Notifying Orchestrator About Replacement

ECOS must notify the orchestrator (EOA) that an agent has been replaced so that:
1. The orchestrator can generate a handoff document for the new agent
2. The GitHub Project kanban can be updated to reassign tasks

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eoa-orchestrator",
    "subject": "[AGENT REPLACED] Handoff required for new agent",
    "priority": "high",
    "content": {
      "type": "agent-replacement-notification",
      "message": "Agent libs-svg-svgbbox has been replaced due to terminal failure. The new agent is online but has no memory of previous work. Please generate handoff documentation and update task assignments.",
      "old_agent": {
        "name": "libs-svg-svgbbox",
        "status": "terminated",
        "last_commit": "abc123",
        "tasks_in_progress": ["task-001", "task-002"]
      },
      "new_agent": {
        "name": "libs-svg-svgbbox",
        "status": "online",
        "working_directory": "~/agents/libs-svg-svgbbox-v2",
        "git_branch": "feature/my-feature"
      },
      "actions_required": [
        "generate_handoff_document",
        "update_github_project_kanban"
      ]
    }
  }'
```

### 4.6.2 Requesting Handoff Document Generation

The orchestrator (EOA) is responsible for generating a comprehensive handoff document that includes:

| Section | Content |
|---------|---------|
| Project Overview | What the project is about |
| Current Sprint Goals | What needs to be achieved |
| Assigned Tasks | Tasks assigned to this agent |
| Task Details | Requirements, acceptance criteria, dependencies |
| Codebase Context | Key files, architecture, conventions |
| In-Progress Work | What the old agent was working on |
| Known Issues | Blockers, bugs, concerns |
| Communication Channels | How to report progress, ask questions |

The orchestrator will create this document at:
```
$CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/AGENT_NAME/handoff-TIMESTAMP.md
```

### 4.6.3 Requesting GitHub Project Update

The orchestrator must update the GitHub Project kanban to:

1. **Reassign tasks** from old agent to new agent
2. **Update task status** if any were marked "in progress" by old agent
3. **Add note** about agent replacement to affected tasks

```bash
# EOA will execute commands like:
gh project item-edit --id ITEM_ID --field-id ASSIGNEE_FIELD --value NEW_AGENT_NAME
```

---

## 4.7 Phase 5: Work Handoff to New Agent

### 4.7.1 Sending Handoff Documentation

Once EOA has generated the handoff document, ECOS sends it to the new agent:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "libs-svg-svgbbox",
    "subject": "[ONBOARDING] Welcome - please read handoff documentation",
    "priority": "urgent",
    "content": {
      "type": "agent-onboarding",
      "message": "Welcome! You are a replacement agent taking over from a previous instance that experienced a terminal failure. You have NO MEMORY of previous work. Please read the handoff documentation immediately to understand your tasks and context.",
      "handoff_document": "thoughts/shared/handoffs/libs-svg-svgbbox/handoff-20250115T110000Z.md",
      "instructions": [
        "1. Read the handoff document completely before doing anything else",
        "2. Review the git history to understand recent changes: git log -10 --oneline",
        "3. Check your assigned tasks in the GitHub Project",
        "4. Reply to this message acknowledging you understand your assignments",
        "5. Ask any clarifying questions before starting work"
      ],
      "git_branch": "feature/my-feature",
      "last_known_commit": "abc123",
      "github_project_url": "https://github.com/orgs/ORG/projects/PROJECT_NUMBER"
    }
  }'
```

### 4.7.2 Sending Task Assignments

After the handoff document, send specific task assignments:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "libs-svg-svgbbox",
    "subject": "[TASK ASSIGNMENTS] Your assigned tasks",
    "priority": "high",
    "content": {
      "type": "task-assignment",
      "message": "These are your assigned tasks. They were previously assigned to your predecessor. Please review and begin work after reading the handoff documentation.",
      "tasks": [
        {
          "task_id": "task-001",
          "title": "Implement bounding box calculation",
          "priority": "high",
          "status": "in_progress",
          "github_issue": "https://github.com/ORG/REPO/issues/123",
          "notes": "Predecessor was ~60% complete. Check recent commits for progress."
        },
        {
          "task_id": "task-002",
          "title": "Add unit tests for SVG parsing",
          "priority": "normal",
          "status": "not_started",
          "github_issue": "https://github.com/ORG/REPO/issues/124",
          "notes": "Not yet started by predecessor."
        }
      ]
    }
  }'
```

### 4.7.3 Awaiting Acknowledgment

The new agent MUST acknowledge the handoff before ECOS considers the replacement complete:

**Expected acknowledgment:**

```json
{
  "type": "handoff-acknowledgment",
  "message": "I have read the handoff documentation and understand my assignments.",
  "handoff_document_read": true,
  "tasks_understood": ["task-001", "task-002"],
  "questions": [],
  "ready_to_begin": true
}
```

**If no acknowledgment within 15 minutes:**

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "libs-svg-svgbbox",
    "subject": "[REMINDER] Handoff acknowledgment required",
    "priority": "urgent",
    "content": {
      "type": "acknowledgment-reminder",
      "message": "Please acknowledge receipt of the handoff documentation. Reply with your understanding of your assignments and any questions.",
      "original_message_timestamp": "2025-01-15T11:00:00Z",
      "response_required_by": "2025-01-15T11:30:00Z"
    }
  }'
```

### 4.7.4 Verifying New Agent Understanding

After acknowledgment, verify the agent correctly understands the tasks:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "libs-svg-svgbbox",
    "subject": "[VERIFICATION] Confirm task understanding",
    "priority": "normal",
    "content": {
      "type": "understanding-verification",
      "message": "Before you begin, please summarize task-001 in your own words, including the acceptance criteria and your planned approach.",
      "task_to_summarize": "task-001",
      "response_format": {
        "task_summary": "Your understanding of what needs to be done",
        "acceptance_criteria": "Your understanding of when it is complete",
        "planned_approach": "How you intend to accomplish it",
        "estimated_time": "Your estimate for completion"
      }
    }
  }'
```

---

## 4.8 Phase 6: Cleanup and Closure

### 4.8.1 Updating Incident Log

Record the complete incident with resolution:

```bash
# Update the incident record with resolution
jq --arg agent "libs-svg-svgbbox" --arg resolution "replaced" '
  .incidents[] |
  select(.agent == $agent and .resolution == null) |
  .resolution = $resolution |
  .resolved_at = (now | strftime("%Y-%m-%dT%H:%M:%SZ")) |
  .replacement_agent = "libs-svg-svgbbox (new instance)" |
  .total_downtime = "75 minutes"
' $CLAUDE_PROJECT_DIR/.ecos/agent-health/incident-log.jsonl > temp.jsonl && mv temp.jsonl $CLAUDE_PROJECT_DIR/.ecos/agent-health/incident-log.jsonl
```

### 4.8.2 Notifying Manager of Completion

Inform the manager that replacement is complete:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eama-assistant-manager",
    "subject": "[RESOLVED] Agent replacement complete",
    "priority": "normal",
    "content": {
      "type": "replacement-complete",
      "message": "Agent libs-svg-svgbbox has been successfully replaced. The new agent has acknowledged the handoff and is ready to begin work.",
      "incident_summary": {
        "original_failure": "host_machine_crash",
        "detected_at": "2025-01-15T10:00:00Z",
        "replacement_approved_at": "2025-01-15T11:00:00Z",
        "new_agent_online_at": "2025-01-15T11:15:00Z",
        "handoff_acknowledged_at": "2025-01-15T11:25:00Z",
        "total_downtime": "75 minutes"
      },
      "new_agent_status": "operational",
      "work_lost": "2 hours of uncommitted changes",
      "work_recovered": "All committed code via git clone",
      "incident_id": "inc-20250115-001"
    }
  }'
```

### 4.8.3 Archiving Old Agent Records

Move old agent's records to archive:

```bash
# Archive old agent configuration
mv $CLAUDE_PROJECT_DIR/.ecos/agent-health/heartbeat-config.json.backup-AGENT_NAME \
   $CLAUDE_PROJECT_DIR/.ecos/archive/agents/

# Keep incident log intact (do not archive)
```

---

## 4.9 Complete Replacement Workflow Checklist

Use this checklist to track progress through the replacement protocol:

```markdown
## Agent Replacement Checklist

Agent: _______________
Replacement started: _______________

### Phase 1: Failure Confirmation
- [ ] All recovery strategies exhausted
- [ ] Terminal failure confirmed
- [ ] Artifact inventory created
- [ ] Git commits documented
- [ ] Logs preserved (if accessible)

### Phase 2: Manager Approval
- [ ] Replacement request sent to EAMA
- [ ] Impact assessment included
- [ ] Replacement plan included
- [ ] Approval received
- [ ] Approval logged

### Phase 3: Create Agent
- [ ] Host selected
- [ ] Local folder created
- [ ] Git repository cloned
- [ ] Branch checked out
- [ ] Claude Code session started
- [ ] AI Maestro registration verified

### Phase 4: Orchestrator Notification
- [ ] Replacement notification sent to EOA
- [ ] Handoff document request sent
- [ ] GitHub Project update requested
- [ ] Handoff document received
- [ ] Kanban updated confirmed

### Phase 5: Work Handoff
- [ ] Handoff documentation sent to new agent
- [ ] Task assignments sent
- [ ] Acknowledgment received
- [ ] Understanding verified

### Phase 6: Cleanup
- [ ] Incident log updated with resolution
- [ ] Manager notified of completion
- [ ] Old agent records archived

Replacement completed: _______________
Total time: _______________
```

---

## Troubleshooting

### New agent does not register with AI Maestro

**Symptom**: Agent status check returns "not_found" after starting Claude Code.

**Cause**: AI Maestro hooks not configured in the new agent's environment.

**Solution**:
1. Check that `~/.claude/settings.json` includes AI Maestro hooks
2. Verify AI Maestro server is running
3. Restart Claude Code session

### Orchestrator does not respond to handoff request

**Symptom**: EOA does not generate handoff document within expected time.

**Cause**: EOA may be busy or also experiencing issues.

**Solution**:
1. Send a reminder message to EOA
2. If no response, escalate to manager (EAMA)
3. As fallback, ECOS can generate a basic handoff from known information

### New agent does not understand handoff documentation

**Symptom**: New agent's acknowledgment shows misunderstanding of tasks.

**Cause**: Handoff documentation incomplete or unclear.

**Solution**:
1. Request EOA to provide additional context
2. Schedule a synchronous Q&A session between ECOS and new agent
3. Have EOA or manager directly explain the tasks

### Git clone fails due to authentication

**Symptom**: User reports git clone fails with authentication error.

**Cause**: New environment does not have git credentials configured.

**Solution**:
1. Request user to configure git credentials: `gh auth login`
2. Or use SSH clone with existing keys: `git clone git@github.com:ORG/REPO.git`
3. Or provide a personal access token for HTTPS clone
