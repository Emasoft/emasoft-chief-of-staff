# Update Procedures for Active Context

This document contains the detailed bash scripts and procedures for updating active context.

**Parent document**: [03-manage-active-context.md](./03-manage-active-context.md)

---

## Table of Contents
1. [Procedure 1: Update Current Focus](#procedure-1-update-current-focus)
2. [Procedure 2: Add Decision to Recent Decisions](#procedure-2-add-decision-to-recent-decisions)
3. [Procedure 3: Add Open Question](#procedure-3-add-open-question)
4. [Procedure 4: Resolve Open Question](#procedure-4-resolve-open-question)

---

## Procedure 1: Update Current Focus

```bash
#!/bin/bash
# update_focus.sh - Update current focus in active context

update_current_focus() {
    local new_focus="$1"
    local context_file=".session_memory/active_context.md"

    # Create backup
    cp "$context_file" "$context_file.bak"

    # Update timestamp
    timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

    # Read current file, update focus section
    awk -v focus="$new_focus" -v ts="$timestamp" '
    BEGIN { in_focus=0; updated=0 }
    /^## Current Focus/ {
        print $0
        print focus
        in_focus=1
        updated=1
        next
    }
    /^## / { in_focus=0 }
    !in_focus || !updated { print }
    /^**Last Updated:**/ {
        print "**Last Updated:** " ts
        next
    }
    { if (!in_focus) print }
    ' "$context_file.bak" > "$context_file"

    rm "$context_file.bak"
    echo "✓ Focus updated"
}

# Usage
update_current_focus "Implementing OAuth2 authentication"
```

---

## Procedure 2: Add Decision to Recent Decisions

```bash
#!/bin/bash
# add_decision.sh - Add decision to active context

add_decision() {
    local decision="$1"
    local rationale="$2"
    local context_file=".session_memory/active_context.md"

    timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

    # Append to Recent Decisions section
    cat >> "$context_file" << EOF

### Decision: $decision
- **Date**: $timestamp
- **Rationale**: $rationale
- **Impact**: [To be documented]

EOF

    echo "✓ Decision added"
}

# Usage
add_decision "Use JWT tokens" "Better API support and mobile compatibility"
```

---

## Procedure 3: Add Open Question

```bash
#!/bin/bash
# add_question.sh - Add open question to active context

add_question() {
    local question="$1"
    local importance="$2"
    local blocked="$3"
    local context_file=".session_memory/active_context.md"

    timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

    cat >> "$context_file" << EOF

### Q: $question
- **Added**: $timestamp
- **Importance**: $importance
- **Blocked**: $blocked
- **Status**: Open

EOF

    echo "✓ Question added"
}

# Usage
add_question "Token expiry duration?" "Security vs UX tradeoff" "Token refresh implementation"
```

---

## Procedure 4: Resolve Open Question

```bash
#!/bin/bash
# resolve_question.sh - Move question from open to decisions

resolve_question() {
    local question_keyword="$1"
    local answer="$2"
    local context_file=".session_memory/active_context.md"

    timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

    # Find and remove question from Open Questions
    # Add to Recent Decisions with answer

    # Manual approach (safer than automated):
    echo "Question resolved: $question_keyword"
    echo "Answer: $answer"
    echo "Please manually:"
    echo "1. Remove question from Open Questions section"
    echo "2. Add to Recent Decisions with answer"
    echo "3. Update timestamp"
}

# Usage
resolve_question "Token expiry" "Set to 1 hour for security, implement refresh tokens"
```
