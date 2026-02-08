---
name: ecos-permission-management
description: Use when requesting EAMA approval for agent lifecycle ops (spawn, terminate, hibernate, wake, plugin install). Trigger with permission requests.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro messaging system and Assistant Manager (EAMA) to be online for approval handling. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ecos-main
workflow-instruction: "support"
procedure: "support-skill"
---

# Emasoft Chief of Staff - Permission Management Skill

## Overview

Permission management is a critical governance function of the Chief of Staff. Before performing certain operations that affect agent resources or system state, ECOS must request approval from the Assistant Manager (EAMA), who serves as the user's representative. This skill teaches you how to request approvals, track pending approvals, handle timeouts, and maintain audit trails.

## Prerequisites

Before using this skill, ensure:
1. Permission registry is accessible
2. Agent roles are defined
3. EAMA approval workflow is available for escalations

## Instructions

1. Identify permission change needed
2. Verify requester authorization
3. Apply permission change
4. Log the change and notify affected agents

## Output

| Permission Type | Output |
|-----------------|--------|
| Grant access | Permission added, agent notified |
| Revoke access | Permission removed, agent notified |
| Escalate | Request forwarded to EAMA for approval |

## What Is Permission Management?

Permission management is the process of obtaining authorization before executing privileged operations. The Chief of Staff must not unilaterally spawn agents, terminate agents, hibernate agents, wake agents, or install plugins without proper approval from the manager (EAMA) unless operating under an explicit autonomous directive.

**Key principle:** ECOS proposes, EAMA approves. The user (via EAMA) maintains control over resource-consuming operations.

## When Approval Is Required

```
+-------------------------------------------------------------+
|                 APPROVAL REQUIRED OPERATIONS                 |
+-------------------------------------------------------------+
|  AGENT SPAWN       - Creating new agent instances            |
|  AGENT TERMINATE   - Permanently stopping agent execution    |
|  AGENT HIBERNATE   - Suspending agent to conserve resources  |
|  AGENT WAKE        - Resuming hibernated agent               |
|  PLUGIN INSTALL    - Installing new Claude Code plugins      |
+-------------------------------------------------------------+
```

**Exception:** If the manager has issued an autonomous operation directive, ECOS may proceed without approval but must notify EAMA after the operation completes.

## The Approval Workflow

```
ECOS                           EAMA                          USER
  |                              |                              |
  |  1. Request approval         |                              |
  |----------------------------->|                              |
  |                              |  2. Present to user          |
  |                              |----------------------------->|
  |                              |                              |
  |                              |  3. User decides             |
  |                              |<-----------------------------|
  |  4. Receive response         |                              |
  |<-----------------------------|                              |
  |                              |                              |
  |  5. Execute or abort         |                              |
  |  6. Log to audit trail       |                              |
```

> **For ACK timeout policy and message retry procedures, see the ecos-notification-protocols skill.**

## Core Procedures

### PROCEDURE 1: Request Approval from Manager

**When to use:** Before executing any agent lifecycle operation or plugin installation.

**Steps:** Identify operation type, compose approval request, send via AI Maestro, await response, handle decision.

See [references/approval-request-procedure.md](references/approval-request-procedure.md) for complete documentation:
- 1.1 What is an approval request
- 1.2 When to request approval (spawn, terminate, hibernate, wake, plugin)
- 1.3 Approval request procedure (identification, justification, composition, transmission, awaiting)
- 1.4 Request message format
- 1.5 Examples
- 1.6 Troubleshooting

### PROCEDURE 2: Track Pending Approvals

**When to use:** When managing multiple operations requiring approval, when checking status of pending requests.

**Steps:** Register new requests, monitor response status, handle multiple concurrent requests, update tracking on resolution.

See [references/approval-tracking.md](references/approval-tracking.md) for complete documentation:
- 2.1 What is approval tracking
- 2.2 Tracking data structure
- 2.3 Tracking procedure (registration, monitoring, concurrent handling, resolution)
- 2.4 State file format
- 2.5 Examples
- 2.6 Troubleshooting

### PROCEDURE 3: Handle Approval Timeouts and Escalation

**When to use:** When no response received within timeout period, when urgent operation is blocked.

**Steps:** Send reminder notifications, send urgent notification, determine proceed or abort, log escalation event.

See [references/approval-escalation.md](references/approval-escalation.md) for complete documentation:
- 3.1 What is approval escalation
- 3.2 Escalation triggers (60s reminder, 90s urgent, 120s proceed/abort)
- 3.3 Escalation procedure
- 3.4 Autonomous operation mode
- 3.5 Examples
- 3.6 Troubleshooting

## Approval Types

| Type | Request When | EAMA Options |
|------|--------------|--------------|
| Agent Spawn | Creating new agent | Approve, Reject, Modify |
| Agent Terminate | Stopping agent | Approve, Reject, Delay |
| Agent Hibernate | Suspending idle agent | Approve, Reject, Terminate Instead |
| Agent Wake | Resuming hibernated agent | Approve, Reject, Spawn Fresh Instead |
| Plugin Install | Installing plugin | Approve, Reject, Request Security Review |

See [references/approval-types-detailed.md](references/approval-types-detailed.md) for justification requirements and detailed decision options.

## Audit Trail Requirements

**All approval operations must be logged:**

```yaml
audit_trail:
  - timestamp: "ISO-8601"
    operation: "spawn|terminate|hibernate|wake|plugin_install"
    target: "agent_name_or_plugin_name"
    request_id: "uuid"
    requested_at: "ISO-8601"
    decision: "approved|rejected|modified|timeout_proceed|timeout_abort"
    decided_at: "ISO-8601"
    decided_by: "eama|autonomous|timeout"
    justification: "reason provided"
    modifications: null | {changes}
    escalation_count: 0|1|2|3
```

**Audit file location:** `docs_dev/audit/ecos-approvals-{date}.yaml`

## Task Checklist

Copy this checklist and track your progress:

- [ ] Understand when approval is required
- [ ] Learn PROCEDURE 1: Request approval from manager
- [ ] Learn PROCEDURE 2: Track pending approvals
- [ ] Learn PROCEDURE 3: Handle approval timeouts
- [ ] Practice sending an agent spawn approval request
- [ ] Practice tracking multiple pending approvals
- [ ] Practice handling a timeout scenario
- [ ] Verify audit trail is properly maintained

## Examples

For complete examples with expected responses, see [references/examples.md](references/examples.md):

- Example 1: Requesting approval to spawn an agent
- Example 2: Requesting approval to terminate an agent
- Example 3: Handling approval timeout (reminder, urgent, proceed)
- Example 4: Operating in autonomous mode (post-operation notification)

## Error Handling

| Issue | Resolution |
|-------|------------|
| EAMA offline | See [approval-escalation.md](references/approval-escalation.md) Section 3.6 |
| Request format rejected | See [approval-request-procedure.md](references/approval-request-procedure.md) Section 1.6 |
| Audit write failure | Ensure `docs_dev/audit/` exists and is writable |
| Conflicting responses | Use response with latest `decided_at` timestamp, log conflict |

## Key Takeaways

1. **Always request approval** - Never execute privileged operations without approval
2. **Use proper message format** - Include all required fields in approval requests
3. **Respect the timeout** - 2 minutes max wait, with notifications at 60s and 90s
4. **Log everything** - Maintain complete audit trail for all approval operations
5. **Handle autonomous mode** - When directive given, skip approval but still notify
6. **Track pending requests** - Maintain state for all outstanding approvals

## Plugin Prefix Reference

| Role | Prefix | Plugin Name |
|------|--------|-------------|
| Chief of Staff | `ecos-` | Emasoft Chief of Staff |
| Assistant Manager | `eama-` | Emasoft Assistant Manager Agent |
| Architect | `eaa-` | Emasoft Architect Agent |
| Orchestrator | `eoa-` | Emasoft Orchestrator Agent |
| Integrator | `eia-` | Emasoft Integrator Agent |

## Resources

- [Approval Request Procedure](references/approval-request-procedure.md)
- [Approval Tracking](references/approval-tracking.md)
- [Approval Escalation](references/approval-escalation.md)
- [Approval Types Detailed](references/approval-types-detailed.md)
- [Examples](references/examples.md)
- [RULE 14 Enforcement](references/rule-14-enforcement.md) - User requirements are immutable
- [Approval Workflow Engine](references/approval-workflow-engine.md) - Complete approval workflow engine procedures

---

**Version:** 1.0
**Last Updated:** 2025-02-03
**Target Audience:** Chief of Staff Agents
**Difficulty Level:** Intermediate
