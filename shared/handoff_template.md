# Handoff Document Template

This template defines the standard format for handoff documents between roles in the 4-plugin architecture.

## Plugin Prefixes

| Plugin | Prefix | Full Name |
|--------|--------|-----------|
| Chief of Staff | `ecos-` | Emasoft Chief of Staff Agent |
| Architect | `eaa-` | Emasoft Architect Agent |
| Orchestrator | `eoa-` | Emasoft Orchestrator Agent |
| Integrator | `eia-` | Emasoft Integrator Agent |

## Handoff File Format

```yaml
---
uuid: "handoff-{uuid}"
from_role: "ecos" | "eaa" | "eoa" | "eia"
to_role: "ecos" | "eaa" | "eoa" | "eia"
created: "ISO-8601 timestamp"
github_issue: "#issue_number"  # Optional
subject: "Brief description"
priority: "urgent" | "high" | "normal" | "low"
requires_ack: true | false
status: "pending" | "acknowledged" | "completed" | "rejected"
---

## Context

[Background information and context for this handoff]

## Requirements / Deliverables

[What needs to be done or what is being delivered]

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Dependencies

- Depends on: [list of dependencies]
- Blocks: [list of blocked items]

## Notes

[Additional notes or considerations]
```

## Chief of Staff Context Handoff

When Chief of Staff hands off context to another session (for session continuity):

```yaml
---
uuid: "handoff-{uuid}"
from_role: "ecos"
to_role: "ecos"  # Same role - session continuity
created: "ISO-8601 timestamp"
handoff_type: "session_continuity"
reason: "context_limit" | "user_request" | "scheduled" | "error_recovery"
---

## Session State

### Active Agents

| Session Name | Role | Status | Task | Progress |
|--------------|------|--------|------|----------|
| eaa-project-abc123 | architect | active | Design API | 75% |
| eoa-project-def456 | orchestrator | blocked | Implement feature | 50% |

### Pending Approvals

| Request ID | Type | From | Waiting Since | Priority |
|------------|------|------|---------------|----------|
| apr-001 | push | eoa-project-def456 | 2025-02-01T10:30:00Z | high |

### Open Issues

| Issue | Assigned To | Status | Blocker |
|-------|-------------|--------|---------|
| #123 | eaa-project-abc123 | in_progress | none |
| #124 | eoa-project-def456 | blocked | needs_approval |

### User Preferences

- Notification level: verbose | normal | quiet
- Auto-approve: [list of auto-approved action types]
- Active project: {project_name}

### Recent Actions

1. [timestamp] Action 1 description
2. [timestamp] Action 2 description
3. [timestamp] Action 3 description

### Pending User Questions

1. [Question about X - waiting since timestamp]

## Checkpoint State

Last validated phase per agent:

| Agent | Phase | Validated At |
|-------|-------|--------------|
| eaa-project-abc123 | design_complete | 2025-02-01T10:00:00Z |
| eoa-project-def456 | tests_written | 2025-02-01T09:45:00Z |

## Resume Instructions

1. Load active agent states
2. Check for pending approvals
3. Resume heartbeat monitoring
4. Continue from last checkpoint
```

## Communication Hierarchy

```
USER <-> ECOS (Chief of Staff) <-> EAA (Architect)
                                  <-> EOA (Orchestrator)
                                  <-> EIA (Integrator)
```

**CRITICAL**: Architect (eaa-), Orchestrator (eoa-), and Integrator (eia-) do NOT communicate directly with each other. All communication flows through Chief of Staff (ecos-).

## Handoff Types

### 1. User Request -> Role Assignment
- From: ecos (chief-of-staff)
- To: eaa | eoa | eia
- Purpose: Route user request to appropriate specialist

### 2. Design Complete -> Orchestration
- From: eaa (via ecos)
- To: eoa (via ecos)
- Purpose: Hand off approved design for implementation

### 3. Implementation Complete -> Integration
- From: eoa (via ecos)
- To: eia (via ecos)
- Purpose: Signal work ready for quality gates

### 4. Quality Gate Results -> User
- From: eia (via ecos)
- To: user
- Purpose: Report integration status and request approvals

### 5. Session Continuity (COS-specific)
- From: ecos
- To: ecos (new session)
- Purpose: Transfer state when context limit reached or session ends

### 6. Emergency Handoff
- From: any role
- To: ecos
- Purpose: Urgent state transfer when agent must terminate unexpectedly

## File Naming Convention

```
handoff-{uuid}-{from}-to-{to}.md

Examples:
- handoff-a1b2c3d4-ecos-to-eaa.md    # COS assigns to Architect
- handoff-e5f6g7h8-eaa-to-ecos.md    # Architect reports to COS
- handoff-i9j0k1l2-ecos-to-eoa.md    # COS assigns to Orchestrator
- handoff-m3n4o5p6-eoa-to-ecos.md    # Orchestrator reports to COS
- handoff-q7r8s9t0-ecos-to-eia.md    # COS assigns to Integrator
- handoff-u1v2w3x4-eia-to-ecos.md    # Integrator reports to COS
- handoff-w5x6y7z8-ecos-to-ecos.md   # COS session continuity
- handoff-a9b0c1d2-eoa-emergency.md  # Emergency handoff from Orchestrator
```

## Storage Location

All handoff files are stored in: `docs_dev/handoffs/`

## Handoff Lifecycle

1. **Created** - Handoff document created, status: pending
2. **Sent** - AI Maestro message sent to recipient
3. **Acknowledged** - Recipient confirms receipt, status: acknowledged
4. **In Progress** - Recipient actively working on task
5. **Completed** - Task finished, status: completed
6. **Rejected** - Recipient cannot accept, status: rejected (with reason)
