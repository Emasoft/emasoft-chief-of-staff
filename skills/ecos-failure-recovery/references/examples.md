# Examples: Failure Recovery Scenarios

## Table of Contents

- [Example 1: Agent Crash Recovery](#example-1-agent-crash-recovery)
- [Example 2: Terminal Failure with Replacement](#example-2-terminal-failure-with-replacement)
- [Example 3: Transient Network Failure](#example-3-transient-network-failure)
- [Example 4: Emergency Handoff with Deadline](#example-4-emergency-handoff-with-deadline)
- [Quick Command Reference](#quick-command-reference)

## Use-Case TOC

- When recovering from a simple agent crash -> [Example 1: Agent Crash Recovery](#example-1-agent-crash-recovery)
- When agent fails repeatedly and needs replacement -> [Example 2: Terminal Failure with Replacement](#example-2-terminal-failure-with-replacement)
- When network hiccup causes temporary unresponsiveness -> [Example 3: Transient Network Failure](#example-3-transient-network-failure)
- When critical deadline is at risk -> [Example 4: Emergency Handoff with Deadline](#example-4-emergency-handoff-with-deadline)
- When you need common curl commands -> [Quick Command Reference](#quick-command-reference)

---

## Example 1: Agent Crash Recovery

**Scenario**: Agent `svgbbox-impl-01` becomes unresponsive after 5-minute heartbeat timeout.

**Classification**: Recoverable (no explicit crash signal, process may still exist)

**Recovery steps**:
```
1. Heartbeat monitor detects svgbbox-impl-01 unresponsive (5 min timeout)
2. Classify as recoverable (no explicit crash signal)
3. Send restart command via tmux
4. Wait for agent to re-register in AI Maestro
5. Verify agent received pending messages
6. Report recovery to EAMA
```

**Commands used**:
```bash
# Step 1: Verify agent status
curl -s "http://localhost:23000/api/agents/svgbbox-impl-01/status" | jq '.status'
# Expected: "offline" or "unknown"

# Step 3: Send restart command (if tmux session exists)
tmux send-keys -t svgbbox-impl-01 "exit" Enter
# Wait 5 seconds
tmux send-keys -t svgbbox-impl-01 "claude" Enter

# Step 4: Wait and verify re-registration
sleep 60
curl -s "http://localhost:23000/api/agents/svgbbox-impl-01/status" | jq '.status'
# Expected: "online"

# Step 5: Verify pending messages delivered
curl -s "http://localhost:23000/api/messages?agent=svgbbox-impl-01&status=pending" | jq '.count'
# Expected: 0

# Step 6: Report to EAMA
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eama-assistant-manager",
    "subject": "[RESOLVED] Agent svgbbox-impl-01 recovered",
    "priority": "normal",
    "content": {
      "type": "recovery-report",
      "message": "Agent svgbbox-impl-01 recovered via restart. No data loss.",
      "agent": "svgbbox-impl-01",
      "recovery_method": "restart",
      "downtime_minutes": 7
    }
  }'
```

---

## Example 2: Terminal Failure with Replacement

**Scenario**: Agent `feature-impl-03` crashes 3 times in 10 minutes.

**Classification**: Terminal (repeated crashes indicate unrecoverable state)

**Replacement protocol**:
```
1. Agent crashes 3 times in 10 minutes
2. Classify as terminal failure
3. Request replacement from EAMA with urgency
4. Receive approval
5. Create new agent with same role and task
6. Handoff work context from failed agent's state backup
7. Verify new agent is operational
8. Archive failed agent records
```

**Commands used**:
```bash
# Step 2: Log terminal classification
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","agent":"feature-impl-03","classification":"terminal","reason":"3 crashes in 10 minutes"}' >> $CLAUDE_PROJECT_DIR/.ecos/agent-health/incident-log.jsonl

# Step 3: Request replacement approval
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eama-assistant-manager",
    "subject": "[APPROVAL REQUIRED] Agent replacement: feature-impl-03",
    "priority": "urgent",
    "content": {
      "type": "replacement-approval-request",
      "message": "Agent feature-impl-03 crashed 3 times in 10 minutes. Terminal failure. Requesting replacement approval.",
      "agent": "feature-impl-03",
      "failure_type": "terminal",
      "crash_count": 3,
      "time_window_minutes": 10,
      "awaiting_approval": true
    }
  }'

# Step 5: After approval, notify orchestrator for handoff
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eoa-orchestrator",
    "subject": "[HANDOFF] Replacement agent created: feature-impl-04",
    "priority": "high",
    "content": {
      "type": "replacement-notification",
      "message": "New agent feature-impl-04 created to replace failed feature-impl-03. Please generate handoff documentation and reassign tasks.",
      "old_agent": "feature-impl-03",
      "new_agent": "feature-impl-04",
      "action_requested": "generate_handoff_and_reassign"
    }
  }'

# Step 7: Verify new agent operational
curl -s "http://localhost:23000/api/agents/feature-impl-04/status" | jq '.status'
# Expected: "online"
```

---

## Example 3: Transient Network Failure

**Scenario**: Agent `api-impl-02` misses one heartbeat due to network hiccup.

**Classification**: Transient (single missed heartbeat, likely auto-recovers)

**Response**:
```
1. Single heartbeat missed
2. Classify as transient (< 5 minute threshold)
3. Wait for auto-recovery
4. Next heartbeat succeeds
5. Resume normal monitoring
```

**Commands used**:
```bash
# Step 1: Note missed heartbeat (internal monitoring)
# Heartbeat system logs: "api-impl-02 heartbeat missed at HH:MM:SS"

# Step 3: Wait (no action required for transient)
sleep 60

# Step 4: Verify recovery
curl -s "http://localhost:23000/api/agents/api-impl-02/status" | jq '.status'
# Expected: "online"

# No escalation needed for transient failures
```

---

## Example 4: Emergency Handoff with Deadline

**Scenario**: Agent `release-prep-01` fails 90 minutes before critical release deadline.

**Classification**: Terminal (cannot risk recovery attempts with tight deadline)

**Emergency handoff**:
```
1. Failure detected 90 minutes before deadline
2. Classify as terminal (no time for recovery attempts)
3. Initiate emergency handoff
4. Notify orchestrator for immediate reassignment
5. Transfer critical tasks to available agent
6. Monitor new agent progress
7. Deadline met
```

**Commands used**:
```bash
# Step 3: Initiate emergency handoff
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eoa-orchestrator",
    "subject": "[EMERGENCY] Critical handoff - 90 minutes to deadline",
    "priority": "urgent",
    "content": {
      "type": "emergency-handoff-request",
      "message": "Agent release-prep-01 failed. Release deadline in 90 minutes. Need IMMEDIATE task reassignment.",
      "failed_agent": "release-prep-01",
      "deadline": "2025-01-15T14:00:00Z",
      "critical_tasks": [
        {"task_id": "release-notes", "estimated_minutes": 30},
        {"task_id": "version-bump", "estimated_minutes": 15},
        {"task_id": "tag-release", "estimated_minutes": 10}
      ],
      "action_requested": "immediate_reassignment"
    }
  }'

# Step 4: Notify manager
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eama-assistant-manager",
    "subject": "[EMERGENCY] Agent failure - critical deadline at risk",
    "priority": "urgent",
    "content": {
      "type": "emergency-notification",
      "message": "Agent release-prep-01 failed. Release deadline in 90 minutes. Emergency handoff initiated.",
      "failed_agent": "release-prep-01",
      "deadline_at_risk": true
    }
  }'
```

---

## Quick Command Reference

### Heartbeat Ping
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "TARGET_AGENT",
    "subject": "[HEARTBEAT] Health check",
    "priority": "low",
    "content": {"type": "heartbeat", "message": "ping"}
  }'
```

### Check Agent Status
```bash
curl -s "http://localhost:23000/api/agents/TARGET_AGENT/status" | jq '.status'
```

### Soft Restart Request
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "AGENT_NAME",
    "subject": "[SYSTEM] Graceful restart requested",
    "priority": "urgent",
    "content": {
      "type": "system-command",
      "message": "Please save state and restart within 2 minutes.",
      "command": "graceful_restart"
    }
  }'
```

### Replacement Approval Request
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
      "message": "Agent AGENT_NAME requires replacement. Terminal failure confirmed.",
      "agent": "AGENT_NAME",
      "failure_type": "terminal",
      "awaiting_approval": true
    }
  }'
```

### Emergency Handoff Request
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eoa-orchestrator",
    "subject": "[EMERGENCY] Work handoff required",
    "priority": "urgent",
    "content": {
      "type": "emergency-handoff-request",
      "message": "Agent failed, critical deadline approaching. Need immediate reassignment.",
      "failed_agent": "AGENT_NAME",
      "critical_tasks": [{"task_id": "task-001", "deadline": "YYYY-MM-DDTHH:MM:SSZ"}],
      "action_requested": "reassign_critical_tasks"
    }
  }'
```
