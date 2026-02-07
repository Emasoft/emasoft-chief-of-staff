---
procedure: support-skill
workflow-instruction: support
operation: execute-recovery-strategy
parent-skill: ecos-failure-recovery
---

# Operation: Execute Recovery Strategy

## Purpose

Attempt to restore a failed agent to operational status using appropriate recovery strategies based on failure classification.

## When To Use This Operation

- After classifying failure as RECOVERABLE
- Before escalating to agent replacement
- When intervention can restore agent function

## Recovery Strategies

| Strategy | When to Use | Time to Recover |
|----------|-------------|-----------------|
| Wait and Retry | Transient failures | 1-5 minutes |
| Restart Agent | Hung/crashed agent | 5-15 minutes |
| Hibernate-Wake | Idle/suspended session | 2-5 minutes |
| Resource Adjustment | Memory/disk exhaustion | 15-60 minutes |

## Steps

### Strategy 1: Wait and Retry (Transient)

1. Set timer for 5 minutes
2. Do not take any action
3. After timeout, re-run failure detection
4. If still failing, escalate to recoverable

### Strategy 2: Restart Agent (Soft)

1. Send soft restart signal via AI Maestro
   ```bash
   curl -X POST "http://localhost:23000/api/agents/AGENT_NAME/restart" \
     -H "Content-Type: application/json" \
     -d '{"type": "soft"}'
   ```
2. Wait 2 minutes for restart
3. Verify agent status
4. If failed, attempt hard restart

### Strategy 3: Restart Agent (Hard)

1. Request hard restart via AI Maestro
   ```bash
   curl -X POST "http://localhost:23000/api/agents/AGENT_NAME/restart" \
     -H "Content-Type: application/json" \
     -d '{"type": "hard"}'
   ```
2. Wait 5 minutes for full restart
3. Verify agent status
4. If failed, classify as terminal

### Strategy 4: Hibernate-Wake Cycle

1. Check if agent is hibernated
2. Send wake signal
   ```bash
   curl -X POST "http://localhost:23000/api/agents/AGENT_NAME/wake"
   ```
3. Wait 2 minutes
4. Verify agent responsive

### Strategy 5: Resource Adjustment

1. Identify resource constraint (memory, disk, CPU)
2. Request resource increase from user if needed
3. Clear caches or temporary files
4. Restart after resources freed

## Recovery Attempt Tracking

Track all recovery attempts:

```json
{
  "agent": "agent-name",
  "attempt": 1,
  "strategy": "soft-restart",
  "timestamp": "ISO8601",
  "result": "success|failed",
  "details": "result details"
}
```

## Checklist

Copy this checklist and track your progress:

- [ ] Recovery strategy selected based on failure type
- [ ] Manager notified (if high severity)
- [ ] Recovery attempt initiated
- [ ] Wait period completed
- [ ] Agent status verified
- [ ] Result documented
- [ ] If failed: attempt next strategy OR escalate to terminal

## Escalation Criteria

Escalate to TERMINAL if:
- 3 consecutive recovery attempts failed
- Recovery succeeded but agent failed again within 10 minutes
- Underlying cause cannot be resolved

## Output

After completing this operation:
- Agent recovered and operational, OR
- Recovery failed and classified as TERMINAL

## Related References

- [recovery-strategies.md](recovery-strategies.md) - Complete recovery procedures
- [recovery-operations.md](recovery-operations.md) - Detailed recovery operations
- [troubleshooting.md](troubleshooting.md) - Recovery issues

## Next Operation

- If recovered: Resume normal monitoring
- If failed: Proceed to [op-replace-agent.md](op-replace-agent.md)
