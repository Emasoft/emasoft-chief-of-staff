# Examples: Failure Recovery Scenarios

## Table of Contents

- [Example 1: Agent Crash Recovery](#example-1-agent-crash-recovery)
- [Example 2: Terminal Failure with Replacement](#example-2-terminal-failure-with-replacement)
- [Example 3: Transient Network Failure](#example-3-transient-network-failure)
- [Example 4: Emergency Handoff with Deadline](#example-4-emergency-handoff-with-deadline)
- [Quick Reference](#quick-reference)

## Use-Case TOC

- When recovering from a simple agent crash -> [Example 1: Agent Crash Recovery](#example-1-agent-crash-recovery)
- When agent fails repeatedly and needs replacement -> [Example 2: Terminal Failure with Replacement](#example-2-terminal-failure-with-replacement)
- When network hiccup causes temporary unresponsiveness -> [Example 3: Transient Network Failure](#example-3-transient-network-failure)
- When critical deadline is at risk -> [Example 4: Emergency Handoff with Deadline](#example-4-emergency-handoff-with-deadline)
- When you need common message patterns -> [Quick Reference](#quick-reference)

---

## Example 1: Agent Crash Recovery

**Scenario**: Agent `svgbbox-impl-01` becomes unresponsive after 5-minute heartbeat timeout.

**Classification**: Recoverable (no explicit crash signal, process may still exist)

**Recovery steps**:
1. Heartbeat monitor detects `svgbbox-impl-01` unresponsive (5 min timeout)
2. Classify as recoverable (no explicit crash signal)
3. Send restart command via tmux
4. Wait for agent to re-register in AI Maestro
5. Verify agent received pending messages
6. Report recovery to EAMA

**Detailed procedure**:

- **Step 1**: Use the `ai-maestro-agents-management` skill to check agent `svgbbox-impl-01` status. Expected: "offline" or "unknown"
- **Step 3**: Send restart command via tmux session (exit and relaunch Claude Code)
- **Step 4**: Wait 60 seconds, then use the `ai-maestro-agents-management` skill to verify agent status is "online"
- **Step 5**: Use the `agent-messaging` skill to check for pending messages for agent `svgbbox-impl-01`. Expected: 0 pending
- **Step 6**: Use the `agent-messaging` skill to report recovery to EAMA:
  - **Recipient**: `eama-assistant-manager`
  - **Subject**: `[RESOLVED] Agent svgbbox-impl-01 recovered`
  - **Priority**: `normal`
  - **Content**: type `recovery-report`, message: "Agent svgbbox-impl-01 recovered via restart. No data loss.", including agent name, recovery method "restart", and downtime in minutes

---

## Example 2: Terminal Failure with Replacement

**Scenario**: Agent `feature-impl-03` crashes 3 times in 10 minutes.

**Classification**: Terminal (repeated crashes indicate unrecoverable state)

**Replacement protocol**:
1. Agent crashes 3 times in 10 minutes
2. Classify as terminal failure
3. Request replacement from EAMA with urgency
4. Receive approval
5. Create new agent with same role and task
6. Handoff work context from failed agent's state backup
7. Verify new agent is operational
8. Archive failed agent records

**Detailed procedure**:

- **Step 2**: Log terminal classification to incident log
- **Step 3**: Use the `agent-messaging` skill to request replacement approval:
  - **Recipient**: `eama-assistant-manager`
  - **Subject**: `[APPROVAL REQUIRED] Agent replacement: feature-impl-03`
  - **Priority**: `urgent`
  - **Content**: type `replacement-approval-request`, message explaining the agent crashed 3 times in 10 minutes, including agent name, failure type "terminal", crash count, time window, and awaiting approval flag
- **Step 5**: After approval, use the `agent-messaging` skill to notify the orchestrator:
  - **Recipient**: `eoa-orchestrator`
  - **Subject**: `[HANDOFF] Replacement agent created: feature-impl-04`
  - **Priority**: `high`
  - **Content**: type `replacement-notification`, message requesting handoff documentation and task reassignment, including old and new agent names
- **Step 7**: Use the `ai-maestro-agents-management` skill to verify new agent `feature-impl-04` status is "online"

---

## Example 3: Transient Network Failure

**Scenario**: Agent `api-impl-02` misses one heartbeat due to network hiccup.

**Classification**: Transient (single missed heartbeat, likely auto-recovers)

**Response**:
1. Single heartbeat missed
2. Classify as transient (< 5 minute threshold)
3. Wait for auto-recovery
4. Next heartbeat succeeds
5. Resume normal monitoring

**Detailed procedure**:

- **Step 1**: Heartbeat system logs: "api-impl-02 heartbeat missed at HH:MM:SS"
- **Step 3**: Wait 60 seconds (no action required for transient failures)
- **Step 4**: Use the `ai-maestro-agents-management` skill to verify agent `api-impl-02` status is "online"
- No escalation needed for transient failures

---

## Example 4: Emergency Handoff with Deadline

**Scenario**: Agent `release-prep-01` fails 90 minutes before critical release deadline.

**Classification**: Terminal (cannot risk recovery attempts with tight deadline)

**Emergency handoff**:
1. Failure detected 90 minutes before deadline
2. Classify as terminal (no time for recovery attempts)
3. Initiate emergency handoff
4. Notify orchestrator for immediate reassignment
5. Transfer critical tasks to available agent
6. Monitor new agent progress
7. Deadline met

**Detailed procedure**:

- **Step 3**: Use the `agent-messaging` skill to initiate emergency handoff:
  - **Recipient**: `eoa-orchestrator`
  - **Subject**: `[EMERGENCY] Critical handoff - 90 minutes to deadline`
  - **Priority**: `urgent`
  - **Content**: type `emergency-handoff-request`, message explaining the failure and deadline urgency, including the failed agent name, deadline timestamp, list of critical tasks with IDs and estimated minutes, and action requested "immediate_reassignment"
- **Step 4**: Use the `agent-messaging` skill to notify the manager:
  - **Recipient**: `eama-assistant-manager`
  - **Subject**: `[EMERGENCY] Agent failure - critical deadline at risk`
  - **Priority**: `urgent`
  - **Content**: type `emergency-notification`, message explaining the failure and initiated handoff, including failed agent name and deadline-at-risk flag

---

## Quick Reference

### Heartbeat Ping

Use the `agent-messaging` skill to send a heartbeat:
- **Recipient**: the target agent session name
- **Subject**: `[HEARTBEAT] Health check`
- **Priority**: `low`
- **Content**: type `heartbeat`, message: "ping"

**Verify**: confirm message delivery via the `agent-messaging` skill's sent messages feature.

### Check Agent Status

Use the `ai-maestro-agents-management` skill to check the target agent's status.

### Soft Restart Request

Use the `agent-messaging` skill to request a graceful restart:
- **Recipient**: the target agent session name
- **Subject**: `[SYSTEM] Graceful restart requested`
- **Priority**: `urgent`
- **Content**: type `system-command`, message: "Please save state and restart within 2 minutes.", command: "graceful_restart"

### Replacement Approval Request

Use the `agent-messaging` skill to request replacement approval:
- **Recipient**: `eama-assistant-manager`
- **Subject**: `[APPROVAL REQUIRED] Agent replacement request`
- **Priority**: `urgent`
- **Content**: type `replacement-approval-request`, message explaining the terminal failure, including agent name, failure type, and awaiting approval flag

### Emergency Handoff Request

Use the `agent-messaging` skill to request emergency handoff:
- **Recipient**: `eoa-orchestrator`
- **Subject**: `[EMERGENCY] Work handoff required`
- **Priority**: `urgent`
- **Content**: type `emergency-handoff-request`, message explaining the failure and deadline urgency, including failed agent name, critical tasks list, and action requested "reassign_critical_tasks"
