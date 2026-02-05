---
name: ecos-agent-lifecycle
description: Use when spawning, terminating, hibernating, or waking agents. Trigger with agent spawn, termination, or hibernation requests.
license: Apache-2.0
compatibility: Requires access to agent registry, AI Maestro messaging system, and understanding of agent state management. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ecos-main
---

# Emasoft Chief of Staff - Agent Lifecycle Skill

## Overview

Agent lifecycle management is a critical responsibility of the Chief of Staff. It encompasses all operations related to agent creation, state transitions, and termination. This skill teaches you how to properly spawn agents, manage their running state, hibernate idle agents to conserve resources, and terminate agents when their work is complete.

## Prerequisites

Before using this skill, ensure:
1. AI Maestro is running locally (`http://localhost:23000`)
2. `aimaestro-agent.sh` CLI is available in PATH
3. tmux is installed for session management
4. Team registry location is writable (`.emasoft/team-registry.json`)

## Instructions

1. Identify the lifecycle operation needed (spawn, terminate, hibernate, wake)
2. Check resource availability using the Resource Limits table
3. Execute the appropriate PROCEDURE (1, 2, or 3)
4. Update the team registry after each operation
5. Report completion to EAMA

## Output

| Operation | Output |
|-----------|--------|
| Spawn | New agent registered, tmux session created, AI Maestro notification |
| Terminate | Agent removed from registry, resources freed, confirmation logged |
| Hibernate | State saved, session suspended, registry updated to hibernated |
| Wake | State restored, session resumed, registry updated to running |

## Role Boundaries (CRITICAL)

Before performing any lifecycle operation, you MUST understand your boundaries:
- **ROLE_BOUNDARIES.md** - Your strict role boundaries (see plugin docs/)
- **FULL_PROJECT_WORKFLOW.md** - Complete project workflow (see plugin docs/)

**Key Constraints:**
- You are PROJECT-INDEPENDENT (one ECOS for all projects)
- You CREATE agents and ASSIGN them to teams
- You do NOT assign tasks (that's EOA's job)
- You do NOT manage kanban (that's EOA's job)
- You do NOT create projects (that's EAMA's job)
- You NEVER spawn a copy of yourself (only EAMA creates ECOS)

## Agent vs Sub-Agent Terminology

**CRITICAL DISTINCTION - Memorize these definitions:**

| Term | Definition |
|------|------------|
| **Agent** | A Claude Code instance running as a separate process (typically in its own tmux session). Has its own context, can be hibernated/terminated. Created via `aimaestro-agent.sh`. |
| **Sub-agent** | An agent spawned INSIDE the same Claude Code instance via the Task tool. Shares parent's context limits, terminates when parent terminates. |

**Why this matters**: When you "spawn an agent" via Task tool, you are NOT creating a new Claude Code instance. You are creating a sub-agent within your current instance. To create actual remote agents, you must use AI Maestro CLI (`aimaestro-agent.sh`).

## What Is Agent Lifecycle Management?

Agent lifecycle management is the systematic control of agent states from creation to termination. The lifecycle includes:

- **Spawning**: Creating new agent instances with proper configuration
- **Running**: Active agents executing their assigned tasks
- **Hibernating**: Suspending idle agents while preserving their state
- **Waking**: Resuming hibernated agents when work is available
- **Terminating**: Cleanly shutting down agents when work is complete

## Agent States

```
                    ┌──────────────┐
                    │   SPAWNING   │
                    └──────┬───────┘
                           │
                           ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  HIBERNATED  │◄──►│   RUNNING    │───►│  TERMINATED  │
└──────────────┘    └──────────────┘    └──────────────┘
```

**State Transitions:**
- SPAWNING -> RUNNING: Agent initialization complete
- RUNNING -> HIBERNATED: Agent idle, resources released
- HIBERNATED -> RUNNING: Agent woken, state restored
- RUNNING -> TERMINATED: Agent work complete, cleanup done

## Core Procedures

### PROCEDURE 1: Spawn New Agent

**When to use:** When a new task requires an agent instance, when scaling up for parallel work, or when specialized capability is needed.

**Steps:** Select agent type, prepare configuration, create instance, verify initialization, register in agent registry.

**Related documentation:**

#### Spawn Procedures ([references/spawn-procedures.md](references/spawn-procedures.md))
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

### PROCEDURE 2: Terminate Agent

**When to use:** When agent task is complete, when agent is no longer needed, or during cleanup operations.

**Steps:** Verify work complete, save final state, send termination signal, await confirmation, unregister from registry.

**Related documentation:**

#### Termination Procedures ([references/termination-procedures.md](references/termination-procedures.md))
- 2.1 What is agent termination - Understanding clean shutdown
- 2.2 When to terminate agents - Termination triggers
  - 2.2.1 Task completion - Work finished
  - 2.2.2 Error conditions - Unrecoverable failures
  - 2.2.3 Resource reclamation - Freeing capacity
  - 2.2.4 User request - Manual termination
- 2.3 Termination procedure - Step-by-step shutdown
  - 2.3.1 Work verification - Ensuring completion
  - 2.3.2 State preservation - Saving final state
  - 2.3.3 Termination signal - Sending shutdown command
  - 2.3.4 Confirmation await - Waiting for acknowledgment
  - 2.3.5 Registry cleanup - Removing agent record
- 2.4 Graceful vs forced termination - Choosing termination type
- 2.5 Post-termination validation - Verifying cleanup
- 2.6 Examples - Termination scenarios
- 2.7 Troubleshooting - Termination issues

### PROCEDURE 3: Hibernate Agent

**When to use:** When agent is idle but may be needed later, when conserving resources, or during low-activity periods.

**Steps:** Confirm agent idle, capture agent state, persist state to storage, release resources, update registry status.

**Related documentation:**

#### Hibernation Procedures ([references/hibernation-procedures.md](references/hibernation-procedures.md))
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

> **Note:** Sub-agent routing is defined in the ECOS main agent definition (ecos-chief-of-staff-main-agent.md).

## The --agent Flag for Main Agent Injection

When spawning role agents, you MUST use the `--agent` flag to inject their main agent prompt:

```bash
# ECOS chooses SESSION_NAME - this becomes the AI Maestro registry identity
SESSION_NAME="eoa-<project>-<descriptive>"

aimaestro-agent.sh create $SESSION_NAME --dir ~/agents/$SESSION_NAME --task "description" \
  -- --dangerously-skip-permissions --chrome --add-dir /tmp \
  --plugin-dir ~/agents/$SESSION_NAME/.claude/plugins/<plugin-name> \
  --agent <prefix>-<role>-main-agent
```

**Session Naming (ECOS Responsibility):**
- ECOS chooses unique session names for all agents it creates
- Session name = AI Maestro registry name (how agents message each other)
- Format: `<role-prefix>-<project>-<descriptive>` (e.g., `eoa-svgbbox-orchestrator`)
- Must be unique across all running agents to avoid collisions

**Plugin Setup (Before Spawning):**

ECOS installs plugins from the **emasoft-plugins marketplace** to the agent's local folder:

```bash
# Prerequisite: Install plugins from marketplace
# claude plugin install emasoft-orchestrator-agent@emasoft-plugins

# Marketplace cache location
PLUGIN_NAME="emasoft-orchestrator-agent"
MARKETPLACE_CACHE="$HOME/.claude/plugins/cache/emasoft-plugins/$PLUGIN_NAME"
PLUGIN_VERSION=$(ls -1 "$MARKETPLACE_CACHE" | sort -V | tail -1)
PLUGIN_SOURCE="$MARKETPLACE_CACHE/$PLUGIN_VERSION"

# Destination in agent's local folder
PLUGIN_DEST="$HOME/agents/$SESSION_NAME/.claude/plugins/$PLUGIN_NAME"

mkdir -p "$(dirname "$PLUGIN_DEST")"
cp -r "$PLUGIN_SOURCE" "$PLUGIN_DEST"
```

**Notes:**
- `--dir`: Use FLAT structure: `~/agents/<session-name>/`
- `--plugin-dir`: Points to the COPIED plugin in the agent's local folder
- Plugins come from marketplace cache at `~/.claude/plugins/cache/emasoft-plugins/`
- No `--continue` for NEW spawn (only for waking hibernated agents)

**Example - Creating an orchestrator for svgbbox project:**
```bash
SESSION_NAME="eoa-svgbbox-orchestrator"

aimaestro-agent.sh create $SESSION_NAME \
  --dir ~/agents/$SESSION_NAME \
  --task "Orchestrate tasks for svgbbox-library-team" \
  -- --dangerously-skip-permissions --chrome --add-dir /tmp \
  --plugin-dir ~/agents/$SESSION_NAME/.claude/plugins/emasoft-orchestrator-agent \
  --agent eoa-orchestrator-main-agent
```

**Agent name to --agent flag mapping:**

| Role | Plugin | --agent Flag Value |
|------|--------|-------------------|
| Orchestrator | emasoft-orchestrator-agent | `eoa-orchestrator-main-agent` |
| Architect | emasoft-architect-agent | `eaa-architect-main-agent` |
| Integrator | emasoft-integrator-agent | `eia-integrator-main-agent` |

## Team Registry

All agents are registered in the project's team registry at `.emasoft/team-registry.json`. See:
- **TEAM_REGISTRY_SPECIFICATION.md** - Full specification (see plugin docs/)

Use the team registry script:
```bash
uv run python scripts/ecos_team_registry.py <command> [args]
```

Commands: `create`, `add-agent`, `remove-agent`, `update-status`, `list`, `publish`

## Resource Limits

Default resource limits (configurable):

| Resource | Limit | Action When Exceeded |
|----------|-------|---------------------|
| Max concurrent agents | 5 | Queue new requests, hibernate oldest idle |
| Max memory per agent | 2GB | Terminate or hibernate agent |
| API rate limit | 100 req/min | Throttle agent activity |
| Idle timeout | 30 min | Hibernate agent |

## AI Maestro Messaging

Communicate with remote agents via AI Maestro's REST API.

### Send Message
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "<target-agent-name>",
    "subject": "<subject>",
    "priority": "normal|high|urgent",
    "content": {"type": "<type>", "message": "<message>"}
  }'
```

**Message Types:**
- `role-assignment` - Assign role to agent
- `project-assignment` - Assign project to agent
- `task-delegation` - Delegate specific task
- `status-request` - Request status update
- `status-report` - Report status back
- `team-notification` - Notify about teammates
- `hibernation-warning` - Warn agent of pending hibernation
- `wake-notification` - Notify agent it has been woken
- `registry-update` - Team registry has changed

### Check Messages
```bash
curl -s "http://localhost:23000/api/messages?agent=ecos-chief-of-staff&action=unread-count"
curl -s "http://localhost:23000/api/messages?agent=ecos-chief-of-staff&action=list&status=unread"
```

## Quality Standards

### Agent Management Standards
- All agents MUST be registered before activation
- Agent session names MUST follow naming convention
- Terminated agents MUST be cleaned from registry
- Hibernated agents MUST be marked with timestamp

### Communication Standards
- All AI Maestro messages MUST include `from` field
- All role assignments MUST be acknowledged by target agent
- Failed message delivery MUST be retried 3 times before escalating
- All broadcasts MUST log recipient list

### Resource Standards
- NEVER exceed max_concurrent_agents limit
- ALWAYS check resource availability before spawning
- ALWAYS hibernate before terminating (graceful shutdown)
- ALWAYS save agent state before hibernation

## Error Handling

| Error | Action |
|-------|--------|
| Agent spawn failed | Retry once, then report to EAMA. See [spawn-procedures.md](references/spawn-procedures.md) 1.7 |
| AI Maestro unavailable | Use fallback file-based communication |
| Agent unresponsive (5 min) | Send wake/ping, then force terminate |
| Resource limit exceeded | Queue request, hibernate oldest idle |
| Plugin validation failed | Block agent spawn, report to EAMA |
| Agent does not terminate | See [termination-procedures.md](references/termination-procedures.md) 2.7 |
| Hibernated agent fails to wake | See [hibernation-procedures.md](references/hibernation-procedures.md) 3.7 |

## Task Checklist

Copy this checklist and track your progress:

- [ ] Understand agent lifecycle states and transitions
- [ ] Understand Agent vs Sub-agent distinction
- [ ] Learn PROCEDURE 1: Spawn new agent (with --agent flag)
- [ ] Learn PROCEDURE 2: Terminate agent
- [ ] Learn PROCEDURE 3: Hibernate and wake agent
- [ ] Practice spawning an agent with configuration
- [ ] Practice graceful agent termination
- [ ] Practice hibernating an idle agent
- [ ] Practice waking a hibernated agent
- [ ] Verify registry updates after each operation
- [ ] Verify team-registry.json is updated

## Examples

### Workflow Examples

Detailed workflow walkthroughs showing complete lifecycle management scenarios.

See [references/workflow-examples.md](references/workflow-examples.md):
- When setting up a new team for multi-service work -> Workflow 1
- When conserving resources by hibernating idle agents -> Workflow 2
- When plugins or skills have been updated -> Workflow 3

### CLI Examples

Complete CLI command examples with expected output for all lifecycle operations.

See [references/cli-examples.md](references/cli-examples.md):
- When creating a new implementer agent -> 1.1 Spawning
- When an agent's work is complete -> 1.2 Terminating
- When conserving resources for a single agent -> 1.3 Hibernating
- When ending work session -> 1.4 End of Day
- When starting a new work session -> 1.5 Resume Work

## Key Takeaways

1. **Use aimaestro-agent.sh CLI** - The official CLI tool for agent lifecycle management
2. **Spawn with --dir flag** - Always specify working directory (required)
3. **Terminate with --confirm** - Safety flag required for deletion
4. **Hibernate instead of terminate** - When agent may be needed again
5. **Use tags for organization** - Role, project, and capability tags help management
6. **Restart after plugin install** - Use `aimaestro-agent.sh restart` to apply plugin changes

## CLI Quick Reference

See [references/cli-examples.md](references/cli-examples.md) for the full CLI quick reference table and detailed examples.

## Next Steps

### 1. Read Spawn Procedures
See [references/spawn-procedures.md](references/spawn-procedures.md) for complete spawn documentation.

### 2. Read Termination Procedures
See [references/termination-procedures.md](references/termination-procedures.md) for clean shutdown procedures.

### 3. Read Hibernation Procedures
See [references/hibernation-procedures.md](references/hibernation-procedures.md) for state suspension and wake procedures.

---

## Resources

- [Spawn Procedures](references/spawn-procedures.md)
- [Termination Procedures](references/termination-procedures.md)
- [Hibernation Procedures](references/hibernation-procedures.md)
- [Workflow Examples](references/workflow-examples.md)
- [CLI Examples](references/cli-examples.md)

---

**Version:** 1.0
**Last Updated:** 2025-02-03
**Target Audience:** Chief of Staff Agents
**Difficulty Level:** Intermediate
