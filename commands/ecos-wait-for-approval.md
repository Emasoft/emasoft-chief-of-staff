---
name: ecos-wait-for-approval
description: "Wait for approval response from EAMA with configurable timeout and polling"
argument-hint: "--request-id <ID> [--timeout <SECONDS>] [--poll-interval <SECONDS>]"
allowed-tools: ["Bash(aimaestro-agent.sh:*)", "Task", "Bash(sleep:*)"]
user-invocable: true
---

# Wait For Approval Command

Wait for an approval response from the Assistant Manager (EAMA) with configurable timeout and polling interval.

## Usage

Poll for an approval response from EAMA using the `agent-messaging` skill:
1. Check for unread messages matching the request ID and type `approval_response`
2. Poll at the configured interval until response received or timeout
3. Return the approval decision when found

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--request-id <ID>` | **Yes** | Request ID to wait for (e.g., ECOS-20250202150000-a1b2c3d4) |
| `--timeout <SECONDS>` | No | Maximum wait time (default: 120 seconds) |
| `--poll-interval <SECONDS>` | No | Check frequency (default: 5 seconds) |
| `--quiet` | No | Minimal output, just return decision |
| `--on-approved <CMD>` | No | Command to execute if approved |
| `--on-rejected <CMD>` | No | Command to execute if rejected |

## Timeout Recommendations

| Operation Type | Recommended Timeout | Reason |
|----------------|---------------------|--------|
| hibernate/wake | 60 seconds | Low risk, quick decision |
| spawn | 120 seconds | Medium risk, may need review |
| install | 120 seconds | Medium risk |
| terminate | 180 seconds | High risk, careful review |
| replace | 300 seconds | High risk, complex decision |

## Examples

```bash
# Basic wait for approval
/ecos-wait-for-approval --request-id ECOS-20250202150000-a1b2c3d4

# Wait with custom timeout
/ecos-wait-for-approval --request-id ECOS-20250202150000-a1b2c3d4 --timeout 300

# Quiet mode for scripting
/ecos-wait-for-approval --request-id ECOS-20250202150000-a1b2c3d4 --quiet

# With conditional execution
/ecos-wait-for-approval --request-id ECOS-20250202150000-a1b2c3d4 \
  --on-approved "aimaestro-agent.sh delete helper-python --confirm" \
  --on-rejected "echo 'Termination denied by manager'"

# Fast polling for urgent requests
/ecos-wait-for-approval --request-id ECOS-20250202150000-a1b2c3d4 \
  --timeout 60 --poll-interval 2
```

## Output Format (Default)

```
=======================================================================
  WAITING FOR APPROVAL
=======================================================================

  Request ID: ECOS-20250202150000-a1b2c3d4
  Operation:  terminate
  Target:     helper-python

  Timeout:    120 seconds
  Polling:    Every 5 seconds

  [........] Waiting for EAMA response...
  [####....] 30s elapsed...
  [######..] 45s elapsed...
  [########] Response received!

=======================================================================
  APPROVAL DECISION: APPROVED
=======================================================================

  Decision:   APPROVED
  Decided at: 2025-02-02 15:02:30 UTC
  Wait time:  47 seconds

  Manager Notes:
  Proceed with termination. Ensure work is backed up first.

  Conditions:
  1. Verify no pending commits
  2. Export agent state before termination

=======================================================================
```

## Output Format (Quiet)

```
APPROVED
```

## Output Format (Timeout)

```
=======================================================================
  WAITING FOR APPROVAL - TIMEOUT
=======================================================================

  Request ID: ECOS-20250202150000-a1b2c3d4
  Operation:  terminate
  Target:     helper-python

  Status: TIMEOUT after 120 seconds

  The approval request did not receive a response within the timeout period.

  Options:
  1. Increase timeout: /ecos-wait-for-approval --request-id ECOS-... --timeout 300
  2. Check manually: /ecos-check-approval-status --request-id ECOS-...
  3. Contact manager: /ecos-notify-manager --subject "Approval pending"

=======================================================================
```

## Return Codes

| Code | Meaning | Action |
|------|---------|--------|
| 0 | Approved | Safe to proceed with operation |
| 1 | Rejected | Operation denied, do not proceed |
| 2 | Timeout | No response, check manually |
| 3 | Deferred | Needs more info, see notes |
| 4 | Error | Technical error during wait |
| 5 | Cancelled | Request was cancelled |

## Polling Strategy

The command uses intelligent polling:

```
Time 0s:    Check immediately
Time 5s:    First poll
Time 10s:   Second poll
...
Time N:     Continue until timeout or response
```

For long timeouts (>300s), polling interval automatically increases:
- 0-60s: Every 5 seconds
- 60-180s: Every 10 seconds
- 180s+: Every 30 seconds

## Integration Pattern

Typical workflow combining request and wait:

1. Submit approval request via `/ecos-request-approval`
2. Wait for response via `/ecos-wait-for-approval --request-id <ID>`
3. If approved, execute the operation (e.g., `/ecos-terminate-agent`)
4. If rejected, log the rejection and notify as appropriate

## Conditional Execution

When using `--on-approved` and `--on-rejected`, the command executes the appropriate action based on the decision:

- **On approved**: Use the `ai-maestro-agents-management` skill to execute the approved operation, then notify the manager of completion using the `agent-messaging` skill
- **On rejected**: Notify the manager that the operation was blocked using the `agent-messaging` skill

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Invalid request ID" | Malformed ID | Check ID format: ECOS-YYYYMMDDHHMMSS-XXXXXXXX |
| "Request not found" | Unknown ID | Verify request was submitted |
| "AI Maestro not responding" | API down | Check AI Maestro service |
| "Polling error" | Network issue | Retry with increased interval |
| "Request already processed" | Duplicate wait | Check previous response |

## Interruption Handling

If wait is interrupted (Ctrl+C):
- Current status is displayed
- Request remains pending
- Can resume with same command

## Best Practices

1. **Set appropriate timeouts** - Don't wait too long for low-risk operations
2. **Use quiet mode for scripts** - Easier to parse in automation
3. **Implement fallback** - Have a plan if approval times out
4. **Monitor progress** - Use default output for interactive sessions
5. **Combine with notification** - Alert manager if timeout is approaching

## Related Commands

- `/ecos-request-approval` - Submit approval request (prerequisite)
- `/ecos-check-approval-status` - Check status without waiting
- `/ecos-notify-manager` - Send follow-up notification
