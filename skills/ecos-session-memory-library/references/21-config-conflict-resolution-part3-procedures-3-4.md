# Resolution Procedures: Immediate Breaking and Irreconcilable Conflicts

## Table of Contents

1. [PROCEDURE 3: Resolve Breaking Changes (Immediate)](#procedure-3-resolve-breaking-changes-immediate)
   - Verifying criticality
   - Pausing current work
   - Logging pause event
   - Adopting new config
   - Restarting task
   - Reporting to orchestrator
2. [PROCEDURE 4: Resolve Irreconcilable Conflicts](#procedure-4-resolve-irreconcilable-conflicts)
   - Identifying conflict
   - Stopping work immediately
   - Documenting conflict
   - Generating resolution options
   - Reporting to orchestrator
   - Waiting for and executing decision

---

## PROCEDURE 3: Resolve Breaking Changes (Immediate)

**When to use:**
- Type C conflict detected
- Security or compliance requirement
- Orchestrator mandates immediate adoption
- Critical bug fix

**Steps:**

### Step 1: Verify criticality

```python
def is_critical_update(notification):
    critical_keywords = [
        'security', 'CVE', 'vulnerability',
        'critical', 'urgent', 'compliance',
        'mandatory', 'emergency'
    ]

    return any(kw in notification.reason.lower() for kw in critical_keywords)
```

### Step 2: Pause current work

```python
def pause_for_critical_update():
    # Save current progress
    current_state = capture_current_state()

    # Update progress.md
    mark_task_paused(current_task, reason='critical config update')

    # Save to disk
    save_all_memory()
```

### Step 3: Log pause event

```markdown
## Work Paused for Critical Config Update

**Paused At:** 2025-12-31 15:00:00
**Current Task:** Implement auth middleware
**Current File:** src/auth/middleware.py (line 45)
**Reason:** Critical security update - CVE-2025-12345
**Config:** toolchain.md (Python 3.12.1 → 3.12.2)
```

### Step 4: Adopt new config

```python
# Update snapshot
update_config_snapshot()

# Apply changes to environment
apply_config_changes('toolchain')

# Verify new config
verify_environment()
```

### Step 5: Restart task with new config

```python
def restart_task_with_new_config():
    # Reload task state
    task_state = load_paused_task()

    # Resume from saved point
    resume_task(task_state.task_name, task_state.file, task_state.line)
```

### Step 6: Log restart

```markdown
## Task Restarted with New Config

**Restarted At:** 2025-12-31 15:05:00
**Task:** Implement auth middleware
**File:** src/auth/middleware.py (line 45)
**New Config:** Python 3.12.2 (security fix applied)
**Status:** Resuming work
```

### Step 7: Report to orchestrator

> **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.
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

## PROCEDURE 4: Resolve Irreconcilable Conflicts

**When to use:**
- Type D conflict detected
- Cannot determine correct action
- Contradictory requirements
- Major architectural conflict

**Steps:**

### Step 1: Identify conflict

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

### Step 2: Stop work immediately

```python
def stop_for_conflict():
    print("IRRECONCILABLE CONFIG CONFLICT DETECTED")
    print("Stopping all work...")

    # Save state
    save_all_memory()

    # Mark as blocked
    mark_session_blocked(reason='config conflict')
```

### Step 3: Document conflict

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

### Step 4: Generate resolution options

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

### Step 5: Report to orchestrator

> **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.
```json
{
  "to": "orchestrator-master",
  "subject": "CONFIG CONFLICT: Cannot proceed",
  "priority": "critical",
  "content": {
    "type": "config-conflict",
    "session_id": "orchestrator-master-20251231-102345",
    "conflict_type": "D",
    "changed_files": ["design/config/toolchain.md"],  // OPTIONAL: If EOA (Emasoft Orchestrator Agent) plugin is installed
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

### Step 6: Wait for orchestrator decision

```
Agent: Critical config conflict detected. Work has been stopped.

CONFLICT: Framework change (React → Vue) incompatible with current task.

I've reported the conflict to the orchestrator with three options:
A) Continue current task with React
B) Restart task with Vue
C) Rollback config to React

Waiting for orchestrator decision...
```

### Step 7: Execute decision

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

**Version:** 1.0
**Last Updated:** 2026-01-01
**Parent Document:** [21-config-conflict-resolution.md](./21-config-conflict-resolution.md)
