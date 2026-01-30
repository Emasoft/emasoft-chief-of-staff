---
name: eama-github-routing
description: Use when routing GitHub operations (issues, PRs, projects, releases) to the appropriate specialist agent
context: fork
triggers:
  - User requests GitHub operation (issues, PRs, projects)
  - GitHub webhook event requires agent action
  - Kanban synchronization needed
---

# GitHub Operation Routing Skill

## Prerequisites

- GitHub CLI (`gh`) must be installed and authenticated
- AI Maestro messaging system must be running
- EIA, EAA, and EOA agents must be available

## Instructions

1. Identify the type of GitHub operation requested (issue, PR, kanban, release)
2. Use the appropriate decision tree to determine routing
3. Check for design or module context that affects routing
4. Create handoff document with required content
5. Send handoff to the appropriate specialist via AI Maestro
6. Track the handoff status

## Table of Contents

1. [Purpose](#purpose)
2. [Primary Routing Principle](#primary-routing-principle)
3. [Master Decision Tree](#master-decision-tree)
4. [Issue Operations Decision Tree](#issue-operations-decision-tree)
   - 4.1 [Issue Routing Matrix](#issue-routing-matrix)
5. [Pull Request Operations Decision Tree](#pull-request-operations-decision-tree)
   - 5.1 [PR Routing Matrix](#pr-routing-matrix)
6. [Kanban/Projects Operations Decision Tree](#kanbanprojects-operations-decision-tree)
   - 6.1 [Kanban Routing Matrix](#kanban-routing-matrix)
7. [Release Operations Decision Tree](#release-operations-decision-tree)
   - 7.1 [Release Routing Matrix](#release-routing-matrix)
8. [Handoff Content Requirements](#handoff-content-requirements)
   - 8.1 [For EIA (Integrator) GitHub Handoffs](#for-eia-integrator-github-handoffs)
   - 8.2 [For EAA (Architect) Design-GitHub Handoffs](#for-eaa-architect-design-github-handoffs)
   - 8.3 [For EOA (Orchestrator) Module-GitHub Handoffs](#for-eoa-orchestrator-module-github-handoffs)
9. [UUID Tracking Across GitHub Operations](#uuid-tracking-across-github-operations)
   - 9.1 [UUID Reference Format in GitHub](#uuid-reference-format-in-github)
   - 9.2 [Searching by UUID](#searching-by-uuid)
10. [Error Handling](#error-handling)
    - 10.1 [Ambiguous Routing](#ambiguous-routing)
    - 10.2 [Missing Context](#missing-context)
    - 10.3 [Agent Unavailable](#agent-unavailable)
11. [References](#references)

---


## Overview

This skill provides decision trees for routing GitHub operations to the appropriate specialist role:
- **EIA** (Integrator Agent) - Primary GitHub handler
- **EAA** (Architect Agent) - Design-linked GitHub operations
- **EOA** (Orchestrator Agent) - Module-related GitHub operations

## Primary Routing Principle

**EIA is the default GitHub handler.** Route to EAA or EOA only when the operation has design or module context.

## Master Decision Tree

```
GitHub operation requested
          │
          ▼
┌────────────────────────────┐
│  What type of operation?   │
└──────────────┬─────────────┘
               │
    ┌──────────┼──────────┬──────────────┐
    │          │          │              │
    ▼          ▼          ▼              ▼
 ISSUE       PR      KANBAN/PROJECT   RELEASE
    │          │          │              │
    ▼          ▼          ▼              ▼
[Issue      [PR        [Project       [Release
 Tree]       Tree]      Tree]          Tree]
```

## Issue Operations Decision Tree

```
┌─────────────────────────────────┐
│ Issue operation requested       │
└───────────────┬─────────────────┘
                ▼
┌─────────────────────────────────┐
│ Is this linked to a design doc? │
└───────────────┬─────────────────┘
        ┌───────┴───────┐
        │ YES           │ NO
        ▼               ▼
┌───────────────┐  ┌─────────────────────┐
│ What action?  │  │ Is this a module    │
└───────┬───────┘  │ implementation task?│
        │          └──────────┬──────────┘
    ┌───┴───┐          ┌──────┴───────┐
    │       │          │ YES          │ NO
    ▼       ▼          ▼              ▼
CREATE   UPDATE   ┌──────────┐   ┌──────────┐
LINK     LINK     │ Route to │   │ Route to │
    │       │     │ EOA      │   │ EIA      │
    │       │     └──────────┘   └──────────┘
    ▼       ▼
┌──────────────┐
│ Route to EAA │
│ with design  │
│ UUID         │
└──────────────┘
```

### Issue Routing Matrix

| Scenario | Route To | Handoff Content |
|----------|----------|-----------------|
| Create bug report | EIA | Issue template, reproduction steps |
| Create feature request | EIA | Issue template, requirements |
| Create issue FROM design | EAA | Design UUID, section reference |
| Link existing issue to design | EAA | Issue number, design UUID |
| Update issue labels/status | EIA | Issue number, changes |
| Close issue with verification | EIA | Issue number, verification results |
| Create module task issue | EOA | Module UUID, task details |
| Track implementation progress | EOA | Issue number, module UUID |

## Pull Request Operations Decision Tree

```
┌─────────────────────────────────┐
│ PR operation requested          │
└───────────────┬─────────────────┘
                ▼
┌─────────────────────────────────┐
│ What operation type?            │
└───────────────┬─────────────────┘
                │
    ┌───────────┼───────────┬────────────┐
    │           │           │            │
    ▼           ▼           ▼            ▼
 CREATE      REVIEW      MERGE       UPDATE
    │           │           │            │
    ▼           ▼           ▼            ▼
┌────────┐ ┌────────┐ ┌────────┐  ┌────────┐
│ Route  │ │ Route  │ │ Route  │  │ Route  │
│ to EIA │ │ to EIA │ │ to EIA │  │ to EIA │
└────────┘ └────────┘ └────────┘  └────────┘
```

**Note**: All PR operations go to EIA. EIA may consult with EAA for design validation or EOA for implementation verification.

### PR Routing Matrix

| Operation | Route To | Handoff Content |
|-----------|----------|-----------------|
| Create PR | EIA | Branch, description, linked issues |
| Review PR | EIA | PR number, review criteria |
| Request changes | EIA | PR number, requested changes |
| Approve PR | EIA | PR number, approval notes |
| Merge PR | EIA | PR number, merge strategy |
| Close PR without merge | EIA | PR number, reason |

## Kanban/Projects Operations Decision Tree

```
┌─────────────────────────────────┐
│ Kanban/Project operation        │
└───────────────┬─────────────────┘
                ▼
┌─────────────────────────────────┐
│ What operation type?            │
└───────────────┬─────────────────┘
                │
    ┌───────────┼───────────┬───────────────┐
    │           │           │               │
    ▼           ▼           ▼               ▼
  SYNC      CREATE       MOVE           STATUS
  BOARD      ITEM        CARD           QUERY
    │           │           │               │
    ▼           ▼           ▼               ▼
┌────────┐ ┌─────────────────────┐   ┌──────────┐
│ Route  │ │ Is item a design    │   │ Handle   │
│ to EIA │ │ or module?          │   │ locally  │
└────────┘ └──────────┬──────────┘   │ (EAMA)   │
                      │              └──────────┘
              ┌───────┴───────┐
              │ DESIGN        │ MODULE
              ▼               ▼
        ┌──────────┐   ┌──────────┐
        │ Route to │   │ Route to │
        │ EAA      │   │ EOA      │
        └──────────┘   └──────────┘
```

### Kanban Routing Matrix

| Operation | Route To | Handoff Content |
|-----------|----------|-----------------|
| Sync board with GitHub | EIA | Project ID, sync scope |
| Create design card | EAA | Design UUID, card details |
| Create module card | EOA | Module UUID, card details |
| Move card (non-specific) | EIA | Card ID, target column |
| Move design card | EAA | Card ID, design context |
| Move module card | EOA | Card ID, module context |
| Query board status | EAMA (local) | Project ID |
| Archive completed items | EIA | Project ID, archive criteria |

## Release Operations Decision Tree

```
┌─────────────────────────────────┐
│ Release operation requested     │
└───────────────┬─────────────────┘
                ▼
┌─────────────────────────────────┐
│ All operations go to EIA        │
│ (Integrator owns releases)      │
└───────────────┬─────────────────┘
                │
                ▼
          ┌──────────┐
          │ Route to │
          │ EIA      │
          └──────────┘
```

### Release Routing Matrix

| Operation | Route To | Handoff Content |
|-----------|----------|-----------------|
| Create release | EIA | Version, changelog, assets |
| Draft release notes | EIA | Version, commit range |
| Tag version | EIA | Tag name, commit SHA |
| Publish release | EIA | Release ID, publish settings |
| Update release | EIA | Release ID, changes |

## Handoff Content Requirements

### For EIA (Integrator) GitHub Handoffs

```markdown
## GitHub Operation Handoff

**Operation Type**: [issue|pr|kanban|release]
**Action**: [create|update|close|merge|sync|etc.]
**Target**: [repo, issue number, PR number, project ID]

### Details
- Specific operation parameters
- Any linked references

### Expected Outcome
- What success looks like
- Verification criteria
```

### For EAA (Architect) Design-GitHub Handoffs

```markdown
## Design-GitHub Link Handoff

**Design UUID**: [uuid]
**Design Path**: [path to design doc]
**GitHub Target**: [issue/card number or ID]

### Link Context
- Why this link exists
- What the GitHub item represents in the design

### Expected Outcome
- Design doc updated with GitHub reference
- GitHub item updated with design reference
```

### For EOA (Orchestrator) Module-GitHub Handoffs

```markdown
## Module-GitHub Handoff

**Module UUID**: [uuid]
**Design Reference**: [design UUID]
**GitHub Target**: [issue/card number or ID]

### Implementation Context
- Module's role in overall implementation
- Dependencies on other modules

### Task Details
- Specific implementation task
- Acceptance criteria
```

## UUID Tracking Across GitHub Operations

### UUID Reference Format in GitHub

When creating GitHub items linked to designs/modules, include UUID reference:

**In Issue Body**:
```markdown
<!-- EAMA-LINK: design-uuid=abc123 -->
<!-- EAMA-LINK: module-uuid=def456 -->
```

**In PR Description**:
```markdown
## Related Design
Design UUID: `abc123` (path: `design/feature-x/DESIGN.md`)

## Implementing Modules
- Module UUID: `def456` (component-a)
- Module UUID: `ghi789` (component-b)
```

**In Kanban Card Notes**:
```
DESIGN: abc123
MODULE: def456
```

### Searching by UUID

EAMA can find GitHub items by UUID using:
```bash
gh issue list --search "EAMA-LINK: design-uuid=abc123"
gh pr list --search "Design UUID: abc123"
```

## Error Handling

### Ambiguous Routing

If operation could go to multiple agents:
1. Default to EIA (most GitHub operations)
2. Ask user for clarification if design/module context unclear
3. Log routing decision for audit

### Missing Context

If handoff lacks required information:
1. Query user for missing details
2. Search locally (design search) before asking
3. Include "INCOMPLETE" flag in handoff for receiving agent

### Agent Unavailable

If target agent is not responding:
1. Queue the handoff
2. Notify user of delay
3. Retry after configured interval
4. Escalate to user if repeated failures

## Examples

### Example 1: Routing a Bug Report Issue to EIA

```
# User request
"Create an issue for the login timeout bug"

# EAMA decision process
1. Operation type: ISSUE
2. Is linked to design doc? NO
3. Is module implementation task? NO
4. Route to: EIA

# Handoff content
## GitHub Operation Handoff

**Operation Type**: issue
**Action**: create
**Target**: main repo

### Details
- Title: Login timeout bug
- Labels: bug, high-priority
- Body: Users experiencing timeout after 30 seconds

### Expected Outcome
- Issue created with appropriate labels
- Issue number returned
```

### Example 2: Routing a Design-Linked Card to EAA

```
# User request
"Create a kanban card for the authentication design"

# EAMA decision process
1. Operation type: KANBAN
2. Is item design or module? DESIGN
3. Route to: EAA

# Handoff includes design UUID for linking
```

## Resources

- [Role Routing SKILL](../eama-role-routing/SKILL.md)
- [Proactive Handoff Protocol](../eama-shared/references/proactive-handoff-protocol.md)
- [Handoff Template](../../shared/handoff_template.md)
