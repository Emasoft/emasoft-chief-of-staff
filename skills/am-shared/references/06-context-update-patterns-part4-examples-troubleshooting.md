# Context Update Patterns - Part 4: Examples and Troubleshooting

This document provides combined examples and troubleshooting guidance.

## Examples

### Example 1: Combined Update - Task Switch with Decision

```bash
# Switching tasks after making decision

# 1. Create snapshot
timestamp=$(date -u +"%Y%m%d_%H%M%S")
cp .session_memory/active_context.md ".session_memory/active_context/context_$timestamp.md"

# 2. Record decision about completed task
cat >> .session_memory/active_context.md << 'EOF'

### Decision: Completed testing approach selection
**Date**: 2026-01-01 14:30 UTC
**Outcome**: Selected Jest over Mocha for better TypeScript support

EOF

# 3. Archive old focus
# (Move to Recent Decisions)

# 4. Update to new focus
cat > .session_memory/active_context.md << 'EOF'
# Active Context

**Last Updated**: 2026-01-01 14:35 UTC

## Current Focus

### Primary Task
Implement user authentication system

[Rest of context...]
EOF
```

### Example 2: Milestone with Pattern Recording

```bash
# Completed milestone, record reusable pattern

# 1. Snapshot
timestamp=$(date -u +"%Y%m%d_%H%M%S")
cp .session_memory/active_context.md ".session_memory/active_context/context_$timestamp.md"
cp .session_memory/progress_tracker.md ".session_memory/progress/progress_$timestamp.md"

# 2. Record pattern
./record_pattern.sh "workflow" "parallel-testing-setup"

# 3. Update context with milestone
cat >> .session_memory/active_context.md << 'EOF'

### Milestone: Testing Infrastructure Complete
**Date**: 2026-01-01 15:00 UTC

**Achievements**:
- Parallel test execution working
- Test time reduced from 30min to 8min
- Pattern recorded for future use

**Pattern**: wf_001 - Parallel testing workflow

EOF
```

---

## Troubleshooting

### Problem: Forgot to Create Snapshot Before Update

**Solution**:
```bash
# If changes not yet made, create snapshot now
timestamp=$(date -u +"%Y%m%d_%H%M%S")
cp .session_memory/active_context.md ".session_memory/active_context/context_$timestamp.md"

# If changes already made, check git
git diff .session_memory/active_context.md  # If in git
# Or check for .bak files
```

### Problem: Context Update Interrupted

**Solution**:
```bash
# Restore from latest snapshot
latest_snapshot=$(ls -t .session_memory/active_context/context_*.md | head -1)
cp "$latest_snapshot" .session_memory/active_context.md

# Resume update
```

### Problem: Multiple Updates Needed Simultaneously

**Solution**:
```bash
# Create snapshot once
timestamp=$(date -u +"%Y%m%d_%H%M%S")
cp .session_memory/active_context.md ".session_memory/active_context/context_$timestamp.md"

# Make all updates
# 1. Update focus
# 2. Record decision
# 3. Add question
# etc.

# Update timestamp once at end
```

### Problem: Pre-Compaction Validation Fails

**Solution**:
```bash
# DO NOT PROCEED with compaction
# Fix validation errors first

# Run detailed validation
./validate_all.sh

# Address each error
# Re-run validation
# Only proceed when all checks pass
```
