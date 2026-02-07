---
procedure: support-skill
workflow-instruction: support
operation: detect-agent-failure
parent-skill: ecos-failure-recovery
---

# Operation: Detect Agent Failure

## Purpose

Detect when an agent becomes unresponsive, crashes, or terminates unexpectedly using heartbeat monitoring, message delivery status, or task completion timeouts.

## When To Use This Operation

- Regularly (every 30-60 seconds for heartbeat monitoring)
- When an agent stops responding to messages
- When task progress stalls unexpectedly
- When AI Maestro reports agent offline
- When message delivery fails repeatedly

## Steps

1. **Check heartbeat status**
   Use the `ai-maestro-agents-management` skill to query the agent's heartbeat status by name.

2. **Query AI Maestro for agent status**
   Use the `ai-maestro-agents-management` skill to query the agent's session details and current status.

3. **Verify message delivery**
   - Send a test ping message
   - Wait for acknowledgment (timeout: 30 seconds)
   - If no response, agent may be unresponsive

4. **Review task progress**
   - Check task tracking file for stalled tasks
   - Compare expected progress vs actual progress
   - Tasks with no progress for >15 minutes may indicate failure

5. **Document findings**
   - Record detection method used
   - Record timestamp of detection
   - Record last known agent state

## Detection Signals

| Signal | Detection Time | Reliability |
|--------|---------------|-------------|
| Heartbeat timeout | 30-60 seconds | High |
| Message delivery failure | Immediate | High |
| Message acknowledgment timeout | 5-15 minutes | Medium |
| Task completion timeout | Variable | Medium |

## Checklist

Copy this checklist and track your progress:

- [ ] Heartbeat status checked
- [ ] AI Maestro agent status queried
- [ ] Message delivery verified
- [ ] Task progress reviewed
- [ ] Detection timestamp recorded
- [ ] Detection method documented
- [ ] Proceed to failure classification

## Output

After completing this operation:
- Agent failure confirmed OR agent responsive
- Detection timestamp recorded
- Ready for Phase 2: Classify Failure Severity

## Related References

- [failure-detection.md](failure-detection.md) - Complete detection procedures
- [troubleshooting.md](troubleshooting.md) - Detection issues

## Next Operation

If failure detected, proceed to: [op-classify-failure-severity.md](op-classify-failure-severity.md)
