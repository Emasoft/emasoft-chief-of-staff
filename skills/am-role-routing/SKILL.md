---
name: am-role-routing
description: Decision logic for routing user requests to appropriate specialist roles
triggers:
  - User submits a new request or task
  - Assistant Manager needs to delegate work
  - Handoff between roles is required
---

# Role Routing Skill

## Purpose

This skill provides the Assistant Manager with decision logic for routing user requests to the appropriate specialist role (Architect, Orchestrator, or Integrator).

## Routing Decision Matrix

| User Intent Pattern | Route To | Handoff Type |
|---------------------|----------|--------------|
| "design", "plan", "architect", "spec", "requirements" | ARCHITECT | task_assignment |
| "build", "implement", "create", "develop", "code" | ORCHESTRATOR | task_assignment |
| "review", "test", "merge", "release", "deploy", "quality" | INTEGRATOR | task_assignment |
| "status", "progress", "update" | Handle directly | none |
| "approve", "reject", "confirm" | Handle directly | approval_response |

## Detailed Routing Rules

### Route to ARCHITECT when:

1. **New project/feature design needed**
   - User says: "Design a...", "Plan how to...", "Create architecture for..."
   - Action: Create handoff with requirements, route to architect

2. **Requirements analysis required**
   - User says: "What do we need for...", "Analyze requirements for..."
   - Action: Create handoff with context, route to architect

3. **Technical specification needed**
   - User says: "Spec out...", "Document how...", "Define the API for..."
   - Action: Create handoff, route to architect

4. **Module planning required**
   - User says: "Break down...", "Modularize...", "Plan implementation of..."
   - Action: Create handoff, route to architect

### Route to ORCHESTRATOR when:

1. **Implementation ready to start**
   - Condition: Approved design/plan exists
   - Action: Create handoff with design docs, route to orchestrator

2. **Task coordination needed**
   - User says: "Build...", "Implement...", "Start development..."
   - Action: Create handoff with requirements, route to orchestrator

3. **Multi-agent work coordination**
   - Condition: Work requires multiple parallel agents
   - Action: Create handoff with task breakdown, route to orchestrator

4. **Progress monitoring required**
   - Condition: Orchestration in progress, need intervention
   - Action: Forward message to orchestrator

### Route to INTEGRATOR when:

1. **Work ready for integration**
   - Condition: Orchestrator signals completion
   - Action: Create handoff with completion report, route to integrator

2. **Code review requested**
   - User says: "Review...", "Check the PR...", "Evaluate changes..."
   - Action: Create handoff with PR details, route to integrator

3. **Quality gates needed**
   - User says: "Test...", "Validate...", "Run quality checks..."
   - Action: Create handoff, route to integrator

4. **Release preparation**
   - User says: "Prepare release...", "Merge...", "Deploy..."
   - Action: Create handoff, route to integrator

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
USER <-> ASSISTANT-MANAGER <-> ARCHITECT
                           <-> ORCHESTRATOR
                           <-> INTEGRATOR
```

**CRITICAL**: Architect, Orchestrator, and Integrator do NOT communicate directly with each other. All communication flows through Assistant Manager.

## Handoff Protocol

### Step 1: Identify Intent
```
Parse user message -> Identify primary intent -> Match to routing rule
```

### Step 2: Create Handoff Document
```
Generate UUID -> Create handoff-{uuid}-am-to-{role}.md -> Save to docs_dev/handoffs/
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
- handoff-a1b2c3d4-am-to-arch.md
- handoff-e5f6g7h8-arch-to-am.md
- handoff-i9j0k1l2-am-to-orch.md
```

## Storage Location

All handoff files are stored in: `docs_dev/handoffs/`

## References

- [Handoff Template](../../shared/handoff_template.md)
- [Message Templates](../../shared/message_templates.md)
