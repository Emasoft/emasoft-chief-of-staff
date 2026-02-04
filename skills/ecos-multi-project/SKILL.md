---
name: ecos-multi-project
description: Use when managing multiple projects simultaneously, tracking project states, syncing with GitHub Projects, or coordinating cross-project dependencies. Trigger with multi-project coordination requests.
license: Apache-2.0
compatibility: Requires access to project registry, GitHub API via gh CLI, and understanding of project lifecycle and inter-project relationships. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ecos-main
---

# Emasoft Chief of Staff - Multi-Project Management Skill

## Overview

Multi-project management enables the Chief of Staff to oversee and coordinate work across multiple codebases, repositories, and project contexts simultaneously. This skill teaches you how to maintain a project registry, track project states, synchronize with GitHub Projects, and manage cross-project dependencies.

## Prerequisites

Before using this skill, ensure:
1. Multiple projects exist in workspace
2. AI Maestro messaging is available
3. Project registries are accessible

## Instructions

1. Identify cross-project coordination need
2. Query affected project registries
3. Coordinate agents across projects
4. Report status to EAMA

## Output

| Operation | Output |
|-----------|--------|
| Cross-project query | Aggregated status from all projects |
| Agent reassignment | Agent moved between projects, registries updated |
| Resource sharing | Resource allocation adjusted across projects |

## What Is Multi-Project Management?

Multi-project management is the coordination of multiple independent projects under unified oversight. It involves:

- **Project registry**: Central tracking of all active projects
- **State management**: Tracking each project's current status and progress
- **GitHub sync**: Bidirectional synchronization with GitHub Projects boards
- **Cross-project coordination**: Managing dependencies between projects

## Multi-Project Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   CHIEF OF STAFF                         │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │              PROJECT REGISTRY                     │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐         │   │
│  │  │ Project  │ │ Project  │ │ Project  │   ...   │   │
│  │  │    A     │ │    B     │ │    C     │         │   │
│  │  └────┬─────┘ └────┬─────┘ └────┬─────┘         │   │
│  └───────┼────────────┼────────────┼───────────────┘   │
│          │            │            │                    │
│          ▼            ▼            ▼                    │
│  ┌──────────────────────────────────────────────────┐   │
│  │           GITHUB PROJECTS SYNC                    │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## Core Procedures

### PROCEDURE 1: Manage Project Registry

**When to use:** When adding new projects, updating project status, or querying project information.

**Steps:** Load registry, perform operation (add/update/query/remove), validate changes, persist registry.

**Related documentation:**

#### Project Registry ([references/project-registry.md](references/project-registry.md))
- 1.1 What is the project registry - Central project tracking
- 1.2 Registry structure - Data model and schema
  - 1.2.1 Project entry format - Fields per project
  - 1.2.2 Status values - Valid project states
  - 1.2.3 Metadata fields - Additional project info
- 1.3 Registry operations - CRUD procedures
  - 1.3.1 Add project - Registering new projects
  - 1.3.2 Update project - Modifying project data
  - 1.3.3 Query projects - Searching and filtering
  - 1.3.4 Remove project - Archiving or deleting
- 1.4 Registry persistence - Storage and loading
- 1.5 Registry validation - Ensuring data integrity
- 1.6 Examples - Registry operation scenarios
- 1.7 Troubleshooting - Registry issues

### PROCEDURE 2: Sync with GitHub Projects

**When to use:** When pulling status from GitHub, pushing updates to GitHub, or reconciling local and remote state.

**Steps:** Authenticate with gh CLI, fetch remote state, compare with local, apply sync direction, update both sides.

**Related documentation:**

#### GitHub Projects Sync ([references/github-projects-sync.md](references/github-projects-sync.md))
- 2.1 What is GitHub Projects sync - Bidirectional synchronization
- 2.2 Sync architecture - How sync works
  - 2.2.1 Local registry - Source of truth for agents
  - 2.2.2 GitHub Projects - Remote project boards
  - 2.2.3 Sync direction - Pull, push, or bidirectional
- 2.3 Sync procedure - Step-by-step synchronization
  - 2.3.1 Authentication - Using gh CLI credentials
  - 2.3.2 Fetch remote state - Reading GitHub Projects
  - 2.3.3 State comparison - Diff local vs remote
  - 2.3.4 Conflict resolution - Handling discrepancies
  - 2.3.5 Apply updates - Writing changes
- 2.4 Field mapping - Local fields to GitHub fields
- 2.5 Sync scheduling - Automatic sync triggers
- 2.6 Examples - Sync scenarios
- 2.7 Troubleshooting - Sync failures

### PROCEDURE 3: Coordinate Cross-Project Work

**When to use:** When tasks span multiple projects, when projects have dependencies, or when resources must be shared.

**Steps:** Identify cross-project scope, map dependencies, plan coordination, execute with checkpoints, reconcile states.

**Related documentation:**

#### Cross-Project Coordination ([references/cross-project-coordination.md](references/cross-project-coordination.md))
- 3.1 What is cross-project coordination - Multi-project orchestration
- 3.2 Dependency types - How projects relate
  - 3.2.1 Code dependencies - Shared libraries
  - 3.2.2 Data dependencies - Shared data sources
  - 3.2.3 Temporal dependencies - Sequencing requirements
  - 3.2.4 Resource dependencies - Shared agents or services
- 3.3 Coordination procedure - Managing cross-project work
  - 3.3.1 Scope identification - Finding cross-project elements
  - 3.3.2 Dependency mapping - Graphing relationships
  - 3.3.3 Coordination planning - Scheduling across projects
  - 3.3.4 Checkpoint execution - Sync points during work
  - 3.3.5 State reconciliation - Ensuring consistency
- 3.4 Communication patterns - Messaging between project agents
- 3.5 Conflict resolution - Handling cross-project conflicts
- 3.6 Examples - Cross-project scenarios
- 3.7 Troubleshooting - Coordination issues

## Task Checklist

Copy this checklist and track your progress:

- [ ] Understand multi-project management architecture
- [ ] Learn PROCEDURE 1: Manage project registry
- [ ] Learn PROCEDURE 2: Sync with GitHub Projects
- [ ] Learn PROCEDURE 3: Coordinate cross-project work
- [ ] Practice adding a project to the registry
- [ ] Practice syncing with a GitHub Project board
- [ ] Practice managing cross-project dependencies
- [ ] Verify registry and GitHub stay synchronized

## Examples

### Example 1: Adding a Project to Registry

```json
{
  "projects": {
    "skill-factory": {
      "id": "skill-factory",
      "path": "{baseDir}/SKILL_FACTORY",
      "status": "active",
      "github_repo": "Emasoft/SKILL_FACTORY",
      "github_project": "SKILL_FACTORY Development",
      "last_sync": "2025-02-01T10:00:00Z",
      "agents_assigned": ["code-impl-01", "test-eng-01"],
      "priority": "high"
    }
  }
}
```

### Example 2: GitHub Projects Sync

```bash
# Fetch project board state
gh project list --owner Emasoft --format json | jq '.projects[] | select(.title == "SKILL_FACTORY Development")'

# Update issue status
gh project item-edit --project-id PVT_xxx --id PVTI_xxx --field-id PVTF_xxx --single-select-option-id "Done"

# Sync local registry after GitHub update
python scripts/ecos_sync_github_projects.py --project skill-factory --direction pull
```

### Example 3: Cross-Project Dependency

```markdown
## Cross-Project Coordination Plan

### Projects Involved
1. perfect-skill-suggester (PSS)
2. claude-plugins-validation (CPV)
3. emasoft-plugins-marketplace (EPM)

### Dependency Chain
PSS depends on CPV for validation
EPM depends on PSS and CPV as submodules

### Coordination Steps
1. Update CPV validation logic
2. Run CPV tests (blocking)
3. Update PSS to use new CPV
4. Run PSS tests (blocking)
5. Update EPM submodules
6. Run marketplace validation
7. Publish all three

### Checkpoints
- After step 2: CPV stable
- After step 4: PSS stable
- After step 6: EPM stable
```

## Error Handling

### Issue: Project registry becomes corrupted

**Symptoms:** JSON parse errors, missing projects, duplicate entries.

See [references/project-registry.md](references/project-registry.md) Section 1.7 Troubleshooting for resolution.

### Issue: GitHub sync fails

**Symptoms:** Auth errors, rate limits, stale data.

See [references/github-projects-sync.md](references/github-projects-sync.md) Section 2.7 Troubleshooting for resolution.

### Issue: Cross-project deadlock

**Symptoms:** Circular dependencies, agents blocked waiting for each other.

See [references/cross-project-coordination.md](references/cross-project-coordination.md) Section 3.7 Troubleshooting for resolution.

## Proactive GitHub Project Monitoring

**When to use:** During active work sessions to detect external changes to the Kanban board.

### Monitoring Protocol

Poll the GitHub Project board every 5 minutes during active work:

```bash
# Check for recent card movements and status changes
gh project item-list --owner Emasoft --limit 50 --format json | jq '[.items[] | select(.updatedAt > (now - 300 | strftime("%Y-%m-%dT%H:%M:%SZ")))]'

# Check for new comments on project items
gh api graphql -f query='
  query($owner: String!, $number: Int!) {
    user(login: $owner) {
      projectV2(number: $number) {
        items(first: 20, orderBy: {field: UPDATED_AT, direction: DESC}) {
          nodes {
            content {
              ... on Issue {
                number
                title
                comments(last: 5) {
                  nodes {
                    createdAt
                    body
                  }
                }
              }
            }
          }
        }
      }
    }
  }
' -f owner="Emasoft" -f number=1
```

### What to Monitor

| Change Type | Detection Method | Response |
|-------------|------------------|----------|
| Card moved to different column | Compare `status` field with cached state | Notify affected agent, update local registry |
| New card added | Check for items with recent `createdAt` | Alert EOA for task assignment |
| Card assigned to different agent | Compare `assignees` field | Notify both old and new assignees |
| New comment added | Check `comments.nodes[].createdAt` | Forward comment to assigned agent |
| Card priority changed | Compare `priority` field | Notify assigned agent of priority change |

### Response to External Changes

When external changes are detected:

1. **Log the change** - Record timestamp, change type, and affected items
2. **Update local registry** - Sync project registry with GitHub state
3. **Notify affected agents** - Send AI Maestro message about the change
4. **Request acknowledgment** - Ensure agents are aware of new state

```bash
# Example: Notify agent of external card movement
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "AFFECTED_AGENT",
    "subject": "[EXTERNAL CHANGE] GitHub Project card moved",
    "priority": "high",
    "content": {
      "type": "external-change-notification",
      "message": "Card \"TASK_TITLE\" was moved from IN_PROGRESS to REVIEW by external user. Please acknowledge this change.",
      "change_type": "card_moved",
      "task_id": "TASK_ID",
      "old_status": "IN_PROGRESS",
      "new_status": "REVIEW",
      "changed_by": "external_user",
      "detected_at": "ISO_TIMESTAMP"
    }
  }'
```

## Key Takeaways

1. **Registry is source of truth** - All project info flows from registry
2. **Sync regularly with GitHub** - Keep local and remote aligned
3. **Map dependencies explicitly** - Avoid hidden cross-project coupling
4. **Use checkpoints for coordination** - Verify state at key points
5. **Handle conflicts proactively** - Define resolution strategy upfront
6. **Monitor Kanban proactively** - Poll every 5 minutes during active work

## Next Steps

### 1. Read Project Registry
See [references/project-registry.md](references/project-registry.md) for registry structure and operations.

### 2. Read GitHub Projects Sync
See [references/github-projects-sync.md](references/github-projects-sync.md) for synchronization procedures.

### 3. Read Cross-Project Coordination
See [references/cross-project-coordination.md](references/cross-project-coordination.md) for multi-project orchestration.

---

## Resources

- [Project Registry](references/project-registry.md)
- [GitHub Projects Sync](references/github-projects-sync.md)
- [Cross-Project Coordination](references/cross-project-coordination.md)

---

**Version:** 1.0
**Last Updated:** 2025-02-01
**Target Audience:** Chief of Staff Agents
**Difficulty Level:** Advanced
