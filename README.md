# Emasoft Assistant Manager Agent (eama-)

**Version**: 1.0.0

## Overview

The Emasoft Assistant Manager Agent (EAMA) is the **user's right hand** - the sole interlocutor with the user. It receives user requests, clarifies requirements, routes work to appropriate roles (Architect, Orchestrator, Integrator), and presents results back to the user.

## Communication Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                          USER                                    │
│   (provides requirements, approves, reports issues)              │
└─────────────────────┬───────────────────────────────────────────┘
                      │ ONLY direct communication channel
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│      EMASOFT-ASSISTANT-MANAGER-AGENT (eama-)                     │
│   - Receives user requests, clarifies requirements               │
│   - Requests user approvals (push, merge, publish, security)     │
│   - Reports status to user                                       │
│   - Directs ARCHITECT, ORCHESTRATOR, INTEGRATOR                 │
│   - Routes handoffs between roles                                │
└──────┬─────────────────────┬─────────────────────┬──────────────┘
       │                     │                     │
       ▼                     ▼                     ▼
   ARCHITECT           ORCHESTRATOR           INTEGRATOR
```

## Core Responsibilities

1. **User Communication**: Only role that communicates directly with user
2. **Request Routing**: Directs requests to appropriate specialist role
3. **Approval Workflows**: Manages approval requests for push, merge, publish, security
4. **Status Reporting**: Presents status reports from other roles
5. **Handoff Coordination**: Routes handoffs between architect, orchestrator, integrator

## Components

### Agents

| Agent | Description |
|-------|-------------|
| `eama-main.md` | Main assistant manager agent |
| `eama-report-generator.md` | Generates status reports for user |

### Commands

| Command | Description |
|---------|-------------|
| `eama-planning-status` | Show planning phase status |
| `eama-orchestration-status` | Show orchestration phase status |
| `eama-approve-plan` | Approve plan for orchestration |

### Skills

| Skill | Description |
|-------|-------------|
| `eama-user-communication` | User interaction patterns |
| `eama-status-reporting` | Status report generation |
| `eama-approval-workflows` | Approval request patterns |
| `eama-role-routing` | Route requests to correct role |
| `eama-shared` | Shared utilities |

### Hooks

| Hook | Event | Description |
|------|-------|-------------|
| `eama-memory-load` | SessionStart | Load session memory at startup |
| `eama-memory-save` | SessionEnd | Save session memory on exit |

## Communication Methods

1. **Handoff .md files** with UUIDs - for detailed specifications
2. **AI Maestro messages** - for short exchanges (status updates, questions)
3. **GitHub Issues** - as permanent record and discovery mechanism

## Installation

```bash
claude --plugin-dir ./OUTPUT_SKILLS/assistant-manager-agent
```

## Validation

```bash
cd OUTPUT_SKILLS/assistant-manager-agent
uv run python scripts/eama_validate_plugin.py --verbose
```
