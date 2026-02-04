# Role Assessment Reference

## Table of Contents

- 1.1 What is role assessment - Understanding role requirements analysis
- 1.2 When to perform assessment - Triggers for role evaluation
- 1.3 Assessment procedure - Step-by-step role analysis
  - 1.3.1 Capability extraction - Identifying required skills
  - 1.3.2 Agent type mapping - Matching skills to agent types
  - 1.3.3 Gap analysis - Finding missing capabilities
  - 1.3.4 Priority ordering - Ranking requirements by importance
- 1.4 Assessment output format - Structured assessment results
- 1.5 Validation checklist - Verifying assessment completeness
- 1.6 Examples - Role assessment scenarios
- 1.7 Troubleshooting - Common assessment issues

---

## 1.1 What is role assessment

Role assessment is the systematic analysis of project requirements to determine which agent roles are needed to complete the work. It involves:

1. Extracting capabilities from project requirements
2. Mapping capabilities to available agent types
3. Identifying gaps where no suitable agent exists
4. Prioritizing requirements by importance and urgency

Role assessment answers the question: "What agents do I need to complete this project?"

---

## 1.2 When to perform assessment

Perform role assessment when:

| Trigger | Description |
|---------|-------------|
| Project start | New project requires initial staffing |
| Feature addition | New features may need new capabilities |
| Task pattern change | Shift in work type requires different agents |
| Agent unavailability | Need to find replacements |
| Performance issues | Current agents not meeting needs |

---

## 1.3 Assessment procedure

### 1.3.1 Capability extraction

**Purpose:** Identify all skills and capabilities required by the project.

**Steps:**
1. Read project requirements document
2. List all technical skills mentioned
3. Identify implicit skills (testing, documentation, etc.)
4. Note domain-specific requirements
5. Record any tool or framework requirements

**Output:** List of required capabilities with descriptions.

### 1.3.2 Agent type mapping

**Purpose:** Match required capabilities to available agent types.

**Steps:**
1. Load agent registry with available agent types
2. For each capability, find matching agent types
3. Record primary and secondary matches
4. Note capabilities with multiple matching agents
5. Flag capabilities with no matching agent

**Agent Type Reference:**

| Agent Type | Primary Capabilities |
|------------|---------------------|
| code-implementer | Python, JavaScript, Go, Rust development |
| test-engineer | Unit tests, integration tests, E2E tests |
| doc-writer | Documentation, README, API docs |
| architect-agent | System design, API design, architecture |
| security-reviewer | Security audit, vulnerability assessment |
| devops-expert | CI/CD, deployment, infrastructure |

### 1.3.3 Gap analysis

**Purpose:** Identify capabilities that cannot be fulfilled by available agents.

**Steps:**
1. List capabilities with no agent match
2. For each gap, determine severity (blocking, degraded, optional)
3. Identify potential mitigations:
   - Can another agent partially cover?
   - Can we use a checklist instead?
   - Must we spawn a specialized agent?
4. Document mitigation strategy for each gap

### 1.3.4 Priority ordering

**Purpose:** Rank requirements by importance for staffing decisions.

**Priority Levels:**
- **CRITICAL:** Project cannot proceed without this capability
- **HIGH:** Major functionality depends on this capability
- **MEDIUM:** Important but workarounds exist
- **LOW:** Nice to have, can be deferred

**Steps:**
1. Assign priority to each capability
2. Group capabilities by priority
3. Identify critical path (capabilities that must complete first)
4. Note dependencies between capabilities

---

## 1.4 Assessment output format

```markdown
# Role Assessment: [Project Name]
Date: [YYYY-MM-DD]
Assessor: [Agent ID]

## Required Capabilities

| ID | Capability | Description | Priority |
|----|------------|-------------|----------|
| C1 | [name] | [description] | [CRITICAL/HIGH/MEDIUM/LOW] |

## Agent Type Mapping

| Capability ID | Primary Agent | Secondary Agent | Notes |
|---------------|---------------|-----------------|-------|
| C1 | [agent-type] | [agent-type] | [notes] |

## Gap Analysis

| Capability ID | Gap Type | Severity | Mitigation |
|---------------|----------|----------|------------|
| C1 | [no-agent/partial] | [blocking/degraded/optional] | [strategy] |

## Staffing Recommendation

| Agent Type | Count | Assigned Capabilities | Priority |
|------------|-------|----------------------|----------|
| [type] | [n] | C1, C2 | [priority] |

## Notes
[Additional considerations]
```

---

## 1.5 Validation checklist

Before finalizing assessment:

- [ ] All project requirements reviewed
- [ ] All capabilities extracted with descriptions
- [ ] Each capability mapped to at least one agent type
- [ ] Gaps identified and severity assigned
- [ ] Mitigation strategy documented for each gap
- [ ] Priorities assigned to all capabilities
- [ ] Dependencies between capabilities noted
- [ ] Staffing recommendation complete

---

## 1.6 Examples

### Example: Web Application Feature

**Project:** Add user authentication to web app

**Capability Extraction:**
- Backend API development (Python/FastAPI)
- JWT token handling
- Password hashing
- Unit test creation
- API documentation
- Security review

**Agent Mapping:**
| Capability | Primary Agent | Notes |
|------------|---------------|-------|
| Backend API | code-implementer | Python expertise |
| JWT handling | code-implementer | Security knowledge |
| Password hashing | code-implementer | Use bcrypt |
| Unit tests | test-engineer | pytest |
| API docs | doc-writer | OpenAPI spec |
| Security review | security-reviewer | OWASP checklist |

**Gap:** No security-reviewer available

**Mitigation:** code-implementer follows OWASP checklist; manual review later.

---

## 1.7 Troubleshooting

### Issue: Cannot determine required capabilities

**Symptoms:** Requirements unclear, many assumptions needed.

**Resolution:**
1. Request clarification from user
2. Start with high-level capabilities
3. Refine as project progresses
4. Document assumptions explicitly

### Issue: Multiple agents match same capability

**Symptoms:** Unclear which agent to assign.

**Resolution:**
1. Check agent availability
2. Consider agent workload
3. Prefer specialist over generalist
4. Document selection rationale

### Issue: Critical capability has no matching agent

**Symptoms:** Blocking gap identified.

**Resolution:**
1. Check if capability can be decomposed
2. Look for partial matches
3. Consider human intervention
4. Escalate to user for decision
