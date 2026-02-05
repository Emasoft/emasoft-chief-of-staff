# Performance Report Formats and Procedures

## Contents

- 1. When to use each report format based on analysis needs
  - 1.1 Individual agent performance analysis
  - 1.2 Team/project aggregate performance review
  - 1.3 Cross-project performance comparison
  - 1.4 Time-based trend analysis
- 2. Calculating performance metrics from raw data
  - 2.1 Core metrics: completion, failure, response time, error rate
  - 2.2 Derived metrics: retry rate, duration, patterns, trends
- 3. Querying performance data sources
  - 3.1 AI Maestro API queries for message history
  - 3.2 Reading handoff files for task outcomes
  - 3.3 Parsing agent logs for execution data
- 4. Structuring performance report content
  - 4.1 Report header and metadata format
  - 4.2 Metrics dashboard table structure
  - 4.3 Analysis sections organization
  - 4.4 Recommendations format and prioritization
- 5. Validating report accuracy before delivery
  - 5.1 Metrics verification checklist
  - 5.2 Statistical significance requirements
  - 5.3 Markdown formatting validation
- 6. Identifying performance patterns and trends
  - 6.1 Strength pattern detection criteria
  - 6.2 Weakness pattern identification rules
  - 6.3 Trend analysis methodology
- 7. Delivering reports with actionable summaries
  - 7.1 Success response format
  - 7.2 Failure response format with diagnostics

---

## 1. Report Format Selection

### 1.1 Individual Agent Report

**When to Use**: Detailed performance profile for a single agent; diagnosing specific agent issues; agent comparison baseline.

**Filename Pattern**: `performance-agent-{agent_name}-{date}-{timestamp}.md`

**Contains**:
- Agent identification (name, session, type)
- Summary metrics dashboard
- Task completion breakdown by category
- Response time distribution
- Error analysis with specific failure types
- Strengths identified (consistently successful task types)
- Weaknesses identified (recurring failure patterns)
- Comparison to team average
- Improvement recommendations

**Use Case**: When orchestrator needs to understand why a specific agent is underperforming or to validate that an agent is suitable for specific task types.

### 1.2 Team/Project Report

**When to Use**: Aggregate performance across all agents working on a project; resource allocation decisions; identifying team bottlenecks.

**Filename Pattern**: `performance-project-{project_name}-{date}-{timestamp}.md`

**Contains**:
- Project overview and scope
- Team composition (agents involved)
- Aggregate metrics dashboard
- Per-agent summary table
- Best performing agents (ranked by completion rate)
- Underperforming agents (below threshold)
- Common failure patterns across team
- Bottleneck identification
- Resource allocation recommendations

**Use Case**: When project manager or orchestrator needs to optimize task distribution, identify team-wide issues, or report project health status.

### 1.3 Cross-Project Comparison

**When to Use**: Compare agent performance across multiple projects; identify environmental factors; validate consistency; best practice extraction.

**Filename Pattern**: `performance-comparison-{date}-{timestamp}.md`

**Contains**:
- Projects included in comparison
- Standardized metrics per project
- Project-by-project ranking
- Agent consistency scores (performance variance across projects)
- Environmental factors analysis
- Best practices from top-performing projects
- Recommendations for underperforming projects

**Use Case**: When you need to understand if performance issues are agent-specific or environment-specific; when extracting patterns that work across contexts.

### 1.4 Trend Analysis Report

**When to Use**: Analyze performance changes over time; validate improvement initiatives; forecast future performance; identify seasonal patterns.

**Filename Pattern**: `performance-trend-{period}-{date}-{timestamp}.md`

**Contains**:
- Time period covered (daily, weekly, monthly)
- Metric trends with direction indicators
- Performance trajectory graphs (ASCII)
- Inflection points identified
- Correlation analysis (what improved/degraded together)
- Seasonal patterns if applicable
- Forecast based on current trajectory
- Action items to maintain/improve trends

**Use Case**: When evaluating the impact of skill updates, plugin changes, or workflow modifications; when you need to predict future performance or resource needs.

---

## 2. Performance Metrics Definitions

### 2.1 Core Metrics

| Metric | Description | Calculation | Data Source |
|--------|-------------|-------------|-------------|
| `tasks_completed` | Total tasks successfully finished | Count of tasks with `[DONE]` status | Handoff files, message logs |
| `tasks_failed` | Total tasks that failed | Count of tasks with `[FAILED]` status | Handoff files, message logs |
| `avg_response_time_seconds` | Mean time to first response | Average of (first_response_timestamp - task_assigned_timestamp) | Message timestamps |
| `error_rate` | Percentage of failed tasks | (tasks_failed / total_tasks) * 100 | Derived from task counts |
| `message_response_rate` | Percentage of messages acknowledged | (messages_responded / messages_received) * 100 | AI Maestro message history |

**Calculation Steps for Core Metrics**:

1. **tasks_completed**:
   ```bash
   # Search all handoff files for [DONE] markers
   grep -r "\[DONE\]" thoughts/shared/handoffs/ | wc -l
   ```

2. **tasks_failed**:
   ```bash
   # Search all handoff files for [FAILED] markers
   grep -r "\[FAILED\]" thoughts/shared/handoffs/ | wc -l
   ```

3. **avg_response_time_seconds**:
   ```bash
   # Extract timestamps from message JSON
   # Calculate delta between task_assigned and first_response
   # Average all deltas
   ```

4. **error_rate**:
   ```python
   error_rate = (tasks_failed / (tasks_completed + tasks_failed)) * 100
   ```

5. **message_response_rate**:
   ```python
   # Count messages with "to": agent_name
   messages_received = len([msg for msg in messages if msg["to"] == agent_name])
   # Count messages with "from": agent_name
   messages_sent = len([msg for msg in messages if msg["from"] == agent_name])
   message_response_rate = (messages_sent / messages_received) * 100 if messages_received > 0 else 0
   ```

### 2.2 Derived Metrics

| Metric | Description | Calculation | Purpose |
|--------|-------------|-------------|---------|
| `completion_rate` | Percentage of tasks completed | (tasks_completed / total_tasks) * 100 | Overall success measure |
| `retry_rate` | Tasks requiring multiple attempts | (tasks_with_retries / total_tasks) * 100 | Reliability indicator |
| `avg_task_duration_minutes` | Mean time to complete tasks | Average of (task_completed_timestamp - task_assigned_timestamp) | Efficiency measure |
| `pattern_frequency` | Recurring error occurrence rate | Count of same error type / total_errors | Problem priority indicator |
| `improvement_trend` | Performance change over time | Current_period_metrics - Previous_period_metrics | Progress tracking |

**Calculation Steps for Derived Metrics**:

1. **completion_rate**:
   ```python
   total_tasks = tasks_completed + tasks_failed
   completion_rate = (tasks_completed / total_tasks) * 100 if total_tasks > 0 else 0
   ```

2. **retry_rate**:
   ```python
   # Parse handoff files for retry indicators
   # Count tasks with checkpoint_n where n > 1
   tasks_with_retries = count_tasks_with_multiple_checkpoints()
   retry_rate = (tasks_with_retries / total_tasks) * 100 if total_tasks > 0 else 0
   ```

3. **avg_task_duration_minutes**:
   ```python
   # For each completed task, extract start and end timestamps
   durations = []
   for task in completed_tasks:
       duration = (task.completed_timestamp - task.assigned_timestamp).total_seconds() / 60
       durations.append(duration)
   avg_task_duration_minutes = sum(durations) / len(durations) if durations else 0
   ```

4. **pattern_frequency**:
   ```python
   # Group errors by type
   error_counts = {}
   for error in all_errors:
       error_type = categorize_error(error)
       error_counts[error_type] = error_counts.get(error_type, 0) + 1
   # Calculate frequency for each pattern
   total_errors = len(all_errors)
   pattern_frequencies = {k: (v / total_errors) * 100 for k, v in error_counts.items()}
   ```

5. **improvement_trend**:
   ```python
   # Compare current period to previous period
   improvement_trend = {
       "completion_rate": current.completion_rate - previous.completion_rate,
       "avg_response_time": previous.avg_response_time - current.avg_response_time,  # Lower is better
       "error_rate": previous.error_rate - current.error_rate  # Lower is better
   }
   ```

---

## 3. Data Source Access Procedures

### 3.1 AI Maestro API Queries

**Primary Endpoint**: `http://localhost:23000/api/messages`

**Query Examples**:

```bash
# Get all messages for a specific agent
curl -s "http://localhost:23000/api/messages?agent={agent_name}&action=list" | jq '.'

# Get messages in a time range
curl -s "http://localhost:23000/api/messages?from_date={ISO_date}&to_date={ISO_date}" | jq '.'

# Example: Get last 7 days of messages for helper-agent-generic
from_date=$(date -u -v-7d +"%Y-%m-%dT%H:%M:%SZ")
to_date=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
curl -s "http://localhost:23000/api/messages?agent=helper-agent-generic&from_date=${from_date}&to_date=${to_date}" | jq '.messages'
```

**Expected Response Structure**:
```json
{
  "messages": [
    {
      "id": "msg_12345",
      "from": "orchestrator-master",
      "to": "helper-agent-generic",
      "subject": "Task Assignment",
      "priority": "high",
      "timestamp": "2026-02-01T14:30:22Z",
      "content": {
        "type": "task_assignment",
        "message": "..."
      },
      "status": "read"
    }
  ]
}
```

**Data Extraction**:
- **Task Assignments**: Filter messages where `content.type == "task_assignment"`
- **Task Completions**: Filter messages where `content.message` contains `[DONE]` or `[FAILED]`
- **Response Times**: Calculate delta between received message timestamp and first reply from agent

### 3.2 Handoff File Parsing

**Location**: `thoughts/shared/handoffs/*/`

**File Structure**:
```
thoughts/shared/handoffs/
├── task-001-analyze-code/
│   ├── current.md
│   └── checkpoint_1.md
├── task-002-generate-report/
│   ├── current.md
│   ├── checkpoint_1.md
│   └── checkpoint_2.md
```

**Query Commands**:

```bash
# Find all handoff directories
find thoughts/shared/handoffs -maxdepth 1 -type d

# List all handoff files
find thoughts/shared/handoffs -name "*.md" -type f

# Parse task outcomes
grep -r "\[DONE\]\|\[FAILED\]" thoughts/shared/handoffs/

# Count completed tasks
grep -r "\[DONE\]" thoughts/shared/handoffs/ | wc -l

# Count failed tasks
grep -r "\[FAILED\]" thoughts/shared/handoffs/ | wc -l

# Find tasks with retries (multiple checkpoints)
find thoughts/shared/handoffs -name "checkpoint_*.md" | cut -d'/' -f4 | sort | uniq -c | awk '$1 > 1'
```

**Parsing Handoff Content**:

Each handoff file contains:
- **Agent name**: In header metadata
- **Task description**: In "Task" section
- **Status**: `[DONE]` or `[FAILED]` markers
- **Timestamps**: In metadata or checkpoint names
- **Error details**: In failed task descriptions

**Example Parsing Script**:
```python
import os
import re
from pathlib import Path

def parse_handoff_files(handoffs_dir):
    tasks = []
    for task_dir in Path(handoffs_dir).iterdir():
        if not task_dir.is_dir():
            continue

        current_file = task_dir / "current.md"
        if not current_file.exists():
            continue

        content = current_file.read_text()

        # Extract status
        status = "DONE" if "[DONE]" in content else "FAILED" if "[FAILED]" in content else "UNKNOWN"

        # Count checkpoints (retries)
        checkpoints = list(task_dir.glob("checkpoint_*.md"))
        retry_count = len(checkpoints)

        # Extract agent name
        agent_match = re.search(r'Agent:\s*(\S+)', content)
        agent_name = agent_match.group(1) if agent_match else "unknown"

        tasks.append({
            "task_id": task_dir.name,
            "agent": agent_name,
            "status": status,
            "retries": retry_count
        })

    return tasks
```

### 3.3 Agent Log Access

**Location**: `logs/agents/`

**Query Commands**:

```bash
# Find agent log files
find logs/agents -name "*.log" -type f

# Extract execution timestamps
grep "started\|completed\|failed" logs/agents/{agent_name}.log

# Count errors in agent logs
grep -i "error\|exception\|failed" logs/agents/{agent_name}.log | wc -l
```

---

## 4. Report Template Structures

### 4.1 Universal Report Header

All reports start with this structure:

```markdown
# Performance Report: {Report Type}

**Generated**: {ISO timestamp}
**Period**: {start_date} to {end_date}
**Report ID**: {unique_id}
**Data Sources**: {list of sources queried}

---

## Executive Summary

{2-3 sentence overview with key findings}

---
```

**Field Definitions**:
- `{Report Type}`: Individual Agent | Team/Project | Cross-Project Comparison | Trend Analysis
- `{ISO timestamp}`: `YYYY-MM-DDTHH:MM:SSZ` format
- `{start_date}`, `{end_date}`: `YYYY-MM-DD` format
- `{unique_id}`: `{report_type}-{target}-{timestamp_compact}` (e.g., `individual-helper-agent-generic-20260201143022`)
- `{list of sources queried}`: AI Maestro API, Handoff files, Agent logs, Session records

### 4.2 Metrics Dashboard Format

Use this table structure for all metric displays:

```markdown
## Metrics Dashboard

| Metric | Value | Trend | Status |
|--------|-------|-------|--------|
| Tasks Completed | {n} | {direction} | {status_emoji} |
| Tasks Failed | {n} | {direction} | {status_emoji} |
| Avg Response Time | {n}s | {direction} | {status_emoji} |
| Error Rate | {n}% | {direction} | {status_emoji} |
| Message Response Rate | {n}% | {direction} | {status_emoji} |
| Completion Rate | {n}% | {direction} | {status_emoji} |
| Avg Task Duration | {n}m | {direction} | {status_emoji} |
```

**Trend Indicators**:
- `↑` - Upward trend (good for completion rate, bad for error rate)
- `↓` - Downward trend (bad for completion rate, good for error rate)
- `→` - No significant change (within 5% variance)

**Status Emojis**:
- `✅` - Excellent (>90% for positive metrics, <10% for negative metrics)
- `⚠️` - Good (70-90% for positive metrics, 10-30% for negative metrics)
- `❌` - Needs improvement (<70% for positive metrics, >30% for negative metrics)

**Positive Metrics**: completion_rate, message_response_rate
**Negative Metrics**: error_rate, avg_response_time, avg_task_duration
**Context-Dependent**: tasks_completed (depends on workload), tasks_failed (absolute count)

### 4.3 Individual Agent Report Template

```markdown
# Performance Report: Individual Agent

**Generated**: {timestamp}
**Period**: {start_date} to {end_date}
**Agent**: {agent_name}
**Session**: {session_name}
**Report ID**: {unique_id}

---

## Executive Summary

{agent_name} completed {completion_rate}% of tasks over {period_days} days with an average response time of {avg_response_time}s. {Summary of key strength}. {Summary of key weakness}.

---

## Metrics Dashboard

| Metric | Value | Trend | Status |
|--------|-------|-------|--------|
| Tasks Completed | {n} | {direction} | {status_emoji} |
| Tasks Failed | {n} | {direction} | {status_emoji} |
| Completion Rate | {n}% | {direction} | {status_emoji} |
| Avg Response Time | {n}s | {direction} | {status_emoji} |
| Error Rate | {n}% | {direction} | {status_emoji} |
| Message Response Rate | {n}% | {direction} | {status_emoji} |
| Avg Task Duration | {n}m | {direction} | {status_emoji} |

---

## Task Breakdown by Category

| Task Type | Completed | Failed | Success Rate |
|-----------|-----------|--------|--------------|
| {category_1} | {n} | {n} | {n}% |
| {category_2} | {n} | {n} | {n}% |
| {category_3} | {n} | {n} | {n}% |

---

## Response Time Distribution

| Percentile | Response Time |
|------------|---------------|
| P50 (Median) | {n}s |
| P75 | {n}s |
| P90 | {n}s |
| P95 | {n}s |
| P99 | {n}s |

---

## Error Analysis

### Error Types

| Error Type | Occurrences | Percentage |
|------------|-------------|------------|
| {error_type_1} | {n} | {n}% |
| {error_type_2} | {n} | {n}% |
| {error_type_3} | {n} | {n}% |

### Recurring Patterns

{List errors that occurred 3+ times with specific examples}

---

## Strengths Identified

- **{Strength_1}**: {Evidence with specific metrics}
- **{Strength_2}**: {Evidence with specific metrics}
- **{Strength_3}**: {Evidence with specific metrics}

---

## Weaknesses Identified

- **{Weakness_1}**: {Evidence with specific metrics and examples}
- **{Weakness_2}**: {Evidence with specific metrics and examples}
- **{Weakness_3}**: {Evidence with specific metrics and examples}

---

## Comparison to Team Average

| Metric | Agent | Team Avg | Difference |
|--------|-------|----------|------------|
| Completion Rate | {n}% | {n}% | {+/-n}% |
| Avg Response Time | {n}s | {n}s | {+/-n}s |
| Error Rate | {n}% | {n}% | {+/-n}% |

---

## Improvement Recommendations

### Priority 1: Critical

**Issue**: {specific problem identified}
**Evidence**: {data supporting the issue}
**Recommendation**: {specific action to take}
**Expected Impact**: {quantified improvement potential}

### Priority 2: Important

{Same structure}

### Priority 3: Nice to Have

{Same structure}

---

**Data Sources**: {list}
**Analysis Date**: {date}
**Next Review**: {suggested_date}
```

### 4.4 Team/Project Report Template

```markdown
# Performance Report: Team/Project

**Generated**: {timestamp}
**Period**: {start_date} to {end_date}
**Project**: {project_name}
**Report ID**: {unique_id}

---

## Executive Summary

Team of {n} agents completed {aggregate_completion_rate}% of tasks over {period_days} days. {Summary of team performance}. {Key bottleneck identified}. {Top performer highlight}.

---

## Project Overview

**Project**: {project_name}
**Scope**: {brief description}
**Team Size**: {n} agents
**Total Tasks**: {n}
**Time Period**: {start_date} to {end_date}

---

## Aggregate Metrics Dashboard

| Metric | Value | Trend | Status |
|--------|-------|-------|--------|
| Total Tasks Completed | {n} | {direction} | {status_emoji} |
| Total Tasks Failed | {n} | {direction} | {status_emoji} |
| Aggregate Completion Rate | {n}% | {direction} | {status_emoji} |
| Team Avg Response Time | {n}s | {direction} | {status_emoji} |
| Team Error Rate | {n}% | {direction} | {status_emoji} |

---

## Per-Agent Summary

| Agent | Tasks Completed | Tasks Failed | Completion Rate | Avg Response Time | Status |
|-------|----------------|--------------|-----------------|-------------------|--------|
| {agent_1} | {n} | {n} | {n}% | {n}s | {status_emoji} |
| {agent_2} | {n} | {n} | {n}% | {n}s | {status_emoji} |
| {agent_3} | {n} | {n} | {n}% | {n}s | {status_emoji} |

---

## Best Performing Agents

1. **{agent_name}** - {completion_rate}% completion rate
   - Strength: {specific strength}
   - Best at: {task types}

2. **{agent_name}** - {completion_rate}% completion rate
   - Strength: {specific strength}
   - Best at: {task types}

---

## Underperforming Agents

1. **{agent_name}** - {completion_rate}% completion rate
   - Issue: {specific issue}
   - Recommended action: {action}

---

## Common Failure Patterns

### Pattern 1: {pattern_name}

- **Occurrences**: {n} times across {n} agents
- **Affected Agents**: {list}
- **Impact**: {description}
- **Root Cause**: {analysis}

### Pattern 2: {pattern_name}

{Same structure}

---

## Bottleneck Identification

### Primary Bottleneck: {bottleneck_description}

- **Evidence**: {specific data}
- **Impact**: {quantified delay or failure rate}
- **Recommendation**: {specific action}

---

## Resource Allocation Recommendations

1. **{Recommendation_1}**: {Details about task redistribution or agent reallocation}
2. **{Recommendation_2}**: {Details about skill improvements needed}
3. **{Recommendation_3}**: {Details about workflow optimization}

---

**Data Sources**: {list}
**Analysis Date**: {date}
**Next Review**: {suggested_date}
```

### 4.5 Improvement Recommendations Format

**Priority Structure**:

```markdown
## Improvement Recommendations

### Priority 1: Critical

**Issue**: {Specific problem identified with metrics}
**Evidence**: {Data supporting the issue - include numbers, frequencies, examples}
**Recommendation**: {Specific, actionable step to take}
**Expected Impact**: {Quantified improvement potential - e.g., "Expected to reduce error rate by 15%"}
**Implementation**: {How to implement - which tool/skill/workflow to modify}

### Priority 2: Important

{Same structure}

### Priority 3: Nice to Have

{Same structure}
```

**Recommendation Categories**:

1. **Plugin Improvements**:
   ```markdown
   **Issue**: Agent lacks specialized skills for {task_type}
   **Evidence**: 45% failure rate on {task_type} tasks vs 10% on other types
   **Recommendation**: Add {skill_name} skill to agent's skill list
   **Expected Impact**: Reduce failure rate to <15% for {task_type}
   **Implementation**: Update agent YAML frontmatter to include {skill_name}
   ```

2. **Agent Configuration**:
   ```markdown
   **Issue**: Agent timeout threshold too low for {task_type}
   **Evidence**: 8 out of 12 failures were timeout errors on large file operations
   **Recommendation**: Increase timeout from 30s to 60s for file operations
   **Expected Impact**: Eliminate timeout-based failures (67% of current errors)
   **Implementation**: Modify agent configuration in plugin manifest
   ```

3. **Workflow Optimization**:
   ```markdown
   **Issue**: Sequential task execution causing delays
   **Evidence**: Average task duration 25m when dependent tasks wait; 8m when parallel
   **Recommendation**: Identify tasks that can run in parallel and update workflow
   **Expected Impact**: Reduce average project completion time by 40%
   **Implementation**: Update orchestrator's task dependency graph
   ```

4. **Resource Allocation**:
   ```markdown
   **Issue**: {agent_name} overloaded with 60% of tasks
   **Evidence**: Response time degraded from 12s to 35s as task queue grew
   **Recommendation**: Distribute {task_type} tasks to {agent_2} and {agent_3}
   **Expected Impact**: Restore response time to <15s, balance team workload
   **Implementation**: Update orchestrator's agent selection logic for {task_type}
   ```

5. **Training Data**:
   ```markdown
   **Issue**: Agent unfamiliar with {specific_scenario}
   **Evidence**: 5 failures on {scenario} with similar error pattern
   **Recommendation**: Add {scenario} examples to {skill_name} skill references
   **Expected Impact**: Enable agent to handle {scenario} successfully
   **Implementation**: Create new reference doc in skill's references/ directory
   ```

---

## 5. Report Validation Procedures

### 5.1 Metrics Verification Checklist

Before delivering any report, verify:

- [ ] **Division by Zero Handled**: All percentage calculations check denominator > 0
- [ ] **Data Points Sufficient**: Minimum 10 data points for statistical significance
- [ ] **Timestamp Consistency**: All dates/times in consistent format (ISO 8601)
- [ ] **Metric Boundaries**: No negative percentages, no values > 100% for rates
- [ ] **Trend Direction Correct**: Upward/downward/stable correctly assigned
- [ ] **Status Emoji Logic**: Thresholds correctly applied (✅ >90%, ⚠️ 70-90%, ❌ <70%)
- [ ] **Comparison Baseline Valid**: Team averages or previous period data exists
- [ ] **Error Categorization Consistent**: Same error types grouped together
- [ ] **Response Time Units Clear**: Specify seconds/minutes/hours explicitly

**Example Validation Code**:

```python
def validate_metrics(metrics):
    errors = []

    # Check division by zero
    if metrics.get("total_tasks", 0) == 0:
        errors.append("Cannot calculate rates: total_tasks is 0")

    # Check percentage boundaries
    for key in ["completion_rate", "error_rate", "message_response_rate"]:
        value = metrics.get(key)
        if value is not None and (value < 0 or value > 100):
            errors.append(f"{key} out of bounds: {value}%")

    # Check data sufficiency
    if metrics.get("total_tasks", 0) < 10:
        errors.append(f"Insufficient data: only {metrics['total_tasks']} tasks")

    # Check timestamp format
    for key in ["start_date", "end_date"]:
        date_str = metrics.get(key)
        if date_str:
            try:
                datetime.fromisoformat(date_str)
            except ValueError:
                errors.append(f"{key} invalid ISO format: {date_str}")

    return errors
```

### 5.2 Statistical Significance Requirements

**Minimum Data Points**:
- Individual agent report: ≥10 tasks
- Team report: ≥30 tasks total (or ≥10 per agent)
- Trend analysis: ≥20 data points across time period
- Cross-project comparison: ≥10 tasks per project

**Pattern Detection Thresholds**:
- Recurring error: ≥3 occurrences of same error type
- Strength pattern: ≥90% success rate over ≥5 tasks
- Weakness pattern: ≤70% success rate over ≥5 tasks
- Trend significance: ≥10% change between periods

**Insufficient Data Handling**:

```markdown
## Data Sufficiency Warning

⚠️ **Limited Data Available**

This report is based on only {n} tasks, which is below the recommended minimum of 10 tasks for statistical significance. Findings should be considered preliminary.

**Recommendation**: Collect data for at least {required - current} more tasks before drawing firm conclusions.
```

### 5.3 Markdown Formatting Validation

**Validation Checklist**:
- [ ] All tables have header row with separator (`|---|---|`)
- [ ] All table cells aligned (consistent `|` placement)
- [ ] Code blocks use triple backticks with language identifier
- [ ] Headers use consistent hierarchy (single `#` for title, `##` for sections)
- [ ] No broken internal links (all `[text](path)` links point to valid files)
- [ ] Lists use consistent markers (`-` for unordered, `1.` for ordered)
- [ ] No trailing whitespace at end of lines
- [ ] File ends with single newline

**Automated Validation Script**:

```bash
# Check table formatting
grep -n "^|" report.md | awk -F'|' 'NF != prev_nf && prev_nf != 0 {print "Line " NR ": inconsistent columns"} {prev_nf = NF}'

# Check code block closure
awk '/```/{count++} END{if(count%2!=0) print "Unclosed code block"}' report.md

# Check header hierarchy
awk '/^#{1,6} /{match($0, /^#+/); len=RLENGTH; if(len>prev+1 && prev!=0) print "Line " NR ": skipped header level"; prev=len}' report.md

# Validate markdown with markdownlint (if installed)
markdownlint report.md
```

---

## 6. Pattern Identification Methodology

### 6.1 Strength Pattern Detection

**Criteria for Identifying Strengths**:

1. **High Success Rate**: Task category with ≥90% completion rate AND ≥5 tasks
2. **Fast Response**: Avg response time ≤15s AND ≤20% variance
3. **Reliable Messaging**: Message response rate ≥90% AND ≤2 missed messages
4. **Consistent Quality**: ≤5% retry rate for task category

**Strength Pattern Template**:

```markdown
- **{Strength Name}**: {Brief description}
  - Evidence: {completion_rate}% success rate across {n} tasks
  - Performance: {specific metric} compared to {baseline}
  - Consistency: {variance description}
```

**Example**:

```markdown
- **Excellent File Operations**: Reliable and fast file read/write/edit tasks
  - Evidence: 95% success rate across 23 file operation tasks
  - Performance: Avg 8s response time (vs team avg 18s)
  - Consistency: Only 1 retry required (4% retry rate)
```

### 6.2 Weakness Pattern Identification

**Criteria for Identifying Weaknesses**:

1. **Low Success Rate**: Task category with ≤70% completion rate AND ≥5 tasks
2. **Recurring Errors**: Same error type ≥3 times
3. **Slow Response**: Avg response time ≥40s OR >50% variance
4. **Poor Messaging**: Message response rate ≤70%
5. **High Retry Rate**: ≥20% of tasks require multiple attempts

**Weakness Pattern Template**:

```markdown
- **{Weakness Name}**: {Brief description of the issue}
  - Evidence: {error_rate}% failure rate across {n} tasks
  - Error Type: {specific error category}
  - Impact: {quantified impact on project/workflow}
  - Frequency: {how often this occurs}
```

**Example**:

```markdown
- **Timeout on Large Files**: Recurring failures when processing files >10MB
  - Evidence: 8 out of 12 large file tasks failed (67% failure rate)
  - Error Type: "TimeoutError: operation exceeded 30s limit"
  - Impact: Blocks data processing workflow, 2-hour avg delay per occurrence
  - Frequency: 3 times in last 7 days
```

### 6.3 Trend Analysis Methodology

**Step 1: Segment Time Period**

Divide analysis period into equal segments:
- Daily trends: 4-6 hour segments
- Weekly trends: Daily segments
- Monthly trends: Weekly segments

**Step 2: Calculate Metrics Per Segment**

For each segment, compute:
- Completion rate
- Average response time
- Error rate
- Task throughput (tasks per hour/day)

**Step 3: Identify Trend Direction**

```python
def calculate_trend(values):
    """
    Returns: "improving", "degrading", or "stable"
    """
    if len(values) < 3:
        return "insufficient_data"

    # Linear regression slope
    x = list(range(len(values)))
    y = values
    slope = calculate_slope(x, y)

    # Threshold: 5% change required for significance
    threshold = 0.05 * (max(values) - min(values))

    if abs(slope) < threshold:
        return "stable"
    elif slope > 0:
        return "improving"  # For positive metrics
    else:
        return "degrading"  # For positive metrics
```

**Step 4: Identify Inflection Points**

Inflection point = segment where trend changed direction significantly (>15% swing)

```python
def find_inflection_points(values, threshold=0.15):
    inflections = []
    for i in range(1, len(values) - 1):
        prev_delta = values[i] - values[i-1]
        next_delta = values[i+1] - values[i]

        # Direction change with significant magnitude
        if prev_delta * next_delta < 0:  # Opposite signs
            magnitude = abs(next_delta - prev_delta) / values[i]
            if magnitude >= threshold:
                inflections.append({
                    "segment": i,
                    "value": values[i],
                    "change_magnitude": magnitude
                })

    return inflections
```

**Step 5: Correlate Metrics**

Identify which metrics moved together:

```python
def correlate_metrics(metric1_values, metric2_values):
    """
    Calculate Pearson correlation coefficient
    Returns: correlation value between -1 and 1
    """
    correlation = pearson_correlation(metric1_values, metric2_values)

    if correlation > 0.7:
        return "strong_positive"
    elif correlation < -0.7:
        return "strong_negative"
    elif abs(correlation) < 0.3:
        return "no_correlation"
    else:
        return "weak_correlation"
```

**Trend Report Section Template**:

```markdown
## Metric Trends

### Completion Rate: {direction} {emoji}

- **Period Start**: {value}%
- **Period End**: {value}%
- **Change**: {+/-}% ({percentage_change}%)
- **Trajectory**: {linear/exponential/plateaued}

### Response Time: {direction} {emoji}

- **Period Start**: {value}s
- **Period End**: {value}s
- **Change**: {+/-}s ({percentage_change}%)
- **Trajectory**: {linear/exponential/plateaued}

## Inflection Points

### Week 3 (2026-01-15 to 2026-01-21)

- **Event**: Completion rate jumped from 71% to 83% (+12%)
- **Correlated Changes**:
  - Response time decreased from 18s to 14s (-22%)
  - Error rate decreased from 15% to 9% (-40%)
- **Possible Cause**: Skill updates deployed on 2026-01-14
- **Recommendation**: Document skill changes as best practice template

## Metric Correlations

| Metric Pair | Correlation | Interpretation |
|-------------|-------------|----------------|
| Completion Rate ↔ Response Time | -0.82 (strong negative) | Faster response = higher completion |
| Error Rate ↔ Retry Rate | +0.91 (strong positive) | More errors = more retries needed |
| Task Duration ↔ File Size | +0.65 (moderate positive) | Larger files = longer tasks |
```

---

## 7. Report Delivery Formats

### 7.1 Success Response Format

When report generation succeeds, return:

```
[DONE] ecos-performance-reporter: {report_type} report generated

Summary: {one-line key finding}
Output: {absolute_file_path}
Period: {start_date} to {end_date}
Data Points: {count}

Key Findings:
- {finding_1}
- {finding_2}
- {finding_3}
```

**Field Requirements**:
- `{report_type}`: Must match one of: individual, team, comparison, trend
- `{one-line key finding}`: Max 120 characters, highlights most important result
- `{absolute_file_path}`: Full path to generated report file (not relative)
- `{start_date}`, `{end_date}`: ISO format dates
- `{count}`: Total tasks analyzed (or messages, or data points)
- `{finding_n}`: Each ≤80 characters, actionable insight

**Example**:

```
[DONE] ecos-performance-reporter: individual report generated

Summary: helper-agent-generic shows 87% completion rate with fast response times
Output: /Users/emanuelesabetta/Code/SKILL_FACTORY/docs_dev/reports/performance-agent-helper-agent-generic-2026-02-01-143022.md
Period: 2026-01-25 to 2026-02-01
Data Points: 23 tasks analyzed

Key Findings:
- Strength: Excellent response time (avg 12s, team avg 18s)
- Strength: High success rate on file operations (95% vs 78% team avg)
- Weakness: Recurring timeout errors on large file processing (3 occurrences)
```

### 7.2 Failure Response Format

When report generation fails, return:

```
[FAILED] ecos-performance-reporter: {report_type} report generation failed

Reason: {specific error description}
Missing Data: {unavailable sources}
Attempted Period: {start_date} to {end_date}
Partial Report: {YES/NO}
{if YES: Output: {file_path}}
```

**Field Requirements**:
- `{specific error description}`: Technical but clear explanation of what went wrong
- `{unavailable sources}`: List specific data sources that couldn't be accessed
- `Partial Report`: YES if some analysis was completed and saved; NO otherwise
- If YES, provide file path to partial results

**Example - Complete Failure**:

```
[FAILED] ecos-performance-reporter: team report generation failed

Reason: AI Maestro API unreachable at http://localhost:23000/api/messages
Missing Data: Message history, task assignments
Attempted Period: 2026-01-25 to 2026-02-01
Partial Report: NO
```

**Example - Partial Success**:

```
[FAILED] ecos-performance-reporter: trend report generation failed

Reason: Insufficient data points for week 1 (only 3 tasks, min 10 required)
Missing Data: Week 1 (2026-01-01 to 2026-01-07) task history
Attempted Period: 2026-01-01 to 2026-02-01
Partial Report: YES
Output: /Users/emanuelesabetta/Code/SKILL_FACTORY/docs_dev/reports/performance-trend-partial-2026-02-01-145530.md

Note: Partial report covers weeks 2-4 only. Week 1 excluded due to insufficient data.
```

---

## Best Practices Summary

1. **Data Integrity**: Only report on verified data; flag uncertain metrics with ⚠️ warning symbol
2. **Statistical Significance**: Require minimum data points before drawing conclusions (n ≥ 10)
3. **Actionable Output**: Every weakness must have a corresponding recommendation
4. **Trend Context**: Always compare current metrics to historical baseline when available
5. **Objective Analysis**: Report facts without subjective interpretation; let data speak
6. **Privacy Consideration**: Aggregate sensitive data; avoid exposing individual failures in public reports
7. **Consistent Formatting**: Use Unicode table borders, ISO timestamps, standardized emojis
8. **Validation Before Delivery**: Run full validation checklist on every report before writing to file
9. **Clear File Naming**: Use descriptive, timestamped filenames for easy sorting and retrieval
10. **Complete Documentation**: Include data sources, analysis date, and next review date in every report

---

## Quick Reference: Report Type Selection Matrix

| Need | Report Type | Key Benefit |
|------|-------------|-------------|
| Diagnose specific agent issue | Individual | Detailed failure analysis, task-level breakdown |
| Optimize team resource allocation | Team/Project | Identifies bottlenecks, load balancing insights |
| Validate agent consistency | Cross-Project Comparison | Environmental vs agent-specific issues |
| Measure improvement over time | Trend Analysis | Validates impact of changes, forecasts future |
| Justify plugin/skill investment | Any + Recommendations | Data-driven improvement suggestions |
| Quick health check | Individual or Team | Metrics dashboard provides instant overview |

---

**End of Report Formats Reference**
