---
procedure: support-skill
workflow-instruction: support
operation: classify-failure-severity
parent-skill: ecos-failure-recovery
---

# Operation: Classify Failure Severity

## Purpose

Classify a detected failure as transient, recoverable, or terminal to determine the appropriate response strategy.

## When To Use This Operation

- After detecting an agent failure (op-detect-agent-failure)
- Before attempting recovery
- When deciding whether to replace an agent

## Failure Categories

| Category | Severity | Recovery Time | Action |
|----------|----------|---------------|--------|
| **Transient** | Low | Automatic < 5 min | Wait and Retry |
| **Recoverable** | Medium | With intervention | Restart / Wake |
| **Terminal** | High | Replacement required | Replace Agent |

## Steps

1. **Gather failure evidence**
   - Check agent logs if available
   - Review AI Maestro status history
   - Note time since last response
   - Check system resource state

2. **Evaluate transient indicators**
   - Network hiccup (brief connectivity loss)
   - API rate limit (temporary throttling)
   - Brief context compaction
   - Duration < 5 minutes

3. **Evaluate recoverable indicators**
   - Session hibernated (no activity timeout)
   - Out of memory (can be restarted)
   - Context window exhausted (needs compaction)
   - Hung process (needs restart)

4. **Evaluate terminal indicators**
   - Host crash (machine down)
   - Disk corruption (data loss)
   - Authentication failure (credentials revoked)
   - 3+ consecutive recovery failures

5. **Document classification**
   - Record failure category
   - Record evidence supporting classification
   - Log to incident log

## Decision Matrix

```
Time since last response < 5 min AND no error state?
  → TRANSIENT (wait for auto-recovery)

Time > 5 min AND session exists AND no crash indicators?
  → RECOVERABLE (attempt restart/wake)

Crash indicators present OR 3+ failed recoveries?
  → TERMINAL (proceed to replacement)
```

## Checklist

Copy this checklist and track your progress:

- [ ] Failure evidence gathered
- [ ] Transient indicators evaluated
- [ ] Recoverable indicators evaluated
- [ ] Terminal indicators evaluated
- [ ] Failure type determined: [ ] Transient [ ] Recoverable [ ] Terminal
- [ ] Evidence documented
- [ ] Incident logged
- [ ] Classification recorded

## Output

After completing this operation:
- Failure classified as TRANSIENT, RECOVERABLE, or TERMINAL
- Evidence documented in incident log
- Recovery path determined

## Incident Log Entry Format

```json
{
  "timestamp": "ISO8601",
  "agent": "agent-name",
  "failure_type": "transient|recoverable|terminal",
  "evidence": ["list", "of", "evidence"],
  "detection_method": "heartbeat|message|task",
  "next_action": "wait|restart|replace"
}
```

## Related References

- [failure-classification.md](failure-classification.md) - Complete classification criteria
- [failure-detection.md](failure-detection.md) - Detection methods

## Next Operation

- If TRANSIENT: Wait 5 minutes, then retry detection
- If RECOVERABLE: Proceed to [op-execute-recovery-strategy.md](op-execute-recovery-strategy.md)
- If TERMINAL: Proceed to [op-replace-agent.md](op-replace-agent.md)
