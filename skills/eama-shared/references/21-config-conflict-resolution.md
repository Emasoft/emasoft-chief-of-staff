# Resolving Config Conflicts

## Table of Contents

1. [Overview](#overview)
2. [Conflict Types and Resolution Strategies](#conflict-types-and-resolution-strategies) → [Part 1](./21-config-conflict-resolution-part1-types-strategies.md)
3. [Resolution Procedures 1-2](#resolution-procedures-1-2) → [Part 2](./21-config-conflict-resolution-part2-procedures-1-2.md)
4. [Resolution Procedures 3-4](#resolution-procedures-3-4) → [Part 3](./21-config-conflict-resolution-part3-procedures-3-4.md)
5. [Decision Trees, Examples, Troubleshooting](#decision-trees-examples-troubleshooting) → [Part 4](./21-config-conflict-resolution-part4-trees-examples-troubleshooting.md)

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

## Conflict Types and Resolution Strategies

**Full content:** [21-config-conflict-resolution-part1-types-strategies.md](./21-config-conflict-resolution-part1-types-strategies.md)

### Conflict Types Quick Reference

| Type | Name | Characteristics | Default Action |
|------|------|-----------------|----------------|
| A | Non-Breaking | Formatting, docs, comments | Adopt immediately |
| B | Breaking (Future) | Major versions, architecture | Defer to next task |
| C | Breaking (Immediate) | Security, compliance | Pause and adopt |
| D | Irreconcilable | Contradictory requirements | Escalate |

### Resolution Strategies Quick Reference

| Strategy | When to Use | Key Steps |
|----------|-------------|-----------|
| 1. Immediate Adoption | Type A, Type C | Update snapshot, apply, continue |
| 2. Deferred Adoption | Type B | Complete task, then adopt |
| 3. Immediate Restart | Type C critical | Pause, adopt, restart |
| 4. Escalate | Type D | Stop, report, await decision |

---

## Resolution Procedures 1-2

**Full content:** [21-config-conflict-resolution-part2-procedures-1-2.md](./21-config-conflict-resolution-part2-procedures-1-2.md)

### PROCEDURE 1: Resolve Non-Breaking Changes (Type A)

**When to use:**
- Type A conflict detected
- Changes are formatting/documentation only
- No code impact

**Steps summary:**
1. Verify change is non-breaking
2. Update config snapshot
3. Apply changes if needed
4. Log resolution
5. Continue work

### PROCEDURE 2: Resolve Breaking Changes - Future (Type B)

**When to use:**
- Type B conflict detected
- Breaking changes but not urgent
- Current task unaffected

**Steps summary:**
1. Assess impact on current task
2. Mark pending config update
3. Complete current task with snapshot config
4. After task completion, adopt new config
5. Update snapshot and resume

---

## Resolution Procedures 3-4

**Full content:** [21-config-conflict-resolution-part3-procedures-3-4.md](./21-config-conflict-resolution-part3-procedures-3-4.md)

### PROCEDURE 3: Resolve Breaking Changes - Immediate (Type C)

**When to use:**
- Type C conflict detected
- Security or compliance requirement
- Orchestrator mandates immediate adoption
- Critical bug fix

**Steps summary:**
1. Verify criticality
2. Pause current work
3. Log pause event
4. Adopt new config
5. Restart task with new config
6. Log restart
7. Report to orchestrator

### PROCEDURE 4: Resolve Irreconcilable Conflicts (Type D)

**When to use:**
- Type D conflict detected
- Cannot determine correct action
- Contradictory requirements
- Major architectural conflict

**Steps summary:**
1. Identify conflict
2. Stop work immediately
3. Document conflict
4. Generate resolution options
5. Report to orchestrator
6. Wait for orchestrator decision
7. Execute decision

---

## Decision Trees, Examples, Troubleshooting

**Full content:** [21-config-conflict-resolution-part4-trees-examples-troubleshooting.md](./21-config-conflict-resolution-part4-trees-examples-troubleshooting.md)

### Decision Tree 1: Initial Conflict Classification

```
Config change detected
└─ Is change breaking?
   ├─ NO → Type A → PROCEDURE 1
   └─ YES → Is critical/security?
            ├─ YES → Type C → PROCEDURE 3
            └─ NO → Affects current task?
                    ├─ NO → Type B → PROCEDURE 2
                    └─ YES → Compatible?
                             ├─ YES → Type B → PROCEDURE 2
                             └─ NO → Type D → PROCEDURE 4
```

### Decision Tree 2: Breaking Change Handling

```
Breaking change detected
└─ Check notification priority
   ├─ CRITICAL → PROCEDURE 3
   ├─ HIGH → Task affected?
   │         ├─ YES → PROCEDURE 3
   │         └─ NO → PROCEDURE 2
   └─ NORMAL → PROCEDURE 2
```

### Example Scenarios

| Scenario | Type | Resolution |
|----------|------|------------|
| Documentation clarification | A | Immediate adoption, continue |
| Python 3.11 → 3.12 | B | Complete task, then adopt |
| CVE security fix | C | Pause, adopt, restart |
| React → Vue framework change | D | Stop, escalate, await decision |

### Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| Cannot determine if breaking | Assume Type B, defer adoption |
| Immediate adoption fails | Rollback, classify as Type D, escalate |

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Target Audience:** Atlas Orchestrator Agents
**Related:** SKILL.md (PROCEDURE 9: Handle Config Version Conflicts)
