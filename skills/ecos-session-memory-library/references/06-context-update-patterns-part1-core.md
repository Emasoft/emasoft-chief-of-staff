# Context Update Patterns - Part 1: Core Patterns

## Table of Contents
1. [When you need to understand the purpose](#purpose)
2. [Understanding update patterns overview](#update-patterns-overview)
3. [When switching tasks](#pattern-1-task-switch-update)
4. [When recording decisions](#pattern-2-decision-recording-update)
5. [When adding questions](#pattern-3-question-addition-update)

**See Also**: [Part 2: Advanced Patterns](06-context-update-patterns-part2-advanced.md) for:
- Pattern 4: Progress Milestone Update
- Pattern 5: Pre-Compaction Update
- Combined Examples
- Troubleshooting

## Purpose

Context update patterns provide standardized workflows for common context modification scenarios. Using these patterns ensures:
- Consistent context structure
- Complete information capture
- Proper snapshot creation
- Index maintenance
- Recovery capability

## Update Patterns Overview

| Pattern | When to Use | Snapshot Required | Index Update |
|---------|-------------|-------------------|--------------|
| Task Switch | Changing primary focus | Yes | No |
| Decision Recording | Making important decision | No | No |
| Question Addition | Adding blocker/question | No | No |
| Progress Milestone | Completing major task | Yes | Maybe |
| Pre-Compaction | Before compaction | Yes (mandatory) | Yes |

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

## Pattern 3: Question Addition Update

### When to Use

Use this pattern when:
- Encountering a blocker
- Need external input
- Waiting on decision
- Facing unclear requirements

### Procedure

#### Step 1: Add to Open Questions

```markdown
## Open Questions

### Q: [Clear question]?
**Added**: 2026-01-01 14:30 UTC
**Priority**: High/Medium/Low

**Why Important**:
[Explanation of significance]

**Blocked Work**:
- Task 1
- Task 2

**Needs Input From**:
[Who can answer]

**Context**:
[Additional context for answerer]
```

#### Step 2: Mark Blocked Tasks

Update progress tracker:

```markdown
## Blocked Tasks

- [ ] Task name - Blocked by Q: [question reference]
  - **Question**: [Link to question in active_context.md]
  - **Blocking Since**: 2026-01-01 14:30 UTC
```

#### Step 3: Update Timestamp

```markdown
**Last Updated**: 2026-01-01 14:30 UTC
```

### Complete Example

```bash
#!/bin/bash
# add_question.sh - Add open question to context

add_question() {
    local question="$1"
    local importance="$2"
    local blocked="$3"

    timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

    cat >> .session_memory/active_context.md << EOF

### Q: $question
**Added**: $timestamp
**Priority**: High

**Why Important**:
$importance

**Blocked Work**:
- $blocked

**Needs Input From**:
[To be filled]

EOF

    # Update progress tracker to mark blocked task
    cat >> .session_memory/progress_tracker.md << EOF

## Blocked Tasks

- [ ] $blocked - Blocked by Q: $question
  - **Blocking Since**: $timestamp

EOF

    echo "✓ Question added - update progress tracker if needed"
}

add_question "Should tokens expire in 1h or 24h?" "Security vs UX tradeoff" "Token refresh implementation"
```
