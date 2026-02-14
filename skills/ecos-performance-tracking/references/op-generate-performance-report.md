---
procedure: support-skill
workflow-instruction: support
operation: generate-performance-report
parent-skill: ecos-performance-tracking
---

# Operation: Generate Performance Report


## Contents

- [Purpose](#purpose)
- [When To Use This Operation](#when-to-use-this-operation)
- [Report Types](#report-types)
- [Steps](#steps)
  - [Step 1: Aggregate Metrics](#step-1-aggregate-metrics)
  - [Step 2: Format for Audience](#step-2-format-for-audience)
- [Quick Stats](#quick-stats)
- [Highlights](#highlights)
- [Concerns](#concerns)
- [Tomorrow's Focus](#tomorrows-focus)
- [Team Overview](#team-overview)
- [Top Performers](#top-performers)
- [Areas for Improvement](#areas-for-improvement)
- [Agent Breakdown](#agent-breakdown)
- [Recommendations](#recommendations)
- [Next Week Focus](#next-week-focus)
- [Summary](#summary)
- [Task Breakdown](#task-breakdown)
- [Strengths This Period](#strengths-this-period)
- [Areas to Improve](#areas-to-improve)
- [Comparison to Previous Period](#comparison-to-previous-period)
  - [Step 3: Include Analysis](#step-3-include-analysis)
  - [Step 4: Provide Recommendations](#step-4-provide-recommendations)
- [Action Items](#action-items)
  - [Step 5: Distribute Report](#step-5-distribute-report)
- [Checklist](#checklist)
- [Output](#output)
- [Report File Locations](#report-file-locations)
- [Related References](#related-references)

## Purpose

Create formatted performance reports for stakeholders, summarizing team and individual metrics with actionable insights.

## When To Use This Operation

- On regular schedule (daily summary, weekly review)
- On request from manager or orchestrator
- After significant events
- At project milestones

## Report Types

| Type | Frequency | Audience | Focus |
|------|-----------|----------|-------|
| Daily Summary | Daily | EOA, EAMA | Quick status |
| Weekly Review | Weekly | EAMA, User | Detailed analysis |
| Individual Report | As needed | Agent, EAMA | Single agent focus |
| Project Report | At milestones | User | Project progress |

## Steps

### Step 1: Aggregate Metrics

Gather data for the report period:

```bash
# Get metrics for date range
START_DATE="2025-02-01"
END_DATE="2025-02-07"

cat $CLAUDE_PROJECT_DIR/.ecos/metrics/task-completions.jsonl | \
  jq -s --arg start "$START_DATE" --arg end "$END_DATE" \
  '[.[] | select(.completed_at >= $start and .completed_at <= $end)]'
```

### Step 2: Format for Audience

#### Daily Summary Format

```markdown
# Daily Performance Summary

Date: [date]

## Quick Stats
- Active Agents: [count]
- Tasks Completed: [count]
- On-Time Rate: [percentage]
- Blockers: [count]

## Highlights
- [Notable achievement]
- [Notable achievement]

## Concerns
- [Issue needing attention]

## Tomorrow's Focus
- [Priority item]
```

#### Weekly Review Format

```markdown
# Weekly Performance Review

Period: [start] to [end]

## Team Overview
- Active Agents: [count]
- Total Tasks Completed: [count]
- On-Time Rate: [percentage]
- First-Pass Quality: [percentage]

## Top Performers
1. [agent]: [achievement]
2. [agent]: [achievement]

## Areas for Improvement
1. [area]: [details]
2. [area]: [details]

## Agent Breakdown

| Agent | Tasks | On-Time | Quality | Notes |
|-------|-------|---------|---------|-------|
| agent-1 | 10 | 90% | 85% | Strong week |
| agent-2 | 8 | 75% | 80% | Estimation issues |

## Recommendations
1. [Recommendation]
2. [Recommendation]

## Next Week Focus
- [Priority]
```

#### Individual Report Format

```markdown
# Individual Performance Report: [agent-name]

Period: [start] to [end]

## Summary
- Tasks Completed: [count]
- On-Time Rate: [percentage]
- First-Pass Quality: [percentage]
- Context Compactions: [count]

## Task Breakdown

| Task | Type | Duration | On-Time | Quality |
|------|------|----------|---------|---------|
| TASK-001 | impl | 4h | Yes | First-pass |
| TASK-002 | review | 1h | Yes | First-pass |

## Strengths This Period
- [Strength with evidence]

## Areas to Improve
- [Weakness with recommendation]

## Comparison to Previous Period
- On-time: [current]% vs [previous]% ([change])
- Quality: [current]% vs [previous]% ([change])
```

### Step 3: Include Analysis

Add insights beyond raw numbers:
- Trends (improving/declining)
- Anomalies (unusual events)
- Correlations (patterns)
- Predictions (potential issues)

### Step 4: Provide Recommendations

Every report should include actionable items:

```markdown
## Action Items

| Item | Owner | Priority | Due |
|------|-------|----------|-----|
| Review estimation process | ECOS | High | Next week |
| Add documentation checklist | EOA | Medium | This sprint |
```

### Step 5: Distribute Report

Save and distribute:

```bash
# Save report
REPORT_FILE="$CLAUDE_PROJECT_DIR/.ecos/reports/weekly-$(date +%Y%m%d).md"

# Notify stakeholders
# Use the agent-messaging skill to notify the manager:
# Recipient: eama-assistant-manager
# Subject: "Weekly Performance Report"
# Content: type "performance-report", report_path: $REPORT_FILE
```

## Checklist

Copy this checklist and track your progress:

- [ ] Report type and period determined
- [ ] Metrics aggregated for period
- [ ] Report formatted for audience
- [ ] Analysis and insights included
- [ ] Recommendations provided
- [ ] Action items listed with owners
- [ ] Report saved to reports directory
- [ ] Stakeholders notified

## Output

After completing this operation:
- Formatted report saved
- Stakeholders notified
- Action items tracked

## Report File Locations

```
$CLAUDE_PROJECT_DIR/.ecos/reports/
  daily-YYYYMMDD.md
  weekly-YYYYMMDD.md
  individual-AGENT-YYYYMMDD.md
  project-MILESTONE.md
```

## Related References

- [performance-reporting.md](performance-reporting.md) - Complete reporting guide
- [report-formats.md](report-formats.md) - Format templates
- [performance-metrics.md](performance-metrics.md) - Metric definitions
