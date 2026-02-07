# Failure Classification for Remote Agents

## Table of Contents

- 2.1 When to use this document
- 2.2 Overview of failure categories
- 2.3 Transient failures
  - 2.3.1 Definition and characteristics
  - 2.3.2 Examples of transient failures
  - 2.3.3 Expected recovery time
  - 2.3.4 Recommended response
- 2.4 Recoverable failures
  - 2.4.1 Definition and characteristics
  - 2.4.2 Examples of recoverable failures
  - 2.4.3 Expected recovery time
  - 2.4.4 Recommended response
- 2.5 Terminal failures
  - 2.5.1 Definition and characteristics
  - 2.5.2 Examples of terminal failures
  - 2.5.3 When replacement is required
  - 2.5.4 Recommended response
- 2.6 Classification decision matrix
- 2.7 Escalation thresholds
- 2.8 Recording failure events

---

## 2.1 When to Use This Document

Use this document when:
- You have detected an agent failure using the methods in `references/failure-detection.md`
- You need to determine the severity of the failure
- You need to decide whether to attempt recovery or proceed to replacement
- You are documenting a failure for the incident log

---

## 2.2 Overview of Failure Categories

ECOS classifies all agent failures into three categories based on severity and recoverability:

| Category | Severity | Recovery Possible | Typical Response |
|----------|----------|-------------------|------------------|
| **Transient** | Low | Yes, automatic | Wait and retry |
| **Recoverable** | Medium | Yes, with intervention | Restart or wake |
| **Terminal** | High | No | Replace agent |

**CRITICAL**: Correct classification is essential. Misclassifying a transient failure as terminal wastes resources. Misclassifying a terminal failure as transient delays recovery and blocks work.

---

## 2.3 Transient Failures

### 2.3.1 Definition and Characteristics

A **transient failure** is a temporary disruption that resolves itself without intervention. The agent remains fundamentally healthy but experiences a brief interruption in communication or processing.

**Key characteristics:**
- Duration: Less than 5 minutes
- Pattern: Isolated incident, not recurring
- Agent state: Preserved (no memory loss, no context loss)
- External cause: Network glitch, temporary server load, brief API timeout

### 2.3.2 Examples of Transient Failures

| Failure | Symptoms | Typical Duration |
|---------|----------|------------------|
| Network hiccup | 1-2 missed heartbeats, then recovery | 30-60 seconds |
| AI Maestro server restart | All agents briefly unreachable | 1-2 minutes |
| API rate limiting | Message delivery delayed | 1-5 minutes |
| High system load | Slow heartbeat responses | Variable |
| Context switching delay | Agent slow after long thinking block | 1-3 minutes |

### 2.3.3 Expected Recovery Time

Transient failures should resolve within **5 minutes** without intervention. If the failure persists beyond 5 minutes, reclassify as **recoverable**.

### 2.3.4 Recommended Response

1. **Do not escalate immediately** - wait for automatic recovery
2. **Continue monitoring** - increase heartbeat frequency temporarily
3. **Log the incident** for pattern analysis
4. **Resume normal operations** once agent responds

**Response action - wait and monitor:**

```bash
# Log the transient failure
echo "{\"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"agent\": \"AGENT_NAME\", \"type\": \"transient\", \"symptoms\": \"missed_heartbeat\", \"resolved\": false}" >> $CLAUDE_PROJECT_DIR/.ecos/agent-health/incident-log.jsonl

# Increase monitoring frequency for next 10 minutes
# (Handled by ECOS scheduler - no manual action needed)
```

---

## 2.4 Recoverable Failures

### 2.4.1 Definition and Characteristics

A **recoverable failure** is a disruption that requires intervention but does not require replacing the agent. The agent can be restored to a working state through restart, wake-up, or reconfiguration.

**Key characteristics:**
- Duration: 5 minutes to 2 hours
- Pattern: May be recurring if underlying cause not addressed
- Agent state: May be partially preserved (context may be intact if session is suspended)
- Intervention required: Manual restart, wake from hibernate, resource adjustment

### 2.4.2 Examples of Recoverable Failures

| Failure | Symptoms | Recovery Method |
|---------|----------|-----------------|
| Session hibernation | Agent unresponsive, session marked "idle" | Wake via terminal command |
| Out of memory | Agent crashed, error in logs | Restart with more memory |
| Infinite loop/hang | Agent responsive but task stuck | Send interrupt, restart task |
| Dependency failure | Agent cannot reach external service | Wait for service, retry |
| User terminal closed | Agent process orphaned | Reconnect terminal session |
| Context window exceeded | Agent cannot process new input | Compact context, restart |

### 2.4.3 Expected Recovery Time

Recoverable failures should be resolved within **2 hours** with appropriate intervention. If recovery attempts fail after 2 hours, reclassify as **terminal**.

### 2.4.4 Recommended Response

1. **Diagnose the specific cause** before attempting recovery
2. **Notify the manager (EAMA)** about the failure and planned recovery action
3. **Attempt recovery** using the appropriate strategy from `references/recovery-strategies.md`
4. **Verify agent functionality** after recovery
5. **Update incident log** with resolution details

**Response action - notify and recover:**

Use the `agent-messaging` skill to send:
- **Recipient**: `eama-assistant-manager`
- **Subject**: `[AGENT FAILURE] Recoverable failure detected`
- **Priority**: `high`
- **Content**: type `failure-report`, message: "Agent libs-svg-svgbbox has experienced a recoverable failure (session hibernated). Attempting wake recovery. Will report result in 10 minutes." Include `agent`: "libs-svg-svgbbox", `failure_type`: "recoverable", `failure_cause`: "session_hibernated", `planned_action`: "wake_via_terminal", `expected_recovery_time`: "10 minutes".

---

## 2.5 Terminal Failures

### 2.5.1 Definition and Characteristics

A **terminal failure** is a catastrophic disruption from which the agent cannot recover. The agent's state is lost, corrupted, or otherwise unrecoverable. The only option is to replace the agent with a new instance.

**Key characteristics:**
- Duration: Permanent (agent will not recover)
- Pattern: May follow repeated recoverable failures
- Agent state: Lost (no memory, no context, no work in progress)
- Replacement required: New agent must be created and onboarded

### 2.5.2 Examples of Terminal Failures

| Failure | Symptoms | Why Terminal |
|---------|----------|--------------|
| Host machine crash | Agent unreachable, no logs | Process terminated, state lost |
| Disk corruption | Agent cannot read/write files | Working directory corrupted |
| Authentication revoked | Agent cannot authenticate to APIs | Cannot be re-authenticated |
| Agent process killed | Abrupt termination, no cleanup | State not persisted |
| Unrecoverable context corruption | Agent produces nonsense output | Context window corrupted |
| Repeated recovery failures | 3+ failed recovery attempts | Underlying issue unresolvable |

### 2.5.3 When Replacement is Required

**Replace the agent if ANY of the following are true:**
- Agent process no longer exists and cannot be restarted
- Agent's working directory is corrupted or deleted
- Agent's authentication credentials are invalid
- Three consecutive recovery attempts have failed
- Agent is producing corrupted or unsafe output
- Manager (EAMA) explicitly orders replacement

### 2.5.4 Recommended Response

1. **Confirm terminal status** - ensure recovery is truly impossible
2. **Notify the manager (EAMA)** immediately with failure details
3. **Request replacement approval** from manager
4. **Preserve any recoverable artifacts** (logs, partial work, git commits)
5. **Initiate replacement protocol** per `references/agent-replacement-protocol.md`
6. **Document the incident** for post-mortem analysis

**Response action - request replacement:**

Use the `agent-messaging` skill to send:
- **Recipient**: `eama-assistant-manager`
- **Subject**: `[CRITICAL] Terminal failure - replacement required`
- **Priority**: `urgent`
- **Content**: type `replacement-request`, message: "Agent libs-svg-svgbbox has experienced a terminal failure and cannot be recovered. Host machine crashed and agent state is lost. Requesting approval to create replacement agent. Estimated replacement time: 30 minutes." Include `agent`: "libs-svg-svgbbox", `failure_type`: "terminal", `failure_cause`: "host_machine_crash", `recovery_attempts`: 0, `recoverable_artifacts`: ["git commits up to abc123", "logs at /var/log/agent-libs-svg.log"], `replacement_cost`: { `time_to_replace`: "30 minutes", `work_to_redo`: "2-3 hours of uncommitted work" }, `awaiting_approval`: true.

---

## 2.6 Classification Decision Matrix

Use this matrix to classify a detected failure:

```
START: Failure detected
    |
    v
[Has agent responded to any probe in last 5 minutes?]
    |                   |
    | No                | Yes
    v                   v
[Check AI Maestro      [TRANSIENT - wait and monitor]
 agent status]              |
    |                       v
    v                      END
[Agent status == "online"?]
    |           |
    | No        | Yes (online but not responding)
    v           v
[Can agent     [Agent likely hung or overloaded]
 process be        |
 found?]           v
    |          [Send interrupt signal]
    |               |
    | No            v
    v          [Agent responds within 2 min?]
[TERMINAL -         |           |
 agent process      | No        | Yes
 gone]              v           v
    |          [RECOVERABLE -  [TRANSIENT -
    v           needs restart]  was just slow]
[Proceed to         |              |
 replacement]       v              v
                [Proceed to       END
                 recovery]
```

**Quick classification guide:**

| Symptom Combination | Classification |
|---------------------|----------------|
| 1-2 missed heartbeats, then recovers | Transient |
| Agent offline, session exists, can wake | Recoverable |
| Agent offline, process exists, can restart | Recoverable |
| Agent offline, process gone, host alive | Terminal |
| Agent offline, host unreachable | Terminal |
| 3+ failed recovery attempts | Terminal |

---

## 2.7 Escalation Thresholds

ECOS uses these thresholds to determine when to escalate to manager (EAMA):

| Failure Type | Escalation Trigger | Notification Priority |
|--------------|-------------------|----------------------|
| Transient | 3+ transient failures within 1 hour | `normal` |
| Recoverable | Immediately upon classification | `high` |
| Terminal | Immediately upon classification | `urgent` |

**Escalation message to manager:**

Use the `agent-messaging` skill to send:
- **Recipient**: `eama-assistant-manager`
- **Subject**: `[ESCALATION] Agent failure requires attention`
- **Priority**: appropriate level (`normal`, `high`, or `urgent`)
- **Content**: type `escalation`, message: description of the situation. Include `agent` (session name), `failure_type` ("transient", "recoverable", or "terminal"), `failure_details` with `first_detected` (ISO timestamp), `symptom` (what was observed), `diagnosis` (what ECOS determined), `recommended_action` (what ECOS proposes), `awaiting_approval` (true/false).

---

## 2.8 Recording Failure Events

All failures MUST be recorded in the incident log for pattern analysis and post-mortem review.

**Incident log location:**
```
$CLAUDE_PROJECT_DIR/.ecos/agent-health/incident-log.jsonl
```

**Incident record format:**

```json
{
  "incident_id": "inc-20250115-001",
  "timestamp": "2025-01-15T10:30:00Z",
  "agent": "libs-svg-svgbbox",
  "failure_type": "recoverable",
  "failure_cause": "session_hibernated",
  "detection_method": "heartbeat_timeout",
  "symptoms": ["3 missed heartbeats", "status API shows idle"],
  "classification_reasoning": "Agent session exists but unresponsive, wake should restore",
  "recovery_action": "wake_via_terminal",
  "recovery_result": "success",
  "time_to_recovery": "5 minutes",
  "escalated_to": "eama-assistant-manager",
  "notes": "User had closed terminal, session went idle"
}
```

**Recording a new incident:**

```bash
# Append incident to log
echo '{
  "incident_id": "inc-'$(date +%Y%m%d-%H%M%S)'",
  "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",
  "agent": "AGENT_NAME",
  "failure_type": "TYPE",
  "failure_cause": "CAUSE",
  "detection_method": "METHOD",
  "symptoms": ["SYMPTOM1", "SYMPTOM2"],
  "classification_reasoning": "WHY_THIS_CLASSIFICATION",
  "recovery_action": "PLANNED_ACTION",
  "recovery_result": "pending",
  "time_to_recovery": null,
  "escalated_to": null,
  "notes": ""
}' >> $CLAUDE_PROJECT_DIR/.ecos/agent-health/incident-log.jsonl
```

---

## Troubleshooting

### Cannot determine if failure is recoverable or terminal

**Symptom**: Agent is offline and you cannot tell if it can be restarted.

**Solution**:
1. Check if the host machine is reachable: `ping HOSTNAME`
2. Check if you can SSH to the host: `ssh USER@HOSTNAME`
3. Check if the agent process exists: `ssh USER@HOSTNAME "pgrep -f 'claude'"`
4. If host unreachable: **Terminal**
5. If host reachable but process gone: **Terminal** (unless session manager can restore)
6. If process exists but unresponsive: **Recoverable** (try restart)

### Repeated transient failures suggesting underlying issue

**Symptom**: Same agent has 5+ transient failures in a day, but always recovers.

**Solution**:
1. Reclassify as **pattern of concern** even if individual failures are transient
2. Escalate to manager with the pattern information
3. Investigate root cause (network stability, resource constraints, etc.)
4. Consider preemptive restart during low-activity period

### Manager unresponsive during terminal failure

**Symptom**: Terminal failure detected but manager (EAMA) does not respond to replacement request.

**Solution**:
1. Wait 15 minutes for manager response
2. If no response, escalate to user directly (if configured)
3. If user unavailable, log the pending replacement and continue monitoring
4. Do NOT proceed with replacement without approval - the manager may have context that affects the decision
