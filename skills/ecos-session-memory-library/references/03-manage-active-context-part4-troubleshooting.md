# Active Context Troubleshooting

This document covers common problems and solutions for active context management.

**Parent document**: [03-manage-active-context.md](./03-manage-active-context.md)

---

## Table of Contents
1. [Problem: Context File Too Large](#problem-context-file-too-large)
2. [Problem: Lost Context After Compaction](#problem-lost-context-after-compaction)
3. [Problem: Duplicate Information in Context](#problem-duplicate-information-in-context)
4. [Problem: Cannot Find Recent Decision](#problem-cannot-find-recent-decision)
5. [Problem: Open Questions Never Get Resolved](#problem-open-questions-never-get-resolved)
6. [Problem: Context Updates Conflict with Active Work](#problem-context-updates-conflict-with-active-work)

---

## Problem: Context File Too Large

**Symptoms**: active_context.md exceeds 500 lines, slow to read/update

**Solution**:
```bash
# Create snapshot
create_context_snapshot

# Archive old decisions to patterns
# Keep only recent (last 3 days) decisions in active context
# Move older decisions to .session_memory/patterns/decision_logic/
```

---

## Problem: Lost Context After Compaction

**Cause**: No snapshot created before compaction

**Solution**:
```bash
# Check for archived pre-compaction state
ls .session_memory/archived/pre_compaction_*/

# Restore from most recent archive
latest_archive=$(ls -t .session_memory/archived/pre_compaction_* | head -1)
cp "$latest_archive/active_context.md" .session_memory/active_context.md
```

---

## Problem: Duplicate Information in Context

**Cause**: Information added multiple times without cleanup

**Solution**:
```bash
# Manual review required
# 1. Read through active_context.md
# 2. Identify duplicates
# 3. Consolidate information
# 4. Remove redundant entries
# 5. Update timestamp
```

---

## Problem: Cannot Find Recent Decision

**Cause**: Decision archived or lost during pruning

**Solution**:
```bash
# Search in context snapshots
grep -r "decision keyword" .session_memory/active_context/

# Search in archived states
grep -r "decision keyword" .session_memory/archived/

# Search in patterns
grep -r "decision keyword" .session_memory/patterns/
```

---

## Problem: Open Questions Never Get Resolved

**Cause**: No process for tracking question resolution

**Solution**:
```markdown
## Open Questions

### Q: Question text?
**Added**: [date]
**Importance**: [why it matters]
**Blocked**: [what's blocked]
**Status**: Open
**Follow-up**: Review on [specific date or milestone]
**Assigned**: [who is responsible for answering]
```

---

## Problem: Context Updates Conflict with Active Work

**Cause**: Trying to update context file while it's being read by another process

**Solution**:
```bash
# Use atomic updates with temp file
temp_file=$(mktemp)
cp .session_memory/active_context.md "$temp_file"

# Make changes to temp file
# ... editing ...

# Atomic move
mv "$temp_file" .session_memory/active_context.md
```
