# Record Patterns - Part 2: Examples & Troubleshooting

## Table of Contents
1. [For fundamentals and procedures](#related-documents)
2. [Complete problem-solution example](#example-1-record-problem-solution-pattern)
3. [Complete workflow example](#example-2-record-workflow-pattern)
4. [If pattern ID collision occurs](#problem-pattern-id-collision)
5. [If pattern index is out of sync](#problem-pattern-index-out-of-sync)
6. [If cannot find appropriate category](#problem-cannot-find-appropriate-category)
7. [If pattern is too large](#problem-pattern-too-large)
8. [If pattern never gets reused](#problem-pattern-never-gets-reused)

## Related Documents

- **Part 1**: [05-record-patterns-part1-fundamentals.md](./05-record-patterns-part1-fundamentals.md) - Categories, triggers, procedures, templates, index management

---

## Examples

### Example 1: Record Problem-Solution Pattern

```markdown
# Pattern: Git Authentication Failure in Parallel Agents

**Pattern ID**: ps_001
**Category**: Problem-Solution
**Created**: 2026-01-01 14:30 UTC

---

## Problem/Task

When spawning multiple agent instances in parallel, git operations fail with authentication errors despite working in single-agent mode.

**Symptoms**:
- `git push` fails with "Authentication failed"
- Error occurs only when >3 agents spawn simultaneously
- Single agent git operations work fine
- GitHub credentials are valid

---

## Context

**When this applies**:
- Orchestrator spawning multiple task agents
- Agents performing git operations (push, pull, clone)
- Using GitHub CLI (gh) for authentication

**Prerequisites**:
- GitHub CLI authenticated (`gh auth status`)
- Git configured with correct user
- Agents using shared credentials

---

## Solution/Procedure

### Step 1: Serialize Git Authentication Operations
Never spawn multiple agents that perform git auth simultaneously.

```bash
# Bad: Spawns all agents at once
for task in "${tasks[@]}"; do
    spawn_agent "$task" &
done
wait

# Good: Spawn with stagger delay
for task in "${tasks[@]}"; do
    spawn_agent "$task"
    sleep 2  # Prevent auth collision
done
```

### Step 2: Use Git Credential Cache
Enable credential caching to reduce auth requests:

```bash
git config --global credential.helper 'cache --timeout=3600'
```

### Step 3: Separate Auth from Operations
Agents should not authenticate - orchestrator handles it:

```bash
# Orchestrator: Ensure auth is valid before spawning agents
gh auth status || gh auth login

# Then spawn agents that use existing auth
spawn_multiple_agents
```

---

## Rationale

**Why this works**:
GitHub CLI has a rate limit on authentication requests. When multiple agents try to authenticate simultaneously, some fail due to rate limiting. By staggering spawns and caching credentials, we stay within rate limits.

**Why alternatives don't work**:
- Using SSH keys: Still hits rate limits on key verification
- Increasing timeout: Doesn't address rate limiting root cause
- Using personal access tokens: Same rate limit applies

---

## Examples

### Example 1: Parallel Testing Across Agents
**Situation**: Need to run tests in 5 parallel agents, each pushing results to git

**Application**:
```bash
# Authenticate once in orchestrator
gh auth status || gh auth login

# Enable credential cache
git config --global credential.helper 'cache --timeout=3600'

# Spawn agents with stagger
for i in {1..5}; do
    spawn_test_agent "test_suite_$i"
    sleep 2
done
```

**Outcome**: All agents successfully push test results without auth failures

---

## Verification

**How to verify success**:
1. Spawn multiple agents that perform git operations
2. Check agent logs for auth errors
3. Verify all git operations complete successfully

**Expected outcome**:
No authentication errors in any agent logs

---

## Related Patterns

- [wf_001]\(./workflow/wf_001_parallel-agent-spawning.md) - Parallel agent spawning best practices

---

## Notes

**Known Limitations**:
- Stagger delay adds time to agent spawning
- Not applicable to truly independent git repos (different auth)

**Additional Resources**:
- GitHub CLI rate limits: https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting
```

### Example 2: Record Workflow Pattern

```markdown
# Pattern: Parallel Test Execution Across Agents

**Pattern ID**: wf_001
**Category**: Workflow
**Created**: 2026-01-01 15:00 UTC

---

## Problem/Task

Execute large test suite efficiently by distributing tests across multiple parallel agent instances.

**Goal**: Reduce total test execution time from 30+ minutes to <10 minutes

---

## Context

**When this applies**:
- Large test suite (50+ test files)
- Tests are independent (no shared state)
- Orchestrator has capacity for multiple agents

**Prerequisites**:
- Test suite can be partitioned
- Test files don't interfere with each other
- Results can be aggregated

---

## Solution/Procedure

### Step 1: Partition Test Suite
Divide tests into roughly equal batches:

```bash
# Get all test files
test_files=(tests/**/*.test.ts)

# Calculate batch size for N agents
num_agents=5
batch_size=$(( (${#test_files[@]} + num_agents - 1) / num_agents ))

# Create batches
for ((i=0; i<num_agents; i++)); do
    start=$((i * batch_size))
    batch=("${test_files[@]:$start:$batch_size}")
    echo "${batch[@]}" > test_batch_$i.txt
done
```

### Step 2: Spawn Test Agents
Create agent for each batch with stagger delay:

```bash
for i in {0..4}; do
    spawn_agent "test_runner" \
        --batch "test_batch_$i.txt" \
        --output "results_$i.json"
    sleep 2  # Prevent resource contention
done
```

### Step 3: Monitor Progress
Track agent completion:

```bash
while true; do
    completed=$(ls results_*.json 2>/dev/null | wc -l)
    echo "Completed: $completed/$num_agents"
    [ $completed -eq $num_agents ] && break
    sleep 5
done
```

### Step 4: Aggregate Results
Combine results from all agents:

```bash
# Merge JSON results
jq -s 'add' results_*.json > final_results.json

# Generate summary
total_tests=$(jq '.total' final_results.json)
passed=$(jq '.passed' final_results.json)
failed=$(jq '.failed' final_results.json)

echo "Total: $total_tests, Passed: $passed, Failed: $failed"
```

---

## Rationale

**Why this works**:
- Tests run in parallel, reducing wall-clock time
- Each agent has dedicated resources
- No test interference due to proper partitioning

---

## Examples

### Example 1: TypeScript Unit Tests
**Situation**: 120 test files, ~25 minutes sequential execution

**Application**:
```bash
# 5 agents, ~24 files each
./partition_tests.sh 5
./spawn_test_agents.sh
./aggregate_results.sh
```

**Outcome**: Completed in 8 minutes (3x speedup)

---

## Verification

**How to verify success**:
1. All test files executed
2. No test duplicated across batches
3. Results properly aggregated
4. Total time < sequential time

---

## Related Patterns

- [ps_001]\(./problem_solution/ps_001_git-auth-failure.md) - Git auth in parallel agents
```

---

## Troubleshooting

### Problem: Pattern ID Collision

**Cause**: Multiple patterns created simultaneously

**Solution**:
```bash
# Check for existing ID before creating
if [ -f ".session_memory/patterns/$category/${pattern_id}_*.md" ]; then
    echo "ERROR: Pattern ID $pattern_id already exists"
    # Increment ID
    pattern_id="${prefix}_$(printf '%03d' $((next_num + 1)))"
fi
```

### Problem: Pattern Index Out of Sync

**Cause**: Pattern file created but index not updated

**Solution**:
```bash
# Rebuild entire index from files
./rebuild_pattern_index.sh
```

### Problem: Cannot Find Appropriate Category

**Cause**: Pattern doesn't fit existing categories

**Solution**:
```bash
# Create new category if truly needed (rare)
new_category="custom_category"
mkdir -p ".session_memory/patterns/$new_category"

# Update index to include new category
# Add to validation scripts
```

### Problem: Pattern Too Large

**Cause**: Trying to capture too much in one pattern

**Solution**:
```markdown
# Split into multiple related patterns
# Example: Large workflow split into:
- wf_001: Main workflow
- wf_002: Prerequisite setup
- wf_003: Result aggregation

# Link them together in "Related Patterns" section
```

### Problem: Pattern Never Gets Reused

**Cause**: Too specific or poorly indexed

**Solution**:
```bash
# Review pattern:
# - Is it truly reusable?
# - Is description clear in index?
# - Is it in correct category?

# If not reusable, move to docs_dev instead
mv .session_memory/patterns/category/pattern.md docs_dev/
```
