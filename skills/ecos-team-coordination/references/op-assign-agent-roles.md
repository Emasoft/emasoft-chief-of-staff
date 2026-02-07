---
operation: assign-agent-roles
procedure: proc-notify-team-ready
workflow-instruction: Step 5 - Team Ready Notification
parent-skill: ecos-team-coordination
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Assign Agent Roles

## When to Use

Trigger this operation when:
- Onboarding a new agent to the team
- Reassigning responsibilities between agents
- Restructuring the team composition
- An agent's current role no longer matches task requirements

## Prerequisites

- Team registry is accessible
- The `agent-messaging` skill is available
- The `ai-maestro-agents-management` skill is available
- Target agent is registered and reachable
- Role definitions are available (see role-assignment.md Section 1.2)

## Procedure

### Step 1: Identify Required Role

Determine which role needs to be filled based on current team needs and pending tasks.

Use the `ai-maestro-agents-management` skill to list all active agent sessions and their metadata, including current role assignments.

### Step 2: Match Agent Capabilities

Evaluate available agents against role requirements. Consider:
- Agent specialization (code-impl, test-engineer, docs-writer, etc.)
- Current workload
- Prior experience with similar tasks

### Step 3: Send Role Assignment Message

Use the `agent-messaging` skill to send:
- **Recipient**: the target agent session name
- **Subject**: `Role Assignment: [Role Name]`
- **Priority**: `high`
- **Content**: type `role-assignment`, message: "You are assigned the [Role Name] role. Responsibilities: [list responsibilities]."

### Step 4: Confirm Acceptance

Wait for agent acknowledgment (up to 60 seconds per ACK timeout policy).

Use the `agent-messaging` skill to check for unread messages from the target agent. Look for a response of type `acknowledgment` confirming role acceptance.

### Step 5: Update Team Roster

Record the role assignment in the team registry:
- Agent session name
- Assigned role
- Assignment timestamp
- Responsibilities

## Checklist

Copy this checklist and track your progress:

- [ ] Identified the required role
- [ ] Evaluated available agents for capability match
- [ ] Sent role assignment message via `agent-messaging` skill
- [ ] Received acknowledgment from agent
- [ ] Updated team roster with new assignment
- [ ] Verified agent understands their responsibilities

## Examples

### Example: Assigning Code Reviewer Role

**Scenario:** A new PR needs review, and no agent currently has the Code Reviewer role.

Use the `agent-messaging` skill to send:
- **Recipient**: `helper-agent-generic`
- **Subject**: `Role Assignment: Code Reviewer`
- **Priority**: `high`
- **Content**: type `role-assignment`, message: "You are assigned the Code Reviewer role. Responsibilities: review PRs, enforce code standards, provide constructive feedback, approve or request changes."

**Expected Response:**

The agent should reply with type `acknowledgment`, message: "Role accepted. Ready to review PRs."

### Example: Reassigning Role During Restructure

**Scenario:** Moving test-engineer-01 from Unit Testing to Integration Testing role.

**Step 1:** Use the `agent-messaging` skill to notify the current agent:
- **Recipient**: `test-engineer-01`
- **Subject**: `Role Transition: Integration Testing`
- **Priority**: `high`
- **Content**: type `role-transition`, message: "Your role is changing from Unit Testing to Integration Testing. Please complete current unit tests and prepare for integration test responsibilities. Acknowledge when ready."

**Step 2:** Wait for acknowledgment, then update the team roster.

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| No acknowledgment received | Agent offline or busy | Retry with higher priority after 60s; use the `ai-maestro-agents-management` skill to check agent status |
| Agent rejects role | Capability mismatch or overload | Discuss with agent, consider alternative assignment, or redistribute workload |
| Multiple agents claim same role | Coordination failure | Arbitrate based on capability match, assign one and notify others of resolution |
| Team roster update fails | Registry unavailable | Log assignment locally, retry roster update when registry recovers |

## Related Operations

- [op-send-team-messages.md](op-send-team-messages.md) - For broadcasting role changes
- [op-maintain-teammate-awareness.md](op-maintain-teammate-awareness.md) - For tracking who has which role
- [role-assignment.md](role-assignment.md) - Detailed role definitions and procedures
