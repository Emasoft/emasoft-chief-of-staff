---
procedure: support-skill
workflow-instruction: support
operation: analyze-strengths-weaknesses
parent-skill: ecos-performance-tracking
---

# Operation: Analyze Strengths and Weaknesses


## Contents

- [Purpose](#purpose)
- [When To Use This Operation](#when-to-use-this-operation)
- [Steps](#steps)
  - [Step 1: Review Collected Metrics](#step-1-review-collected-metrics)
  - [Step 2: Identify Performance Patterns](#step-2-identify-performance-patterns)
  - [Step 3: Compare Against Benchmarks](#step-3-compare-against-benchmarks)
  - [Step 4: Document Findings](#step-4-document-findings)
- [Strengths](#strengths)
- [Weaknesses](#weaknesses)
- [Recommendations](#recommendations)
  - [Step 5: Make Recommendations](#step-5-make-recommendations)
- [Checklist](#checklist)
- [Example Analysis Output](#example-analysis-output)
- [Strengths](#strengths)
- [Weaknesses](#weaknesses)
- [Recommendations](#recommendations)
- [Output](#output)
- [Related References](#related-references)
- [Next Operation](#next-operation)

## Purpose

Identify what each agent does well and where they struggle, enabling better task assignment and team optimization.

## When To Use This Operation

- When making role assignments
- After performance issues arise
- During team planning
- Weekly performance reviews
- Before major project phases

## Steps

### Step 1: Review Collected Metrics

Gather metrics for the agent being analyzed:

```bash
# Get all task completions for an agent
cat $CLAUDE_PROJECT_DIR/.ecos/metrics/task-completions.jsonl | \
  jq -s '[.[] | select(.agent == "AGENT_NAME")]'
```

### Step 2: Identify Performance Patterns

Look for patterns in:

**Task Type Performance:**
```markdown
| Task Type | Count | Completion Rate | On-Time Rate | First-Pass Rate |
|-----------|-------|-----------------|--------------|-----------------|
| Implementation | 10 | 90% | 80% | 85% |
| Code Review | 15 | 100% | 95% | 95% |
| Debugging | 5 | 80% | 60% | 70% |
| Testing | 8 | 100% | 90% | 100% |
```

**Time-Based Performance:**
- Morning vs afternoon
- Start of week vs end
- Complex vs simple tasks

### Step 3: Compare Against Benchmarks

**Team Benchmarks:**
- Average completion rate: 90%
- Average on-time rate: 85%
- Average first-pass quality: 80%

**Individual vs Benchmark:**
```markdown
| Metric | Agent | Benchmark | Delta |
|--------|-------|-----------|-------|
| Completion rate | 95% | 90% | +5% (strength) |
| On-time rate | 70% | 85% | -15% (weakness) |
| First-pass quality | 90% | 80% | +10% (strength) |
```

### Step 4: Document Findings

```markdown
# Agent Analysis: [agent-name]

Period: [start] to [end]
Tasks analyzed: [count]

## Strengths

1. **[Strength 1]**: [Evidence]
   - Metric: [value] vs benchmark [benchmark]
   - Impact: [how this benefits the team]

2. **[Strength 2]**: [Evidence]
   - Metric: [value] vs benchmark [benchmark]
   - Impact: [how this benefits the team]

## Weaknesses

1. **[Weakness 1]**: [Evidence]
   - Metric: [value] vs benchmark [benchmark]
   - Root cause: [if known]
   - Mitigation: [suggested approach]

2. **[Weakness 2]**: [Evidence]
   - Metric: [value] vs benchmark [benchmark]
   - Root cause: [if known]
   - Mitigation: [suggested approach]

## Recommendations

1. **Task Assignment**: [What tasks to assign/avoid]
2. **Pairing**: [Who to pair with for weak areas]
3. **Focus Areas**: [What to improve]
```

### Step 5: Make Recommendations

Based on analysis:

| Strength/Weakness | Recommendation |
|-------------------|----------------|
| Strong at code review | Assign code review tasks |
| Weak at estimation | Provide estimates for review |
| Strong at testing | Lead test initiatives |
| Weak at documentation | Require documentation checklist |

## Checklist

Copy this checklist and track your progress:

- [ ] Metrics for agent retrieved
- [ ] Task type performance analyzed
- [ ] Time-based patterns identified
- [ ] Compared against benchmarks
- [ ] Strengths documented (with evidence)
- [ ] Weaknesses documented (with evidence)
- [ ] Root causes identified where possible
- [ ] Recommendations made
- [ ] Analysis saved to agent profile

## Example Analysis Output

```markdown
# Agent Analysis: helper-agent-generic

## Strengths
1. **Code Review Speed**: Completes reviews 25% faster than average
   - 15 reviews, average 1.2 hours vs team average 1.6 hours
2. **First-Pass Quality**: 90% of code passes review on first attempt
   - 10 tasks, 9 passed first review
3. **Communication**: Clear, concise status updates
   - Average response time: 5 minutes

## Weaknesses
1. **Complex Algorithms**: Struggles with optimization tasks
   - 3 algorithm tasks, 33% on-time rate
   - Root cause: Limited optimization experience
2. **Documentation**: Often leaves docs incomplete
   - 40% of tasks required documentation rework
3. **Estimation**: Underestimates by average of 30%
   - 10 tasks, average overrun 1.3 hours

## Recommendations
- Assign code review tasks (strength)
- Pair with senior agent for algorithm work
- Require documentation checklist for all tasks
- Add 30% buffer to estimates
```

## Output

After completing this operation:
- Strengths identified with evidence
- Weaknesses identified with mitigation strategies
- Recommendations for task assignment
- Agent profile updated

## Related References

- [strength-weakness-analysis.md](strength-weakness-analysis.md) - Complete analysis guide
- [performance-metrics.md](performance-metrics.md) - Metric definitions

## Next Operation

After analysis: [op-generate-performance-report.md](op-generate-performance-report.md)
