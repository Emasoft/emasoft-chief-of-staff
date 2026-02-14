---
procedure: support-skill
workflow-instruction: support
operation: collect-performance-metrics
parent-skill: ecos-performance-tracking
---

# Operation: Collect Performance Metrics


## Contents

- [Purpose](#purpose)
- [When To Use This Operation](#when-to-use-this-operation)
- [Metric Categories](#metric-categories)
- [Steps](#steps)
  - [Step 1: Define Metrics to Track](#step-1-define-metrics-to-track)
- [Agent Metrics Template](#agent-metrics-template)
  - [Task Metrics](#task-metrics)
  - [Quality Metrics](#quality-metrics)
  - [Efficiency Metrics](#efficiency-metrics)
  - [Communication Metrics](#communication-metrics)
  - [Step 2: Capture Data at Task Completion](#step-2-capture-data-at-task-completion)
  - [Step 3: Aggregate Over Time Periods](#step-3-aggregate-over-time-periods)
  - [Step 4: Validate Data Quality](#step-4-validate-data-quality)
- [Data Quality Check](#data-quality-check)
  - [Step 5: Store Metrics](#step-5-store-metrics)
- [Checklist](#checklist)
- [Metric Collection Automation](#metric-collection-automation)
- [Output](#output)
- [Related References](#related-references)
- [Next Operation](#next-operation)

## Purpose

Systematically collect quantifiable metrics about agent behavior, output quality, and efficiency.

## When To Use This Operation

- Continuously during agent operation
- At task completion
- During periodic reviews (daily, weekly)
- When performance issues are suspected

## Metric Categories

| Category | Metrics |
|----------|---------|
| Task Completion | Completion rate, time to complete, on-time rate |
| Quality | First-pass quality, error rate, rework rate |
| Efficiency | Context usage, API calls per task |
| Communication | Response time, message clarity |

## Steps

### Step 1: Define Metrics to Track

For each agent, track:

```markdown
## Agent Metrics Template

Agent: [agent-name]
Period: [start] to [end]

### Task Metrics
- Tasks assigned: [count]
- Tasks completed: [count]
- Completion rate: [percentage]
- Average time to complete: [hours]
- On-time rate: [percentage]

### Quality Metrics
- First-pass quality rate: [percentage]
- Error count: [count]
- Rework instances: [count]

### Efficiency Metrics
- Average context usage: [percentage]
- API calls per task: [count]
- Context compactions: [count]

### Communication Metrics
- Average response time: [minutes]
- Escalations: [count]
- Blockers reported: [count]
```

### Step 2: Capture Data at Task Completion

When a task completes, record:

```json
{
  "agent": "agent-name",
  "task_id": "TASK-001",
  "task_type": "implementation|review|debug|test",
  "assigned_at": "ISO8601",
  "completed_at": "ISO8601",
  "duration_hours": 4.5,
  "estimated_hours": 4.0,
  "on_time": true,
  "first_pass": true,
  "rework_count": 0,
  "blockers_encountered": 0,
  "context_usage_peak": 75,
  "api_calls": 23
}
```

### Step 3: Aggregate Over Time Periods

```bash
# Example: Calculate completion rate for an agent
cat $CLAUDE_PROJECT_DIR/.ecos/metrics/task-completions.jsonl | \
  jq -s '[.[] | select(.agent == "AGENT_NAME")] | {
    total: length,
    completed: [.[] | select(.completed_at != null)] | length,
    rate: ([.[] | select(.completed_at != null)] | length) / length * 100
  }'
```

### Step 4: Validate Data Quality

Before using metrics:
- Check for missing entries
- Verify timestamps are reasonable
- Ensure consistent units
- Flag anomalies for review

```markdown
## Data Quality Check

- Total records: [count]
- Complete records: [count]
- Missing fields: [list]
- Anomalies: [list]
- Data quality score: [percentage]
```

### Step 5: Store Metrics

Save to performance data directory:

```
$CLAUDE_PROJECT_DIR/.ecos/metrics/
  task-completions.jsonl
  quality-records.jsonl
  efficiency-records.jsonl
  communication-records.jsonl
```

## Checklist

Copy this checklist and track your progress:

- [ ] Metrics to track defined
- [ ] Data capture at task completion configured
- [ ] Aggregation period determined (daily/weekly)
- [ ] Data quality validated
- [ ] Metrics stored in structured format
- [ ] Anomalies flagged for review
- [ ] Ready for analysis

## Metric Collection Automation

```bash
#!/bin/bash
# Record task completion metric

AGENT="$1"
TASK_ID="$2"
DURATION="$3"
ESTIMATE="$4"
FIRST_PASS="$5"

METRICS_FILE="$CLAUDE_PROJECT_DIR/.ecos/metrics/task-completions.jsonl"

jq -n \
  --arg agent "$AGENT" \
  --arg task "$TASK_ID" \
  --arg completed "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --argjson duration "$DURATION" \
  --argjson estimate "$ESTIMATE" \
  --argjson first_pass "$FIRST_PASS" \
  '{
    agent: $agent,
    task_id: $task,
    completed_at: $completed,
    duration_hours: $duration,
    estimated_hours: $estimate,
    on_time: ($duration <= ($estimate * 1.1)),
    first_pass: $first_pass
  }' >> "$METRICS_FILE"
```

## Output

After completing this operation:
- Metrics collected and validated
- Data stored in structured format
- Ready for analysis and reporting

## Related References

- [performance-metrics.md](performance-metrics.md) - Complete metrics guide
- [report-formats.md](report-formats.md) - Report format templates

## Next Operation

After collection: [op-analyze-strengths-weaknesses.md](op-analyze-strengths-weaknesses.md)
