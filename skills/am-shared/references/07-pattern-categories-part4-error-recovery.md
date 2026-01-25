# Error-Recovery Patterns

## Definition

An Error-Recovery pattern documents:
- Error or failure type
- Symptoms and detection
- Root cause
- Recovery procedure
- Prevention measures
- Verification steps

## Structure

```markdown
# Pattern: [Error Name]

**Pattern ID**: er_XXX
**Category**: Error-Recovery

## Error Description
[What fails and how]

**Symptoms**:
- Observable symptom 1
- Observable symptom 2
- Error messages

**Impact**:
[What breaks when this error occurs]

## Detection
[How to detect this error]

```bash
# Detection commands
command to check for error
```

## Root Cause
[Why this error occurs]

**Common Triggers**:
- Trigger 1
- Trigger 2

## Recovery Procedure

### Step 1: Stop Further Damage
[Immediate actions to prevent escalation]

### Step 2: Assess State
[How to check current state]

### Step 3: Restore to Known-Good State
[Recovery steps]

### Step 4: Verify Recovery
[Verification procedure]

## Prevention
[How to prevent this error]

**Checklist**:
- [ ] Prevention measure 1
- [ ] Prevention measure 2

## Examples
[Concrete recovery scenarios]

## Related Patterns
[Links to related error patterns]
```

## When to Create

Create an Error-Recovery pattern when:
- Error caused significant disruption
- Error is likely to recur
- Recovery procedure is non-obvious
- Error has been encountered before
- Prevention measures exist

## Examples of Good Error-Recovery Patterns

- Recovery from failed compaction
- Handling context overflow
- Git repository corruption recovery
- Database rollback procedure
- Build system failure recovery

## Examples of Bad Error-Recovery Patterns

- Simple retry logic (too trivial)
- Unrecoverable errors (no solution)
- External service failures (no control)
- User errors (different category)
