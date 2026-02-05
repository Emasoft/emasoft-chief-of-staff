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

```bash
# Get agent status from AI Maestro
curl -s "http://localhost:23000/api/agents" | jq '.agents[] | select(.session_name == "<agent-name>")'
```

**Expected fields:**
- `status`: "online", "offline", "hibernated"
- `last_seen`: ISO timestamp (check if stale)
- `session_name`: Full session name

**What to look for:**
- If `status == "offline"` → Agent may be down
- If `last_seen > 10 minutes ago` → Agent may be stale
- If agent not in registry → Agent never registered or crashed

### 1.2 Verifying tmux Session Existence

**Purpose**: Confirm the tmux session is running.

```bash
# Verify tmux session exists
tmux has-session -t <agent-name> 2>/dev/null && echo "SESSION_EXISTS" || echo "SESSION_MISSING"
```

**What to look for:**
- `SESSION_MISSING` → TERMINAL failure (session crashed)
- `SESSION_EXISTS` → Continue to process health check

### 1.3 Checking Process Health

**Purpose**: Verify Claude Code process is running inside the tmux session.

```bash
# Check if Claude Code process is running in the session
tmux list-panes -t <agent-name> -F '#{pane_pid}' 2>/dev/null | xargs -I {} ps -p {} -o pid,state,comm
```

**What to look for:**
- Process not found → RECOVERABLE failure (process crashed but session exists)
- `state == D` (uninterruptible sleep) → Possible stuck process
- `state == S` (sleeping) → Normal idle state

### 1.4 Testing Message Response

**Purpose**: Confirm the agent can receive and respond to messages.

```bash
# Send health check ping
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'${SESSION_NAME}'",
    "to": "<agent-name>",
    "subject": "Health Check Ping",
    "priority": "high",
    "content": {"type": "health-check", "message": "PING"}
  }'

# Wait 60 seconds, then check for response
sleep 60
curl -s "http://localhost:23000/api/messages?agent=${SESSION_NAME}&action=list&status=unread" | \
  jq '.messages[] | select(.subject == "Health Check Pong")'
```

**What to look for:**
- No response within 60 seconds → RECOVERABLE or TERMINAL depending on other checks
- Response received → Agent is healthy

### 1.5 Checking Host Reachability for Remote Agents

**Purpose**: For remote agents, verify the host machine is reachable.

```bash
# If agent is on remote host
ping -c 3 <host-ip> && echo "HOST_REACHABLE" || echo "HOST_UNREACHABLE"
```

**What to look for:**
- `HOST_UNREACHABLE` → TERMINAL failure (host down, cannot recover remotely)
- `HOST_REACHABLE` → Host is up, agent issue is local

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
1. **Session exists?** No → TERMINAL
2. **Process running?** No → RECOVERABLE
3. **Responds to pings?** No → Count failures (1 = TRANSIENT, 2-3 = RECOVERABLE, 3+ = TERMINAL)
4. **Last seen recent?** No → RECOVERABLE

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
    |               +-- Attempt soft restart:
    |                   - Send SIGTERM to process
    |                   - Wait 30 seconds
    |                   - Check if recovered
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
                        +-- Auto-replace authorized? --> Route to lifecycle-manager:
                        |                               - Terminate failed agent
                        |                               - Spawn replacement
                        |                               - Reassign tasks
                        |
                        +-- Approval required? --> Request approval from EAMA:
                                                   - Wait for response
                                                   - Execute approved action
```

### 3.2 Transient Recovery (Automatic)

**When to use**: Single missed health check, first-time failure.

**Procedure:**

```bash
# 1. Wait 30 seconds
sleep 30

# 2. Re-check health
curl -s "http://localhost:23000/api/agents" | jq '.agents[] | select(.session_name == "<agent>")'

# 3. If still failing, retry up to 3 times with exponential backoff
for i in 1 2 3; do
    sleep $((30 * i))
    # Check health again
done
```

**Decision after 3 retries:**
- If healthy → Log and continue monitoring
- If still failing → Escalate to RECOVERABLE

### 3.3 Recoverable Recovery (Automatic with Notification)

**When to use**: Agent unresponsive but session exists, process may be stuck.

**Procedure:**

```bash
# 1. Notify agent of pending recovery
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'${SESSION_NAME}'",
    "to": "<agent>",
    "subject": "Recovery Warning",
    "priority": "urgent",
    "content": {"type": "recovery-warning", "message": "You will be restarted in 60 seconds due to unresponsiveness"}
  }'

# 2. Wait for potential self-recovery
sleep 60

# 3. If still unresponsive, attempt restart via lifecycle-manager
# Route to ecos-lifecycle-manager with restart request
```

**Decision after restart:**
- If healthy → Log and continue monitoring
- If still failing → Escalate to TERMINAL

### 3.4 Terminal Recovery (Requires Approval Unless Pre-Authorized)

**When to use**: Session crashed, host unreachable, or repeated failures.

**Procedure:**

```bash
# 1. Notify orchestrator of task orphaning risk
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'${SESSION_NAME}'",
    "to": "orchestrator-master",
    "subject": "Agent Failure - Tasks Need Reassignment",
    "priority": "urgent",
    "content": {"type": "failure-report", "message": "Agent <agent> has TERMINAL failure. Assigned tasks need reassignment."}
  }'

# 2. Notify manager for critical failure
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'${SESSION_NAME}'",
    "to": "assistant-manager",
    "subject": "CRITICAL: Agent Failure",
    "priority": "urgent",
    "content": {"type": "critical-failure", "message": "Agent <agent> has experienced TERMINAL failure. Classification: <reason>. Recovery options: 1) Replace agent, 2) Reassign tasks only, 3) Manual investigation. Awaiting approval."}
  }'

# 3. Check if pre-authorized for auto-replace
recovery_policy=$(cat "$CLAUDE_PROJECT_DIR/thoughts/shared/recovery-policy.json" | jq '.auto_replace_on_terminal')

if [ "$recovery_policy" == "true" ]; then
    # Auto-replace via lifecycle-manager
    # Route to ecos-lifecycle-manager
else
    # Wait for manager approval
    # Poll for approval message
fi
```

**Required notifications:**
- Orchestrator → Task reassignment
- Manager → Approval request

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

# Check health
curl -s "http://localhost:23000/api/agents" | jq '.agents[] | select(.session_name == "<agent-name>")'
```

### 4.2 Wake via Lifecycle Manager

**When to use**: Soft restart failed or process is in unrecoverable state.

**Steps:**
1. Route restart request to `ecos-lifecycle-manager`
2. Lifecycle manager uses `aimaestro-agent.sh restart <agent-name>`
3. Wait for agent to re-register with AI Maestro
4. Verify health

**Message format:**
```json
{
  "from": "chief-of-staff",
  "to": "ecos-lifecycle-manager",
  "subject": "Restart Agent",
  "priority": "high",
  "content": {
    "type": "restart-request",
    "agent": "<agent-name>",
    "reason": "unresponsive",
    "method": "wake"
  }
}
```

### 4.3 Full Agent Replacement

**When to use**: Terminal failure (session crashed, cannot restart).

**Steps:**
1. Route replacement request to `ecos-lifecycle-manager`
2. Lifecycle manager:
   - Terminates old agent (cleanup)
   - Spawns new agent with incremented name (e.g., worker-001 → worker-002)
   - Transfers tasks to new agent
3. Update agent registry
4. Notify all affected parties

**Message format:**
```json
{
  "from": "chief-of-staff",
  "to": "ecos-lifecycle-manager",
  "subject": "Agent Replacement Request",
  "priority": "high",
  "content": {
    "type": "replacement-request",
    "message": "Replace failed agent with new instance",
    "failed_agent": "worker-test-billing-003",
    "replacement_config": {
      "session_name": "worker-test-billing-004",
      "role": "tester",
      "project": "billing-service",
      "plugins": ["emasoft-orchestrator-agent"],
      "directory": "/Users/dev/projects/billing-tests"
    },
    "transfer_tasks": ["review PR #42", "run integration tests"]
  }
}
```

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

**Message schema:**
```json
{
  "from": "chief-of-staff",
  "to": "<agent>",
  "subject": "Recovery Warning",
  "priority": "urgent",
  "content": {
    "type": "recovery-warning",
    "message": "You have been unresponsive for 3 minutes. Recovery will be attempted in 60 seconds.",
    "recovery_type": "soft_restart",
    "countdown_seconds": 60
  }
}
```

**When to send:**
- Before all RECOVERABLE actions
- At least 60 seconds before forced restart
- Allows agent to self-correct if possible

### 7.2 Notifying Orchestrator of Orphaned Tasks

**Purpose**: Prevent task loss when agent fails.

**Message schema:**
```json
{
  "from": "chief-of-staff",
  "to": "orchestrator-master",
  "subject": "Agent Failure - Tasks Need Reassignment",
  "priority": "urgent",
  "content": {
    "type": "failure-report",
    "message": "Agent worker-test-billing-003 has experienced TERMINAL failure.",
    "failed_agent": "worker-test-billing-003",
    "failure_classification": "TERMINAL",
    "failure_reason": "tmux session crashed",
    "orphaned_tasks": ["review PR #42", "run integration tests"],
    "recommended_action": "reassign_tasks"
  }
}
```

**When to send:**
- ALL TERMINAL failures
- RECOVERABLE failures where agent has assigned tasks

### 7.3 Escalating to Manager for Approval

**Purpose**: Get human approval for terminal recovery actions.

**Message schema:**
```json
{
  "from": "chief-of-staff",
  "to": "assistant-manager",
  "subject": "CRITICAL: Agent Terminal Failure",
  "priority": "urgent",
  "content": {
    "type": "critical-failure",
    "message": "Agent worker-test-billing-003 has experienced TERMINAL failure requiring approval.",
    "failed_agent": "worker-test-billing-003",
    "failure_classification": "TERMINAL",
    "failure_reason": "tmux session crashed, multiple recovery attempts failed",
    "recovery_attempts": 3,
    "orphaned_tasks": ["review PR #42", "run integration tests"],
    "recovery_options": [
      {"option": "replace", "description": "Terminate and spawn replacement agent"},
      {"option": "reassign_only", "description": "Reassign tasks to existing agents"},
      {"option": "investigate", "description": "Manual investigation required"}
    ],
    "awaiting": "approval"
  }
}
```

**When to send:**
- TERMINAL failures when `auto_replace_on_terminal: false`
- Repeated RECOVERABLE failures (3+ attempts)

### 7.4 Requesting Agent Replacement

**Purpose**: Execute approved terminal recovery.

**Message schema:**
```json
{
  "from": "chief-of-staff",
  "to": "ecos-lifecycle-manager",
  "subject": "Agent Replacement Request",
  "priority": "high",
  "content": {
    "type": "replacement-request",
    "message": "Replace failed agent with new instance",
    "failed_agent": "worker-test-billing-003",
    "replacement_config": {
      "session_name": "worker-test-billing-004",
      "role": "tester",
      "project": "billing-service",
      "plugins": ["emasoft-orchestrator-agent"],
      "directory": "/Users/dev/projects/billing-tests"
    },
    "transfer_tasks": ["review PR #42", "run integration tests"]
  }
}
```

**When to send:**
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
