---
operation: plan-agent-capacity
procedure: proc-evaluate-project
workflow-instruction: Step 2 - Chief of Staff Evaluates Project
parent-skill: ecos-staff-planning
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Plan Agent Capacity


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Create Agent Inventory](#step-1-create-agent-inventory)
- [Agent Inventory](#agent-inventory)
  - [Step 2: Estimate Task Requirements](#step-2-estimate-task-requirements)
  - [Step 3: Calculate Task Allocation](#step-3-calculate-task-allocation)
  - [Step 4: Identify Bottlenecks](#step-4-identify-bottlenecks)
  - [Step 5: Recommend Mitigations](#step-5-recommend-mitigations)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Sprint Capacity Planning](#example-sprint-capacity-planning)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)
- [Detailed Reference](#detailed-reference)

## When to Use

Perform this operation when:
- Scheduling work across available agents
- Handling resource conflicts between competing tasks
- Optimizing throughput for a set of tasks
- Identifying bottlenecks in current allocation
- Making scaling decisions (add or remove agents)

## Prerequisites

- Role assessment completed (know what agent types are needed)
- Task list with estimates available
- Agent registry access to check current agent status
- Understanding of project timeline and deadlines

## Procedure

### Step 1: Create Agent Inventory

List all available agents and their current status:

1. Query the agent registry for active agents
2. Record each agent's type and unique identifier
3. Check the health status of each agent (RUNNING, IDLE, ERROR)
4. Note current utilization percentage for each agent
5. Flag any agents at or near capacity limits

**Output Format:**
```markdown
## Agent Inventory
| Agent ID | Type | Status | Utilization |
|----------|------|--------|-------------|
| code-impl-01 | code-implementer | RUNNING | 60% |
| test-eng-01 | test-engineer | IDLE | 0% |
```

### Step 2: Estimate Task Requirements

Size each task for capacity planning:

1. List all tasks that need to be completed
2. For each task, estimate:
   - **Complexity:** Simple, Medium, Complex
   - **Duration:** Expected time to complete
   - **Context tokens:** Approximate token usage
   - **Dependencies:** What must complete first
3. Use the estimation table below as a guide

**Estimation Reference:**

| Complexity | Duration | Context Tokens |
|------------|----------|----------------|
| Simple | 15-30 min | 5-10K tokens |
| Medium | 1-2 hours | 20-40K tokens |
| Complex | 4-8 hours | 50-80K tokens |

### Step 3: Calculate Task Allocation

Assign tasks to agents optimally:

1. Sort tasks by priority (CRITICAL tasks first)
2. Sort agents by availability (IDLE agents first)
3. For each task in priority order:
   - Find a capable agent with lowest utilization
   - Check if the agent has capacity for the task
   - If capacity available: assign task, update utilization
   - If no capacity: mark task as BLOCKED, note the constraint
4. Calculate estimated completion time for each assignment

**Output Format:**
```markdown
| Task | Agent | Start | Duration | Status |
|------|-------|-------|----------|--------|
| Auth module | code-impl-01 | Now | 2h | ASSIGNED |
| Auth tests | test-eng-01 | After auth | 1h | PENDING |
```

### Step 4: Identify Bottlenecks

Find constraints limiting throughput:

1. Look for single-instance agents with queued tasks
2. Identify sequential dependencies creating chains
3. Check for shared resources (same files, same APIs)
4. Note external dependencies (rate limits, user input)
5. Calculate the impact of each bottleneck

**Common Bottleneck Types:**
- **Singleton bottleneck:** Only one agent of needed type
- **Dependency bottleneck:** Tasks waiting for prior completion
- **Resource bottleneck:** Shared resource creates contention
- **External bottleneck:** External system limits throughput

### Step 5: Recommend Mitigations

For each bottleneck, propose a mitigation:

1. Singleton: Can we spawn another instance?
2. Dependency: Can tasks be reordered or parallelized?
3. Resource: Can we batch operations or stagger access?
4. External: Can we cache results or reduce calls?

Document each bottleneck and its mitigation in the capacity plan.

## Checklist

Copy this checklist and track your progress:

- [ ] Query agent registry for available agents
- [ ] Record agent types, IDs, and status
- [ ] Check health status of each agent
- [ ] Note current utilization percentages
- [ ] List all tasks requiring agents
- [ ] Estimate complexity for each task
- [ ] Estimate duration for each task
- [ ] Estimate context token usage
- [ ] Identify task dependencies
- [ ] Sort tasks by priority
- [ ] Assign tasks to available agents
- [ ] Calculate utilization after assignments
- [ ] Identify all bottlenecks
- [ ] Document mitigation for each bottleneck
- [ ] Compile capacity plan document

## Examples

### Example: Sprint Capacity Planning

**Scenario:** Plan capacity for a 2-week sprint with 5 features.

**Step 1 - Agent Inventory:**
```
| Agent ID | Type | Status | Utilization |
|----------|------|--------|-------------|
| code-impl-01 | code-implementer | IDLE | 0% |
| code-impl-02 | code-implementer | IDLE | 0% |
| test-eng-01 | test-engineer | IDLE | 0% |
| doc-01 | doc-writer | IDLE | 0% |
```

**Step 2 - Task Estimation:**
```
| Feature | Complexity | Duration | Agent Type |
|---------|------------|----------|------------|
| F1-Auth | Complex | 8h | code-implementer |
| F2-Profile | Medium | 4h | code-implementer |
| F3-Settings | Simple | 2h | code-implementer |
| F4-Notifications | Medium | 4h | code-implementer |
| F5-Export | Simple | 2h | code-implementer |
| Test all | Complex | 8h | test-engineer |
| Docs | Medium | 4h | doc-writer |
```

**Step 3 - Allocation:**
```
| Task | Agent | Start | End | Status |
|------|-------|-------|-----|--------|
| F1-Auth | code-impl-01 | Day 1 | Day 1 | ASSIGNED |
| F2-Profile | code-impl-02 | Day 1 | Day 1 | ASSIGNED |
| F3-Settings | code-impl-01 | Day 2 | Day 2 | PENDING |
| F4-Notifications | code-impl-02 | Day 2 | Day 2 | PENDING |
| F5-Export | code-impl-01 | Day 2 | Day 2 | PENDING |
| Test all | test-eng-01 | Day 3 | Day 4 | PENDING |
| Docs | doc-01 | Day 4 | Day 4 | PENDING |
```

**Step 4 - Bottlenecks:**
```
1. test-engineer singleton
   - Only 1 instance available
   - All test tasks serialize through it
   - Impact: 8h sequential wait

2. Testing depends on all features
   - Cannot start until features complete
   - Impact: 2 days delay minimum
```

**Step 5 - Mitigations:**
```
1. test-engineer singleton
   - Mitigation: Parallelize test runs where possible
   - Alternative: Start testing features as they complete

2. Feature dependency
   - Mitigation: Start testing F1 while F4/F5 still in progress
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| All agents at capacity | More work than agents can handle | Scale up with more agents; defer lower priority tasks |
| Agents mostly idle | Blocking dependencies | Check for hidden blockers; start independent work |
| Single agent is bottleneck | Type has only one instance | Spawn another instance; accept constraint and plan around it |
| Task estimates way off | Poor estimation | Track actual vs estimated; refine estimation factors |

## Related Operations

- [op-assess-role-requirements.md](op-assess-role-requirements.md) - Must complete role assessment before capacity planning
- [op-create-staffing-templates.md](op-create-staffing-templates.md) - Capture working capacity patterns as templates

## Detailed Reference

For comprehensive details on capacity planning methodology, see [capacity-planning.md](capacity-planning.md).
