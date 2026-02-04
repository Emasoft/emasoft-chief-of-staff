# Performance Metrics Reference

## Table of Contents

- 1.1 [Categories Of Performance Metrics](#11-categories-of-performance-metrics)
- 1.2 [Task Completion Metrics](#12-task-completion-metrics)
- 1.3 [Quality Metrics](#13-quality-metrics)
- 1.4 [Efficiency Metrics](#14-efficiency-metrics)
- 1.5 [Communication Metrics](#15-communication-metrics)
- 1.6 [Collecting Metric Data](#16-collecting-metric-data)
- 1.7 [Performance Metrics Examples](#17-performance-metrics-examples)
- 1.8 [Troubleshooting](#18-troubleshooting)

---

## 1.1 Categories Of Performance Metrics

Performance metrics are organized into four categories that together provide a complete picture of agent performance.

### Task Completion

Measures related to completing assigned work:
- Tasks completed count
- On-time completion rate
- Deadline adherence
- Task abandonment rate

### Quality

Measures related to the quality of output:
- First-pass acceptance rate
- Rework frequency
- Error rate
- Review feedback score

### Efficiency

Measures related to resource utilization:
- Time per task
- Estimation accuracy
- Context usage
- Tool efficiency

### Communication

Measures related to team interaction:
- Response time
- Update frequency
- Clarity score
- Escalation appropriateness

---

## 1.2 Task Completion Metrics

### Tasks Completed

**Definition:** Count of tasks moved to complete status.

**Calculation:**
```
Tasks Completed = COUNT(tasks WHERE status = 'complete')
```

**Time periods:**
- Daily: Tasks completed today
- Weekly: Tasks completed this week
- Total: All tasks ever completed

**Data source:** Progress tracking file, task management system

### On-Time Rate

**Definition:** Percentage of tasks completed by their deadline.

**Calculation:**
```
On-Time Rate = (Tasks Completed On Time / Total Tasks Completed) * 100
```

**What counts as on-time:**
- Completed before deadline: On-time
- Completed on deadline day: On-time
- Completed after deadline: Late

**Thresholds:**
- Excellent: > 90%
- Good: 75-90%
- Needs Improvement: < 75%

### Deadline Adherence

**Definition:** Average time relative to deadline for completed tasks.

**Calculation:**
```
Deadline Adherence = AVG(Deadline - Completion Time)
```

**Interpretation:**
- Positive value: Completed early (average days early)
- Zero: Completed exactly on deadline
- Negative value: Completed late (average days late)

### Task Abandonment Rate

**Definition:** Percentage of assigned tasks that were abandoned or reassigned.

**Calculation:**
```
Abandonment Rate = (Abandoned Tasks / Total Assigned Tasks) * 100
```

**What counts as abandoned:**
- Task reassigned to another agent
- Task cancelled while in progress
- Task blocked indefinitely without resolution

**Thresholds:**
- Good: < 5%
- Acceptable: 5-10%
- Concerning: > 10%

---

## 1.3 Quality Metrics

### First-Pass Acceptance Rate

**Definition:** Percentage of deliverables accepted without requiring revisions.

**Calculation:**
```
First-Pass Rate = (Tasks Accepted First Attempt / Total Tasks Reviewed) * 100
```

**What counts as first-pass:**
- Code merged without changes requested
- Document approved without edits
- Test passed without modifications

**Thresholds:**
- Excellent: > 85%
- Good: 70-85%
- Needs Improvement: < 70%

### Rework Frequency

**Definition:** Average number of revision cycles per task.

**Calculation:**
```
Rework Frequency = Total Revision Cycles / Total Tasks Completed
```

**What counts as a revision cycle:**
- Each round of review feedback
- Each request for changes
- Each rejection requiring update

**Thresholds:**
- Excellent: < 1.2 cycles
- Good: 1.2-1.5 cycles
- Needs Improvement: > 1.5 cycles

### Error Rate

**Definition:** Errors discovered in completed work.

**Calculation:**
```
Error Rate = Errors Found / Total Deliverables
```

**Types of errors:**
- Bugs in code
- Incorrect implementations
- Missing requirements
- Documentation errors

**Thresholds:**
- Excellent: < 0.1 per task
- Good: 0.1-0.3 per task
- Needs Improvement: > 0.3 per task

### Review Feedback Score

**Definition:** Qualitative assessment of review feedback.

**Categories:**
- Positive: "Good work", "Clean code", "Well done"
- Neutral: "Minor changes", "Small fixes needed"
- Negative: "Major issues", "Needs significant rework"

**Score calculation:**
```
Score = (Positive * 1.0 + Neutral * 0.5 + Negative * 0.0) / Total Reviews
```

---

## 1.4 Efficiency Metrics

### Time Per Task

**Definition:** Average time from task start to completion.

**Calculation:**
```
Time Per Task = Total Work Time / Tasks Completed
```

**Normalization:** Should be normalized by task complexity when comparing agents.

**Complexity categories:**
- Simple: < 2 hours expected
- Medium: 2-8 hours expected
- Complex: > 8 hours expected

### Estimation Accuracy

**Definition:** How close actual time is to estimated time.

**Calculation:**
```
Accuracy = (Actual Time / Estimated Time) * 100
```

**Interpretation:**
- 100%: Perfect estimate
- < 100%: Completed faster than estimated
- > 100%: Took longer than estimated

**Thresholds:**
- Excellent: 90-110%
- Good: 80-120%
- Needs Improvement: < 80% or > 120%

### Context Efficiency

**Definition:** How effectively the agent uses context window.

**Indicators:**
- Context compaction frequency
- Percentage of context used for active work
- Context recovery success rate

**Healthy patterns:**
- Compaction requests: < 2 per day
- Active context usage: > 70%
- Recovery success: 100%

### Tool Efficiency

**Definition:** Effective use of available tools.

**Indicators:**
- Tools used appropriately for task type
- Retry rate (failed tool calls)
- Tool substitution (using wrong tool)

**Healthy patterns:**
- Appropriate tool usage: > 95%
- Retry rate: < 5%
- Substitutions: < 2%

---

## 1.5 Communication Metrics

### Response Time

**Definition:** Time from receiving message to acknowledging or responding.

**Calculation:**
```
Response Time = Response Timestamp - Message Received Timestamp
```

**Expectations by priority:**
- Urgent: < 5 minutes
- High: < 15 minutes
- Normal: < 30 minutes

**Thresholds:**
- Excellent: Within expected time 95%+
- Good: Within expected time 80-95%
- Needs Improvement: < 80%

### Update Frequency

**Definition:** How often the agent provides status updates during active work.

**Expected frequency:**
- During active work: Every 2 hours
- When blocked: Immediately
- At task transitions: Always

**Calculation:**
```
Update Compliance = Actual Updates / Expected Updates
```

**Thresholds:**
- Good: > 90% compliance
- Acceptable: 70-90% compliance
- Needs Improvement: < 70% compliance

### Clarity Score

**Definition:** Subjective assessment of communication clarity.

**Assessment criteria:**
- Is the message understandable?
- Does it include necessary context?
- Is it appropriately concise?
- Does it answer the question asked?

**Score:**
- Clear: All criteria met
- Mostly Clear: 3 of 4 criteria met
- Unclear: < 3 criteria met

### Escalation Appropriateness

**Definition:** Whether escalations are used correctly.

**Appropriate escalation:**
- Issue genuinely requires escalation
- Escalated to correct person
- Sufficient context provided
- Alternatives attempted first

**Inappropriate escalation:**
- Issue could be resolved without escalation
- Escalated to wrong person
- Insufficient context
- No attempt to resolve first

---

## 1.6 Collecting Metric Data

### Automatic Collection

Many metrics can be collected automatically:

**From AI Maestro:**
- Message timestamps (response time)
- Message counts (update frequency)
- Session activity (active time)

**From task tracking:**
- Task status changes (completion)
- Assignment timestamps (duration)
- Deadline comparison (on-time rate)

**From code review:**
- Review iterations (rework)
- Approval/rejection (first-pass)
- Comments (feedback score)

### Manual Collection

Some metrics require manual observation:

**Quality assessments:**
- Clarity score (requires reading)
- Appropriateness judgments
- Context quality

**Recording manual observations:**
```markdown
# design/memory/performance/manual-observations.md

## 2025-02-01

### helper-agent-generic

**Observation:** Response to status request was unclear
**Category:** Communication Clarity
**Score:** Unclear
**Notes:** Message lacked task ID and current status, only said "working on it"
```

### Data Storage

Store performance data in structured format:

```markdown
# design/memory/performance/metrics-[agent]-[date].md

## Agent: helper-agent-generic
## Date: 2025-02-01

### Task Completion
- Tasks Completed: 3
- On-Time: 3/3 (100%)
- Abandoned: 0

### Quality
- First-Pass: 2/3 (67%)
- Rework Cycles: 1.3 avg
- Errors Found: 1

### Efficiency
- Avg Time/Task: 2.5 hours
- Est Accuracy: 115%

### Communication
- Avg Response Time: 8 minutes
- Updates Provided: 6/6 (100%)
- Clarity Issues: 1
```

---

## 1.7 Performance Metrics Examples

### Example: Daily Metric Summary

```markdown
# Daily Performance Metrics

Date: 2025-02-01
Agent: helper-agent-generic

## Summary
| Category | Score | Trend |
|----------|-------|-------|
| Task Completion | 100% | +5% |
| Quality | 67% | -10% |
| Efficiency | 115% | Stable |
| Communication | 92% | Stable |

## Details

### Tasks
- Completed: TASK-041, TASK-042, TASK-043
- All on time

### Quality Issues
- TASK-042 required revision (missing error handling)

### Efficiency
- Average 15% over estimate (acceptable)

### Communication
- 1 clarity issue noted (status update)
```

### Example: Comparative Agent Metrics

```markdown
# Team Performance Comparison

Week: 2025-W05

| Agent | Tasks | On-Time | First-Pass | Response |
|-------|-------|---------|------------|----------|
| helper-agent-generic | 8 | 88% | 75% | 8 min |
| libs-svg-svgbbox | 12 | 100% | 92% | 5 min |
| helper-agent-backup | 5 | 60% | 80% | 15 min |

## Analysis
- libs-svg-svgbbox highest performer across all metrics
- helper-agent-backup struggling with deadlines
- helper-agent-generic quality declining (was 85% last week)
```

### Example: Trend Analysis

```markdown
# Performance Trend: helper-agent-generic

## On-Time Rate (last 4 weeks)
- Week 02: 85%
- Week 03: 90%
- Week 04: 95%
- Week 05: 88%

**Trend:** Generally improving, slight dip this week

## First-Pass Rate (last 4 weeks)
- Week 02: 85%
- Week 03: 80%
- Week 04: 75%
- Week 05: 67%

**Trend:** Declining - needs investigation

## Recommendation
Quality is declining while speed is maintained. May be rushing.
Suggest reviewing work before submission.
```

---

## 1.8 Troubleshooting

### Issue: Metrics data is inconsistent

**Symptoms:** Numbers do not add up, missing periods, duplicates.

**Possible causes:**
- Multiple sources not synced
- Manual entry errors
- Timezone issues

**Resolution:**
1. Establish single source of truth
2. Validate data at collection time
3. Use consistent timestamps (UTC)
4. Reconcile sources regularly

### Issue: Metrics seem unfair between agents

**Symptoms:** Agent with harder tasks appears worse.

**Possible causes:**
- Task complexity not accounted for
- External factors affecting performance
- Different measurement standards

**Resolution:**
1. Normalize by task complexity
2. Compare similar task types
3. Consider external factors
4. Apply consistent measurement

### Issue: Too many metrics to track

**Symptoms:** Data collection burden, analysis paralysis.

**Possible causes:**
- Trying to measure everything
- No prioritization of metrics
- Redundant measures

**Resolution:**
1. Focus on key metrics (5-10 maximum)
2. Eliminate redundant measures
3. Automate where possible
4. Review metric value periodically

### Issue: Historical data is lost

**Symptoms:** Cannot compare to previous periods, no trends.

**Possible causes:**
- No archival process
- Files overwritten
- Session memory not preserved

**Resolution:**
1. Implement metric archival
2. Use date-stamped files
3. Aggregate before compaction
4. Backup metric files

---

**Version:** 1.0
**Last Updated:** 2025-02-01
