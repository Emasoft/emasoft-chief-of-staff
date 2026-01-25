# Task Dependencies

## Overview

Task dependency management tracks relationships between tasks to:
- Prevent starting tasks before prerequisites complete
- Identify parallelization opportunities
- Calculate critical path
- Estimate completion time
- Avoid circular dependencies

---

## Table of Contents

This document is split into 4 parts for efficient context loading.

### Part 1: Dependency Types and Notation
**File**: [09-task-dependencies-part1-types-notation.md](./09-task-dependencies-part1-types-notation.md)

**Contents**:
- 1.1 Type 1: Sequential Dependency - When Task B cannot start until Task A completes
- 1.2 Type 2: Parallel with Merge - When independent tasks converge to common successor
- 1.3 Type 3: Split Dependency - When one task enables multiple parallel workstreams
- 1.4 Type 4: Partial Dependency - When Task B can start after Task A reaches milestone
- 1.5 Type 5: Optional Dependency - When Task B is enhanced but not blocked by Task A
- 2.1 Text-Based Notation - Linear chains, parallel paths, complex graphs, tables
- 2.2 In-Task Dependency Recording - How to record dependencies in task definitions

---

### Part 2: Dependency Management
**File**: [09-task-dependencies-part2-management.md](./09-task-dependencies-part2-management.md)

**Contents**:
- Procedure 1: Record Dependency - How to record task dependencies with scripts
- Procedure 2: Check Dependencies Met - How to verify all dependencies are satisfied
- Procedure 3: Update Dependencies After Task Completion - How to unblock waiting tasks
- Procedure 4: Detect Circular Dependencies - How to find circular dependency chains

---

### Part 3: Critical Path Analysis and Validation
**File**: [09-task-dependencies-part3-critical-path.md](./09-task-dependencies-part3-critical-path.md)

**Contents**:
- 1.1 Definition - What is critical path and why it matters
- 1.2 Calculation Procedure - Step-by-step critical path calculation
- 1.3 Critical Path Script - Automated critical path analysis
- 2.1 Validation Checklist - Dependency validation requirements
- 2.2 Validation Script - Automated dependency validation

---

### Part 4: Examples and Troubleshooting
**File**: [09-task-dependencies-part4-examples.md](./09-task-dependencies-part4-examples.md)

**Contents**:
- Example 1: Simple Sequential Dependencies - Linear task chain example
- Example 2: Parallel Development with Merge - Frontend/backend parallel work example
- Example 3: Complex Dependency Graph - Multi-path dependency example
- Example 4: Partial Dependencies - Milestone-based dependency example
- Troubleshooting: Task Stuck Waiting on Dependency
- Troubleshooting: Circular Dependency Detected
- Troubleshooting: Too Many Dependencies
- Troubleshooting: Unknown Task Scope
- Troubleshooting: Dependency Information Lost

---

## Quick Reference

### Dependency Type Summary

| Type | Notation | Use Case |
|------|----------|----------|
| Sequential | `A → B` | B needs artifacts from A |
| Parallel Merge | `A,B → C` | Independent tasks with common successor |
| Split | `A → B,C,D` | One task enables multiple workstreams |
| Partial | `A (milestone) → B` | Start before full completion |
| Optional | `A ~~> B` | Nice-to-have, not blocking |

### When to Read Each Part

| If you need to... | Read |
|-------------------|------|
| Understand dependency types | Part 1 |
| Learn dependency notation | Part 1 |
| Record or check dependencies | Part 2 |
| Detect circular dependencies | Part 2 |
| Calculate critical path | Part 3 |
| Validate dependencies | Part 3 |
| See real-world examples | Part 4 |
| Fix dependency problems | Part 4 |

---

## Related References

- [08-manage-progress-tracking.md](./08-manage-progress-tracking.md) - How to track task progress
- [08-manage-progress-tracking-part2-task-management.md](./08-manage-progress-tracking-part2-task-management.md) - How to complete tasks properly
- [03-manage-active-context-part2-snapshots-pruning.md](./03-manage-active-context-part2-snapshots-pruning.md) - How to save/restore session state
