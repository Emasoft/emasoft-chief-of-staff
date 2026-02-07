# Edge Case Protocols for Chief of Staff Agent

This document defines standardized protocols for handling edge cases and failure scenarios in the Chief of Staff Agent (ecos-) plugin.

## Table of Contents

- 1.0 AI Maestro Unavailable
  - 1.1 Detection Methods
  - 1.2 Response Workflow
  - 1.3 Fallback Communication
- 2.0 GitHub Unavailable
  - 2.1 Detection Methods
  - 2.2 Response Workflow
  - 2.3 Status Caching
- 3.0 Remote Agent Timeout
  - 3.1 Detection Methods
  - 3.2 Architect Agent Timeout
  - 3.3 Orchestrator Agent Timeout
  - 3.4 Integrator Agent Timeout
- 4.0 User Incomplete Input
  - 4.1 Detection Methods
  - 4.2 Clarification Protocol
  - 4.3 Progressive Requirement Gathering
- 5.0 Approval Workflow Failures
  - 5.1 User Unresponsive
  - 5.2 Conflicting Approvals
  - 5.3 Approval Timeout
- 6.0 Role Routing Failures
  - 6.1 Agent Unavailable
  - 6.2 Ambiguous Routing
  - 6.3 Capacity Issues
- 7.0 Handoff Failures
  - 7.1 Missing Handoff Files
  - 7.2 Corrupted Handoff Data
  - 7.3 Version Mismatch
- 8.0 Session Memory Failures
  - 8.1 Memory Load Failure
  - 8.2 Memory Save Failure
  - 8.3 Memory Corruption

---

## 1.0 AI Maestro Unavailable

### 1.1 Detection Methods

The Chief of Staff is the primary communication hub. AI Maestro unavailability severely impacts operations.

| Check | Method | Failure Indicator |
|-------|--------|-------------------|
| API Health | Use the `ai-maestro-agents-management` skill to check AI Maestro health | HTTP 503/504 or timeout |
| Connection Test | Use the `agent-messaging` skill to check unread message count | Connection timeout after 10 seconds |
| Agent Registry | Use the `ai-maestro-agents-management` skill to list agents | Registry unreachable |

### 1.2 Response Workflow

When AI Maestro is unavailable:

1. **Log the failure**:
   ```bash
   echo "$(date -Iseconds) | AIMAESTRO_UNAVAILABLE | $AIMAESTRO_API" >> .claude/logs/maestro-failures.log
   ```

2. **Queue ALL outgoing messages**:
   ```bash
   mkdir -p .claude/queue/outbox
   # Queue for each role
   for role in architect orchestrator integrator; do
     if [ -n "$MESSAGE_FOR_${role^^}" ]; then
       cat > ".claude/queue/outbox/${role}-$(date +%s).json" <<EOF
   {
     "to": "${role}",
     "subject": "${SUBJECT}",
     "priority": "${PRIORITY}",
     "content": {"type": "${TYPE}", "message": "${MESSAGE}"},
     "queued_at": "$(date -Iseconds)"
   }
   EOF
     fi
   done
   ```

3. **Display warning to user**:
   ```
   WARNING: AI Maestro is unavailable.

   Impact:
   - Cannot send messages to Architect, Orchestrator, Integrator
   - Queued N outgoing messages
   - Status updates may be delayed

   Workaround:
   - Direct file-based communication available
   - GitHub Issues can be used for urgent matters

   Will retry every 5 minutes.
   After 30 minutes, will request user guidance.
   ```

4. **Use fallback communication** (see 1.3)

5. **Retry every 5 minutes**

### 1.3 Fallback Communication

When AI Maestro is down, use these methods:

| Priority | Method | For |
|----------|--------|-----|
| 1st | Direct handoff files | Complex instructions |
| 2nd | GitHub Issues | Urgent items, permanent record |
| 3rd | Shared directory polling | Simple status checks |

**Handoff File Fallback**:
```bash
mkdir -p .claude/handoffs
cat > ".claude/handoffs/to-${ROLE}-$(date +%s).md" <<EOF
# Handoff: User Request

**From**: Chief of Staff
**To**: ${ROLE}
**Priority**: ${PRIORITY}
**Timestamp**: $(date -Iseconds)

## Request
${REQUEST_DETAILS}

## Expected Response
${EXPECTED_RESPONSE}

## Delivery Method
Please respond via GitHub Issue #${ISSUE_NUMBER} or handoff file.
---
*AI Maestro unavailable - using file-based handoff*
EOF
```

---

## 2.0 GitHub Unavailable

### 2.1 Detection Methods

| Check | Command | Failure Indicator |
|-------|---------|-------------------|
| API Status | `gh api rate_limit` | HTTP 5xx errors |
| Network | `gh repo view` | Network failure |
| Rate Limit | `gh api rate_limit --jq '.rate.remaining'` | Returns 0 |

### 2.2 Response Workflow

1. **Cache current state**:
   ```bash
   mkdir -p .claude/cache/github
   gh issue list --json number,title,state,labels > .claude/cache/github/issues.json
   gh pr list --json number,title,state > .claude/cache/github/prs.json
   echo "$(date -Iseconds)" > .claude/cache/github/cached_at
   ```

2. **Notify user**:
   ```
   WARNING: GitHub is temporarily unavailable.

   - Status reports will use cached data (from: [timestamp])
   - Issue/PR operations are queued
   - Will retry every 10 minutes

   Cached State Summary:
   - Open Issues: N
   - Open PRs: M
   - Last sync: [timestamp]
   ```

3. **Queue GitHub operations**:
   ```bash
   mkdir -p .claude/queue/github
   cat > ".claude/queue/github/op-$(date +%s).json" <<EOF
   {
     "operation": "issue_comment|pr_review|label_update",
     "target": "issue_number or pr_number",
     "params": {...},
     "queued_at": "$(date -Iseconds)"
   }
   EOF
   ```

4. **Continue with cached data**

5. **Retry every 10 minutes**

### 2.3 Status Caching

Maintain cached status for user reports:

| Data | Location | Use |
|------|----------|-----|
| Issues | `.claude/cache/github/issues.json` | Status reports |
| PRs | `.claude/cache/github/prs.json` | Merge status |
| Project board | `.claude/cache/github/project.json` | Progress view |

**Cached Status Report Template**:
```markdown
## Project Status (Cached Data)

**Warning**: GitHub unavailable. Data from [timestamp].

### Open Issues
| # | Title | Labels |
|---|-------|--------|
[cached data]

### Open PRs
| # | Title | Status |
|---|-------|--------|
[cached data]

*Status may be outdated. Will refresh when GitHub recovers.*
```

---

## 3.0 Remote Agent Timeout

### 3.1 Detection Methods

| Condition | Threshold | Detection |
|-----------|-----------|-----------|
| No ACK received | 5 minutes | Agent did not acknowledge request |
| No progress update | 20 minutes | No status update after ACK |
| Session terminated | Immediate | AI Maestro reports agent offline |

### 3.2 Architect Agent Timeout

When Architect does not respond:

1. **First Reminder (5 min no ACK / 20 min no progress)**:
   ```
   To Architect: Status check on design task [TASK_ID].
   Please provide update or confirm you are working on this.
   ```

2. **Wait 5 minutes**

3. **Urgent Reminder**:
   ```
   URGENT: Design task [TASK_ID] - no response.
   Will escalate to user in 5 minutes if no response.
   ```

4. **Escalate to User**:
   ```
   USER ATTENTION REQUIRED

   Architect agent is not responding.
   Task: [TASK_ID] - [DESCRIPTION]
   Waited: 15 minutes

   Options:
   1. Wait longer (specify time)
   2. Restart Architect session
   3. Proceed without design (high risk)
   4. Cancel the request

   Please advise.
   ```

### 3.3 Orchestrator Agent Timeout

When Orchestrator does not respond:

1. **Follow same escalation ladder**

2. **User options include**:
   ```
   Options:
   1. Wait longer
   2. Restart Orchestrator session
   3. Check task status manually
   4. Pause all orchestration
   ```

3. **If user chooses to proceed without Orchestrator**:
   - Warn about loss of coordination
   - Suggest direct agent communication
   - Document the deviation

### 3.4 Integrator Agent Timeout

When Integrator does not respond:

1. **Follow same escalation ladder**

2. **User options include**:
   ```
   Options:
   1. Wait longer
   2. Restart Integrator session
   3. Review PRs manually
   4. Pause integration work
   ```

3. **Critical warning if pending merges**:
   ```
   WARNING: Integrator offline with pending PR merges.

   Pending PRs:
   - PR #123: Ready to merge
   - PR #124: Awaiting review

   These will not be processed until Integrator recovers.
   Consider manual review if urgent.
   ```

---

## 4.0 User Incomplete Input

### 4.1 Detection Methods

| Missing Element | Detection Pattern |
|-----------------|-------------------|
| Project name | User request lacks subject identifier |
| Requirements | "Do something" without specifics |
| Success criteria | No definition of done |
| Constraints | No performance/security/timeline requirements |
| Scope | "Make it better" without scope boundaries |

### 4.2 Clarification Protocol

1. **Acknowledge the request**:
   ```
   Thank you for your request. I want to make sure I understand correctly.
   ```

2. **List what was understood**:
   ```
   What I understand:
   - You want to [interpreted request]
   - This relates to [project/context if known]
   ```

3. **List what needs clarification**:
   ```
   To proceed, I need the following information:

   REQUIRED:
   1. [Specific question about missing requirement]
   2. [Specific question about scope]

   OPTIONAL (but helpful):
   3. [Question about preferences]
   4. [Question about constraints]
   ```

4. **Block progression** until required items answered

5. **Confirm understanding** before routing to other agents:
   ```
   Let me confirm my understanding:

   - Project: [name]
   - Goal: [goal]
   - Scope: [scope]
   - Success criteria: [criteria]

   Is this correct? (yes/no/corrections)
   ```

### 4.3 Progressive Requirement Gathering

For complex requests, gather requirements progressively:

**Phase 1: High-Level**
```
1. What is the main goal?
2. Who will use this?
3. When do you need it?
```

**Phase 2: Details** (after Phase 1 answered)
```
4. What specific features are required?
5. Are there any constraints (budget, tech stack, etc.)?
6. What does success look like?
```

**Phase 3: Validation** (after Phase 2 answered)
```
7. Let me summarize the requirements...
8. Is anything missing?
9. Shall I proceed with routing this to the Architect?
```

---

## 5.0 Approval Workflow Failures

### 5.1 User Unresponsive

**Detection**: Approval request pending for more than 2 hours.

**Response Workflow**:

1. **Send reminder**:
   ```
   REMINDER: Approval Request Pending

   Request: [DESCRIPTION]
   Requested: [TIME] (2 hours ago)

   This is blocking progress on [TASK/PROJECT].

   Please respond with: approve / reject / defer
   ```

2. **If still no response after 4 hours**:
   ```
   SECOND REMINDER: Approval Required

   Request: [DESCRIPTION]
   Waiting: 4 hours

   Impact: [DESCRIPTION OF BLOCKED WORK]

   Options:
   1. Approve now
   2. Reject (with reason)
   3. Defer (specify when to ask again)
   4. Delegate (specify who can approve)
   ```

3. **After 8 hours**, log and wait for user to return:
   ```
   APPROVAL PENDING - User Unresponsive

   Request: [DESCRIPTION]
   Status: On hold - awaiting user input

   Work on [PROJECT] is paused until approval received.

   This message will remain until you respond.
   ```

### 5.2 Conflicting Approvals

**Detection**: Multiple approval requests with conflicting outcomes.

**Response Workflow**:

1. **Present the conflict**:
   ```
   APPROVAL CONFLICT DETECTED

   Request A: Deploy to production
   Your Response: Approved

   Request B: Hold all deployments for security review
   Your Response: Approved

   These are mutually exclusive. Please clarify:
   1. Proceed with deployment (ignore security hold)
   2. Honor security hold (delay deployment)
   3. Modified approach: [suggest alternative]
   ```

2. **Block both actions** until resolved

3. **Document resolution** for audit trail

### 5.3 Approval Timeout

**Detection**: Approval has explicit deadline that passed.

**Response Workflow**:

1. **If non-critical**:
   ```
   APPROVAL EXPIRED

   Request: [DESCRIPTION]
   Deadline: [TIME] (passed)

   The approval window has closed.
   Should I resubmit the request? (yes/no)
   ```

2. **If critical**:
   ```
   CRITICAL: Approval Deadline Missed

   Request: [DESCRIPTION]
   Impact: [DESCRIPTION OF IMPACT]

   Immediate action required:
   1. Approve now (if still valid)
   2. Cancel request
   3. Escalate to [alternative approver]
   ```

---

## 6.0 Role Routing Failures

### 6.1 Agent Unavailable

**Detection**: Target role agent is offline or unresponsive.

**Response Workflow**:

1. **Check agent status**:
   Use the `ai-maestro-agents-management` skill to query the status of the target agent by name.

2. **If offline**:
   ```
   AGENT UNAVAILABLE: ${ROLE^}

   The ${ROLE} agent is currently offline.

   Options:
   1. Queue request (will be delivered when agent returns)
   2. Wait for agent to come online
   3. Proceed with alternative approach

   What would you like to do?
   ```

3. **Queue the request** with notification settings

### 6.2 Ambiguous Routing

**Detection**: Request could go to multiple roles.

**Response Workflow**:

1. **Present the ambiguity**:
   ```
   ROUTING CLARIFICATION NEEDED

   Your request could be handled by:

   1. ARCHITECT - If you need design/planning
      "Design the authentication system architecture"

   2. ORCHESTRATOR - If you need implementation coordination
      "Start implementing the authentication system"

   3. INTEGRATOR - If you need code review/merging
      "Review the authentication PR"

   Which best describes your intent?
   ```

2. **Wait for user clarification**

3. **Route accordingly**

### 6.3 Capacity Issues

**Detection**: Target role agent at capacity.

**Response Workflow**:

1. **Check capacity**:
   ```
   CAPACITY LIMIT: ${ROLE^}

   The ${ROLE} agent is currently at capacity.

   Current workload:
   - Task 1: [description] (in progress)
   - Task 2: [description] (in progress)
   - Task 3: [description] (queued)

   Options:
   1. Queue this request (estimated wait: [TIME])
   2. Increase priority (may delay other tasks)
   3. Wait for current tasks to complete

   What would you like to do?
   ```

2. **Act on user choice**

---

## 7.0 Handoff Failures

### 7.1 Missing Handoff Files

**Detection**: Expected handoff file not found.

**Response Workflow**:

1. **Search for handoff**:
   ```bash
   # Check standard locations
   find .claude/handoffs -name "*${UUID}*" -o -name "*${PROJECT}*"
   ```

2. **If not found**:
   ```
   HANDOFF FILE MISSING

   Expected: .claude/handoffs/${FILENAME}
   Source: ${SOURCE_AGENT}

   Attempting recovery:
   1. Requesting resend from ${SOURCE_AGENT}
   2. Checking backup locations

   Please wait...
   ```

3. **Request resend** from source agent

4. **If still missing**, escalate to user

### 7.2 Corrupted Handoff Data

**Detection**: Handoff file fails JSON/schema validation.

**Response Workflow**:

1. **Identify corruption**:
   ```
   HANDOFF DATA CORRUPTED

   File: .claude/handoffs/${FILENAME}
   Error: ${VALIDATION_ERROR}

   Attempting to extract valid data...
   ```

2. **Attempt partial recovery**:
   - Extract readable sections
   - Document what was recovered
   - Document what was lost

3. **Request clarification** on missing/corrupted sections

### 7.3 Version Mismatch

**Detection**: Handoff format version incompatible.

**Response Workflow**:

1. **Report the mismatch**:
   ```
   HANDOFF VERSION MISMATCH

   File: .claude/handoffs/${FILENAME}
   File Version: ${FILE_VERSION}
   Expected Version: ${EXPECTED_VERSION}

   This may cause data interpretation errors.

   Options:
   1. Attempt conversion (may lose some data)
   2. Request resend in current format
   3. Proceed with manual interpretation
   ```

2. **Act on user choice**

---

## 8.0 Session Memory Failures

### 8.1 Memory Load Failure

**Detection**: SessionStart hook fails to load memory.

**Response Workflow**:

1. **Check memory files**:
   ```bash
   ls -la .claude/memory/
   # Check for: active-context.json, progress.json, decisions.json
   ```

2. **If files missing**:
   ```
   SESSION MEMORY: Starting Fresh

   No previous session memory found.

   This could mean:
   - New project (expected)
   - Memory files deleted (check backups)
   - Wrong project directory

   Proceeding with empty session memory.
   Previous context will need to be re-established.
   ```

3. **If files exist but corrupted**:
   ```
   SESSION MEMORY: Corruption Detected

   Memory files exist but cannot be loaded.

   Attempting recovery from backups...
   Found backup from: [TIMESTAMP]

   Options:
   1. Restore from backup
   2. Start fresh (lose previous context)
   3. Manual inspection (advanced)
   ```

### 8.2 Memory Save Failure

**Detection**: SessionEnd hook fails to save memory.

**Response Workflow**:

1. **Attempt retry**:
   ```
   SESSION MEMORY: Save Failed

   Attempting to save session memory...
   Retry 1/3...
   ```

2. **If retries fail**:
   ```
   SESSION MEMORY: CRITICAL SAVE FAILURE

   Could not save session memory to disk.

   Error: ${ERROR_MESSAGE}

   Recovery options:
   1. Check disk space
   2. Check file permissions
   3. Save to alternative location

   CURRENT SESSION STATE:
   [Display current context summary]

   Please copy this information if needed before closing.
   ```

3. **Attempt alternative save location**:
   ```bash
   mkdir -p /tmp/claude-memory-recovery
   cp -r .claude/memory/* /tmp/claude-memory-recovery/
   ```

### 8.3 Memory Corruption

**Detection**: Memory files fail integrity check.

**Response Workflow**:

1. **Detect corruption**:
   ```
   SESSION MEMORY: Integrity Check Failed

   File: .claude/memory/${FILENAME}
   Issue: ${CORRUPTION_DESCRIPTION}

   Checking backups...
   ```

2. **Restore from backup if available**:
   ```
   Found backup from [TIMESTAMP].

   Backup contains:
   - Tasks: N entries
   - Decisions: M entries
   - Context: [summary]

   Restore this backup? (yes/no)
   ```

3. **If no backup**, start fresh with documentation:
   ```
   No valid backup available.

   Starting fresh session.

   Please note: Previous context has been lost.
   You may need to re-establish:
   - Current project state
   - In-progress tasks
   - Pending decisions
   ```

---

## Emergency Recovery

If multiple edge cases compound:

1. **Prioritize user communication**
2. **Save all current state locally**:
   ```bash
   mkdir -p .claude/recovery/$(date +%Y%m%d_%H%M%S)
   cp -r .claude/memory .claude/handoffs .claude/queue .claude/recovery/
   ```

3. **Present clear status to user**:
   ```
   SYSTEM STATUS: Multiple Issues Detected

   AI Maestro: [status]
   GitHub: [status]
   Architect: [status]
   Orchestrator: [status]
   Integrator: [status]
   Memory: [status]

   Impact: [summary of what's not working]

   Recommended Action: [specific recommendation]

   All data has been saved to: .claude/recovery/[timestamp]
   ```

4. **Wait for user guidance**

---

## Related Documents

- [01-initialize-session-memory.md](./01-initialize-session-memory.md) - Memory initialization
- [10-recovery-procedures.md](./10-recovery-procedures.md) - Detailed recovery
- [14-context-sync.md](./14-context-sync.md) - Context synchronization
- [SKILL.md](../SKILL.md) - Core Chief of Staff skill
