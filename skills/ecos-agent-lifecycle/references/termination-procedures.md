# Termination Procedures Reference

## Table of Contents

- 2.1 What is agent termination - Understanding clean shutdown
- 2.2 When to terminate agents - Termination triggers
  - 2.2.1 Task completion - Work finished
  - 2.2.2 Error conditions - Unrecoverable failures
  - 2.2.3 Resource reclamation - Freeing capacity
  - 2.2.4 User request - Manual termination
- 2.3 Termination procedure - Step-by-step shutdown
  - 2.3.1 Work verification - Ensuring completion
  - 2.3.2 State preservation - Saving final state
  - 2.3.3 Termination signal - Sending shutdown command
  - 2.3.4 Confirmation await - Waiting for acknowledgment
  - 2.3.5 Registry cleanup - Removing agent record
- 2.4 Graceful vs forced termination - Choosing termination type
- 2.5 Post-termination validation - Verifying cleanup
- 2.6 Examples - Termination scenarios
- 2.7 Troubleshooting - Termination issues

---

## 2.1 What is agent termination

Agent termination is the process of cleanly shutting down an agent instance. Proper termination:

1. Ensures all work is saved
2. Preserves final state for reference
3. Releases resources (context, connections)
4. Updates registry to reflect removal
5. Notifies dependent agents

---

## 2.2 When to terminate agents

### 2.2.1 Task completion

Terminate when:
- Agent has completed all assigned tasks
- No pending work remains
- Final deliverables are verified

### 2.2.2 Error conditions

Terminate when:
- Agent is in unrecoverable error state
- Repeated failures despite recovery attempts
- Agent is corrupted or malfunctioning

### 2.2.3 Resource reclamation

Terminate when:
- System resources are constrained
- Agent has been idle beyond threshold
- Project phase is complete

### 2.2.4 User request

Terminate when:
- User explicitly requests termination
- Project is cancelled
- Agent is no longer needed

---

## 2.3 Termination procedure

### 2.3.1 Work verification

**Purpose:** Confirm agent has completed or saved all work.

**Verification Steps:**
1. Query agent for current task status
2. Check for any in-progress operations
3. Verify all outputs have been written
4. Confirm no pending commits

**Work Status Check:**

Use the `agent-messaging` skill to query the target agent's current task status. Expect a response including status (e.g., IDLE), pending task count, and last activity timestamp.

### 2.3.2 State preservation

**Purpose:** Save final state for reference and potential recovery.

**State to Preserve:**
- Final task status and outcomes
- Any learned patterns or insights
- Error logs if terminating due to error
- Performance metrics

**State Snapshot Location:**
```
design/memory/agents/
└── code-impl-01/
    ├── final-state.md
    ├── task-log.md
    └── metrics.json
```

### 2.3.3 Termination signal

**Purpose:** Send shutdown command to agent.

**Graceful Termination:**

Use the `agent-messaging` skill to send:
- **Recipient**: the target agent session name (e.g., `code-impl-01`)
- **Subject**: `Termination Request`
- **Priority**: `high`
- **Content**: type `terminate-request`, message: "Please save state and terminate gracefully". Include `reason` (e.g., "Task completed"), `graceful`: true, `timeout`: 60.

**Verify**: confirm message delivery via the `agent-messaging` skill's sent messages feature.

**Forced Termination:**

Use the `agent-messaging` skill to send:
- **Recipient**: the target agent session name (e.g., `code-impl-01`)
- **Subject**: `Forced Termination`
- **Priority**: `urgent`
- **Content**: type `terminate-request`, message: "Immediate termination required". Include `reason` (e.g., "Error condition"), `graceful`: false.

**Verify**: confirm message delivery via the `agent-messaging` skill's sent messages feature.

### 2.3.4 Confirmation await

**Purpose:** Wait for agent to acknowledge termination.

**Expected Response:**
```json
{
  "from": "code-impl-01",
  "subject": "Termination Acknowledged",
  "content": {
    "type": "terminate-response",
    "message": "Terminating gracefully",
    "state_saved": true,
    "final_status": "COMPLETED"
  }
}
```

**Timeout:** 60 seconds for graceful, 10 seconds for forced

### 2.3.5 Registry cleanup

**Purpose:** Remove agent from registry after termination.

**Registry Update:**
```json
{
  "agent_id": "code-impl-01",
  "status": "TERMINATED",
  "terminated_at": "2025-02-01T11:00:00Z",
  "termination_reason": "Task completed",
  "final_status": "COMPLETED"
}
```

After recording termination, remove from active agents list.

---

## 2.4 Graceful vs forced termination

### Graceful Termination

**When to use:**
- Normal task completion
- Planned shutdown
- Agent is responsive

**Behavior:**
1. Agent receives termination request
2. Agent saves all state
3. Agent completes any in-progress writes
4. Agent sends confirmation
5. Agent stops

**Timeout:** 60 seconds (configurable)

### Forced Termination

**When to use:**
- Agent unresponsive
- Urgent resource need
- Error recovery

**Behavior:**
1. Termination signal sent
2. Brief wait for response (10 seconds)
3. If no response, mark as terminated
4. State may be lost

**Warning:** Forced termination may result in lost work.

---

## 2.5 Post-termination validation

**Validation Checklist:**

- [ ] Agent removed from active registry
- [ ] State snapshot saved (if graceful)
- [ ] Resources released (context freed)
- [ ] Dependent agents notified
- [ ] No orphaned processes
- [ ] Logs archived

**Validation Steps:**

1. Use the `ai-maestro-agents-management` skill to list all agents and verify the terminated agent no longer appears in the active registry.
2. Check state saved by verifying that `design/memory/agents/code-impl-01/final-state.md` exists (for graceful terminations).

---

## 2.6 Examples

### Example 1: Graceful Termination After Task Completion

```python
# Agent completed its task
agent_id = "code-impl-auth-01"

# Step 1: Verify work complete
status = get_agent_status(agent_id)
assert status["pending_tasks"] == 0

# Step 2: Request graceful termination
send_termination_request(agent_id, graceful=True, reason="Task completed")

# Step 3: Wait for confirmation
response = await_termination_response(agent_id, timeout=60)
assert response["state_saved"] == True

# Step 4: Update registry
update_registry(agent_id, status="TERMINATED")

# Step 5: Notify orchestrator
notify_chief_of_staff(f"Agent {agent_id} terminated successfully")
```

### Example 2: Forced Termination Due to Error

```python
# Agent is stuck in error state
agent_id = "test-eng-broken-01"

# Step 1: Attempt graceful first
try:
    send_termination_request(agent_id, graceful=True, timeout=30)
except TimeoutError:
    # Step 2: Force terminate
    send_termination_request(agent_id, graceful=False)

# Step 3: Mark as terminated regardless of response
update_registry(agent_id, status="TERMINATED", reason="Forced due to error")

# Step 4: Log the incident
log_incident(agent_id, "Forced termination after graceful timeout")
```

---

## 2.7 Troubleshooting

### Issue: Agent does not respond to termination request

**Symptoms:** No acknowledgment received, agent still appears active.

**Resolution:**
1. Verify agent is receiving messages (check AI Maestro)
2. Try pinging agent to confirm responsiveness
3. If unresponsive, use forced termination
4. Check for stuck processes manually
5. Update registry manually if needed

### Issue: State not saved during termination

**Symptoms:** No state snapshot found, work lost.

**Resolution:**
1. Check if termination was forced (state not saved in forced)
2. Look for partial state files
3. Check agent logs for save errors
4. Recover from any backup or git history
5. Document the loss for process improvement

### Issue: Agent remains in registry after termination

**Symptoms:** Terminated agent still appears as active.

**Resolution:**
1. Manually update registry status to TERMINATED
2. Verify no resurrection logic is running
3. Check for duplicate agent IDs
4. Clean up stale entries periodically

### Issue: Dependent agents not notified

**Symptoms:** Other agents waiting for terminated agent.

**Resolution:**
1. Manually notify waiting agents
2. Update dependency graph
3. Unblock waiting tasks
4. Add notification step to termination procedure
