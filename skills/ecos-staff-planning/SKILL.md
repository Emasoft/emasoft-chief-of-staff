---
name: ecos-staff-planning
description: Use when analyzing staffing needs, assessing role requirements, planning agent capacity, or creating staffing templates for multi-agent orchestration. Trigger with team sizing or staffing requests.
license: Apache-2.0
compatibility: Requires access to agent registry, project configuration files, and understanding of agent capabilities and workload patterns. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ecos-main
---

# Emasoft Chief of Staff - Staff Planning Skill

## Overview

Staff planning is a core responsibility of the Chief of Staff agent. It involves analyzing project requirements, assessing available agent capabilities, planning capacity allocation, and creating staffing templates that ensure efficient multi-agent orchestration. This skill teaches you how to perform comprehensive staffing analysis and planning.

## Prerequisites

Before using this skill, ensure:
1. Task requirements are defined
2. Available agent pool is known
3. Resource limits are understood

## Instructions

1. Analyze task requirements
2. Determine required agent count and types
3. Check resource availability
4. Recommend team composition

## Output

| Analysis Type | Output |
|---------------|--------|
| Task analysis | Required skills, estimated effort |
| Team sizing | Recommended agent count by role |
| Resource check | Availability vs requirements |

## What Is Staff Planning?

Staff planning is the process of determining which agents are needed, when they are needed, and how they should be allocated across projects and tasks. Unlike simple task assignment, staff planning considers:

- **Agent capabilities**: What each agent type can do
- **Workload patterns**: When agents are busy vs available
- **Project dependencies**: Which tasks must complete before others can start
- **Resource constraints**: Context limits, API quotas, concurrent execution limits

## Staff Planning Components

### 1. Role Assessment

Evaluating what agent roles are required for a project or task set:
- Identifying required capabilities (coding, testing, documentation, etc.)
- Matching capabilities to available agent types
- Determining specialization depth needed
- Assessing multi-role requirements

### 2. Capacity Planning

Determining how much work agents can handle:
- Estimating task durations
- Calculating parallel execution limits
- Planning for context window constraints
- Scheduling around blocking operations

### 3. Staffing Templates

Reusable configurations for common scenarios:
- Project bootstrap templates
- Feature development templates
- Bug triage templates
- Release preparation templates

## Core Procedures

### PROCEDURE 1: Assess Role Requirements

**When to use:** At project start, when adding new features, or when task patterns change.

**Steps:** Analyze project requirements, list required capabilities, map to agent types, identify gaps.

**Related documentation:**

#### Role Assessment ([references/role-assessment.md](references/role-assessment.md))
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

### PROCEDURE 2: Plan Agent Capacity

**When to use:** When scheduling work, handling resource conflicts, or optimizing throughput.

**Steps:** Inventory available agents, estimate task requirements, calculate allocation, identify bottlenecks.

**Related documentation:**

#### Capacity Planning ([references/capacity-planning.md](references/capacity-planning.md))
- 2.1 What is capacity planning - Understanding capacity constraints
- 2.2 Capacity metrics - Measuring agent capacity
  - 2.2.1 Context window utilization - Token budget tracking
  - 2.2.2 Concurrent execution limits - Parallel task boundaries
  - 2.2.3 Blocking operation impact - Synchronous wait times
- 2.3 Capacity planning procedure - Step-by-step planning
  - 2.3.1 Agent inventory - Listing available agents
  - 2.3.2 Task estimation - Sizing work items
  - 2.3.3 Allocation calculation - Assigning agents to tasks
  - 2.3.4 Bottleneck identification - Finding constraints
- 2.4 Load balancing strategies - Distributing work evenly
- 2.5 Scaling decisions - When to add more agents
- 2.6 Examples - Capacity planning scenarios
- 2.7 Troubleshooting - Capacity planning issues

### PROCEDURE 3: Create Staffing Templates

**When to use:** When establishing repeatable staffing patterns or standardizing team compositions.

**Steps:** Identify common scenario, list required roles, define agent assignments, document template.

**Related documentation:**

#### Staffing Templates ([references/staffing-templates.md](references/staffing-templates.md))
- 3.1 What are staffing templates - Reusable staffing configurations
- 3.2 Template structure - Standard template format
  - 3.2.1 Metadata section - Template identification
  - 3.2.2 Roles section - Required agent types
  - 3.2.3 Assignments section - Default agent allocations
  - 3.2.4 Constraints section - Scheduling limitations
- 3.3 Built-in templates - Standard templates included
  - 3.3.1 Project bootstrap template - New project setup
  - 3.3.2 Feature development template - Feature implementation
  - 3.3.3 Bug triage template - Issue investigation
  - 3.3.4 Release preparation template - Release workflow
- 3.4 Creating custom templates - Building new templates
- 3.5 Template validation - Ensuring template correctness
- 3.6 Examples - Template usage scenarios
- 3.7 Troubleshooting - Template issues

## Task Checklist

Copy this checklist and track your progress:

- [ ] Understand staff planning purpose and components
- [ ] Learn PROCEDURE 1: Assess role requirements
- [ ] Learn PROCEDURE 2: Plan agent capacity
- [ ] Learn PROCEDURE 3: Create staffing templates
- [ ] Practice role assessment for a sample project
- [ ] Practice capacity planning with constraints
- [ ] Create a custom staffing template
- [ ] Validate templates work correctly

## Examples

### Example 1: Role Assessment for Feature Development

```markdown
## Role Assessment: User Authentication Feature

### Required Capabilities
1. Python backend development
2. API design and implementation
3. Security best practices
4. Unit test creation
5. Integration test creation
6. Documentation writing

### Agent Type Mapping
| Capability | Agent Type | Priority |
|------------|------------|----------|
| Backend development | code-implementer | HIGH |
| API design | architect-agent | HIGH |
| Security practices | security-reviewer | MEDIUM |
| Unit tests | test-engineer | HIGH |
| Integration tests | test-engineer | MEDIUM |
| Documentation | doc-writer | LOW |

### Gap Analysis
- No security-reviewer agent available
- Mitigation: code-implementer will follow security checklist
```

### Example 2: Capacity Planning

```markdown
## Capacity Plan: Sprint 42

### Available Agents
- code-implementer: 2 instances
- test-engineer: 1 instance
- doc-writer: 1 instance

### Task Allocation
| Task | Agent | Duration | Parallel |
|------|-------|----------|----------|
| Auth module | code-impl-1 | 4h | Yes |
| User profile | code-impl-2 | 3h | Yes |
| Auth tests | test-eng | 2h | After auth |
| API docs | doc-writer | 1h | After auth |

### Bottleneck
- test-engineer is single instance
- All test tasks must serialize through it
```

## Error Handling

### Issue: Not enough agents for required roles

**Symptoms:** Role assessment shows gaps, tasks remain unassigned.

See [references/role-assessment.md](references/role-assessment.md) Section 1.7 Troubleshooting for resolution.

### Issue: Agent capacity exceeded

**Symptoms:** Tasks queue indefinitely, context windows exhausted.

See [references/capacity-planning.md](references/capacity-planning.md) Section 2.7 Troubleshooting for resolution.

### Issue: Template does not fit project needs

**Symptoms:** Template roles do not match requirements, assignments incorrect.

See [references/staffing-templates.md](references/staffing-templates.md) Section 3.7 Troubleshooting for resolution.

## Key Takeaways

1. **Role assessment precedes staffing** - Know what you need before allocating
2. **Capacity planning prevents overload** - Plan around constraints
3. **Templates accelerate setup** - Reuse proven patterns
4. **Gaps require mitigation** - Document workarounds for missing roles
5. **Bottlenecks need attention** - Single-instance agents create serialization

## Next Steps

### 1. Read Role Assessment
See [references/role-assessment.md](references/role-assessment.md) for complete role analysis procedures.

### 2. Read Capacity Planning
See [references/capacity-planning.md](references/capacity-planning.md) for capacity calculation methods.

### 3. Read Staffing Templates
See [references/staffing-templates.md](references/staffing-templates.md) for template creation and usage.

---

## Resources

- [Role Assessment](references/role-assessment.md)
- [Capacity Planning](references/capacity-planning.md)
- [Staffing Templates](references/staffing-templates.md)

---

**Version:** 1.0
**Last Updated:** 2025-02-01
**Target Audience:** Chief of Staff Agents
**Difficulty Level:** Intermediate
