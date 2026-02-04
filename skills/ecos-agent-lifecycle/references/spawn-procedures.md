# Spawn Procedures Reference

## Table of Contents

- 1.1 What is agent spawning - Understanding agent creation
- 1.2 When to spawn agents - Triggers for new agents
  - 1.2.1 Task assignment triggers - New work arrives
  - 1.2.2 Scaling triggers - Parallel execution needed
  - 1.2.3 Specialization triggers - Specific capability required
- 1.3 Spawn procedure - Step-by-step agent creation
  - 1.3.1 Agent type selection - Choosing the right agent
  - 1.3.2 Configuration preparation - Setting parameters
  - 1.3.3 Instance creation - Executing spawn command
  - 1.3.4 Initialization verification - Confirming agent ready
  - 1.3.5 Registry registration - Recording agent existence
- 1.4 Spawn configuration format - Standard configuration structure
- 1.5 AI Maestro integration - Messaging new agents
- 1.6 Examples - Spawn scenarios
- 1.7 Troubleshooting - Spawn failures and recovery

---

## 1.1 What is agent spawning

Agent spawning is the process of creating a new agent instance to perform work. Spawning involves:

1. Selecting the appropriate agent type
2. Preparing configuration parameters
3. Creating the agent instance
4. Verifying successful initialization
5. Registering the agent in the registry

Spawned agents run as subagents of the Chief of Staff and communicate via AI Maestro.

---

## 1.2 When to spawn agents

### 1.2.1 Task assignment triggers

Spawn a new agent when:
- A new task arrives that requires agent work
- No existing agent is available for the task
- Task requires fresh context (no prior state)

### 1.2.2 Scaling triggers

Spawn additional agents when:
- Multiple tasks can run in parallel
- Single agent is overloaded
- Task queue is growing faster than completion

### 1.2.3 Specialization triggers

Spawn specialized agent when:
- Task requires specific capability not in current agents
- Domain expertise needed (security, DevOps, etc.)
- Different language or framework required

---

## 1.3 Spawn procedure

### 1.3.1 Agent type selection

**Purpose:** Choose the correct agent type for the task.

**Agent Type Reference:**

| Agent Type | Primary Use Case |
|------------|-----------------|
| code-implementer | Writing and modifying code |
| test-engineer | Creating and running tests |
| doc-writer | Documentation and README |
| architect-agent | System design and planning |
| code-reviewer | Code quality review |
| security-reviewer | Security audit |
| devops-expert | CI/CD and deployment |
| debug-specialist | Debugging and troubleshooting |

**Selection Criteria:**
1. Match task requirements to agent capabilities
2. Prefer specialists over generalists for specific tasks
3. Consider agent availability and current load
4. Check for required tools and permissions

### 1.3.2 Configuration preparation

**Purpose:** Prepare spawn configuration with all required parameters.

**Required Parameters:**
```yaml
agent_type: "code-implementer"    # Type of agent to spawn
task: "Implement user login"      # Initial task description
project: "/path/to/project"       # Project directory
```

**Optional Parameters:**
```yaml
timeout: 3600                     # Max runtime in seconds
context_limit: 80000              # Max context tokens
priority: "high"                  # Task priority
dependencies: ["task-123"]        # Tasks to wait for
environment:                      # Environment variables
  DEBUG: "true"
```

### 1.3.3 Instance creation

**Purpose:** Execute the spawn command to create the agent.

**Using Task Tool:**
```python
# Spawn via Claude Code Task tool
result = Task(
    description="Implement user login feature",
    prompt="""
    You are a code-implementer agent.
    Project: /path/to/project
    Task: Implement user login with JWT authentication

    Report progress via AI Maestro to chief-of-staff.
    """,
    subagent_type="code-implementer"
)
```

**Using AI Maestro:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "agent-spawner",
    "subject": "Spawn Request",
    "priority": "high",
    "content": {
      "type": "spawn-request",
      "message": "Spawn code-implementer",
      "config": {
        "agent_type": "code-implementer",
        "task": "Implement user login",
        "project": "/path/to/project"
      }
    }
  }'
```

### 1.3.4 Initialization verification

**Purpose:** Confirm the agent started successfully.

**Verification Steps:**
1. Check spawn command return status
2. Wait for agent initialization message
3. Verify agent appears in registry
4. Confirm agent is responding to messages

**Verification Timeout:** 30 seconds (configurable)

### 1.3.5 Registry registration

**Purpose:** Record the new agent in the agent registry.

**Registry Entry:**
```json
{
  "agent_id": "code-impl-login-01",
  "agent_type": "code-implementer",
  "status": "RUNNING",
  "spawned_at": "2025-02-01T10:00:00Z",
  "spawned_by": "chief-of-staff",
  "task": "Implement user login",
  "project": "/path/to/project"
}
```

---

## 1.4 Spawn configuration format

**Complete Configuration Schema:**

```yaml
# Required fields
agent_type: string              # Agent type identifier
task: string                    # Task description
project: string                 # Project path

# Optional fields
agent_id: string                # Custom agent ID (auto-generated if not provided)
timeout: integer                # Max runtime in seconds (default: 3600)
context_limit: integer          # Max context tokens (default: 100000)
priority: string                # "critical", "high", "normal", "low"
dependencies: list[string]      # Task IDs to wait for
environment: map[string,string] # Environment variables
skills: list[string]            # Skills to activate
tools: list[string]             # Tools to enable
reporting:
  frequency: string             # "on_complete", "periodic", "on_error"
  interval: integer             # Reporting interval in seconds
  destination: string           # Where to send reports
```

---

## 1.5 AI Maestro integration

**Sending spawn request:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "agent-spawner",
    "subject": "Spawn Request",
    "content": {
      "type": "spawn-request",
      "message": "Spawn agent for task",
      "config": {...}
    }
  }'
```

**Receiving spawn confirmation:**
```json
{
  "from": "agent-spawner",
  "subject": "Spawn Confirmation",
  "content": {
    "type": "spawn-response",
    "message": "Agent spawned successfully",
    "agent_id": "code-impl-01",
    "status": "RUNNING"
  }
}
```

**Messaging spawned agent:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "code-impl-01",
    "subject": "Task Update",
    "content": {
      "type": "instruction",
      "message": "Priority changed to critical"
    }
  }'
```

---

## 1.6 Examples

### Example 1: Spawn for Feature Implementation

```python
# Spawn code-implementer for auth feature
spawn_config = {
    "agent_type": "code-implementer",
    "task": "Implement JWT authentication",
    "project": "/Users/dev/myproject",
    "timeout": 7200,  # 2 hours
    "priority": "high",
    "skills": ["python-development", "security-basics"]
}

result = spawn_agent(spawn_config)
# Returns: {"agent_id": "code-impl-auth-01", "status": "RUNNING"}
```

### Example 2: Spawn Multiple Parallel Agents

```python
# Spawn 3 test engineers for parallel test writing
for i in range(3):
    spawn_config = {
        "agent_type": "test-engineer",
        "task": f"Write tests for module {i+1}",
        "project": "/Users/dev/myproject",
        "dependencies": ["code-impl-auth-01"]  # Wait for auth complete
    }
    spawn_agent(spawn_config)

# Result: 3 test-engineer agents spawned, all waiting for auth
```

---

## 1.7 Troubleshooting

### Issue: Spawn command times out

**Symptoms:** No agent created, timeout error returned.

**Resolution:**
1. Check system resources (memory, CPU)
2. Verify Claude Code is running
3. Check for conflicting agents
4. Increase timeout and retry
5. Check logs for spawn errors

### Issue: Agent spawns but does not respond

**Symptoms:** Agent in registry but no messages received.

**Resolution:**
1. Verify AI Maestro is running
2. Check agent ID matches in messages
3. Look for agent error logs
4. Try sending a ping message
5. Terminate and respawn if unresponsive

### Issue: Agent spawns with wrong configuration

**Symptoms:** Agent working on wrong task or project.

**Resolution:**
1. Terminate the incorrectly configured agent
2. Review spawn configuration
3. Verify all required fields present
4. Respawn with corrected configuration
5. Confirm via initialization message

### Issue: Too many agents spawned

**Symptoms:** System slow, agents competing for resources.

**Resolution:**
1. Check spawn throttling settings
2. Review scaling triggers
3. Hibernate or terminate excess agents
4. Implement spawn limits
5. Add spawn approval workflow
