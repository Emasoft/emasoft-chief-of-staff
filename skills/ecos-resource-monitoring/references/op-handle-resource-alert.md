---
procedure: support-skill
workflow-instruction: support
operation: handle-resource-alert
parent-skill: ecos-resource-monitoring
---

# Operation: Handle Resource Alert


## Contents

- [Purpose](#purpose)
- [When To Use This Operation](#when-to-use-this-operation)
- [Alert Severity Levels](#alert-severity-levels)
- [Steps](#steps)
  - [Step 1: Identify Alert Type](#step-1-identify-alert-type)
  - [Step 2: Assess Severity](#step-2-assess-severity)
- [Alert Assessment](#alert-assessment)
  - [Step 3: Take Immediate Action](#step-3-take-immediate-action)
  - [Step 4: Notify Relevant Parties](#step-4-notify-relevant-parties)
  - [Step 5: Document Incident](#step-5-document-incident)
- [Resource Alert Incident](#resource-alert-incident)
- [Immediate Actions Taken](#immediate-actions-taken)
- [Resolution](#resolution)
- [Prevention](#prevention)
- [Checklist](#checklist)
- [Alert Response Matrix](#alert-response-matrix)
- [Output](#output)
- [Related References](#related-references)

## Purpose

Respond to resource threshold violations with appropriate actions to maintain system health and agent operations.

## When To Use This Operation

- When resource thresholds are exceeded
- When monitoring scripts trigger alerts
- When degradation is detected
- When agents report resource-related issues

## Alert Severity Levels

| Level | Indicator | Response Time | Actions |
|-------|-----------|---------------|---------|
| INFO | Approaching threshold | Monitor closely | Log, continue |
| WARNING | Threshold exceeded | 15 minutes | Mitigate, notify |
| CRITICAL | Severe violation | Immediate | Stop spawning, reduce load |

## Steps

### Step 1: Identify Alert Type

Common alert types:
- **CPU_HIGH**: CPU usage > 85%
- **MEMORY_LOW**: Free memory < 1GB
- **DISK_FULL**: Disk usage > 85%
- **SESSION_LIMIT**: Sessions > 85% of max
- **RATE_LIMIT**: API calls approaching limit
- **NETWORK_DOWN**: AI Maestro unreachable

### Step 2: Assess Severity

```markdown
## Alert Assessment

Alert Type: [type]
Current Value: [value]
Threshold: [threshold]
Severity: [INFO/WARNING/CRITICAL]

Timestamp: [ISO8601]
Duration: [how long has this been occurring]
```

### Step 3: Take Immediate Action

#### For CPU_HIGH:
1. Identify agents with high CPU usage
2. Request context compaction from busy agents
3. Pause non-critical agent spawning
4. If critical: reduce agent count

#### For MEMORY_LOW:
1. Identify agents with large context windows
2. Request context compaction
3. Clear system caches if safe
4. Pause new agent spawning

#### For DISK_FULL:
1. Identify large log files
2. Archive or delete old logs
3. Clear temporary files
4. Alert user if action needed

#### For SESSION_LIMIT:
1. Do not spawn new agents
2. Prioritize existing work
3. Queue new agent requests
4. Consider agent consolidation

#### For RATE_LIMIT:
1. Reduce message frequency
2. Batch operations where possible
3. Implement backoff
4. Queue non-urgent messages

#### For NETWORK_DOWN:
1. Attempt reconnection
2. Use fallback communication if available
3. Queue messages
4. Alert user immediately

### Step 4: Notify Relevant Parties

For WARNING and CRITICAL alerts:

> **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.
```json
{
  "from": "ecos-chief-of-staff",
  "to": "eama-assistant-manager",
  "subject": "RESOURCE ALERT: [type]",
  "priority": "high",
  "content": {
    "type": "resource-alert",
    "message": "Resource threshold exceeded. Immediate action taken.",
    "alert_type": "[type]",
    "severity": "[WARNING/CRITICAL]",
    "current_value": "[value]",
    "threshold": "[threshold]",
    "action_taken": "[what was done]",
    "recommended_action": "[if user action needed]"
  }
}
```

### Step 5: Document Incident

```markdown
## Resource Alert Incident

**Timestamp:** [ISO8601]
**Alert Type:** [type]
**Severity:** [level]
**Current Value:** [value]
**Threshold:** [threshold]

## Immediate Actions Taken

1. [Action 1]
2. [Action 2]
3. [Action 3]

## Resolution

[What resolved the issue]
[Time to resolution]

## Prevention

[What can prevent future occurrences]
```

## Checklist

Copy this checklist and track your progress:

- [ ] Alert type identified
- [ ] Severity assessed
- [ ] Immediate action taken
- [ ] Affected agents notified (if applicable)
- [ ] Manager notified (WARNING/CRITICAL)
- [ ] Incident documented
- [ ] Resolution verified
- [ ] Monitoring frequency increased
- [ ] Prevention measures noted

## Alert Response Matrix

| Alert Type | Immediate Action | Notify |
|------------|------------------|--------|
| CPU_HIGH | Compact contexts | EAMA if critical |
| MEMORY_LOW | Compact contexts, pause spawning | EAMA if critical |
| DISK_FULL | Clear logs | EAMA, user |
| SESSION_LIMIT | Stop spawning | EAMA |
| RATE_LIMIT | Backoff | EAMA if persistent |
| NETWORK_DOWN | Reconnect | EAMA, user immediately |

## Output

After completing this operation:
- Alert addressed with appropriate action
- Incident documented
- Stakeholders notified
- Monitoring continues at increased frequency

## Related References

- [resource-alerts.md](resource-alerts.md) - Complete alert handling guide
- [system-resources.md](system-resources.md) - Resource monitoring
- [monitoring-commands.md](monitoring-commands.md) - Command reference
