---
procedure: support-skill
workflow-instruction: support
operation: monitor-instance-limits
parent-skill: ecos-resource-monitoring
---

# Operation: Monitor Instance Limits

## Purpose

Track active agent sessions, API rate limits, and concurrency constraints to ensure team capacity is maintained.

## When To Use This Operation

- Before spawning new agents
- When approaching limits
- When coordination slows
- During capacity planning
- Every 5 minutes during active operations

## Steps

### Step 1: Count Active Sessions

Use the `ai-maestro-agents-management` skill to list all active sessions and count them.

The skill will return the active session count and session names.

**Recommended Limits:**
- Conservative: 10 concurrent agents
- Normal: 15 concurrent agents
- Maximum: 20 concurrent agents

### Step 2: Check API Rate Limits

Use the `ai-maestro-agents-management` skill to query API statistics, including message send rates.

The skill will return message counts and rate limit status.

**Rate Limit Awareness:**
- Track messages per minute
- Track API calls per minute
- Leave 20% headroom for bursts

### Step 3: Verify Concurrency Headroom

```bash
# Calculate headroom
max_sessions=20
active=$active_count
headroom=$((max_sessions - active))

echo "Concurrency headroom: $headroom sessions available"

if [ "$headroom" -lt 3 ]; then
  echo "WARNING: Low concurrency headroom"
fi
```

### Step 4: Assess Scaling Needs

Based on current usage and planned operations:

1. **Planned agent spawns:** How many agents will be needed?
2. **Current headroom:** Can we accommodate them?
3. **Resource constraints:** Do system resources allow more agents?

```markdown
## Scaling Assessment

Current active: [X] agents
Max allowed: [Y] agents
Headroom: [Z] agents

Planned operations:
- [Operation 1]: needs [N] agents
- [Operation 2]: needs [M] agents

Total needed: [N+M] agents
Can proceed: [YES/NO]
```

### Step 5: Document Instance State

```json
{
  "timestamp": "ISO8601",
  "active_sessions": 12,
  "max_sessions": 20,
  "headroom": 8,
  "messages_last_minute": 45,
  "api_calls_last_minute": 23,
  "status": "normal"
}
```

## Checklist

Copy this checklist and track your progress:

- [ ] Active sessions counted
- [ ] Session list reviewed
- [ ] API rate limits checked
- [ ] Concurrency headroom calculated
- [ ] Scaling needs assessed
- [ ] Instance state documented
- [ ] Alerts triggered if limits approached

## Instance Limit Thresholds

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| Active sessions | < 70% of max | 70-85% | > 85% |
| Messages/minute | < 50 | 50-80 | > 80 |
| API calls/minute | < 40 | 40-60 | > 60 |
| Headroom | > 5 | 3-5 | < 3 |

## Output

After completing this operation:
- Current instance usage documented
- Headroom for new agents calculated
- Scaling feasibility determined

## Related References

- [instance-limits.md](instance-limits.md) - Complete instance limit guide
- [monitoring-commands.md](monitoring-commands.md) - Command reference
- [resource-alerts.md](resource-alerts.md) - Alert handling

## Next Operation

If limits approached: [op-handle-resource-alert.md](op-handle-resource-alert.md)
