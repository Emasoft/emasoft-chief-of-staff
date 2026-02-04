# Strength-Weakness Analysis Reference

## Table of Contents

- 2.1 [Performance Analysis Framework](#21-performance-analysis-framework)
- 2.2 [Identifying Agent Strengths](#22-identifying-agent-strengths)
- 2.3 [Identifying Agent Weaknesses](#23-identifying-agent-weaknesses)
- 2.4 [Comparing Against Benchmarks](#24-comparing-against-benchmarks)
- 2.5 [Recognizing Performance Patterns](#25-recognizing-performance-patterns)
- 2.6 [Making Performance Recommendations](#26-making-performance-recommendations)
- 2.7 [Analysis Examples](#27-analysis-examples)
- 2.8 [Troubleshooting](#28-troubleshooting)

---

## 2.1 Performance Analysis Framework

The analysis framework provides a systematic approach to understanding agent performance.

### Framework Components

1. **Data Collection**: Gather metrics from all available sources
2. **Pattern Recognition**: Identify consistent behaviors over time
3. **Benchmark Comparison**: Compare against standards and peers
4. **Root Cause Analysis**: Understand why patterns exist
5. **Recommendation Generation**: Suggest actionable improvements

### Analysis Principles

**Fairness:**
- Compare similar roles and task types
- Account for external factors
- Use consistent criteria

**Evidence-based:**
- Base conclusions on data, not impressions
- Require multiple data points before conclusions
- Distinguish correlation from causation

**Actionable:**
- Focus on what can be changed
- Provide specific recommendations
- Set measurable improvement goals

### Analysis Frequency

| Analysis Type | Frequency | Purpose |
|--------------|-----------|---------|
| Quick check | Daily | Identify immediate issues |
| Trend analysis | Weekly | Track patterns over time |
| Deep analysis | Monthly | Comprehensive performance review |
| Role fit | Quarterly | Evaluate role assignments |

---

## 2.2 Identifying Agent Strengths

Strengths are areas where an agent consistently performs above average.

### Strength Indicators

**Metric-based indicators:**
- Consistently above team average
- Improving trend over time
- Exceeds benchmarks

**Behavioral indicators:**
- Volunteers for certain task types
- Completes certain tasks faster
- Higher quality on certain work

### Strength Categories

**Task Type Strengths:**
- Code implementation
- Code review
- Testing
- Documentation
- Debugging
- Architecture

**Skill Strengths:**
- Speed (fast completion)
- Quality (few errors)
- Communication (clear updates)
- Reliability (consistent performance)

**Domain Strengths:**
- Specific technology expertise
- Particular codebase knowledge
- Integration understanding

### Strength Identification Process

**Step 1: Gather performance data**

Collect at least 4 weeks of metrics for the agent.

**Step 2: Calculate averages by category**

```markdown
## Agent: helper-agent-generic

| Category | Agent Avg | Team Avg | Difference |
|----------|-----------|----------|------------|
| Code Review Speed | 1.5 hrs | 2.0 hrs | -0.5 hrs (25% faster) |
| First-Pass Rate | 90% | 75% | +15% |
| Response Time | 5 min | 10 min | -5 min (50% faster) |
```

**Step 3: Identify significant positive differences**

Strengths are categories where the agent is >10% better than average.

**Step 4: Validate with behavioral observation**

Confirm the metrics align with observed behavior.

**Step 5: Document strengths**

```markdown
## Confirmed Strengths

1. **Code Review Speed**: 25% faster than team average
   - Evidence: 4-week avg 1.5 hrs vs team 2.0 hrs
   - Observation: Quick to identify issues, concise feedback

2. **First-Pass Quality**: 15% higher than team
   - Evidence: 90% acceptance vs team 75%
   - Observation: Thorough self-review before submission
```

---

## 2.3 Identifying Agent Weaknesses

Weaknesses are areas where an agent consistently underperforms.

### Weakness Indicators

**Metric-based indicators:**
- Consistently below team average
- Declining trend over time
- Fails to meet benchmarks

**Behavioral indicators:**
- Avoids certain task types
- Requires more guidance on certain work
- Higher error rate on certain tasks

### Weakness Categories

**Task Type Weaknesses:**
- Struggles with complex algorithms
- Difficulty with large refactors
- Poor test coverage
- Incomplete documentation

**Skill Weaknesses:**
- Slow completion
- Error-prone output
- Poor communication
- Inconsistent performance

**Domain Weaknesses:**
- Unfamiliar technology
- New codebase areas
- Integration gaps

### Weakness Identification Process

**Step 1: Gather performance data**

Use same data set as strength analysis.

**Step 2: Calculate averages by category**

Identify categories where agent is below average.

**Step 3: Identify significant negative differences**

Weaknesses are categories where the agent is >10% worse than average.

**Step 4: Investigate root causes**

Before documenting as weakness, understand why:
- Lack of experience?
- Poor fit for task type?
- External factors?
- Training needed?

**Step 5: Document weaknesses with context**

```markdown
## Identified Weaknesses

1. **Documentation Completion**: 20% below team average
   - Evidence: 60% complete vs team 80%
   - Root cause: Prioritizes code over docs
   - Mitigation: Add documentation checklist to workflow

2. **Estimation Accuracy**: 35% average overrun
   - Evidence: Tasks take 135% of estimate
   - Root cause: Underestimates complexity
   - Mitigation: Add buffer or pair on estimates
```

### Distinguishing Weakness from Circumstance

Not all underperformance is a weakness:

| Circumstance | How to Identify | Response |
|--------------|-----------------|----------|
| New to role | Recent role change, improving trend | Give time to ramp |
| Difficult tasks | Assigned harder work than peers | Normalize comparison |
| External factors | One-time drop, known cause | Do not count in analysis |
| Actual weakness | Persistent, no external cause | Document and address |

---

## 2.4 Comparing Against Benchmarks

Benchmarks provide objective standards for comparison.

### Types of Benchmarks

**Team Average:**
Average performance across all team members in the same role.

**Historical Personal:**
The agent's own performance in previous periods.

**Industry Standard:**
External standards for similar work.

**Defined Target:**
Specific goals set by the organization.

### Benchmark Calculation

**Team Average Benchmark:**
```
Team Avg = SUM(All Agent Metrics) / Number of Agents
```

**Historical Personal Benchmark:**
```
Personal Benchmark = AVG(Agent's Last 4 Weeks)
```

**Improvement from Personal:**
```
Improvement = (Current Period - Previous Period) / Previous Period * 100
```

### Benchmark Comparison Table

```markdown
## Benchmark Comparison: helper-agent-generic

| Metric | Current | Team Avg | Personal History | Target |
|--------|---------|----------|------------------|--------|
| On-Time Rate | 88% | 82% | 85% | 90% |
| First-Pass | 75% | 75% | 80% | 85% |
| Response Time | 8 min | 10 min | 8 min | 10 min |

## Analysis
- On-Time: Above team avg, above history, below target
- First-Pass: At team avg, below history, below target (DECLINING)
- Response: Above all benchmarks
```

### Using Benchmarks for Assessment

| Comparison | Interpretation |
|------------|----------------|
| Above all benchmarks | Strong performer, maintain |
| Above team, below target | Good but can improve |
| At team average | Acceptable, room for growth |
| Below team average | Needs attention |
| Declining from personal | Investigate cause |

---

## 2.5 Recognizing Performance Patterns

Patterns reveal consistent behaviors that inform analysis and recommendations.

### Common Positive Patterns

**Steady Performer:**
- Consistent metrics week over week
- Few spikes or dips
- Reliable for planning

**Improving Trend:**
- Metrics improving over time
- Learning and adapting
- Good candidate for advancement

**Task Specialist:**
- Exceptional on certain task types
- Average or below on others
- Route matching tasks

**Quality First:**
- Slower but higher quality
- Low rework rate
- Best for critical work

### Common Negative Patterns

**Declining Trend:**
- Metrics worsening over time
- May indicate burnout, disengagement, or role mismatch
- Investigate cause

**Inconsistent Performer:**
- High variance in metrics
- Unpredictable output
- May need more guidance

**Speed Over Quality:**
- Fast completion, high rework
- Creates downstream work
- May need to slow down

**Avoidance Pattern:**
- Certain task types always delayed or abandoned
- May indicate weakness or discomfort
- Consider role adjustment

### Pattern Detection Methods

**Trend Analysis:**
Plot metrics over time, look for slopes.

**Variance Analysis:**
Calculate standard deviation, high variance indicates inconsistency.

**Correlation Analysis:**
Check if certain task types correlate with performance changes.

**Sequence Analysis:**
Look for patterns in task ordering (e.g., quality drops after long work streaks).

### Pattern Documentation

```markdown
## Performance Patterns: helper-agent-generic

### Pattern 1: Quality Decline After Long Streaks
- Observation: Quality drops after 4+ consecutive tasks
- Evidence: First-pass rate 90% for tasks 1-3, 50% for tasks 4+
- Hypothesis: Fatigue or context overload
- Recommendation: Limit consecutive tasks, enforce breaks

### Pattern 2: Strong on Review, Weak on Implementation
- Observation: Review tasks 25% faster, implementation tasks 20% slower
- Evidence: 4-week task type comparison
- Hypothesis: Better suited for review role
- Recommendation: Emphasize review assignments
```

---

## 2.6 Making Performance Recommendations

Recommendations translate analysis into actionable improvements.

### Recommendation Types

**Role Adjustment:**
Change the agent's role to better match strengths.

**Task Routing:**
Assign specific task types based on capability.

**Training/Coaching:**
Provide guidance to address weaknesses.

**Process Change:**
Modify workflows to prevent issues.

**Monitoring:**
Increase oversight for specific concerns.

### Recommendation Format

```markdown
## Recommendation

**Issue:** [What the analysis revealed]
**Root Cause:** [Why this is happening]
**Recommendation:** [What to do]
**Expected Outcome:** [What improvement to expect]
**Measurement:** [How to verify improvement]
**Owner:** [Who is responsible]
**Timeline:** [When to implement and review]
```

### Recommendation Priority

| Priority | Criteria | Timeline |
|----------|----------|----------|
| Critical | Performance severely impacting work | Immediate |
| High | Significant gap from target | Within 1 week |
| Medium | Moderate improvement opportunity | Within 2 weeks |
| Low | Nice-to-have optimization | When convenient |

### Recommendation Examples

**Role Adjustment:**
```markdown
## Recommendation: Role Change for helper-agent-backup

**Issue:** Consistently underperforming as Developer (60% on-time, 70% quality)
**Root Cause:** Skill set better matched to testing/QA
**Recommendation:** Transition from Developer to Test Engineer role
**Expected Outcome:** Improved on-time (target: 85%), better quality alignment
**Measurement:** Compare metrics after 2 weeks in new role
**Owner:** Chief of Staff
**Timeline:** Transition this week, evaluate in 2 weeks
```

**Process Change:**
```markdown
## Recommendation: Add Documentation Checkpoint

**Issue:** Team documentation completion at 65% (target: 90%)
**Root Cause:** Docs treated as afterthought, not part of "done"
**Recommendation:** Add documentation checklist to task completion criteria
**Expected Outcome:** Documentation rate increase to 85%+
**Measurement:** Track docs completion rate weekly
**Owner:** Orchestrator
**Timeline:** Implement Monday, measure for 2 weeks
```

---

## 2.7 Analysis Examples

### Example: Complete Agent Analysis

```markdown
# Performance Analysis: helper-agent-generic

**Period:** 2025-01 (4 weeks)
**Role:** Code Reviewer

## Summary

| Category | Score | Trend | Benchmark |
|----------|-------|-------|-----------|
| Task Completion | 88% | Stable | At team avg |
| Quality | 75% | Declining | Below target |
| Efficiency | 115% | Improving | At target |
| Communication | 92% | Stable | Above avg |

## Strengths

1. **Response Time**: Consistently responds within 5 minutes
2. **Review Throughput**: Completes 25% more reviews than average
3. **Communication Clarity**: Clear, actionable feedback

## Weaknesses

1. **Quality Declining**: First-pass from 85% to 75% over 4 weeks
2. **Documentation**: Consistently leaves review notes incomplete

## Patterns

- Quality drops after 4+ consecutive reviews
- Better performance in morning hours

## Root Cause Analysis

Quality decline appears related to task volume. Agent is being assigned more work than sustainable while maintaining quality.

## Recommendations

1. **Reduce Review Load** (High Priority)
   - Limit to 6 reviews per day instead of 8
   - Expected: Quality returns to 85%+
   - Timeline: Immediate

2. **Documentation Checklist** (Medium Priority)
   - Add checklist for review completion
   - Expected: Documentation rate improves to 90%
   - Timeline: This week

3. **Morning Prioritization** (Low Priority)
   - Assign complex reviews in morning
   - Expected: Better quality on complex reviews
   - Timeline: When scheduling allows
```

### Example: Comparative Team Analysis

```markdown
# Team Performance Comparison

**Period:** Week 5, 2025
**Roles Compared:** Developers (3 agents)

## Performance Matrix

| Agent | Tasks | On-Time | First-Pass | Efficiency | Comm |
|-------|-------|---------|------------|------------|------|
| dev-agent-1 | 8 | 88% | 85% | 105% | 90% |
| dev-agent-2 | 12 | 100% | 92% | 95% | 95% |
| dev-agent-3 | 5 | 60% | 80% | 140% | 75% |

## Analysis

**Top Performer:** dev-agent-2
- Highest volume, perfect on-time, best quality
- Recommend: Lead developer role consideration

**Solid Performer:** dev-agent-1
- Balanced metrics, no concerns
- Recommend: Continue current assignment

**Needs Attention:** dev-agent-3
- Low volume, poor on-time, slow efficiency
- Root cause: Taking on tasks beyond capability
- Recommend: Simpler task assignments, mentoring

## Team Actions

1. Pair dev-agent-3 with dev-agent-2 for mentoring
2. Increase dev-agent-2 task complexity level
3. Review dev-agent-3 after 2 weeks
```

---

## 2.8 Troubleshooting

### Issue: Analysis seems unfair to certain agents

**Symptoms:** Agents complain, metrics do not match perception.

**Possible causes:**
- Not accounting for task difficulty
- External factors not considered
- Measurement bias

**Resolution:**
1. Normalize by task complexity
2. Document external factors
3. Review measurement consistency
4. Get feedback from agents

### Issue: Cannot determine root cause

**Symptoms:** Metrics show problem but cause unclear.

**Possible causes:**
- Insufficient data
- Multiple contributing factors
- Hidden variables

**Resolution:**
1. Gather more data over longer period
2. Interview the agent directly
3. Test hypotheses with controlled changes
4. Consult with orchestrator for insights

### Issue: Recommendations not implemented

**Symptoms:** Same issues persist week after week.

**Possible causes:**
- Recommendations not communicated
- No ownership assigned
- Competing priorities

**Resolution:**
1. Assign explicit owner to each recommendation
2. Set implementation deadline
3. Track recommendation status
4. Escalate stalled items

### Issue: Agent performance does not improve

**Symptoms:** Recommendations implemented but no change.

**Possible causes:**
- Wrong root cause identified
- Recommendation insufficient
- Agent capability limitation

**Resolution:**
1. Re-analyze to verify root cause
2. Try different or stronger intervention
3. If persistent, consider role change
4. Discuss with user if options exhausted

---

**Version:** 1.0
**Last Updated:** 2025-02-01
