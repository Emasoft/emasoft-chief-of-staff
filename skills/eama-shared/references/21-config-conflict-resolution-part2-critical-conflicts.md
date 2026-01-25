# Config Conflict Resolution - Part 2: Critical Conflicts and Troubleshooting

## Table of Contents

1. [Critical Resolution Procedures](#resolution-procedures)
   - 1.1 [PROCEDURE 3: Resolve Breaking Changes (Immediate)](#procedure-3-resolve-breaking-changes-immediate)
   - 1.2 [PROCEDURE 4: Resolve Irreconcilable Conflicts](#procedure-4-resolve-irreconcilable-conflicts)
2. [Decision Trees](#decision-trees)
   - 2.1 [Decision Tree 1: Initial Conflict Classification](#decision-tree-1-initial-conflict-classification)
   - 2.2 [Decision Tree 2: Breaking Change Handling](#decision-tree-2-breaking-change-handling)
3. [Examples](#examples)
   - 3.1 [Example 1: Resolving Non-Breaking Change](#example-1-resolving-non-breaking-change)
   - 3.2 [Example 2: Resolving Breaking Change (Future)](#example-2-resolving-breaking-change-future)
   - 3.3 [Example 3: Resolving Critical Security Update](#example-3-resolving-critical-security-update)
4. [Troubleshooting](#troubleshooting)
   - 4.1 [Issue: Cannot determine if change is breaking](#issue-cannot-determine-if-change-is-breaking)
   - 4.2 [Issue: Immediate adoption fails](#issue-immediate-adoption-fails)

**See Also:** [Part 1: Concepts and Simple Conflicts](21-config-conflict-resolution-part1-concepts-and-simple-conflicts.md) for overview, conflict types, and Procedures 1-2.

---

## Resolution Procedures

### PROCEDURE 3: Resolve Breaking Changes (Immediate)

**When to use:**
- Type C conflict detected
- Security or compliance requirement
- Orchestrator mandates immediate adoption
- Critical bug fix

**Steps:**

1. **Verify criticality**
   ```python
   def is_critical_update(notification):
       critical_keywords = [
           'security', 'CVE', 'vulnerability',
           'critical', 'urgent', 'compliance',
           'mandatory', 'emergency'
       ]

       return any(kw in notification.reason.lower() for kw in critical_keywords)
   ```

2. **Pause current work**
   ```python
   def pause_for_critical_update():
       # Save current progress
       current_state = capture_current_state()

       # Update progress.md
       mark_task_paused(current_task, reason='critical config update')

       # Save to disk
       save_all_memory()
   ```

3. **Log pause event**
   ```markdown
   ## Work Paused for Critical Config Update

   **Paused At:** 2025-12-31 15:00:00
   **Current Task:** Implement auth middleware
   **Current File:** src/auth/middleware.py (line 45)
   **Reason:** Critical security update - CVE-2025-12345
   **Config:** toolchain.md (Python 3.12.1 → 3.12.2)
   ```

4. **Adopt new config**
   ```python
   # Update snapshot
   update_config_snapshot()

   # Apply changes to environment
   apply_config_changes('toolchain')

   # Verify new config
   verify_environment()
   ```

5. **Restart task with new config**
   ```python
   def restart_task_with_new_config():
       # Reload task state
       task_state = load_paused_task()

       # Resume from saved point
       resume_task(task_state.task_name, task_state.file, task_state.line)
   ```

6. **Log restart**
   ```markdown
   ## Task Restarted with New Config

   **Restarted At:** 2025-12-31 15:05:00
   **Task:** Implement auth middleware
   **File:** src/auth/middleware.py (line 45)
   **New Config:** Python 3.12.2 (security fix applied)
   **Status:** Resuming work
   ```

7. **Report to orchestrator**
   ```json
   {
     "to": "orchestrator-master",
     "subject": "Critical config adopted",
     "priority": "high",
     "content": {
       "type": "config-adopted",
       "session_id": "orchestrator-master-20251231-102345",
       "config": "toolchain.md",
       "change": "Python 3.12.1 → 3.12.2",
       "reason": "CVE-2025-12345 security fix",
       "paused_at": "2025-12-31T15:00:00",
       "resumed_at": "2025-12-31T15:05:00",
       "impact": "5 minutes downtime"
     }
   }
   ```

---

### PROCEDURE 4: Resolve Irreconcilable Conflicts

**When to use:**
- Type D conflict detected
- Cannot determine correct action
- Contradictory requirements
- Major architectural conflict

**Steps:**

1. **Identify conflict**
   ```python
   def identify_conflict(snapshot_config, current_config):
       conflicts = []

       # Check for incompatible requirements
       snapshot_reqs = extract_requirements(snapshot_config)
       current_reqs = extract_requirements(current_config)

       for req_type in snapshot_reqs:
           if req_type in current_reqs:
               if not compatible(snapshot_reqs[req_type], current_reqs[req_type]):
                   conflicts.append({
                       'type': req_type,
                       'snapshot': snapshot_reqs[req_type],
                       'current': current_reqs[req_type]
                   })

       return conflicts
   ```

2. **Stop work immediately**
   ```python
   def stop_for_conflict():
       print("IRRECONCILABLE CONFIG CONFLICT DETECTED")
       print("Stopping all work...")

       # Save state
       save_all_memory()

       # Mark as blocked
       mark_session_blocked(reason='config conflict')
   ```

3. **Document conflict**
   ```markdown
   ## IRRECONCILABLE CONFIG CONFLICT

   **Detected:** 2025-12-31 15:00:00
   **Config:** toolchain.md
   **Conflict Type:** D (Irreconcilable)

   ### Conflict Details
   **Snapshot Requirement:** React 17 for frontend framework
   **Current Requirement:** Vue 3 for frontend framework

   **Issue:** Cannot use both React and Vue simultaneously
   **Impact:** Current task (React component) incompatible with new config (Vue)
   **Work Blocked:** Cannot proceed without resolution
   ```

4. **Generate resolution options**
   ```python
   options = [
       {
           'id': 'A',
           'description': 'Continue with snapshot config (React 17)',
           'impact': 'Complete current task, ignore new config',
           'risk': 'Work may be obsolete if Vue is final decision'
       },
       {
           'id': 'B',
           'description': 'Adopt current config (Vue 3)',
           'impact': 'Restart task from beginning with Vue',
           'risk': 'Lose progress on React implementation'
       },
       {
           'id': 'C',
           'description': 'Rollback config change',
           'impact': 'Restore config to React 17',
           'risk': 'May conflict with orchestrator decision'
       }
   ]
   ```

5. **Report to orchestrator**
   ```json
   {
     "to": "orchestrator-master",
     "subject": "CONFIG CONFLICT: Cannot proceed",
     "priority": "critical",
     "content": {
       "type": "config-conflict",
       "session_id": "orchestrator-master-20251231-102345",
       "conflict_type": "D",
       "changed_files": [".atlas/config/toolchain.md"],
       "current_task": "Implement React auth component",
       "conflict_description": "Snapshot requires React 17, current config requires Vue 3",
       "options": [
         {"id": "A", "description": "Continue with React 17"},
         {"id": "B", "description": "Restart with Vue 3"},
         {"id": "C", "description": "Rollback to React 17"}
       ],
       "recommendation": "A",
       "awaiting_decision": true
     }
   }
   ```

6. **Wait for orchestrator decision**
   ```
   Agent: Critical config conflict detected. Work has been stopped.

   CONFLICT: Framework change (React → Vue) incompatible with current task.

   I've reported the conflict to the orchestrator with three options:
   A) Continue current task with React
   B) Restart task with Vue
   C) Rollback config to React

   Waiting for orchestrator decision...
   ```

7. **Execute decision**
   ```python
   def execute_resolution_decision(decision):
       if decision == 'A':
           # Continue with snapshot
           print("Continuing with snapshot config (React 17)")
           resume_work()

       elif decision == 'B':
           # Adopt new config and restart
           print("Adopting new config (Vue 3) and restarting task")
           update_config_snapshot()
           restart_task_from_beginning()

       elif decision == 'C':
           # Rollback
           print("Rolling back config change")
           request_config_rollback()
           resume_work()
   ```

---

## Decision Trees

### Decision Tree 1: Initial Conflict Classification

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

---

### Decision Tree 2: Breaking Change Handling

```
Breaking change detected
└─ Check notification priority
   ├─ CRITICAL → PROCEDURE 3 (Immediate)
   ├─ HIGH → Check current task impact
   │         ├─ Affected → PROCEDURE 3 (Immediate)
   │         └─ Not affected → PROCEDURE 2 (Future)
   └─ NORMAL → PROCEDURE 2 (Future)
```

---

## Examples

### Example 1: Resolving Non-Breaking Change

**Change detected:**
```diff
# standards.md
- Line length: 88 characters
+ Line length: 88 characters (enforced by ruff formatter)
```

**Resolution:**
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

---

### Example 2: Resolving Breaking Change (Future)

**Change detected:**
```diff
# toolchain.md
- Python: 3.11.7
+ Python: 3.12.1
```

**Resolution:**
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

---

### Example 3: Resolving Critical Security Update

**Notification received:**
```
CRITICAL: CVE-2025-12345 requires Python 3.12.2
Priority: CRITICAL
Action: Immediate adoption required
```

**Resolution:**
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

---

## Troubleshooting

### Issue: Cannot determine if change is breaking

**Symptoms:**
- Change seems minor but might affect code
- Unclear impact

**Solution:**
1. Assume breaking (safer)
2. Use deferred adoption (Type B)
3. Review impact during task transition
4. Ask orchestrator if unclear

---

### Issue: Immediate adoption fails

**Symptoms:**
- Config adopted but environment broken
- Code doesn't work with new config

**Solution:**
1. Rollback to snapshot
2. Classify as Type D (irreconcilable)
3. Escalate to orchestrator
4. Do not attempt further adoption

---

**Back to:** [Part 1: Concepts and Simple Conflicts](21-config-conflict-resolution-part1-concepts-and-simple-conflicts.md)

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Target Audience:** Atlas Orchestrator Agents
**Related:** SKILL.md (PROCEDURE 9: Handle Config Version Conflicts)
