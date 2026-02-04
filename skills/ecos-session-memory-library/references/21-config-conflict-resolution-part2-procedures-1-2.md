# Resolution Procedures: Non-Breaking and Future Breaking Changes

## Table of Contents

1. [PROCEDURE 1: Resolve Non-Breaking Changes](#procedure-1-resolve-non-breaking-changes)
   - When to use this procedure
   - Step-by-step verification and adoption
   - Logging resolution
2. [PROCEDURE 2: Resolve Breaking Changes (Future)](#procedure-2-resolve-breaking-changes-future)
   - Assessing impact on current task
   - Marking pending config updates
   - Completing with snapshot config
   - Adopting after task completion

---

## PROCEDURE 1: Resolve Non-Breaking Changes

**When to use:**
- Type A conflict detected
- Changes are formatting/documentation only
- No code impact

**Steps:**

### Step 1: Verify change is non-breaking

```python
def is_non_breaking(diff):
    # Non-breaking patterns
    non_breaking = [
        'comment', 'documentation', 'formatting',
        'whitespace', 'typo fix', 'clarification'
    ]

    # Check if all changes match non-breaking patterns
    for change in diff.additions + diff.deletions:
        if not any(pattern in change.lower() for pattern in non_breaking):
            return False

    return True
```

### Step 2: Update config snapshot

```python
# Replace snapshot section for this config
update_snapshot_section('toolchain', current_toolchain_content)
```

### Step 3: Apply changes if needed

```python
# Usually no code changes needed for non-breaking updates
# But may need to update comments or documentation
if changes_affect_code_comments:
    update_code_comments(diff.additions)
```

### Step 4: Log resolution

```markdown
## Config Conflict Resolution

### Resolution: 2025-12-31 15:00:00
**Config:** toolchain.md
**Conflict Type:** A (Non-Breaking)
**Change:** Documentation clarification
**Resolution:** Immediate adoption
**Impact:** None - continued without interruption
```

### Step 5: Continue work

```
Agent: Config update applied (non-breaking documentation change).
       Continuing work on current task.
```

---

## PROCEDURE 2: Resolve Breaking Changes (Future)

**When to use:**
- Type B conflict detected
- Breaking changes but not urgent
- Current task unaffected

**Steps:**

### Step 1: Assess impact on current task

```python
def assess_impact_on_current_task(config_changes, current_task):
    # Check if current task uses changed features
    affected_features = extract_affected_features(config_changes)

    for feature in affected_features:
        if feature_used_by_task(feature, current_task):
            return 'IMMEDIATE'  # Current task affected

    return 'FUTURE'  # Only future tasks affected
```

### Step 2: Mark pending config update

```markdown
## Pending Config Updates

### Update Scheduled: toolchain.md
**Detected:** 2025-12-31 15:00:00
**Change:** Python 3.11 → 3.12
**Type:** Breaking (future application)
**Scheduled:** After current task completion
**Current Task:** Implement auth middleware (unaffected by Python version)
```

### Step 3: Complete current task with snapshot config

```
Agent: Config update detected (Python 3.11 → 3.12).
       Current task uses Python 3.11 code - completing with snapshot config.
       Will adopt Python 3.12 for next task.
```

### Step 4: After task completion, adopt new config

```python
def on_task_complete():
    # Check for pending config updates
    if has_pending_config_updates():
        print("Adopting pending config updates...")

        # Update snapshot
        update_config_snapshot()

        # Log adoption
        log_config_adoption()

        # Notify orchestrator
        notify_config_adopted()
```

### Step 5: Update snapshot and resume with new config

```markdown
## Config Adoption Complete

**Adopted:** 2025-12-31 15:30:00
**Config:** toolchain.md
**Change:** Python 3.11 → 3.12
**Trigger:** Current task completed
**Next Task:** Will use Python 3.12
```

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Parent Document:** [21-config-conflict-resolution.md](./21-config-conflict-resolution.md)
