# Resource Alerts Reference

## Table of Contents

- 3.1 [Types Of Resource Alerts](#31-types-of-resource-alerts)
- 3.2 [Alert Severity Levels](#32-alert-severity-levels)
- 3.3 [Alert Response Procedures](#33-alert-response-procedures)
- 3.4 [Alert Escalation](#34-alert-escalation)
- 3.5 [Alert Prevention](#35-alert-prevention)
- 3.6 [Resource Alert Examples](#36-resource-alert-examples)
- 3.7 [Troubleshooting](#37-troubleshooting)

---

## 3.1 Types Of Resource Alerts

Resource alerts notify the Chief of Staff when resources approach or exceed limits.

### Memory Alert

Triggered when memory usage exceeds thresholds.

**Causes:**
- Too many active agents
- Large context windows
- Memory leaks in long-running processes

**Indicators:**
- Memory usage > 70% (warning)
- Memory usage > 85% (critical)
- Swap usage increasing

### CPU Alert

Triggered when CPU load is excessive.

**Causes:**
- Too many concurrent operations
- Infinite loops or runaway processes
- Heavy computation tasks

**Indicators:**
- Load average > 0.7 per core (warning)
- Load average > 1.0 per core (critical)
- Sustained high usage

### Disk Alert

Triggered when disk space is low.

**Causes:**
- Log file growth
- Accumulated session memories
- Large artifacts or downloads

**Indicators:**
- Disk usage > 75% (warning)
- Disk usage > 90% (critical)
- Inodes exhausted

### Network Alert

Triggered when network connectivity is degraded.

**Causes:**
- Network outage
- Service downtime
- High latency

**Indicators:**
- Failed connectivity checks
- Latency > 500ms
- Packet loss

### Rate Limit Alert

Triggered when approaching API rate limits.

**Causes:**
- High API call volume
- Burst activity
- Inefficient patterns

**Indicators:**
- Rate limit remaining < 20%
- Rate limit errors occurring
- Throttling detected

### Instance Limit Alert

Triggered when session or concurrency limits are approached.

**Causes:**
- Scaling without checks
- Stale sessions accumulating
- Coordination overhead

**Indicators:**
- Sessions > 80% of limit
- Concurrency bottlenecks
- Queue buildup

---

## 3.2 Alert Severity Levels

### INFO

Informational alerts that require awareness but no immediate action.

**Characteristics:**
- Resource usage elevated but safe
- Trend worth monitoring
- No impact on operations

**Response:**
- Acknowledge and note
- Monitor for changes
- No immediate action required

### WARNING

Alerts indicating a developing issue that needs attention soon.

**Characteristics:**
- Resource approaching threshold
- Performance may be affected
- Action recommended within 30 minutes

**Response:**
- Assess the situation
- Plan corrective action
- Implement if resources permit
- Increase monitoring frequency

### CRITICAL

Alerts indicating a serious issue requiring immediate attention.

**Characteristics:**
- Resource at or exceeding threshold
- Operations affected
- Action required within 10 minutes

**Response:**
- Stop non-essential operations
- Implement immediate mitigation
- Notify relevant parties
- Document actions taken

### EMERGENCY

Alerts indicating a system-threatening condition.

**Characteristics:**
- Resources exhausted or failing
- Operations cannot continue
- Immediate action required

**Response:**
- Execute emergency procedures
- Notify user immediately
- Preserve critical state
- Prepare for recovery

---

## 3.3 Alert Response Procedures

### Memory Alert Response

**WARNING (70-85%):**
1. Identify agents with largest context
2. Request context compaction from idle agents
3. Pause new agent spawning
4. Monitor every 5 minutes

**CRITICAL (85-95%):**
1. Immediately request all agents compact context
2. Terminate idle agents
3. Pause non-critical tasks
4. Notify orchestrator and user

**EMERGENCY (>95%):**
1. Force terminate non-essential agents
2. Preserve only critical agent states
3. Notify user immediately
4. Prepare for potential crash

### CPU Alert Response

**WARNING (0.7-1.0 load/core):**
1. Identify CPU-heavy processes
2. Reduce parallel operations
3. Prioritize critical tasks
4. Monitor every 5 minutes

**CRITICAL (1.0-2.0 load/core):**
1. Pause new task assignments
2. Serialize concurrent operations
3. Identify and stop runaway processes
4. Notify orchestrator

**EMERGENCY (>2.0 load/core):**
1. Stop all non-essential operations
2. Terminate processes causing load
3. Notify user
4. Allow system to recover

### Disk Alert Response

**WARNING (75-90%):**
1. Identify large files and directories
2. Archive old logs and memories
3. Clean temporary files
4. Plan capacity increase if recurring

**CRITICAL (90-95%):**
1. Emergency log rotation
2. Delete non-essential files
3. Pause write-heavy operations
4. Notify user

**EMERGENCY (>95%):**
1. Delete oldest log files immediately
2. Clear all temp directories
3. Stop operations that write to disk
4. Notify user urgently

### Network Alert Response

**DEGRADED (high latency):**
1. Reduce API call frequency
2. Increase timeouts
3. Queue non-urgent requests
4. Monitor connectivity

**CRITICAL (intermittent):**
1. Pause remote operations
2. Use local operations only
3. Queue all remote requests
4. Notify orchestrator

**EMERGENCY (no connectivity):**
1. Stop all remote communication
2. Preserve local state
3. Notify user
4. Wait for recovery

---

## 3.4 Alert Escalation

### Escalation Path

| Level | First Response | If Unresolved (10 min) | If Still Unresolved (30 min) |
|-------|---------------|----------------------|------------------------------|
| WARNING | Chief of Staff handles | Notify orchestrator | Notify user |
| CRITICAL | Chief of Staff + orchestrator | Notify user | Force intervention |
| EMERGENCY | Immediate user notification | - | - |

### Escalation Message Format

```markdown
## Resource Alert Escalation

**Time:** [timestamp]
**Alert Type:** [type]
**Severity:** [level]
**Duration:** [how long active]

### Current State
[Description of current resource state]

### Actions Taken
1. [Action 1] - [result]
2. [Action 2] - [result]

### Why Escalating
[Reason escalation is needed]

### Recommended Action
[What the escalation target should do]
```

### User Notification Format

```bash
# Send urgent user notification
curl -X POST "http://localhost:23000/api/notifications/user" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "resource-alert",
    "severity": "critical",
    "title": "Memory Critical - Action Required",
    "message": "Memory usage at 92%. Agents are being terminated. Please review."
  }'
```

---

## 3.5 Alert Prevention

### Proactive Monitoring

Prevent alerts by continuous monitoring:

```markdown
## Monitoring Schedule

| Resource | Check Interval | Warning Lead Time |
|----------|---------------|-------------------|
| Memory | 5 minutes | 15 minutes |
| CPU | 5 minutes | 10 minutes |
| Disk | 15 minutes | 1 hour |
| Network | 5 minutes | Immediate |
| Rate Limits | Per request | 10 minutes |
```

### Capacity Planning

Prevent resource exhaustion:

1. **Track trends**: Record resource usage over time
2. **Predict needs**: Estimate future resource requirements
3. **Plan scaling**: Schedule resource increases before needed
4. **Review patterns**: Identify recurring issues and address root causes

### Best Practices

**Memory:**
- Request compaction proactively at 60%
- Limit context window sizes
- Archive old session memories

**CPU:**
- Serialize heavy operations
- Use efficient tool patterns
- Avoid parallel git operations

**Disk:**
- Rotate logs daily
- Archive completed session data weekly
- Clean temp files after operations

**Network:**
- Batch API requests
- Cache responses
- Use exponential backoff

**Rate Limits:**
- Monitor usage vs limits
- Distribute calls across time
- Queue requests when approaching limits

---

## 3.6 Resource Alert Examples

### Example: Memory Warning Alert

```markdown
# Resource Alert: Memory Warning

**Timestamp:** 2025-02-01T10:30:00Z
**Type:** Memory
**Severity:** WARNING
**Current Value:** 72%
**Threshold:** 70%

## Analysis
- 8 active agents consuming ~70% of memory
- orchestrator-master has largest context (45% of agent memory)
- Memory usage trending upward (+5% in last hour)

## Actions Taken
1. Requested context compaction from 3 idle agents
2. Paused new agent spawning
3. Increased monitoring to 5-minute intervals

## Expected Outcome
Memory usage should drop to ~60% after compactions complete.

## Escalation
None required at this time.
```

### Example: CPU Critical Alert

```markdown
# Resource Alert: CPU Critical

**Timestamp:** 2025-02-01T14:15:00Z
**Type:** CPU
**Severity:** CRITICAL
**Current Value:** 1.2 load per core
**Threshold:** 1.0 load per core

## Analysis
- libs-svg-svgbbox running intensive parsing operation
- 4 agents running parallel file searches
- Load has been elevated for 10 minutes

## Actions Taken
1. Paused new task assignments
2. Serialized remaining file searches (1 at a time)
3. Asked libs-svg-svgbbox for estimated completion time

## Current State
Load beginning to decrease. Expect recovery in 10 minutes.

## Escalation
Notified orchestrator-master of reduced capacity.
```

### Example: Emergency Disk Alert

```markdown
# Resource Alert: Disk Emergency

**Timestamp:** 2025-02-01T16:00:00Z
**Type:** Disk
**Severity:** EMERGENCY
**Current Value:** 97%
**Threshold:** 95%

## Analysis
- Debug logging left enabled generated 2GB of logs
- Disk almost full

## Immediate Actions
1. Deleted logs older than 1 day: freed 1.8GB
2. Cleared ~/.claude/cache: freed 500MB
3. Stopped all write operations

## Current State
Disk now at 78%. Crisis averted.

## Post-Incident Actions Required
1. Disable verbose logging in production
2. Implement log rotation (daily, max 500MB)
3. Add disk alert at 60% for earlier warning

## User Notification
Sent notification about incident and corrective actions.
```

---

## 3.7 Troubleshooting

### Issue: Alerts not triggering

**Symptoms:** Resources exceed thresholds but no alerts generated.

**Possible causes:**
- Monitoring not running
- Thresholds misconfigured
- Alert output not delivered

**Resolution:**
1. Verify monitoring script is running
2. Check threshold values
3. Test alert delivery mechanism
4. Review monitoring logs

### Issue: Too many false positive alerts

**Symptoms:** Frequent alerts that do not indicate real problems.

**Possible causes:**
- Thresholds too sensitive
- Normal spikes triggering alerts
- Transient conditions detected

**Resolution:**
1. Increase thresholds appropriately
2. Add sustained-duration requirement
3. Implement alert dampening
4. Review and tune over time

### Issue: Alert response not effective

**Symptoms:** Actions taken but resource issue persists.

**Possible causes:**
- Root cause not addressed
- Action insufficient
- New load appeared

**Resolution:**
1. Analyze actual resource consumers
2. Take stronger action
3. Escalate sooner
4. Address root cause, not symptoms

### Issue: Escalation not reaching recipients

**Symptoms:** Escalated alerts not acknowledged or acted upon.

**Possible causes:**
- Notification mechanism failing
- Recipients not monitoring
- Message format unclear

**Resolution:**
1. Verify notification delivery
2. Use multiple notification channels
3. Require acknowledgment
4. Follow up via alternative means

---

**Version:** 1.0
**Last Updated:** 2025-02-01
