# Approval Types - Detailed Reference

## Table of Contents (Use-Case Oriented)

- 1. Agent Spawn Approval - When creating a new agent instance
  - 1.1 When to request spawn approval
  - 1.2 Justification requirements for spawn
  - 1.3 EAMA decision options for spawn
- 2. Agent Terminate Approval - When permanently stopping an agent
  - 2.1 When to request terminate approval
  - 2.2 Justification requirements for terminate
  - 2.3 EAMA decision options for terminate
- 3. Agent Hibernate Approval - When suspending an idle agent
  - 3.1 When to request hibernate approval
  - 3.2 Justification requirements for hibernate
  - 3.3 EAMA decision options for hibernate
- 4. Agent Wake Approval - When resuming a hibernated agent
  - 4.1 When to request wake approval
  - 4.2 Justification requirements for wake
  - 4.3 EAMA decision options for wake
- 5. Plugin Install Approval - When installing a new plugin
  - 5.1 When to request plugin install approval
  - 5.2 Justification requirements for plugin install
  - 5.3 EAMA decision options for plugin install

---

## 1. Agent Spawn Approval

**Request when:** Creating a new agent instance to perform work.

### 1.1 When to Request Spawn Approval

Request spawn approval when:
- A task requires a new agent to be created
- The task cannot be handled by existing agents
- A specialized agent role is needed
- Load balancing requires additional capacity

### 1.2 Justification Requirements for Spawn

Your approval request MUST include:

| Field | Description | Example |
|-------|-------------|---------|
| `agent_role` | The type/role of agent | `code-implementer`, `test-engineer` |
| `task` | What the agent will do | `Implement user authentication module` |
| `working_directory` | Where the agent operates | `{baseDir}/auth` |
| `expected_duration` | How long the agent will run | `2 hours`, `30 minutes` |
| `resource_requirements` | Resource level needed | `standard`, `high-memory` |

### 1.3 EAMA Decision Options for Spawn

EAMA can respond with:

| Decision | Meaning | ECOS Action |
|----------|---------|-------------|
| **Approve** | Proceed with spawn | Execute spawn with specified parameters |
| **Reject** | Do not spawn | Cancel spawn, log rejection |
| **Modify** | Change parameters | Spawn with modified parameters |

**Modify examples:**
- Change `working_directory` to a different path
- Reduce `expected_duration` to limit runtime
- Change `agent_role` to a different type

---

## 2. Agent Terminate Approval

**Request when:** Permanently stopping an agent that has completed or failed.

### 2.1 When to Request Terminate Approval

Request terminate approval when:
- Agent has completed all assigned tasks
- Agent has failed and cannot recover
- Agent is redundant (duplicate functionality)
- Agent resources need to be reclaimed

### 2.2 Justification Requirements for Terminate

Your approval request MUST include:

| Field | Description | Example |
|-------|-------------|---------|
| `agent_name` | Name of agent to terminate | `data-processor-03` |
| `reason` | Why termination is requested | `task_complete`, `failed`, `redundant` |
| `final_report` | Summary of agent work | `Processed 1500 records successfully` |
| `pending_work` | Any incomplete work | `none` or description |

### 2.3 EAMA Decision Options for Terminate

EAMA can respond with:

| Decision | Meaning | ECOS Action |
|----------|---------|-------------|
| **Approve** | Proceed with termination | Terminate agent, clean up resources |
| **Reject** | Do not terminate | Keep agent running |
| **Delay** | Wait for conditions | Hold termination until specified condition |

**Delay examples:**
- Wait for batch 2 processing
- Wait for user review of output
- Wait until end of business day

---

## 3. Agent Hibernate Approval

**Request when:** Suspending an idle agent to conserve resources.

### 3.1 When to Request Hibernate Approval

Request hibernate approval when:
- Agent has been idle for extended period
- Resources need to be conserved
- Agent may be needed again later
- Task is paused but not complete

### 3.2 Justification Requirements for Hibernate

Your approval request MUST include:

| Field | Description | Example |
|-------|-------------|---------|
| `agent_name` | Name of agent to hibernate | `code-reviewer-02` |
| `idle_duration` | How long agent has been idle | `15 minutes`, `1 hour` |
| `last_activity` | When agent last did work | `2025-02-02T09:45:00Z` |
| `expected_wake_trigger` | What will wake the agent | `PR submitted`, `user request` |

### 3.3 EAMA Decision Options for Hibernate

EAMA can respond with:

| Decision | Meaning | ECOS Action |
|----------|---------|-------------|
| **Approve** | Proceed with hibernation | Hibernate agent, preserve state |
| **Reject** | Do not hibernate | Keep agent active |
| **Terminate Instead** | Terminate rather than hibernate | Terminate agent instead |

**Terminate Instead reasoning:**
- Agent unlikely to be needed again
- State not worth preserving
- Resources more valuable than quick resume

---

## 4. Agent Wake Approval

**Request when:** Resuming a hibernated agent to continue work.

### 4.1 When to Request Wake Approval

Request wake approval when:
- Trigger condition for hibernated agent met
- Task needs to resume
- User requests agent activation
- Scheduled wake time reached

### 4.2 Justification Requirements for Wake

Your approval request MUST include:

| Field | Description | Example |
|-------|-------------|---------|
| `agent_name` | Name of agent to wake | `code-reviewer-02` |
| `reason` | Why wake is needed | `PR submitted for review` |
| `task_to_resume` | What agent will do | `Review PR #123` |
| `priority` | Urgency level | `high`, `normal`, `low` |

### 4.3 EAMA Decision Options for Wake

EAMA can respond with:

| Decision | Meaning | ECOS Action |
|----------|---------|-------------|
| **Approve** | Proceed with wake | Resume agent from hibernation |
| **Reject** | Do not wake | Keep agent hibernated |
| **Spawn Fresh Instead** | Create new agent | Terminate hibernated, spawn new |

**Spawn Fresh Instead reasoning:**
- Hibernated state may be stale
- Task requirements have changed
- Clean slate preferred

---

## 5. Plugin Install Approval

**Request when:** Installing a new Claude Code plugin for additional capabilities.

### 5.1 When to Request Plugin Install Approval

Request plugin install approval when:
- New capability required by current task
- User has requested plugin functionality
- Workflow optimization needs new tool
- Dependency for other operation

### 5.2 Justification Requirements for Plugin Install

Your approval request MUST include:

| Field | Description | Example |
|-------|-------------|---------|
| `plugin_name` | Name of plugin | `code-analyzer-pro` |
| `plugin_version` | Version to install | `1.2.3` |
| `source` | Where plugin comes from | `marketplace`, `local` |
| `capability` | What plugin adds | `Static code analysis` |
| `security_implications` | Security considerations | `Reads source files only` |

### 5.3 EAMA Decision Options for Plugin Install

EAMA can respond with:

| Decision | Meaning | ECOS Action |
|----------|---------|-------------|
| **Approve** | Proceed with installation | Install plugin |
| **Reject** | Do not install | Cancel installation |
| **Request Security Review** | Need more info | Provide detailed security analysis |

**Security Review includes:**
- Plugin permissions required
- Data access patterns
- Network access requirements
- Known vulnerabilities

---

**Version:** 1.0
**Last Updated:** 2025-02-03
