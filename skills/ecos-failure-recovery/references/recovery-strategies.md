# Recovery Strategies for Agent Failures

## Table of Contents

- 3.1 When to use this document
- 3.2 Overview of recovery strategies
- 3.3 Strategy: Wait and Retry
  - 3.3.1 When to use wait and retry
  - 3.3.2 Implementation procedure
  - 3.3.3 Retry backoff schedule
  - 3.3.4 Success and failure criteria
- 3.4 Strategy: Restart Agent
  - 3.4.1 When to use restart
  - 3.4.2 Soft restart procedure
  - 3.4.3 Hard restart procedure
  - 3.4.4 Post-restart verification
- 3.5 Strategy: Hibernate-Wake Cycle
  - 3.5.1 When to use hibernate-wake
  - 3.5.2 Checking agent hibernation status
  - 3.5.3 Wake procedure
  - 3.5.4 Post-wake verification
- 3.6 Strategy: Resource Adjustment
  - 3.6.1 When to use resource adjustment
  - 3.6.2 Common resource issues and fixes
  - 3.6.3 Requesting resource changes
- 3.7 Strategy: Replace Agent
  - 3.7.1 When to proceed to replacement
  - 3.7.2 Pre-replacement checklist
  - 3.7.3 Initiating replacement protocol
- 3.8 Strategy selection flowchart

---

## 3.1 When to Use This Document

Use this document when:
- You have classified a failure as **recoverable** per `references/failure-classification.md`
- You need to select the appropriate recovery strategy
- You are executing a recovery procedure
- You need to verify recovery success

**IMPORTANT**: This document covers recovery strategies. If the failure is classified as **terminal**, skip to `references/agent-replacement-protocol.md`.

---

## 3.2 Overview of Recovery Strategies

ECOS employs five recovery strategies in order of escalating intervention:

| Strategy | Intervention Level | Time to Recovery | When to Use |
|----------|-------------------|------------------|-------------|
| Wait and Retry | None | 1-5 minutes | Transient failures |
| Restart Agent | Low | 5-15 minutes | Hung or crashed agent |
| Hibernate-Wake | Low | 2-5 minutes | Idle/hibernated session |
| Resource Adjustment | Medium | 15-60 minutes | Resource exhaustion |
| Replace Agent | High | 30-120 minutes | Unrecoverable state |

**Golden Rule**: Always try the least invasive strategy first. Each failed strategy provides information for the next attempt.

---

## 3.3 Strategy: Wait and Retry

### 3.3.1 When to Use Wait and Retry

Use this strategy when:
- Failure is classified as **transient**
- Agent has missed 1-2 heartbeats but status API shows "online" or "busy"
- Network issues are suspected (other agents also having brief issues)
- Agent is likely processing a complex request

**Do NOT use when:**
- Agent has been unresponsive for more than 5 minutes
- Status API shows agent as "offline"
- Agent process is confirmed dead

### 3.3.2 Implementation Procedure

1. **Log the wait decision:**
```bash
echo "{\"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"agent\": \"AGENT_NAME\", \"action\": \"wait_and_retry\", \"attempt\": 1}" >> $CLAUDE_PROJECT_DIR/.ecos/agent-health/recovery-log.jsonl
```

2. **Set a timer for the retry interval** (see backoff schedule below)

3. **Continue monitoring** - send periodic heartbeats at increased frequency

4. **Evaluate at each interval** - did agent respond?

### 3.3.3 Retry Backoff Schedule

| Attempt | Wait Duration | Total Elapsed | Next Action if No Recovery |
|---------|---------------|---------------|---------------------------|
| 1 | 30 seconds | 30 seconds | Retry |
| 2 | 60 seconds | 1.5 minutes | Retry |
| 3 | 120 seconds | 3.5 minutes | Retry |
| 4 | 60 seconds | 4.5 minutes | Escalate to Restart |

**Maximum wait time**: 5 minutes. After 4 failed attempts, escalate to Restart strategy.

### 3.3.4 Success and Failure Criteria

**Success**: Agent responds to heartbeat or message within the retry window.
```bash
# Log successful recovery
echo "{\"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"agent\": \"AGENT_NAME\", \"action\": \"wait_and_retry\", \"result\": \"success\", \"attempts\": 2, \"total_downtime\": \"90 seconds\"}" >> $CLAUDE_PROJECT_DIR/.ecos/agent-health/recovery-log.jsonl
```

**Failure**: No response after 4 attempts (5 minutes total).
```bash
# Log failed recovery, prepare for escalation
echo "{\"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"agent\": \"AGENT_NAME\", \"action\": \"wait_and_retry\", \"result\": \"failed\", \"attempts\": 4, \"escalating_to\": \"restart\"}" >> $CLAUDE_PROJECT_DIR/.ecos/agent-health/recovery-log.jsonl
```

---

## 3.4 Strategy: Restart Agent

### 3.4.1 When to Use Restart

Use this strategy when:
- Wait and Retry has failed
- Agent process exists but is unresponsive
- Agent is hung on a stuck operation
- Out-of-memory crash with recoverable state

**Do NOT use when:**
- Agent process does not exist (use Replace instead)
- Agent host is unreachable (cannot execute restart commands)
- Agent has corrupted working directory (use Replace instead)

### 3.4.2 Soft Restart Procedure

A soft restart sends a graceful termination signal and allows the agent to clean up before restarting.

**Step 1: Request graceful shutdown via AI Maestro**

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "AGENT_SESSION_NAME",
    "subject": "[SYSTEM] Graceful restart requested",
    "priority": "urgent",
    "content": {
      "type": "system-command",
      "message": "ECOS has detected you are unresponsive. Please save your state and restart. If you receive this message, acknowledge and restart within 2 minutes.",
      "command": "graceful_restart",
      "timeout_seconds": 120
    }
  }'
```

**Step 2: Wait 2 minutes for acknowledgment**

**Step 3: If no acknowledgment, proceed to hard restart**

### 3.4.3 Hard Restart Procedure

A hard restart forcefully terminates the agent process and starts a new one. Use only when soft restart fails.

**IMPORTANT**: Hard restart requires SSH access to the agent's host or coordination with the user who controls that host.

**Step 1: Notify manager about hard restart**

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eama-assistant-manager",
    "subject": "[ACTION] Hard restart required for agent",
    "priority": "high",
    "content": {
      "type": "action-notification",
      "message": "Soft restart failed for agent libs-svg-svgbbox. Initiating hard restart. The agent may lose unsaved work.",
      "agent": "libs-svg-svgbbox",
      "action": "hard_restart",
      "risk": "Unsaved work may be lost",
      "proceeding_in": "30 seconds"
    }
  }'
```

**Step 2: Request user to execute restart** (ECOS cannot directly control remote processes)

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "USER_OR_ADMIN_AGENT",
    "subject": "[USER ACTION REQUIRED] Restart agent process",
    "priority": "urgent",
    "content": {
      "type": "user-action-required",
      "message": "Please restart the Claude Code session for agent libs-svg-svgbbox. The session is unresponsive and cannot be recovered remotely.",
      "instructions": [
        "1. Find the terminal running libs-svg-svgbbox Claude Code session",
        "2. Press Ctrl+C to terminate the session",
        "3. Run: claude --resume (or start a new session)",
        "4. Verify the agent is responsive"
      ],
      "agent": "libs-svg-svgbbox",
      "urgency": "Please complete within 10 minutes"
    }
  }'
```

**Step 3: Wait for restart confirmation**

### 3.4.4 Post-Restart Verification

After restart (soft or hard), verify the agent is functional:

**Step 1: Wait 60 seconds for agent to initialize**

**Step 2: Send verification heartbeat**

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "AGENT_SESSION_NAME",
    "subject": "[VERIFICATION] Post-restart health check",
    "priority": "high",
    "content": {
      "type": "verification",
      "message": "Please confirm you are operational after restart. Respond with your current status and any issues.",
      "expected_response": "status_report",
      "timeout_seconds": 120
    }
  }'
```

**Step 3: Verify response and log result**

```bash
# Log successful restart
echo "{\"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"agent\": \"AGENT_NAME\", \"action\": \"restart\", \"type\": \"soft|hard\", \"result\": \"success\", \"downtime\": \"X minutes\"}" >> $CLAUDE_PROJECT_DIR/.ecos/agent-health/recovery-log.jsonl
```

---

## 3.5 Strategy: Hibernate-Wake Cycle

### 3.5.1 When to Use Hibernate-Wake

Use this strategy when:
- Agent's Claude Code session went idle and was suspended
- Terminal session was backgrounded or disconnected
- tmux/screen session detached
- SSH connection dropped but session persists

**Do NOT use when:**
- Agent process is confirmed dead
- Session was explicitly terminated (not hibernated)

### 3.5.2 Checking Agent Hibernation Status

**Step 1: Check AI Maestro for session status**

```bash
curl -s "http://localhost:23000/api/agents/AGENT_SESSION_NAME/status" | jq '.status'
```

Look for status values indicating hibernation:
- `"idle"` - Session exists but inactive
- `"suspended"` - Session explicitly suspended
- `"backgrounded"` - Terminal in background

**Step 2: Check if session exists on host** (if you have SSH access)

```bash
# Check for tmux session
ssh USER@HOST "tmux list-sessions | grep AGENT_SESSION_NAME"

# Check for screen session
ssh USER@HOST "screen -list | grep AGENT_SESSION_NAME"

# Check for Claude process
ssh USER@HOST "pgrep -f 'claude.*AGENT_SESSION_NAME'"
```

### 3.5.3 Wake Procedure

**For tmux sessions:**

```bash
# Request user to wake tmux session
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "USER_OR_ADMIN_AGENT",
    "subject": "[USER ACTION REQUIRED] Wake hibernated agent",
    "priority": "high",
    "content": {
      "type": "user-action-required",
      "message": "Agent libs-svg-svgbbox is hibernated in a tmux session. Please wake it.",
      "instructions": [
        "1. SSH to the host: ssh USER@HOST",
        "2. Attach to tmux: tmux attach -t SESSION_NAME",
        "3. The Claude session should resume automatically",
        "4. If not responsive, press Enter to wake it"
      ],
      "agent": "libs-svg-svgbbox"
    }
  }'
```

**For idle Claude sessions:**

Sometimes a Claude Code session goes idle due to inactivity. Sending a message may wake it:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "AGENT_SESSION_NAME",
    "subject": "[WAKE] Activity ping",
    "priority": "high",
    "content": {
      "type": "wake-ping",
      "message": "This is a wake-up ping. Please acknowledge if you are active.",
      "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
    }
  }'
```

### 3.5.4 Post-Wake Verification

Same as post-restart verification (see section 3.4.4).

---

## 3.6 Strategy: Resource Adjustment

### 3.6.1 When to Use Resource Adjustment

Use this strategy when:
- Agent crashed due to out-of-memory (OOM)
- Agent is throttled due to CPU limits
- Agent cannot write due to disk full
- Context window exceeded Claude's limits

**Do NOT use when:**
- The resource issue is on a remote host you cannot modify
- The resource issue is transient (will resolve itself)

### 3.6.2 Common Resource Issues and Fixes

| Issue | Symptoms | Fix |
|-------|----------|-----|
| Out of Memory | OOM killer in logs, agent terminated | Increase memory limit, reduce workload |
| CPU Throttled | Very slow responses, high latency | Reduce concurrent tasks, wait for other work to complete |
| Disk Full | Write errors, cannot save files | Clean up old files, request disk space |
| Context Exceeded | Agent cannot process messages | Compact context, start fresh task |

### 3.6.3 Requesting Resource Changes

ECOS cannot directly modify system resources. Request changes via manager:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eama-assistant-manager",
    "subject": "[RESOURCE REQUEST] Agent needs more resources",
    "priority": "high",
    "content": {
      "type": "resource-request",
      "message": "Agent libs-svg-svgbbox crashed due to insufficient memory. Requesting memory increase to allow recovery.",
      "agent": "libs-svg-svgbbox",
      "resource_issue": "out_of_memory",
      "current_allocation": "4GB RAM",
      "requested_allocation": "8GB RAM",
      "justification": "Processing large SVG files requires more memory",
      "alternative": "Reduce batch size from 100 to 20 files"
    }
  }'
```

---

## 3.7 Strategy: Replace Agent

### 3.7.1 When to Proceed to Replacement

Proceed to replacement when:
- All other recovery strategies have failed
- Agent is classified as **terminal** failure
- Recovery would take longer than replacement
- Manager approves replacement

### 3.7.2 Pre-Replacement Checklist

Before initiating replacement, verify:

- [ ] Recovery attempts exhausted (document all attempts)
- [ ] Manager (EAMA) notified and approved
- [ ] Recoverable artifacts identified (git commits, logs, partial work)
- [ ] Replacement host available
- [ ] Task handoff documentation prepared (or will be generated)
- [ ] GitHub Project updated with agent status

### 3.7.3 Initiating Replacement Protocol

See `references/agent-replacement-protocol.md` for the complete replacement workflow.

**Short version:**

```bash
# Request replacement from manager
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eama-assistant-manager",
    "subject": "[REPLACEMENT] Recovery failed, replacement required",
    "priority": "urgent",
    "content": {
      "type": "replacement-request",
      "message": "All recovery strategies have failed for agent libs-svg-svgbbox. Requesting approval to proceed with replacement.",
      "agent": "libs-svg-svgbbox",
      "recovery_attempts": [
        {"strategy": "wait_and_retry", "result": "failed", "attempts": 4},
        {"strategy": "restart_soft", "result": "failed", "reason": "no acknowledgment"},
        {"strategy": "restart_hard", "result": "failed", "reason": "process not found"}
      ],
      "recommendation": "replace",
      "awaiting_approval": true
    }
  }'
```

---

## 3.8 Strategy Selection Flowchart

```
START: Recoverable failure detected
    |
    v
[How long has agent been unresponsive?]
    |
    |-- Less than 5 minutes --> [WAIT AND RETRY]
    |                                |
    |                                v
    |                           [Recovered?]
    |                            |       |
    |                            | No    | Yes --> END (success)
    |                            v
    |                       [Escalate to RESTART]
    |
    |-- 5-15 minutes --> [Check session status]
    |                         |
    |                         |-- "idle"/"suspended" --> [HIBERNATE-WAKE]
    |                         |                               |
    |                         |                               v
    |                         |                          [Recovered?]
    |                         |                           |       |
    |                         |                           | No    | Yes --> END
    |                         |                           v
    |                         |                      [Escalate to RESTART]
    |                         |
    |                         |-- "offline" --> [RESTART]
    |                                               |
    |                                               v
    |                                          [Recovered?]
    |                                           |       |
    |                                           | No    | Yes --> END
    |                                           v
    |                                      [Check for resource issues]
    |                                           |
    |                                           |-- Yes --> [RESOURCE ADJUSTMENT]
    |                                           |                   |
    |                                           |                   v
    |                                           |              [Recovered?]
    |                                           |               |       |
    |                                           |               | No    | Yes --> END
    |                                           |               v
    |                                           |          [Escalate to REPLACE]
    |                                           |
    |                                           |-- No --> [Escalate to REPLACE]
    |
    |-- More than 15 minutes --> [RESTART immediately]
                                      |
                                      v
                                 [Follow RESTART path above]
```

---

## Troubleshooting

### Soft restart never receives acknowledgment

**Symptom**: Soft restart message sent, but agent never acknowledges.

**Cause**: Agent's message polling hook may be disabled or the agent is truly unresponsive.

**Solution**:
1. Check AI Maestro message queue - is the message delivered?
2. If delivered but not acknowledged, agent is unresponsive
3. Proceed to hard restart

### Hard restart fails because process not found

**Symptom**: Cannot restart because there is no process to restart.

**Cause**: Agent process already terminated, this is likely a terminal failure.

**Solution**:
1. Reclassify as terminal failure
2. Proceed to replacement protocol

### Wake succeeds but agent immediately goes back to sleep

**Symptom**: Agent responds after wake, then becomes unresponsive again within minutes.

**Cause**: Underlying issue causing hibernation not resolved (user closed terminal, session manager policy, etc.)

**Solution**:
1. Investigate why session keeps hibernating
2. Request user to keep terminal active
3. Consider setting up a keep-alive mechanism
4. If persistent, may need to move agent to a different host

### Resource adjustment denied by manager

**Symptom**: Manager rejects resource increase request.

**Cause**: Resource constraints on the system, budget limitations, or alternative solutions preferred.

**Solution**:
1. Implement the alternative suggested by manager (e.g., reduce workload)
2. If no alternative viable, discuss with manager
3. May need to accept degraded performance or split tasks across multiple agents
