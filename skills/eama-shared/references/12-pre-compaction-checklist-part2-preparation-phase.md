# Pre-Compaction Preparation Phase

This file contains scripts and procedures for the preparation phase of pre-compaction.

## Table of Contents
1. [Context Preparation Script](#step-1-context-preparation)
2. [Pattern Extraction Script](#step-2-pattern-extraction)
3. [Progress Review Script](#step-3-progress-review)

---

## Step 1: Context Preparation

```bash
#!/bin/bash
# prepare_context.sh - Prepare context for compaction

prepare_context() {
    echo "=== Context Preparation ==="
    echo ""

    # Check current focus is documented
    echo "Check: Current focus documented..."
    if grep -q "^## Current Focus" .session_memory/active_context.md && \
       ! grep -A 5 "^## Current Focus" .session_memory/active_context.md | grep -q "\[To be filled\]"; then
        echo "✓ Current focus documented"
    else
        echo "✗ Current focus needs update"
        return 1
    fi

    # Check decisions recorded
    echo ""
    echo "Check: Recent decisions recorded..."
    if grep -q "^## Recent Decisions" .session_memory/active_context.md; then
        decision_count=$(grep "^### Decision:" .session_memory/active_context.md | wc -l)
        echo "✓ $decision_count decision(s) recorded"
    else
        echo "⚠ No decisions section found"
    fi

    # Check open questions
    echo ""
    echo "Check: Open questions documented..."
    if grep -q "^## Open Questions" .session_memory/active_context.md; then
        question_count=$(grep "^### Q:" .session_memory/active_context.md | wc -l)
        echo "✓ $question_count open question(s) documented"
    else
        echo "⚠ No open questions section found"
    fi

    echo ""
    echo "✓ Context preparation check complete"
}

prepare_context
```

---

## Step 2: Pattern Extraction

```bash
#!/bin/bash
# extract_patterns.sh - Extract patterns before compaction

extract_patterns() {
    echo "=== Pattern Extraction ==="
    echo ""

    # Review context for patterns
    echo "Review context for extractable patterns..."
    echo ""
    echo "Look for:"
    echo "1. Problems solved (Problem-Solution patterns)"
    echo "2. Effective procedures (Workflow patterns)"
    echo "3. Important decisions (Decision-Logic patterns)"
    echo "4. Error recoveries (Error-Recovery patterns)"
    echo ""

    # Count existing patterns
    pattern_count=$(find .session_memory/patterns -name "*.md" -type f | wc -l)
    echo "Current pattern count: $pattern_count"
    echo ""

    # Prompt for pattern extraction
    echo "Manual review required:"
    echo "1. Read through active_context.md"
    echo "2. Identify reusable knowledge"
    echo "3. Create pattern files for each"
    echo "4. Update pattern index"
    echo ""

    read -p "Patterns extracted and index updated? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "✓ Pattern extraction complete"
        return 0
    else
        echo "✗ Pattern extraction incomplete"
        return 1
    fi
}

extract_patterns
```

---

## Step 3: Progress Review

```bash
#!/bin/bash
# review_progress.sh - Review progress before compaction

review_progress() {
    echo "=== Progress Review ==="
    echo ""

    # Count tasks by status
    active=$(grep -c "^- \[ \].*In progress" .session_memory/progress_tracker.md 2>/dev/null || echo "0")
    completed=$(grep -c "^- \[x\]" .session_memory/progress_tracker.md 2>/dev/null || echo "0")
    blocked=$(grep -c "^- \[ \].*Blocked" .session_memory/progress_tracker.md 2>/dev/null || echo "0")

    echo "Active tasks: $active"
    echo "Completed tasks: $completed"
    echo "Blocked tasks: $blocked"
    echo ""

    # Check for critical work
    if [ "$active" -gt 0 ]; then
        echo "⚠ WARNING: $active active task(s)"
        echo "  Review active tasks before compaction"
        grep "^- \[ \]" .session_memory/progress_tracker.md | head -5
        echo ""
        read -p "Safe to proceed with active tasks? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return 1
        fi
    fi

    echo "✓ Progress review complete"
}

review_progress
```

---

## Preparation Phase Summary

The preparation phase ensures:

1. **Context is documented** - All current focus, decisions, and questions are recorded
2. **Patterns are extracted** - Valuable knowledge is saved to pattern files before context is compacted
3. **Progress is reviewed** - Active, completed, and blocked tasks are accounted for

**CRITICAL**: Do not proceed to the backup phase if any preparation step fails.
