# Recovery Operations Reference

## Contents

- [1. Detecting Agent Failures Using Health Checks](#1-detecting-agent-failures-using-health-checks)
  - [1.1 Checking AI Maestro Registry](#11-checking-ai-maestro-registry)
  - [1.2 Verifying tmux Session Existence](#12-verifying-tmux-session-existence)
  - [1.3 Checking Process Health](#13-checking-process-health)
  - [1.4 Testing Message Response](#14-testing-message-response)
  - [1.5 Checking Host Reachability for Remote Agents](#15-checking-host-reachability-for-remote-agents)
- [2. Classifying Failure Severity (Transient/Recoverable/Terminal)](#2-classifying-failure-severity-transientrecoverableterminal)
  - [2.1 Failure Classification Criteria Table](#21-failure-classification-criteria-table)
  - [2.2 Classification Algorithm](#22-classification-algorithm)
- [3. Executing Recovery Strategies Based on Failure Type](#3-executing-recovery-strategies-based-on-failure-type)
  - [3.1 Recovery Strategy Decision Tree](#31-recovery-strategy-decision-tree)
  - [3.2 Transient Recovery (Automatic)](#32-transient-recovery-automatic)
  - [3.3 Recoverable Recovery (Automatic with Notification)](#33-recoverable-recovery-automatic-with-notification)
  - [3.4 Terminal Recovery (Requires Approval Unless Pre-Authorized)](#34-terminal-recovery-requires-approval-unless-pre-authorized)
- [4. Restarting Unresponsive Agents](#4-restarting-unresponsive-agents)
  - [4.1 Soft Restart Procedure](#41-soft-restart-procedure)
  - [4.2 Wake via Lifecycle Manager](#42-wake-via-lifecycle-manager)
  - [4.3 Full Agent Replacement](#43-full-agent-replacement)
- [5. Configuring Recovery Policies](#5-configuring-recovery-policies)
  - [5.1 Recovery Policy File Location](#51-recovery-policy-file-location)
  - [5.2 Recovery Policy Parameters](#52-recovery-policy-parameters)
- [6. Logging All Recovery Actions](#6-logging-all-recovery-actions)
  - [6.1 Recovery Log File Format](#61-recovery-log-file-format)
  - [6.2 Recovery Event Schema](#62-recovery-event-schema)
- [7. Coordinating with Other Agents During Recovery](#7-coordinating-with-other-agents-during-recovery)
  - [7.1 Sending Recovery Warnings](#71-sending-recovery-warnings)
  - [7.2 Notifying Orchestrator of Orphaned Tasks](#72-notifying-orchestrator-of-orphaned-tasks)
  - [7.3 Escalating to Manager for Approval](#73-escalating-to-manager-for-approval)
  - [7.4 Requesting Agent Replacement](#74-requesting-agent-replacement)
- [8. Monitoring Agent Health Continuously](#8-monitoring-agent-health-continuously)
  - [8.1 Continuous Health Check Loop](#81-continuous-health-check-loop)
  - [8.2 On-Demand Health Check](#82-on-demand-health-check)

---

## 1. Detecting Agent Failures Using Health Checks

When monitoring agent health, run these checks in order:

### 1.1 Checking AI Maestro Registry

**Purpose**: Verify agent registration and last-seen timestamp.

Use the `ai-maestro-agents-management` skill to get the agent's details by session name. The result includes status, last_seen timestamp, and session_name fields.

**What to look for:**
- If `status == "offline"` then the agent may be down
- If `last_seen > 10 minutes ago` then the agent may be stale
- If agent not in registry then the agent never registered or crashed

### 1.2 Verifying tmux Session Existence

**Purpose**: Confirm the tmux session is running.

```bash
# Verify tmux session exists
tmux has-session -t <agent-name> 2>/dev/null && echo "SESSION_EXISTS" || echo "SESSION_MISSING"
```

**What to look for:**
- `SESSION_MISSING` then TERMINAL failure (session crashed)
- `SESSION_EXISTS` then continue to process health check

### 1.3 Checking Process Health

**Purpose**: Verify Claude Code process is running inside the tmux session.

```bash
# Check if Claude Code process is running in the session
tmux list-panes -t <agent-name> -F '#{pane_pid}' 2>/dev/null | xargs -I {} ps -p {} -o pid,state,comm
```

**What to look for:**
- Process not found then RECOVERABLE failure (process crashed but session exists)
- `state == D` (uninterruptible sleep) then possible stuck process
- `state == S` (sleeping) then normal idle state

### 1.4 Testing Message Response

**Purpose**: Confirm the agent can receive and respond to messages.

Use the `agent-messaging` skill to send a health check ping:
- **Recipient**: the target agent session name
- **Subject**: `Health Check Ping`
- **Priority**: `high`
- **Content**: type `health-check`, message: "PING"

**Verify**: confirm message delivery via the `agent-messaging` skill's sent messages feature.

Wait 60 seconds, then use the `agent-messaging` skill to check for unread messages. Look for a response with subject "Health Check Pong".

**What to look for:**
- No response within 60 seconds then RECOVERABLE or TERMINAL depending on other checks
- Response received then agent is healthy

### 1.5 Checking Host Reachability for Remote Agents

**Purpose**: For remote agents, verify the host machine is reachable.

```bash
# If agent is on remote host
ping -c 3 <host-ip> && echo "HOST_REACHABLE" || echo "HOST_UNREACHABLE"
```

**What to look for:**
- `HOST_UNREACHABLE` then TERMINAL failure (host down, cannot recover remotely)
- `HOST_REACHABLE` then host is up, agent issue is local

---

## 2. Classifying Failure Severity (Transient/Recoverable/Terminal)

### 2.1 Failure Classification Criteria Table

| Classification | Criteria | Typical Causes | Auto-Recovery? |
|----------------|----------|----------------|----------------|
| **TRANSIENT** | Single missed ping, process restarting | Network blip, brief overload | YES |
| **RECOVERABLE** | Session exists but unresponsive for 2-5 min | Memory pressure, stuck process | YES |
| **TERMINAL** | Session missing, host unreachable, repeated failures | Crash, hardware failure, corruption | NO (needs approval) |

### 2.2 Classification Algorithm

Use this decision tree to classify failures:

```
IF tmux_session_missing:
    IF host_unreachable:
        RETURN "TERMINAL" (host down)
    ELSE:
        RETURN "TERMINAL" (session crashed)

IF process_not_running:
    RETURN "RECOVERABLE" (process crashed but session exists)

IF no_ping_response:
    IF first_failure:
        RETURN "TRANSIENT" (retry)
    ELIF failures_count < 3:
        RETURN "RECOVERABLE" (unresponsive)
    ELSE:
        RETURN "TERMINAL" (repeated failures)

IF last_seen > 10_minutes_ago:
    RETURN "RECOVERABLE" (stale)

RETURN "HEALTHY"
```

**Key decision points:**
1. **Session exists?** No then TERMINAL
2. **Process running?** No then RECOVERABLE
3. **Responds to pings?** No then count failures (1 = TRANSIENT, 2-3 = RECOVERABLE, 3+ = TERMINAL)
4. **Last seen recent?** No then RECOVERABLE

---

## 3. Executing Recovery Strategies Based on Failure Type

### 3.1 Recovery Strategy Decision Tree

```
FAILURE_DETECTED
    |
    +-- TRANSIENT?
    |       |
    |       YES --> Retry health check (3x)
    |               |
    |               +-- Still failing? --> Escalate to RECOVERABLE
    |               +-- Healthy? --> Log & continue monitoring
    |
    +-- RECOVERABLE?
    |       |
    |       YES --> Notify agent of pending recovery
    |               |
    |               +-- Attempt soft restart
    |                   |
    |                   +-- Recovered? --> Log & continue monitoring
    |                   +-- Not recovered? --> Attempt wake via lifecycle-manager
    |                       |
    |                       +-- Recovered? --> Log & continue monitoring
    |                       +-- Not recovered? --> Escalate to TERMINAL
    |
    +-- TERMINAL?
            |
            YES --> Notify affected parties:
                    - Orchestrator (EOA) for task reassignment
                    - Manager (EAMA) for critical failure
                    |
                    +-- Check recovery policy
                        |
                        +-- Auto-replace authorized? --> Route to lifecycle-manager
                        |
                        +-- Approval required? --> Request approval from EAMA
```

### 3.2 Transient Recovery (Automatic)

**When to use**: Single missed health check, first-time failure.

**Procedure:**

1. Wait 30 seconds
2. Use the `ai-maestro-agents-management` skill to re-check the agent's status
3. If still failing, retry up to 3 times with exponential backoff (30s, 60s, 90s)

**Decision after 3 retries:**
- If healthy then log and continue monitoring
- If still failing then escalate to RECOVERABLE

### 3.3 Recoverable Recovery (Automatic with Notification)

**When to use**: Agent unresponsive but session exists, process may be stuck.

**Procedure:**

1. Use the `agent-messaging` skill to notify the agent of pending recovery:
   - **Recipient**: the failing agent session name
   - **Subject**: `Recovery Warning`
   - **Priority**: `urgent`
   - **Content**: type `recovery-warning`, message: "You will be restarted in 60 seconds due to unresponsiveness."

2. Wait 60 seconds for potential self-recovery

3. If still unresponsive, use the `ai-maestro-agents-management` skill to restart the agent

**Decision after restart:**
- If healthy then log and continue monitoring
- If still failing then escalate to TERMINAL

### 3.4 Terminal Recovery (Requires Approval Unless Pre-Authorized)

**When to use**: Session crashed, host unreachable, or repeated failures.

**Procedure:**

1. Use the `agent-messaging` skill to notify the orchestrator of task orphaning risk:
   - **Recipient**: the orchestrator session name (e.g., `orchestrator-master`)
   - **Subject**: `Agent Failure - Tasks Need Reassignment`
   - **Priority**: `urgent`
   - **Content**: type `failure-report`, message: "Agent [agent-name] has TERMINAL failure. Assigned tasks need reassignment."

2. Use the `agent-messaging` skill to notify the manager for critical failure:
   - **Recipient**: `eama-assistant-manager` (or the manager session name)
   - **Subject**: `CRITICAL: Agent Failure`
   - **Priority**: `urgent`
   - **Content**: type `critical-failure`, message: "Agent [agent-name] has experienced TERMINAL failure. Classification: [reason]. Recovery options: 1) Replace agent, 2) Reassign tasks only, 3) Manual investigation. Awaiting approval."

3. Check the recovery policy file at `$CLAUDE_PROJECT_DIR/thoughts/shared/recovery-policy.json`. If `auto_replace_on_terminal` is true, proceed with automatic replacement via the `ai-maestro-agents-management` skill. Otherwise, wait for manager approval by polling inbox.

**Required notifications:**
- Orchestrator: Task reassignment
- Manager: Approval request

---

## 4. Restarting Unresponsive Agents

### 4.1 Soft Restart Procedure

**When to use**: Agent process is stuck but tmux session exists.

**Steps:**
1. Send SIGTERM to the Claude Code process
2. Wait 30 seconds for graceful shutdown
3. Process should automatically restart (tmux keeps session alive)
4. Verify health after restart

**Command:**
```bash
# Get the process PID
PID=$(tmux list-panes -t <agent-name> -F '#{pane_pid}')

# Send SIGTERM
kill -TERM $PID

# Wait for restart
sleep 30
```

After waiting, use the `ai-maestro-agents-management` skill to check the agent's status.

### 4.2 Wake via Lifecycle Manager

**When to use**: Soft restart failed or process is in unrecoverable state.

**Steps:**
1. Use the `ai-maestro-agents-management` skill to restart the agent
2. Wait for agent to re-register with AI Maestro
3. Verify health

### 4.3 Full Agent Replacement

**When to use**: Terminal failure (session crashed, cannot restart).

**Steps:**
1. Use the `ai-maestro-agents-management` skill to terminate the failed agent (cleanup)
2. Use the `ai-maestro-agents-management` skill to spawn a new agent with incremented name (e.g., worker-001 to worker-002)
3. Transfer tasks to new agent
4. Update agent registry
5. Notify all affected parties using the `agent-messaging` skill

---

## 5. Configuring Recovery Policies

### 5.1 Recovery Policy File Location

**Path:** `$CLAUDE_PROJECT_DIR/thoughts/shared/recovery-policy.json`

This file must be accessible to the Recovery Coordinator agent.

### 5.2 Recovery Policy Parameters

```json
{
  "auto_replace_on_terminal": false,
  "max_auto_recovery_attempts": 3,
  "transient_retry_count": 3,
  "transient_retry_backoff_seconds": 30,
  "recoverable_wait_seconds": 60,
  "health_check_interval_seconds": 300,
  "stale_threshold_minutes": 10,
  "unresponsive_threshold_minutes": 5,
  "notify_manager_on": ["terminal", "repeated_recoverable"],
  "notify_orchestrator_on": ["terminal", "recoverable_with_tasks"]
}
```

**Parameter descriptions:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `auto_replace_on_terminal` | boolean | If true, automatically replace agents on terminal failure without approval |
| `max_auto_recovery_attempts` | integer | Max retries before escalating to next failure level |
| `transient_retry_count` | integer | Number of retries for transient failures |
| `transient_retry_backoff_seconds` | integer | Base delay between transient retries (exponential backoff) |
| `recoverable_wait_seconds` | integer | Wait time after sending recovery warning |
| `health_check_interval_seconds` | integer | Continuous monitoring poll interval |
| `stale_threshold_minutes` | integer | Minutes before last_seen is considered stale |
| `unresponsive_threshold_minutes` | integer | Minutes without response before RECOVERABLE classification |
| `notify_manager_on` | array | Failure types that trigger manager notification |
| `notify_orchestrator_on` | array | Failure types that trigger orchestrator notification |

**Safety recommendation:**
- Set `auto_replace_on_terminal: false` in production
- Require manual approval for terminal failures to prevent cascading issues

---

## 6. Logging All Recovery Actions

### 6.1 Recovery Log File Format

**Path:** `$CLAUDE_PROJECT_DIR/thoughts/shared/recovery-log.json`

**Structure:**
```json
{
  "recovery_events": [
    {
      "timestamp": "2026-02-02T10:30:00Z",
      "agent": "worker-dev-auth-001",
      "failure_type": "RECOVERABLE",
      "failure_reason": "No ping response for 3 minutes",
      "detection_method": "health_check_ping",
      "recovery_action": "soft_restart",
      "recovery_result": "success",
      "duration_seconds": 45,
      "notifications_sent": [
        {"to": "worker-dev-auth-001", "type": "recovery-warning"}
      ]
    }
  ]
}
```

### 6.2 Recovery Event Schema

**Required fields:**
- `timestamp`: ISO 8601 timestamp of failure detection
- `agent`: Full session name of failed agent
- `failure_type`: "TRANSIENT", "RECOVERABLE", or "TERMINAL"
- `failure_reason`: Human-readable explanation
- `detection_method`: How failure was detected
- `recovery_action`: Action taken
- `recovery_result`: "success", "failed", or "pending_approval"

**Optional fields:**
- `duration_seconds`: Time from detection to recovery
- `notifications_sent`: Array of messages sent
- `approval_status`: If awaiting approval
- `orphaned_tasks`: List of tasks needing reassignment
- `replacement_agent`: New agent session name (if replaced)
- `approval_by`: Who approved terminal recovery

**Logging rules:**
- Log ALL recovery events (even transient)
- Log before and after state changes
- Include all notifications sent
- For terminal failures, log orphaned tasks

---

## 7. Coordinating with Other Agents During Recovery

### 7.1 Sending Recovery Warnings

**Purpose**: Notify the failing agent before forceful restart.

Use the `agent-messaging` skill to send:
- **Recipient**: the failing agent session name
- **Subject**: `Recovery Warning`
- **Priority**: `urgent`
- **Content**: type `recovery-warning`, message: "You have been unresponsive for 3 minutes. Recovery will be attempted in 60 seconds." Include `recovery_type`: "soft_restart", `countdown_seconds`: 60.

**Verify**: confirm message delivery via the `agent-messaging` skill's sent messages feature.

**When to send:**
- Before all RECOVERABLE actions
- At least 60 seconds before forced restart
- Allows agent to self-correct if possible

### 7.2 Notifying Orchestrator of Orphaned Tasks

**Purpose**: Prevent task loss when agent fails.

Use the `agent-messaging` skill to send:
- **Recipient**: the orchestrator session name (e.g., `orchestrator-master`)
- **Subject**: `Agent Failure - Tasks Need Reassignment`
- **Priority**: `urgent`
- **Content**: type `failure-report`, message: "Agent [agent-name] has experienced TERMINAL failure." Include `failed_agent`, `failure_classification`: "TERMINAL", `failure_reason`, `orphaned_tasks` (list of task descriptions), `recommended_action`: "reassign_tasks".

**Verify**: confirm message delivery via the `agent-messaging` skill's sent messages feature.

**When to send:**
- ALL TERMINAL failures
- RECOVERABLE failures where agent has assigned tasks

### 7.3 Escalating to Manager for Approval

**Purpose**: Get human approval for terminal recovery actions.

Use the `agent-messaging` skill to send:
- **Recipient**: `eama-assistant-manager` (or the manager session name)
- **Subject**: `CRITICAL: Agent Terminal Failure`
- **Priority**: `urgent`
- **Content**: type `critical-failure`, message: "Agent [agent-name] has experienced TERMINAL failure requiring approval." Include `failed_agent`, `failure_classification`: "TERMINAL", `failure_reason`, `recovery_attempts` count, `orphaned_tasks` list, `recovery_options` array listing "replace", "reassign_only", and "investigate" options with descriptions, `awaiting`: "approval".

**Verify**: confirm message delivery via the `agent-messaging` skill's sent messages feature.

**When to send:**
- TERMINAL failures when `auto_replace_on_terminal: false`
- Repeated RECOVERABLE failures (3+ attempts)

### 7.4 Requesting Agent Replacement

**Purpose**: Execute approved terminal recovery.

Use the `ai-maestro-agents-management` skill to:
1. Terminate the failed agent
2. Spawn a replacement agent with the specified configuration (session name, role, project, plugins, directory)
3. Transfer tasks to the new agent

**When to execute:**
- After manager approval OR
- When `auto_replace_on_terminal: true`

---

## 8. Monitoring Agent Health Continuously

### 8.1 Continuous Health Check Loop

**Frequency**: Every `health_check_interval_seconds` (default: 300 seconds / 5 minutes)

**Workflow:**
```
EVERY health_check_interval (default 5 minutes):

    FOR each agent IN agent_registry WHERE status == "active":

        1. Run failure detection checklist

        2. IF failure detected:
            a. Classify failure
            b. Execute recovery strategy
            c. Log recovery event

        3. Update agent last_checked timestamp

    END FOR

    Generate health summary if any failures occurred
```

**What to monitor:**
- All agents with status "active"
- Skip agents marked "hibernated"
- Log all check timestamps

**Health summary format:**
```json
{
  "timestamp": "2026-02-02T14:00:00Z",
  "total_agents_checked": 15,
  "healthy_agents": 13,
  "transient_failures": 1,
  "recoverable_failures": 1,
  "terminal_failures": 0,
  "recovery_actions_taken": 2
}
```

### 8.2 On-Demand Health Check

**When triggered:**
- Explicit request from orchestrator
- Explicit request from manager
- After suspicious activity (e.g., task timeout)

**Workflow:**
```
1. Run full failure detection checklist for specified agent(s)
2. Report findings immediately
3. Execute recovery if authorized
4. Return detailed status report
```

**Status report format:**
```json
{
  "agent": "worker-dev-auth-001",
  "check_timestamp": "2026-02-02T14:05:00Z",
  "status": "HEALTHY",
  "checks": {
    "registry": "PASS",
    "tmux_session": "PASS",
    "process_health": "PASS",
    "message_response": "PASS"
  },
  "recovery_needed": false
}
```

---

## Integration with Other Agents

| Agent | Integration Point | Purpose |
|-------|------------------|---------|
| **ecos-lifecycle-manager** | Replacement execution | Terminate failed agents, spawn replacements |
| **ecos-main** | Routing target | Receives recovery coordination requests |
| **ecos-resource-monitor** | Resource data | Check if failure is resource-related |
| **orchestrator-master (EOA)** | Task reassignment | Notify of orphaned tasks |
| **assistant-manager (EAMA)** | Escalation | Approve terminal recovery actions |

**Key integration rules:**
- Always notify EOA when tasks are orphaned
- Always notify EAMA for terminal failures (unless pre-authorized)
- Always route restart/replacement to lifecycle-manager
- Always check resource-monitor for context on resource-related failures
