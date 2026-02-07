---
operation: create-staffing-templates
procedure: proc-evaluate-project
workflow-instruction: Step 2 - Chief of Staff Evaluates Project
parent-skill: ecos-staff-planning
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Create Staffing Templates

## When to Use

Perform this operation when:
- Establishing repeatable staffing patterns for common scenarios
- Standardizing team compositions across similar projects
- Documenting a successful staffing configuration for reuse
- Onboarding new projects with known staffing needs
- Optimizing setup time for recurring project types

## Prerequisites

- Experience with the scenario being templated (have done it at least once)
- Understanding of required roles and their responsibilities
- Knowledge of typical task assignments for the scenario
- Awareness of common constraints and dependencies

## Procedure

### Step 1: Identify the Scenario

Define what this template will be used for:

1. Name the scenario clearly (e.g., "feature-development", "bug-triage")
2. Write a one-sentence description of when to use this template
3. List the key characteristics that define this scenario
4. Identify how often this scenario occurs (frequent = high value template)
5. Note any variations of the scenario that might need separate templates

**Common Scenario Types:**
- Project bootstrap (new project setup)
- Feature development (implementing a feature)
- Bug triage (investigating and fixing bugs)
- Release preparation (preparing a release)
- Maintenance (ongoing support work)

### Step 2: Define Required Roles

List all roles needed for this scenario:

1. For each role, specify:
   - **Role name:** Descriptive name for the position
   - **Agent type:** Which agent type fills this role
   - **Count:** How many instances needed
   - **Required:** Is this role mandatory or optional?
   - **Description:** What this role does in the scenario

2. Consider both required and optional roles
3. Identify roles that can be combined if resources are limited

**Role Definition Format:**
```yaml
- name: "lead-developer"
  agent_type: "code-implementer"
  count: 1
  required: true
  description: "Leads implementation, makes architectural decisions"
```

### Step 3: Define Task Assignments

Map tasks to roles:

1. For each role, list the tasks it handles
2. Set priority for each assignment (high, medium, low)
3. Identify dependencies between assignments
4. Note any tasks that span multiple roles
5. Estimate typical duration for each task group

**Assignment Format:**
```yaml
- role: "lead-developer"
  tasks:
    - "Core feature implementation"
    - "Code review"
    - "Architecture decisions"
  priority: "high"
  depends_on: []
```

### Step 4: Define Constraints

Document limitations and requirements:

1. **Resource constraints:**
   - Maximum parallel agents allowed
   - Maximum context per agent
   - API rate limits to observe

2. **Tool requirements:**
   - Required tools that must be available
   - Configuration dependencies

3. **Scheduling constraints:**
   - Work hour limitations
   - Break requirements
   - Deadline pressure handling

**Constraints Format:**
```yaml
constraints:
  max_parallel_agents: 3
  max_context_per_agent: 80000
  required_tools:
    - "pytest"
    - "ruff"
  scheduling:
    work_hours: "continuous"
    breaks_required: false
```

### Step 5: Validate and Store Template

Ensure the template is correct and save it:

1. Check that all roles have valid agent types
2. Verify dependencies form an acyclic graph (no circular dependencies)
3. Confirm required roles are achievable with available agents
4. Test the template on a sample scenario if possible
5. Save the template in the templates directory

**Template Storage Location:**
```
design/templates/staffing/
├── project-bootstrap.yaml
├── feature-development.yaml
├── bug-triage.yaml
├── release-preparation.yaml
└── custom/
    └── my-new-template.yaml
```

## Checklist

Copy this checklist and track your progress:

- [ ] Identify the scenario this template covers
- [ ] Write clear scenario name and description
- [ ] List key characteristics of the scenario
- [ ] Define all required roles with agent types
- [ ] Define all optional roles with agent types
- [ ] Specify count needed for each role
- [ ] Write description for each role
- [ ] List tasks for each role
- [ ] Set priority for each task assignment
- [ ] Identify dependencies between assignments
- [ ] Define resource constraints
- [ ] List required tools
- [ ] Define scheduling constraints
- [ ] Validate all agent types exist
- [ ] Check for circular dependencies
- [ ] Save template to templates directory
- [ ] Document template in template index

## Examples

### Example: Creating a Code Review Template

**Scenario:** Create a template for code review workflow.

**Step 1 - Scenario Identification:**
```
Name: code-review
Description: Template for reviewing pull requests and ensuring code quality
Characteristics:
- Triggered by PR submission
- Requires code analysis skills
- Needs testing verification
- Produces review feedback
Frequency: Multiple times per day (high value template)
```

**Step 2 - Role Definition:**
```yaml
roles:
  - name: "reviewer"
    agent_type: "code-reviewer"
    count: 1
    required: true
    description: "Reviews code for quality, style, and correctness"

  - name: "test-verifier"
    agent_type: "test-engineer"
    count: 1
    required: true
    description: "Verifies tests pass and coverage is adequate"

  - name: "security-checker"
    agent_type: "security-reviewer"
    count: 1
    required: false
    description: "Checks for security vulnerabilities"
```

**Step 3 - Task Assignments:**
```yaml
assignments:
  - role: "reviewer"
    tasks:
      - "Code style check"
      - "Logic review"
      - "Architecture alignment check"
      - "Documentation review"
    priority: "high"

  - role: "test-verifier"
    tasks:
      - "Run test suite"
      - "Check coverage report"
      - "Verify new tests added"
    priority: "high"
    depends_on: ["reviewer"]

  - role: "security-checker"
    tasks:
      - "Dependency vulnerability scan"
      - "Code security patterns check"
    priority: "medium"
    depends_on: ["reviewer"]
```

**Step 4 - Constraints:**
```yaml
constraints:
  max_parallel_agents: 3
  max_context_per_agent: 50000
  required_tools:
    - "ruff"
    - "pytest"
    - "coverage"
  scheduling:
    work_hours: "continuous"
    timeout: "2 hours"
```

**Step 5 - Validation:**
```
Validation Results:
[PASS] All agent types exist in registry
[PASS] Dependency graph is acyclic
[PASS] Required roles have available agents
[PASS] Constraints are achievable

Template saved to: design/templates/staffing/code-review.yaml
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Template roles not matching available agents | Agent type does not exist | Check agent registry; substitute similar type |
| Dependency cycle in assignments | Circular wait condition | Draw dependency graph; break cycle by removing one dependency |
| Template too rigid for project | Does not fit actual needs | Use as starting point; modify as needed; create variant template |
| Template validation fails | Missing required fields | Check template against schema; fill in all required fields |

## Related Operations

- [op-assess-role-requirements.md](op-assess-role-requirements.md) - Role assessment informs template creation
- [op-plan-agent-capacity.md](op-plan-agent-capacity.md) - Capacity planning validates template feasibility

## Detailed Reference

For comprehensive details on staffing templates, see [staffing-templates.md](staffing-templates.md).

## Built-in Templates Reference

The following templates are pre-defined and available:

| Template | Use Case | Key Roles |
|----------|----------|-----------|
| project-bootstrap | New project setup | architect, implementer, documenter |
| feature-development | Feature implementation | developer, tester, reviewer |
| bug-triage | Bug investigation and fix | investigator, tester |
| release-preparation | Release workflow | release-manager, tester, documenter |

See [staffing-templates.md](staffing-templates.md) Section 3.3 for full details on each built-in template.
