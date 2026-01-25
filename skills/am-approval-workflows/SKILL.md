---
name: am-approval-workflows
description: Standard workflows for handling approval requests from other roles
triggers:
  - Any role sends an approval request via AI Maestro
  - User needs to make a decision about code, releases, or security
  - Quality gates require human authorization
---

# Approval Workflows Skill

## Purpose

This skill provides the Assistant Manager with standard workflows for handling approval requests from other roles and presenting them to the user for decision.

## Approval Types

### 1. Push Approval

**Trigger**: Code is ready to be pushed to remote repository

**Workflow**:
1. Receive approval request from Orchestrator/Integrator
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
1. Receive approval request from Integrator
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
4. Send approval response to Integrator

### 3. Publish Approval

**Trigger**: Package/release is ready to be published

**Workflow**:
1. Receive approval request from Integrator
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
4. Send approval response to Integrator

### 4. Security Approval

**Trigger**: Action with security implications requires authorization

**Workflow**:
1. Receive approval request from any role
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

**Trigger**: Architect has completed design document

**Workflow**:
1. Receive completion signal from Architect
2. Present to user:
   ```
   ## Design Approval Requested

   **Design**: {design_name}
   **Document**: {path_to_design_doc}
   **Modules**: {count} modules defined
   **Estimated Scope**: {scope_summary}

   Review the design document and approve to proceed with implementation.
   - [Approve] - Proceed to orchestration
   - [Request Changes] - Send back to Architect
   - [Discuss] - I have questions
   ```
3. Record user decision
4. If approved, create handoff to Orchestrator

## Approval State Tracking

All approvals are tracked in state file:

```yaml
approvals:
  - id: "approval-{uuid}"
    type: "merge"
    requested_by: "integrator"
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

## References

- [Message Templates](../../shared/message_templates.md)
- [Handoff Template](../../shared/handoff_template.md)
