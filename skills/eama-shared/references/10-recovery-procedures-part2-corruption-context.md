# Recovery from Corrupted Memory and Lost Context

**Parent Document**: [10-recovery-procedures.md](10-recovery-procedures.md)

## Table of Contents

1. [Recovery from Corrupted Memory](#recovery-from-corrupted-memory)
   - [Scenario](#corrupted-scenario)
   - [Symptoms](#corrupted-symptoms)
   - [Recovery Procedure](#corrupted-recovery-procedure)
2. [Recovery from Lost Context](#recovery-from-lost-context)
   - [Scenario](#lost-context-scenario)
   - [Symptoms](#lost-context-symptoms)
   - [Recovery Procedure](#lost-context-recovery-procedure)

---

## Recovery from Corrupted Memory

### Corrupted Scenario

One or more memory files corrupted (invalid markdown, truncated, encoding issues).

**When this happens:**
- File write interrupted (crash, disk full)
- Encoding issues from copy/paste
- Concurrent write attempts
- Disk errors

**Severity**: Medium
**Recovery Time**: 2-5 minutes
**Data Loss Risk**: Low (snapshots usually available)

### Corrupted Symptoms

How to recognize corrupted files:

- Cannot read file (read errors)
- Markdown syntax errors (broken headers, unclosed blocks)
- Truncated content (file ends mid-sentence)
- Special characters/encoding issues (garbage characters)
- File size unexpectedly small or zero

### Corrupted Recovery Procedure

```bash
#!/bin/bash
# recover_corrupted_file.sh - Restore corrupted file from snapshot

recover_corrupted_file() {
    local corrupted_file="$1"
    local file_basename=$(basename "$corrupted_file")

    echo "=== Recovering Corrupted File ==="
    echo "File: $corrupted_file"

    # Backup corrupted version for analysis
    backup_file="${corrupted_file}.corrupted.$(date +%Y%m%d_%H%M%S)"
    cp "$corrupted_file" "$backup_file" 2>/dev/null || true
    echo "Corrupted version backed up: $backup_file"

    # Find replacement based on file type
    case "$file_basename" in
        "active_context.md")
            # Restore from context snapshot
            latest_snapshot=$(ls -t .session_memory/active_context/context_*.md 2>/dev/null | head -1)
            if [ -n "$latest_snapshot" ]; then
                cp "$latest_snapshot" "$corrupted_file"
                echo "Restored from: $latest_snapshot"
            else
                echo "No snapshot available"
                return 1
            fi
            ;;

        "progress_tracker.md")
            # Restore from progress snapshot
            latest_snapshot=$(ls -t .session_memory/progress/progress_*.md 2>/dev/null | head -1)
            if [ -n "$latest_snapshot" ]; then
                cp "$latest_snapshot" "$corrupted_file"
                echo "Restored from: $latest_snapshot"
            else
                echo "No snapshot available"
                return 1
            fi
            ;;

        "pattern_index.md")
            # Rebuild from pattern files
            echo "Rebuilding pattern index from files..."
            ./rebuild_pattern_index.sh
            echo "Pattern index rebuilt"
            ;;

        *)
            echo "Unknown file type: $file_basename"
            return 1
            ;;
    esac

    # Validate restored file
    if [ -f "$corrupted_file" ] && [ -r "$corrupted_file" ]; then
        echo "File restored and readable"
        return 0
    else
        echo "Restoration failed"
        return 1
    fi
}

# Usage:
# recover_corrupted_file ".session_memory/active_context.md"
```

**What this does:**
1. Backs up corrupted file for later analysis
2. Identifies file type and appropriate recovery source
3. Restores from snapshot or rebuilds from source files
4. Validates the restored file is readable

---

### Pattern Index Rebuild Script

When pattern_index.md is corrupted, rebuild from pattern files:

```bash
#!/bin/bash
# rebuild_pattern_index.sh - Rebuild pattern index from individual pattern files

rebuild_pattern_index() {
    echo "=== Rebuilding Pattern Index ==="

    local output_file=".session_memory/pattern_index.md"
    local patterns_dir=".session_memory/patterns"

    # Start fresh index
    cat > "$output_file" << 'EOF'
# Pattern Index

**Last Rebuilt**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Status**: Rebuilt from pattern files

## Patterns by Category

EOF

    # Process each category directory
    for category_dir in "$patterns_dir"/*/; do
        if [ -d "$category_dir" ]; then
            category=$(basename "$category_dir")
            echo "### $category" >> "$output_file"
            echo "" >> "$output_file"

            # List patterns in category
            for pattern_file in "$category_dir"/*.md; do
                if [ -f "$pattern_file" ]; then
                    pattern_name=$(basename "$pattern_file" .md)
                    # Extract first line as description
                    description=$(head -1 "$pattern_file" | sed 's/^# //')
                    echo "- [$pattern_name]($pattern_file): $description" >> "$output_file"
                fi
            done
            echo "" >> "$output_file"
        fi
    done

    echo "Pattern index rebuilt with $(find "$patterns_dir" -name "*.md" | wc -l) patterns"
}

rebuild_pattern_index
```

---

## Recovery from Lost Context

### Lost Context Scenario

Context information lost but structure intact (accidental deletion, overwrite, etc.).

**When this happens:**
- Accidental file deletion
- Overwrite with empty content
- Reset to template state
- Failed update operation

**Severity**: Medium
**Recovery Time**: 5-10 minutes
**Data Loss Risk**: Medium (depends on snapshot availability)

### Lost Context Symptoms

How to recognize lost context:

- Empty or minimal context file
- Only template/boilerplate content
- Missing recent decisions
- Missing open questions
- Missing current focus

### Lost Context Recovery Procedure

```bash
#!/bin/bash
# recover_lost_context.sh - Reconstruct context from available sources

recover_lost_context() {
    echo "=== Recovering Lost Context ==="

    # Step 1: Check for snapshots
    echo "Step 1: Checking for context snapshots..."
    latest_snapshot=$(ls -t .session_memory/active_context/context_*.md 2>/dev/null | head -1)

    if [ -n "$latest_snapshot" ]; then
        echo "Found snapshot: $latest_snapshot"
        cp "$latest_snapshot" .session_memory/active_context.md
        echo "Context restored from snapshot"
    else
        echo "No snapshot available - attempting reconstruction"

        # Step 2: Reconstruct from progress tracker
        echo "Step 2: Reconstructing from progress tracker..."

        cat > .session_memory/active_context.md << 'EOF'
# Active Context

**Last Updated**: [RECONSTRUCTED]
**Status**: Recovered from progress tracker

## Current Focus

[Review progress tracker for active tasks]

## Recent Decisions

[To be filled from memory or git history]

## Open Questions

[Check progress tracker for blocked tasks]

## Context Notes

**Recovery Note**: Context lost and reconstructed from available sources.
Review and update with current information.

EOF

        echo "Minimal context created - manual update required"
    fi

    # Step 3: Mine information from other sources
    echo "Step 3: Mining additional information..."

    # Check git history for recent activity
    if git rev-parse --git-dir > /dev/null 2>&1; then
        echo "Recent git commits:"
        git log --oneline -10 2>/dev/null || true
    fi

    # Check for pattern files (might contain context)
    recent_patterns=$(ls -t .session_memory/patterns/*/*.md 2>/dev/null | head -5)
    if [ -n "$recent_patterns" ]; then
        echo "Recent patterns recorded:"
        echo "$recent_patterns"
    fi

    echo ""
    echo "=== Recovery Actions Required ==="
    echo "1. Review reconstructed context"
    echo "2. Fill in current focus from progress tracker"
    echo "3. Add recent decisions from memory/notes"
    echo "4. Update open questions from blocked tasks"
    echo "5. Create new snapshot of reconstructed context"
}

recover_lost_context
```

**What this does:**
1. Attempts to restore from snapshot
2. If no snapshot, creates minimal structure
3. Mines git history for recent context
4. Lists recent patterns that might provide context
5. Provides action items for manual completion

---

## Source Mining Techniques

When snapshots are unavailable, mine context from other sources:

### Mining from Git History

```bash
#!/bin/bash
# mine_git_context.sh - Extract context from git history

echo "=== Mining Context from Git History ==="

# Recent commits with messages
echo "Recent commits:"
git log --oneline -20

# Files changed recently
echo ""
echo "Recently changed files:"
git diff --stat HEAD~10

# Commit messages for context
echo ""
echo "Detailed commit messages (last 5):"
git log -5 --format="---
%h: %s
%b"
```

### Mining from Documentation

```bash
#!/bin/bash
# mine_docs_context.sh - Extract context from documentation

echo "=== Mining Context from Documentation ==="

# Check for project documentation
if [ -d "docs" ] || [ -d "docs_dev" ]; then
    echo "Documentation files:"
    find docs docs_dev -name "*.md" -type f 2>/dev/null | head -20

    # Look for progress/status files
    echo ""
    echo "Progress-related documentation:"
    find docs docs_dev -name "*progress*" -o -name "*status*" -o -name "*task*" 2>/dev/null
fi

# Check for TODO files
if [ -f "TODO.md" ] || [ -f "TODO" ]; then
    echo ""
    echo "TODO file found - may contain current tasks"
fi
```

### Mining from Pattern Files

```bash
#!/bin/bash
# mine_patterns_context.sh - Extract context from recorded patterns

echo "=== Mining Context from Patterns ==="

# Recent patterns
echo "Most recent patterns:"
ls -lt .session_memory/patterns/*/*.md 2>/dev/null | head -10

# Decision patterns specifically
echo ""
echo "Recent decision patterns:"
ls -lt .session_memory/patterns/decision/*.md 2>/dev/null | head -5

# Problem patterns (might indicate current issues)
echo ""
echo "Recent problem patterns:"
ls -lt .session_memory/patterns/problem/*.md 2>/dev/null | head -5
```

---

## Quick Reference Checklist

### For Corrupted Files:

```
[ ] 1. Identify corrupted file
[ ] 2. Backup corrupted version
[ ] 3. Find appropriate snapshot
[ ] 4. Restore from snapshot
[ ] 5. Validate restored file
[ ] 6. Document recovery
```

### For Lost Context:

```
[ ] 1. Check for snapshots
[ ] 2. Restore or create minimal context
[ ] 3. Mine git history
[ ] 4. Mine documentation
[ ] 5. Mine pattern files
[ ] 6. Manually update context
[ ] 7. Create new snapshot
[ ] 8. Document recovery
```

---

## Related Documents

- [10-recovery-procedures.md](10-recovery-procedures.md) - Main recovery index
- [Part 1: Failed Compaction](10-recovery-procedures-part1-failed-compaction.md) - Compaction recovery
- [Part 3: Emergency Recovery](10-recovery-procedures-part3-snapshot-emergency.md) - Complete memory loss
- [Part 4a: Examples](10-recovery-procedures-part4a-examples.md) - Complete workflow examples
- [Part 4b: Troubleshooting](10-recovery-procedures-part4b-troubleshooting.md) - Common problems and solutions
