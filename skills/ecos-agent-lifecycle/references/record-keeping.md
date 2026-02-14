# Record-Keeping and Logging


## Contents

- [Lifecycle Log](#lifecycle-log)
- [Approval Requests Log](#approval-requests-log)
- [Team Assignments Log](#team-assignments-log)
- [Project: svgbbox-library](#project-svgbbox-library)
- [Project: auth-service](#project-auth-service)
- [Operation Audit Trail](#operation-audit-trail)
- [Log Maintenance](#log-maintenance)
- [Log Access](#log-access)
- [Agent Registry Structures](#agent-registry-structures)
  - [Central Agent Registry](#central-agent-registry)
  - [Team Registry (Project-Level)](#team-registry-project-level)
- [Session State Formats](#session-state-formats)
  - [Hibernation State Snapshot](#hibernation-state-snapshot)
  - [Health Check Response Format](#health-check-response-format)
  - [Team Status Report Format](#team-status-report-format)
- [Log Query Examples](#log-query-examples)
  - [Get recent spawns](#get-recent-spawns)
  - [Find all operations for specific agent](#find-all-operations-for-specific-agent)
  - [Check hibernation/wake cycles](#check-hibernationwake-cycles)
  - [Get approval decisions from current month](#get-approval-decisions-from-current-month)
  - [Trace specific operation by request ID](#trace-specific-operation-by-request-id)
- [Best Practices](#best-practices)

**CRITICAL:** All ECOS operations MUST be logged for audit, debugging, and accountability.

---

## Lifecycle Log

**Location:** `$CLAUDE_PROJECT_DIR/docs_dev/chief-of-staff/agent-lifecycle.log`

**Purpose:** Complete audit trail of all agent lifecycle operations

**Format:**
```
[<ISO_timestamp>] [<operation>] [<agent_name>] <details>
```

**Operations:**
- `SPAWN` - Agent created
- `TERMINATE` - Agent removed
- `HIBERNATE` - Agent put to sleep
- `WAKE` - Agent restored from hibernation
- `TEAM_ADD` - Agent added to team
- `TEAM_REMOVE` - Agent removed from team
- `STATUS_CHANGE` - Agent status updated
- `FAILURE` - Operation failed
- `ROLLBACK` - Rollback executed

**Example entries:**
```
[2026-02-04T10:30:00Z] [SPAWN] [worker-dev-auth-001] Created with role eoa-orchestrator-main-agent in /path/to/project
[2026-02-04T10:30:15Z] [TEAM_ADD] [worker-dev-auth-001] Added to svgbbox-library-team with role developer
[2026-02-04T12:00:00Z] [HIBERNATE] [worker-dev-003] Hibernated due to 2h inactivity
[2026-02-04T14:00:00Z] [WAKE] [worker-dev-003] Restored from hibernation for new task
[2026-02-04T16:00:00Z] [TERMINATE] [worker-deploy-002] Removed after project deployment complete
[2026-02-04T16:05:00Z] [FAILURE] [worker-test-005] Spawn failed: Directory already exists
[2026-02-04T16:05:01Z] [ROLLBACK] [worker-test-005] Rollback completed: Cleaned up partial registration
```

**Logging procedure:**
```bash
log_file="$CLAUDE_PROJECT_DIR/docs_dev/chief-of-staff/agent-lifecycle.log"
mkdir -p "$(dirname "$log_file")"
echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] [$operation] [$agent_name] $details" >> "$log_file"
```

---

## Approval Requests Log

**Location:** `$CLAUDE_PROJECT_DIR/docs_dev/chief-of-staff/approvals/approval-requests-<YYYY-MM>.log`

**Purpose:** Track all approval requests and decisions (monthly rotation)

**Format:** Same as ecos-approval-coordinator audit trail

**Example:**
```
[2026-02-04T10:29:30Z] [AR-1706795370-f3a2b1] [SUBMIT] type=agent_spawn requester=ecos-chief-of-staff operation="Create worker-dev-auth-001"
[2026-02-04T10:29:45Z] [AR-1706795370-f3a2b1] [DECIDE] decision=approved by=manager reason="Team needs auth developer"
[2026-02-04T10:30:00Z] [AR-1706795370-f3a2b1] [EXEC_DONE] result=success duration=15000ms
```

---

## Team Assignments Log

**Location:** `$CLAUDE_PROJECT_DIR/docs_dev/chief-of-staff/team-assignments.md`

**Purpose:** Human-readable summary of current team assignments across all projects

**Format:** Markdown table with project grouping

**Example:**
```markdown
# Team Assignments

**Last Updated:** 2026-02-04T16:00:00Z

## Project: svgbbox-library

**Team Lead:** svgbbox-orchestrator (EOA)

| Agent Name | Role | Status | Added | Last Active |
|------------|------|--------|-------|-------------|
| worker-dev-001 | developer | active | 2026-02-01 | 2026-02-04 15:45 |
| worker-dev-002 | developer | active | 2026-02-03 | 2026-02-04 16:00 |
| worker-test-001 | test-engineer | active | 2026-02-01 | 2026-02-04 14:30 |
| worker-dev-003 | developer | hibernated | 2026-02-02 | 2026-02-04 12:00 |

**Registry:** `/path/to/svgbbox/.emasoft/team-registry.json`

---

## Project: auth-service

**Team Lead:** auth-orchestrator (EOA)

| Agent Name | Role | Status | Added | Last Active |
|------------|------|--------|-------|-------------|
| worker-dev-auth-001 | developer | active | 2026-02-04 | 2026-02-04 16:00 |
| worker-deploy-001 | deploy-agent | active | 2026-02-04 | 2026-02-04 15:00 |

**Registry:** `/path/to/auth-service/.emasoft/team-registry.json`
```

**Update procedure:**
```bash
# Regenerate team-assignments.md from all team registries
uv run python scripts/ecos_generate_team_report.py --output "$CLAUDE_PROJECT_DIR/docs_dev/chief-of-staff/team-assignments.md"
```

---

## Operation Audit Trail

**Location:** `$CLAUDE_PROJECT_DIR/docs_dev/chief-of-staff/operations/operation-<YYYY-MM-DD>.log`

**Purpose:** Detailed operation logs (daily rotation)

**Format:**
```
[<timestamp>] [<request_id>] [<agent>] <operation> <status> <details>
```

**Example:**
```
[2026-02-04T10:29:30Z] [OP-1706795370-001] [ecos-chief-of-staff] agent_spawn STARTED target=worker-dev-auth-001
[2026-02-04T10:29:35Z] [OP-1706795370-001] [ecos-chief-of-staff] approval_request SUBMITTED request_id=AR-1706795370-f3a2b1
[2026-02-04T10:29:45Z] [OP-1706795370-001] [ecos-chief-of-staff] approval_received APPROVED by=manager
[2026-02-04T10:29:50Z] [OP-1706795370-001] [ecos-chief-of-staff] spawn_execute STARTED agent=worker-dev-auth-001 via ai-maestro-agents-management skill
[2026-02-04T10:30:00Z] [OP-1706795370-001] [ecos-chief-of-staff] spawn_execute SUCCESS duration=10s
[2026-02-04T10:30:05Z] [OP-1706795370-001] [ecos-chief-of-staff] health_check SENT target=worker-dev-auth-001
[2026-02-04T10:30:10Z] [OP-1706795370-001] [ecos-chief-of-staff] health_check RECEIVED response="OK"
[2026-02-04T10:30:15Z] [OP-1706795370-001] [ecos-chief-of-staff] team_add SUCCESS team=svgbbox-library-team
[2026-02-04T10:30:20Z] [OP-1706795370-001] [ecos-chief-of-staff] agent_spawn COMPLETED total_duration=50s
```

---

## Log Maintenance

**Rotation Policy:**
- Lifecycle log: **Never rotate** (permanent audit trail)
- Approval requests: **Monthly rotation** (keep 12 months)
- Team assignments: **Regenerate daily** (single current file)
- Operation logs: **Daily rotation** (keep 30 days)

**Archival:**
```bash
# Archive old logs (run monthly)
uv run python scripts/ecos_archive_logs.py --older-than 30d --destination "$CLAUDE_PROJECT_DIR/docs_dev/chief-of-staff/archives/"
```

---

## Log Access

All logs stored in `$CLAUDE_PROJECT_DIR/docs_dev/chief-of-staff/` are:
- **Git-ignored** (local only)
- **Read/write by ECOS** (and sub-agents)
- **Read-only by EOA** (for status queries)

---

## Agent Registry Structures

### Central Agent Registry

**Location:** `$CLAUDE_PROJECT_DIR/docs_dev/chief-of-staff/agent-registry.json`

**Purpose:** Master registry of all agents spawned by ECOS

**Structure:**
```json
{
  "registry_version": "1.0",
  "last_updated": "2026-02-04T16:00:00Z",
  "agents": {
    "worker-dev-001": {
      "name": "worker-dev-001",
      "role": "developer",
      "type": "eoa-orchestrator-main-agent",
      "status": "active",
      "tmux_session": "worker-dev-001",
      "workspace": "/Users/user/Code/svgbbox-library",
      "spawned_at": "2026-02-01T10:00:00Z",
      "spawned_by": "ecos-chief-of-staff",
      "last_active": "2026-02-04T15:45:00Z",
      "team_memberships": [
        {
          "team_id": "svgbbox-library-team",
          "project": "svgbbox-library",
          "added_at": "2026-02-01T10:05:00Z"
        }
      ],
      "hibernation": null
    },
    "worker-dev-003": {
      "name": "worker-dev-003",
      "role": "developer",
      "type": "eoa-orchestrator-main-agent",
      "status": "hibernated",
      "tmux_session": "worker-dev-003",
      "workspace": "/Users/user/Code/svgbbox-library",
      "spawned_at": "2026-02-02T14:00:00Z",
      "spawned_by": "ecos-chief-of-staff",
      "last_active": "2026-02-04T12:00:00Z",
      "team_memberships": [
        {
          "team_id": "svgbbox-library-team",
          "project": "svgbbox-library",
          "added_at": "2026-02-02T14:10:00Z"
        }
      ],
      "hibernation": {
        "hibernated_at": "2026-02-04T12:00:00Z",
        "reason": "inactivity_2h",
        "can_wake": true,
        "state_snapshot": "/path/to/hibernation-state.json"
      }
    }
  }
}
```

### Team Registry (Project-Level)

**Location:** `<project_root>/.emasoft/team-registry.json`

**Purpose:** Track agents assigned to a specific project team

**Structure:**
```json
{
  "team_id": "svgbbox-library-team",
  "project_name": "svgbbox-library",
  "project_root": "/Users/user/Code/svgbbox-library",
  "team_lead": "svgbbox-orchestrator",
  "created_at": "2026-02-01T09:00:00Z",
  "last_updated": "2026-02-04T16:00:00Z",
  "members": [
    {
      "agent_name": "worker-dev-001",
      "role": "developer",
      "status": "active",
      "added_at": "2026-02-01T10:05:00Z",
      "added_by": "ecos-chief-of-staff",
      "tmux_session": "worker-dev-001",
      "last_active": "2026-02-04T15:45:00Z"
    },
    {
      "agent_name": "worker-dev-002",
      "role": "developer",
      "status": "active",
      "added_at": "2026-02-03T11:00:00Z",
      "added_by": "ecos-chief-of-staff",
      "tmux_session": "worker-dev-002",
      "last_active": "2026-02-04T16:00:00Z"
    },
    {
      "agent_name": "worker-test-001",
      "role": "test-engineer",
      "status": "active",
      "added_at": "2026-02-01T10:15:00Z",
      "added_by": "ecos-chief-of-staff",
      "tmux_session": "worker-test-001",
      "last_active": "2026-02-04T14:30:00Z"
    },
    {
      "agent_name": "worker-dev-003",
      "role": "developer",
      "status": "hibernated",
      "added_at": "2026-02-02T14:10:00Z",
      "added_by": "ecos-chief-of-staff",
      "tmux_session": "worker-dev-003",
      "last_active": "2026-02-04T12:00:00Z"
    }
  ]
}
```

---

## Session State Formats

### Hibernation State Snapshot

**Location:** `$CLAUDE_PROJECT_DIR/docs_dev/chief-of-staff/hibernation/<agent_name>-<timestamp>.json`

**Purpose:** Save agent state before hibernation for restoration

**Structure:**
```json
{
  "agent_name": "worker-dev-003",
  "hibernated_at": "2026-02-04T12:00:00Z",
  "tmux_session": "worker-dev-003",
  "workspace": "/Users/user/Code/svgbbox-library",
  "role": "developer",
  "session_state": {
    "working_directory": "/Users/user/Code/svgbbox-library/src",
    "git_branch": "feature/auth-module",
    "open_files": [
      "src/auth/validator.py",
      "tests/test_auth.py"
    ],
    "last_command": "uv run pytest tests/test_auth.py",
    "environment_vars": {
      "PYTHONPATH": "/Users/user/Code/svgbbox-library",
      "DEBUG": "1"
    },
    "active_tasks": [
      {
        "task_id": "TASK-123",
        "description": "Implement token validation",
        "status": "in-progress",
        "progress": 75
      }
    ]
  },
  "team_memberships": [
    {
      "team_id": "svgbbox-library-team",
      "project": "svgbbox-library"
    }
  ],
  "can_wake": true,
  "notes": "Hibernated due to 2h inactivity. Can be woken for new auth-related tasks."
}
```

### Health Check Response Format

**Purpose:** Standardized response from agents to health checks

**Structure:**
```json
{
  "status": "healthy",
  "agent_name": "worker-dev-001",
  "timestamp": "2026-02-04T16:00:00Z",
  "tmux_session": "worker-dev-001",
  "workspace": "/Users/user/Code/svgbbox-library",
  "current_state": {
    "working": true,
    "current_task": "Implementing authentication module",
    "load": "medium",
    "blocked": false
  },
  "uptime_seconds": 21600,
  "last_activity": "2026-02-04T15:45:00Z",
  "team_memberships": ["svgbbox-library-team"]
}
```

### Team Status Report Format

**Purpose:** Summary of team status sent by EOA to ECOS

**Structure:**
```json
{
  "team_id": "svgbbox-library-team",
  "team_lead": "svgbbox-orchestrator",
  "project": "svgbbox-library",
  "report_timestamp": "2026-02-04T16:00:00Z",
  "summary": {
    "total_members": 4,
    "active": 3,
    "hibernated": 1,
    "blocked": 0
  },
  "members": [
    {
      "agent_name": "worker-dev-001",
      "role": "developer",
      "status": "active",
      "current_task": "Implementing authentication module",
      "last_active": "2026-02-04T15:45:00Z"
    },
    {
      "agent_name": "worker-dev-002",
      "role": "developer",
      "status": "active",
      "current_task": "Writing API documentation",
      "last_active": "2026-02-04T16:00:00Z"
    },
    {
      "agent_name": "worker-test-001",
      "role": "test-engineer",
      "status": "active",
      "current_task": "Running integration tests",
      "last_active": "2026-02-04T14:30:00Z"
    },
    {
      "agent_name": "worker-dev-003",
      "role": "developer",
      "status": "hibernated",
      "hibernated_at": "2026-02-04T12:00:00Z",
      "reason": "inactivity_2h"
    }
  ],
  "issues": [],
  "resource_usage": {
    "cpu_average": 45,
    "memory_mb": 2048
  }
}
```

---

## Log Query Examples

### Get recent spawns
```bash
grep "\[SPAWN\]" "$CLAUDE_PROJECT_DIR/docs_dev/chief-of-staff/agent-lifecycle.log" | tail -10
```

### Find all operations for specific agent
```bash
grep "\[worker-dev-001\]" "$CLAUDE_PROJECT_DIR/docs_dev/chief-of-staff/agent-lifecycle.log"
```

### Check hibernation/wake cycles
```bash
grep -E "\[(HIBERNATE|WAKE)\]" "$CLAUDE_PROJECT_DIR/docs_dev/chief-of-staff/agent-lifecycle.log"
```

### Get approval decisions from current month
```bash
month=$(date +"%Y-%m")
grep "\[DECIDE\]" "$CLAUDE_PROJECT_DIR/docs_dev/chief-of-staff/approvals/approval-requests-${month}.log"
```

### Trace specific operation by request ID
```bash
request_id="OP-1706795370-001"
grep "\[$request_id\]" "$CLAUDE_PROJECT_DIR/docs_dev/chief-of-staff/operations/operation-"*.log
```

---

## Best Practices

1. **Always log before and after operations** - Record intent before execution, result after
2. **Use consistent timestamps** - ISO 8601 format with UTC timezone
3. **Include request IDs** - Correlate multi-step operations
4. **Log failures explicitly** - Never silently skip failed operations
5. **Preserve audit trail** - Never delete lifecycle log
6. **Rotate proactively** - Don't let logs grow unbounded
7. **Make logs searchable** - Use consistent formatting and keywords
8. **Cross-reference registries** - Link logs to agent registry entries
