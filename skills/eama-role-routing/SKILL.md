---
name: eama-role-routing
description: Decision logic for routing user requests to appropriate specialist roles
triggers:
  - User submits a new request or task
  - Assistant Manager needs to delegate work
  - Handoff between roles is required
---

# Role Routing Skill

## Purpose

This skill provides the Assistant Manager (EAMA) with decision logic for routing user requests to the appropriate specialist role:
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

## References

- [Handoff Template](../../shared/handoff_template.md)
- [Message Templates](../../shared/message_templates.md)
