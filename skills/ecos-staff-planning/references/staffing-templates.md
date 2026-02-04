# Staffing Templates Reference

## Table of Contents

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

---

## 3.1 What are staffing templates

Staffing templates are reusable configurations that define team compositions for common scenarios. They specify:

- Which agent roles are needed
- How many of each role
- Default task assignments
- Scheduling constraints

Templates accelerate project setup by providing proven staffing patterns.

---

## 3.2 Template structure

### 3.2.1 Metadata section

```yaml
metadata:
  name: "template-name"
  version: "1.0.0"
  description: "What this template is for"
  author: "Chief of Staff"
  created: "2025-02-01"
  tags: ["development", "feature", "sprint"]
```

### 3.2.2 Roles section

```yaml
roles:
  - name: "lead-developer"
    agent_type: "code-implementer"
    count: 1
    required: true
    description: "Leads implementation, makes architectural decisions"

  - name: "support-developer"
    agent_type: "code-implementer"
    count: 1
    required: false
    description: "Assists lead, handles simpler tasks"

  - name: "tester"
    agent_type: "test-engineer"
    count: 1
    required: true
    description: "Writes and runs tests"
```

### 3.2.3 Assignments section

```yaml
assignments:
  - role: "lead-developer"
    tasks:
      - "Core feature implementation"
      - "Code review"
      - "Architecture decisions"
    priority: "high"

  - role: "tester"
    tasks:
      - "Unit test creation"
      - "Integration test creation"
      - "Test execution"
    priority: "high"
    depends_on: ["lead-developer"]
```

### 3.2.4 Constraints section

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

---

## 3.3 Built-in templates

### 3.3.1 Project bootstrap template

**Use case:** Setting up a new project from scratch.

```yaml
metadata:
  name: "project-bootstrap"
  description: "Initial setup for new projects"

roles:
  - name: "architect"
    agent_type: "architect-agent"
    count: 1
    required: true

  - name: "implementer"
    agent_type: "code-implementer"
    count: 1
    required: true

  - name: "documenter"
    agent_type: "doc-writer"
    count: 1
    required: false

assignments:
  - role: "architect"
    tasks:
      - "Project structure design"
      - "Technology selection"
      - "Initial configuration"

  - role: "implementer"
    tasks:
      - "Skeleton code creation"
      - "Build system setup"
      - "CI/CD pipeline"
    depends_on: ["architect"]

  - role: "documenter"
    tasks:
      - "README creation"
      - "Setup documentation"
    depends_on: ["implementer"]
```

### 3.3.2 Feature development template

**Use case:** Implementing a single feature end-to-end.

```yaml
metadata:
  name: "feature-development"
  description: "Complete feature implementation workflow"

roles:
  - name: "developer"
    agent_type: "code-implementer"
    count: 1
    required: true

  - name: "tester"
    agent_type: "test-engineer"
    count: 1
    required: true

  - name: "reviewer"
    agent_type: "code-reviewer"
    count: 1
    required: false

assignments:
  - role: "developer"
    tasks:
      - "Feature implementation"
      - "Unit tests (basic)"
      - "Documentation inline"

  - role: "tester"
    tasks:
      - "Test plan creation"
      - "Unit test expansion"
      - "Integration tests"
    depends_on: ["developer"]

  - role: "reviewer"
    tasks:
      - "Code review"
      - "Quality check"
    depends_on: ["tester"]
```

### 3.3.3 Bug triage template

**Use case:** Investigating and fixing a reported bug.

```yaml
metadata:
  name: "bug-triage"
  description: "Bug investigation and resolution"

roles:
  - name: "investigator"
    agent_type: "code-implementer"
    count: 1
    required: true

  - name: "tester"
    agent_type: "test-engineer"
    count: 1
    required: true

assignments:
  - role: "investigator"
    tasks:
      - "Reproduce bug"
      - "Root cause analysis"
      - "Fix implementation"

  - role: "tester"
    tasks:
      - "Regression test creation"
      - "Fix verification"
    depends_on: ["investigator"]
```

### 3.3.4 Release preparation template

**Use case:** Preparing a release for publication.

```yaml
metadata:
  name: "release-preparation"
  description: "Release workflow from code freeze to publish"

roles:
  - name: "release-manager"
    agent_type: "devops-expert"
    count: 1
    required: true

  - name: "tester"
    agent_type: "test-engineer"
    count: 1
    required: true

  - name: "documenter"
    agent_type: "doc-writer"
    count: 1
    required: true

assignments:
  - role: "tester"
    tasks:
      - "Full test suite execution"
      - "Regression testing"
      - "Performance testing"

  - role: "documenter"
    tasks:
      - "Changelog update"
      - "Release notes"
      - "Version bump documentation"
    depends_on: ["tester"]

  - role: "release-manager"
    tasks:
      - "Version bump"
      - "Build creation"
      - "Package publication"
    depends_on: ["documenter"]
```

---

## 3.4 Creating custom templates

**Procedure:**

1. Identify the scenario that repeats
2. List roles needed for that scenario
3. Define task assignments for each role
4. Add constraints and dependencies
5. Validate the template
6. Store in templates directory

**Template file location:**
```
design/templates/staffing/
├── project-bootstrap.yaml
├── feature-development.yaml
├── bug-triage.yaml
├── release-preparation.yaml
└── custom/
    └── my-template.yaml
```

---

## 3.5 Template validation

**Validation checks:**

- [ ] Metadata complete (name, description, version)
- [ ] All roles have agent_type specified
- [ ] Required roles flagged appropriately
- [ ] Assignments reference valid roles
- [ ] Dependencies form acyclic graph
- [ ] Constraints are achievable

**Validation command:**
```bash
python scripts/ecos_validate_template.py templates/my-template.yaml
```

---

## 3.6 Examples

### Example: Applying Feature Development Template

```python
# Load template
template = load_template("feature-development")

# Customize for specific feature
template.metadata.description = "User authentication feature"
template.roles[0].count = 2  # Two developers

# Apply template
staffing_plan = apply_template(template, project="myapp")

# Output
# Spawning code-implementer-01 as developer
# Spawning code-implementer-02 as developer
# Spawning test-engineer-01 as tester
# Assignments created: 6 tasks across 3 agents
```

---

## 3.7 Troubleshooting

### Issue: Template roles not matching available agents

**Symptoms:** Cannot spawn required agent type.

**Resolution:**
1. Check agent registry for available types
2. Substitute similar agent type if capability overlaps
3. Mark role as optional if not critical
4. Update template for your environment

### Issue: Dependency cycle in assignments

**Symptoms:** Tasks cannot start, circular wait.

**Resolution:**
1. Draw dependency graph
2. Identify the cycle
3. Break cycle by removing one dependency
4. Reorder tasks if needed

### Issue: Template too rigid for project

**Symptoms:** Template does not fit actual needs.

**Resolution:**
1. Use template as starting point only
2. Modify roles and assignments as needed
3. Consider creating a custom template
4. Document deviations for future reference
