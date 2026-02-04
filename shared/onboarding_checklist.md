# Agent Onboarding Checklist

This document defines the standard onboarding process for agents spawned by the Chief of Staff.

## Pre-Start Checklist

Before spawning a new agent, verify the following conditions are met:

### Resource Availability

- [ ] CPU usage below threshold (80%)
- [ ] Memory usage below threshold (85%)
- [ ] Disk usage below threshold (90%)
- [ ] Current agent count below MAX_CONCURRENT_AGENTS (10)
- [ ] Project agent count below MAX_AGENTS_PER_PROJECT (5)

### Role Availability

- [ ] Target role is valid (architect, orchestrator, or integrator)
- [ ] No conflicting agent already active for same task
- [ ] Required session name is available

### Context Preparation

- [ ] Handoff document created with UUID
- [ ] GitHub issue linked (if applicable)
- [ ] Clear task description prepared
- [ ] Acceptance criteria defined
- [ ] Dependencies identified

## Configuration Steps

Execute these steps in order when spawning an agent:

### Step 1: Generate Session Identity

```bash
# Generate unique session identifier
SESSION_UUID=$(uuidgen | tr '[:upper:]' '[:lower:]' | cut -d'-' -f1)
SESSION_NAME="${ROLE_PREFIX}${PROJECT_NAME}-${SESSION_UUID}"
```

### Step 2: Create Handoff Document

```bash
# Create handoff in standard location
HANDOFF_PATH="docs_dev/handoffs/handoff-${SESSION_UUID}-ecos-to-${ROLE}.md"
```

### Step 3: Register Agent in Tracking

```bash
# Register agent with AI Maestro (if available)
curl -X POST "http://localhost:23000/api/agents" \
  -H "Content-Type: application/json" \
  -d '{
    "session_name": "'${SESSION_NAME}'",
    "role": "'${ROLE}'",
    "project": "'${PROJECT_NAME}'",
    "status": "starting",
    "handoff": "'${HANDOFF_PATH}'"
  }'
```

### Step 4: Spawn Agent Process

```bash
# Spawn the agent with appropriate configuration
claude --session "${SESSION_NAME}" \
       --project "${PROJECT_DIR}" \
       --plugin-dir "${PLUGIN_PATH}"
```

## Briefing Content

Every spawned agent receives the following briefing message:

### Mandatory Briefing Elements

1. **Identity Confirmation**
   - Session name
   - Assigned role
   - Parent coordinator (Chief of Staff session)

2. **Task Assignment**
   - Clear task description
   - Link to handoff document
   - Link to GitHub issue (if applicable)

3. **Communication Protocol**
   - How to send status updates
   - How to request approvals
   - How to report blockers
   - How to signal completion

4. **Constraints**
   - Maximum execution time
   - Resource limits
   - Scope boundaries
   - Approval requirements

5. **Success Criteria**
   - Specific deliverables expected
   - Acceptance criteria checklist
   - Verification steps

### Briefing Message Template

```json
{
  "to": "{agent-session-name}",
  "subject": "[ONBOARDING] Welcome - {role} for {project}",
  "priority": "high",
  "content": {
    "type": "onboarding",
    "message": "You have been assigned as {role} for {project}. Your task: {task_description}",
    "session_name": "{agent-session-name}",
    "coordinator": "{ecos-session-name}",
    "handoff_document": "{handoff_path}",
    "github_issue": "#{issue_number}",
    "constraints": {
      "max_duration_minutes": 60,
      "requires_approval_for": ["push", "merge", "publish"],
      "scope": "{scope_description}"
    },
    "success_criteria": [
      "{criterion_1}",
      "{criterion_2}",
      "{criterion_3}"
    ],
    "ack_required": true
  }
}
```

## Post-Start Verification

After spawning an agent, verify successful onboarding:

### Immediate Verification (within 60 seconds)

- [ ] Agent process is running
- [ ] Agent acknowledged onboarding message
- [ ] Agent loaded correct handoff document
- [ ] Heartbeat received from agent

### Ongoing Monitoring

- [ ] Regular heartbeat checks (every 300 seconds)
- [ ] Status update requests honored
- [ ] Agent stays within scope boundaries
- [ ] Resource usage remains within limits

## Onboarding Failure Handling

If onboarding fails at any step:

### Step 1: Record Failure

```json
{
  "event": "onboarding_failure",
  "agent": "{session_name}",
  "step": "{failed_step}",
  "error": "{error_message}",
  "timestamp": "{ISO-8601}"
}
```

### Step 2: Cleanup

- Remove agent from tracking registry
- Delete incomplete handoff document
- Release reserved resources

### Step 3: Report to User

- Notify user of spawn failure
- Provide error details
- Suggest remediation steps

### Step 4: Retry Decision

- If retriable error: attempt up to 3 times
- If persistent failure: escalate to user
- If resource exhaustion: queue for later

## Onboarding Timeout Handling

If agent does not acknowledge within ONBOARDING_TIMEOUT_SECONDS (60):

1. Send warning message to agent
2. Wait additional 30 seconds
3. If still no response:
   - Mark agent as unresponsive
   - Terminate agent process
   - Report failure to user
   - Clean up resources
