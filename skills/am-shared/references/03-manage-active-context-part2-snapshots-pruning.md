# Context Snapshots and Pruning

This document covers creating context snapshots and pruning old content from active context.

**Parent document**: [03-manage-active-context.md](./03-manage-active-context.md)

---

## Table of Contents
1. [When to Create Snapshots](#when-to-create-snapshots)
2. [Snapshot Procedure](#snapshot-procedure)
3. [When to Prune](#when-to-prune)
4. [Pruning Procedure](#pruning-procedure)
5. [Safe Pruning Checklist](#safe-pruning-checklist)

---

## When to Create Snapshots

Create context snapshots:
- Before major context updates
- Before compaction (mandatory)
- After resolving complex questions
- At user request
- When context reaches size threshold

---

## Snapshot Procedure

```bash
#!/bin/bash
# create_context_snapshot.sh - Create timestamped context snapshot

create_context_snapshot() {
    local timestamp=$(date -u +"%Y%m%d_%H%M%S")
    local snapshot_file=".session_memory/active_context/context_$timestamp.md"
    local source_file=".session_memory/active_context.md"

    # Copy current context
    cp "$source_file" "$snapshot_file"

    # Update symlink to latest
    ln -sf "context_$timestamp.md" .session_memory/active_context/context_latest.md

    echo "✓ Context snapshot created: $snapshot_file"

    # Keep only last 10 snapshots
    cd .session_memory/active_context
    ls -t context_*.md | tail -n +11 | xargs rm -f 2>/dev/null || true

    echo "✓ Old snapshots cleaned up"
}

create_context_snapshot
```

---

## When to Prune

Prune context when:
- File size exceeds 500 lines
- Contains decisions older than 7 days
- Contains resolved questions
- Before compaction
- Context feels cluttered

---

## Pruning Procedure

```bash
#!/bin/bash
# prune_context.sh - Remove stale content from active context

prune_context() {
    local context_file=".session_memory/active_context.md"

    # Create snapshot before pruning
    create_context_snapshot

    echo "Pruning context..."

    # Archive old decisions to patterns
    # Keep only last 7 days of decisions
    cutoff_date=$(date -u -d "7 days ago" +"%Y-%m-%d" 2>/dev/null || date -u -v-7d +"%Y-%m-%d")

    echo "Cutoff date: $cutoff_date"
    echo "Decisions older than this will be archived"

    # Manual pruning checklist:
    echo "Pruning checklist:"
    echo "1. ✓ Snapshot created"
    echo "2. [ ] Remove resolved questions from Open Questions"
    echo "3. [ ] Archive decisions older than $cutoff_date to patterns/"
    echo "4. [ ] Remove outdated context notes"
    echo "5. [ ] Consolidate duplicate information"
    echo "6. [ ] Update timestamp"

    echo "⚠ Manual pruning required - automated pruning risks losing important context"
}

prune_context
```

---

## Safe Pruning Checklist

Before pruning, verify:
- [ ] Snapshot created and verified
- [ ] No active tasks reference old decisions
- [ ] Old decisions archived to patterns (if reusable)
- [ ] Open questions actually resolved (not just removed)
- [ ] Context notes still relevant
