# Task Dependencies - Part 1: Dependency Types and Notation

## Table of Contents
1. [Dependency Types](#dependency-types)
   - 1.1 [Type 1: Sequential Dependency](#type-1-sequential-dependency)
   - 1.2 [Type 2: Parallel with Merge](#type-2-parallel-with-merge)
   - 1.3 [Type 3: Split Dependency](#type-3-split-dependency)
   - 1.4 [Type 4: Partial Dependency](#type-4-partial-dependency)
   - 1.5 [Type 5: Optional Dependency](#type-5-optional-dependency)
2. [Dependency Notation](#dependency-notation)
   - 2.1 [Text-Based Notation](#text-based-notation)
   - 2.2 [In-Task Dependency Recording](#in-task-dependency-recording)

---

## Dependency Types

### Type 1: Sequential Dependency

**Definition**: Task B cannot start until Task A completes.

**Notation**: `A → B`

**Example**:
```
OAuth setup → Implement callback handler
```

**Use Case**: Task B needs artifacts or knowledge from Task A

### Type 2: Parallel with Merge

**Definition**: Tasks A and B can run in parallel, both required for Task C.

**Notation**:
```
A ─┐
   ├─> C
B ─┘
```

**Example**:
```
Unit tests ─┐
            ├─> Deploy
Integration tests ─┘
```

**Use Case**: Independent tasks with common successor

### Type 3: Split Dependency

**Definition**: Task A produces multiple independent follow-up tasks.

**Notation**:
```
    ├─> B
A ─┼─> C
    └─> D
```

**Example**:
```
        ├─> Frontend implementation
API design ─┼─> Backend implementation
        └─> Documentation update
```

**Use Case**: One task enables multiple parallel workstreams

### Type 4: Partial Dependency

**Definition**: Task B can start after Task A reaches certain milestone.

**Notation**: `A (milestone) → B`

**Example**:
```
API implementation (basic endpoints done) → Frontend development
```

**Use Case**: Don't wait for full completion, start based on partial progress

### Type 5: Optional Dependency

**Definition**: Task B is enhanced by Task A, but can proceed without it.

**Notation**: `A ~~> B` (dashed arrow)

**Example**:
```
Performance optimization ~~> Deploy
```

**Use Case**: Nice-to-have prerequisite, not blocking

---

## Dependency Notation

### Text-Based Notation

```markdown
## Task Dependencies

### Linear Chain
```
Task A → Task B → Task C
```

### Parallel Paths
```
Task A → Task C
Task B → Task C
```

### Complex Graph
```
Task A
  ├─> Task B
  │     └─> Task D
  └─> Task C
        └─> Task D
```

### Dependency Table
| Task | Depends On | Type | Status |
|------|------------|------|--------|
| Task A | None | - | Complete |
| Task B | Task A | Sequential | Active |
| Task C | Task A | Sequential | Waiting |
| Task D | Task B, Task C | Merge | Waiting |
```

### In-Task Dependency Recording

```markdown
- [ ] Task name
  - **Dependencies**: Task A, Task B
  - **Dependency Type**: Merge (requires both)
  - **Can Start When**: Both Task A and Task B complete
```

---

**Navigation**:
- [Back to main: Task Dependencies](./09-task-dependencies.md)
- [Next: Part 2 - Dependency Management](./09-task-dependencies-part2-management.md)
