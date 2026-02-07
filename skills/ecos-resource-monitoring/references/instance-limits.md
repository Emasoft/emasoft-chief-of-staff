# Instance Limits Reference

## Table of Contents

- 2.1 [Types Of Instance Limits](#21-types-of-instance-limits)
- 2.2 [Counting Active Sessions](#22-counting-active-sessions)
- 2.3 [Tracking API Rate Limits](#23-tracking-api-rate-limits)
- 2.4 [Managing Concurrency](#24-managing-concurrency)
- 2.5 [Making Scaling Decisions](#25-making-scaling-decisions)
- 2.6 [Instance Limit Examples](#26-instance-limit-examples)
- 2.7 [Troubleshooting](#27-troubleshooting)

---

## 2.1 Types Of Instance Limits

Instance limits are constraints on how many agents and operations can run simultaneously.

### Session Limits

Maximum number of Claude Code sessions that can run:
- Limited by system resources (memory, CPU)
- Limited by license/subscription (if applicable)
- Practical limit for coordination efficiency

**Recommended limits:**
- Small projects: 5-10 sessions
- Medium projects: 10-20 sessions
- Large projects: 20-30 sessions (requires careful coordination)

### API Rate Limits

Limits on API calls to external services:
- Anthropic API rate limits
- AI Maestro message throughput
- GitHub API limits
- Other integrated services

### Concurrency Limits

Limits on simultaneous operations:
- Parallel tool executions
- Concurrent git operations
- Simultaneous file writes to same directory

### Message Queue Limits

Limits on message handling:
- Messages per minute
- Pending messages per agent
- Broadcast frequency

---

## 2.2 Counting Active Sessions

### Query AI Maestro Registry

Use the `ai-maestro-agents-management` skill to list all registered sessions. The skill returns session details including name, status, and last seen timestamp.

From the results:
- Count total sessions
- Count sessions by status (active, idle, offline)
- Note each session's last seen timestamp

### Session Categorization

Categorize sessions by role or domain by examining the session name prefixes:
- `eoa-` prefix: Orchestrator agents
- `eaa-` prefix: Architect agents
- `eia-` prefix: Integrator agents
- `epa-` or `<project>-programmer-` prefix: Programmer agents

### Session Count History

Track session counts over time in a markdown file:

```markdown
# design/memory/session-history.md

## Session Count History

| Timestamp | Total | Active | Idle | Notes |
|-----------|-------|--------|------|-------|
| 2025-02-01T08:00:00Z | 5 | 5 | 0 | Morning startup |
| 2025-02-01T10:00:00Z | 12 | 10 | 2 | Peak coordination |
| 2025-02-01T12:00:00Z | 8 | 6 | 2 | Post-sprint |
```

---

## 2.3 Tracking API Rate Limits

### Anthropic API Limits

Track usage against Anthropic API limits:

```markdown
## Anthropic API Usage

**Rate Limits (example - verify current limits):**
- Requests per minute: 60
- Tokens per minute: 100,000
- Requests per day: 10,000

**Current Usage (last hour):**
- Requests: 245
- Tokens: 45,000
- Trend: Stable
```

### AI Maestro Throughput

Use the `ai-maestro-agents-management` skill to get service statistics, including:
- Total message count
- Messages in the last hour
- Pending message count

### Rate Limit Headers

When making external API calls, capture rate limit headers:

```bash
# Example: Check GitHub rate limit using gh CLI
gh api rate_limit --jq '.rate | {limit, remaining, reset}'

# Example output:
# {"limit":5000,"remaining":4987,"reset":1706780400}
```

### Rate Limit Tracking File

```markdown
# design/memory/rate-limits.md

## Rate Limit Status

Last Updated: 2025-02-01T10:00:00Z

### Anthropic API
- Limit: 60 req/min
- Current Usage: 35 req/min
- Status: OK

### GitHub API
- Limit: 5000 req/hour
- Remaining: 4500
- Reset: 2025-02-01T11:00:00Z
- Status: OK

### AI Maestro
- Estimated capacity: 100 msg/min
- Current: 20 msg/min
- Status: OK
```

---

## 2.4 Managing Concurrency

### Tool Execution Concurrency

Manage how many tools run simultaneously:

**Safe concurrent operations:**
- Multiple file reads
- Multiple greps in different directories
- Parallel AI Maestro queries

**Operations requiring serialization:**
- Git operations (clone, pull, push, commit)
- File writes to same file
- Database migrations

### Git Concurrency Rule

Never run multiple git operations simultaneously:

```markdown
## Git Concurrency Rule

**CRITICAL: Only ONE git operation at a time across all agents**

Before any git operation:
1. Check if git lock exists
2. If locked, wait or queue operation
3. Acquire lock
4. Perform operation
5. Release lock

Lock file: design/memory/git.lock
```

### File Write Concurrency

Prevent write conflicts:

```markdown
## File Write Rules

1. **Different files:** Can write in parallel
2. **Same file:** Must coordinate or serialize
3. **Same directory with patterns:** Use unique names

Coordination methods:
- AI Maestro locking messages
- File-based locks
- Orchestrator assignment (only one agent writes to each file)
```

### Concurrency Tracking

```markdown
# design/memory/concurrency-status.md

## Active Operations

| Agent | Operation | Resource | Started | Status |
|-------|-----------|----------|---------|--------|
| orchestrator-master | git push | repo | 10:00:00 | In Progress |
| helper-agent-generic | file write | auth.py | 10:01:00 | In Progress |

## Queued Operations

| Agent | Operation | Resource | Queued | Waiting For |
|-------|-----------|----------|--------|-------------|
| libs-svg-svgbbox | git commit | repo | 10:02:00 | orchestrator-master |
```

---

## 2.5 Making Scaling Decisions

### When to Scale Up

Add more agents when:
- Workload exceeds current capacity
- Tasks are waiting due to agent unavailability
- Deadlines are at risk due to throughput
- Specialization is needed for new task types

**Scale-up checklist:**
- [ ] Resources available (memory > 30% free)
- [ ] Session limit not reached
- [ ] Coordination overhead acceptable
- [ ] Role and task defined for new agent

### When to Scale Down

Remove agents when:
- Workload has decreased
- Resources are constrained
- Coordination overhead exceeds benefit
- Tasks completed, no new work

**Scale-down checklist:**
- [ ] Agent has no in-progress tasks
- [ ] All assigned tasks transferred
- [ ] Agent acknowledged shutdown
- [ ] Roster updated

### Capacity Assessment

```markdown
## Capacity Assessment

Current State:
- Active Agents: 8
- Memory Usage: 65%
- CPU Load: 0.6/core
- Pending Tasks: 15
- Avg Task Duration: 30 min

Capacity Analysis:
- Current throughput: 16 tasks/hour
- Required throughput: 20 tasks/hour
- Gap: 4 tasks/hour

Recommendation: Add 2 Developer agents (25% capacity increase)

Constraints:
- Memory allows 4 more agents before warning threshold
- Session limit allows 12 more agents
- Coordination complexity: manageable at 10 agents
```

### Scaling Decision Matrix

| Condition | Action |
|-----------|--------|
| High workload + Resources available | Scale up |
| High workload + Resources constrained | Optimize or defer |
| Low workload + Many agents | Scale down |
| Critical deadline | Scale up if possible |
| Coordination issues | Scale down |

---

## 2.6 Instance Limit Examples

### Example: Pre-Spawn Resource Check

Before spawning a new agent, perform a resource check:

1. Use the `ai-maestro-agents-management` skill to list all agents and count the total sessions. Compare against the maximum session limit (default: 20).

2. Check system memory:
   ```bash
   # macOS
   memory_pressure | head -5

   # Linux
   free -m | awk '/^Mem:/ {printf("%.0f%% used\n", $3/$2 * 100)}'
   ```

3. If session count is at or above the limit, or memory usage exceeds 80%, do NOT spawn a new agent. Instead, consider hibernating idle agents first.

4. If resources are available, proceed with the spawn operation.

### Example: Rate Limit Monitoring

Periodically check rate limits across services:

1. Check GitHub API rate limit:
   ```bash
   gh api rate_limit --jq '.rate | {limit, remaining, reset}' 2>/dev/null
   ```

2. Use the `ai-maestro-agents-management` skill to get service statistics for AI Maestro message throughput.

3. Record results in `design/memory/rate-limits.md`.

### Example: Scaling Decision Log

```markdown
# Scaling Decision Log

## 2025-02-01T10:00:00Z - Scale Up

**Decision:** Add 2 Developer agents
**Reason:** Sprint deadline approaching, 20 tasks pending, current throughput insufficient
**Resources:** Memory at 60%, CPU at 0.5/core - headroom available
**Result:** agents helper-agent-dev-1 and helper-agent-dev-2 spawned

## 2025-02-01T16:00:00Z - Scale Down

**Decision:** Remove 3 agents
**Reason:** Sprint complete, minimal pending work
**Resources:** Memory at 75%, can recover capacity
**Agents removed:** helper-agent-dev-1, helper-agent-dev-2, helper-agent-backup
**Result:** Memory dropped to 55%
```

---

## 2.7 Troubleshooting

### Issue: Session count exceeds expected limit

**Symptoms:** More sessions than configured maximum.

**Possible causes:**
- Stale sessions not cleaned up
- Limit not enforced
- Sessions spawned without check

**Resolution:**
1. Use the `ai-maestro-agents-management` skill to list all agents and identify stale sessions
2. Force cleanup of inactive sessions using the skill
3. Enforce pre-spawn checks
4. Update session registry

### Issue: Rate limits being hit frequently

**Symptoms:** API calls failing with rate limit errors.

**Possible causes:**
- Too many agents making calls
- Inefficient API usage patterns
- Burst activity

**Resolution:**
1. Implement request batching
2. Add delays between calls
3. Reduce concurrent API users
4. Cache API responses where possible

### Issue: Git operations deadlock

**Symptoms:** Git operations hang, agents waiting indefinitely.

**Possible causes:**
- Lock not released after failure
- Multiple agents ignored locking
- Lock file corrupted

**Resolution:**
1. Check for stale lock: `cat design/memory/git.lock`
2. Verify lock holder is still active
3. Force release if holder is gone
4. Clear git lock file and retry

### Issue: Cannot spawn new agents despite available resources

**Symptoms:** Spawn fails but resources look OK.

**Possible causes:**
- Session name collision
- AI Maestro registry full
- Hidden resource constraint

**Resolution:**
1. Check for existing session with same name using the `ai-maestro-agents-management` skill
2. Use unique session name
3. Use the `ai-maestro-agents-management` skill to check service health
4. Review all resource constraints

---

**Version:** 1.0
**Last Updated:** 2025-02-01
