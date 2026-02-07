# Cross-Project Coordination Reference

## Table of Contents

- 3.1 What is cross-project coordination - Multi-project orchestration
- 3.2 Dependency types - How projects relate
  - 3.2.1 Code dependencies - Shared libraries
  - 3.2.2 Data dependencies - Shared data sources
  - 3.2.3 Temporal dependencies - Sequencing requirements
  - 3.2.4 Resource dependencies - Shared agents or services
- 3.3 Coordination procedure - Managing cross-project work
  - 3.3.1 Scope identification - Finding cross-project elements
  - 3.3.2 Dependency mapping - Graphing relationships
  - 3.3.3 Coordination planning - Scheduling across projects
  - 3.3.4 Checkpoint execution - Sync points during work
  - 3.3.5 State reconciliation - Ensuring consistency
- 3.4 Communication patterns - Messaging between project agents
- 3.5 Conflict resolution - Handling cross-project conflicts
- 3.6 Examples - Cross-project scenarios
- 3.7 Troubleshooting - Coordination issues

---

## 3.1 What is cross-project coordination

Cross-project coordination is the management of work that spans multiple projects. It handles:

- Dependencies between projects
- Shared resources across projects
- Sequencing of cross-project tasks
- Consistency of shared state

---

## 3.2 Dependency types

### 3.2.1 Code dependencies

Projects that share code:
- Library used by multiple projects
- Submodules or git subtrees
- Shared utility packages

**Example:**
```
emasoft-plugins-marketplace
├── perfect-skill-suggester (submodule)
└── claude-plugins-validation (submodule)
```

Changes to PSS require EPM to update its submodule.

### 3.2.2 Data dependencies

Projects that share data:
- Shared configuration files
- Common data sources
- Synchronized databases

**Example:**
```
Project A writes to config/shared-settings.json
Project B reads from config/shared-settings.json
```

### 3.2.3 Temporal dependencies

Projects that must execute in sequence:
- Release A before Release B
- Build library before building app
- Run migrations before tests

**Example:**
```
1. Update validation library (CPV)
2. Update PSS to use new CPV
3. Update marketplace to include new PSS
```

### 3.2.4 Resource dependencies

Projects that share limited resources:
- Same agent assigned to multiple projects
- Shared API rate limits
- Shared test environment

**Example:**
```
test-engineer-01 assigned to both PSS and CPV
Cannot run both test suites simultaneously
```

---

## 3.3 Coordination procedure

### 3.3.1 Scope identification

**Purpose:** Identify all projects involved in the work.

**Steps:**
1. List primary project(s) for the task
2. Check for code dependencies
3. Check for data dependencies
4. Check for temporal dependencies
5. Check for resource dependencies
6. Document all involved projects

**Scope Document:**
```markdown
## Cross-Project Scope

### Primary Project
- perfect-skill-suggester

### Related Projects
- claude-plugins-validation (code dependency - uses validator)
- emasoft-plugins-marketplace (code dependency - submodule)

### Resources
- test-engineer-01 (shared with CPV)
```

### 3.3.2 Dependency mapping

**Purpose:** Graph relationships between projects.

**Dependency Graph:**
```
┌─────────────────────────────────────┐
│        Dependency Graph             │
├─────────────────────────────────────┤
│                                     │
│  ┌─────┐         ┌─────┐            │
│  │ CPV │ ◄────── │ PSS │            │
│  └──┬──┘         └──┬──┘            │
│     │               │               │
│     │    ┌─────┐    │               │
│     └───►│ EPM │◄───┘               │
│          └─────┘                    │
│                                     │
│  Legend:                            │
│  ──► depends on                     │
│                                     │
└─────────────────────────────────────┘
```

### 3.3.3 Coordination planning

**Purpose:** Schedule work across projects.

**Planning Steps:**
1. Identify critical path
2. Schedule independent work in parallel
3. Insert checkpoints between dependent phases
4. Allocate shared resources
5. Define sync points

**Coordination Plan:**
```markdown
## Coordination Plan: PSS Update

### Phase 1: Update CPV (Independent)
- Agent: code-impl-cpv
- Duration: 2 hours
- Checkpoint: CPV tests pass

### Phase 2: Update PSS (Depends on Phase 1)
- Agent: code-impl-pss
- Duration: 4 hours
- Checkpoint: PSS tests pass

### Phase 3: Update EPM (Depends on Phases 1 & 2)
- Agent: devops-epm
- Duration: 1 hour
- Checkpoint: Marketplace validation passes

### Sync Points
- After Phase 1: Notify PSS agent
- After Phase 2: Notify EPM agent
- After Phase 3: Notify Chief of Staff
```

### 3.3.4 Checkpoint execution

**Purpose:** Verify state at sync points.

**Checkpoint Types:**
- Test pass: All tests in project pass
- Build success: Project builds without errors
- Validation pass: Validation scripts succeed
- Manual approval: Human confirms readiness

**Checkpoint Procedure:**
1. Pause downstream work
2. Run checkpoint verification
3. If pass, notify downstream agents
4. If fail, notify upstream agent for fix
5. Resume when checkpoint satisfied

### 3.3.5 State reconciliation

**Purpose:** Ensure consistency across projects.

**Reconciliation Steps:**
1. After checkpoint, capture state of each project
2. Verify no conflicting changes
3. Update shared resources (submodules, configs)
4. Commit synchronized state
5. Document reconciliation

---

## 3.4 Communication patterns

### Pattern 1: Completion Notification

When a project phase completes, notify dependent projects.

Use the `agent-messaging` skill to send:
- **Recipient**: `code-impl-pss`
- **Subject**: `Dependency Ready`
- **Content**: type `dependency-ready`, message: "CPV validation library updated". Include `project`: "claude-plugins-validation", `version`: "1.3.0".

### Pattern 2: Blocking Request

When a project needs to block another for resource.

Use the `agent-messaging` skill to send:
- **Recipient**: `chief-of-staff`
- **Subject**: `Resource Request`
- **Priority**: `high`
- **Content**: type `resource-request`, message: "Need test-engineer-01 for PSS tests". Include `resource`: "test-engineer-01", `duration`: "30 minutes".

### Pattern 3: State Sync Request

When a project needs another to sync shared state.

Use the `agent-messaging` skill to send:
- **Recipient**: `code-impl-pss`
- **Subject**: `Sync Request`
- **Content**: type `sync-request`, message: "Please push PSS changes for submodule update". Include `sync_type`: "git-push".

---

## 3.5 Conflict resolution

### Conflict Type 1: Resource Contention

Two projects need same resource simultaneously.

**Resolution:**
1. Check priority of each project
2. Higher priority gets resource first
3. Lower priority waits or uses alternative
4. Schedule resource sharing window

### Conflict Type 2: Version Mismatch

Projects using incompatible versions of shared code.

**Resolution:**
1. Identify which version is correct
2. Update lagging project
3. Re-run affected tests
4. Document version requirements

### Conflict Type 3: Circular Dependency

Projects waiting for each other.

**Resolution:**
1. Identify the cycle
2. Break cycle by:
   - Defining clear order
   - Using intermediate state
   - Parallel development with integration point
3. Document to prevent recurrence

---

## 3.6 Examples

### Example: Three-Project Release

**Scenario:** Release new version of PSS requires updating CPV and EPM.

**Coordination Plan:**

```markdown
## Release Coordination: PSS 1.3.0

### Projects
- CPV: claude-plugins-validation (dependency)
- PSS: perfect-skill-suggester (primary)
- EPM: emasoft-plugins-marketplace (consumer)

### Phases

**Phase 1: CPV Update (2h)**
- Update validation rules
- Run CPV tests
- Checkpoint: CPV tests pass
- Push to GitHub

**Phase 2: PSS Update (4h)**
- Update PSS to use new CPV
- Add new features
- Run PSS tests (includes CPV validation)
- Checkpoint: PSS tests pass
- Push to GitHub

**Phase 3: EPM Update (1h)**
- Update PSS submodule in EPM
- Update CPV submodule in EPM
- Run marketplace validation
- Checkpoint: EPM validation pass
- Push to GitHub

### Checkpoints
1. After CPV: `cpv_tests_pass`
2. After PSS: `pss_tests_pass`
3. After EPM: `epm_validation_pass`

### Final: All three repos updated and consistent
```

---

## 3.7 Troubleshooting

### Issue: Deadlock between projects

**Symptoms:** Both projects waiting for each other.

**Resolution:**
1. Identify the dependency cycle
2. Determine which can proceed first
3. Manually advance one project
4. Add explicit ordering to prevent recurrence

### Issue: Submodule out of sync

**Symptoms:** Submodule points to old commit.

**Resolution:**
1. Navigate to parent project
2. Update submodule: `git submodule update --remote`
3. Commit submodule update
4. Verify downstream projects work

### Issue: Shared config conflicts

**Symptoms:** Projects overwriting each other's config changes.

**Resolution:**
1. Implement config locking
2. Merge config changes carefully
3. Use config versioning
4. Assign config ownership to one project

### Issue: Agent cannot switch projects

**Symptoms:** Agent context has wrong project.

**Resolution:**
1. Explicitly set project in agent message
2. Clear agent context if needed
3. Hibernate and wake with new project
4. Spawn new agent for different project
