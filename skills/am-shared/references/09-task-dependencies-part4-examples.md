# Task Dependencies - Part 4: Examples and Troubleshooting

## Table of Contents
1. [Examples](#examples)
   - 1.1 [Example 1: Simple Sequential Dependencies](#example-1-simple-sequential-dependencies)
   - 1.2 [Example 2: Parallel Development with Merge](#example-2-parallel-development-with-merge)
   - 1.3 [Example 3: Complex Dependency Graph](#example-3-complex-dependency-graph)
   - 1.4 [Example 4: Partial Dependencies](#example-4-partial-dependencies)
2. [Troubleshooting](#troubleshooting)
   - 2.1 [Task Stuck Waiting on Dependency](#problem-task-stuck-waiting-on-dependency)
   - 2.2 [Circular Dependency Detected](#problem-circular-dependency-detected)
   - 2.3 [Too Many Dependencies](#problem-too-many-dependencies)
   - 2.4 [Unknown Task Scope](#problem-unknown-task-scope)
   - 2.5 [Dependency Information Lost](#problem-dependency-information-lost)

---

## Examples

### Example 1: Simple Sequential Dependencies

```markdown
## Active Tasks

- [x] Task A: Design API
  - **Started**: 2026-01-01 09:00 UTC
  - **Completed**: 2026-01-01 11:00 UTC
  - **Duration**: 2 hours

- [ ] Task B: Implement API
  - **Started**: 2026-01-01 11:00 UTC
  - **Dependencies**: Task A
  - **Dependency Type**: Sequential
  - **Progress**: 50%

- [ ] Task C: Write API documentation
  - **Dependencies**: Task B
  - **Dependency Type**: Sequential
  - **Status**: Waiting for Task B

## Task Dependencies

```
Task A (completed) → Task B (50%) → Task C (waiting)
```

**Status**: On track, linear progression
```

### Example 2: Parallel Development with Merge

```markdown
## Active Tasks

- [ ] Task X: Implement frontend
  - **Started**: 2026-01-01 10:00 UTC
  - **Dependencies**: API design (completed)
  - **Progress**: 60%
  - **Estimated Completion**: 2026-01-01 14:00 UTC

- [ ] Task Y: Implement backend
  - **Started**: 2026-01-01 10:00 UTC
  - **Dependencies**: API design (completed)
  - **Progress**: 70%
  - **Estimated Completion**: 2026-01-01 13:00 UTC

- [ ] Task Z: Integration testing
  - **Dependencies**: Task X, Task Y
  - **Dependency Type**: Merge (requires both)
  - **Status**: Waiting
  - **Can Start**: When both X and Y complete

## Task Dependencies

```
API design (completed)
  ├─> Frontend (60%) ─┐
  └─> Backend (70%) ──├─> Integration tests (waiting)
                       └─> (Can start when both complete)
```

**Status**: Parallel work in progress
**Critical Path**: API design → Frontend → Integration (frontend is slower)
**Optimization**: Frontend is on critical path, consider accelerating
```

### Example 3: Complex Dependency Graph

```markdown
## Task Dependency Graph

```
Task A: OAuth setup (completed)
  ├─> Task B: Callback handler (active, 80%)
  │     └─> Task E: Integration tests (waiting)
  └─> Task C: JWT implementation (active, 50%)
        ├─> Task D: Token refresh (waiting)
        └─> Task E: Integration tests (waiting)
```

**Analysis**:
- Task E requires both B and D
- Task D depends on C
- Critical path: A → C → D → E

**Current Status**:
- B nearly done (80%)
- C slower progress (50%)
- C is on critical path
- Need to prioritize C over B

**Action**: Focus resources on Task C (critical path)
```

### Example 4: Partial Dependencies

```markdown
## Active Tasks

- [ ] Task A: Implement authentication API (20 endpoints)
  - **Progress**: 40% (8/20 endpoints done)
  - **Milestone**: Basic endpoints (5) complete

- [ ] Task B: Build frontend login form
  - **Dependencies**: Task A (basic endpoints milestone)
  - **Dependency Type**: Partial
  - **Status**: Active (started after milestone reached)
  - **Progress**: 30%

- [ ] Task C: Write comprehensive API tests
  - **Dependencies**: Task A (100% complete)
  - **Dependency Type**: Sequential
  - **Status**: Waiting (needs all 20 endpoints)

## Dependency Notes

**Partial Dependency Explanation**:
- Task B doesn't need all 20 endpoints
- Can start with just login/logout endpoints (basic milestone)
- Task C needs full API completion for comprehensive testing

**Benefits**:
- Faster overall completion (parallelization)
- Early feedback on API design from frontend work
```

---

## Troubleshooting

### Problem: Task Stuck Waiting on Dependency

**Solution**:
```bash
# Check if dependency is actually complete
grep "- \[x\] Dependency Name" .session_memory/progress_tracker.md

# If complete, update waiting task to active
# If not complete, check if partial dependency is possible
# Or if dependency can be broken into smaller tasks
```

### Problem: Circular Dependency Detected

**Solution**:
```markdown
# Example: Task A depends on B, Task B depends on A

# Resolution Options:

1. **Split Task**: Break one task into two parts
   - Task A1 (no dependency)
   - Task A2 (depends on B)
   - Task B (depends on A1)

2. **Remove Dependency**: One dependency may not be real
   - Review if A truly needs B
   - Or if B truly needs A

3. **Reorder**: Change implementation order
   - Implement A first (without B)
   - Then B (using A)
   - Then update A if needed
```

### Problem: Too Many Dependencies

**Solution**:
```bash
# Task has 5+ dependencies

# Review:
# - Are all dependencies necessary?
# - Can task be split into smaller tasks?
# - Can some dependencies be partial instead of complete?

# Refactor:
# - Break complex task into smaller tasks
# - Each smaller task has fewer dependencies
# - Easier to manage and parallelize
```

### Problem: Unknown Task Scope

**Solution** (per RULE 13 - NO time estimates):
```markdown
# Use complexity classification instead of time estimates

## Add Complexity to Tasks

- [ ] Task A - Brief description
  - **Complexity**: Medium (2-5 files, moderate dependencies)
  - **Blockers**: None

## Track Progress by Percentage
- **Progress**: 60% complete
- **Completed**: Core logic, unit tests
- **Remaining**: Integration tests, documentation

## Order by Dependencies, Not Duration
Use dependency graph to determine critical path based on blocking relationships
```

### Problem: Dependency Information Lost

**Solution**:
```bash
# Restore from snapshot
cp .session_memory/progress/progress_latest.md .session_memory/progress_tracker.md

# Or reconstruct from context
grep -r "depends on" .session_memory/active_context/

# Rebuild dependency graph
./rebuild_dependency_graph.sh
```

---

**Navigation**:
- [Back to main: Task Dependencies](./09-task-dependencies.md)
- [Previous: Part 3 - Critical Path and Validation](./09-task-dependencies-part3-critical-path.md)
