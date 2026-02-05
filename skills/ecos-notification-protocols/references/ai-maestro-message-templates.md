# AI Maestro Message Templates for ECOS

Reference for all AI Maestro curl command templates used by Emasoft Chief of Staff (ECOS).

## Contents

- [1. Standard AI Maestro API Format](#1-standard-ai-maestro-api-format)
- [2. When Requesting Approval from EAMA](#2-when-requesting-approval-from-eama)
- [3. When Escalating Issues to EAMA](#3-when-escalating-issues-to-eama)
- [4. When Notifying Agents of Upcoming Operations](#4-when-notifying-agents-of-upcoming-operations)
- [5. When Reporting Operation Results](#5-when-reporting-operation-results)
- [6. When Notifying EOA of New Agent Availability](#6-when-notifying-eoa-of-new-agent-availability)
- [7. When Requesting Team Status from EOA](#7-when-requesting-team-status-from-eoa)
- [8. When Broadcasting Team Updates](#8-when-broadcasting-team-updates)
- [9. Message Type Reference](#9-message-type-reference)

---

## 1. Standard AI Maestro API Format

**Base URL:** `http://localhost:23000/api/messages`

**Method:** `POST`

**Headers:**
```
Content-Type: application/json
```

**Body structure:**
```json
{
  "from": "<sender_session_name>",
  "to": "<recipient_session_name>",
  "subject": "<subject_line>",
  "priority": "<urgent|high|normal|low>",
  "content": {
    "type": "<message_type>",
    "message": "<message_body>",
    // ... additional fields based on message type
  }
}
```

**Generic template:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "<sender>",
    "to": "<recipient>",
    "subject": "<subject>",
    "priority": "normal",
    "content": {
      "type": "<type>",
      "message": "<message>"
    }
  }'
```

---

## 2. When Requesting Approval from EAMA

**Use case:** Before spawning, terminating, or replacing agents. ECOS requires approval for resource allocation and destructive operations.

**When to use:**
- Before spawning new agents (unless autonomous mode is ON and within limits)
- Before terminating agents (destructive operation)
- Before replacing failed agents (involves terminate + spawn)
- Before installing plugins on agents (changes agent capabilities)

**Template:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'${SESSION_NAME}'",
    "to": "eama-main",
    "subject": "APPROVAL REQUIRED: <operation_type>",
    "priority": "normal",
    "content": {
      "type": "approval_request",
      "message": "Request to <operation_description>.\n\nRequester: '${SESSION_NAME}'\nTarget: <target_agent_or_resource>\nJustification: <why_needed>\nRisk: <low|medium|high>\nRollback: <rollback_plan>",
      "request_id": "<request_id>",
      "timeout_seconds": 120
    }
  }'
```

**Example - Agent Spawn:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eama-main",
    "subject": "APPROVAL REQUIRED: agent_spawn",
    "priority": "normal",
    "content": {
      "type": "approval_request",
      "message": "Request to spawn agent worker-dev-auth-001 for auth module development.\n\nRequester: ecos-chief-of-staff\nTarget: worker-dev-auth-001\nJustification: Team needs additional developer for auth module\nRisk: low\nRollback: Terminate agent, remove from registry",
      "request_id": "AR-1706795200-f3a2b1",
      "timeout_seconds": 120
    }
  }'
```

**Expected response fields:**
- `decision`: `approved` | `rejected` | `revision_needed`
- `reason`: Explanation of decision
- `conditions`: Any conditions attached to approval (optional)

---

## 3. When Escalating Issues to EAMA

**Use case:** When issues occur outside ECOS authority or require human intervention.

**When to escalate:**
- Agent spawn failure after 3 attempts
- Resource exhaustion (memory/disk/CPU)
- Approval timeout for critical operations
- GitHub API failure (persistent)
- Plugin installation failure
- Agent communication failure
- Cross-project dependency conflict

**Template:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eama-assistant-manager",
    "subject": "[ESCALATION] <SITUATION_TYPE>",
    "priority": "<PRIORITY>",
    "content": {
      "type": "escalation",
      "message": "<DESCRIPTION_OF_ISSUE>",
      "situation": "<SITUATION_TYPE>",
      "severity": "<low|medium|high|critical>",
      "affected_resources": ["<RESOURCE_1>", "<RESOURCE_2>"],
      "attempts_made": <NUMBER>,
      "last_error": "<ERROR_DETAILS>",
      "recommended_action": "<WHAT_ECOS_RECOMMENDS>",
      "requires_user_decision": true,
      "escalation_id": "ESC-<TIMESTAMP>-<RANDOM>"
    }
  }'
```

**Example - Agent Spawn Failure:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eama-assistant-manager",
    "subject": "[ESCALATION] Agent Spawn Failure",
    "priority": "urgent",
    "content": {
      "type": "escalation",
      "message": "Failed to spawn agent worker-dev-auth-001 after 3 attempts. Persistent error: Directory already exists despite cleanup attempts.",
      "situation": "agent_spawn_failure",
      "severity": "high",
      "affected_resources": ["worker-dev-auth-001", "svgbbox-library-team"],
      "attempts_made": 3,
      "last_error": "Directory /path/to/project already exists",
      "recommended_action": "Manual cleanup of directory or use --force-folder flag",
      "requires_user_decision": true,
      "escalation_id": "ESC-1706795400-abc123"
    }
  }'
```

**Escalation Priority Guidelines:**
| Situation | Priority | Timeout |
|-----------|----------|---------|
| Agent spawn failure (3 attempts) | `urgent` | 5 min |
| Resource exhaustion | `urgent` | 5 min |
| Approval timeout (critical) | `urgent` | 2 min |
| Agent conflict | `high` | 10 min |
| GitHub API failure | `high` | 15 min |
| Plugin failure | `normal` | 30 min |

---

## 4. When Notifying Agents of Upcoming Operations

**Use case:** Before hibernating, terminating, or moving an agent. Give the agent time to save state.

**When to use:**
- Before hibernating agent (30s notice)
- Before terminating agent (30s notice)
- Before moving agent to different project (60s notice)

**Template:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'${SESSION_NAME}'",
    "to": "<target_agent>",
    "subject": "NOTICE: <operation_type> in <seconds>s",
    "priority": "high",
    "content": {
      "type": "operation_notice",
      "message": "You will be <operation> in <seconds> seconds. <instructions>",
      "operation": "<operation_type>",
      "countdown_seconds": <seconds>
    }
  }'
```

**Example - Hibernation Notice:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "worker-dev-003",
    "subject": "NOTICE: Hibernation in 30s",
    "priority": "high",
    "content": {
      "type": "operation_notice",
      "message": "You will be hibernated in 30 seconds due to inactivity. Save your current state and prepare for hibernation. You will be woken when needed.",
      "operation": "hibernate",
      "countdown_seconds": 30
    }
  }'
```

**Example - Termination Notice:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "worker-deploy-002",
    "subject": "NOTICE: Termination in 30s",
    "priority": "high",
    "content": {
      "type": "operation_notice",
      "message": "You will be terminated in 30 seconds. Project deployment complete. Save any final state and prepare for shutdown.",
      "operation": "terminate",
      "countdown_seconds": 30
    }
  }'
```

**Standard countdown times:**
- Hibernation: 30 seconds
- Termination: 30 seconds
- Project move: 60 seconds

---

## 5. When Reporting Operation Results

**Use case:** After completing spawn, terminate, hibernate, wake operations. Report back to requester.

**When to use:**
- After successful agent spawn
- After failed agent spawn (with rollback details)
- After agent termination (success or failure)
- After hibernation or wake operations
- After any operation requested by another agent

**Template:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'${SESSION_NAME}'",
    "to": "<requester_agent>",
    "subject": "RESULT: <operation_type> - <SUCCESS|FAILED>",
    "priority": "normal",
    "content": {
      "type": "operation_result",
      "message": "Operation <operation_type> <succeeded|failed>.\n\nTarget: <target>\nResult: <result_details>\nDuration: <duration_ms>ms",
      "operation": "<operation_type>",
      "status": "success|failure",
      "target": "<target_resource>",
      "duration_ms": <duration>
    }
  }'
```

**Example - Spawn Success:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "ecos-lifecycle-manager",
    "subject": "RESULT: agent_spawn - SUCCESS",
    "priority": "normal",
    "content": {
      "type": "operation_result",
      "message": "Operation agent_spawn succeeded.\n\nTarget: worker-dev-auth-001\nResult: Agent spawned, registered, and responding\nDuration: 6000ms",
      "operation": "agent_spawn",
      "status": "success",
      "target": "worker-dev-auth-001",
      "duration_ms": 6000
    }
  }'
```

**Example - Spawn Failure:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "ecos-lifecycle-manager",
    "subject": "RESULT: agent_spawn - FAILED",
    "priority": "high",
    "content": {
      "type": "operation_result",
      "message": "Operation agent_spawn failed.\n\nTarget: worker-dev-auth-001\nError: Directory already exists\nRollback: Completed successfully\nRecommendation: Use --force-folder flag or choose different directory",
      "operation": "agent_spawn",
      "status": "failure",
      "target": "worker-dev-auth-001",
      "error": "Directory already exists"
    }
  }'
```

**Status values:**
- `success`: Operation completed successfully
- `failure`: Operation failed (include `error` field)
- `partial`: Operation partially completed (include details)

---

## 6. When Notifying EOA of New Agent Availability

**Use case:** After spawning agent and adding to team. Inform the orchestrator that a new team member is ready.

**When to use:**
- After successfully spawning new agent
- After adding agent to team registry
- After verifying agent responds to health check

**Template:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'${SESSION_NAME}'",
    "to": "<eoa_agent_name>",
    "subject": "NEW AGENT: <agent_name> available",
    "priority": "normal",
    "content": {
      "type": "team_update",
      "message": "New agent <agent_name> added to your team.\n\nRole: <role>\nCapabilities: <capabilities_list>\nWorking directory: <path>\n\nAgent is ready to receive task assignments.",
      "agent_name": "<agent_name>",
      "role": "<role>",
      "team_registry": "<registry_path>"
    }
  }'
```

**Example - New Developer Agent:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "svgbbox-orchestrator",
    "subject": "NEW AGENT: worker-test-001 available",
    "priority": "normal",
    "content": {
      "type": "team_update",
      "message": "New agent worker-test-001 added to your team.\n\nRole: test-engineer\nCapabilities: Unit testing, integration testing, test reporting\nWorking directory: /path/to/svgbbox\n\nAgent is ready to receive task assignments.",
      "agent_name": "worker-test-001",
      "role": "test-engineer",
      "team_registry": "/path/to/svgbbox/.emasoft/team-registry.json"
    }
  }'
```

**Standard roles:**
- `developer`: Code implementation
- `test-engineer`: Testing and quality assurance
- `deploy-agent`: Deployment and release
- `debug-specialist`: Debugging and investigation
- `code-reviewer`: Code review and quality gates

---

## 7. When Requesting Team Status from EOA

**Use case:** Checking current status of all team members. Used for monitoring and resource planning.

**When to use:**
- Before deciding to spawn new agent (check if existing agents available)
- During periodic health checks
- When user requests team status report
- Before hibernating idle agents

**Template:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'${SESSION_NAME}'",
    "to": "<eoa_agent_name>",
    "subject": "REQUEST: Team status report",
    "priority": "normal",
    "content": {
      "type": "status_request",
      "message": "Please provide current status of all team members:\n- Active agents\n- Hibernated agents\n- In-progress tasks\n- Idle agents",
      "request_id": "<request_id>"
    }
  }'
```

**Example:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "svgbbox-orchestrator",
    "subject": "REQUEST: Team status report",
    "priority": "normal",
    "content": {
      "type": "status_request",
      "message": "Please provide current status of all team members:\n- Active agents\n- Hibernated agents\n- In-progress tasks\n- Idle agents",
      "request_id": "SR-1706795400-xyz123"
    }
  }'
```

**Expected response format:**
```json
{
  "type": "status_response",
  "request_id": "SR-1706795400-xyz123",
  "active_agents": ["agent1", "agent2"],
  "hibernated_agents": ["agent3"],
  "in_progress_tasks": [
    {"agent": "agent1", "task": "description"}
  ],
  "idle_agents": ["agent2"]
}
```

---

## 8. When Broadcasting Team Updates

**Use case:** Informing all team members of registry changes. Used when team composition changes.

**When to use:**
- After adding new agent to team
- After removing agent from team
- After updating agent roles
- After team registry structure changes

**Template:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'${SESSION_NAME}'",
    "to": "<agent1>,<agent2>,<agent3>",
    "subject": "TEAM UPDATE: <update_description>",
    "priority": "normal",
    "content": {
      "type": "team_broadcast",
      "message": "<update_details>",
      "team_registry": "<registry_path>",
      "action": "refresh_registry"
    }
  }'
```

**Example - New Member Added:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "svgbbox-orchestrator,worker-dev-001,worker-test-001",
    "subject": "TEAM UPDATE: New member added",
    "priority": "normal",
    "content": {
      "type": "team_broadcast",
      "message": "Team registry updated: worker-dev-002 added with role developer.\n\nPlease refresh your team registry from:\n/path/to/svgbbox/.emasoft/team-registry.json",
      "team_registry": "/path/to/svgbbox/.emasoft/team-registry.json",
      "action": "refresh_registry"
    }
  }'
```

**Broadcast actions:**
- `refresh_registry`: Re-read team registry file
- `update_roles`: Role assignments changed
- `member_removed`: Agent removed from team
- `member_added`: New agent added to team

---

## 9. Message Type Reference

**Quick reference for all message types used by ECOS:**

| Message Type | Purpose | Priority | Response Expected |
|--------------|---------|----------|-------------------|
| `approval_request` | Request permission from EAMA | `normal` | Yes (timeout: 120s) |
| `escalation` | Report critical issue to EAMA | `urgent`/`high` | Yes (varies) |
| `operation_notice` | Warn agent of upcoming operation | `high` | No |
| `operation_result` | Report operation outcome | `normal`/`high` | No |
| `team_update` | Notify EOA of new agent | `normal` | No |
| `status_request` | Request team status from EOA | `normal` | Yes (timeout: 60s) |
| `team_broadcast` | Notify all team members | `normal` | No |
| `health_check` | Verify agent is responsive | `normal` | Yes (timeout: 30s) |

**Message priority guidelines:**
- `urgent`: Immediate attention required (< 5 min response)
- `high`: Important, handle soon (< 15 min response)
- `normal`: Standard priority (< 60 min response)
- `low`: Non-critical, handle when convenient

**Timeout recommendations:**
- Approval requests: 120 seconds
- Status requests: 60 seconds
- Health checks: 30 seconds
- Escalations: Varies by severity (2-30 minutes)

---

## Notes

- **Always use full session names** (e.g., `ecos-chief-of-staff`, not `ecos`)
- **Always generate unique request IDs** for operations requiring tracking
- **Always specify rollback plan** in approval requests
- **Always include duration** in operation results (helps performance tracking)
- **Always use `type` field** in content object for message routing
- **Multiple recipients**: Use comma-separated list in `to` field (e.g., `"to": "agent1,agent2,agent3"`)
