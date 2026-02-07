# Error Handling Reference

## Table of Contents

- 1.1 [Error Handling Philosophy](#11-error-handling-philosophy)
- 1.2 [Error Categories](#12-error-categories)
- 1.3 [Communication Errors](#13-communication-errors)
- 1.4 [Coordination Errors](#14-coordination-errors)
- 1.5 [Resource Errors](#15-resource-errors)
- 1.6 [State Management Errors](#16-state-management-errors)
- 1.7 [Error Logging and Reporting](#17-error-logging-and-reporting)
- 1.8 [Recovery Procedures](#18-recovery-procedures)

---

## 1.1 Error Handling Philosophy

The Chief of Staff follows a fail-fast approach: errors are surfaced immediately rather than hidden or worked around. This prevents small issues from becoming large problems.

### Core Principles

**1. Fail Fast**
When an error occurs, report it immediately. Do not:
- Suppress or ignore errors
- Implement silent fallbacks
- Continue with incomplete data

**2. Fail Loud**
Make errors visible:
- Log all errors with context
- Report errors to relevant parties
- Update state to reflect error conditions

**3. No Workarounds**
Do not implement workarounds for errors:
- Fix the root cause
- If cannot fix, escalate
- Workarounds hide problems and create debt

**4. Explicit Recovery**
Recovery must be explicit, not automatic:
- Document recovery procedures
- Require confirmation before recovery
- Verify state after recovery

### Error Response Flow

```
Error Occurs
    ↓
Log Error (always)
    ↓
Assess Severity
    ↓
┌─────────────────────────────────────┐
│ Critical: Stop work, escalate       │
│ High: Pause task, notify            │
│ Medium: Continue, track for review  │
│ Low: Log only, continue             │
└─────────────────────────────────────┘
    ↓
Update State
    ↓
Notify Relevant Parties
    ↓
Await Resolution (if Critical/High)
```

---

## 1.2 Error Categories

### Communication Errors

Errors in inter-agent messaging:
- Message delivery failure
- Response timeout
- Invalid message format
- Session not found

### Coordination Errors

Errors in team coordination:
- Role assignment failure
- Task conflict
- Duplicate assignment
- Missing acknowledgment

### Resource Errors

Errors related to system resources:
- Memory exhaustion
- Disk full
- Network unavailable
- Rate limit exceeded

### State Management Errors

Errors in state file operations:
- File read failure
- File write failure
- Corrupted state
- Inconsistent state

### Integration Errors

Errors with external systems:
- AI Maestro unavailable
- API failures
- Authentication issues
- Version mismatch

---

## 1.3 Communication Errors

### Message Delivery Failure

**Error:** Message sent but not delivered

**Detection:**
- No delivery confirmation
- API returns error
- Delivery status shows failed

**Response:**
```markdown
1. Log the failure with message details
2. Check recipient session exists
3. If exists: Retry once with backoff
4. If still fails: Report to orchestrator
5. Update pending actions with failure status
```

**Example:**
1. Use the `agent-messaging` skill to check the delivery status of the message by its ID
2. If delivery failed, use the `ai-maestro-agents-management` skill to check if the recipient session exists and is online

### Response Timeout

**Error:** Expected response not received within timeout

**Detection:**
- No response after expected time
- Request/acknowledgment not matched

**Response:**
```markdown
1. Log timeout with request details
2. Send reminder with higher priority
3. If still no response: Check agent status
4. If agent active: Escalate as potential issue
5. If agent inactive: Route to alternative agent
```

**Timeouts by Priority:**
| Priority | Initial Wait | Retry Wait | Max Attempts |
|----------|--------------|------------|--------------|
| Urgent | 5 min | 2 min | 3 |
| High | 15 min | 5 min | 2 |
| Normal | 30 min | 10 min | 2 |

### Invalid Message Format

**Error:** Received message has invalid format

**Detection:**
- JSON parse failure
- Missing required fields
- Wrong field types

**Response:**
```markdown
1. Log received message (sanitized)
2. Do not process malformed message
3. Reply to sender with format error
4. Request resend in correct format
```

### Session Not Found

**Error:** Recipient session does not exist

**Detection:**
- 404 from session lookup
- Session not in registry

**Response:**
```markdown
1. Log the lookup failure
2. Check for similar session names (typo?)
3. Check if session recently went offline
4. Update roster if session is gone
5. Route message to alternative if available
```

---

## 1.4 Coordination Errors

### Role Assignment Failure

**Error:** Cannot assign role to agent

**Detection:**
- Assignment rejected
- No acknowledgment received
- Agent reports inability

**Response:**
```markdown
1. Log assignment attempt and failure reason
2. If rejection: Check if role conflict exists
3. If no acknowledgment: Verify agent is active
4. If inability: Find alternative agent
5. Update roster to reflect actual state
```

### Task Conflict

**Error:** Multiple agents working on same task

**Detection:**
- Duplicate task updates
- Merge conflicts
- Agents report overlap

**Response:**
```markdown
1. Immediately notify both agents to pause
2. Determine who should continue
3. Have other agent abandon or merge work
4. Document conflict for prevention
5. Review assignment process
```

### Duplicate Assignment

**Error:** Task assigned to multiple agents

**Detection:**
- Task appears in multiple agent workloads
- Assignment log shows duplicates

**Response:**
```markdown
1. Stop new work on task
2. Identify all assigned agents
3. Designate single owner
4. Notify others to stop
5. Reconcile any parallel work
```

### Missing Acknowledgment

**Error:** Agent does not acknowledge assignment

**Detection:**
- No response to assignment message
- Agent continues other work
- Status does not update

**Response:**
```markdown
1. Send reminder with higher priority
2. If still no ack: Check agent status
3. If active but unresponsive: Flag for investigation
4. If inactive: Reassign to available agent
5. Document pattern if recurring
```

---

## 1.5 Resource Errors

### Memory Exhaustion

**Error:** System running out of memory

**Detection:**
- Memory usage > 95%
- Swap thrashing
- OOM warnings

**Response:**
```markdown
1. CRITICAL: Stop all non-essential operations
2. Request immediate context compaction from all agents
3. Terminate non-essential agents if needed
4. Notify user of emergency
5. Monitor until stable (< 80%)
```

### Disk Full

**Error:** No disk space available

**Detection:**
- Disk usage > 95%
- Write operations failing
- Log rotation failing

**Response:**
```markdown
1. CRITICAL: Stop all write operations
2. Identify largest files (logs, caches)
3. Delete oldest logs (preserve last hour)
4. Clear caches and temp files
5. Monitor until stable (< 85%)
```

### Network Unavailable

**Error:** Cannot reach AI Maestro or other services

**Detection:**
- Connection refused
- DNS failures
- Timeout on all requests

**Response:**
```markdown
1. Log connectivity failure
2. Attempt ping to localhost services
3. If AI Maestro down: Cannot coordinate, pause operations
4. Notify user of coordination pause
5. Retry connectivity every 1 minute
6. Resume operations when connectivity restored
```

### Rate Limit Exceeded

**Error:** API rate limit reached

**Detection:**
- 429 HTTP response
- Rate limit headers show zero remaining
- Requests being throttled

**Response:**
```markdown
1. Log rate limit hit with endpoint details
2. Check reset time from headers
3. Queue requests until reset
4. Reduce request frequency
5. Review patterns causing high usage
```

---

## 1.6 State Management Errors

### File Read Failure

**Error:** Cannot read state file

**Detection:**
- File not found
- Permission denied
- I/O error

**Response:**
```markdown
1. Log file access failure
2. Check file path is correct
3. Check permissions
4. If file missing: Check backup directory
5. If no backup: Initialize new state file
6. Report data loss if unrecoverable
```

### File Write Failure

**Error:** Cannot write state file

**Detection:**
- Write operation fails
- Disk full during write
- Permission denied

**Response:**
```markdown
1. CRITICAL: State may be lost
2. Log write failure with state content
3. Check disk space
4. Check permissions
5. Attempt write to alternative location
6. Hold state in memory until resolved
7. Notify user of potential state loss
```

### Corrupted State

**Error:** State file is corrupted or invalid

**Detection:**
- Parse error reading file
- Invalid structure
- Missing required sections

**Response:**
```markdown
1. Log corruption details
2. Attempt to parse valid sections
3. Check backup directory for recent valid copy
4. If backup available: Restore from backup
5. If no backup: Reconstruct from sources
6. Document what was lost
```

### Inconsistent State

**Error:** State contradicts reality or other sources

**Detection:**
- Roster differs from AI Maestro
- Metrics do not match logs
- References to non-existent items

**Response:**
```markdown
1. Identify the inconsistency
2. Determine authoritative source
3. Update state to match reality
4. Log the correction
5. Investigate how inconsistency arose
```

---

## 1.7 Error Logging and Reporting

### Error Log Format

```markdown
## Error Log Entry

**Timestamp:** [ISO timestamp]
**Error ID:** ERR-[sequential number]
**Category:** [communication|coordination|resource|state|integration]
**Severity:** [critical|high|medium|low]
**Component:** [cos-state|roster|messaging|etc]
**Operation:** [what was being attempted]

### Error Details
**Message:** [error message]
**Code:** [error code if any]

### Context
[relevant context for debugging]

### Stack/Trace
[any trace information if available]

### Response
**Action Taken:** [what was done]
**Result:** [outcome of action]
**Escalated:** [yes/no, to whom]
```

### Error Log Location

```
design/memory/errors/error-log-[YYYY-MM-DD].md
```

### Reporting Errors

**To Orchestrator:**
For coordination-affecting errors, high severity.

Use the `agent-messaging` skill to send:
- **Recipient**: the orchestrator session name (e.g., `orchestrator-master`)
- **Subject**: `Error Report: [brief description]`
- **Priority**: `high`
- **Content**: type `alert`, severity: "high", message: "Error in [component]: [description]. Action taken: [action]."

**To User:**
For critical errors or unresolved issues.

Use the `agent-messaging` skill to send to the user's agent or manager:
- **Recipient**: `eama-assistant-manager` (or the user's agent session name)
- **Subject**: `[CRITICAL ERROR] [Error Title]`
- **Priority**: `urgent`
- **Content**: type `error`, severity: "critical", message: "[Description and required action]."

---

## 1.8 Recovery Procedures

### Recovery Principles

1. **Stop the bleeding**: Prevent further damage first
2. **Assess the scope**: Understand what is affected
3. **Preserve evidence**: Log state before recovery
4. **Recover incrementally**: Test each step
5. **Verify completeness**: Confirm recovery worked

### Communication Recovery

```markdown
## Communication Recovery Procedure

When: AI Maestro connectivity lost and restored

1. Use the `ai-maestro-agents-management` skill to verify AI Maestro is healthy

2. Re-register session if needed using the `ai-maestro-agents-management` skill

3. Use the `agent-messaging` skill to check for missed messages (filter by time window: last 1 hour)

4. Process any missed messages in order

5. Send test message to verify operation

6. Resume normal operations
```

### State Recovery

```markdown
## State Recovery Procedure

When: State files corrupted or lost

1. Stop all state modifications

2. Check backup directory:
   ls design/memory/backups/

3. Find most recent valid backup

4. Restore from backup:
   cp backup/cos-state.md design/memory/

5. Validate restored state:
   - Check sections present
   - Verify timestamps reasonable
   - Compare to AI Maestro data

6. Reconcile any gaps:
   - Query AI Maestro for current team
   - Rebuild roster from sessions
   - Reset pending actions

7. Log recovery details

8. Resume operations
```

### Team Recovery

```markdown
## Team Recovery Procedure

When: Multiple agents offline or coordination broken

1. Use the `ai-maestro-agents-management` skill to list all registered sessions

2. Rebuild roster from query results

3. For each expected agent not present:
   - Log as missing
   - Check for recent messages
   - Notify user if critical role

4. For unexpected new agents:
   - Verify identity
   - Request role clarification
   - Add to roster or flag for review

5. Send team status broadcast

6. Verify responses from active agents

7. Resume normal coordination
```

### Full Reset

```markdown
## Full Reset Procedure

When: State unrecoverable, clean start needed

WARNING: This loses current state. Use only if necessary.

1. Confirm with user this is appropriate

2. Archive current state (even if broken):
   mv design/memory design/memory.broken.$(date +%s)

3. Create fresh directory structure:
   mkdir -p design/memory/{alerts,performance,onboarding,handoffs,backups}

4. Initialize empty state files:
   [initialize each required file]

5. Query AI Maestro for current reality:
   - Registered sessions
   - Pending messages
   - Recent history

6. Rebuild minimal state from reality

7. Notify all agents of reset

8. Resume with fresh state
```

---

**Version:** 1.0
**Last Updated:** 2025-02-01
