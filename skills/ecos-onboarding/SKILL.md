---
name: ecos-onboarding
description: Use when onboarding new agents to the team, providing role briefings, conducting project handoffs, and ensuring agents are ready to contribute effectively. Trigger with new agent or new project setup.
license: Apache-2.0
compatibility: Requires AI Maestro messaging API access, project documentation access, and role definition documents. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ecos-main
workflow-instruction: "Step 4"
procedure: "proc-create-team"
---

# Emasoft Chief of Staff Onboarding Skill

## Overview

Agent onboarding is the process of integrating new AI agents into a coordinated team. The Chief of Staff ensures that each new agent understands their role, the project context, key procedures, and how to communicate with teammates. Proper onboarding reduces confusion, prevents errors, and accelerates time-to-productivity.

## Prerequisites

Before using this skill, ensure:
1. Agent to be onboarded is created and running
2. Project documentation is available
3. Team registry is accessible

## Instructions

1. Identify what needs onboarding (agent or project)
2. Gather required context and documentation
3. Send onboarding materials to target
4. Verify understanding and readiness

## Output

| Onboarding Type | Output |
|-----------------|--------|
| New agent | Agent understands role and context |
| New project | Project registered, team assigned |
| Role change | Agent updated with new responsibilities |

## What Is Agent Onboarding?

Agent onboarding is a structured process to prepare a new agent for effective participation in a multi-agent team. Unlike human onboarding which may take days or weeks, agent onboarding happens in minutes but must be thorough and precise.

**Key characteristics:**
- **Structured**: Follows a defined checklist
- **Role-specific**: Tailored to the agent's assigned role
- **Context-rich**: Provides necessary project knowledge
- **Verifiable**: Confirms understanding before work begins

## Onboarding Components

### 1. Onboarding Checklist
A systematic list of items to cover during onboarding.

### 2. Role Briefing
Detailed explanation of the agent's role, responsibilities, and expectations.

### 3. Project Handoff
Transfer of essential project knowledge, conventions, and current state.

## Core Procedures

### PROCEDURE 1: Execute Onboarding Checklist

**When to use:** When a new agent joins the team or when reassigning an agent to a different project.

**Steps:** Initiate onboarding session, verify agent identity, work through each checklist item, confirm completion, document onboarding.

**Related documentation:**

#### Onboarding Checklist ([references/onboarding-checklist.md](references/onboarding-checklist.md))
- 1.1 Checklist purpose → Purpose Of The Onboarding Checklist section
- 1.2 Pre-onboarding steps → Pre Onboarding Preparation section
- 1.3 Core checklist items → Core Onboarding Checklist section
- 1.4 Role-specific items → Role Specific Additions section
- 1.5 Verification steps → Onboarding Verification section
- 1.6 Documentation → Documenting Onboarding Completion section
- 1.7 Examples → Onboarding Checklist Examples section
- 1.8 Issues → Troubleshooting section

### PROCEDURE 2: Deliver Role Briefing

**When to use:** After initial onboarding checklist, when role changes, or when role responsibilities are updated.

**Steps:** Retrieve role definition, explain responsibilities, clarify reporting structure, set expectations, answer questions, confirm understanding.

**Related documentation:**

#### Role Briefing ([references/role-briefing.md](references/role-briefing.md))
- 2.1 Briefing components → Role Briefing Components section
- 2.2 Responsibility explanation → Explaining Role Responsibilities section
- 2.3 Reporting structure → Clarifying Reporting Structure section
- 2.4 Expectations setting → Setting Performance Expectations section
- 2.5 Q&A handling → Handling Agent Questions section
- 2.6 Understanding confirmation → Confirming Role Understanding section
- 2.7 Examples → Role Briefing Examples section
- 2.8 Issues → Troubleshooting section

### PROCEDURE 3: Conduct Project Handoff

**When to use:** When onboarding to a specific project, when transferring work between agents, or when bringing backup agents up to speed.

**Steps:** Provide project overview, share current state, explain conventions, transfer working knowledge, verify comprehension.

**Related documentation:**

#### Project Handoff ([references/project-handoff.md](references/project-handoff.md))
- 3.1 Handoff preparation → Preparing For Project Handoff section
- 3.2 Project overview → Providing Project Overview section
- 3.3 Current state → Sharing Current State section
- 3.4 Conventions → Explaining Project Conventions section
- 3.5 Knowledge transfer → Transferring Working Knowledge section
- 3.6 Verification → Verifying Handoff Completion section
- 3.7 Examples → Project Handoff Examples section
- 3.8 Issues → Troubleshooting section

## Task Checklist

Copy this checklist and track your progress:

- [ ] Understand onboarding purpose and components
- [ ] Learn PROCEDURE 1: Execute onboarding checklist
- [ ] Learn PROCEDURE 2: Deliver role briefing
- [ ] Learn PROCEDURE 3: Conduct project handoff
- [ ] Practice complete onboarding workflow
- [ ] Create onboarding templates for common roles
- [ ] Verify onboarding completeness metrics

## Examples

### Example 1: Initiating Onboarding for New Developer

```bash
# Send onboarding initiation message
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "new-developer-agent",
    "subject": "Welcome - Onboarding Session Starting",
    "priority": "high",
    "content": {
      "type": "request",
      "message": "Welcome to the team. I am the Chief of Staff and will conduct your onboarding. Please confirm you are ready to begin the onboarding process."
    }
  }'
```

### Example 2: Role Briefing Message

```markdown
# Role Briefing: Developer

## Your Assigned Role
You are assigned as a **Developer** on the Authentication Module.

## Responsibilities
1. Implement features from the backlog
2. Write unit tests for all new code
3. Update documentation for your changes
4. Participate in code reviews when requested

## Reporting Structure
- **Report to:** orchestrator-master for task assignments
- **Coordinate with:** auth-code-reviewer for reviews
- **Escalate to:** chief-of-staff for blockers

## Expectations
- Acknowledge task assignments promptly
- Provide regular status updates during active work
- Request clarification if requirements are unclear
- Follow project coding conventions

Please confirm you understand these responsibilities.
```

### Example 3: Project Handoff Summary

```markdown
# Project Handoff: Authentication Module

## Project Overview
We are building a secure authentication module for the main application.
Current sprint: Sprint 5 (2 weeks remaining)

## Current State
- Login endpoint: COMPLETE
- Logout endpoint: IN PROGRESS (60%)
- Password reset: NOT STARTED
- Session management: BLOCKED (waiting on logout)

## Key Files
- src/auth/login.py - Login implementation
- src/auth/logout.py - Logout implementation (your focus)
- tests/auth/ - Test directory

## Conventions
- Use async/await for all I/O operations
- All endpoints return JSON
- Error responses use standard error format
- Tests required for all new functions

## Active Context
The logout endpoint is partially implemented. Current work is at line 145.
Next step: Implement session invalidation.
```

## Error Handling

### Issue: Agent does not respond to onboarding initiation

**Symptoms:** No acknowledgment, onboarding cannot begin.

**Solution:** Verify agent session is active, retry with higher priority, check for messaging issues, escalate to user if persistent.

### Issue: Agent claims not to understand role briefing

**Symptoms:** Agent asks repeated clarification questions, demonstrates confusion.

**Solution:** Provide more specific examples, break down responsibilities into smaller steps, have agent repeat back understanding, consider if role is appropriate match.

### Issue: Project handoff is incomplete

**Symptoms:** Agent lacks critical context, makes errors based on missing information.

**Solution:** Review handoff checklist, identify gaps, send supplementary information, verify understanding of each critical point.

## Handoff Validation Checklist

Before sending any handoff document to a new agent, validate using this checklist:

```markdown
### Handoff Validation Checklist

Before sending handoff:
- [ ] All required fields present (from/to/type/UUID/task)
- [ ] UUID is unique (check existing handoffs: `ls $CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/`)
- [ ] Target agent exists and is alive (`curl -s "http://localhost:23000/api/agents" | jq -r '.agents[].name'`)
- [ ] All referenced files exist (`test -f <path> && echo "EXISTS" || echo "MISSING"`)
- [ ] No placeholder [TBD] markers (`grep -r "\[TBD\]" handoff.md`)
- [ ] Document is valid markdown (no broken links, proper formatting)
- [ ] Acceptance criteria clearly defined
- [ ] Current state accurately reflects reality
- [ ] Contact information for questions provided
```

**Validation command:**
```bash
# Validate handoff document before sending
python scripts/ecos_validate_handoff.py --file <handoff_document.md>
```

**Required fields for all handoffs:**

| Field | Description | Example |
|-------|-------------|---------|
| `from` | Sending agent name | `ecos-chief-of-staff` |
| `to` | Target agent name | `new-developer-agent` |
| `type` | Handoff type | `project-handoff`, `role-briefing`, `emergency-handoff` |
| `UUID` | Unique handoff identifier | `HO-20250204-auth-001` |
| `task` | Task or role being handed off | `Authentication Module Development` |

## Key Takeaways

1. **Onboarding is mandatory** - Never assign work before onboarding is complete
2. **Verification is essential** - Confirm understanding at each step
3. **Role briefing must be specific** - Generic descriptions cause confusion
4. **Project handoff includes state** - Not just structure but current progress
5. **Document completion** - Record that onboarding happened and what was covered
6. **Validate before sending** - Always run handoff validation checklist

## Resources

- [Onboarding Checklist](references/onboarding-checklist.md)
- [Role Briefing](references/role-briefing.md)
- [Project Handoff](references/project-handoff.md)

---

**Version:** 1.0
**Last Updated:** 2025-02-01
**Target Audience:** Emasoft Chief of Staff Agent
**Difficulty Level:** Intermediate
