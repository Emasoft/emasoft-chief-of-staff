# Choosing the Right Category

## Table of Contents

- [Decision Flow](#decision-flow)
- [Category Selection Matrix](#category-selection-matrix)
- [Examples by Category](#examples-by-category)
- [Pattern Examples](#pattern-examples)

## Decision Flow

```
Is it about solving a specific problem?
├── YES → Problem-Solution (ps_)
└── NO
    ↓
    Is it a multi-step procedure for a task?
    ├── YES → Workflow (wf_)
    └── NO
        ↓
        Is it about making a decision?
        ├── YES → Decision-Logic (dl_)
        └── NO
            ↓
            Is it about recovering from an error?
            ├── YES → Error-Recovery (er_)
            └── NO
                ↓
                Is it a configuration that works well?
                ├── YES → Configuration (cfg_)
                └── NO → Consider if pattern is needed
```

## Category Selection Matrix

| Characteristic | ps_ | wf_ | dl_ | er_ | cfg_ |
|----------------|-----|-----|-----|-----|------|
| Addresses specific problem | ✓ | | | ✓ | |
| Multi-step procedure | | ✓ | | ✓ | |
| Decision criteria | | | ✓ | | |
| Recovery focus | | | | ✓ | |
| Configuration focus | | | | | ✓ |
| Reusable | ✓ | ✓ | ✓ | ✓ | ✓ |

## Examples by Category

**Scenario**: "Git authentication fails when spawning multiple agents"

**Analysis**:
- Is it a problem? → YES
- Does it have a solution? → YES
- **Category**: Problem-Solution (ps_)

**Scenario**: "Procedure for running tests in parallel"

**Analysis**:
- Is it a procedure? → YES
- Multiple steps? → YES
- **Category**: Workflow (wf_)

**Scenario**: "Criteria for approving feature requests"

**Analysis**:
- Is it a decision? → YES
- Has criteria? → YES
- **Category**: Decision-Logic (dl_)

**Scenario**: "How to recover from failed compaction"

**Analysis**:
- Is it error recovery? → YES
- Has recovery steps? → YES
- **Category**: Error-Recovery (er_)

**Scenario**: "ESLint setup for TypeScript"

**Analysis**:
- Is it configuration? → YES
- Works well? → YES
- **Category**: Configuration (cfg_)

---

# Pattern Examples

## Example 1: Categorizing New Pattern

```bash
# Situation: Found solution for slow test execution

# Analysis:
# - Is it a problem? YES (tests are slow)
# - Is it a procedure? YES (steps to parallelize)
# - Main focus: procedure, not problem

# Decision: Workflow pattern (wf_)

# Create pattern
./create_pattern.sh workflow "parallel-test-execution"
```

## Example 2: Re-categorizing Existing Pattern

```bash
# Pattern originally in ps_005: "Choosing between JWT and session cookies"

# Analysis:
# - Not really a problem with solution
# - More about decision criteria
# - Should be decision-logic

# Re-categorize
mv .session_memory/patterns/problem_solution/ps_005_jwt-vs-sessions.md \
   .session_memory/patterns/decision_logic/dl_003_authentication-method.md

# Update index
./rebuild_pattern_index.sh
```

## Example 3: Multi-Category Pattern

```bash
# Situation: Context overflow (problem) with recovery procedure

# Create two related patterns:

# 1. Problem-Solution: Why overflow happens and prevention
./create_pattern.sh problem_solution "context-overflow-causes"

# 2. Error-Recovery: How to recover when it happens
./create_pattern.sh error_recovery "context-overflow-recovery"

# Link them in Related Patterns section
```

## Example 4: Pattern Not Fitting Any Category

```bash
# Situation: Notes about team communication preferences

# Analysis:
# - Not a problem to solve
# - Not a procedure
# - Not a decision with criteria
# - Not error recovery
# - Not configuration

# Decision: Not a pattern, move to docs_dev/
echo "[Notes]" > docs_dev/team-communication-notes.md
```
