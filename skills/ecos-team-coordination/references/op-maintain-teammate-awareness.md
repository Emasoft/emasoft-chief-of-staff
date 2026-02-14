---
operation: maintain-teammate-awareness
procedure: proc-notify-team-ready
workflow-instruction: Step 5 - Team Ready Notification
parent-skill: ecos-team-coordination
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Maintain Teammate Awareness


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Poll AI Maestro for Active Sessions](#step-1-poll-ai-maestro-for-active-sessions)
  - [Step 2: Query Each Agent's Status](#step-2-query-each-agents-status)
  - [Step 3: Update Team Roster](#step-3-update-team-roster)
  - [Step 4: Identify Inactive Agents](#step-4-identify-inactive-agents)
  - [Step 5: Flag Issues](#step-5-flag-issues)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Initial Team State Discovery](#example-initial-team-state-discovery)
  - [Example: Pre-Task Assignment Check](#example-pre-task-assignment-check)
  - [Example: Team Status Report Generation](#example-team-status-report-generation)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

Trigger this operation when:
- Starting a coordination session (initial team state discovery)
- Before assigning new tasks (verify agent availability)
- Reporting team status to user or manager
- Detecting potential issues (inactive agents, overloaded agents)
- Periodically during long operations (every 5-10 minutes)

## Prerequisites

- AI Maestro is running
- The `ai-maestro-agents-management` skill is available
- The `agent-messaging` skill is available
- Team roster exists with expected agents
- Permission to query agent sessions
- Understanding of expected team composition

## Procedure

### Step 1: Poll AI Maestro for Active Sessions

Use the `ai-maestro-agents-management` skill to list all registered sessions. Note each session's name, status, and last seen timestamp.

### Step 2: Query Each Agent's Status

For agents that need detailed status, use the `agent-messaging` skill to send a status request:
- **Recipient**: the target agent session name
- **Subject**: `Status Check`
- **Priority**: `normal`
- **Content**: type `status-request`, message: "Please report your current status: task, progress, blockers."

### Step 3: Update Team Roster

Compile status information into team roster:
- Agent name
- Session status (active/inactive/hibernating)
- Current task (if known)
- Last seen timestamp
- Any reported blockers

### Step 4: Identify Inactive Agents

Compare expected team members against the active sessions returned by the `ai-maestro-agents-management` skill. For each expected agent that does not appear in the active list, flag it as MISSING.

### Step 5: Flag Issues

Document any anomalies:
- Agents that should be active but are not
- Agents that have not responded to status requests
- Agents with stale lastSeen timestamps (more than 5 minutes)
- Agents reporting blockers

## Checklist

Copy this checklist and track your progress:

- [ ] Used `ai-maestro-agents-management` skill to poll all active sessions
- [ ] Sent status requests to key agents via `agent-messaging` skill
- [ ] Updated team roster with current information
- [ ] Identified any inactive or missing agents
- [ ] Flagged issues for follow-up
- [ ] Documented team state for reporting

## Examples

### Example: Initial Team State Discovery

**Scenario:** Chief of Staff starting a new coordination session.

1. Use the `ai-maestro-agents-management` skill to list all registered sessions. Note name, status, and last seen timestamp for each.

2. Use the `agent-messaging` skill to check for unread messages in the Chief of Staff inbox. Note any pending issues from other agents.

**Expected results:**
- A list of all active agents with their current status
- Any unread messages requiring attention

### Example: Pre-Task Assignment Check

**Scenario:** Before assigning a task to `code-impl-auth`, verify availability.

1. Use the `ai-maestro-agents-management` skill to list agents and find `code-impl-auth`. Check its status.

2. If the agent is active, use the `agent-messaging` skill to send:
   - **Recipient**: `code-impl-auth`
   - **Subject**: `Availability Check`
   - **Priority**: `normal`
   - **Content**: type `status-request`, message: "Are you available for a new task? Please report current workload."

3. If the agent is NOT active, log a warning and consider waking or spawning a replacement.

### Example: Team Status Report Generation

**Scenario:** Generate a summary for the user.

1. Use the `ai-maestro-agents-management` skill to list all sessions.
2. For each session, record agent name, status, and last seen timestamp.
3. Format as a team status report with all agent details.

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| AI Maestro unavailable | Service not running | Use the `ai-maestro-agents-management` skill to check service health; notify user if service is down |
| Agent shows stale lastSeen | Agent hibernated or crashed | Attempt to wake agent; if no response, flag for user attention |
| Status request times out | Agent busy or unresponsive | Wait 30 seconds, retry once; if still no response, mark as "unresponsive" |
| Team roster mismatch | New agents not registered | Update expected team list; query for newly registered sessions |
| Inconsistent status data | Cache or sync issue | Force refresh by re-querying all sessions; clear local roster cache |

## Related Operations

- [op-assign-agent-roles.md](op-assign-agent-roles.md) - Awareness informs role assignments
- [op-send-team-messages.md](op-send-team-messages.md) - Status requests use messaging
- [teammate-awareness.md](teammate-awareness.md) - Complete awareness reference documentation
