# Workflow Patterns

## Definition

A Workflow pattern documents:
- A task or goal
- Prerequisites
- Step-by-step procedure
- Expected outcome
- Variations for different contexts

## Structure

```markdown
# Pattern: [Workflow Name]

**Pattern ID**: wf_XXX
**Category**: Workflow

## Task Description
[What this workflow accomplishes]

**Goal**: [Clear goal statement]

## Prerequisites
- Prerequisite 1
- Prerequisite 2

## Procedure

### Phase 1: [Phase Name]
#### Step 1: [Action]
[Details and examples]

#### Step 2: [Action]
[Details and examples]

### Phase 2: [Phase Name]
[Steps...]

## Expected Outcome
[What success looks like]

**Verification**:
- Check 1
- Check 2

## Variations

### Variation A: [When to use]
[Modified steps]

### Variation B: [When to use]
[Modified steps]

## Common Issues
[Problems that might occur]

## Examples
[Concrete usage examples]
```

## When to Create

Create a Workflow pattern when:
- You developed an efficient procedure
- Procedure has multiple steps
- Procedure is likely to be repeated
- Procedure has variations for different contexts

## Examples of Good Workflow Patterns

- Parallel test execution across agents
- Safe code refactoring procedure
- Feature branch to production workflow
- Database migration procedure
- Documentation generation workflow

## Examples of Bad Workflow Patterns

- Single-step procedures (too simple)
- Unique one-time procedures (not reusable)
- Standard tool usage (already documented)
- Trivial tasks (not worth documenting)
