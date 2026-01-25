# Config Conflict Types and Resolution Strategies

## Table of Contents

1. [Conflict Types Overview](#conflict-types)
   - [Type A: Non-Breaking Changes](#type-a-non-breaking-changes)
   - [Type B: Breaking Changes - Future Application](#type-b-breaking-changes---future-application)
   - [Type C: Breaking Changes - Immediate Application](#type-c-breaking-changes---immediate-application)
   - [Type D: Irreconcilable Conflicts](#type-d-irreconcilable-conflicts)
2. [Resolution Strategies](#resolution-strategies)
   - [Strategy 1: Immediate Adoption](#strategy-1-immediate-adoption)
   - [Strategy 2: Deferred Adoption](#strategy-2-deferred-adoption)
   - [Strategy 3: Immediate Restart](#strategy-3-immediate-restart)
   - [Strategy 4: Escalate to Orchestrator](#strategy-4-escalate-to-orchestrator)

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

**Version:** 1.0
**Last Updated:** 2026-01-01
**Parent Document:** [21-config-conflict-resolution.md](./21-config-conflict-resolution.md)
