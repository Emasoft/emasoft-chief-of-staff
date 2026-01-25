# Problem-Solution Patterns

## Definition

A Problem-Solution pattern documents:
- A specific problem encountered
- The context where it occurred
- The solution that worked
- Why the solution worked
- When to apply this solution

## Structure

```markdown
# Pattern: [Problem Name]

**Pattern ID**: ps_XXX
**Category**: Problem-Solution

## Problem Description
[Clear description of problem]

**Symptoms**:
- Observable symptom 1
- Observable symptom 2

**Context**:
- When this problem occurs
- Prerequisites or conditions

## Root Cause
[Explanation of why problem occurs]

## Solution
[Step-by-step solution]

### Step 1: [Action]
[Details]

### Step 2: [Action]
[Details]

## Why This Works
[Explanation of mechanism]

## When to Use
- Condition 1
- Condition 2

## Examples
[Concrete examples]

## Prevention
[How to prevent this problem]
```

## When to Create

Create a Problem-Solution pattern when:
- You spent >15 minutes solving a problem
- Problem is likely to recur
- Solution is non-obvious
- Problem affected workflow significantly

## Examples of Good Problem-Solution Patterns

- Git authentication failure in parallel agents
- Context overflow during compaction
- Test failures due to race conditions
- Build errors after dependency update
- CI/CD pipeline timing out

## Examples of Bad Problem-Solution Patterns

- Simple typo fix (too trivial)
- One-time unique issue (not reusable)
- Problem without clear solution (incomplete)
- Already well-documented elsewhere (redundant)
