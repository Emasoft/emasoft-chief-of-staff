# Record Patterns - Part 1: Fundamentals

## Table of Contents
1. [When you need to understand the purpose](#purpose)
2. [Understanding what patterns are](#what-are-patterns)
3. [Understanding pattern categories](#pattern-categories)
4. [When to record patterns](#when-to-record-patterns)
5. [How to record patterns](#pattern-recording-procedure)
6. [Understanding file structure](#pattern-file-structure)
7. [Managing pattern index](#pattern-index-management)
8. [For examples and troubleshooting](#related-documents)

## Related Documents

- **Part 2**: [05-record-patterns-part2-examples.md](./05-record-patterns-part2-examples.md) - Complete examples and troubleshooting

---

## Purpose

Pattern recording captures reusable knowledge discovered during work. Patterns enable:
- Quick reference for recurring situations
- Knowledge transfer across sessions
- Decision consistency
- Error recovery procedures
- Best practice documentation

## What Are Patterns

Patterns are **reusable solutions to recurring problems** or **effective procedures for common tasks**.

**Key Characteristics**:
- **Reusable**: Can be applied to similar situations
- **Concrete**: Specific enough to be actionable
- **Complete**: Contains all information needed to apply it
- **Proven**: Based on actual experience, not theory

**Not Patterns**:
- One-time solutions specific to unique situations
- Vague ideas or principles without concrete steps
- Incomplete procedures missing critical information
- Untested theories or assumptions

## Pattern Categories

### 1. Problem-Solution (ps_)

**Definition**: A specific problem encountered and the solution that worked.

**Structure**:
- Problem description
- Context where it occurred
- Solution that worked
- Why it worked
- When to apply this solution

**Example Scenario**: Git authentication fails when spawning multiple agents

### 2. Workflow (wf_)

**Definition**: An effective procedure for accomplishing a common task.

**Structure**:
- Task description
- Prerequisites
- Step-by-step procedure
- Expected outcome
- Variations for different contexts

**Example Scenario**: Parallel test execution across multiple agent instances

### 3. Decision-Logic (dl_)

**Definition**: Decision trees or logic for making consistent choices.

**Structure**:
- Decision point
- Criteria to consider
- Decision tree or flowchart
- Examples of application
- Edge cases

**Example Scenario**: When to approve vs. reject feature requests

### 4. Error-Recovery (er_)

**Definition**: Procedures for recovering from specific errors or failures.

**Structure**:
- Error description and symptoms
- Root cause
- Recovery procedure
- Prevention measures
- Verification steps

**Example Scenario**: Recovery from context overflow during compaction

### 5. Configuration (cfg_)

**Definition**: Working configurations for tools, services, or environments.

**Structure**:
- What is being configured
- Why this configuration
- Configuration steps or file
- Verification procedure
- Common issues

**Example Scenario**: ESLint configuration for TypeScript projects

## When to Record Patterns

Record a pattern when:

### Trigger 1: Problem Solved After Significant Effort
**Criteria**: Spent >15 minutes solving a problem that might recur

**Action**: Record as Problem-Solution pattern

**Procedure**:
1. Document the problem clearly
2. Describe the solution
3. Explain why it worked
4. Note when to use this solution

### Trigger 2: Effective Workflow Discovered
**Criteria**: Found an efficient way to accomplish a common task

**Action**: Record as Workflow pattern

**Procedure**:
1. Document the task
2. List prerequisites
3. Write step-by-step procedure
4. Note variations

### Trigger 3: Important Decision Made
**Criteria**: Made a decision that affects future work or establishes precedent

**Action**: Record as Decision-Logic pattern

**Procedure**:
1. Document decision criteria
2. Explain rationale
3. Provide decision tree
4. Give examples

### Trigger 4: Error Recovery Successful
**Criteria**: Recovered from a failure using a specific procedure

**Action**: Record as Error-Recovery pattern

**Procedure**:
1. Document error symptoms
2. Explain root cause
3. Provide recovery steps
4. Add prevention measures

### Trigger 5: Configuration Works Well
**Criteria**: Configuration solves a problem or improves workflow

**Action**: Record as Configuration pattern

**Procedure**:
1. Document what is configured
2. Provide configuration
3. Explain why it works
4. Add verification steps

## Pattern Recording Procedure

### Step 1: Identify Pattern Type

Determine which category fits best:
- Problem you solved? → Problem-Solution
- Effective procedure? → Workflow
- Important decision? → Decision-Logic
- Error recovery? → Error-Recovery
- Working configuration? → Configuration

### Step 2: Generate Pattern ID

```bash
# Get next pattern number for category
category="problem_solution"  # or workflow, decision_logic, etc.
prefix="ps"  # or wf, dl, er, cfg

# Count existing patterns
count=$(ls .session_memory/patterns/$category/ 2>/dev/null | wc -l)
next_num=$(printf "%03d" $((count + 1)))

# Example: ps_001, wf_002, etc.
pattern_id="${prefix}_${next_num}"
```

### Step 3: Create Pattern File

```bash
# Generate filename
description="brief-description-kebab-case"
filename="${pattern_id}_${description}.md"
filepath=".session_memory/patterns/$category/$filename"

# Create file with template
cat > "$filepath" << 'EOF'
# Pattern: [Brief Title]

**Pattern ID**: [pattern_id]
**Category**: [category]
**Created**: [timestamp]

## Problem/Task
[Description of problem or task]

## Context
[When/where this applies]

## Solution/Procedure
[Step-by-step solution or procedure]

## Rationale
[Why this works]

## Examples
[Concrete examples of application]

## Related Patterns
[Links to related patterns]

EOF

echo "Pattern file created: $filepath"
```

### Step 4: Fill Pattern Content

Edit the pattern file with specific details:
- Clear problem/task description
- Concrete steps or solution
- Explanation of why it works
- Real examples from experience

### Step 5: Update Pattern Index

```bash
# Add entry to pattern index
category_display=$(echo "$category" | sed 's/_/ /g' | sed 's/\b\(.\)/\u\1/g')

cat >> .session_memory/pattern_index.md << EOF

- [$pattern_id] $description - [Link](patterns/$category/$filename)

EOF

echo "Pattern index updated"
```

### Step 6: Verify Pattern

Check that:
- [ ] File is in correct category directory
- [ ] Pattern ID is unique
- [ ] All sections are filled
- [ ] Examples are concrete
- [ ] Index is updated

## Pattern File Structure

### Template

```markdown
# Pattern: [Brief Descriptive Title]

**Pattern ID**: ps_001 (or wf_001, dl_001, etc.)
**Category**: Problem-Solution (or other category)
**Created**: 2026-01-01 14:30 UTC
**Last Updated**: 2026-01-01 14:30 UTC

---

## Problem/Task

[Clear description of the problem or task this pattern addresses]

**Symptoms** (for Problem-Solution):
- Symptom 1
- Symptom 2

**Goal** (for Workflow):
[What you're trying to accomplish]

---

## Context

**When this applies**:
- Context 1
- Context 2

**Prerequisites**:
- Prerequisite 1
- Prerequisite 2

**Constraints**:
- Constraint 1

---

## Solution/Procedure

### Step 1: [First Step]
[Detailed description]

```bash
# Code example if applicable
command --flags
```

### Step 2: [Second Step]
[Detailed description]

### Step 3: [Third Step]
[Detailed description]

---

## Rationale

**Why this works**:
[Explanation of underlying mechanism]

**Why alternatives don't work**:
- Alternative 1: [Why it fails]
- Alternative 2: [Why it fails]

---

## Examples

### Example 1: [Scenario Name]
**Situation**: [Specific scenario]

**Application**:
```
[How pattern was applied]
```

**Outcome**: [Result]

### Example 2: [Another Scenario]
[Similar structure]

---

## Verification

**How to verify success**:
1. Check 1
2. Check 2

**Expected outcome**:
[What success looks like]

---

## Related Patterns

- [ps_002]\(./problem_solution/ps_002_related-pattern.md) - Related problem
- [wf_003]\(./workflow/wf_003_related-workflow.md) - Related workflow

---

## Notes

**Known Limitations**:
- Limitation 1

**Future Improvements**:
- Improvement 1

**Additional Resources**:
- [External link or reference]
```

## Pattern Index Management

### Index Structure

```markdown
# Pattern Index

**Last Updated**: 2026-01-01 14:30 UTC
**Total Patterns**: 15

---

## Problem-Solution Patterns

- [ps_001] Git auth failure in parallel agents - [Link]\(patterns/problem_solution/ps_001_git-auth-failure.md)
- [ps_002] Context overflow during compaction - [Link]\(patterns/problem_solution/ps_002_context-overflow.md)

## Workflow Patterns

- [wf_001] Parallel test execution - [Link]\(patterns/workflow/wf_001_parallel-testing.md)
- [wf_002] Safe code refactoring - [Link]\(patterns/workflow/wf_002_safe-refactoring.md)

## Decision-Logic Patterns

- [dl_001] Feature request approval - [Link]\(patterns/decision_logic/dl_001_feature-approval.md)

## Error-Recovery Patterns

- [er_001] Recovery from failed compaction - [Link]\(patterns/error_recovery/er_001_compaction-recovery.md)

## Configuration Patterns

- [cfg_001] ESLint for TypeScript - [Link]\(patterns/configuration/cfg_001_eslint-typescript.md)

---

## Pattern Categories

### By Frequency of Use
1. ps_001 (used 12 times)
2. wf_001 (used 8 times)
3. er_001 (used 5 times)

### By Recency
1. cfg_001 (added 2026-01-01)
2. dl_001 (added 2025-12-30)
3. ps_002 (added 2025-12-29)
```

### Rebuild Index Script

```bash
#!/bin/bash
# rebuild_pattern_index.sh - Regenerate pattern index from files

rebuild_pattern_index() {
    local index_file=".session_memory/pattern_index.md"
    local timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

    # Count total patterns
    total=$(find .session_memory/patterns -name "*.md" -type f | wc -l)

    # Start new index
    cat > "$index_file" << EOF
# Pattern Index

**Last Updated**: $timestamp
**Total Patterns**: $total

---

EOF

    # Add patterns by category
    categories=("problem_solution" "workflow" "decision_logic" "error_recovery" "configuration")
    category_names=("Problem-Solution Patterns" "Workflow Patterns" "Decision-Logic Patterns" "Error-Recovery Patterns" "Configuration Patterns")

    for i in "${!categories[@]}"; do
        category="${categories[$i]}"
        category_name="${category_names[$i]}"

        echo "## $category_name" >> "$index_file"
        echo "" >> "$index_file"

        # Find all patterns in this category
        if [ -d ".session_memory/patterns/$category" ]; then
            for pattern in .session_memory/patterns/$category/*.md; do
                if [ -f "$pattern" ]; then
                    basename=$(basename "$pattern" .md)
                    # Extract pattern ID and description
                    pattern_id=$(echo "$basename" | grep -oP '^[a-z]+_\d+')
                    description=$(echo "$basename" | sed "s/${pattern_id}_//")

                    # Format for index
                    echo "- [$pattern_id] $description - [Link](patterns/$category/$(basename "$pattern"))" >> "$index_file"
                fi
            done
        fi

        echo "" >> "$index_file"
    done

    echo "✓ Pattern index rebuilt: $total patterns"
}

rebuild_pattern_index
```
