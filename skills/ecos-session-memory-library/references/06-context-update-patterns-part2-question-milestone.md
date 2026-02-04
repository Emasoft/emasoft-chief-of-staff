# Context Update Patterns - Part 2: Question Addition and Progress Milestone

This document covers patterns for adding questions and recording progress milestones.

## Table of Contents

- [Pattern 3: Question Addition Update](#pattern-3-question-addition-update)
- [Pattern 4: Progress Milestone Update](#pattern-4-progress-milestone-update)

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

---

## Pattern 4: Progress Milestone Update

### When to Use

Use this pattern when:
- Completing major task or phase
- Reaching project milestone
- Finishing sprint or iteration
- Achieving significant goal

### Procedure

#### Step 1: Create Context Snapshot

```bash
# Snapshot current state
timestamp=$(date -u +"%Y%m%d_%H%M%S")
cp .session_memory/active_context.md ".session_memory/active_context/context_$timestamp.md"
cp .session_memory/progress_tracker.md ".session_memory/progress/progress_$timestamp.md"
```

#### Step 2: Update Progress Tracker

Move completed task:

```markdown
## Completed Tasks

- [x] [Task name]
  - **Started**: 2026-01-01 10:00 UTC
  - **Completed**: 2026-01-01 14:30 UTC
  - **Duration**: 4.5 hours
  - **Outcome**: [What was achieved]
  - **Learnings**: [What was learned]
```

#### Step 3: Update Active Context

Add to Recent Decisions:

```markdown
## Recent Decisions

### Milestone: [Milestone Name]
**Date**: 2026-01-01 14:30 UTC

**What Was Achieved**:
- Achievement 1
- Achievement 2

**Key Learnings**:
- Learning 1
- Learning 2

**Next Phase**:
[What comes next]
```

#### Step 4: Record Pattern (if reusable)

If milestone involved reusable knowledge, create pattern:

```bash
# Create workflow pattern for reusable procedures
./record_pattern.sh "workflow" "Task completion procedure"
```

### Complete Example

```bash
#!/bin/bash
# milestone_update.sh - Update context after milestone

milestone_update() {
    local milestone_name="$1"

    timestamp=$(date -u +"%Y%m%d_%H%M%S")
    timestamp_display=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

    # Create snapshots
    cp .session_memory/active_context.md ".session_memory/active_context/context_$timestamp.md"
    cp .session_memory/progress_tracker.md ".session_memory/progress/progress_$timestamp.md"

    # Add milestone to context
    cat >> .session_memory/active_context.md << EOF

### Milestone: $milestone_name
**Date**: $timestamp_display

**What Was Achieved**:
[To be filled]

**Key Learnings**:
[To be filled]

**Next Phase**:
[To be filled]

EOF

    echo "✓ Milestone snapshot created"
    echo "✓ Update context with milestone details"
}

milestone_update "Authentication System Complete"
```
