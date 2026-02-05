---
name: ecos-performance-tracking
description: Use when tracking team performance, analyzing agent strengths and weaknesses, collecting metrics, and generating performance reports. Trigger with performance review or metrics requests.
license: Apache-2.0
compatibility: Requires AI Maestro for agent metrics, session memory for historical data, and reporting capabilities. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ecos-main
---

# Emasoft Chief of Staff Performance Tracking Skill

## Overview

Performance tracking enables the Chief of Staff to understand how well the agent team is performing, identify individual strengths and weaknesses, and make data-driven decisions about team composition and task assignment. This skill teaches systematic approaches to collecting metrics, analyzing performance, and generating useful reports.

## Prerequisites

Before using this skill, ensure:
1. Agent metrics are being collected
2. Performance baselines are established
3. Reporting templates are available

## Instructions

1. Identify performance metrics needed
2. Query agent activity logs
3. Calculate performance indicators
4. Generate performance report

## Output

| Metric Type | Output |
|-------------|--------|
| Task completion | Completion rate, average time |
| Resource usage | Memory, CPU, API calls |
| Quality metrics | Error rate, rework rate |

## What Is Performance Tracking?

Performance tracking is the systematic collection and analysis of metrics about agent behavior, output quality, and efficiency. Unlike traditional employee performance reviews, agent performance tracking happens continuously and focuses on measurable outcomes rather than subjective assessments.

**Key characteristics:**
- **Data-driven**: Based on measurable metrics, not impressions
- **Continuous**: Ongoing tracking, not point-in-time reviews
- **Actionable**: Insights lead to concrete improvements
- **Fair**: Consistent criteria applied to all agents

## Performance Tracking Components

### 1. Performance Metrics
Quantifiable measures of agent output and behavior.

### 2. Strength-Weakness Analysis
Identification of what each agent does well and where they struggle.

### 3. Performance Reporting
Communication of findings to relevant stakeholders.

## Core Procedures

### PROCEDURE 1: Collect Performance Metrics

**When to use:** Continuously during agent operation, at task completion, during periodic reviews.

**Steps:** Define metrics to track, capture data at relevant events, aggregate over time periods, validate data quality.

**Related documentation:**

#### Performance Metrics ([references/performance-metrics.md](references/performance-metrics.md))
- 1.1 Metric categories → Categories Of Performance Metrics section
- 1.2 Task metrics → Task Completion Metrics section
- 1.3 Quality metrics → Quality Metrics section
- 1.4 Efficiency metrics → Efficiency Metrics section
- 1.5 Communication metrics → Communication Metrics section
- 1.6 Data collection → Collecting Metric Data section
- 1.7 Examples → Performance Metrics Examples section
- 1.8 Issues → Troubleshooting section

### PROCEDURE 2: Analyze Strengths and Weaknesses

**When to use:** When making role assignments, after performance issues, during team planning.

**Steps:** Review collected metrics, identify patterns, compare against benchmarks, document findings.

**Related documentation:**

#### Strength-Weakness Analysis ([references/strength-weakness-analysis.md](references/strength-weakness-analysis.md))
- 2.1 Analysis framework → Performance Analysis Framework section
- 2.2 Identifying strengths → Identifying Agent Strengths section
- 2.3 Identifying weaknesses → Identifying Agent Weaknesses section
- 2.4 Benchmarking → Comparing Against Benchmarks section
- 2.5 Pattern recognition → Recognizing Performance Patterns section
- 2.6 Recommendations → Making Performance Recommendations section
- 2.7 Examples → Analysis Examples section
- 2.8 Issues → Troubleshooting section

### PROCEDURE 3: Generate Performance Reports

**When to use:** On regular schedule (daily/weekly), on request, after significant events.

**Steps:** Aggregate metrics, format for audience, include analysis, provide recommendations.

**Related documentation:**

#### Performance Reporting ([references/performance-reporting.md](references/performance-reporting.md))
- 3.1 Report types → Types Of Performance Reports section
- 3.2 Report structure → Structuring Performance Reports section
- 3.3 Daily reports → Daily Performance Summaries section
- 3.4 Weekly reports → Weekly Performance Reviews section
- 3.5 Individual reports → Individual Agent Reports section
- 3.6 Distribution → Distributing Reports section
- 3.7 Examples → Performance Report Examples section
- 3.8 Issues → Troubleshooting section

## Task Checklist

Copy this checklist and track your progress:

- [ ] Understand performance tracking purpose and scope
- [ ] Learn PROCEDURE 1: Collect performance metrics
- [ ] Learn PROCEDURE 2: Analyze strengths and weaknesses
- [ ] Learn PROCEDURE 3: Generate performance reports
- [ ] Configure metric collection
- [ ] Establish performance baselines
- [ ] Create reporting templates

## Examples

### Example 1: Recording Task Completion Metric

```markdown
# Task Completion Record

Agent: helper-agent-generic
Task: TASK-042 (Implement logout endpoint)
Assigned: 2025-02-01T08:00:00Z
Completed: 2025-02-01T12:30:00Z
Duration: 4.5 hours
Estimated: 4 hours
Quality: Passed review on first attempt
Blockers: None

Metrics:
- On-time: YES (within 110% of estimate)
- First-pass quality: YES
- Blocker-free: YES
```

### Example 2: Agent Strength-Weakness Summary

```markdown
# Agent Analysis: helper-agent-generic

## Strengths
1. **Code Review Speed**: Completes reviews 25% faster than average
2. **First-Pass Quality**: 90% of code passes review on first attempt
3. **Communication**: Clear, concise status updates

## Weaknesses
1. **Complex Algorithms**: Struggles with optimization tasks
2. **Documentation**: Often leaves docs incomplete
3. **Estimation**: Underestimates by average of 30%

## Recommendations
- Assign code review tasks (strength)
- Pair with senior agent for algorithm work (weakness mitigation)
- Require documentation checklist for all tasks
```

### Example 3: Weekly Performance Summary

```markdown
# Weekly Performance Summary

Period: 2025-01-27 to 2025-02-02

## Team Overview
- Active Agents: 8
- Tasks Completed: 45
- On-Time Rate: 82%
- First-Pass Quality: 75%

## Top Performers
1. libs-svg-svgbbox: 12 tasks, 100% on-time
2. helper-agent-generic: 8 tasks, 88% first-pass

## Areas for Improvement
1. Documentation completion rate: 65% (target: 90%)
2. Estimation accuracy: +35% average overrun

## Recommendations
- Add documentation checkpoint to workflow
- Review estimation process with underperforming agents
```

## Error Handling

### Issue: Metrics data is incomplete

**Symptoms:** Missing entries, gaps in timelines, inconsistent records.

**Solution:** Automate metric collection, add validation at data entry, backfill where possible from logs.

### Issue: Performance comparison seems unfair

**Symptoms:** Agent assigned harder tasks appears to underperform.

**Solution:** Normalize metrics by task complexity, compare similar task types, consider external factors.

### Issue: Reports not driving improvements

**Symptoms:** Same issues appear week after week, no action taken.

**Solution:** Include specific action items, assign owners, track action completion, escalate stalled items.

## Key Takeaways

1. **Metrics must be meaningful** - Measure what matters, not just what is easy
2. **Context is crucial** - Raw numbers need interpretation
3. **Fairness requires consistency** - Apply same standards to all
4. **Reports should drive action** - Information without action is waste
5. **Track improvement over time** - Performance is a journey, not a snapshot

## Resources

- [Performance Metrics](references/performance-metrics.md)
- [Strength-Weakness Analysis](references/strength-weakness-analysis.md)
- [Performance Reporting](references/performance-reporting.md)
- [Report Formats](references/report-formats.md) - Performance report formats

---

**Version:** 1.0
**Last Updated:** 2025-02-01
**Target Audience:** Emasoft Chief of Staff Agent
**Difficulty Level:** Intermediate
