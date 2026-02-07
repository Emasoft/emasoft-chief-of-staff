---
procedure: support-skill
workflow-instruction: support
operation: record-discovered-pattern
parent-skill: ecos-session-memory-library
---

# Operation: Record Discovered Pattern

## Purpose

Capture recurring patterns, effective solutions, and lessons learned for future reference.

## When To Use This Operation

- After identifying a recurring pattern
- When discovering an anti-pattern to avoid
- When finding an effective solution worth remembering
- When learning project conventions

## Pattern Categories

| Category | Description | Example |
|----------|-------------|---------|
| Problem-Solution | Recurring problems and their fixes | Error handling approach |
| Workflow | Effective sequences of actions | Deployment procedure |
| Decision-Logic | Criteria for making choices | When to escalate |
| Error-Recovery | Recovery from specific failures | Memory exhaustion fix |
| Configuration | Settings that work well | Optimal timeout values |

## Steps

### Step 1: Identify the Pattern

Document what you observed:
- What situation triggered this?
- What was the successful approach?
- Why does it work?
- When should it be applied?

### Step 2: Open patterns.md

```bash
PATTERNS_FILE="$CLAUDE_PROJECT_DIR/design/memory/patterns.md"
```

### Step 3: Add Pattern Entry

```markdown
## Pattern: [Descriptive Name]

**Category:** [Problem-Solution|Workflow|Decision-Logic|Error-Recovery|Configuration]
**Discovered:** [ISO8601]
**Context:** [When/where this was discovered]

### Problem
[What problem or situation does this address?]

### Solution
[What is the effective approach?]

### Example
[Concrete example of applying this pattern]

### When to Use
- [Condition 1]
- [Condition 2]

### When NOT to Use
- [Exception 1]
- [Exception 2]
```

### Step 4: Update Index

Add to the index at the top of patterns.md:

```markdown
## Index
- [Pattern Name 1](#pattern-name-1) - [Category]
- [Pattern Name 2](#pattern-name-2) - [Category]
- [NEW] [Your Pattern](#your-pattern) - [Category]
```

### Step 5: Update Timestamp

```markdown
# Discovered Patterns

Last Updated: [ISO8601]
```

## Checklist

Copy this checklist and track your progress:

- [ ] Pattern identified and understood
- [ ] Category determined
- [ ] Problem statement written
- [ ] Solution documented
- [ ] Example provided
- [ ] Usage conditions listed
- [ ] Index updated
- [ ] File timestamp updated

## Example Pattern Entry

```markdown
## Pattern: Fail-Fast Error Propagation

**Category:** Error-Recovery
**Discovered:** 2025-02-05T10:00:00Z
**Context:** Discovered during debugging of silent failures in agent coordination

### Problem
Silent failures cause cascading issues. Agents continue with corrupted state, leading to confusing bugs later.

### Solution
Let errors propagate immediately. Handle errors only at boundary layers (API endpoints, message handlers). No try/catch in internal functions.

### Example
```python
# WRONG - swallows error
def process_task(task):
    try:
        result = do_work(task)
    except Exception:
        result = None  # Silent failure!
    return result

# RIGHT - propagates error
def process_task(task):
    return do_work(task)  # Let it fail if it fails
```

### When to Use
- Internal processing functions
- Data transformation
- Business logic

### When NOT to Use
- API request handlers (need to return error response)
- User-facing interfaces (need friendly messages)
```

## Output

After completing this operation:
- Pattern documented in patterns.md
- Index updated
- Available for future reference

## Related References

- [05-record-patterns.md](05-record-patterns.md) - Complete pattern recording guide
- [07-pattern-categories.md](07-pattern-categories.md) - Category definitions

## Next Operation

Continue work or use [op-update-active-context.md](op-update-active-context.md) to record context
