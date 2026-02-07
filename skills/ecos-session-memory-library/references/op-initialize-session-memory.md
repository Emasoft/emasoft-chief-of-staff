---
procedure: support-skill
workflow-instruction: support
operation: initialize-session-memory
parent-skill: ecos-session-memory-library
---

# Operation: Initialize Session Memory

## Purpose

Create or load session memory files at session start to enable persistence across interactions and context compaction.

## When To Use This Operation

- At the start of every new session
- After context compaction
- When resuming after interruption
- When memory files need recreation

## Session Memory Components

| File | Purpose | Location |
|------|---------|----------|
| activeContext.md | Current work state | design/memory/ |
| patterns.md | Learned patterns | design/memory/ |
| progress.md | Task tracking | design/memory/ |

## Steps

### Step 1: Check Directory Exists

```bash
MEMORY_DIR="$CLAUDE_PROJECT_DIR/design/memory"

if [ ! -d "$MEMORY_DIR" ]; then
  mkdir -p "$MEMORY_DIR"
  echo "Created memory directory"
fi
```

### Step 2: Read or Create Memory Files

For each memory file:

**activeContext.md:**
```markdown
# Active Context

Last Updated: [ISO8601]
Session ID: [session-id]

## Current Focus
- **Active Task:** None
- **Working On:** Session initialization

## Open Questions
- None

## Recent Decisions
- None

## Session Notes
- Session started at [timestamp]
```

**patterns.md:**
```markdown
# Discovered Patterns

Last Updated: [ISO8601]

## Index
- None yet

## Patterns
(Patterns will be added as they are discovered)
```

**progress.md:**
```markdown
# Task Progress

Last Updated: [ISO8601]

## Active Tasks
- None

## Completed Tasks
- None

## Blocked Tasks
- None
```

### Step 3: Validate Markdown Syntax

Verify each file:
- Valid Markdown structure
- Required sections present
- No syntax errors

```bash
# Simple validation - check required sections exist
grep -q "## Current Focus" "$MEMORY_DIR/activeContext.md" || echo "Missing section in activeContext.md"
grep -q "## Index" "$MEMORY_DIR/patterns.md" || echo "Missing section in patterns.md"
grep -q "## Active Tasks" "$MEMORY_DIR/progress.md" || echo "Missing section in progress.md"
```

### Step 4: Report Loaded State

```markdown
## Session Memory Initialized

- activeContext.md: [loaded/created]
- patterns.md: [loaded/created]
- progress.md: [loaded/created]

Current Focus: [from activeContext.md]
Active Tasks: [count from progress.md]
Patterns: [count from patterns.md]
```

## Checklist

Copy this checklist and track your progress:

- [ ] Memory directory exists or created
- [ ] activeContext.md loaded or created
- [ ] patterns.md loaded or created
- [ ] progress.md loaded or created
- [ ] All files validated for Markdown syntax
- [ ] Session state reported
- [ ] Ready to begin work

## Output

After completing this operation:
- All three memory files exist and are valid
- Current state loaded into session
- Ready for normal operations

## Directory Structure

```
design/
  memory/
    activeContext.md    # Current work state
    patterns.md         # Learned patterns
    progress.md         # Task tracking
    config-snapshot.md  # Config state (optional)
    archive/            # Archived old data
```

## Related References

- [01-initialize-session-memory.md](01-initialize-session-memory.md) - Complete initialization guide
- [02-memory-directory-structure.md](02-memory-directory-structure.md) - Directory structure details
- [04-memory-validation.md](04-memory-validation.md) - Validation procedures

## Next Operation

After initialization: [op-update-active-context.md](op-update-active-context.md) (when work begins)
