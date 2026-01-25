# Context Update Patterns - Part 1: Task Switch and Decision Recording

This document covers the first two update patterns for context management.

## Pattern 1: Task Switch Update

### When to Use

Use this pattern when:
- Starting a new task
- Switching focus to different work
- Completing current task and moving to next
- Responding to priority change

### Procedure

#### Step 1: Create Context Snapshot

```bash
# Snapshot current context before switching
timestamp=$(date -u +"%Y%m%d_%H%M%S")
snapshot_file=".session_memory/active_context/context_$timestamp.md"

cp .session_memory/active_context.md "$snapshot_file"

# Update symlink
ln -sf "context_$timestamp.md" .session_memory/active_context/context_latest.md

echo "✓ Snapshot created: $snapshot_file"
```

#### Step 2: Archive Old Focus

Move old focus to Recent Decisions if work completed:

```markdown
## Recent Decisions

### Completed: [Old Task Name]
- **Completed**: 2026-01-01 14:30 UTC
- **Outcome**: [What was achieved]
- **Key Learnings**: [What was learned]
- **Next Steps**: [Any follow-up needed]
```

#### Step 3: Update Current Focus

```markdown
## Current Focus

**Updated**: 2026-01-01 14:35 UTC

### Primary Task
[New task name and description]

**Objectives**:
- Objective 1
- Objective 2

**Why This Task**:
[Rationale for switching to this task]

**Progress**:
- [ ] Subtask 1
- [ ] Subtask 2

**Next Steps**:
1. First immediate action
2. Second immediate action
```

#### Step 4: Update Timestamp

```markdown
**Last Updated**: 2026-01-01 14:35 UTC
**Compaction Count**: [current count]
```

#### Step 5: Verify Update

```bash
# Check file is valid
head -20 .session_memory/active_context.md

# Verify snapshot exists
ls -lh .session_memory/active_context/context_$timestamp.md
```

### Complete Example

```bash
#!/bin/bash
# task_switch.sh - Switch to new task with proper context update

task_switch() {
    local new_task="$1"
    local old_task="$2"

    # Step 1: Snapshot
    timestamp=$(date -u +"%Y%m%d_%H%M%S")
    cp .session_memory/active_context.md ".session_memory/active_context/context_$timestamp.md"
    ln -sf "context_$timestamp.md" .session_memory/active_context/context_latest.md

    # Step 2-4: Update context (manual edit recommended)
    echo "Context snapshot created"
    echo ""
    echo "Update checklist:"
    echo "1. [ ] Move '$old_task' to Recent Decisions"
    echo "2. [ ] Update Current Focus to '$new_task'"
    echo "3. [ ] Update timestamp"
    echo "4. [ ] List objectives and next steps"
    echo ""
    echo "Edit: .session_memory/active_context.md"
}

task_switch "Implement user authentication" "Fix test failures"
```

---

## Pattern 2: Decision Recording Update

### When to Use

Use this pattern when:
- Making important technical decision
- Choosing between alternatives
- Establishing precedent
- Making architectural choice

### Procedure

#### Step 1: Document Decision

```markdown
## Recent Decisions

### Decision: [Decision Name]
**Date**: 2026-01-01 14:30 UTC
**Impact**: High/Medium/Low

**What Was Decided**:
[Clear statement of decision]

**Rationale**:
[Why this decision was made]

**Alternatives Considered**:
1. Alternative 1 - [Why not chosen]
2. Alternative 2 - [Why not chosen]

**Impact Areas**:
- Area 1: [How affected]
- Area 2: [How affected]

**Dependencies**:
- Dependency 1
- Dependency 2
```

#### Step 2: Update Affected Sections

If decision affects current focus, update it:

```markdown
## Current Focus

[Existing focus]

**Recent Decision Impact**:
- Decision: [decision name]
- Changes to plan: [how plan changed]
- New next steps: [updated steps]
```

#### Step 3: Update Timestamp

```markdown
**Last Updated**: 2026-01-01 14:30 UTC
```

### Complete Example

```bash
#!/bin/bash
# record_decision.sh - Record important decision in context

record_decision() {
    local decision_name="$1"
    local rationale="$2"

    timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

    # Append to Recent Decisions section
    cat >> .session_memory/active_context.md << EOF

### Decision: $decision_name
**Date**: $timestamp
**Impact**: [To be filled]

**What Was Decided**:
[To be filled]

**Rationale**:
$rationale

**Alternatives Considered**:
[To be filled]

**Impact Areas**:
[To be filled]

EOF

    echo "✓ Decision added to context - complete details manually"
}

record_decision "Use JWT tokens" "Better API and mobile support"
```
