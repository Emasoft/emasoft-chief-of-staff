# Capacity Planning Reference

## Table of Contents

- 2.1 What is capacity planning - Understanding capacity constraints
- 2.2 Capacity metrics - Measuring agent capacity
  - 2.2.1 Context window utilization - Token budget tracking
  - 2.2.2 Concurrent execution limits - Parallel task boundaries
  - 2.2.3 Blocking operation impact - Synchronous wait times
- 2.3 Capacity planning procedure - Step-by-step planning
  - 2.3.1 Agent inventory - Listing available agents
  - 2.3.2 Task estimation - Sizing work items
  - 2.3.3 Allocation calculation - Assigning agents to tasks
  - 2.3.4 Bottleneck identification - Finding constraints
- 2.4 Load balancing strategies - Distributing work evenly
- 2.5 Scaling decisions - When to add more agents
- 2.6 Examples - Capacity planning scenarios
- 2.7 Troubleshooting - Capacity planning issues

---

## 2.1 What is capacity planning

Capacity planning is the process of determining how much work agents can handle and allocating tasks accordingly. It considers:

- **Available capacity:** How much work can agents perform?
- **Required capacity:** How much work needs to be done?
- **Constraints:** What limits throughput?
- **Optimization:** How to maximize efficiency?

Capacity planning prevents overload and identifies bottlenecks before they block work.

---

## 2.2 Capacity metrics

### 2.2.1 Context window utilization

Each agent has a context window with token limits:

| Metric | Description | Threshold |
|--------|-------------|-----------|
| Current tokens | Tokens used in current context | Monitor |
| Max tokens | Context window size | Hard limit |
| Utilization % | Current / Max * 100 | Warning at 70% |
| Compaction trigger | When to compact context | 80% |

**Tracking:**
```
Context: 45,000 / 100,000 tokens (45%)
Status: HEALTHY
Action: Continue normal operation
```

### 2.2.2 Concurrent execution limits

Agents have limits on parallel work:

| Limit Type | Description | Typical Value |
|------------|-------------|---------------|
| Task parallelism | Simultaneous tasks per agent | 1 (sequential) |
| Agent parallelism | Simultaneous agents | 20 (subagent limit) |
| API rate limits | Requests per minute | Varies by tier |

### 2.2.3 Blocking operation impact

Certain operations block agent progress:

| Operation | Typical Duration | Impact |
|-----------|------------------|--------|
| Test suite run | 1-30 minutes | High (agent waits) |
| Build process | 2-10 minutes | Medium |
| External API call | 1-60 seconds | Low |
| User input wait | Indefinite | Critical |

---

## 2.3 Capacity planning procedure

### 2.3.1 Agent inventory

**Purpose:** List all available agents and their capacity.

**Steps:**
1. Query agent registry for active agents
2. Record agent types and counts
3. Check agent health status
4. Note any agents at capacity limits

**Output Format:**
```markdown
## Agent Inventory
| Agent ID | Type | Status | Utilization |
|----------|------|--------|-------------|
| code-impl-01 | code-implementer | RUNNING | 60% |
| test-eng-01 | test-engineer | IDLE | 0% |
```

### 2.3.2 Task estimation

**Purpose:** Estimate work required for each task.

**Estimation Factors:**
- Task complexity (simple, medium, complex)
- Dependencies (blocked, ready, in-progress)
- Expected duration (hours/minutes)
- Context requirements (tokens needed)

**Estimation Table:**

| Task Complexity | Duration | Context |
|-----------------|----------|---------|
| Simple | 15-30 min | 5-10K tokens |
| Medium | 1-2 hours | 20-40K tokens |
| Complex | 4-8 hours | 50-80K tokens |

### 2.3.3 Allocation calculation

**Purpose:** Assign tasks to agents optimally.

**Algorithm:**
1. Sort tasks by priority (CRITICAL first)
2. Sort agents by availability (IDLE first)
3. For each task:
   - Find capable agent with lowest utilization
   - Check if agent has capacity for task
   - Assign task if capacity available
   - Mark task as blocked if no capacity

**Allocation Table:**
```markdown
| Task | Agent | Start | Duration | Status |
|------|-------|-------|----------|--------|
| Auth module | code-impl-01 | Now | 2h | ASSIGNED |
| Auth tests | test-eng-01 | After auth | 1h | PENDING |
```

### 2.3.4 Bottleneck identification

**Purpose:** Find constraints limiting throughput.

**Common Bottlenecks:**
- Single-instance agents (test-engineer)
- Sequential dependencies (must wait for prior task)
- Shared resources (same file being edited)
- External dependencies (API rate limits)

**Bottleneck Report:**
```markdown
## Bottlenecks Identified

1. **test-engineer singleton**
   - Only 1 instance available
   - 5 tasks queued waiting
   - Mitigation: Prioritize critical tests

2. **Auth module dependency**
   - 3 tasks blocked on auth completion
   - Estimated unblock: 2 hours
   - Mitigation: None (hard dependency)
```

---

## 2.4 Load balancing strategies

### Strategy 1: Round-Robin

Distribute tasks evenly across agents of same type.

**When to use:** Tasks are similar complexity, agents are equivalent.

### Strategy 2: Least-Loaded

Assign to agent with lowest current utilization.

**When to use:** Task complexity varies, want even distribution.

### Strategy 3: Affinity-Based

Assign to agent already working on related code.

**When to use:** Context switching is expensive, agent has relevant context.

### Strategy 4: Priority-Based

Reserve capacity for high-priority tasks.

**When to use:** Critical tasks must not wait.

---

## 2.5 Scaling decisions

### When to scale up (add agents)

- All agents at >80% utilization
- Task queue growing faster than completion
- Critical tasks waiting more than threshold
- New capability needed

### When to scale down (remove agents)

- Agents idle for extended period
- Task queue empty
- Project phase complete
- Resource constraints

### Scaling procedure

1. Monitor utilization over time window (not instant)
2. Calculate trend (increasing, stable, decreasing)
3. If increasing and >70%, consider scaling up
4. If decreasing and <30%, consider scaling down
5. Execute scaling decision via agent lifecycle procedures

---

## 2.6 Examples

### Example: Sprint Planning

**Scenario:** Plan capacity for 2-week sprint with 10 features.

**Agent Inventory:**
- 2x code-implementer
- 1x test-engineer
- 1x doc-writer

**Task Estimation:**
| Feature | Complexity | Duration | Agent Type |
|---------|------------|----------|------------|
| F1-Auth | Complex | 8h | code-impl |
| F2-Profile | Medium | 4h | code-impl |
| F3-Settings | Simple | 2h | code-impl |
| ... | ... | ... | ... |

**Capacity Calculation:**
- Sprint hours: 80h per agent (2 weeks)
- Code capacity: 2 x 80 = 160h
- Code required: 80h (sum of features)
- Utilization: 50% (healthy headroom)

**Bottleneck:** test-engineer at 100% if all tests run sequentially.

**Mitigation:** Parallelize test runs where possible.

---

## 2.7 Troubleshooting

### Issue: Agents constantly at capacity

**Symptoms:** All agents >90% utilized, tasks queueing.

**Resolution:**
1. Review task estimates (over-estimating?)
2. Identify tasks that can be deferred
3. Scale up with additional agents
4. Reduce scope if possible

### Issue: Agents mostly idle

**Symptoms:** Agents <30% utilized, wasted capacity.

**Resolution:**
1. Check for blocking dependencies
2. Look for hidden work not tracked
3. Consider hibernating idle agents
4. Review if all agents needed

### Issue: Single agent is bottleneck

**Symptoms:** One agent at 100%, others waiting.

**Resolution:**
1. Can another agent type partially help?
2. Can tasks be reordered to reduce blocking?
3. Can we spawn another instance of bottleneck agent?
4. Accept the constraint and plan around it
