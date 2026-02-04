# Onboarding Checklist Reference

## Table of Contents

- 1.1 [Purpose Of The Onboarding Checklist](#11-purpose-of-the-onboarding-checklist)
- 1.2 [Pre Onboarding Preparation](#12-pre-onboarding-preparation)
- 1.3 [Core Onboarding Checklist](#13-core-onboarding-checklist)
- 1.4 [Role Specific Additions](#14-role-specific-additions)
- 1.5 [Onboarding Verification](#15-onboarding-verification)
- 1.6 [Documenting Onboarding Completion](#16-documenting-onboarding-completion)
- 1.7 [Onboarding Checklist Examples](#17-onboarding-checklist-examples)
- 1.8 [Troubleshooting](#18-troubleshooting)

---

## 1.1 Purpose Of The Onboarding Checklist

The onboarding checklist ensures that every new agent receives consistent, complete preparation before beginning work. Without a checklist, critical information may be missed, leading to errors, confusion, and wasted effort.

**Benefits of using a checklist:**
- Ensures no critical items are forgotten
- Provides consistent experience for all agents
- Creates audit trail of what was covered
- Enables verification of readiness
- Reduces onboarding time through structure

**Checklist philosophy:**
- Cover essentials, not everything
- Verify understanding, not just delivery
- Adapt to role, not one-size-fits-all
- Document completion for accountability

---

## 1.2 Pre Onboarding Preparation

Before initiating onboarding with a new agent, the Chief of Staff must prepare.

### Gather Information

**Agent information:**
- Session name (full domain-subdomain-name format)
- Intended role
- Any special capabilities or constraints
- Previous experience if rejoining

**Project information:**
- Current project state
- Active tasks and their status
- Key documentation locations
- Current team composition

### Prepare Materials

**Documents to have ready:**
- Role definition document
- Project overview document
- Coding/work conventions
- Communication protocols
- Team roster with roles

### Verify Prerequisites

Check that:
- Agent session is active and responsive
- AI Maestro messaging is working
- Required documents are accessible
- Time is available for complete onboarding

### Pre-Onboarding Checklist

```markdown
## Pre-Onboarding Checklist

Agent: [session name]
Role: [intended role]
Date: [date]

- [ ] Agent session verified active
- [ ] Role definition document ready
- [ ] Project overview prepared
- [ ] Conventions document available
- [ ] Team roster current
- [ ] AI Maestro messaging tested
- [ ] Time blocked for onboarding (est. 15-30 min)
```

---

## 1.3 Core Onboarding Checklist

The core checklist applies to all agents regardless of role.

### Phase 1: Welcome and Orientation

```markdown
## Phase 1: Welcome and Orientation

- [ ] 1.1 Send welcome message
- [ ] 1.2 Confirm agent acknowledgment
- [ ] 1.3 Explain onboarding process overview
- [ ] 1.4 Set expectations for session duration
```

### Phase 2: Team Introduction

```markdown
## Phase 2: Team Introduction

- [ ] 2.1 Explain team structure
- [ ] 2.2 Introduce key team members and roles
- [ ] 2.3 Explain Chief of Staff role
- [ ] 2.4 Explain orchestrator role
- [ ] 2.5 Share team roster location
```

### Phase 3: Communication Setup

```markdown
## Phase 3: Communication Setup

- [ ] 3.1 Verify AI Maestro connectivity
- [ ] 3.2 Explain message priority levels
- [ ] 3.3 Explain expected response times
- [ ] 3.4 Test bidirectional messaging
- [ ] 3.5 Explain escalation procedures
```

### Phase 4: Role Assignment

```markdown
## Phase 4: Role Assignment

- [ ] 4.1 Explain assigned role
- [ ] 4.2 Detail specific responsibilities
- [ ] 4.3 Clarify what is NOT in scope
- [ ] 4.4 Explain reporting structure
- [ ] 4.5 Confirm role understanding
```

### Phase 5: Project Context

```markdown
## Phase 5: Project Context

- [ ] 5.1 Provide project overview
- [ ] 5.2 Explain current state
- [ ] 5.3 Share active goals/sprint info
- [ ] 5.4 Point to key documentation
- [ ] 5.5 Explain conventions and standards
```

### Phase 6: Tooling and Access

```markdown
## Phase 6: Tooling and Access

- [ ] 6.1 Verify file system access
- [ ] 6.2 Verify required tool availability
- [ ] 6.3 Explain any access restrictions
- [ ] 6.4 Test critical operations
```

### Phase 7: First Task

```markdown
## Phase 7: First Task

- [ ] 7.1 Assign simple first task
- [ ] 7.2 Explain task expectations
- [ ] 7.3 Set task priority
- [ ] 7.4 Explain how to report completion
- [ ] 7.5 Confirm agent is ready to begin
```

---

## 1.4 Role Specific Additions

Each role has additional checklist items beyond the core checklist.

### Developer Role Additions

```markdown
## Developer-Specific Items

- [ ] D.1 Explain code submission process
- [ ] D.2 Explain testing requirements
- [ ] D.3 Share coding style guide
- [ ] D.4 Explain PR creation process
- [ ] D.5 Introduce code reviewer contact
```

### Code Reviewer Role Additions

```markdown
## Code Reviewer-Specific Items

- [ ] R.1 Explain review criteria
- [ ] R.2 Share review checklist
- [ ] R.3 Explain approval process
- [ ] R.4 Explain how to request changes
- [ ] R.5 Set review SLA expectations
```

### Test Engineer Role Additions

```markdown
## Test Engineer-Specific Items

- [ ] T.1 Explain test framework(s) used
- [ ] T.2 Share test directory structure
- [ ] T.3 Explain coverage requirements
- [ ] T.4 Explain test result reporting
- [ ] T.5 Introduce CI/CD pipeline overview
```

### DevOps Role Additions

```markdown
## DevOps-Specific Items

- [ ] O.1 Explain deployment pipeline
- [ ] O.2 Share infrastructure access
- [ ] O.3 Explain monitoring dashboards
- [ ] O.4 Share incident response procedures
- [ ] O.5 Explain change management process
```

---

## 1.5 Onboarding Verification

After completing the checklist, verify the agent is truly ready.

### Understanding Check

Ask the agent to summarize back:
1. Their role and top 3 responsibilities
2. Who they report to
3. How to escalate issues
4. Their first assigned task

### Practical Test

Have the agent complete a simple task that exercises:
- Communication (send a message)
- File access (read a document)
- Tool usage (run a simple command)
- Reporting (send completion update)

### Readiness Confirmation

The agent should explicitly confirm:
- "I understand my role as [ROLE]"
- "My responsibilities are [LIST]"
- "I report to [AGENT] for [PURPOSE]"
- "I am ready to begin work on [FIRST TASK]"

### Verification Checklist

```markdown
## Verification Checklist

- [ ] Agent correctly summarized role
- [ ] Agent correctly identified responsibilities
- [ ] Agent correctly stated reporting structure
- [ ] Agent completed practical test successfully
- [ ] Agent explicitly confirmed readiness
```

---

## 1.6 Documenting Onboarding Completion

Onboarding must be documented for audit and recovery purposes.

### Onboarding Record Location

Store onboarding records in:
```
design/memory/onboarding/[session-name]-[date].md
```

### Record Format

```markdown
# Onboarding Record

## Agent Information
- **Session Name:** helper-agent-generic
- **Role Assigned:** Code Reviewer
- **Onboarding Date:** 2025-02-01
- **Onboarded By:** chief-of-staff-agent

## Checklist Completion
- Phase 1 (Welcome): COMPLETE
- Phase 2 (Team): COMPLETE
- Phase 3 (Communication): COMPLETE
- Phase 4 (Role): COMPLETE
- Phase 5 (Project): COMPLETE
- Phase 6 (Tooling): COMPLETE
- Phase 7 (First Task): COMPLETE
- Role-Specific: COMPLETE

## Verification Results
- Understanding Check: PASSED
- Practical Test: PASSED
- Readiness Confirmation: RECEIVED

## First Task Assigned
- Task: Review PR #123
- Priority: High

## Notes
Agent showed strong understanding of review criteria.
Suggested adding review checklist to project docs.

## Status
ONBOARDING COMPLETE - Agent cleared for work
```

### Updating Team Records

After onboarding completion:
1. Add agent to team roster with role
2. Update team capacity metrics
3. Notify orchestrator of new team member
4. Log onboarding in coordination state

---

## 1.7 Onboarding Checklist Examples

### Example: Complete Developer Onboarding Flow

```markdown
# Onboarding Session: libs-svg-svgbbox

## Transcript Summary

10:00 - Sent welcome message
10:01 - Agent acknowledged, confirmed ready
10:02 - Explained team structure (5 members)
10:04 - Covered AI Maestro messaging, tested bidirectional
10:06 - Assigned Developer role for SVG library
10:08 - Detailed responsibilities: implement parser, write tests, docs
10:10 - Provided project overview: SVG parsing library, Sprint 3
10:12 - Shared conventions: TypeScript, Jest tests, JSDoc
10:14 - Verified file access to /libs/svg-parser/
10:15 - Assigned first task: implement basic SVG element parser
10:16 - Agent confirmed understanding and readiness

## Verification
Agent summary: "I am a Developer on SVG library. I implement parser features, write tests, update docs. I report to orchestrator-master."
Practical test: Successfully read project README, sent test message.

## Status: COMPLETE
```

### Example: Abbreviated Re-Onboarding

When an agent rejoins after brief absence:

```markdown
# Re-Onboarding Session: helper-agent-backup

## Context
Agent was offline for 4 hours. No role change.
Abbreviated onboarding focusing on state changes.

## Covered Items
- [ ] Current sprint state (unchanged)
- [ ] Tasks reassigned during absence: 0
- [ ] New team members: 0
- [ ] Pending items for this agent: PR #145 review

## Verification
Agent confirmed current state understanding.

## Status: COMPLETE (abbreviated)
```

---

## 1.8 Troubleshooting

### Issue: Agent is slow to respond during onboarding

**Symptoms:** Long delays between messages, onboarding taking too long.

**Possible causes:**
- Agent processing other work
- Network latency
- Agent context is full

**Resolution:**
1. Ask agent to focus exclusively on onboarding
2. Simplify messages, send smaller chunks
3. Set explicit response timeout expectations
4. If persistent, reschedule onboarding

### Issue: Agent cannot access required resources

**Symptoms:** File read failures, tool not found errors.

**Possible causes:**
- Permissions issue
- Wrong path provided
- Tool not installed in agent environment

**Resolution:**
1. Verify paths are absolute and correct
2. Check agent has required tool access
3. Provide alternative access method if available
4. Document limitation and escalate if blocking

### Issue: Agent misunderstands role after briefing

**Symptoms:** Agent asks questions outside role scope, attempts unauthorized actions.

**Possible causes:**
- Role briefing was unclear
- Agent has preconceptions from prior context
- Multiple roles mentioned caused confusion

**Resolution:**
1. Repeat role briefing with emphasis on scope
2. Explicitly state what is NOT in scope
3. Use examples of correct behavior
4. Have agent summarize back until correct

### Issue: Onboarding interrupted

**Symptoms:** Session ended mid-onboarding, agent went offline.

**Possible causes:**
- Agent session crashed
- User intervention
- System issue

**Resolution:**
1. Document progress at interruption point
2. When agent returns, resume from last completed phase
3. Do quick recap before continuing
4. Re-verify completed phases if significant time passed

### Issue: Agent refuses role assignment

**Symptoms:** Agent explicitly declines role or states inability to perform.

**Possible causes:**
- Capability mismatch
- Conflicting prior assignment
- Agent has additional context about limitations

**Resolution:**
1. Understand the specific concern
2. If valid, assign different role
3. If misunderstanding, clarify and retry
4. If persistent refusal, escalate to user

---

**Version:** 1.0
**Last Updated:** 2025-02-01
