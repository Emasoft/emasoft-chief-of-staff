# Decision-Logic Patterns

## Definition

A Decision-Logic pattern documents:
- A decision point or question
- Criteria for making decision
- Decision tree or flowchart
- Examples of application
- Edge cases and exceptions

## Structure

```markdown
# Pattern: [Decision Name]

**Pattern ID**: dl_XXX
**Category**: Decision-Logic

## Decision Point
[The question or choice]

## Context
[When this decision is needed]

## Decision Criteria

### Factor 1: [Name]
**Weight**: High/Medium/Low
**Considerations**:
- Point 1
- Point 2

### Factor 2: [Name]
**Weight**: High/Medium/Low
**Considerations**:
- Point 1
- Point 2

## Decision Tree

```
START
├── If [condition A]
│   └── Choose: [Option 1]
├── Else if [condition B]
│   └── Choose: [Option 2]
└── Else
    └── Choose: [Option 3]
```

## Options Analysis

### Option 1: [Name]
**Pros**:
- Pro 1
- Pro 2

**Cons**:
- Con 1
- Con 2

**When to Choose**: [Conditions]

### Option 2: [Name]
[Similar analysis]

## Examples
[Concrete decision scenarios]

## Edge Cases
[Special situations]

## Related Decisions
[Links to related decision patterns]
```

## When to Create

Create a Decision-Logic pattern when:
- Decision affects significant work
- Decision establishes precedent
- Decision criteria are complex
- Decision is likely to recur
- Multiple options need evaluation

## Examples of Good Decision-Logic Patterns

- Feature request approval criteria
- Technology stack selection logic
- Test strategy selection
- Refactoring vs. rewrite decision
- Priority assignment logic

## Examples of Bad Decision-Logic Patterns

- Trivial yes/no choices (too simple)
- One-time unique decisions (not reusable)
- Personal preferences (not objective)
- Obvious decisions (not valuable)
