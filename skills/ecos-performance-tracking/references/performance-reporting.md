# Performance Reporting Reference

## Table of Contents

- 3.1 [Types Of Performance Reports](#31-types-of-performance-reports)
- 3.2 [Structuring Performance Reports](#32-structuring-performance-reports)
- 3.3 [Daily Performance Summaries](#33-daily-performance-summaries)
- 3.4 [Weekly Performance Reviews](#34-weekly-performance-reviews)
- 3.5 [Individual Agent Reports](#35-individual-agent-reports)
- 3.6 [Distributing Reports](#36-distributing-reports)
- 3.7 [Performance Report Examples](#37-performance-report-examples)
- 3.8 [Troubleshooting](#38-troubleshooting)

---

## 3.1 Types Of Performance Reports

Different reports serve different purposes and audiences.

### Daily Summary

**Purpose:** Quick status update on daily activity
**Audience:** Orchestrator, Chief of Staff
**Depth:** High-level metrics only
**Action focus:** Immediate issues requiring attention

### Weekly Review

**Purpose:** Comprehensive performance analysis
**Audience:** Orchestrator, User, Team
**Depth:** Detailed metrics with trends
**Action focus:** Strategic improvements

### Individual Agent Report

**Purpose:** Focused analysis on single agent
**Audience:** Agent, Orchestrator, Chief of Staff
**Depth:** Complete agent-specific metrics
**Action focus:** Personal development

### Incident Report

**Purpose:** Document and analyze performance incidents
**Audience:** Stakeholders involved
**Depth:** Deep dive on specific event
**Action focus:** Prevent recurrence

### Ad-Hoc Report

**Purpose:** Answer specific questions
**Audience:** Requester
**Depth:** Varies by question
**Action focus:** Inform decisions

---

## 3.2 Structuring Performance Reports

All performance reports follow a consistent structure for readability.

### Standard Report Sections

**Header:**
- Report title and type
- Time period covered
- Generated timestamp
- Report author (Chief of Staff)

**Executive Summary:**
- 2-3 sentence overview
- Key highlights
- Critical issues if any

**Metrics Section:**
- Organized by category
- Current values with comparisons
- Visual indicators (trends, status)

**Analysis Section:**
- Interpretation of metrics
- Pattern identification
- Root cause insights

**Recommendations Section:**
- Prioritized action items
- Owners and timelines
- Success criteria

**Appendix (if needed):**
- Detailed data tables
- Supporting evidence
- Methodology notes

### Report Formatting

**Tables for metrics:**
```markdown
| Metric | Current | Previous | Target | Status |
|--------|---------|----------|--------|--------|
| On-Time Rate | 85% | 80% | 90% | Improving |
```

**Status indicators:**
- Rising trend: Improving
- Stable: Stable
- Declining trend: Declining
- Above target: Good (or Met)
- Below target: Needs Attention

**Highlight formatting:**
- **Bold** for key findings
- > Blockquotes for recommendations
- Lists for action items

---

## 3.3 Daily Performance Summaries

Daily summaries provide a quick pulse check on team activity.

### Daily Summary Template

```markdown
# Daily Performance Summary

**Date:** [YYYY-MM-DD]
**Generated:** [timestamp]

## Quick Stats

| Metric | Today | 7-Day Avg |
|--------|-------|-----------|
| Active Agents | X | Y |
| Tasks Completed | X | Y |
| On-Time Rate | X% | Y% |

## Highlights
- [Notable achievement or event]
- [Notable achievement or event]

## Issues
- [Issue requiring attention, if any]

## Tomorrow Focus
- [Key priorities for tomorrow]
```

### What to Include

**Always include:**
- Active agent count
- Tasks completed
- On-time completion rate
- Any critical issues

**Optionally include:**
- Top performer of the day
- Blockers encountered
- Resource status

### What to Exclude

- Detailed analysis (save for weekly)
- Individual agent deep dives
- Historical trends (save for weekly)
- Minor variances

### Daily Summary Example

```markdown
# Daily Performance Summary

**Date:** 2025-02-01
**Generated:** 2025-02-01T18:00:00Z

## Quick Stats

| Metric | Today | 7-Day Avg |
|--------|-------|-----------|
| Active Agents | 8 | 7 |
| Tasks Completed | 12 | 10 |
| On-Time Rate | 92% | 85% |

## Highlights
- libs-svg-svgbbox completed 4 tasks, all on-time
- Zero escalations to user today

## Issues
- None

## Tomorrow Focus
- Sprint 5 deadline: ensure remaining 3 tasks complete
- helper-agent-backup needs onboarding follow-up
```

---

## 3.4 Weekly Performance Reviews

Weekly reviews provide comprehensive analysis for strategic decisions.

### Weekly Review Template

```markdown
# Weekly Performance Review

**Week:** [YYYY-WNN]
**Period:** [Start Date] to [End Date]
**Generated:** [timestamp]

## Executive Summary

[2-3 sentences summarizing the week]

## Team Overview

| Metric | This Week | Last Week | Change | Target |
|--------|-----------|-----------|--------|--------|
| Tasks Completed | X | Y | +/-Z% | T |
| On-Time Rate | X% | Y% | +/-Z% | T% |
| First-Pass Quality | X% | Y% | +/-Z% | T% |
| Avg Response Time | X min | Y min | +/-Z% | T min |

## Individual Performance

| Agent | Tasks | On-Time | Quality | Status |
|-------|-------|---------|---------|--------|
| [agent] | X | Y% | Z% | [status] |

## Trend Analysis

### Improving
- [Metric/behavior that improved and why]

### Stable
- [Metric/behavior that remained consistent]

### Declining
- [Metric/behavior that declined and why]

## Issues and Root Causes

### Issue 1: [Title]
- **Description:** [What happened]
- **Impact:** [How it affected work]
- **Root Cause:** [Why it happened]
- **Resolution:** [What was done or needs to be done]

## Recommendations

### Priority 1: [Recommendation]
- **Rationale:** [Why this is important]
- **Owner:** [Who is responsible]
- **Timeline:** [When to implement]
- **Success Measure:** [How to verify]

## Next Week Focus

- [Key priority 1]
- [Key priority 2]
- [Key priority 3]

## Appendix

### Raw Data
[Detailed metrics tables if needed]
```

### Weekly Review Focus Areas

**Week over week comparison:**
- What improved?
- What declined?
- What stayed the same?

**Goal tracking:**
- Are we on track for sprint/milestone?
- Any risks to delivery?

**Resource health:**
- Team capacity adequate?
- Any burnout indicators?
- Resource constraints?

**Quality trends:**
- First-pass rates
- Rework frequency
- Error patterns

---

## 3.5 Individual Agent Reports

Individual reports focus on a single agent for targeted development.

### Individual Report Template

```markdown
# Individual Performance Report

**Agent:** [session name]
**Role:** [current role]
**Period:** [start date] to [end date]
**Generated:** [timestamp]

## Performance Summary

| Category | Score | Trend | Team Avg | Target |
|----------|-------|-------|----------|--------|
| Task Completion | X% | [trend] | Y% | Z% |
| Quality | X% | [trend] | Y% | Z% |
| Efficiency | X% | [trend] | Y% | Z% |
| Communication | X% | [trend] | Y% | Z% |

## Detailed Metrics

### Task Completion
- Tasks completed: X
- On-time: Y (Z%)
- Abandoned: N

### Quality
- First-pass rate: X%
- Rework cycles: Y avg
- Errors found: N

### Efficiency
- Average task time: X hours
- Estimation accuracy: Y%
- Context compactions: N

### Communication
- Avg response time: X minutes
- Update compliance: Y%
- Clarity issues: N

## Strengths

1. **[Strength 1]**: [Evidence and details]
2. **[Strength 2]**: [Evidence and details]

## Areas for Improvement

1. **[Area 1]**: [Evidence and details]
   - Recommended action: [What to do]

2. **[Area 2]**: [Evidence and details]
   - Recommended action: [What to do]

## Comparison to Previous Period

| Metric | Current | Previous | Change |
|--------|---------|----------|--------|
| [metric] | X | Y | +/-Z% |

## Goals for Next Period

1. [Goal 1] - Target: [measurable target]
2. [Goal 2] - Target: [measurable target]

## Notes

[Any additional observations or context]
```

### When to Generate Individual Reports

- Quarterly for all agents
- When performance issues are identified
- Before role changes
- At agent request
- When user requests agent assessment

---

## 3.6 Distributing Reports

Reports must reach the right audience to be effective.

### Distribution Matrix

| Report Type | Orchestrator | User | Agent | Team |
|-------------|--------------|------|-------|------|
| Daily Summary | Yes | No* | No | No |
| Weekly Review | Yes | Yes | No | Summary |
| Individual Report | Yes | On request | Yes (own) | No |
| Incident Report | Yes | Yes | Involved | Relevant |

*User receives daily summary only if there are critical issues.

### Distribution Methods

**Via AI Maestro Message:**
Use the `agent-messaging` skill to send:
- **Recipient**: `orchestrator-master`
- **Subject**: `Weekly Performance Review - Week 5`
- **Priority**: `normal`
- **Content**: type `report`, message: "Weekly performance review attached. See design/memory/reports/weekly-W05.md"

**Via File Storage:**
Save reports to shared location:
```
design/memory/reports/
  daily-2025-02-01.md
  weekly-W05.md
  individual-helper-agent-generic-2025-02.md
```

**Via User Notification:**
For critical issues or user-requested reports:
Use the `agent-messaging` skill to send a user notification via EAMA:
- **Recipient**: `eama-assistant-manager` (for user escalation)
- **Subject**: `Weekly Performance Report Available`
- **Priority**: `normal`
- **Content**: type `report`, message: "See design/memory/reports/weekly-W05.md"

### Report Retention

| Report Type | Retention |
|-------------|-----------|
| Daily Summary | 30 days |
| Weekly Review | 1 year |
| Individual Report | 1 year |
| Incident Report | Indefinite |

---

## 3.7 Performance Report Examples

### Example: Daily Summary

```markdown
# Daily Performance Summary

**Date:** 2025-02-01
**Generated:** 2025-02-01T18:00:00Z

## Quick Stats

| Metric | Today | 7-Day Avg |
|--------|-------|-----------|
| Active Agents | 8 | 7 |
| Tasks Completed | 12 | 10 |
| On-Time Rate | 92% | 85% |

## Highlights
- Sprint 5 on track: 12/15 tasks complete
- libs-svg-svgbbox: 4 tasks completed, 100% on-time

## Issues
- helper-agent-backup: 2 tasks delayed, requires follow-up

## Tomorrow Focus
- Complete remaining 3 Sprint 5 tasks
- Onboarding follow-up with helper-agent-backup
```

### Example: Weekly Review (Abbreviated)

```markdown
# Weekly Performance Review

**Week:** 2025-W05
**Period:** 2025-01-27 to 2025-02-02
**Generated:** 2025-02-02T18:00:00Z

## Executive Summary

Strong week with 45 tasks completed (vs 38 last week). On-time rate improved to 82% from 78%. Quality remains stable at 75%. One agent (helper-agent-backup) needs attention due to declining metrics.

## Team Overview

| Metric | This Week | Last Week | Change | Target |
|--------|-----------|-----------|--------|--------|
| Tasks Completed | 45 | 38 | +18% | 40 |
| On-Time Rate | 82% | 78% | +4% | 90% |
| First-Pass Quality | 75% | 76% | -1% | 85% |
| Avg Response Time | 8 min | 9 min | -11% | 10 min |

## Individual Performance

| Agent | Tasks | On-Time | Quality | Status |
|-------|-------|---------|---------|--------|
| orchestrator-master | 5 | 100% | N/A | Excellent |
| libs-svg-svgbbox | 15 | 93% | 87% | Strong |
| helper-agent-generic | 12 | 83% | 75% | Good |
| helper-agent-backup | 8 | 50% | 63% | Needs Attention |
| other-agents | 5 | 80% | 80% | Acceptable |

## Recommendations

### Priority 1: Address helper-agent-backup Performance
- **Rationale:** 50% on-time rate is significantly below target
- **Owner:** Chief of Staff
- **Timeline:** This week
- **Success Measure:** On-time rate improves to 70%+

### Priority 2: Improve Team Quality
- **Rationale:** 75% first-pass is 10% below target
- **Owner:** Orchestrator
- **Timeline:** Next 2 weeks
- **Success Measure:** First-pass rate reaches 80%+

## Next Week Focus

1. Sprint 6 kickoff and task assignment
2. helper-agent-backup performance coaching
3. Quality improvement initiative launch
```

### Example: Individual Report (Abbreviated)

```markdown
# Individual Performance Report

**Agent:** helper-agent-generic
**Role:** Developer
**Period:** January 2025
**Generated:** 2025-02-01T10:00:00Z

## Performance Summary

| Category | Score | Trend | Team Avg | Target |
|----------|-------|-------|----------|--------|
| Task Completion | 88% | Stable | 82% | 90% |
| Quality | 75% | Declining | 75% | 85% |
| Efficiency | 115% | Improving | 110% | 100% |
| Communication | 92% | Stable | 85% | 90% |

## Strengths

1. **Fast Response Time**: Average 5 minutes (team avg 10 minutes)
2. **High Throughput**: 25% more tasks than average
3. **Clear Communication**: Feedback consistently rated "clear"

## Areas for Improvement

1. **Quality Declining**: First-pass from 85% to 75% over month
   - Recommended action: Implement self-review checklist

2. **Documentation**: Often incomplete
   - Recommended action: Add doc completion to definition of done

## Goals for Next Period

1. First-pass quality to 82% (from 75%)
2. Documentation completion to 90% (from 70%)
3. Maintain response time under 10 minutes
```

---

## 3.8 Troubleshooting

### Issue: Reports not being read

**Symptoms:** No action on recommendations, no questions about content.

**Possible causes:**
- Reports too long
- Wrong distribution
- Not actionable

**Resolution:**
1. Add executive summary at top
2. Verify distribution list
3. Make recommendations specific and actionable
4. Ask for acknowledgment

### Issue: Data in reports is incorrect

**Symptoms:** Stakeholders dispute numbers, metrics do not match experience.

**Possible causes:**
- Calculation errors
- Data collection gaps
- Timing discrepancies

**Resolution:**
1. Show calculation methodology
2. Verify data sources
3. Use consistent time periods
4. Add data validation

### Issue: Reports take too long to produce

**Symptoms:** Reports are late, consume too much time.

**Possible causes:**
- Manual data gathering
- Complex formatting
- Too much content

**Resolution:**
1. Automate data collection
2. Use templates
3. Focus on key metrics only
4. Produce simpler reports more frequently

### Issue: Recommendations not implemented

**Symptoms:** Same recommendations appear week after week.

**Possible causes:**
- No ownership assigned
- Competing priorities
- Recommendations too vague

**Resolution:**
1. Assign explicit owner and deadline
2. Track recommendation status
3. Make recommendations specific and achievable
4. Escalate stalled items

---

**Version:** 1.0
**Last Updated:** 2025-02-01
