# AI Maestro Message Templates for ECOS

Reference for all inter-agent message templates used by Emasoft Chief of Staff (ECOS).

## Contents

- [1. Standard Message Format](#1-standard-message-format)
- [2. When Requesting Approval from EAMA](#2-when-requesting-approval-from-eama)
- [3. When Escalating Issues to EAMA](#3-when-escalating-issues-to-eama)
- [4. When Notifying Agents of Upcoming Operations](#4-when-notifying-agents-of-upcoming-operations)
- [5. When Reporting Operation Results](#5-when-reporting-operation-results)
- [6. When Notifying EOA of New Agent Availability](#6-when-notifying-eoa-of-new-agent-availability)
- [7. When Requesting Team Status from EOA](#7-when-requesting-team-status-from-eoa)
- [8. When Broadcasting Team Updates](#8-when-broadcasting-team-updates)
- [9. Message Type Reference](#9-message-type-reference)

---

## 1. Standard Message Format

All messages are sent using the `agent-messaging` skill. Each message includes:

- **Recipient**: the target agent session name
- **Subject**: descriptive subject line
- **Priority**: `urgent`, `high`, `normal`, or `low`
- **Content**: structured object with `type` and `message` fields, plus additional fields as needed

---

## 2. When Requesting Approval from EAMA

**Use case:** Before spawning, terminating, or replacing agents. ECOS requires approval for resource allocation and destructive operations.

**When to use:**
- Before spawning new agents (unless autonomous mode is ON and within limits)
- Before terminating agents (destructive operation)
- Before replacing failed agents (involves terminate + spawn)
- Before installing plugins on agents (changes agent capabilities)

Use the `agent-messaging` skill to send a message:
- **Recipient**: `eama-main`
- **Subject**: `APPROVAL REQUIRED: <operation_type>`
- **Priority**: `normal`
- **Content**: type `approval_request`, including:
  - Description of the requested operation
  - Requester session name
  - Target agent or resource
  - Justification for the operation
  - Risk level (low, medium, high)
  - Rollback plan
  - Unique request ID
  - Timeout in seconds (default 120)

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

Use the `agent-messaging` skill to send a message:
- **Recipient**: `eama-assistant-manager`
- **Subject**: `[ESCALATION] <SITUATION_TYPE>`
- **Priority**: based on severity (see table below)
- **Content**: type `escalation`, including:
  - Description of the issue
  - Situation type
  - Severity (low, medium, high, critical)
  - Affected resources list
  - Number of attempts made
  - Last error details
  - Recommended action
  - Whether user decision is required
  - Unique escalation ID

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

Use the `agent-messaging` skill to send a message:
- **Recipient**: the target agent session name
- **Subject**: `NOTICE: <operation_type> in <seconds>s`
- **Priority**: `high`
- **Content**: type `operation_notice`, including:
  - Description of the upcoming operation
  - Operation type (hibernate, terminate, move)
  - Countdown in seconds

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

Use the `agent-messaging` skill to send a message:
- **Recipient**: the requesting agent session name
- **Subject**: `RESULT: <operation_type> - <SUCCESS|FAILED>`
- **Priority**: `normal` (success) or `high` (failure)
- **Content**: type `operation_result`, including:
  - Operation description and outcome
  - Operation type
  - Status (success, failure, partial)
  - Target resource
  - Duration in milliseconds
  - Error details (if failed)

**Status values:**
- `success`: Operation completed successfully
- `failure`: Operation failed (include error details)
- `partial`: Operation partially completed (include details)

---

## 6. When Notifying EOA of New Agent Availability

**Use case:** After spawning agent and adding to team. Inform the orchestrator that a new team member is ready.

**When to use:**
- After successfully spawning new agent
- After adding agent to team registry
- After verifying agent responds to health check

Use the `agent-messaging` skill to send a message:
- **Recipient**: the project orchestrator session name
- **Subject**: `NEW AGENT: <agent_name> available`
- **Priority**: `normal`
- **Content**: type `team_update`, including:
  - Agent name
  - Assigned role
  - Capabilities list
  - Working directory path
  - Team registry path
  - Note that agent is ready to receive task assignments

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

Use the `agent-messaging` skill to send a message:
- **Recipient**: the project orchestrator session name
- **Subject**: `REQUEST: Team status report`
- **Priority**: `normal`
- **Content**: type `status_request`, including:
  - Request for active agents, hibernated agents, in-progress tasks, idle agents
  - Unique request ID for tracking

**Expected response format:**
The orchestrator should respond with type `status_response` including lists of active agents, hibernated agents, in-progress tasks, and idle agents.

---

## 8. When Broadcasting Team Updates

**Use case:** Informing all team members of registry changes. Used when team composition changes.

**When to use:**
- After adding new agent to team
- After removing agent from team
- After updating agent roles
- After team registry structure changes

Use the `agent-messaging` skill to send a message to each team member:
- **Recipient**: each agent in the team (comma-separated or individual messages)
- **Subject**: `TEAM UPDATE: <update_description>`
- **Priority**: `normal`
- **Content**: type `team_broadcast`, including:
  - Description of the update
  - Team registry path
  - Action to take (e.g., `refresh_registry`, `update_roles`, `member_removed`, `member_added`)

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
- **Multiple recipients**: Send individual messages to each recipient, or use comma-separated list in recipient field
