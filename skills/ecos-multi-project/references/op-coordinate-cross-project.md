---
name: op-coordinate-cross-project
description: Operation procedure for coordinating work across multiple projects with dependencies.
workflow-instruction: "support"
procedure: "support-skill"
---

# Operation: Coordinate Cross-Project Work

## Purpose

Manage work that spans multiple projects, handling dependencies, sequencing, and synchronization between project boundaries.

## When to Use

- When changes in one project depend on changes in another
- When releasing coordinated updates across projects
- When sharing resources (agents, services) between projects
- When managing a multi-repo feature or migration

## Prerequisites

- All involved projects registered in project registry
- Understanding of dependency relationships
- Agents available for coordination
- AI Maestro messaging for cross-agent communication

## Procedure

### Step 1: Map Project Dependencies

```markdown
## Dependency Map

### Projects Involved
1. Project A (upstream)
2. Project B (depends on A)
3. Project C (depends on A and B)

### Dependency Graph
```
A ──┬──► B ──┐
    │        ├──► C
    └────────┘
```

### Blocking Dependencies
- C cannot start until A and B complete
- B cannot start until A completes
```

### Step 2: Create Cross-Project Issues

In each project, create linked issues:

```bash
# In Project A
gh issue create --repo $PROJECT_A_REPO \
  --title "[Cross-Project] Component A for Feature X" \
  --body "Part of cross-project feature X.

**Downstream:** Blocks work in Project B and C.
**Coordination:** See tracking issue in main project." \
  --label "type:feature" \
  --label "cross-project"

# Get issue number
A_ISSUE=$?
```

Repeat for Projects B and C with appropriate references.

### Step 3: Create Coordination Tracking

Create a coordination document or issue:

```bash
gh issue create --repo $MAIN_PROJECT_REPO \
  --title "[Coordination] Cross-Project Feature X" \
  --body "## Cross-Project Coordination

### Dependencies
- [ ] Project A #$A_ISSUE - Must complete first
- [ ] Project B #$B_ISSUE - Depends on A
- [ ] Project C #$C_ISSUE - Depends on A and B

### Checkpoints
- [ ] Checkpoint 1: A stable (after A complete)
- [ ] Checkpoint 2: B stable (after B complete)
- [ ] Checkpoint 3: C stable (after all complete)

### Communication
- ECOS coordinates
- Agents communicate via AI Maestro
- Status updates in this issue" \
  --label "coordination" \
  --label "priority:high"
```

### Step 4: Sequence Work Execution

```bash
# Phase 1: Start Project A
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "eoa-main",
    "subject": "Start cross-project work: Project A",
    "priority": "high",
    "content": {
      "type": "task-assignment",
      "message": "Begin work on Project A component for Feature X. Notify ECOS when complete.",
      "project": "project-a",
      "issue": '$A_ISSUE'
    }
  }'
```

### Step 5: Monitor Checkpoints

```bash
# Wait for Phase 1 completion
# When notified of A completion, verify:
gh issue view $A_ISSUE --repo $PROJECT_A_REPO --json state
# Should be: closed or labeled "done"

# Start Phase 2 (Project B)
# ... similar messaging
```

### Step 6: Reconcile States

After all phases complete:

```bash
# Update coordination issue
gh issue comment $COORDINATION_ISSUE --body "## Cross-Project Complete

All phases completed:
- [x] Project A - $(date)
- [x] Project B - $(date)
- [x] Project C - $(date)

Feature X is ready for integration testing."

# Update project registries
for PROJECT in project-a project-b project-c; do
  jq '.projects["'"$PROJECT"'"].last_cross_project = "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"' .emasoft/project-registry.json > temp.json && mv temp.json .emasoft/project-registry.json
done
```

## Example

**Scenario:** Coordinate PSS, CPV, and EPM marketplace update.

```markdown
## Cross-Project Coordination Plan

### Projects Involved
1. claude-plugins-validation (CPV) - validation logic
2. perfect-skill-suggester (PSS) - uses CPV
3. emasoft-plugins-marketplace (EPM) - contains both as submodules

### Dependency Chain
CPV → PSS → EPM

### Execution Steps
1. Update CPV validation logic
2. Run CPV tests (blocking checkpoint)
3. Update PSS to use new CPV
4. Run PSS tests (blocking checkpoint)
5. Update EPM submodules to latest
6. Run marketplace validation (final checkpoint)
7. Publish updates

### Checkpoints
- After step 2: CPV stable
- After step 4: PSS stable
- After step 6: EPM stable
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Circular dependency | Bad dependency mapping | Refactor to break cycle |
| Checkpoint timeout | Downstream project slow | Escalate, consider parallel work |
| State inconsistency | Partial updates | Roll back to last checkpoint |
| Agent unavailable | Resource constraints | Reassign or queue work |

## Notes

- Document all dependencies explicitly upfront
- Use checkpoints to verify stable states
- Communicate actively between project agents
- Have rollback plan for each phase
- Track coordination in dedicated issue for visibility
