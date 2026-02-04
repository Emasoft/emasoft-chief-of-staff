# Config Conflict Resolution - Part 1: Concepts and Simple Conflicts

## Table of Contents

1. [Overview](#overview)
   - 1.1 [What Is Config Conflict Resolution?](#what-is-config-conflict-resolution)
   - 1.2 [Why Resolution Matters](#why-resolution-matters)
2. [Conflict Types](#conflict-types)
   - 2.1 [Type A: Non-Breaking Changes](#type-a-non-breaking-changes)
   - 2.2 [Type B: Breaking Changes - Future Application](#type-b-breaking-changes---future-application)
   - 2.3 [Type C: Breaking Changes - Immediate Application](#type-c-breaking-changes---immediate-application)
   - 2.4 [Type D: Irreconcilable Conflicts](#type-d-irreconcilable-conflicts)
3. [Resolution Strategies](#resolution-strategies)
   - 3.1 [Strategy 1: Immediate Adoption](#strategy-1-immediate-adoption)
   - 3.2 [Strategy 2: Deferred Adoption](#strategy-2-deferred-adoption)
   - 3.3 [Strategy 3: Immediate Restart](#strategy-3-immediate-restart)
   - 3.4 [Strategy 4: Escalate to Orchestrator](#strategy-4-escalate-to-orchestrator)
4. [Resolution Procedures for Simple Conflicts](#resolution-procedures)
   - 4.1 [PROCEDURE 1: Resolve Non-Breaking Changes](#procedure-1-resolve-non-breaking-changes)
   - 4.2 [PROCEDURE 2: Resolve Breaking Changes (Future)](#procedure-2-resolve-breaking-changes-future)

**See Also:** [Part 2: Critical Conflicts and Troubleshooting](21-config-conflict-resolution-part2-critical-conflicts.md) for Procedures 3-4, decision trees, examples, and troubleshooting.

---

## Overview

### What Is Config Conflict Resolution?

Config conflict resolution is the process of deciding how to handle differences between the session config snapshot and current central config. When configs change during a session, the agent must decide whether to adopt the new config, continue with the snapshot, or escalate to the orchestrator.

### Why Resolution Matters

**Without resolution:**
- Work becomes incompatible with standards
- Agent uses outdated or incorrect config
- Conflicts accumulate and cause errors

**With resolution:**
- Clear decision on which config to use
- Controlled adoption of config changes
- Documented resolution for audit trail

---

## Conflict Types

### Type A: Non-Breaking Changes

**Characteristics:**
- Formatting updates
- Documentation additions
- Comment improvements
- Minor version bumps (compatible)

**Impact:** Minimal - can adopt without code changes

**Default Action:** Adopt immediately and continue

**Example:**
```diff
# Snapshot
- Line length: 88 characters
+ Line length: 88 characters (PEP 8 standard)
```

---

### Type B: Breaking Changes - Future Application

**Characteristics:**
- Major version updates (Python 3.11 → 3.12)
- New framework versions
- Architecture changes
- Standards affecting future work

**Impact:** Breaking - requires code changes, but not for current task

**Default Action:** Complete current task with snapshot, adopt for next task

**Example:**
```diff
# Snapshot
- Python: 3.11.7
+ Python: 3.12.1
```

Current task uses Python 3.11 code - finish task, then upgrade.

---

### Type C: Breaking Changes - Immediate Application

**Characteristics:**
- Security patches
- Critical bug fixes
- Urgent standards updates
- Compliance requirements

**Impact:** Critical - requires immediate adoption and restart

**Default Action:** Pause work, adopt config, restart task

**Example:**
```diff
# Snapshot
- Python: 3.12.1
+ Python: 3.12.2 (CVE-2025-12345 security fix)
```

Security issue - must adopt immediately.

---

### Type D: Irreconcilable Conflicts

**Characteristics:**
- Contradictory requirements
- Incompatible tool versions
- Mutually exclusive standards
- Conflicting architectural decisions

**Impact:** Cannot proceed - requires orchestrator decision

**Default Action:** Stop work, report conflict, await decision

**Example:**
```
Snapshot requires: React 17
Current requires: Vue 3
(Framework change - incompatible)
```

---

## Resolution Strategies

### Strategy 1: Immediate Adoption

**When to use:**
- Non-breaking changes (Type A)
- Critical immediate changes (Type C)
- Orchestrator explicitly requests immediate adoption

**Process:**
1. Update config snapshot with new config
2. Apply changes to current work if needed
3. Log adoption in activeContext.md
4. Continue work without interruption

---

### Strategy 2: Deferred Adoption

**When to use:**
- Breaking changes affecting future work (Type B)
- Current task almost complete
- Orchestrator recommends deferred adoption

**Process:**
1. Complete current task using snapshot config
2. Mark pending config update in activeContext.md
3. After task completion, update snapshot
4. Apply new config to next task
5. Report adoption to orchestrator

---

### Strategy 3: Immediate Restart

**When to use:**
- Critical breaking changes (Type C)
- Security vulnerabilities
- Mandatory compliance updates
- Orchestrator requires immediate action

**Process:**
1. Pause current work
2. Save progress with "paused for config update" status
3. Update config snapshot
4. Restart current task with new config
5. Report restart to orchestrator

---

### Strategy 4: Escalate to Orchestrator

**When to use:**
- Irreconcilable conflicts (Type D)
- Unclear impact of changes
- Multiple conflicting requirements
- Agent cannot determine correct action

**Process:**
1. Stop work immediately
2. Document conflict details
3. Present options to orchestrator
4. Wait for orchestrator decision
5. Execute decided option

---

## Resolution Procedures

### PROCEDURE 1: Resolve Non-Breaking Changes

**When to use:**
- Type A conflict detected
- Changes are formatting/documentation only
- No code impact

**Steps:**

1. **Verify change is non-breaking**
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

2. **Update config snapshot**
   ```python
   # Replace snapshot section for this config
   update_snapshot_section('toolchain', current_toolchain_content)
   ```

3. **Apply changes if needed**
   ```python
   # Usually no code changes needed for non-breaking updates
   # But may need to update comments or documentation
   if changes_affect_code_comments:
       update_code_comments(diff.additions)
   ```

4. **Log resolution**
   ```markdown
   ## Config Conflict Resolution

   ### Resolution: 2025-12-31 15:00:00
   **Config:** toolchain.md
   **Conflict Type:** A (Non-Breaking)
   **Change:** Documentation clarification
   **Resolution:** Immediate adoption
   **Impact:** None - continued without interruption
   ```

5. **Continue work**
   ```
   Agent: Config update applied (non-breaking documentation change).
          Continuing work on current task.
   ```

---

### PROCEDURE 2: Resolve Breaking Changes (Future)

**When to use:**
- Type B conflict detected
- Breaking changes but not urgent
- Current task unaffected

**Steps:**

1. **Assess impact on current task**
   ```python
   def assess_impact_on_current_task(config_changes, current_task):
       # Check if current task uses changed features
       affected_features = extract_affected_features(config_changes)

       for feature in affected_features:
           if feature_used_by_task(feature, current_task):
               return 'IMMEDIATE'  # Current task affected

       return 'FUTURE'  # Only future tasks affected
   ```

2. **Mark pending config update**
   ```markdown
   ## Pending Config Updates

   ### Update Scheduled: toolchain.md
   **Detected:** 2025-12-31 15:00:00
   **Change:** Python 3.11 → 3.12
   **Type:** Breaking (future application)
   **Scheduled:** After current task completion
   **Current Task:** Implement auth middleware (unaffected by Python version)
   ```

3. **Complete current task with snapshot config**
   ```
   Agent: Config update detected (Python 3.11 → 3.12).
          Current task uses Python 3.11 code - completing with snapshot config.
          Will adopt Python 3.12 for next task.
   ```

4. **After task completion, adopt new config**
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

5. **Update snapshot and resume with new config**
   ```markdown
   ## Config Adoption Complete

   **Adopted:** 2025-12-31 15:30:00
   **Config:** toolchain.md
   **Change:** Python 3.11 → 3.12
   **Trigger:** Current task completed
   **Next Task:** Will use Python 3.12
   ```

---

**Continue to:** [Part 2: Critical Conflicts and Troubleshooting](21-config-conflict-resolution-part2-critical-conflicts.md)

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Target Audience:** Chief of Staff Agents
**Related:** SKILL.md (PROCEDURE 9: Handle Config Version Conflicts)
