# Decision Trees, Examples, and Troubleshooting

## Table of Contents

1. [Decision Trees](#decision-trees)
   - [Decision Tree 1: Initial Conflict Classification](#decision-tree-1-initial-conflict-classification)
   - [Decision Tree 2: Breaking Change Handling](#decision-tree-2-breaking-change-handling)
2. [Examples](#examples)
   - [Example 1: Resolving Non-Breaking Change](#example-1-resolving-non-breaking-change)
   - [Example 2: Resolving Breaking Change (Future)](#example-2-resolving-breaking-change-future)
   - [Example 3: Resolving Critical Security Update](#example-3-resolving-critical-security-update)
3. [Troubleshooting](#troubleshooting)
   - [Cannot determine if change is breaking](#issue-cannot-determine-if-change-is-breaking)
   - [Immediate adoption fails](#issue-immediate-adoption-fails)

---

## Decision Trees

### Decision Tree 1: Initial Conflict Classification

Use this decision tree when a config change is first detected to determine the conflict type and which procedure to follow.

```
Config change detected
└─ Is change breaking?
   ├─ NO → Type A (Non-Breaking)
   │        └─ PROCEDURE 1: Adopt immediately
   └─ YES → Is change critical/security?
            ├─ YES → Type C (Immediate Breaking)
            │        └─ PROCEDURE 3: Pause and adopt
            └─ NO → Does it affect current task?
                    ├─ NO → Type B (Future Breaking)
                    │       └─ PROCEDURE 2: Defer to next task
                    └─ YES → Is it compatible?
                             ├─ YES → Type B (Future Breaking)
                             │       └─ PROCEDURE 2: Complete then adopt
                             └─ NO → Type D (Irreconcilable)
                                     └─ PROCEDURE 4: Escalate
```

**How to use this tree:**

1. Start at "Config change detected"
2. Answer each question based on the change characteristics
3. Follow the branches until you reach a Type classification
4. Execute the indicated PROCEDURE

---

### Decision Tree 2: Breaking Change Handling

Use this decision tree when you have already determined the change is breaking (Types B, C, or D).

```
Breaking change detected
└─ Check notification priority
   ├─ CRITICAL → PROCEDURE 3 (Immediate)
   ├─ HIGH → Check current task impact
   │         ├─ Affected → PROCEDURE 3 (Immediate)
   │         └─ Not affected → PROCEDURE 2 (Future)
   └─ NORMAL → PROCEDURE 2 (Future)
```

**Priority mapping:**

| Priority | Keywords in notification |
|----------|--------------------------|
| CRITICAL | security, CVE, vulnerability, emergency, compliance |
| HIGH | urgent, important, breaking, major |
| NORMAL | update, change, improvement |

---

## Examples

### Example 1: Resolving Non-Breaking Change

**Scenario:** Documentation clarification detected in standards.md

**Change detected:**
```diff
# standards.md
- Line length: 88 characters
+ Line length: 88 characters (enforced by ruff formatter)
```

**Resolution process:**

```
Config Update Detected (Non-Breaking)
======================================

Config: standards.md
Change: Documentation clarification
Type: A (Non-Breaking)

Resolution: Immediate adoption
└─ Updated snapshot
└─ No code changes needed
└─ Continuing work

Time: <1 second
Impact: None
```

**What the agent does:**
1. Recognizes change is documentation only
2. Updates config snapshot immediately
3. Logs the adoption
4. Continues work without interruption

---

### Example 2: Resolving Breaking Change (Future)

**Scenario:** Python version upgrade detected, but current task doesn't require new features

**Change detected:**
```diff
# toolchain.md
- Python: 3.11.7
+ Python: 3.12.1
```

**Resolution process:**

```
Config Update Detected (Breaking - Future)
===========================================

Config: toolchain.md
Change: Python 3.11.7 → 3.12.1
Type: B (Future Breaking)
Current Task: Uses Python 3.11 syntax

Resolution: Deferred adoption
└─ Completing current task with Python 3.11
└─ Will adopt Python 3.12 for next task
└─ No immediate impact

Scheduled: After task "Implement auth middleware" completes
```

**What the agent does:**
1. Assesses impact on current task (minimal)
2. Marks pending config update in activeContext.md
3. Completes current task with snapshot config
4. Adopts new config after task completion
5. Reports adoption to orchestrator

---

### Example 3: Resolving Critical Security Update

**Scenario:** CVE security fix requires immediate Python update

**Notification received:**
```
CRITICAL: CVE-2025-12345 requires Python 3.12.2
Priority: CRITICAL
Action: Immediate adoption required
```

**Resolution process:**

```
CRITICAL CONFIG UPDATE
======================

PAUSING WORK...
└─ Saving progress... Done
└─ Current: Python 3.12.1
└─ Required: Python 3.12.2 (security fix)

ADOPTING NEW CONFIG...
└─ Updating snapshot... Done
└─ Applying changes... Done
└─ Verifying environment... OK

RESTARTING TASK...
└─ Task: Implement auth middleware
└─ File: src/auth/middleware.py (line 45)
└─ Status: Resumed with Python 3.12.2

Downtime: 3 minutes
```

**What the agent does:**
1. Recognizes CRITICAL priority from keywords
2. Immediately pauses current work
3. Saves all progress to memory files
4. Updates config snapshot
5. Applies config changes to environment
6. Restarts task from saved position
7. Reports to orchestrator with downtime metrics

---

## Troubleshooting

### Issue: Cannot determine if change is breaking

**Symptoms:**
- Change seems minor but might affect code
- Unclear impact
- No clear classification

**Solution:**
1. **Assume breaking (safer)** - When in doubt, treat as Type B
2. **Use deferred adoption** - Complete current task first
3. **Review impact during task transition** - Assess before starting new task
4. **Ask orchestrator if unclear** - Escalate if still uncertain

**Example decision:**
```
Agent: Config change detected in toolchain.md.
       Change: Build tool flag modification
       Impact: Unclear

       Treating as Type B (Future Breaking) to be safe.
       Will complete current task, then evaluate before next task.
```

---

### Issue: Immediate adoption fails

**Symptoms:**
- Config adopted but environment broken
- Code doesn't work with new config
- Tests fail after adoption

**Solution:**
1. **Rollback to snapshot** - Restore previous working config
2. **Classify as Type D** - Treat as irreconcilable conflict
3. **Escalate to orchestrator** - Report the failed adoption
4. **Do not attempt further adoption** - Wait for guidance

**Example handling:**
```
Agent: ADOPTION FAILED

       Attempted: Python 3.12.2 adoption
       Result: Environment verification failed
       Error: Package X incompatible with Python 3.12.2

       Rolling back to snapshot (Python 3.12.1)...
       └─ Rollback complete

       Escalating to orchestrator as Type D conflict.
       Work paused until resolution received.
```

**Escalation message:**
```json
{
  "to": "orchestrator-master",
  "subject": "CONFIG ADOPTION FAILED",
  "priority": "critical",
  "content": {
    "type": "adoption-failure",
    "config": "toolchain.md",
    "attempted_change": "Python 3.12.1 → 3.12.2",
    "error": "Package X incompatible with Python 3.12.2",
    "current_state": "Rolled back to Python 3.12.1",
    "awaiting_decision": true
  }
}
```

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Parent Document:** [21-config-conflict-resolution.md](./21-config-conflict-resolution.md)
