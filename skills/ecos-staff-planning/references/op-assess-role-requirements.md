---
operation: assess-role-requirements
procedure: proc-evaluate-project
workflow-instruction: Step 2 - Chief of Staff Evaluates Project
parent-skill: ecos-staff-planning
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Assess Role Requirements


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Extract Capabilities from Requirements](#step-1-extract-capabilities-from-requirements)
  - [Step 2: Map Capabilities to Agent Types](#step-2-map-capabilities-to-agent-types)
  - [Step 3: Perform Gap Analysis](#step-3-perform-gap-analysis)
  - [Step 4: Assign Priorities](#step-4-assign-priorities)
  - [Step 5: Create Staffing Recommendation](#step-5-create-staffing-recommendation)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Web Authentication Feature](#example-web-authentication-feature)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)
- [Detailed Reference](#detailed-reference)

## When to Use

Perform this operation when:
- Starting a new project that needs staffing decisions
- Adding new features that may require different agent capabilities
- Task patterns change and current agents may not match needs
- An agent becomes unavailable and replacements are needed
- Performance issues suggest current agents are not meeting needs

## Prerequisites

- Project requirements document or task description available
- Access to agent registry with available agent types
- Understanding of project scope and complexity

## Procedure

### Step 1: Extract Capabilities from Requirements

Read the project requirements and identify all required skills:

1. Read the project requirements document or task description
2. List all technical skills explicitly mentioned
3. Identify implicit skills (testing, documentation, deployment)
4. Note domain-specific requirements (security, performance, compliance)
5. Record any tool or framework requirements

**Output:** A list of required capabilities with descriptions.

### Step 2: Map Capabilities to Agent Types

Match each capability to available agent types:

1. Load the agent registry to see available agent types
2. For each capability, find the primary matching agent type
3. Identify secondary matches (agents that can partially cover)
4. Note capabilities with multiple matching agents
5. Flag capabilities with no matching agent (these are gaps)

**Agent Type Reference:**

| Agent Type | Primary Capabilities |
|------------|---------------------|
| code-implementer | Python, JavaScript, Go, Rust development |
| test-engineer | Unit tests, integration tests, E2E tests |
| doc-writer | Documentation, README, API docs |
| architect-agent | System design, API design, architecture |
| security-reviewer | Security audit, vulnerability assessment |
| devops-expert | CI/CD, deployment, infrastructure |

### Step 3: Perform Gap Analysis

Identify capabilities that cannot be fulfilled:

1. List all capabilities with no agent match
2. For each gap, determine severity:
   - **Blocking:** Project cannot proceed without this
   - **Degraded:** Project can proceed with reduced quality
   - **Optional:** Nice to have, not required
3. Identify potential mitigations for each gap:
   - Can another agent partially cover this capability?
   - Can we use a checklist or manual process instead?
   - Must we request a specialized agent be spawned?
4. Document the mitigation strategy for each gap

### Step 4: Assign Priorities

Rank capabilities by importance:

1. Assign priority to each capability:
   - **CRITICAL:** Project cannot proceed without this
   - **HIGH:** Major functionality depends on this
   - **MEDIUM:** Important but workarounds exist
   - **LOW:** Nice to have, can be deferred
2. Group capabilities by priority level
3. Identify the critical path (capabilities that must complete first)
4. Note dependencies between capabilities

### Step 5: Create Staffing Recommendation

Generate the final assessment output:

1. Compile the capability list with priorities
2. Include the agent type mapping for each capability
3. Document all gaps and their mitigations
4. Recommend agent types and counts needed
5. Note any assumptions or constraints

## Checklist

Copy this checklist and track your progress:

- [ ] Read project requirements document
- [ ] Extract all technical skills required
- [ ] Identify implicit skills (testing, docs, etc.)
- [ ] Load agent registry with available types
- [ ] Map each capability to primary agent type
- [ ] Identify secondary agent type matches
- [ ] Flag capabilities with no matching agent
- [ ] Determine severity of each gap
- [ ] Document mitigation for each gap
- [ ] Assign priority to each capability
- [ ] Identify critical path dependencies
- [ ] Create staffing recommendation document

## Examples

### Example: Web Authentication Feature

**Scenario:** Assess roles needed for user authentication feature.

**Step 1 Output - Capability Extraction:**
```
Required Capabilities:
1. Backend API development (Python/FastAPI)
2. JWT token handling
3. Password hashing (bcrypt)
4. Unit test creation (pytest)
5. Integration test creation
6. API documentation (OpenAPI)
7. Security review (OWASP compliance)
```

**Step 2 Output - Agent Mapping:**
```
| Capability | Primary Agent | Secondary Agent |
|------------|---------------|-----------------|
| Backend API | code-implementer | - |
| JWT handling | code-implementer | - |
| Password hashing | code-implementer | - |
| Unit tests | test-engineer | code-implementer |
| Integration tests | test-engineer | - |
| API docs | doc-writer | code-implementer |
| Security review | security-reviewer | - |
```

**Step 3 Output - Gap Analysis:**
```
Gap: security-reviewer not available
Severity: DEGRADED
Mitigation: code-implementer follows OWASP checklist; manual review later
```

**Step 4 Output - Priorities:**
```
CRITICAL: Backend API, JWT handling, Password hashing
HIGH: Unit tests, Integration tests
MEDIUM: Security review
LOW: API docs
```

**Step 5 Output - Recommendation:**
```
Recommended Staffing:
- 1x code-implementer (primary development)
- 1x test-engineer (testing)
- 1x doc-writer (optional, can defer)

Gap Mitigation:
- Security review: Use OWASP checklist, schedule manual review
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Cannot determine required capabilities | Requirements unclear | Request clarification from user; document assumptions |
| Multiple agents match same capability | Unclear which to assign | Check availability, prefer specialist over generalist |
| Critical capability has no matching agent | Blocking gap identified | Decompose capability; check partial matches; escalate to user |
| Agent registry unavailable | System issue | Use cached registry; report issue to orchestrator |

## Related Operations

- [op-plan-agent-capacity.md](op-plan-agent-capacity.md) - After assessing roles, plan capacity allocation
- [op-create-staffing-templates.md](op-create-staffing-templates.md) - Create reusable patterns from assessments

## Detailed Reference

For comprehensive details on role assessment methodology, see [role-assessment.md](role-assessment.md).
