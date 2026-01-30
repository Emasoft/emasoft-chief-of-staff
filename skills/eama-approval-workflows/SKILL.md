---
name: eama-approval-workflows
description: Use when handling approval requests from other roles that require user decisions on code, releases, or security gates
context: fork
triggers:
  - Any role sends an approval request via AI Maestro
  - User needs to make a decision about code, releases, or security
  - Quality gates require human authorization
---

# Approval Workflows Skill

## Overview

This skill provides the Assistant Manager (EAMA) with standard workflows for handling approval requests from other roles and presenting them to the user for decision.

## Prerequisites

- AI Maestro messaging system must be running
- EAMA must have access to `docs_dev/handoffs/` directory
- State file must be writable for approval tracking

## Instructions

1. Listen for approval requests from other roles via AI Maestro
2. Parse the approval request to determine type (push, merge, publish, security, design)
3. Present the approval request to the user using the appropriate template
4. Record the user's decision with timestamp
5. Send the approval response back to the requesting role
6. Update the approval state tracking file

## Plugin Prefix Reference

| Role | Prefix | Plugin Name |
|------|--------|-------------|
| Assistant Manager | `eama-` | Emasoft Assistant Manager Agent |
| Architect | `eaa-` | Emasoft Architect Agent |
| Orchestrator | `eoa-` | Emasoft Orchestrator Agent |
| Integrator | `eia-` | Emasoft Integrator Agent |

## Approval Types

### 1. Push Approval

**Trigger**: Code is ready to be pushed to remote repository

**Workflow**:
1. Receive approval request from EOA/EIA
2. Present to user:
   ```
   ## Push Approval Requested

   **Branch**: {branch_name}
   **Changes**: {summary_of_changes}
   **Files Modified**: {count}
   **Tests Status**: {passed/failed}

   Do you approve pushing these changes?
   - [Approve] - Push to remote
   - [Reject] - Cancel push
   - [Review] - Show me the changes first
   ```
3. Record user decision
4. Send approval response to requesting role

### 2. Merge Approval

**Trigger**: PR is ready to be merged

**Workflow**:
1. Receive approval request from EIA
2. Present to user:
   ```
   ## Merge Approval Requested

   **PR**: #{pr_number} - {pr_title}
   **Branch**: {source} -> {target}
   **Reviews**: {review_status}
   **CI Status**: {ci_status}
   **Conflicts**: {yes/no}

   Do you approve merging this PR?
   - [Approve] - Merge PR
   - [Reject] - Close without merging
   - [Request Changes] - Add comments
   ```
3. Record user decision
4. Send approval response to EIA

### 3. Publish Approval

**Trigger**: Package/release is ready to be published

**Workflow**:
1. Receive approval request from EIA
2. Present to user:
   ```
   ## Publish Approval Requested

   **Package**: {package_name}
   **Version**: {version}
   **Target**: {npm/pypi/github releases/etc}
   **Changelog**: {summary}
   **Breaking Changes**: {yes/no}

   Do you approve publishing this release?
   - [Approve] - Publish
   - [Reject] - Cancel
   - [Review] - Show release notes
   ```
3. Record user decision
4. Send approval response to EIA

### 4. Security Approval

**Trigger**: Action with security implications requires authorization

**Workflow**:
1. Receive approval request from any role (EAA/EOA/EIA)
2. Present to user:
   ```
   ## Security Approval Required

   **Action**: {action_description}
   **Risk Level**: {low/medium/high/critical}
   **Affected Systems**: {list}
   **Justification**: {reason_for_action}
   **Rollback Plan**: {description}

   This action has security implications. Do you authorize it?
   - [Authorize] - Proceed with action
   - [Deny] - Block action
   - [More Info] - Explain risks in detail
   ```
3. Record user decision with timestamp
4. Send authorization response

### 5. Design Approval

**Trigger**: EAA (Architect) has completed design document

**Workflow**:
1. Receive completion signal from EAA
2. Present to user:
   ```
   ## Design Approval Requested

   **Design**: {design_name}
   **Document**: {path_to_design_doc}
   **Modules**: {count} modules defined
   **Estimated Scope**: {scope_summary}

   Review the design document and approve to proceed with implementation.
   - [Approve] - Proceed to orchestration
   - [Request Changes] - Send back to EAA
   - [Discuss] - I have questions
   ```
3. Record user decision
4. If approved, create handoff to EOA

## Approval State Tracking

All approvals are tracked in state file:

```yaml
approvals:
  - id: "approval-{uuid}"
    type: "merge"
    requested_by: "eia"
    requested_at: "ISO-8601"
    status: "pending" | "approved" | "rejected"
    user_decision: null | "approve" | "reject" | "request_changes"
    decided_at: null | "ISO-8601"
    conditions: []
    notes: ""
```

## Escalation Rules

### Auto-Reject Conditions
- Request older than 24 hours without response
- Requesting role session terminated
- Blocking security vulnerability detected

### Auto-Approve Conditions (NEVER by default)
- No auto-approve without explicit user configuration
- All approvals require human decision

### Escalation Triggers
- Security approval with "critical" risk level
- Approval request with "urgent" priority
- Multiple failed approval attempts

## User Notification

When approval is requested:
1. Display approval request prominently
2. If user is idle, send reminder after 5 minutes
3. Block relevant workflow until decision received
4. Log all approval requests and decisions

## Examples

### Example 1: Handling a Push Approval Request

```
# Incoming message from EOA via AI Maestro
Subject: Push Approval Requested
Priority: high
Content: Branch feature/user-auth ready for push. 5 files modified. All tests passed.

# EAMA presents to user
## Push Approval Requested

**Branch**: feature/user-auth
**Changes**: Added user authentication module
**Files Modified**: 5
**Tests Status**: All 23 tests passed

Do you approve pushing these changes?
- [Approve] - Push to remote
- [Reject] - Cancel push
- [Review] - Show me the changes first

# User responds: "Approve"

# EAMA sends response to EOA
Subject: Push Approved
Content: User approved push for feature/user-auth at 2025-01-30T10:00:00Z
```

### Example 2: Security Approval with Critical Risk

```
# EAMA receives security approval request
## Security Approval Required

**Action**: Update production database schema
**Risk Level**: critical
**Affected Systems**: users, orders, payments
**Justification**: Required for GDPR compliance
**Rollback Plan**: Restore from backup-2025-01-29

This action has security implications. Do you authorize it?
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Approval request timeout | No user response in 24 hours | Auto-reject and notify requesting role |
| Invalid approval type | Unknown type in request | Query sender for clarification |
| State file write failure | Permissions or disk issue | Retry 3 times, then escalate to user |
| Missing handoff context | Incomplete request | Return to sender with "INCOMPLETE" flag |

## Resources

- [Message Templates](../../shared/message_templates.md)
- [Handoff Template](../../shared/handoff_template.md)
