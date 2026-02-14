---
procedure: support-skill
workflow-instruction: support
operation: handle-config-conflicts
parent-skill: ecos-session-memory-library
---

# Operation: Handle Config Version Conflicts


## Contents

- [Purpose](#purpose)
- [When To Use This Operation](#when-to-use-this-operation)
- [Conflict Types](#conflict-types)
- [Steps](#steps)
  - [Step 1: Classify the Conflict](#step-1-classify-the-conflict)
- [Conflict Classification](#conflict-classification)
  - [Step 2A: Resolve Type A (Non-Breaking)](#step-2a-resolve-type-a-non-breaking)
- [Type A Resolution](#type-a-resolution)
  - [Step 2B: Resolve Type B (Breaking-Future)](#step-2b-resolve-type-b-breaking-future)
- [Type B Resolution](#type-b-resolution)
  - [Step 2C: Resolve Type C (Breaking-Immediate)](#step-2c-resolve-type-c-breaking-immediate)
- [Type C Resolution](#type-c-resolution)
  - [Step 2D: Resolve Type D (Irreconcilable)](#step-2d-resolve-type-d-irreconcilable)
- [Type D Resolution](#type-d-resolution)
  - [Step 3: Update Records](#step-3-update-records)
- [Decision Tree](#decision-tree)
- [Checklist](#checklist)
  - [For All Types](#for-all-types)
  - [For Type A](#for-type-a)
  - [For Type B](#for-type-b)
  - [For Type C](#for-type-c)
  - [For Type D](#for-type-d)
- [Output](#output)
- [Related References](#related-references)

## Purpose

Resolve conflicts when configuration changes during a session create incompatibilities with current work.

## When To Use This Operation

- When change detection reveals critical differences
- When high-priority config notifications arrive
- When current work becomes incompatible with new config
- When orchestrator requests resolution

## Conflict Types

| Type | Description | Response |
|------|-------------|----------|
| **Type A** | Non-Breaking | Adopt immediately |
| **Type B** | Breaking-Future | Complete task, then adopt |
| **Type C** | Breaking-Immediate | Pause, adopt, restart |
| **Type D** | Irreconcilable | Stop, escalate |

## Steps

### Step 1: Classify the Conflict

Determine conflict type based on:
- What changed
- Impact on current work
- Urgency of the change

```markdown
## Conflict Classification

Change: [description]
Current work impact: [none/minor/major/blocking]
Change urgency: [low/medium/high/critical]

Classification: Type [A/B/C/D]
```

### Step 2A: Resolve Type A (Non-Breaking)

Changes like formatting, documentation, comments.

1. Adopt new config immediately
2. Update config snapshot
3. Continue work
4. Log change

```markdown
## Type A Resolution

Action: Adopted immediately
Snapshot updated: [timestamp]
Work continues: Yes
```

### Step 2B: Resolve Type B (Breaking-Future)

Changes that will break future work but not current.

1. Continue current task to completion
2. After task completes, adopt new config
3. Update snapshot
4. Begin new work with new config

```markdown
## Type B Resolution

Action: Deferred adoption
Current task: [task-id]
Adoption scheduled: After task completion
```

### Step 2C: Resolve Type C (Breaking-Immediate)

Security patches, critical fixes that cannot wait.

1. **Pause current work immediately**
2. Save work state to memory files
3. Adopt new config
4. Update snapshot
5. Restart current work with new config

```markdown
## Type C Resolution

Action: Immediate adoption
Current task paused: [task-id]
Work state saved: [timestamp]
New config adopted: [timestamp]
Restarting with: [new config version]
```

### Step 2D: Resolve Type D (Irreconcilable)

Contradictory requirements that cannot be resolved automatically.

1. **Stop all work immediately**
2. Document the conflict
3. Notify manager (EAMA)
4. Wait for user decision

```markdown
## Type D Resolution

Action: Escalated to user
Work stopped: [timestamp]
Conflict: [description]
Notified: EAMA via [message-id]
Awaiting: User decision
```

### Step 3: Update Records

After resolution:

1. Update config-snapshot.md with new state
2. Update activeContext.md with resolution details
3. Log resolution in patterns.md if instructive

## Decision Tree

```
Change detected
  │
  ├─ Does change affect current work?
  │   └─ NO → Type A (adopt immediately)
  │
  ├─ Is change a security/critical fix?
  │   └─ YES → Type C (pause, adopt, restart)
  │
  ├─ Can current task complete first?
  │   └─ YES → Type B (complete task, then adopt)
  │
  └─ Are requirements contradictory?
      └─ YES → Type D (stop, escalate)
```

## Checklist

Copy this checklist and track your progress:

### For All Types
- [ ] Conflict detected and documented
- [ ] Conflict type classified
- [ ] Resolution strategy selected

### For Type A
- [ ] New config adopted
- [ ] Snapshot updated
- [ ] Work continues

### For Type B
- [ ] Current task noted
- [ ] Adoption scheduled
- [ ] Continue current work

### For Type C
- [ ] Work paused
- [ ] State saved
- [ ] New config adopted
- [ ] Snapshot updated
- [ ] Work restarted

### For Type D
- [ ] Work stopped
- [ ] Conflict documented
- [ ] EAMA notified
- [ ] Awaiting user decision

## Output

After completing this operation:
- Conflict resolved (or escalated)
- Config snapshot updated
- Records updated
- Work continues (or paused awaiting decision)

## Related References

- [21-config-conflict-resolution.md](21-config-conflict-resolution.md) - Complete conflict resolution guide
- [20-config-change-detection.md](20-config-change-detection.md) - Change detection
- [19-config-snapshot-creation.md](19-config-snapshot-creation.md) - Snapshot management
