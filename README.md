# Emasoft Chief of Staff (ecos-)

**Version**: 1.2.0

## Overview

The Emasoft Chief of Staff (ECOS) manages **remote agents** across multiple projects. It handles staff planning, agent lifecycle, approval workflows, failure recovery, and coordinates with the Assistant Manager (EAMA) and Orchestrator (EOA).

**Key Role**: ECOS is responsible for keeping agents ready and correctly configured. It must notify the manager (EAMA) after every change, and request approval for critical operations.

## CRITICAL: Role Boundaries

**See [docs/ROLE_BOUNDARIES.md](docs/ROLE_BOUNDARIES.md) for complete role definitions.**

### ECOS Scope: PROJECT-INDEPENDENT

ECOS is **organization-wide** - there is ONE Chief of Staff managing agents across ALL projects.

### What ECOS Does:
- ✅ Creates/terminates/hibernates/wakes agents (with EAMA approval)
- ✅ Configures agents with skills and plugins for their roles
- ✅ Assigns agents to project teams
- ✅ Handles handoff protocols when agents are replaced
- ✅ Monitors agent health and availability
- ✅ Reports agent performance to EAMA

### What ECOS Does NOT Do:
- ❌ **Create projects** (EAMA only)
- ❌ **Assign tasks to agents** (EOA only)
- ❌ **Manage GitHub Project kanban** (EOA only)
- ❌ **Make architectural decisions** (EAA only)
- ❌ **Perform code review** (EIA only)
- ❌ **Communicate directly with user** (EAMA only)

### Key Distinction: ECOS vs EOA

| Aspect | ECOS (Chief of Staff) | EOA (Orchestrator) |
|--------|----------------------|-------------------|
| Scope | Organization-wide (ONE) | Project-linked (ONE per project) |
| Manages | Agent EXISTENCE | Agent WORK |
| Creates | Agents, teams | Task assignments |
| Owns | Agent registry | GitHub Project kanban |
| Question answered | "Who exists?" | "Who does what?" |

## Agent Management Integration

This plugin uses two skills for agent and messaging operations:

- **`ai-maestro-agents-management` skill** - For all agent lifecycle operations (create, terminate, hibernate, wake, install plugins, list agents, check health)
- **`agent-messaging` skill** - For all inter-agent communication (send messages, check inbox, broadcast notifications, approval requests)

### Required Claude Code Arguments

**IMPORTANT**: When spawning agents, always include the standard Claude Code flags as program arguments:

| Argument | Purpose |
|----------|---------|
| `continue` | Resume previous session context |
| `--dangerously-skip-permissions` | Skip permission dialogs for automation |
| `--chrome` | Enable Chrome DevTools integration |
| `--add-dir <TEMP>` | Add temp directory access |

**Platform-specific temp directories:**
- **macOS/Linux**: `/tmp`
- **Windows**: `%TEMP%` or `C:\Users\<user>\AppData\Local\Temp`

## Communication Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                          USER                                    │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│      EAMA (Assistant Manager)                                    │
│   - User's right hand, sole interlocutor                         │
│   - Approves/rejects ECOS requests                               │
└──────┬──────────────────────────────────────────────────────────┘
       │ requests approval, reports status
       ▼
┌─────────────────────────────────────────────────────────────────┐
│      ECOS (Chief of Staff)                                       │
│   - Manages agent lifecycle                                      │
│   - Coordinates approvals and notifications                      │
│   - Handles failure recovery                                     │
└──────┬─────────────────────┬─────────────────────┬──────────────┘
       │                     │                     │
       ▼                     ▼                     ▼
   ARCHITECT           ORCHESTRATOR           INTEGRATOR
   (EAA)                (EOA)                   (EIA)
```

## Core Responsibilities

1. **Approval Workflows**: Request manager approval before agent spawn/terminate/replace
2. **Agent Lifecycle**: Create, hibernate, wake, terminate agents via AI Maestro CLI
3. **Notification Protocols**: Notify agents before/after operations, wait for acknowledgment
4. **Failure Recovery**: Detect failures, classify severity, execute recovery strategies
5. **Team Assignment**: Assign agents to project teams (NOT task assignment - that's EOA)
6. **Skill/Plugin Configuration**: Configure agents with appropriate skills for their roles
7. **Performance Reporting**: Report agent strengths/weaknesses to manager

**Note**: ECOS does NOT manage tasks or kanban boards. When a new agent is created or an agent is replaced, ECOS notifies EOA so that EOA can handle task (re)assignment.

## Components

### Agents (10)

| Agent | Description |
|-------|-------------|
| `ecos-main` | Main Chief of Staff coordinator |
| `ecos-staff-planner` | Analyzes task requirements, determines staffing needs |
| `ecos-lifecycle-manager` | Manages agent create/terminate/hibernate/wake |
| `ecos-project-coordinator` | Tracks multi-project assignments |
| `ecos-plugin-configurator` | Configures plugins for agents |
| `ecos-skill-validator` | Validates skill configurations |
| `ecos-resource-monitor` | Monitors system resources and limits |
| `ecos-performance-reporter` | Analyzes and reports agent performance |
| `ecos-recovery-coordinator` | Detects failures and coordinates recovery |
| `ecos-approval-coordinator` | Manages approval workflows with manager |

### Commands (26)

#### Agent Lifecycle
| Command | Description |
|---------|-------------|
| `/ecos-staff-status` | List all agents |
| `/ecos-spawn-agent` | Create new agent |
| `/ecos-terminate-agent` | Delete agent |
| `/ecos-hibernate-agent` | Hibernate agent |
| `/ecos-wake-agent` | Wake hibernated agent |

#### Project Management
| Command | Description |
|---------|-------------|
| `/ecos-list-projects` | List managed projects |
| `/ecos-add-project` | Add project to management |
| `/ecos-remove-project` | Remove project from management |
| `/ecos-assign-project` | Assign agent to project |

#### Plugin/Skill Management
| Command | Description |
|---------|-------------|
| `/ecos-configure-plugins` | Configure plugins for agents |
| `/ecos-validate-skills` | Validate skill configurations |
| `/ecos-reindex-skills` | Reindex skill database |
| `/ecos-install-skill-notify` | Install skill with notification protocol |

#### Approval Workflows
| Command | Description |
|---------|-------------|
| `/ecos-request-approval` | Request approval from manager |
| `/ecos-check-approval-status` | Check pending approval status |
| `/ecos-wait-for-approval` | Wait for approval response |
| `/ecos-notify-manager` | Notify manager about issues |

#### Notification Protocols
| Command | Description |
|---------|-------------|
| `/ecos-notify-agents` | Notify agents before/after operations |
| `/ecos-wait-for-agent-ok` | Wait for agent acknowledgment |
| `/ecos-broadcast-notification` | Send notification to multiple agents |

#### Recovery & Health
| Command | Description |
|---------|-------------|
| `/ecos-health-check` | Check agent health status |
| `/ecos-replace-agent` | Replace failed agent with new one |
| `/ecos-transfer-work` | Transfer work between agents |
| `/ecos-recovery-workflow` | Execute recovery workflow |

#### Reporting
| Command | Description |
|---------|-------------|
| `/ecos-resource-report` | Show resource usage report |
| `/ecos-performance-report` | Show performance metrics |

### Skills (13)

| Skill | Description |
|-------|-------------|
| `ecos-agent-lifecycle` | Agent spawn, terminate, hibernate, wake procedures |
| `ecos-failure-recovery` | Failure detection, classification, recovery strategies |
| `ecos-multi-project` | Multi-project tracking and coordination |
| `ecos-notification-protocols` | Pre/post operation notifications, acknowledgment |
| `ecos-onboarding` | Agent onboarding checklists and procedures |
| `ecos-performance-tracking` | Performance metrics and reporting |
| `ecos-permission-management` | Approval request/response workflows |
| `ecos-plugin-management` | Plugin configuration and installation |
| `ecos-resource-monitoring` | Resource limits and monitoring |
| `ecos-session-memory-library` | Session memory persistence and management |
| `ecos-skill-management` | Skill validation and reindexing |
| `ecos-staff-planning` | Staff planning and role assignment |
| `ecos-team-coordination` | Team messaging and coordination |

### Hooks

| Hook | Event | Description |
|------|-------|-------------|
| `ecos-memory-load` | SessionStart | Load session memory at startup |
| `ecos-memory-save` | SessionEnd | Save session memory on exit |
| `ecos-heartbeat` | UserPromptSubmit | Check agent health |
| `ecos-stop-check` | Stop | Verify all work complete before exit |

## Key Protocols

### Approval Protocol

1. ECOS sends approval request to EAMA via AI Maestro
2. ECOS waits up to 2 minutes for response (reminders at 30s, 60s, 90s)
3. If approved: ECOS executes operation
4. If rejected: ECOS aborts and notifies requester
5. If timeout: ECOS may proceed but logs this and notifies EAMA

### Skill Installation Protocol

1. ECOS notifies agent about upcoming skill install (will hibernate/wake)
2. ECOS asks agent to finish current work and send "ok"
3. ECOS waits up to 2 minutes for acknowledgment
4. ECOS uses the `ai-maestro-agents-management` skill to install the plugin on the agent
5. After wake, ECOS asks agent to verify skill is active

### Agent Replacement Protocol

1. ECOS detects agent cannot be recovered
2. ECOS requests approval from EAMA
3. If approved: ECOS creates new agent on local host
4. ECOS notifies EOA to generate handoff document
5. ECOS notifies EOA to update GitHub Project kanban
6. ECOS sends handoff docs to new agent
7. New agent acknowledges and begins work

## Communication Methods

1. **AI Maestro messages** - for approval requests, notifications, status updates
2. **Handoff .md files** with UUIDs - for detailed specifications
3. **GitHub Issues** - as permanent record

## Installation (Production)

Install from the Emasoft marketplace. Use `--scope local` to install only for the current project directory, or `--scope global` for all projects.

```bash
# Add Emasoft marketplace (first time only)
claude plugin marketplace add emasoft-plugins --url https://github.com/Emasoft/emasoft-plugins

# Install plugin (--scope local = this project only, recommended)
claude plugin install emasoft-chief-of-staff@emasoft-plugins --scope local

# RESTART Claude Code after installing (required!)
```

Once installed, start a session with the main agent:

```bash
claude --agent ecos-chief-of-staff-main-agent
```

## Development Only (--plugin-dir)

`--plugin-dir` loads a plugin directly from a local directory without marketplace installation. Use only during plugin development.

```bash
claude --plugin-dir ./OUTPUT_SKILLS/emasoft-chief-of-staff
```

## Validation

```bash
cd OUTPUT_SKILLS/emasoft-chief-of-staff
uv run python scripts/validate_plugin.py . --verbose
```

## Cross-Plugin Coordination

ECOS coordinates with:
- **EAMA** (emasoft-assistant-manager-agent):
  - Requests approval for agent lifecycle operations
  - Reports agent status and performance
  - Receives autonomous operation directives
- **EOA** (emasoft-orchestrator-agent):
  - Notifies when new agent is ready for task assignment
  - Requests handoff document generation when replacing agents
  - Informs EOA to reassign kanban tasks from failed to replacement agents
  - **Note**: EOA owns task assignment and kanban management
- **EIA** (emasoft-integrator-agent): Code review and deployment coordination
- **EAA** (emasoft-architect-agent): Architecture decisions for staffing requirements
