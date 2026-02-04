# Session Memory Examples

## Table of Contents

- [Example 1: Initializing Session Memory](#example-1-initializing-session-memory) - Using the initialize-memory.py script
- [Example 2: Recovering After Interruption](#example-2-recovering-after-interruption) - Reading activeContext.md to resume work
- [Example 3: Updating Progress After Task Completion](#example-3-updating-progress-after-task-completion) - Marking tasks complete in progress.md

---

## Example 1: Initializing Session Memory

```python
# Using the initialize-memory.py script
python scripts/initialize-memory.py --project /path/to/project

# Output
Created design/memory/
Created design/memory/activeContext.md
Created design/memory/patterns.md
Created design/memory/progress.md
Session memory initialized successfully
```

## Example 2: Recovering After Interruption

```markdown
# In activeContext.md after recovery
## Current State
- **Last Active Task**: Implementing user login module
- **Current File**: src/auth/login.py:145
- **Pending Operations**: None
- **Recovery Timestamp**: 2025-01-30T10:00:00Z

# Agent reads this and resumes from line 145 of login.py
```

## Example 3: Updating Progress After Task Completion

```markdown
# In progress.md
## Tasks

- [x] Design authentication module (completed: 2025-01-29)
- [x] Implement login endpoint (completed: 2025-01-30)
- [ ] Implement logout endpoint (in progress)
- [ ] Add session management (blocked by: logout endpoint)
```

---

**Version:** 1.0
**Last Updated:** 2025-02-03
