---
name: eama-user-communication
description: Use when communicating with users for clarification, presenting options, requesting approval, or reporting completion
context: fork
agent: eama-main
user-invocable: false
triggers:
  - when clarifying requirements
  - when presenting options to user
  - when requesting approval
  - when reporting completion
---

# User Communication Skill

## Overview

Standardize how the assistant manager communicates with users for consistency and clarity.

## Prerequisites

None required. This skill provides communication patterns that can be used immediately.

## Instructions

1. Identify the communication type needed (clarification, options, approval, completion)
2. Use the appropriate template from the Communication Patterns section
3. Fill in all placeholders with specific information
4. Follow the Quality Rules to ensure clarity
5. Include relevant UUIDs, issue numbers, and file paths for traceability

## Communication Patterns

### 1. Clarification Request

When user input is incomplete:
```
I need clarification on the following:

1. [Specific question]
2. [Specific question]

Please provide:
- [What you need]
- [Format expected]
```

### 2. Option Presentation

When presenting choices:
```
I've identified [N] options:

**Option A: [Name]**
- Pros: [list]
- Cons: [list]
- Effort: [estimate]

**Option B: [Name]**
...

Which would you prefer?
```

### 3. Approval Request

When needing approval:
```
**Approval Requested**

Action: [What will happen]
Impact: [What changes]
Reversible: Yes/No

Please respond with:
- "approve" to proceed
- "deny" to cancel
- "modify" to adjust
```

### 4. Completion Report

When work is done:
```
**Task Complete**

Summary: [1-2 sentences]
Changes made:
- [file: change]

Verification: [How to check]
Next steps: [What happens now]
```

## Quality Rules

1. **Be Specific**: Never say "some files" - list them
2. **Be Actionable**: Always tell user what to do next
3. **Be Honest**: Admit uncertainty, don't guess
4. **Be Concise**: Use bullets, avoid walls of text
5. **Be Traceable**: Include UUIDs, issue numbers

## Examples

### Example 1: Clarification Request

```markdown
I need clarification on the following:

1. Should the login support both email and username?
2. What is the session timeout duration?

Please provide:
- Your preference for login identifiers
- Timeout in minutes (e.g., 30, 60, 120)
```

### Example 2: Completion Report

```markdown
**Task Complete**

Summary: Implemented user login endpoint with OAuth2 support.

Changes made:
- src/auth/login.py: Added login handler
- src/auth/oauth.py: Added OAuth2 flow
- tests/test_login.py: Added 15 test cases

Verification: Run `pytest tests/test_login.py` - all tests should pass

Next steps: Proceed with logout endpoint implementation
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| No user response | User inactive | Wait, then send gentle reminder |
| Ambiguous user input | Unclear response | Ask for specific clarification |
| Template mismatch | Wrong pattern selected | Re-evaluate and use correct template |

## Resources

- [eama-approval-workflows SKILL](../eama-approval-workflows/SKILL.md) - Approval communication patterns
- [eama-role-routing SKILL](../eama-role-routing/SKILL.md) - Routing communication patterns
- [Message Templates](../../shared/message_templates.md)
