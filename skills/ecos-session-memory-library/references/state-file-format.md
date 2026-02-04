# State File Format Reference

## Table of Contents

- 1.1 [Overview of State Files](#11-overview-of-state-files)
- 1.2 [Chief of Staff State File](#12-chief-of-staff-state-file)
- 1.3 [Team Roster File](#13-team-roster-file)
- 1.4 [Coordination Log File](#14-coordination-log-file)
- 1.5 [Performance Data Files](#15-performance-data-files)
- 1.6 [Alert State File](#16-alert-state-file)
- 1.7 [State File Operations](#17-state-file-operations)
- 1.8 [Troubleshooting](#18-troubleshooting)

---

## 1.1 Overview of State Files

The Chief of Staff uses several state files to persist its working state across sessions and context compactions. These files enable continuity, recovery, and coordination.

### State File Directory Structure

```
design/memory/
├── cos-state.md          # Chief of Staff main state
├── team-roster.md        # Current team composition
├── coordination-log.md   # Coordination event log
├── alerts/               # Alert state files
│   └── active-alerts.md
├── performance/          # Performance data
│   ├── metrics-[date].md
│   └── reports/
├── onboarding/           # Onboarding records
│   └── [agent]-[date].md
└── handoffs/             # Handoff documents
    └── [project]-[date].md
```

### State File Principles

1. **Markdown format**: All state files use Markdown for readability
2. **Timestamp everything**: Include ISO timestamps for all entries
3. **Append-friendly**: Design for append operations where possible
4. **Human-readable**: Files should be understandable without tools
5. **Machine-parseable**: Use consistent structure for automation

---

## 1.2 Chief of Staff State File

The main state file tracks the Chief of Staff's current operating state.

### Location

```
design/memory/cos-state.md
```

### Format

```markdown
# Chief of Staff State

## Session Info
- **Session ID:** cos-[timestamp]
- **Started:** [ISO timestamp]
- **Last Updated:** [ISO timestamp]
- **Status:** active|idle|busy

## Current Focus
- **Primary Task:** [current main task]
- **Priority:** [priority level]
- **Started:** [when this focus began]

## Pending Actions
| ID | Action | Priority | Deadline | Status |
|----|--------|----------|----------|--------|
| 1 | [action] | high | [time] | pending |

## Active Alerts
| Alert ID | Type | Severity | Since |
|----------|------|----------|-------|
| [id] | [type] | [severity] | [time] |

## Recent Decisions
| Time | Decision | Rationale |
|------|----------|-----------|
| [time] | [decision] | [why] |

## Coordination State
- **Team Size:** [count]
- **Active Agents:** [count]
- **Last Roster Update:** [time]
- **Last Team Broadcast:** [time]

## Resource Status
- **Memory:** [percent]%
- **CPU Load:** [load]
- **Last Check:** [time]

## Notes
[Any additional context needed for session continuity]
```

### Update Triggers

Update the state file when:
- Focus changes
- Pending action added or completed
- Alert state changes
- Significant decision made
- Team composition changes
- Resource status changes significantly

---

## 1.3 Team Roster File

The team roster tracks all agents in the coordinated team.

### Location

```
design/memory/team-roster.md
```

### Format

```markdown
# Team Roster

Last Updated: [ISO timestamp]
Total Agents: [count]
Active: [count]
Inactive: [count]

## Active Team Members

| Session Name | Role | Status | Last Seen | Current Task | Performance |
|--------------|------|--------|-----------|--------------|-------------|
| [name] | [role] | [status] | [time] | [task] | [rating] |

### [Session Name]
- **Role:** [role]
- **Assigned:** [when assigned]
- **Status:** [detailed status]
- **Capabilities:** [list]
- **Notes:** [any notes]

## Inactive Team Members

| Session Name | Role | Last Active | Reason |
|--------------|------|-------------|--------|
| [name] | [role] | [time] | [reason] |

## Role Summary

| Role | Assigned | Target |
|------|----------|--------|
| Developer | 3 | 4 |
| Code Reviewer | 2 | 2 |
| Test Engineer | 1 | 1 |

## Team Changes Log

| Time | Change | Agent | Details |
|------|--------|-------|---------|
| [time] | joined | [name] | [details] |
| [time] | left | [name] | [details] |
| [time] | role change | [name] | [from -> to] |
```

### Update Triggers

Update the roster when:
- New agent joins
- Agent leaves or goes offline
- Role changes
- Status changes
- Current task changes
- Regular polling interval (15 min)

---

## 1.4 Coordination Log File

The coordination log records all coordination events for audit and recovery.

### Location

```
design/memory/coordination-log.md
```

### Format

```markdown
# Coordination Log

Session: [session ID]
Started: [ISO timestamp]

## Events

### [ISO timestamp]
**Type:** [event type]
**Involved:** [agents involved]
**Action:** [what happened]
**Outcome:** [result]
**Notes:** [additional context]

---

### [ISO timestamp]
**Type:** message_sent
**Involved:** cos -> orchestrator-master
**Action:** Task assignment notification
**Outcome:** Delivered
**Notes:** Task TASK-042

---

### [ISO timestamp]
**Type:** team_change
**Involved:** helper-agent-generic
**Action:** Joined team as Developer
**Outcome:** Onboarding complete
**Notes:** Sprint 5 assignment

---
```

### Event Types

| Type | Description |
|------|-------------|
| `message_sent` | Message sent to agent |
| `message_received` | Message received from agent |
| `broadcast` | Broadcast sent to team |
| `team_change` | Agent joined, left, or changed role |
| `alert_triggered` | Resource alert triggered |
| `alert_resolved` | Resource alert resolved |
| `escalation` | Issue escalated |
| `decision` | Significant decision made |
| `onboarding` | Onboarding event |
| `handoff` | Project handoff event |

### Log Rotation

- Archive logs weekly
- Keep current week in active file
- Archived logs: `coordination-log-[YYYY-WNN].md`

---

## 1.5 Performance Data Files

Performance data is stored per-date and per-agent.

### Daily Metrics Location

```
design/memory/performance/metrics-[YYYY-MM-DD].md
```

### Daily Metrics Format

```markdown
# Daily Performance Metrics

Date: [YYYY-MM-DD]
Generated: [ISO timestamp]

## Team Summary

| Metric | Value | Previous | Change |
|--------|-------|----------|--------|
| Tasks Completed | [n] | [n] | [+/-n] |
| On-Time Rate | [n]% | [n]% | [+/-n]% |
| Quality Rate | [n]% | [n]% | [+/-n]% |

## Individual Metrics

### [Agent Name]

| Metric | Value |
|--------|-------|
| Tasks Completed | [n] |
| On-Time | [n] ([n]%) |
| First-Pass | [n] ([n]%) |
| Avg Response Time | [n] min |
| Issues | [n] |

**Tasks:**
- [TASK-ID]: [status] at [time]

**Notes:**
[Any observations]

---
```

### Agent Metrics Location

```
design/memory/performance/agent-[name]-[YYYY-MM].md
```

### Agent Metrics Format

```markdown
# Agent Performance: [name]

Period: [YYYY-MM]
Role: [role]

## Monthly Summary

| Metric | Value | Team Avg | Target |
|--------|-------|----------|--------|
| Tasks | [n] | [n] | [n] |
| On-Time | [n]% | [n]% | [n]% |
| Quality | [n]% | [n]% | [n]% |

## Weekly Breakdown

| Week | Tasks | On-Time | Quality |
|------|-------|---------|---------|
| W01 | [n] | [n]% | [n]% |

## Trend

[Description of performance trend]

## Strengths
1. [Strength]

## Areas for Improvement
1. [Area]

## Recommendations
1. [Recommendation]
```

---

## 1.6 Alert State File

Tracks active and recent alerts.

### Location

```
design/memory/alerts/active-alerts.md
```

### Format

```markdown
# Active Alerts

Last Updated: [ISO timestamp]

## Critical

### ALERT-[ID]
- **Type:** [type]
- **Severity:** critical
- **Triggered:** [time]
- **Resource:** [resource]
- **Value:** [current value]
- **Threshold:** [threshold]
- **Actions Taken:** [list of actions]
- **Status:** active|acknowledged|resolving

## Warning

### ALERT-[ID]
- **Type:** [type]
- **Severity:** warning
- **Triggered:** [time]
- **Resource:** [resource]
- **Value:** [current value]
- **Threshold:** [threshold]
- **Status:** active

## Recently Resolved

| Alert ID | Type | Duration | Resolved At |
|----------|------|----------|-------------|
| [id] | [type] | [duration] | [time] |
```

### Alert Lifecycle

1. **Created**: Alert triggered when threshold exceeded
2. **Active**: Alert is current and requires attention
3. **Acknowledged**: Someone has seen the alert
4. **Resolving**: Actions being taken
5. **Resolved**: Alert condition no longer present

---

## 1.7 State File Operations

### Reading State Files

```bash
# Read Chief of Staff state
cat design/memory/cos-state.md

# Read team roster
cat design/memory/team-roster.md

# Read today's performance
cat design/memory/performance/metrics-$(date +%Y-%m-%d).md
```

### Updating State Files

**Atomic updates recommended:**
1. Read current file
2. Make modifications in memory
3. Write complete file (not append)
4. This prevents partial updates if interrupted

**Append-safe sections:**
- Coordination log (append new entries)
- Recent decisions (append new entries)
- Team changes log (append new entries)

### Backing Up State Files

```bash
# Backup all state files
BACKUP_DIR="design/memory/backups/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp design/memory/*.md "$BACKUP_DIR/"
cp -r design/memory/performance "$BACKUP_DIR/"
cp -r design/memory/alerts "$BACKUP_DIR/"
```

### Validating State Files

Check that state files are well-formed:
- Markdown syntax is valid
- Required sections present
- Timestamps are ISO format
- Tables have correct columns

---

## 1.8 Troubleshooting

### Issue: State file is corrupted

**Symptoms:** Parsing errors, missing sections, invalid format.

**Possible causes:**
- Interrupted write
- Concurrent access
- Encoding issues

**Resolution:**
1. Check backup directory for recent copy
2. If no backup, reconstruct from logs
3. Validate file format before using
4. Implement write-then-rename pattern

### Issue: State file grows too large

**Symptoms:** Slow reads, memory issues, large file size.

**Possible causes:**
- Log sections not rotated
- Old data not archived
- Verbose entries

**Resolution:**
1. Archive old log entries
2. Keep only last N entries in active file
3. Use summary counts instead of full lists
4. Implement regular archival schedule

### Issue: State file out of sync with reality

**Symptoms:** Team roster incorrect, metrics wrong, stale data.

**Possible causes:**
- Updates not written
- Session crashed before save
- Multiple writers conflicting

**Resolution:**
1. Rebuild state from source (AI Maestro, logs)
2. Implement more frequent saves
3. Use single-writer pattern
4. Add validation checks

### Issue: Cannot find state file

**Symptoms:** File not found errors.

**Possible causes:**
- Wrong path
- Directory not created
- File deleted

**Resolution:**
1. Verify directory structure exists
2. Create missing directories
3. Initialize empty state files if missing
4. Check for path typos

### Issue: Concurrent access problems

**Symptoms:** Overwrites, lost updates, inconsistent data.

**Possible causes:**
- Multiple agents writing
- No locking mechanism
- Race conditions

**Resolution:**
1. Designate single owner per file
2. Use file locking if needed
3. Implement read-modify-write with locks
4. Consider append-only log pattern

---

**Version:** 1.0
**Last Updated:** 2025-02-01
