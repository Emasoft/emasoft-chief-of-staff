# Hibernation Procedures Reference

## Table of Contents

- 3.1 What is agent hibernation - Understanding state suspension
- 3.2 When to hibernate agents - Hibernation triggers
  - 3.2.1 Idle timeout - No activity for threshold period
  - 3.2.2 Resource pressure - System capacity constrained
  - 3.2.3 Scheduled pause - Planned inactivity window
- 3.3 Hibernation procedure - Step-by-step suspension
  - 3.3.1 Idle confirmation - Verifying no active work
  - 3.3.2 State capture - Serializing agent state
  - 3.3.3 State persistence - Writing to storage
  - 3.3.4 Resource release - Freeing memory and connections
  - 3.3.5 Registry update - Marking as hibernated
- 3.4 State snapshot format - Hibernation state structure
- 3.5 Wake procedure - Resuming hibernated agents
  - 3.5.1 State retrieval - Loading from storage
  - 3.5.2 State restoration - Deserializing agent state
  - 3.5.3 Resource reacquisition - Reconnecting services
  - 3.5.4 Registry update - Marking as running
  - 3.5.5 Work resumption - Continuing interrupted tasks
- 3.6 Examples - Hibernation and wake scenarios
- 3.7 Troubleshooting - Hibernation issues

---

## 3.1 What is agent hibernation

Agent hibernation is the suspension of an agent's execution while preserving its complete state. Unlike termination, hibernation allows the agent to resume exactly where it left off. Hibernation:

1. Preserves complete agent state
2. Releases runtime resources
3. Allows quick resumption
4. Reduces system load during idle periods

---

## 3.2 When to hibernate agents

### 3.2.1 Idle timeout

Hibernate when:
- Agent has no active tasks
- Idle duration exceeds threshold (default: 30 minutes)
- No pending work expected soon

### 3.2.2 Resource pressure

Hibernate when:
- System memory is constrained
- Too many active agents
- Need to free context window slots

### 3.2.3 Scheduled pause

Hibernate when:
- Work is paused for external dependency
- User requests temporary suspension
- End of work session

---

## 3.3 Hibernation procedure

### 3.3.1 Idle confirmation

**Purpose:** Verify agent is not actively working.

**Checks:**
1. No in-progress tasks
2. No pending file writes
3. No waiting on user input
4. Last activity beyond threshold

**Idle Check Command:**
Use the `agent-messaging` skill to check the agent's activity status. Expect a response showing `status: "IDLE"` and `last_activity` timestamp.

### 3.3.2 State capture

**Purpose:** Serialize complete agent state for storage.

**State Components:**
- Current context (task, project, position)
- Progress tracking (tasks done, pending)
- Learned patterns (session knowledge)
- Active file references
- Environment variables
- Tool states

### 3.3.3 State persistence

**Purpose:** Write state to durable storage.

**Storage Location:**
```
design/memory/agents/
└── code-impl-01/
    └── hibernate/
        ├── state.json       # Serialized state
        ├── context.md       # Context snapshot
        └── progress.md      # Task progress
```

**State File Format:**
```json
{
  "agent_id": "code-impl-01",
  "hibernated_at": "2025-02-01T10:30:00Z",
  "state_version": "1.0",
  "context": {
    "current_task": "Implement login validation",
    "current_file": "src/auth/login.py",
    "current_line": 145,
    "project": "/Users/dev/myproject"
  },
  "progress": {
    "tasks_completed": 3,
    "tasks_pending": 2,
    "task_list": [...]
  },
  "patterns": [...],
  "environment": {...}
}
```

### 3.3.4 Resource release

**Purpose:** Free runtime resources.

**Resources to Release:**
- Context window (tokens)
- API connections
- File handles
- Memory allocations

### 3.3.5 Registry update

**Purpose:** Mark agent as hibernated in registry.

**Registry Entry:**
```json
{
  "agent_id": "code-impl-01",
  "status": "HIBERNATED",
  "hibernated_at": "2025-02-01T10:30:00Z",
  "state_location": "design/memory/agents/code-impl-01/hibernate/",
  "wake_triggers": ["message_received", "task_assigned", "manual"]
}
```

---

## 3.4 State snapshot format

**Complete Snapshot Structure:**

```yaml
# Metadata
agent_id: "code-impl-01"
agent_type: "code-implementer"
hibernated_at: "2025-02-01T10:30:00Z"
state_version: "1.0"

# Context
context:
  current_task: "Implement login validation"
  task_description: "Add validation for login form inputs"
  current_file: "src/auth/login.py"
  current_line: 145
  project: "/Users/dev/myproject"
  working_directory: "/Users/dev/myproject/src/auth"

# Progress
progress:
  phase: "implementation"
  tasks_completed:
    - id: "T1"
      description: "Setup auth module structure"
      completed_at: "2025-02-01T09:00:00Z"
    - id: "T2"
      description: "Implement password hashing"
      completed_at: "2025-02-01T09:30:00Z"
  tasks_pending:
    - id: "T4"
      description: "Implement login validation"
      status: "in-progress"
    - id: "T5"
      description: "Add error handling"
      status: "not_started"

# Patterns learned
patterns:
  - type: "code_pattern"
    description: "Project uses bcrypt for password hashing"
  - type: "convention"
    description: "All validators return (bool, error_message) tuple"

# Environment
environment:
  PYTHON_PATH: "/Users/dev/myproject/src"
  DEBUG: "true"

# Wake instructions
wake_instructions:
  resume_task: "T4"
  resume_file: "src/auth/login.py"
  resume_line: 145
  context_to_load: ["context.md", "progress.md"]
```

---

## 3.5 Wake procedure

### 3.5.1 State retrieval

**Purpose:** Load state from storage.

**Steps:**
1. Locate state files in hibernate directory
2. Read state.json
3. Validate state integrity
4. Check state version compatibility

### 3.5.2 State restoration

**Purpose:** Deserialize state into running agent.

**Steps:**
1. Parse state JSON/YAML
2. Restore context variables
3. Load progress tracking
4. Restore learned patterns
5. Set environment variables

### 3.5.3 Resource reacquisition

**Purpose:** Reconnect to required services.

**Steps:**
1. Acquire context window slot
2. Reconnect to project directory
3. Open required file handles
4. Verify tool availability

### 3.5.4 Registry update

**Purpose:** Mark agent as running.

**Registry Update:**
```json
{
  "agent_id": "code-impl-01",
  "status": "RUNNING",
  "woken_at": "2025-02-01T14:00:00Z",
  "hibernation_duration": "3h 30m",
  "resumed_task": "T4"
}
```

### 3.5.5 Work resumption

**Purpose:** Continue from where agent left off.

**Steps:**
1. Navigate to resume file and line
2. Read wake instructions
3. Resume pending task
4. Report wake status to Chief of Staff

---

## 3.6 Examples

### Example 1: Hibernating an Idle Agent

```python
agent_id = "code-impl-01"

# Step 1: Confirm idle
status = get_agent_status(agent_id)
if status["status"] != "IDLE":
    raise Exception("Cannot hibernate active agent")

# Step 2: Request hibernation
send_message(
    to=agent_id,
    subject="Hibernation Request",
    content={
        "type": "hibernate-request",
        "message": "Please save state and hibernate",
        "reason": "Idle timeout exceeded"
    }
)

# Step 3: Wait for state save confirmation
response = await_response(agent_id, timeout=60)
assert response["state_saved"] == True

# Step 4: Update registry
update_registry(agent_id, status="HIBERNATED")
```

### Example 2: Waking a Hibernated Agent

```python
agent_id = "code-impl-01"

# Step 1: Verify agent is hibernated
status = get_registry_status(agent_id)
assert status == "HIBERNATED"

# Step 2: Load state
state = load_hibernation_state(agent_id)

# Step 3: Spawn agent with state
spawn_agent_with_state(agent_id, state)

# Step 4: Wait for ready signal
await_agent_ready(agent_id, timeout=60)

# Step 5: Update registry
update_registry(agent_id, status="RUNNING")

# Step 6: Agent resumes automatically from wake_instructions
```

---

## 3.7 Troubleshooting

### Issue: State file corrupted

**Symptoms:** Cannot deserialize state, parse errors.

**Resolution:**
1. Check for partial writes (system crash during hibernate)
2. Look for backup state files
3. Attempt partial state recovery
4. If unrecoverable, terminate and respawn fresh

### Issue: Agent fails to wake

**Symptoms:** Wake command sent but agent not responding.

**Resolution:**
1. Verify state file exists and is valid
2. Check for resource availability (context slots)
3. Try spawning fresh with state restoration
4. Check for version incompatibility
5. Fall back to fresh spawn if needed

### Issue: Agent wakes but loses context

**Symptoms:** Agent running but does not remember prior work.

**Resolution:**
1. Check state restoration logs
2. Verify context.md was loaded
3. Manually point agent to resume file/line
4. Provide summary of prior work
5. Document state preservation improvements

### Issue: Resource conflict during wake

**Symptoms:** Cannot acquire resources, another agent has them.

**Resolution:**
1. Wait for resource to become available
2. Hibernate the blocking agent
3. Force resource release if safe
4. Wake with reduced resource allocation
