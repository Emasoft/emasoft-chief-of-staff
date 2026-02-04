# Performance Report Template

This template defines the standard format for agent performance reports requested by Chief of Staff.

## Report Metadata

```yaml
---
report_id: "perf-{agent_session}-{date}"
agent_session: "{session_name}"
role: "architect" | "orchestrator" | "integrator"
generated: "ISO-8601 timestamp"
period_start: "ISO-8601 timestamp"
period_end: "ISO-8601 timestamp"
report_type: "full" | "summary" | "metrics_only"
---
```

## Executive Summary

**Agent**: {session_name}
**Role**: {role}
**Reporting Period**: {period_start} to {period_end}
**Overall Status**: Healthy | Warning | Critical

### Key Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Tasks Completed | X | Y | OK/WARN/CRIT |
| Tasks Failed | X | <Y | OK/WARN/CRIT |
| Average Duration | Xm | <Ym | OK/WARN/CRIT |
| Blockers Encountered | X | <Y | OK/WARN/CRIT |
| Approvals Requested | X | - | INFO |

---

## Task Performance

### Completed Tasks

| Task ID | Description | Duration | Result |
|---------|-------------|----------|--------|
| task-001 | {description} | 15m | success |
| task-002 | {description} | 30m | success |

### Failed Tasks

| Task ID | Description | Failure Reason | Recovery Action |
|---------|-------------|----------------|-----------------|
| task-003 | {description} | {reason} | {action_taken} |

### In-Progress Tasks

| Task ID | Description | Progress | ETA | Blockers |
|---------|-------------|----------|-----|----------|
| task-004 | {description} | 50% | 30m | none |

---

## Resource Usage

### Compute Resources

| Resource | Current | Peak | Threshold | Status |
|----------|---------|------|-----------|--------|
| CPU | X% | Y% | 80% | OK/WARN |
| Memory | X% | Y% | 85% | OK/WARN |
| Disk | X% | Y% | 90% | OK/WARN |

### Token Usage

| Metric | Value | Budget | Remaining |
|--------|-------|--------|-----------|
| Context Tokens | X | Y | Z |
| Input Tokens | X | - | - |
| Output Tokens | X | - | - |

---

## Communication Metrics

### Messages Sent

| Type | Count | Avg Response Time |
|------|-------|-------------------|
| Status Updates | X | Ym |
| Completion Signals | X | Ym |
| Approval Requests | X | Ym |
| Error Reports | X | Ym |

### Messages Received

| Type | Count | Avg Processing Time |
|------|-------|---------------------|
| Task Assignments | X | Ym |
| Status Requests | X | Ym |
| Heartbeat Polls | X | Ym |

### Heartbeat Status

| Metric | Value |
|--------|-------|
| Polls Received | X |
| Polls Responded | X |
| Response Rate | X% |
| Avg Response Time | Xms |

---

## Blockers and Issues

### Current Blockers

| Blocker ID | Description | Severity | Waiting Since | Action Required |
|------------|-------------|----------|---------------|-----------------|
| blk-001 | {description} | high | {timestamp} | {action} |

### Resolved Blockers

| Blocker ID | Description | Duration | Resolution |
|------------|-------------|----------|------------|
| blk-002 | {description} | 15m | {how_resolved} |

---

## Approval Activity

### Requests Made

| Request ID | Type | Status | Wait Time | Outcome |
|------------|------|--------|-----------|---------|
| apr-001 | push | approved | 5m | success |
| apr-002 | merge | pending | 10m | waiting |

### Approval Statistics

| Metric | Value |
|--------|-------|
| Total Requests | X |
| Approved | X |
| Rejected | X |
| Pending | X |
| Avg Wait Time | Xm |

---

## Quality Metrics

### Code Quality (for Orchestrator/Integrator)

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Tests Written | X | Y | OK/WARN |
| Tests Passing | X% | 100% | OK/WARN |
| Lint Errors | X | 0 | OK/WARN |
| Type Errors | X | 0 | OK/WARN |

### Design Quality (for Architect)

| Metric | Value |
|--------|-------|
| Designs Proposed | X |
| Designs Approved | X |
| Revisions Requested | X |
| Avg Revision Cycles | X |

---

## Recommendations

Based on the metrics above:

1. **Performance**: {recommendation_about_performance}
2. **Resource Usage**: {recommendation_about_resources}
3. **Communication**: {recommendation_about_communication}
4. **Quality**: {recommendation_about_quality}

---

## Report Footer

```yaml
generated_by: "ecos-{session}"
generation_duration: "Xms"
next_scheduled_report: "ISO-8601 timestamp"
```
