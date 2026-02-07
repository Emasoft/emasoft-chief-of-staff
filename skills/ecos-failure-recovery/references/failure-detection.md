# Failure Detection for Remote Agents

## Table of Contents

- 1.1 When to use this document
- 1.2 Overview of failure detection mechanisms
- 1.3 Heartbeat monitoring via AI Maestro
  - 1.3.1 How heartbeat polling works
  - 1.3.2 Configuring heartbeat intervals
  - 1.3.3 Interpreting heartbeat responses
- 1.4 Message delivery failure detection
  - 1.4.1 Detecting undelivered messages
  - 1.4.2 Detecting unacknowledged messages
  - 1.4.3 Timeout thresholds for message acknowledgment
- 1.5 Task completion timeout detection
  - 1.5.1 Monitoring task progress
  - 1.5.2 Detecting stalled tasks
  - 1.5.3 Distinguishing slow tasks from failed agents
- 1.6 Agent status queries
  - 1.6.1 Querying agent online status
  - 1.6.2 Interpreting status responses
- 1.7 Failure detection decision flowchart

---

## 1.1 When to Use This Document

Use this document when you need to:
- Implement proactive agent health monitoring
- Detect that a remote agent may have crashed or become unresponsive
- Determine whether an agent is offline, unreachable, or simply busy
- Set up heartbeat polling for agents under your supervision

---

## 1.2 Overview of Failure Detection Mechanisms

The Emasoft Chief of Staff (ECOS) uses four primary mechanisms to detect agent failures:

| Mechanism | What It Detects | Response Time |
|-----------|-----------------|---------------|
| Heartbeat monitoring | Agent offline/crashed | 30-60 seconds |
| Message delivery failure | Agent unreachable | Immediate |
| Message acknowledgment timeout | Agent unresponsive | 5-15 minutes |
| Task completion timeout | Agent stalled/hung | Varies by task |

**CRITICAL**: No single mechanism is definitive. ECOS must correlate multiple signals before declaring an agent failed. A single missed heartbeat does not indicate failure.

---

## 1.3 Heartbeat Monitoring via AI Maestro

### 1.3.1 How Heartbeat Polling Works

ECOS sends periodic "ping" messages to agents and expects "pong" responses. The AI Maestro messaging system tracks message delivery and response.

**Heartbeat request**: Use the `agent-messaging` skill to send:
- **Recipient**: the target agent session name
- **Subject**: `[HEARTBEAT] Health check`
- **Priority**: `low`
- **Content**: type `heartbeat`, message: "ping". Include `timestamp` (current ISO timestamp) and `sequence` (incrementing number).

**Expected response from healthy agent**: The agent uses the `agent-messaging` skill to reply with:
- **Recipient**: `ecos-chief-of-staff`
- **Subject**: `[HEARTBEAT] Response`
- **Priority**: `low`
- **Content**: type `heartbeat-response`, message: "pong". Include `original_timestamp`, `response_timestamp`, `sequence`, `status` (healthy/busy/degraded), and `current_task` description.

### 1.3.2 Configuring Heartbeat Intervals

ECOS maintains heartbeat configuration per agent based on their assigned role and criticality:

| Agent Role | Heartbeat Interval | Missed Before Alert |
|------------|-------------------|---------------------|
| Critical infrastructure | 30 seconds | 2 consecutive |
| Active development | 60 seconds | 3 consecutive |
| Background/batch processing | 5 minutes | 3 consecutive |
| Idle/standby | 15 minutes | 5 consecutive |

**Configuration storage**: ECOS stores heartbeat configuration in a local tracking file at:
```
$CLAUDE_PROJECT_DIR/.ecos/agent-health/heartbeat-config.json
```

Example configuration:

```json
{
  "agents": {
    "libs-svg-svgbbox": {
      "role": "active-development",
      "interval_seconds": 60,
      "missed_threshold": 3,
      "last_heartbeat": "2025-01-15T10:30:05Z",
      "consecutive_missed": 0
    },
    "orchestrator-master": {
      "role": "critical-infrastructure",
      "interval_seconds": 30,
      "missed_threshold": 2,
      "last_heartbeat": "2025-01-15T10:30:00Z",
      "consecutive_missed": 0
    }
  }
}
```

### 1.3.3 Interpreting Heartbeat Responses

| Response Status | Meaning | Action Required |
|-----------------|---------|-----------------|
| `healthy` | Agent functioning normally | None |
| `busy` | Agent working, may be slow to respond | Extend timeout |
| `degraded` | Agent experiencing issues | Monitor closely |
| `no response` | No response within timeout | Increment missed counter |
| `delivery_failed` | Message could not be delivered | Check agent status |

**IMPORTANT**: After incrementing the missed counter, check if it exceeds the threshold. If so, proceed to failure classification (see references/failure-classification.md).

---

## 1.4 Message Delivery Failure Detection

### 1.4.1 Detecting Undelivered Messages

When using the `agent-messaging` skill to send a message, check the response for delivery errors. If the skill reports delivery failure, note the error type.

**Common delivery failure reasons:**

| Error Code | Meaning | Indicates |
|------------|---------|-----------|
| `agent_not_found` | No agent with that session name | Agent never registered or wrong name |
| `agent_offline` | Agent registered but not connected | Agent crashed or disconnected |
| `timeout` | Delivery timed out | Network issues or overloaded server |

### 1.4.2 Detecting Unacknowledged Messages

Even when delivery succeeds, the agent may not acknowledge receipt. ECOS tracks sent messages and monitors for acknowledgments.

Use the `agent-messaging` skill to list sent messages filtered by status "unacknowledged" to identify messages that were delivered but not acknowledged.

### 1.4.3 Timeout Thresholds for Message Acknowledgment

| Message Priority | Acknowledgment Timeout | Action on Timeout |
|------------------|----------------------|-------------------|
| `urgent` | 2 minutes | Immediate escalation |
| `high` | 5 minutes | Send reminder, then escalate |
| `normal` | 15 minutes | Send reminder |
| `low` | 1 hour | Log only |

**CRITICAL**: Acknowledgment timeout alone does not indicate agent failure. The agent may be:
- Busy with a long-running task
- Waiting for user input
- Processing a large context

Always correlate with heartbeat data before escalating.

---

## 1.5 Task Completion Timeout Detection

### 1.5.1 Monitoring Task Progress

ECOS tracks all assigned tasks with expected completion times. The tracking file is at:
```
$CLAUDE_PROJECT_DIR/.ecos/agent-health/task-tracking.json
```

Example entry:

```json
{
  "task_id": "task-20250115-001",
  "agent": "libs-svg-svgbbox",
  "description": "Implement bounding box calculation",
  "assigned_at": "2025-01-15T09:00:00Z",
  "expected_completion": "2025-01-15T12:00:00Z",
  "last_progress_update": "2025-01-15T10:30:00Z",
  "progress_percentage": 60,
  "status": "in_progress"
}
```

### 1.5.2 Detecting Stalled Tasks

A task is considered stalled when:
1. No progress update received for more than 30 minutes, AND
2. Expected completion time has passed, AND
3. Agent has not sent any messages explaining the delay

### 1.5.3 Distinguishing Slow Tasks from Failed Agents

**CRITICAL**: A stalled task does not necessarily mean a failed agent. Before escalating:

1. **Send a status inquiry message** using the `agent-messaging` skill:
   - **Recipient**: the agent session name
   - **Subject**: `[STATUS CHECK] Task progress inquiry`
   - **Priority**: `high`
   - **Content**: type `status-inquiry`, message: "Your task ([task-id]) appears stalled. Please provide a status update within 5 minutes." Include `task_id` and `expected_response_by` timestamp.

2. **Wait for response** (5 minutes for high priority)

3. **Check heartbeat status** - if heartbeats are still responding, agent is alive but task may be blocked

4. **Only declare failure** if:
   - No response to status inquiry, AND
   - Heartbeats have stopped, OR
   - Agent explicitly reports it cannot continue

---

## 1.6 Agent Status Queries

### 1.6.1 Querying Agent Online Status

Use the `ai-maestro-agents-management` skill to get the agent's details by session name. The result includes status, last_seen timestamp, registered_at, host, and unread message count.

Example response for online agent:

```json
{
  "session_name": "libs-svg-svgbbox",
  "status": "online",
  "last_seen": "2025-01-15T10:30:00Z",
  "registered_at": "2025-01-15T08:00:00Z",
  "host": "workstation-1",
  "unread_messages": 2
}
```

### 1.6.2 Interpreting Status Responses

| Status | Meaning | Failure Likelihood |
|--------|---------|-------------------|
| `online` | Agent connected and responsive | Low |
| `idle` | Agent connected but no recent activity | Low |
| `busy` | Agent actively processing | Low |
| `offline` | Agent disconnected | High - investigate |
| `not_found` | No agent with this name | Check name, may be crashed |

---

## 1.7 Failure Detection Decision Flowchart

```
START: Routine health check
    |
    v
[Send heartbeat] --> [Response received?]
    |                       |
    | No                    | Yes
    v                       v
[Increment missed     [Reset missed counter]
 counter]                   |
    |                       v
    v                  [Agent healthy]
[Missed >= threshold?]      |
    |                       v
    | No                   END
    v
[Schedule next heartbeat]
    |
    | Yes
    v
[Check agent status via ai-maestro-agents-management skill]
    |
    v
[Status == "offline"?]
    |           |
    | Yes       | No (online but not responding)
    v           v
[FAILURE:      [Send high-priority status inquiry]
 Agent              |
 OFFLINE]           v
    |          [Response within 5 min?]
    v               |           |
[Proceed to         | No        | Yes
 classification]    v           v
                [FAILURE:   [Agent busy,
                 Agent       extend timeout]
                 UNRESPONSIVE]    |
                    |            v
                    v           END
               [Proceed to
                classification]
```

After detecting a failure, proceed to **references/failure-classification.md** to determine severity and appropriate response.

---

## Troubleshooting

### Heartbeats show agent offline but it is running

**Symptom**: Heartbeat monitoring reports agent offline, but you can see the agent's Claude Code session is active.

**Cause**: The agent may not have the AI Maestro message polling hook enabled, or the hook is failing silently.

**Solution**:
1. Check if the agent has AI Maestro hooks configured in its `~/.claude/settings.json`
2. Use the `ai-maestro-agents-management` skill to check service health
3. Check agent's hook logs for errors

### False positives during long operations

**Symptom**: Agent reported as unresponsive while performing a long git operation or large file processing.

**Cause**: The agent's main thread is blocked and cannot respond to heartbeats.

**Solution**:
1. Configure longer heartbeat intervals for agents that perform long-blocking operations
2. Instruct agents to send "busy" status before starting long operations
3. Use task-based monitoring instead of heartbeat-based for these agents

### AI Maestro not responding

**Symptom**: All status checks fail.

**Cause**: AI Maestro server is not running.

**Solution**:
1. Use the `ai-maestro-agents-management` skill to check service health
2. If the service is down, start AI Maestro: `cd ~/ai-maestro && ./start.sh`
3. Check if the port is blocked by firewall or another process
