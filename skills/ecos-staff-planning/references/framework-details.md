# Staff Planning Framework Details

## Contents

- 1.0 Analyzing task requirements to determine staffing needs
  - 1.1 Classifying tasks by project type, complexity, and timeline
  - 1.2 Assessing task complexity to determine agent count
  - 1.3 Matching task requirements to agent specializations
  - 1.4 Evaluating resource constraints before staffing
  - 1.5 Identifying parallelization opportunities for concurrent work
- 2.0 Composing teams for different project types
  - 2.1 Staffing frontend projects with component-focused teams
  - 2.2 Staffing backend projects with API-focused teams
  - 2.3 Staffing full-stack projects with multi-layer teams
  - 2.4 Staffing DevOps projects with infrastructure teams
- 3.0 Allocating resources efficiently across agents
  - 3.1 Deciding when to recommend more agents for parallelization
  - 3.2 Deciding when to recommend fewer agents to reduce overhead
  - 3.3 Choosing between agents and sub-agents based on task duration
  - 3.4 Managing resource constraints and system limitations
- 4.0 Producing staffing recommendations in standardized format
  - 4.1 Writing staffing plans with task analysis and execution phases
  - 4.2 Documenting parallelization opportunities and dependencies
  - 4.3 Identifying risks and mitigation strategies
- 5.0 Following best practices for resource allocation
  - 5.1 Minimizing coordination overhead between agents
  - 5.2 Planning handoffs between execution phases
  - 5.3 Avoiding git conflicts in parallel work

---

## 1.0 Analyzing task requirements to determine staffing needs

### 1.1 Classifying tasks by project type, complexity, and timeline

**Procedure**: Classify the incoming task across five key dimensions to understand staffing requirements.

| Dimension | Options | Staffing Impact |
|-----------|---------|-----------------|
| **Project Type** | frontend, backend, full-stack, devops, documentation | Determines specialist roles needed |
| **Task Complexity** | simple, moderate, complex | Affects agent count |
| **Timeline** | urgent (<1 day), normal (1-7 days), extended (>7 days) | Affects parallelization |
| **Scope** | single-file, module, multi-module, system-wide | Affects coordination needs |
| **Dependencies** | isolated, loosely-coupled, tightly-coupled | Affects sequencing |

**How to classify**:

1. **Project Type**: Read the task description and identify whether it involves UI components (frontend), APIs/databases (backend), both (full-stack), infrastructure (devops), or written content (documentation).

2. **Task Complexity**: Assess the number of files, modules, and systems involved. Use the complexity tiers defined in section 1.2.

3. **Timeline**: Check if explicit deadlines exist. If urgent, parallelization becomes higher priority.

4. **Scope**: Count affected files and modules. Single-file = isolated. Module = contained. Multi-module = cross-cutting. System-wide = architectural.

5. **Dependencies**: Identify whether components can be worked on independently (isolated), need limited coordination (loosely-coupled), or require tight synchronization (tightly-coupled).

### 1.2 Assessing task complexity to determine agent count

**Procedure**: Use predefined complexity tiers to estimate required agent count.

**Simple Tasks** (1 agent, sub-agents optional):
- Single file modifications
- Bug fixes with clear scope
- Documentation updates
- Configuration changes
- Code formatting/linting

**Staffing recommendation**: One agent or sub-agent is sufficient. No coordination overhead needed.

**Moderate Tasks** (1-2 agents, sub-agents recommended):
- New feature in existing module
- Refactoring with limited scope
- Test suite expansion
- API endpoint additions
- Integration with single external service

**Staffing recommendation**: Primary agent for implementation, sub-agents for support tasks (testing, review).

**Complex Tasks** (2-4 agents, full team coordination):
- New module development
- Cross-cutting refactoring
- Multi-service integration
- Major architectural changes
- Full-stack feature development
- CI/CD pipeline setup

**Staffing recommendation**: Full team with defined roles. Architect for design, Orchestrators for parallel implementation, Integrator for testing and review.

### 1.3 Matching task requirements to agent specializations

**Procedure**: Map task types to available agent roles based on specialization.

| Task Type | Primary Agent | Supporting Agents |
|-----------|---------------|-------------------|
| Architecture design | Architect | Planner |
| Implementation planning | Architect | Orchestrator |
| Code implementation | Orchestrator | Experimenter, DevOps |
| Code review | Integrator | Code Reviewer |
| Testing | Integrator | Test Engineer |
| Deployment | Integrator | DevOps, Docker Expert |
| Bug investigation | Integrator | Debug Specialist, Bug Investigator |
| Documentation | Architect | Documentation Writer |
| API integration | Orchestrator | API Coordinator |

**How to match**:

1. Identify the primary task type (architecture, implementation, review, testing, etc.)
2. Assign the primary agent role with relevant specialization
3. Identify supporting tasks that can be delegated to sub-agents
4. Ensure no role conflicts (e.g., don't assign same sub-agent to parallel tasks)

### 1.4 Evaluating resource constraints before staffing

**Procedure**: Check system limitations to ensure staffing plan is feasible.

| Constraint | Threshold | Recommendation |
|------------|-----------|----------------|
| **Max concurrent agents** | 4-6 | Queue additional work |
| **Context memory** | ~100K tokens per agent | Split large tasks |
| **tmux sessions** | System-dependent | Monitor with `tmux list-sessions` |
| **API rate limits** | Provider-dependent | Stagger agent starts |
| **Disk I/O** | Check with `df -h` | Avoid parallel writes to same files |

**How to check constraints**:

- **Check tmux sessions**: Run `tmux list-sessions` in the terminal
- **Check disk space**: Run `df -h "${CLAUDE_PROJECT_DIR:-$HOME}"` in the terminal
- **Check running agents**: Use the `ai-maestro-agents-management` skill to list all agents and their status
- **Check agent workload**: Use the `agent-messaging` skill to check pending messages count

**Interpretation**:
- If max concurrent agents reached, recommend queuing or sequential phasing
- If context memory near limit, recommend splitting tasks across agents
- If disk space low, recommend cleanup before proceeding
- If many pending messages, recommend waiting for agent availability

### 1.5 Identifying parallelization opportunities for concurrent work

**Procedure**: Analyze task structure to find independent workstreams.

**CAN parallelize:**
- Independent file modifications
- Tests for different modules
- Documentation for different features
- Code review and test writing (if reviewing different code)

**CANNOT parallelize:**
- Git operations (auth conflicts, repo corruption)
- Modifications to same files
- Sequential dependencies (A must complete before B)
- Database migrations (ordering matters)

**How to identify**:

1. List all subtasks in the project
2. For each subtask, identify its inputs (files read) and outputs (files written)
3. Two subtasks can run in parallel if:
   - They do not write to the same files
   - They do not perform git operations
   - One's output is not the other's input (no dependency)
4. Group parallelizable subtasks into "phases" of concurrent work
5. Sequence phases where dependencies exist

---

## 2.0 Composing teams for different project types

### 2.1 Staffing frontend projects with component-focused teams

**Template**:

```
Recommended Team:
- 1x Architect (design, component structure)
- 1x Orchestrator (implementation coordination)
- 1x Integrator (testing, review, deployment)

Sub-agents:
- Code Reviewer (per PR)
- Test Engineer (component tests)
- Screenshot Analyzer (visual regression)
```

**Rationale**:
- Architect defines component hierarchy, state management, and UI patterns
- Orchestrator implements components, handles styling, and coordinates frontend logic
- Integrator runs tests, performs visual regression checks, and deploys
- Sub-agents handle repetitive tasks (review each PR, write tests for each component)

**When to use**: Task involves React/Vue/Angular components, CSS/styling, browser APIs, or frontend build tools.

### 2.2 Staffing backend projects with API-focused teams

**Template**:

```
Recommended Team:
- 1x Architect (API design, data modeling)
- 1x Orchestrator (implementation)
- 1x Integrator (testing, review)

Sub-agents:
- API Coordinator (external integrations)
- Test Engineer (unit + integration tests)
- Debug Specialist (issue investigation)
```

**Rationale**:
- Architect designs REST/GraphQL endpoints, database schema, and service architecture
- Orchestrator implements business logic, database queries, and API routes
- Integrator writes integration tests, reviews code, and validates API contracts
- Sub-agents handle external API integration and debugging edge cases

**When to use**: Task involves REST APIs, GraphQL, database models, authentication, or server-side logic.

### 2.3 Staffing full-stack projects with multi-layer teams

**Template**:

```
Recommended Team:
- 1x Architect (overall design)
- 2x Orchestrator (frontend + backend)
- 1x Integrator (integration, review, deploy)

Sub-agents:
- Code Reviewer (per PR)
- Test Engineer (full-stack tests)
- DevOps Expert (infrastructure)
```

**Rationale**:
- Architect designs end-to-end architecture, API contracts, and data flow
- Two Orchestrators work in parallel: one on frontend, one on backend
- Integrator ensures frontend and backend integrate correctly, writes E2E tests, and deploys
- Sub-agents handle code review, test writing, and infrastructure setup

**When to use**: Task involves both UI and server components, requires frontend-backend integration, or needs E2E testing.

### 2.4 Staffing DevOps projects with infrastructure teams

**Template**:

```
Recommended Team:
- 1x Architect (infrastructure design)
- 1x Orchestrator (automation scripts)
- 1x Integrator (validation, rollout)

Sub-agents:
- Docker Container Expert (containerization)
- DevOps Expert (CI/CD, monitoring)
```

**Rationale**:
- Architect designs infrastructure topology, networking, and deployment strategy
- Orchestrator writes Dockerfiles, CI/CD pipelines, and infrastructure-as-code
- Integrator validates deployments, monitors rollout, and verifies infrastructure health
- Sub-agents handle container optimization and CI/CD configuration

**When to use**: Task involves Docker, Kubernetes, CI/CD pipelines, infrastructure-as-code, or deployment automation.

---

## 3.0 Allocating resources efficiently across agents

### 3.1 Deciding when to recommend more agents for parallelization

**Conditions that justify multiple agents**:

- Task has clear parallelization opportunities (independent modules, separate layers)
- Deadline is tight and work can be split without coordination overhead
- Different specializations needed (e.g., frontend + backend expertise)
- Independent modules can be developed simultaneously without conflicts

**How to decide**:

1. Estimate time for single-agent execution
2. Identify parallelizable subtasks
3. Calculate time with multiple agents (original time / N agents + coordination overhead)
4. If parallelized time + overhead < single-agent time, recommend multiple agents

**Example**: Full-stack feature with frontend (2 days) + backend (2 days) + integration (1 day) = 5 days single-agent. With 2 agents: frontend and backend in parallel (2 days) + integration (1 day) + coordination (0.5 days) = 3.5 days. **Recommend 2 agents.**

### 3.2 Deciding when to recommend fewer agents to reduce overhead

**Conditions that justify single agent or sub-agents**:

- Task is tightly coupled with many dependencies between components
- Limited system resources available (CPU, memory, tmux sessions)
- Simple scope that one agent can handle efficiently
- Coordination overhead would exceed parallelization benefit

**How to decide**:

1. Count dependencies between subtasks
2. If >50% of subtasks depend on each other, coordination overhead is high
3. Estimate coordination time: ~10-20% of total time per additional agent
4. If coordination overhead > parallelization benefit, recommend fewer agents

**Example**: Refactoring tightly-coupled service layer with 10 files. All files share common interfaces and must be updated consistently. Parallelizing would require constant synchronization. **Recommend 1 agent.**

### 3.3 Choosing between agents and sub-agents based on task duration

**Decision tree**:

```
Is the task long-running (>30 min)?
  YES -> Agent
  NO -> Is persistent state needed?
    YES -> Agent
    NO -> Is parent context needed?
      YES -> Sub-agent
      NO -> Is parallelization with parent needed?
        YES -> Agent
        NO -> Sub-agent
```

**Agent** (separate Claude Code instance):
- Long-running tasks (hours to days)
- Tasks requiring persistent state
- Tasks that may outlive the parent session
- Parallel workstreams that should not block each other

**Sub-agent** (Task tool spawn within same instance):
- Quick operations (minutes)
- Tasks that need parent context
- Sequential steps in a workflow
- Operations that must complete before proceeding

**When to use**: Apply this decision tree to every subtask in the staffing plan.

### 3.4 Managing resource constraints and system limitations

**Constraints to monitor**:

| Constraint | Check Command | Threshold | Action |
|------------|---------------|-----------|--------|
| Concurrent agents | Use `ai-maestro-agents-management` skill to list agents | 4-6 agents | Queue additional work |
| Context memory | Check task size | ~100K tokens per agent | Split large tasks |
| Disk space | `df -h "${CLAUDE_PROJECT_DIR}"` | <10% free | Cleanup or use different volume |
| Pending messages | Use `agent-messaging` skill to check pending count | >20 messages | Wait for agents to catch up |

**Action plan when constrained**:

1. **Too many concurrent agents**: Recommend phased execution. Complete Phase 1 agents before starting Phase 2.
2. **Context memory limit**: Split large tasks into smaller chunks. Each agent handles one chunk.
3. **Low disk space**: Recommend cleanup (delete logs, build artifacts) before proceeding.
4. **High message backlog**: Recommend delaying new agent spawns until existing agents complete current work.

---

## 4.0 Producing staffing recommendations in standardized format

### 4.1 Writing staffing plans with task analysis and execution phases

**Standard format**:

```markdown
## Staffing Plan: [Task/Project Name]
Generated: [ISO timestamp]

### Task Analysis

| Dimension | Assessment |
|-----------|------------|
| Project Type | [frontend/backend/full-stack/devops/documentation] |
| Complexity | [simple/moderate/complex] |
| Timeline | [urgent/normal/extended] |
| Scope | [single-file/module/multi-module/system-wide] |
| Dependencies | [isolated/loosely-coupled/tightly-coupled] |

### Recommended Staffing

| Role | Agent Type | Assignment | Justification |
|------|------------|------------|---------------|
| [role] | [agent/sub-agent] | [agent name] | [why this agent] |

### Execution Plan

1. **Phase 1**: [description]
   - Agents: [list]
   - Duration: [estimate]
   - Parallelizable: [yes/no]

2. **Phase 2**: [description]
   - Agents: [list]
   - Duration: [estimate]
   - Dependencies: [Phase 1 completion]

### Resource Requirements

- Total Agents: [N]
- Max Concurrent: [M]
- Estimated Duration: [time]
- Critical Path: [sequence]
```

**How to write**:

1. **Task Analysis**: Fill in classification from section 1.1
2. **Recommended Staffing**: List each role from section 1.3 matching
3. **Execution Plan**: Group subtasks into phases from section 1.5 parallelization analysis
4. **Resource Requirements**: Summarize totals

### 4.2 Documenting parallelization opportunities and dependencies

**Add to staffing plan**:

```markdown
### Parallelization Opportunities

| Task A | Task B | Can Parallel | Notes |
|--------|--------|--------------|-------|
| Frontend implementation | Backend API | Yes | Independent layers |
| Database migration | API implementation | No | API depends on schema |
| Test writing | Code review | Yes | Different code artifacts |
```

**How to document**:

1. List all subtasks from execution plan
2. For each pair of subtasks, determine if they can run in parallel (see section 1.5)
3. Add "Notes" column explaining why or why not
4. This helps Chief of Staff understand why certain agents must wait for others

### 4.3 Identifying risks and mitigation strategies

**Add to staffing plan**:

```markdown
### Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Git conflicts from parallel edits | Medium | High | Assign different file sets to each agent |
| Context memory overflow | Low | Medium | Split large refactoring into phases |
| API rate limiting | Low | Low | Stagger agent start times by 5 minutes |
| Integration test failures | Medium | Medium | Reserve Integrator for full test pass before merge |
```

**Common risks**:

- **Git conflicts**: Multiple agents editing same files. **Mitigation**: Partition file sets.
- **Context overflow**: Large tasks exceed agent context window. **Mitigation**: Split into smaller subtasks.
- **Resource exhaustion**: Too many concurrent agents. **Mitigation**: Phased execution.
- **Dependency blocking**: Agent waiting for another's output. **Mitigation**: Clear phase sequencing.

---

## 5.0 Following best practices for resource allocation

### 5.1 Minimizing coordination overhead between agents

**Principle**: Each additional agent adds coordination cost. Ensure benefit exceeds cost.

**Coordination overhead sources**:
- Handoffs between agents (passing context, explaining prior work)
- Synchronization points (waiting for shared dependencies)
- Conflict resolution (merge conflicts, API contract changes)
- Communication delays (messages, status updates)

**How to minimize**:

1. **Clear role boundaries**: Each agent owns distinct files/modules. No overlap.
2. **Explicit interfaces**: Define API contracts, data structures upfront. No mid-flight changes.
3. **Asynchronous work**: Agents work independently, synchronize only at phase boundaries.
4. **Batch communication**: Use AI Maestro messages for updates, not real-time chat.

**Example**: Instead of 3 agents all working on the same module with constant coordination, assign Agent A to auth module, Agent B to billing module, Agent C to reporting module. They synchronize once at integration phase.

### 5.2 Planning handoffs between execution phases

**Procedure**: Define clear handoff points where one agent completes work and another begins.

**Handoff checklist**:
- [ ] Prior agent completes assigned work
- [ ] Prior agent writes handoff document with context, decisions, and open issues
- [ ] Prior agent commits all changes to git
- [ ] Handoff document location shared via AI Maestro message
- [ ] Next agent reads handoff document before starting work
- [ ] Next agent acknowledges receipt and understanding

**Handoff document template**:

```markdown
# Handoff: [Phase Name] to [Next Phase]

## Completed Work
- [List of completed subtasks]
- [Files modified]
- [Commits made]

## Decisions Made
- [Architectural decisions]
- [Trade-offs chosen]

## Open Issues
- [Unresolved questions]
- [Known limitations]

## Context for Next Agent
- [Important background]
- [Where to start]
```

**When to handoff**: At end of each execution phase in the staffing plan.

### 5.3 Avoiding git conflicts in parallel work

**Principle**: Never allow multiple agents to perform git operations simultaneously or edit the same files.

**Rules**:
- **ONE agent owns git operations per branch** (typically Integrator)
- **Other agents work on separate feature branches** and notify Integrator when ready to merge
- **Never parallelize**: commits, pushes, pulls, merges, rebases
- **Partition file ownership**: Assign disjoint file sets to each agent

**File partitioning example**:

| Agent | Assigned Files | Can Edit |
|-------|----------------|----------|
| Orchestrator A | `src/frontend/*` | Yes |
| Orchestrator B | `src/backend/*` | Yes |
| Integrator | `tests/integration/*`, `README.md` | Yes |
| Orchestrator A | `src/backend/*` | **NO** |

**How to enforce**:

1. In staffing plan, explicitly list assigned files for each agent
2. Agents must check assigned files before editing
3. If agent needs to edit file outside assignment, request via AI Maestro message
4. Integrator merges all branches and resolves conflicts centrally

---

## Checklist for Staffing Plans

Use this checklist to validate every staffing plan before submitting to Chief of Staff:

- [ ] Task complexity correctly assessed (simple/moderate/complex)
- [ ] Project type identified (frontend/backend/full-stack/devops/documentation)
- [ ] Timeline constraints considered (urgent/normal/extended)
- [ ] All required roles covered (Architect, Orchestrator, Integrator as needed)
- [ ] Parallelization opportunities identified and documented
- [ ] Resource constraints verified (max concurrent agents, context memory, disk space)
- [ ] Dependencies mapped between subtasks and phases
- [ ] Risks documented with mitigation strategies
- [ ] Execution phases defined with clear boundaries
- [ ] Duration estimates provided for each phase
- [ ] Critical path identified (longest sequence of dependent tasks)
- [ ] Handoff points specified between phases
- [ ] File ownership partitioned to avoid git conflicts
- [ ] Agent vs sub-agent decisions justified
- [ ] Staffing recommendation format followed exactly

---

**Remember**: The goal is **accurate assessment and optimal resource allocation**. Every recommendation must be justified by the analysis framework in this document.
