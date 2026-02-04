# Pattern Categories

## Table of Contents

1. [Purpose](#purpose)
2. [Category Definitions](#category-definitions)
3. [Pattern Category Details](#pattern-category-details)
4. [How to Choose Categories](#choosing-the-right-category)

---

## Purpose

Pattern categories organize reusable knowledge by type. Proper categorization enables:
- Quick pattern discovery
- Consistent pattern structure
- Efficient pattern reuse
- Clear organization

---

## Category Definitions

### Category Table

| Category | Prefix | Purpose | When to Use |
|----------|--------|---------|-------------|
| Problem-Solution | `ps_` | Document problems and solutions | After solving a tricky problem |
| Workflow | `wf_` | Document effective procedures | After discovering efficient workflow |
| Decision-Logic | `dl_` | Document decision criteria | After making important decision |
| Error-Recovery | `er_` | Document recovery procedures | After recovering from error/failure |
| Configuration | `cfg_` | Document working configurations | After finding effective configuration |

---

## Pattern Category Details

Each pattern category has its own detailed reference document with structure templates, when to create, and examples.

### Problem-Solution Patterns (ps_)

See [07-pattern-categories-part1-problem-solution.md](07-pattern-categories-part1-problem-solution.md)

**Contents**:
- Definition of Problem-Solution patterns
- Structure template with all required sections
- When to create a Problem-Solution pattern
- Examples of good Problem-Solution patterns
- Examples of bad Problem-Solution patterns

### Workflow Patterns (wf_)

See [07-pattern-categories-part2-workflow.md](07-pattern-categories-part2-workflow.md)

**Contents**:
- Definition of Workflow patterns
- Structure template with phases and variations
- When to create a Workflow pattern
- Examples of good Workflow patterns
- Examples of bad Workflow patterns

### Decision-Logic Patterns (dl_)

See [07-pattern-categories-part3-decision-logic.md](07-pattern-categories-part3-decision-logic.md)

**Contents**:
- Definition of Decision-Logic patterns
- Structure template with decision trees and options analysis
- When to create a Decision-Logic pattern
- Examples of good Decision-Logic patterns
- Examples of bad Decision-Logic patterns

### Error-Recovery Patterns (er_)

See [07-pattern-categories-part4-error-recovery.md](07-pattern-categories-part4-error-recovery.md)

**Contents**:
- Definition of Error-Recovery patterns
- Structure template with detection and recovery steps
- When to create an Error-Recovery pattern
- Examples of good Error-Recovery patterns
- Examples of bad Error-Recovery patterns

### Configuration Patterns (cfg_)

See [07-pattern-categories-part5-configuration.md](07-pattern-categories-part5-configuration.md)

**Contents**:
- Definition of Configuration patterns
- Structure template with verification and common issues
- When to create a Configuration pattern
- Examples of good Configuration patterns
- Examples of bad Configuration patterns

---

## Choosing the Right Category

See [07-pattern-categories-part6-choosing-examples.md](07-pattern-categories-part6-choosing-examples.md) for detailed decision flow, selection matrix, and practical examples.

### Quick Decision Flow

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

### Quick Reference Matrix

| Characteristic | ps_ | wf_ | dl_ | er_ | cfg_ |
|----------------|-----|-----|-----|-----|------|
| Addresses specific problem | ✓ | | | ✓ | |
| Multi-step procedure | | ✓ | | ✓ | |
| Decision criteria | | | ✓ | | |
| Recovery focus | | | | ✓ | |
| Configuration focus | | | | | ✓ |
| Reusable | ✓ | ✓ | ✓ | ✓ | ✓ |

---

## Part Files Reference

| Part File | Lines | Content |
|-----------|-------|---------|
| [part1-problem-solution.md](07-pattern-categories-part1-problem-solution.md) | ~75 | Problem-Solution pattern details |
| [part2-workflow.md](07-pattern-categories-part2-workflow.md) | ~85 | Workflow pattern details |
| [part3-decision-logic.md](07-pattern-categories-part3-decision-logic.md) | ~100 | Decision-Logic pattern details |
| [part4-error-recovery.md](07-pattern-categories-part4-error-recovery.md) | ~100 | Error-Recovery pattern details |
| [part5-configuration.md](07-pattern-categories-part5-configuration.md) | ~105 | Configuration pattern details |
| [part6-choosing-examples.md](07-pattern-categories-part6-choosing-examples.md) | ~140 | Category selection and examples |
