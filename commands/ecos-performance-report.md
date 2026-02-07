---
name: ecos-performance-report
description: "Generate agent performance report with metrics, strengths, and improvement areas"
argument-hint: "[--agent SESSION_NAME] [--period DAYS] [--project PROJECT_ID]"
user-invocable: true
allowed-tools: ["Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/ecos_performance_report.py:*)"]
---

# Performance Report Command

Generate a comprehensive performance report for AI Maestro agents. Shows task completion metrics, response times, error rates, and identifies strengths and areas for improvement.

## Usage

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ecos_performance_report.py" $ARGUMENTS
```

## What This Command Does

1. **Collects Performance Metrics**
   - Tasks assigned vs completed
   - Average task completion time
   - Error and retry rates
   - Message response latency

2. **Analyzes Agent Effectiveness**
   - Success rate by task type
   - Code quality metrics (if available)
   - Test pass rates for submitted code
   - Review feedback scores

3. **Identifies Patterns**
   - Strengths: Task types with high success
   - Weaknesses: Task types with failures/retries
   - Trends: Improvement or degradation over time

4. **Generates Recommendations**
   - Skill training suggestions
   - Workload balancing advice
   - Configuration optimizations

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--agent SESSION_NAME` | No | Specific agent (default: all agents) |
| `--period DAYS` | No | Analysis period in days (default: 7) |
| `--project PROJECT_ID` | No | Filter by GitHub project ID |
| `--format text|json|csv` | No | Output format (default: text) |
| `--compare` | No | Include comparison to previous period |
| `--detailed` | No | Include per-task breakdown |

## Examples

### Report for all agents (last 7 days)

```bash
/ecos-performance-report
```

### Report for specific agent

```bash
/ecos-performance-report --agent libs-svg-svgbbox
```

### Last 30 days with comparison

```bash
/ecos-performance-report --period 30 --compare
```

### Filter by project

```bash
/ecos-performance-report --project PVT_kwDOABC123 --period 14
```

### Detailed CSV export

```bash
/ecos-performance-report --format csv --detailed
```

## Output Example

```
╔════════════════════════════════════════════════════════════════╗
║                  AGENT PERFORMANCE REPORT                      ║
║                  Period: 2026-01-25 to 2026-02-01 (7 days)     ║
╠════════════════════════════════════════════════════════════════╣
║ OVERVIEW                                                       ║
╠════════════════════════════════════════════════════════════════╣
║ Total Agents: 4                                                ║
║ Total Tasks Assigned: 156                                      ║
║ Total Tasks Completed: 142                                     ║
║ Overall Success Rate: 91.0%                                    ║
║ Average Completion Time: 2h 34m                                ║
╠════════════════════════════════════════════════════════════════╣
║ AGENT SUMMARY                                                  ║
╠════════════════════════════════════════════════════════════════╣
║ Agent Name              │ Tasks │ Success │ Avg Time │ Rating  ║
║─────────────────────────────────────────────────────────────── ║
║ orchestrator-master     │ 45    │ 95.6%   │ 1h 12m   │ ★★★★★   ║
║ libs-svg-svgbbox        │ 38    │ 92.1%   │ 3h 05m   │ ★★★★    ║
║ helper-agent-generic    │ 52    │ 88.5%   │ 2h 48m   │ ★★★★    ║
║ claude-skills-factory   │ 21    │ 85.7%   │ 4h 21m   │ ★★★     ║
╠════════════════════════════════════════════════════════════════╣
║ TASK TYPE BREAKDOWN                                            ║
╠════════════════════════════════════════════════════════════════╣
║ Task Type               │ Count │ Success │ Avg Time           ║
║─────────────────────────────────────────────────────────────── ║
║ Implementation          │ 68    │ 89.7%   │ 3h 45m             ║
║ Bug Fix                 │ 42    │ 95.2%   │ 1h 20m             ║
║ Code Review             │ 28    │ 96.4%   │ 45m                ║
║ Documentation           │ 12    │ 91.7%   │ 2h 10m             ║
║ Testing                 │ 6     │ 66.7%   │ 5h 30m             ║
╠════════════════════════════════════════════════════════════════╣
║ STRENGTHS                                                      ║
╠════════════════════════════════════════════════════════════════╣
║ ✓ orchestrator-master: Excellent at code review (100% success) ║
║ ✓ libs-svg-svgbbox: Fast bug fixes (avg 52m)                   ║
║ ✓ Overall: High success rate on documentation tasks            ║
╠════════════════════════════════════════════════════════════════╣
║ AREAS FOR IMPROVEMENT                                          ║
╠════════════════════════════════════════════════════════════════╣
║ ✗ Testing tasks: 66.7% success rate (below 80% threshold)      ║
║ ✗ claude-skills-factory: Long completion times (4h+ avg)       ║
║ ✗ helper-agent-generic: High retry rate on complex tasks       ║
╠════════════════════════════════════════════════════════════════╣
║ RECOMMENDATIONS                                                ║
╠════════════════════════════════════════════════════════════════╣
║ 1. Add testing-specific skills to agents handling test tasks   ║
║ 2. Consider splitting large tasks for claude-skills-factory    ║
║ 3. Route complex tasks to orchestrator-master (highest rating) ║
╚════════════════════════════════════════════════════════════════╝
```

## Performance Metrics Explained

| Metric | Description | Good Threshold |
|--------|-------------|----------------|
| Success Rate | Tasks completed without errors | >90% |
| Avg Completion Time | Mean time from assignment to done | <4 hours |
| Retry Rate | Tasks requiring multiple attempts | <10% |
| Response Latency | Time to first response | <5 minutes |
| Error Rate | Tasks failed without completion | <5% |

## Rating Calculation

Agent ratings (1-5 stars) are calculated based on:
- Success rate (40% weight)
- Average completion time (30% weight)
- Error rate (20% weight)
- Retry rate (10% weight)

## Data Sources

Performance data is collected from:
- AI Maestro message logs
- GitHub issue/PR tracking
- Agent session logs
- Task completion reports

## Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| "No data available" | No tasks in period | Extend period or check agent activity |
| "Agent not found" | Invalid SESSION_NAME | Verify agent name |
| "AI Maestro unavailable" | API not running | Start AI Maestro service |
| "Insufficient history" | Period exceeds log retention | Use shorter period |

## Prerequisites

- AI Maestro must be running (use `ai-maestro-agents-management` skill to verify)
- Agents must have activity logs available
- For project filtering: GitHub API access required

## Notes

- Performance data is refreshed every 15 minutes
- Historical data is retained for 90 days by default
- Comparisons show percentage change from previous period
- Use `--detailed` for per-task debugging but expect longer output

## Related Commands

- `/ecos-resource-report` - System resource monitoring
- `/ecos-orchestration-status` - Current orchestration state
- `/ecos-planning-status` - Planning phase progress
