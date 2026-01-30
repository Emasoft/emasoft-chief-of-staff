---
name: eama-role-routing
description: Use when routing user requests to appropriate specialist roles (Architect, Orchestrator, or Integrator)
context: fork
triggers:
  - User submits a new request or task
  - Assistant Manager needs to delegate work
  - Handoff between roles is required
---

# Role Routing Skill

## Overview

This skill provides the Assistant Manager (EAMA) with decision logic for routing user requests to the appropriate specialist role:

## Prerequisites

- AI Maestro messaging system must be running
- All specialist agents (EAA, EOA, EIA) must be registered
- `docs_dev/handoffs/` directory must exist and be writable
- UUID generation capability required

## Instructions

1. Parse user message to identify primary intent
2. Match intent to routing rule using the decision matrix
3. If handling directly (status, approval, clarification), respond immediately
4. If routing to specialist, create handoff document with UUID
5. Save handoff to `docs_dev/handoffs/`
6. Send via AI Maestro to target role
7. Track handoff status and monitor for acknowledgment
8. Report routing decision to user
- **EAA** - Architect Agent
- **EOA** - Orchestrator Agent
- **EIA** - Integrator Agent

## Plugin Prefix Reference

| Role | Prefix | Plugin Name |
|------|--------|-------------|
| Assistant Manager | `eama-` | Emasoft Assistant Manager Agent |
| Architect | `eaa-` | Emasoft Architect Agent |
| Orchestrator | `eoa-` | Emasoft Orchestrator Agent |
| Integrator | `eia-` | Emasoft Integrator Agent |

## Routing Decision Matrix

| User Intent Pattern | Route To | Handoff Type |
|---------------------|----------|--------------|
| "design", "plan", "architect", "spec", "requirements" | EAA (Architect) | task_assignment |
| "build", "implement", "create", "develop", "code" | EOA (Orchestrator) | task_assignment |
| "review", "test", "merge", "release", "deploy", "quality" | EIA (Integrator) | task_assignment |
| "status", "progress", "update" | Handle directly | none |
| "approve", "reject", "confirm" | Handle directly | approval_response |

## Detailed Routing Rules

### Route to EAA (Architect) when:

1. **New project/feature design needed**
   - User says: "Design a...", "Plan how to...", "Create architecture for..."
   - Action: Create handoff with requirements, route to eaa

2. **Requirements analysis required**
   - User says: "What do we need for...", "Analyze requirements for..."
   - Action: Create handoff with context, route to eaa

3. **Technical specification needed**
   - User says: "Spec out...", "Document how...", "Define the API for..."
   - Action: Create handoff, route to eaa

4. **Module planning required**
   - User says: "Break down...", "Modularize...", "Plan implementation of..."
   - Action: Create handoff, route to eaa

### Route to EOA (Orchestrator) when:

1. **Implementation ready to start**
   - Condition: Approved design/plan exists
   - Action: Create handoff with design docs, route to eoa

2. **Task coordination needed**
   - User says: "Build...", "Implement...", "Start development..."
   - Action: Create handoff with requirements, route to eoa

3. **Multi-agent work coordination**
   - Condition: Work requires multiple parallel agents
   - Action: Create handoff with task breakdown, route to eoa

4. **Progress monitoring required**
   - Condition: Orchestration in progress, need intervention
   - Action: Forward message to eoa

### Route to EIA (Integrator) when:

1. **Work ready for integration**
   - Condition: Orchestrator signals completion
   - Action: Create handoff with completion report, route to eia

2. **Code review requested**
   - User says: "Review...", "Check the PR...", "Evaluate changes..."
   - Action: Create handoff with PR details, route to eia

3. **Quality gates needed**
   - User says: "Test...", "Validate...", "Run quality checks..."
   - Action: Create handoff, route to eia

4. **Release preparation**
   - User says: "Prepare release...", "Merge...", "Deploy..."
   - Action: Create handoff, route to eia

### Handle Directly (no routing):

1. **Status requests**
   - User says: "What's the status?", "How's progress?"
   - Action: Query relevant role, compile report, present to user

2. **Approval decisions**
   - User says: "Yes, approve", "No, reject", "Proceed with..."
   - Action: Record decision, forward to requesting role

3. **Clarification requests**
   - User says: "Explain...", "What does X mean?"
   - Action: Answer directly or query relevant role

4. **Configuration/settings**
   - User says: "Set...", "Configure...", "Enable..."
   - Action: Handle directly

## Communication Hierarchy

```
USER <-> EAMA (Assistant Manager) <-> EAA (Architect)
                                  <-> EOA (Orchestrator)
                                  <-> EIA (Integrator)
```

**CRITICAL**: EAA, EOA, and EIA do NOT communicate directly with each other. All communication flows through EAMA.

## Handoff Protocol

### Step 1: Identify Intent
```
Parse user message -> Identify primary intent -> Match to routing rule
```

### Step 2: Create Handoff Document
```
Generate UUID -> Create handoff-{uuid}-eama-to-{role}.md -> Save to docs_dev/handoffs/
```

### Step 3: Send via AI Maestro
```
Compose message -> Set appropriate priority -> Send to role session
```

### Step 4: Track Handoff
```
Log handoff in state -> Set status to "pending" -> Monitor for acknowledgment
```

### Step 5: Report to User
```
Confirm routing -> Provide tracking info -> Set expectation for response
```

## File Naming Convention

```
handoff-{uuid}-{from}-to-{to}.md

Examples:
- handoff-a1b2c3d4-eama-to-eaa.md    # AM assigns to Architect
- handoff-e5f6g7h8-eaa-to-eama.md    # Architect reports to AM
- handoff-i9j0k1l2-eama-to-eoa.md    # AM assigns to Orchestrator
- handoff-m3n4o5p6-eoa-to-eama.md    # Orchestrator reports to AM
- handoff-q7r8s9t0-eama-to-eia.md    # AM assigns to Integrator
```

## Storage Location

All handoff files are stored in: `docs_dev/handoffs/`

## GitHub Operations Routing

### Route to EIA (Integrator) for:

| Operation | User Intent Pattern | Handoff Content |
|-----------|---------------------|-----------------|
| Issue creation | "create issue", "open bug", "file ticket" | Issue title, body, labels |
| Issue update | "update issue", "change status", "add label" | Issue number, changes |
| PR operations | "create PR", "merge PR", "review PR" | PR details, branch info |
| Kanban sync | "sync kanban", "update board", "move card" | Project ID, item updates |
| Release management | "release", "tag version", "publish" | Version, changelog |

### Route to EAA (Architect) for:

| Operation | User Intent Pattern | Handoff Content |
|-----------|---------------------|-----------------|
| Issue-to-design linking | "link issue to design", "connect to spec" | Issue number, design UUID |
| Design from issue | "design for issue #X", "spec from requirement" | Issue number, scope |

### Route to EOA (Orchestrator) for:

| Operation | User Intent Pattern | Handoff Content |
|-----------|---------------------|-----------------|
| Module issues | "module implementation issue", "task tracking" | Module UUID, task breakdown |
| Implementation issues | "development issue", "coding task" | Design UUID, module list |

**Cross-reference**: See [eama-github-routing SKILL](../eama-github-routing/SKILL.md) for complete GitHub decision trees.

## Design Document Routing

### Handle Locally (EAMA):

| Operation | Tool | Details |
|-----------|------|---------|
| Search designs by UUID | `eama_design_search.py --uuid` | Returns matching design docs |
| Search designs by keyword | `eama_design_search.py --keyword` | Full-text search in design/* |
| Search designs by status | `eama_design_search.py --status` | Filter by draft/approved/deprecated |
| List all designs | `eama_design_search.py --list` | Catalog of all design documents |

### Route to EAA (Architect) for:

| Operation | User Intent Pattern | Handoff Content |
|-----------|---------------------|-----------------|
| Create new design | "design", "create spec", "architect solution" | Requirements, constraints |
| Update design | "modify design", "update spec", "revise architecture" | Design UUID, changes |
| Review design | "review design", "validate architecture" | Design UUID, review criteria |

### Search Before Route Decision Tree

```
User mentions design/spec/architecture
          │
          ▼
    ┌─────────────────┐
    │ Does user give  │
    │ UUID or path?   │
    └────────┬────────┘
             │
     ┌───────┴───────┐
     │ YES           │ NO
     ▼               ▼
┌────────────┐  ┌─────────────────┐
│ Search by  │  │ Search by       │
│ UUID/path  │  │ keyword/context │
└─────┬──────┘  └────────┬────────┘
      │                  │
      ▼                  ▼
┌───────────────────────────────────┐
│   Design found?                   │
└────────────────┬──────────────────┘
         ┌───────┴───────┐
         │ YES           │ NO
         ▼               ▼
┌────────────────┐  ┌─────────────────┐
│ Include design │  │ Route to EAA to │
│ context in     │  │ create new      │
│ routing        │  │ design          │
└────────────────┘  └─────────────────┘
```

## Module Orchestration Routing

### Route to EOA (Orchestrator) for:

| Operation | User Intent Pattern | Handoff Content |
|-----------|---------------------|-----------------|
| Start module implementation | "implement module", "build component" | Module UUID from design |
| Coordinate parallel work | "parallelize", "split tasks" | Task breakdown, dependencies |
| Resume orchestration | "continue building", "resume work" | Orchestration state, progress |
| Replan modules | "reorganize tasks", "reprioritize" | Current state, new priorities |

### Orchestration Handoff Checklist

When routing to EOA, handoff MUST include:

1. **Design Reference**: UUID of approved design
2. **Module List**: Modules to implement (from design)
3. **Priority Order**: Which modules first
4. **Dependencies**: Inter-module dependencies
5. **Constraints**: Time, resources, technical limits
6. **Success Criteria**: What defines "done"

## Examples

### Example 1: Routing a Design Request to EAA

```
# User says: "Design a user authentication system"

# EAMA identifies intent: "design" -> Route to EAA

# Creates handoff
## Handoff: handoff-a1b2c3d4-eama-to-eaa.md

**From**: EAMA (Assistant Manager)
**To**: EAA (Architect)
**Type**: task_assignment

### Request
Design a user authentication system

### Requirements
- Support OAuth2 and password-based auth
- Include role-based access control
- Must integrate with existing user database

### Expected Deliverable
- Design document in design/auth-system/DESIGN.md
- Module breakdown with dependencies
```

### Example 2: Handling Status Request Directly

```
# User says: "What's the status of the project?"

# EAMA identifies intent: "status" -> Handle directly

# EAMA queries all roles, compiles report, presents to user
# No handoff created - direct response
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Ambiguous intent | Multiple possible routes | Ask user for clarification |
| Target agent unavailable | Session not running | Queue handoff, notify user, retry |
| Handoff directory missing | Not initialized | Create `docs_dev/handoffs/` automatically |
| UUID collision | Extremely rare | Generate new UUID and retry |

## Resources

- [Handoff Template](../../shared/handoff_template.md)
- [Message Templates](../../shared/message_templates.md)
- [GitHub Routing SKILL](../eama-github-routing/SKILL.md)
- [Proactive Handoff Protocol](../eama-shared/references/proactive-handoff-protocol.md)
