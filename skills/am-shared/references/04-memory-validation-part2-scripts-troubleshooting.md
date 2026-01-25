# Memory Validation - Part 2: Scripts, Checklists, and Troubleshooting

## Table of Contents
1. [Using the master validation script](#master-validation-script)
2. [How to follow validation checklist](#validation-checklist)
3. [Quick pre-compaction validation example](#example-1-quick-pre-compaction-validation)
4. [Validation with auto-repair example](#example-2-validation-with-auto-repair)
5. [Validation report generation example](#example-3-validation-report-generation)
6. [If issues occur](#troubleshooting)

**Related Document**: [Part 1: Fundamentals and Procedures](./04-memory-validation-part1-procedures.md)

---

## Validation Scripts

### Master Validation Script

```bash
#!/bin/bash
# validate_all.sh - Run all validation levels

validate_all() {
    local start_time=$(date +%s)
    local total_errors=0

    echo "======================================="
    echo "  Session Memory Validation Suite"
    echo "======================================="
    echo ""

    # Level 1: Structure
    ./validate_structure.sh
    if [ $? -ne 0 ]; then
        ((total_errors++))
        echo "⚠ Structure validation failed - aborting further checks"
        return 1
    fi
    echo ""

    # Level 2: Content
    ./validate_content.sh
    if [ $? -ne 0 ]; then
        ((total_errors++))
    fi
    echo ""

    # Level 3: Consistency
    ./validate_consistency.sh
    # Consistency warnings don't increment errors
    echo ""

    # Level 4: Recovery
    ./validate_recovery.sh
    if [ $? -ne 0 ]; then
        ((total_errors++))
    fi
    echo ""

    # Final summary
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))

    echo "======================================="
    echo "  Validation Complete"
    echo "======================================="
    echo "Duration: ${duration}s"
    echo "Errors: $total_errors"
    echo ""

    if [ $total_errors -eq 0 ]; then
        echo "✓ All validations PASSED"
        return 0
    else
        echo "✗ Validation FAILED ($total_errors checks failed)"
        return 1
    fi
}

validate_all
```

## Validation Checklist

Use this checklist before compaction or after major changes:

```markdown
# Memory Validation Checklist

## Pre-Validation
- [ ] Working directory is correct
- [ ] No active memory operations running
- [ ] Changes committed (if in git)

## Structure Validation
- [ ] .session_memory directory exists
- [ ] All required subdirectories present
- [ ] All required root files exist
- [ ] Pattern category directories exist
- [ ] No broken symlinks
- [ ] Permissions are correct

## Content Validation
- [ ] active_context.md has valid header
- [ ] active_context.md has required sections
- [ ] progress_tracker.md has valid header
- [ ] pattern_index.md has valid header
- [ ] No markdown syntax errors
- [ ] No corrupted files

## Consistency Validation
- [ ] Pattern index matches actual pattern files
- [ ] No orphaned pattern files
- [ ] All snapshots are complete
- [ ] Timestamps are consistent
- [ ] No contradictory information

## Recovery Validation
- [ ] Recent snapshot exists (< 24 hours old)
- [ ] Snapshot is complete and readable
- [ ] Pre-compaction archives exist (if applicable)
- [ ] Archive index is up to date
- [ ] Test restoration succeeds

## Post-Validation
- [ ] All errors addressed
- [ ] Warnings reviewed and documented
- [ ] Validation results logged
- [ ] Ready to proceed with operation
```

## Examples

### Example 1: Quick Pre-Compaction Validation

```bash
#!/bin/bash
# quick_validate.sh - Fast validation before compaction

quick_validate() {
    echo "Quick validation before compaction..."

    # Critical checks only
    errors=0

    # Check structure
    [ -d ".session_memory" ] || ((errors++))
    [ -f ".session_memory/active_context.md" ] || ((errors++))
    [ -f ".session_memory/progress_tracker.md" ] || ((errors++))

    # Check for recent snapshot
    latest=$(ls -t .session_memory/snapshots/snapshot_*/metadata.txt 2>/dev/null | head -1)
    [ -n "$latest" ] || ((errors++))

    if [ $errors -eq 0 ]; then
        echo "✓ Quick validation passed"
        return 0
    else
        echo "✗ Quick validation failed ($errors critical errors)"
        echo "Run full validation before compaction"
        return 1
    fi
}

quick_validate
```

### Example 2: Validation with Auto-Repair

```bash
#!/bin/bash
# validate_and_repair.sh - Validate and auto-fix simple issues

validate_and_repair() {
    echo "Validating with auto-repair..."

    # Fix missing directories
    mkdir -p .session_memory/{active_context,patterns,progress,snapshots,archived}
    mkdir -p .session_memory/patterns/{problem_solution,workflow,decision_logic,error_recovery,configuration}

    # Remove broken symlinks
    find .session_memory -type l ! -exec test -e {} \; -delete

    # Fix permissions
    chmod -R u+rw .session_memory
    find .session_memory -type d -exec chmod u+x {} \;

    # Create missing root files with minimal content
    [ -f ".session_memory/session_info.md" ] || cat > .session_memory/session_info.md << 'EOF'
# Session Information
**Status:** Auto-repaired
EOF

    [ -f ".session_memory/active_context.md" ] || cat > .session_memory/active_context.md << 'EOF'
# Active Context
**Status:** Auto-repaired - needs manual update
EOF

    [ -f ".session_memory/progress_tracker.md" ] || cat > .session_memory/progress_tracker.md << 'EOF'
# Progress Tracker
**Status:** Auto-repaired - needs manual update
EOF

    [ -f ".session_memory/pattern_index.md" ] || cat > .session_memory/pattern_index.md << 'EOF'
# Pattern Index
**Status:** Auto-repaired - needs manual update
EOF

    echo "✓ Auto-repair complete - run validation to verify"
}

validate_and_repair
./validate_all.sh
```

### Example 3: Validation Report Generation

```bash
#!/bin/bash
# generate_validation_report.sh - Create detailed validation report

generate_validation_report() {
    report_file="validation_report_$(date +%Y%m%d_%H%M%S).md"

    cat > "$report_file" << EOF
# Memory Validation Report

**Generated:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Project:** $(pwd)

## Summary

$(./validate_all.sh 2>&1)

## Directory Structure

\`\`\`
$(tree .session_memory 2>/dev/null || find .session_memory -type d)
\`\`\`

## File Inventory

### Root Files
$(ls -lh .session_memory/*.md 2>/dev/null)

### Pattern Files
$(find .session_memory/patterns -name "*.md" | wc -l) pattern files

### Snapshots
$(ls -d .session_memory/snapshots/snapshot_* 2>/dev/null | wc -l) snapshots

### Archives
$(ls -d .session_memory/archived/pre_compaction_* 2>/dev/null | wc -l) archives

## Recommendations

[To be filled by manual review]

EOF

    echo "✓ Report generated: $report_file"
}

generate_validation_report
```

## Troubleshooting

### Problem: Validation Fails Due to Missing Directories

**Solution**:
```bash
# Run structure repair
mkdir -p .session_memory/{active_context,patterns,progress,snapshots,archived}
mkdir -p .session_memory/patterns/{problem_solution,workflow,decision_logic,error_recovery,configuration}

# Re-run validation
./validate_structure.sh
```

### Problem: Markdown Syntax Errors Detected

**Solution**:
```bash
# Find files with errors
find .session_memory -name "*.md" -exec sh -c '
    backticks=$(grep -o "```" "$1" | wc -l)
    if [ $((backticks % 2)) -ne 0 ]; then
        echo "Unmatched code blocks: $1"
    fi
' _ {} \;

# Manually fix each file
```

### Problem: Pattern Index Out of Sync

**Solution**:
```bash
# Rebuild pattern index
./rebuild_pattern_index.sh  # See pattern-recording.md

# Verify
./validate_consistency.sh
```

### Problem: No Recent Snapshots

**Solution**:
```bash
# Create snapshot immediately
./create_context_snapshot.sh
./create_progress_snapshot.sh

# Verify
./validate_recovery.sh
```

### Problem: Validation Timeout

**Cause**: Too many files, slow disk, or hung process

**Solution**:
```bash
# Run validation levels individually with timeouts
timeout 30s ./validate_structure.sh
timeout 60s ./validate_content.sh
timeout 30s ./validate_consistency.sh
timeout 30s ./validate_recovery.sh
```
