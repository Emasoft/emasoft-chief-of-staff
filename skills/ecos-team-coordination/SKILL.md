---
name: ecos-team-coordination
description: Use when coordinating team members across agent sessions, assigning roles, managing messaging, and maintaining team status. Trigger with team formation, updates, or coordination needs.
user-invocable: false
license: Apache-2.0
compatibility: Requires AI Maestro messaging API access, session name resolution, and inter-agent communication capabilities. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ecos-main
workflow-instruction: "Step 5"
procedure: "proc-notify-team-ready"
---

# Emasoft Chief of Staff Team Coordination Skill

## Overview

Team coordination is a core responsibility of the Chief of Staff agent. This skill teaches you how to manage distributed agent teams, assign roles effectively, coordinate messaging between team members, and maintain awareness of all active teammates and their current status.

## Prerequisites

Before using this skill, ensure:
1. Team registry is accessible
2. AI Maestro messaging is available
3. Agent roles are defined

## Instructions

1. Identify coordination need
2. Query team registry for current state
3. Execute coordination action
4. Update team registry and notify agents

## Output

| Coordination Type | Output |
|-------------------|--------|
| Team formation | New team created, agents assigned |
| Role assignment | Agent roles updated, registry modified |
| Status sync | All agents aligned on current state |

## What Is Team Coordination?

Team coordination is the process of organizing multiple AI agents to work together on shared goals. The Chief of Staff acts as the central coordination point, ensuring agents are assigned appropriate roles, can communicate effectively, and remain aware of each other's progress and status.

**Key characteristics:**
- **Distributed**: Team members run in separate Claude Code sessions
- **Asynchronous**: Communication happens via message queues, not direct calls
- **Role-based**: Each agent has a defined role with specific responsibilities
- **Status-aware**: Chief of Staff tracks all team member states

## Team Coordination Components

### 1. Role Assignment
Matching agents to roles based on capabilities and task requirements.

### 2. Team Messaging
Facilitating communication between team members via AI Maestro.

### 3. Teammate Awareness
Maintaining visibility into all team members' current status and activities.

## Core Procedures

### PROCEDURE 1: Assign Agent Roles

**When to use:** When onboarding a new agent, reassigning responsibilities, or restructuring the team.

**Steps:** Identify required role, match agent capabilities, send role assignment message, confirm acceptance, update team roster.

**Related documentation:**

#### Role Assignment ([references/role-assignment.md](references/role-assignment.md))
- 1.1 Understanding roles → What Are Agent Roles section
- 1.2 Role definitions → Standard Role Definitions section
- 1.3 Capability matching → Matching Agents To Roles section
- 1.4 Assignment procedure → Role Assignment Procedure section
- 1.5 Role confirmation → Confirming Role Acceptance section
- 1.6 Role transitions → Managing Role Transitions section
- 1.7 Examples → Role Assignment Examples section
- 1.8 Issues → Troubleshooting section

### PROCEDURE 2: Send Team Messages

**When to use:** When broadcasting updates, sending targeted instructions, or facilitating inter-agent communication.

**Steps:** Identify recipients, compose message with priority, send via AI Maestro API, confirm delivery, log in coordination state.

**Related documentation:**

#### Team Messaging ([references/team-messaging.md](references/team-messaging.md))
- 2.1 Message types → Team Message Types section
- 2.2 Message priorities → Message Priority Levels section
- 2.3 Broadcast messages → Sending Broadcast Messages section
- 2.4 Targeted messages → Sending Targeted Messages section
- 2.5 Message routing → Message Routing Rules section
- 2.6 Delivery confirmation → Confirming Message Delivery section
- 2.7 Examples → Team Messaging Examples section
- 2.8 Issues → Troubleshooting section

### PROCEDURE 3: Maintain Teammate Awareness

**When to use:** Continuously during coordination, before assigning tasks, when reporting team status.

**Steps:** Poll AI Maestro for active sessions, query each agent's status, update team roster, identify inactive agents, flag issues.

**Related documentation:**

#### Teammate Awareness ([references/teammate-awareness.md](references/teammate-awareness.md))
- 3.1 Team roster → Managing The Team Roster section
- 3.2 Status polling → Polling Agent Status section
- 3.3 Activity detection → Detecting Agent Activity section
- 3.4 Inactive handling → Handling Inactive Agents section
- 3.5 Status reporting → Reporting Team Status section
- 3.6 Examples → Teammate Awareness Examples section
- 3.7 Issues → Troubleshooting section

## Task Checklist

Copy this checklist and track your progress:

- [ ] Understand team coordination purpose and components
- [ ] Learn PROCEDURE 1: Assign agent roles
- [ ] Learn PROCEDURE 2: Send team messages
- [ ] Learn PROCEDURE 3: Maintain teammate awareness
- [ ] Practice role assignment workflow
- [ ] Practice team messaging via AI Maestro
- [ ] Practice status monitoring and reporting

## Examples

### Example 1: Assigning a Role to a New Agent

Use the `agent-messaging` skill to send a role assignment message:
- **Recipient**: `helper-agent-generic`
- **Subject**: `Role Assignment: Code Reviewer`
- **Priority**: `high`
- **Content**: type `role-assignment`, explaining that the agent is assigned the Code Reviewer role with responsibilities: review PRs, enforce code standards, provide feedback

**Verify**: confirm message delivery and await role acceptance acknowledgment.

### Example 2: Broadcasting a Team Update

Use the `agent-messaging` skill to broadcast a message to all team members:
- **Subject**: `Sprint Planning Complete`
- **Priority**: `normal`
- **Content**: type `announcement`, informing that Sprint 5 planning is complete and all tasks are assigned

**Verify**: confirm delivery to all team members.

### Example 3: Checking Team Status

Use the `ai-maestro-agents-management` skill to list all active sessions and their status, including each agent's name, status, and last seen timestamp.

**Verify**: all expected team members appear in the list with correct status.

## Error Handling

### Issue: Agent does not respond to role assignment

**Symptoms:** No acknowledgment received, agent continues previous behavior.

**Solution:** Retry with higher priority, check if agent is active, escalate to user if unresponsive after 3 attempts.

### Issue: Team messages are not delivered

**Symptoms:** Delivery confirmation missing, recipients unaware of messages.

**Solution:** Verify AI Maestro is running, check recipient session names, validate message format.

### Issue: Team roster becomes stale

**Symptoms:** Inactive agents shown as active, missing new agents, wrong status.

**Solution:** Force refresh via status polling, clear and rebuild roster, verify session registry.

## Key Takeaways

1. **Role assignment requires confirmation** - Do not assume assignment succeeded without acknowledgment
2. **Message priority matters** - Use appropriate priority to ensure timely delivery
3. **Continuous awareness is essential** - Poll status regularly, not just when needed
4. **Log all coordination actions** - Maintain audit trail for debugging and recovery
5. **Handle failures gracefully** - Retry, escalate, but never ignore coordination failures

## Resources

- [Role Assignment](references/role-assignment.md)
- [Team Messaging](references/team-messaging.md)
- [Teammate Awareness](references/teammate-awareness.md)

---

**Version:** 1.0
**Last Updated:** 2025-02-01
**Target Audience:** Emasoft Chief of Staff Agent
**Difficulty Level:** Intermediate
