# Project Handoff Reference

## Table of Contents

- 3.1 [Preparing For Project Handoff](#31-preparing-for-project-handoff)
- 3.2 [Providing Project Overview](#32-providing-project-overview)
- 3.3 [Sharing Current State](#33-sharing-current-state)
- 3.4 [Explaining Project Conventions](#34-explaining-project-conventions)
- 3.5 [Transferring Working Knowledge](#35-transferring-working-knowledge)
- 3.6 [Verifying Handoff Completion](#36-verifying-handoff-completion)
- 3.7 [Project Handoff Examples](#37-project-handoff-examples)
- 3.8 [Troubleshooting](#38-troubleshooting)

---

## 3.1 Preparing For Project Handoff

Before conducting a project handoff, gather all necessary information.

### Information Gathering Checklist

```markdown
## Pre-Handoff Checklist

Project: [project name]
Receiving Agent: [session name]
Date: [date]

### Project Documentation
- [ ] Project README location identified
- [ ] Architecture docs available
- [ ] API documentation current
- [ ] Setup/installation guide exists

### Current State
- [ ] Current sprint/milestone known
- [ ] Active tasks documented
- [ ] Blockers identified
- [ ] Recent changes summarized

### Codebase
- [ ] Repository location confirmed
- [ ] Key directories identified
- [ ] Coding conventions documented
- [ ] Test structure known

### Context
- [ ] Handoff reason documented
- [ ] Previous agent notes gathered (if transfer)
- [ ] Known issues listed
- [ ] Upcoming priorities noted
```

### Handoff Document Preparation

Create a handoff document to share with the receiving agent:

**Location:** `design/memory/handoffs/[project]-[date].md`

**Template:**
```markdown
# Project Handoff: [Project Name]

**Date:** [ISO timestamp]
**From:** [previous agent or Chief of Staff]
**To:** [receiving agent session name]

## 1. Project Overview
[Summary of what the project is]

## 2. Current State
[What is done, in progress, and pending]

## 3. Key Files and Directories
[Map of important locations]

## 4. Conventions
[How things are done in this project]

## 5. Active Context
[What the agent needs to know right now]

## 6. First Task
[What to do first]
```

---

## 3.2 Providing Project Overview

The project overview gives the agent essential context about what they are working on.

### Overview Components

**1. Project Purpose**

What is being built and why:

```markdown
## Project Purpose

This project is the **Authentication Module** for the main application.

**Goals:**
- Provide secure user login and logout
- Manage user sessions
- Support password reset flows

**Users:**
- End users of the application
- Other microservices that need to verify authentication
```

**2. Project Scope**

What is included and excluded:

```markdown
## Project Scope

**In Scope:**
- Login/logout endpoints
- Session management
- Password reset flow
- JWT token generation

**Out of Scope:**
- User registration (handled by User module)
- Authorization/permissions (handled by RBAC module)
- 2FA (future phase)
```

**3. Technology Stack**

What technologies are used:

```markdown
## Technology Stack

- **Language:** Python 3.12
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **Testing:** pytest
- **Authentication:** JWT with refresh tokens
```

**4. Architecture Overview**

How the system is structured:

```markdown
## Architecture

The module follows a layered architecture:

1. **API Layer** (src/api/): HTTP endpoint handlers
2. **Service Layer** (src/services/): Business logic
3. **Repository Layer** (src/repositories/): Database access
4. **Models** (src/models/): Data structures

External integrations:
- Redis for session storage
- Email service for password reset
```

---

## 3.3 Sharing Current State

The receiving agent must understand what has been done and what remains.

### Sprint/Milestone State

```markdown
## Current Sprint: Sprint 5

**Sprint Goal:** Complete core authentication flow
**Duration:** Jan 20 - Feb 3, 2025
**Days Remaining:** 3

### Sprint Tasks

| Task | Status | Assignee | Notes |
|------|--------|----------|-------|
| TASK-041: Login endpoint | Complete | - | Merged PR #120 |
| TASK-042: Logout endpoint | In Progress | YOU | 60% complete |
| TASK-043: Password reset | Not Started | - | Blocked by logout |
| TASK-044: Session refresh | Not Started | - | Low priority |
```

### Active Work Description

```markdown
## Active Work: TASK-042 Logout Endpoint

### What Has Been Done
- Endpoint skeleton created at src/api/auth.py:145
- Token validation logic implemented
- Unit tests for token validation added

### What Remains
- Implement session invalidation in Redis
- Add logout event logging
- Write integration tests
- Update API documentation

### Current Location
- File: src/api/auth.py
- Line: 145
- Function: logout_user()

### Next Step
Implement the Redis session invalidation. The Redis client is already configured in src/core/redis.py.
```

### Known Issues

```markdown
## Known Issues

1. **ISSUE-012: Session timeout inconsistency**
   - Sometimes sessions expire early
   - Workaround: Refresh token more frequently
   - Fix planned for next sprint

2. **ISSUE-015: Slow login on cold start**
   - First login after restart takes 2-3 seconds
   - Cause: Database connection pool warming
   - Low priority, not blocking
```

---

## 3.4 Explaining Project Conventions

Conventions ensure the agent's work fits with existing code.

### Coding Conventions

```markdown
## Coding Conventions

### Code Style
- Use ruff for formatting (line length 88)
- Type hints required for all functions
- Docstrings required for public functions

### Naming
- Functions: snake_case
- Classes: PascalCase
- Constants: UPPER_SNAKE_CASE
- Private: prefix with underscore

### File Organization
- One class per file for large classes
- Related utilities can share a file
- Tests mirror source structure
```

### Testing Conventions

```markdown
## Testing Conventions

### Test Organization
- Unit tests: tests/unit/
- Integration tests: tests/integration/
- Test files: test_[module_name].py

### Test Naming
- test_[function]_[scenario]_[expected_result]
- Example: test_login_invalid_password_returns_401

### Test Requirements
- Unit tests for all public functions
- Integration tests for all API endpoints
- Minimum 80% coverage for new code
```

### Git Conventions

```markdown
## Git Conventions

### Branches
- main: production-ready code
- develop: integration branch
- feature/[TASK-ID]-[short-description]: feature work
- fix/[ISSUE-ID]-[short-description]: bug fixes

### Commits
- Prefix: feat:, fix:, docs:, test:, refactor:
- Include task/issue ID
- Example: "feat(TASK-042): implement session invalidation"

### Pull Requests
- Title: [TASK-ID] Short description
- Description: What, Why, How, Testing
- Must pass CI before review
```

### Communication Conventions

```markdown
## Communication Conventions

### Status Updates
- Provide regular updates during active work
- Include: task ID, progress, blockers

### Completion Reports
- Include: what was done, PR link, what to verify

### Asking for Help
- First: check documentation
- Second: search codebase for examples
- Third: ask team via AI Maestro
```

---

## 3.5 Transferring Working Knowledge

Working knowledge is the practical information that helps an agent be effective.

### Key Files Map

```markdown
## Key Files

### Core Files
- `src/api/auth.py` - Authentication endpoints
- `src/services/auth_service.py` - Auth business logic
- `src/repositories/user_repository.py` - User data access
- `src/core/security.py` - JWT and password utilities

### Configuration
- `config/settings.py` - Application settings
- `.env` - Environment variables (not in repo)

### Tests
- `tests/unit/test_auth_service.py` - Service tests
- `tests/integration/test_auth_api.py` - API tests

### Documentation
- `docs/API.md` - API documentation
- `docs/ARCHITECTURE.md` - Architecture overview
```

### Common Patterns

```markdown
## Common Patterns in This Codebase

### Error Handling
```python
# All endpoints use HTTPException
from fastapi import HTTPException

def login(credentials: LoginRequest):
    if not valid:
        raise HTTPException(status_code=401, detail="Invalid credentials")
```

### Database Access
```python
# Always use repository pattern
user = user_repository.get_by_email(email)
# Never write SQL directly in services
```

### Response Format
```python
# All responses use standard format
return {"status": "success", "data": result}
# Errors: {"status": "error", "message": "..."}
```
```

### Gotchas and Tips

```markdown
## Gotchas and Tips

### Things That Might Trip You Up

1. **Redis Keys**: Session keys include user ID prefix
   - Correct: `session:user:123:token`
   - Wrong: `session:token`

2. **Time Zones**: All timestamps are UTC
   - Use `datetime.utcnow()` not `datetime.now()`

3. **Environment Variables**: Some are loaded at import time
   - Restart needed after changing .env

### Tips for Success

1. Run tests frequently: `pytest tests/unit/ -v`
2. Check lint before committing: `ruff check src/`
3. The auth service has good examples to follow
4. When in doubt, check existing endpoints for patterns
```

---

## 3.6 Verifying Handoff Completion

After the handoff, verify the receiving agent can work effectively.

### Verification Steps

**Step 1: Access Verification**

Confirm the agent can access required resources:

```markdown
## Access Verification

Ask agent to confirm:
- [ ] Can read project README at /path/to/README.md
- [ ] Can access source code at /src/
- [ ] Can run tests: `pytest tests/unit/ -v`
- [ ] Can send messages via AI Maestro
```

**Step 2: Understanding Verification**

Confirm the agent understands the project:

```markdown
## Understanding Verification

Ask agent to explain:
- [ ] What is the project's purpose?
- [ ] What is the current state of TASK-042?
- [ ] What are the coding conventions for this project?
- [ ] What should be done if blocked?
```

**Step 3: Practical Verification**

Have agent complete a simple task:

```markdown
## Practical Verification

Ask agent to:
- [ ] Read the active file (src/api/auth.py)
- [ ] Identify the current work location (line 145)
- [ ] Describe what the next step should be
- [ ] Send a test status update
```

### Handoff Sign-Off

Once verified, document completion:

```markdown
## Handoff Completion

**Handoff Complete:** YES
**Verified By:** chief-of-staff-agent
**Date:** 2025-02-01T10:30:00Z

**Verification Results:**
- Access: All resources accessible
- Understanding: Correctly explained project and state
- Practical: Successfully identified next step

**Agent Ready:** YES
**First Task Assigned:** Continue TASK-042 logout endpoint
```

---

## 3.7 Project Handoff Examples

### Example: New Agent Joining Project

```markdown
# Project Handoff: Auth Module

**Date:** 2025-02-01T10:00:00Z
**To:** helper-agent-generic (newly assigned Developer)

## 1. Project Overview

You are joining the Authentication Module project. This module handles user login, logout, and session management for the main application.

**Tech Stack:** Python 3.12, FastAPI, PostgreSQL, Redis
**Sprint:** Sprint 5 (3 days remaining)

## 2. Current State

| Task | Status | Notes |
|------|--------|-------|
| Login endpoint | Complete | PR #120 merged |
| Logout endpoint | In Progress | Your focus |
| Password reset | Not Started | Next priority |

## 3. Key Files

- `src/api/auth.py` - Endpoints (your focus: line 145)
- `src/services/auth_service.py` - Business logic
- `tests/unit/test_auth_service.py` - Unit tests

## 4. Conventions

- Type hints required
- 80% test coverage minimum
- Commit format: "feat(TASK-ID): description"

## 5. Your Assignment

Continue TASK-042: Logout endpoint
- Current progress: 60%
- Next step: Implement Redis session invalidation
- Priority: High

## 6. Getting Started

1. Read src/api/auth.py, focus on logout_user() at line 145
2. Review src/core/redis.py for Redis client usage
3. Run existing tests: pytest tests/unit/test_auth_service.py -v
4. Send status update when you've oriented yourself
```

### Example: Agent-to-Agent Transfer

```markdown
# Project Handoff: Auth Module

**Date:** 2025-02-01T14:00:00Z
**From:** original-developer-agent
**To:** helper-agent-generic (taking over)

## 1. Why This Transfer

original-developer-agent is being reassigned to a higher priority project. You are taking over their in-progress work.

## 2. Work in Progress

### TASK-042: Logout Endpoint (60% complete)

**What I completed:**
- Endpoint skeleton at src/api/auth.py:145
- Token validation logic
- Basic unit tests

**What remains:**
- Redis session invalidation (see TODO at line 167)
- Logout event logging
- Integration tests

**Current blocker:** None, ready to continue

### My Notes

- The Redis client in src/core/redis.py has a delete_session() method that should work
- I was planning to add logging at the service layer, not API layer
- Integration tests should follow the pattern in test_login_api.py

## 3. Files I Modified

- src/api/auth.py (logout_user function)
- tests/unit/test_auth_service.py (added logout tests)

## 4. PRs in Progress

- PR #125: WIP logout endpoint (draft, do not merge yet)

## 5. Recommendations

- Review my commits in PR #125 for context
- The session invalidation should take about 2 hours
- Ask me via AI Maestro if anything is unclear
```

---

## 3.8 Troubleshooting

### Issue: Agent cannot find referenced files

**Symptoms:** File not found errors, confusion about paths.

**Possible causes:**
- Paths are relative, agent needs absolute
- Directory structure changed since handoff doc
- Agent looking in wrong location

**Resolution:**
1. Provide absolute paths
2. Verify files exist at specified locations
3. Update handoff doc if structure changed
4. Have agent list directory to confirm access

### Issue: Agent misunderstands project state

**Symptoms:** Agent attempts already-completed work, skips incomplete work.

**Possible causes:**
- Handoff doc is outdated
- State changed after handoff
- Agent misread the state section

**Resolution:**
1. Verify handoff doc is current
2. Re-explain current state clearly
3. Have agent summarize state back to confirm
4. Update handoff doc if corrections needed

### Issue: Agent cannot run tests

**Symptoms:** Test commands fail, dependencies missing.

**Possible causes:**
- Environment not configured
- Dependencies not installed
- Virtual environment not activated

**Resolution:**
1. Verify test command is correct
2. Ensure dependencies are installed (`uv sync`)
3. Check virtual environment activation
4. Provide step-by-step setup if needed

### Issue: Conventions not followed after handoff

**Symptoms:** Agent code does not match project style.

**Possible causes:**
- Conventions section was unclear
- Agent has habits from other projects
- Conventions doc is outdated

**Resolution:**
1. Point to specific convention violations
2. Provide concrete examples of correct style
3. Reference existing code as templates
4. Run linter to catch style issues early

### Issue: Handoff takes too long

**Symptoms:** Handoff consumes excessive time, delays work start.

**Possible causes:**
- Too much information transferred
- Agent asks many clarifying questions
- Handoff doc disorganized

**Resolution:**
1. Focus on essential information only
2. Defer non-urgent details to follow-up
3. Organize handoff doc with clear sections
4. Provide links to detailed docs rather than including all content

---

**Version:** 1.0
**Last Updated:** 2025-02-01
