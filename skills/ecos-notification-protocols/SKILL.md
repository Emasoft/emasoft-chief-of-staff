---
name: ecos-notification-protocols
description: Use when notifying agents about upcoming operations, requesting acknowledgments before proceeding, or sending failure notifications after operation errors. Trigger with notification or alert events.
license: Apache-2.0
compatibility: Requires access to AI Maestro messaging system and understanding of agent coordination protocols. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ecos-main
---

# Emasoft Chief of Staff - Notification Protocols Skill

## Overview

Notification protocols ensure agents are properly informed about operations that affect them. Before performing operations like skill installation, agent restart, or configuration changes, the Chief of Staff must notify affected agents, wait for acknowledgment, and then proceed. This skill teaches you how to send pre-operation notifications, handle acknowledgment workflows, and report failures.

## Prerequisites

Before using this skill, ensure:
1. AI Maestro messaging system is running
2. Target agents are registered and reachable
3. Notification templates are available

## Instructions

1. Identify the notification type needed
2. Select appropriate notification template
3. Send notification via AI Maestro
4. Verify delivery and acknowledgment

## Output

| Notification Type | Output |
|-------------------|--------|
| Status update | Notification sent, delivery confirmed |
| Alert | Alert sent, escalation tracked |
| Broadcast | Message sent to all agents, receipt logged |

## What Are Notification Protocols?

Notification protocols are the standardized communication patterns the Chief of Staff uses to coordinate with other agents during operations. The protocols ensure:

- **No surprise interruptions**: Agents know when operations will affect them
- **Graceful state preservation**: Agents have time to save work before operations
- **Acknowledgment tracking**: Operations proceed only when agents are ready
- **Failure transparency**: Agents are informed when operations fail

## Protocol Types

```
┌───────────────────────────────────────────────────────────────────┐
│                    NOTIFICATION PROTOCOLS                          │
├───────────────────┬───────────────────┬───────────────────────────┤
│  PRE-OPERATION    │  POST-OPERATION   │  FAILURE                   │
│  Notifications    │  Notifications    │  Notifications             │
├───────────────────┼───────────────────┼───────────────────────────┤
│  - Warn agents    │  - Confirm done   │  - Report failures         │
│  - Request ack    │  - Ask verify     │  - Provide diagnostics     │
│  - Wait for ok    │  - Resume work    │  - Suggest recovery        │
└───────────────────┴───────────────────┴───────────────────────────┘
```

**Protocol Flow:**
1. PRE-OPERATION -> Send warning, wait for acknowledgment
2. EXECUTE -> Perform the operation
3. POST-OPERATION or FAILURE -> Send confirmation or failure notification

## Core Procedures

### PROCEDURE 1: Pre-Operation Notification

**When to use:** Before skill installation, plugin installation, agent restart, configuration changes, or any operation that will interrupt an agent.

**Steps:** Identify affected agents, compose notification message, send via AI Maestro, track acknowledgments, handle timeouts.

**Related documentation:**

#### Pre-Operation Notifications ([references/pre-operation-notifications.md](references/pre-operation-notifications.md))
- 1.1 What are pre-operation notifications - Understanding warning messages
- 1.2 When to send pre-operation notifications - Notification triggers
  - 1.2.1 Skill installation - Agent will be hibernated and woken
  - 1.2.2 Plugin installation - Agent restart required
  - 1.2.3 Configuration changes - Settings will change
  - 1.2.4 System maintenance - Temporary disruption expected
- 1.3 Pre-operation notification procedure - Step-by-step process
  - 1.3.1 Identify affected agents - Who needs to know
  - 1.3.2 Compose notification - What to tell them
  - 1.3.3 Send notification - Using AI Maestro API
  - 1.3.4 Track acknowledgments - Monitor responses
  - 1.3.5 Handle timeouts - When agents don't respond
- 1.4 Notification message format - Standard message structure
- 1.5 Priority levels - When to use each priority
- 1.6 Examples - Pre-operation scenarios
- 1.7 Troubleshooting - Notification delivery issues

### PROCEDURE 2: Post-Operation Notification

**When to use:** After skill installation completes, after agent restart, after configuration changes apply, or after any operation that affected an agent.

**Steps:** Confirm operation completed, compose success message, send confirmation, request verification, log outcome.

**Related documentation:**

#### Post-Operation Notifications ([references/post-operation-notifications.md](references/post-operation-notifications.md))
- 2.1 What are post-operation notifications - Understanding confirmation messages
- 2.2 When to send post-operation notifications - Confirmation triggers
  - 2.2.1 Skill installation complete - Skill is now active
  - 2.2.2 Agent restart complete - Agent is back online
  - 2.2.3 Configuration applied - Settings now active
  - 2.2.4 Maintenance complete - Normal operations resume
- 2.3 Post-operation notification procedure - Step-by-step process
  - 2.3.1 Confirm operation success - Verify completion
  - 2.3.2 Compose confirmation - What to tell agents
  - 2.3.3 Send notification - Using AI Maestro API
  - 2.3.4 Request verification - Ask agent to confirm
  - 2.3.5 Log outcome - Record the result
- 2.4 Verification request format - Asking agents to confirm
- 2.5 Examples - Post-operation scenarios
- 2.6 Troubleshooting - Verification issues

### PROCEDURE 3: Acknowledgment Protocol

**When to use:** When you need agent confirmation before proceeding, when operations require agent readiness, or when coordinating multi-agent operations.

**Steps:** Send acknowledgment request, start timeout timer, send reminders, process response, proceed or handle timeout.

**Related documentation:**

#### Acknowledgment Protocol ([references/acknowledgment-protocol.md](references/acknowledgment-protocol.md))
- 3.1 What is the acknowledgment protocol - Understanding coordination
- 3.2 When to require acknowledgments - Acknowledgment triggers
  - 3.2.1 Disruptive operations - Agent will be interrupted
  - 3.2.2 State-changing operations - Agent context affected
  - 3.2.3 Multi-agent coordination - Synchronized actions needed
- 3.3 Acknowledgment procedure - Step-by-step process
  - 3.3.1 Send acknowledgment request - Ask for "ok"
  - 3.3.2 Start timeout timer - See standardized timeouts below
  - 3.3.3 Send reminders - At 15s, 30s, 45s intervals for pre-operation ACK
  - 3.3.4 Process response - Handle "ok" or other responses
  - 3.3.5 Proceed or timeout - Continue or handle no response
- 3.4 Acknowledgment message format - Standard request structure
- 3.5 Reminder message format - Standard reminder structure
- 3.6 Response handling - What agents can send back
- 3.7 Timeout behavior - What happens without response
- 3.8 Examples - Acknowledgment scenarios
- 3.9 Troubleshooting - Acknowledgment issues

### Standardized ACK Timeout Policy

**CRITICAL:** All ECOS components MUST use these standardized timeout values:

| ACK Type | Timeout | Reminders | Use Case |
|----------|---------|-----------|----------|
| Pre-operation ACK | **60 seconds** | 15s, 30s, 45s | Before disruptive operations (hibernate, restart, etc.) |
| Approval request | **2 minutes** | 60s, 90s | Requesting manager approval for operations |
| Emergency handoff ACK | **30 seconds** | 10s, 20s | Time-critical emergency situations |
| Health check response | **30 seconds** | None | Verifying agent is alive |

**Important:** These timeouts are SEQUENTIAL, not parallel. Total wait time calculation:

```
Example: Skill installation with approval

1. Pre-operation ACK request to agent    → Wait up to 60 seconds
2. Approval request to EAMA              → Wait up to 2 minutes
3. Post-operation verification           → Wait up to 30 seconds
                                           ─────────────────────
Total maximum wait time                  = 3 minutes 30 seconds
```

**Timeout behavior:**
- Pre-operation ACK timeout: Send final notice, then proceed with operation
- Approval request timeout: Log timeout, proceed if autonomous mode enabled, otherwise abort
- Emergency handoff ACK timeout: Proceed immediately (cannot wait in emergencies)

### PROCEDURE 4: Failure Notification

**When to use:** When skill installation fails, when agent restart fails, when configuration change fails, or when any operation error occurs.

**Steps:** Capture error details, compose failure message, send to affected agents, provide recovery guidance, log failure.

**Related documentation:**

#### Failure Notifications ([references/failure-notifications.md](references/failure-notifications.md))
- 4.1 What are failure notifications - Understanding error messages
- 4.2 When to send failure notifications - Failure triggers
  - 4.2.1 Installation failures - Skill or plugin not installed
  - 4.2.2 Restart failures - Agent did not come back online
  - 4.2.3 Configuration failures - Settings not applied
  - 4.2.4 Timeout failures - Operation did not complete in time
- 4.3 Failure notification procedure - Step-by-step process
  - 4.3.1 Capture error details - What went wrong
  - 4.3.2 Compose failure message - What to tell agents
  - 4.3.3 Send notification - Using AI Maestro API
  - 4.3.4 Provide recovery guidance - How to proceed
  - 4.3.5 Log failure - Record for analysis
- 4.4 Failure message format - Standard error structure
- 4.5 Error severity levels - Critical, error, warning
- 4.6 Recovery guidance patterns - Common recovery steps
- 4.7 Examples - Failure scenarios
- 4.8 Troubleshooting - Notification delivery during failures

## Task Checklist

Copy this checklist and track your progress:

- [ ] Understand the four notification protocol types
- [ ] Learn PROCEDURE 1: Pre-operation notification
- [ ] Learn PROCEDURE 2: Post-operation notification
- [ ] Learn PROCEDURE 3: Acknowledgment protocol
- [ ] Learn PROCEDURE 4: Failure notification
- [ ] Practice sending pre-operation notification with acknowledgment
- [ ] Practice sending post-operation confirmation
- [ ] Practice handling acknowledgment timeout
- [ ] Practice sending failure notification
- [ ] Verify message delivery via AI Maestro

## Examples

### Example 1: Skill Installation Notification Flow (Complete)

This example shows the full notification flow for installing a skill on an agent.

**Step 1: Send Pre-Operation Notification**

```bash
# Notify agent about upcoming skill installation
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "code-impl-auth",
    "subject": "Skill Installation Pending",
    "priority": "high",
    "content": {
      "type": "pre-operation",
      "message": "I will install the security-audit skill on your agent. This requires hibernating and waking you. Please finish your current work and reply with \"ok\" when ready. I will wait up to 2 minutes.",
      "operation": "skill-install",
      "skill_name": "security-audit",
      "expected_downtime": "30 seconds",
      "requires_acknowledgment": true
    }
  }'
```

**Step 2: Wait for Acknowledgment (with reminders)**

```bash
# Check for agent response
curl -s "http://localhost:23000/api/messages?agent=chief-of-staff&action=list&status=unread" | jq '.messages[] | select(.from == "code-impl-auth")'

# If no response after 30 seconds, send reminder
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "code-impl-auth",
    "subject": "Reminder: Skill Installation Pending",
    "priority": "high",
    "content": {
      "type": "reminder",
      "message": "Reminder: Please reply \"ok\" when ready for skill installation. 90 seconds remaining.",
      "original_subject": "Skill Installation Pending",
      "time_remaining": "90 seconds"
    }
  }'
```

**Step 3: Receive Acknowledgment**

```json
{
  "from": "code-impl-auth",
  "to": "chief-of-staff",
  "subject": "RE: Skill Installation Pending",
  "content": {
    "type": "acknowledgment",
    "message": "ok",
    "ready": true
  }
}
```

**Step 4: Perform Installation**

```bash
# Hibernate agent, install skill, wake agent
aimaestro-agent.sh hibernate code-impl-auth
# ... install skill ...
aimaestro-agent.sh wake code-impl-auth
```

**Step 5: Send Post-Operation Notification**

```bash
# Notify agent that installation is complete
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "code-impl-auth",
    "subject": "Skill Installation Complete",
    "priority": "normal",
    "content": {
      "type": "post-operation",
      "message": "The security-audit skill has been installed. Please verify the skill is active by checking your available skills. Reply with confirmation.",
      "operation": "skill-install",
      "skill_name": "security-audit",
      "status": "success",
      "verification_requested": true
    }
  }'
```

### Example 2: Handling Acknowledgment Timeout

```bash
# After 2 minutes with no response, proceed anyway
echo "[$(date)] WARNING: No acknowledgment from code-impl-auth after 2 minutes. Proceeding with skill installation."

# Send final notice
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "code-impl-auth",
    "subject": "Proceeding Without Acknowledgment",
    "priority": "high",
    "content": {
      "type": "timeout-notice",
      "message": "No response received after 2 minutes. Proceeding with skill installation now. You will be hibernated and woken shortly.",
      "operation": "skill-install",
      "timeout_occurred": true
    }
  }'

# Proceed with installation
aimaestro-agent.sh hibernate code-impl-auth
```

### Example 3: Failure Notification

```bash
# Skill installation failed - notify agent
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "code-impl-auth",
    "subject": "Skill Installation Failed",
    "priority": "high",
    "content": {
      "type": "failure",
      "message": "Failed to install security-audit skill. Error: Skill validation failed - missing required SKILL.md file. You can continue your previous work. I will retry installation after fixing the skill package.",
      "operation": "skill-install",
      "skill_name": "security-audit",
      "status": "failed",
      "error_code": "SKILL_VALIDATION_FAILED",
      "error_details": "Missing required SKILL.md file",
      "recovery_action": "Skill package will be fixed and installation retried"
    }
  }'
```

### Example 4: Broadcast Notification to Multiple Agents

```bash
# Define target agents
AGENTS=("code-impl-auth" "test-engineer-01" "docs-writer")

# Send broadcast notification about system maintenance
for agent in "${AGENTS[@]}"; do
  curl -X POST "http://localhost:23000/api/messages" \
    -H "Content-Type: application/json" \
    -d "{
      \"to\": \"$agent\",
      \"subject\": \"System Maintenance in 5 Minutes\",
      \"priority\": \"high\",
      \"content\": {
        \"type\": \"broadcast\",
        \"message\": \"System maintenance will begin in 5 minutes. All agents will be hibernated. Please save your work and reply with 'ok' when ready.\",
        \"operation\": \"system-maintenance\",
        \"broadcast_id\": \"maint-$(date +%Y%m%d%H%M%S)\",
        \"total_recipients\": ${#AGENTS[@]},
        \"requires_acknowledgment\": true
      }
    }"
done
```

## Error Handling

### Issue: Notification not delivered

**Symptoms:** Agent does not receive message, no response observed.

See [references/pre-operation-notifications.md](references/pre-operation-notifications.md) Section 1.7 Troubleshooting for resolution.

### Issue: Acknowledgment timeout

**Symptoms:** Agent does not respond within 2 minutes.

See [references/acknowledgment-protocol.md](references/acknowledgment-protocol.md) Section 3.9 Troubleshooting for resolution.

### Issue: Agent sends unexpected response

**Symptoms:** Agent responds with something other than "ok".

See [references/acknowledgment-protocol.md](references/acknowledgment-protocol.md) Section 3.6 Response handling for resolution.

### Issue: Failure notification not received

**Symptoms:** Agent unaware of operation failure.

See [references/failure-notifications.md](references/failure-notifications.md) Section 4.8 Troubleshooting for resolution.

## Key Takeaways

1. **Always notify before disruptive operations** - Never surprise agents with interruptions
2. **Use acknowledgment protocol for critical operations** - Wait for "ok" before proceeding
3. **Send reminders at 30s, 60s, 90s** - Give agents multiple chances to respond
4. **Proceed after 2 minute timeout** - Do not wait indefinitely
5. **Log timeout occurrences** - Track agents that did not respond
6. **Send post-operation confirmations** - Let agents verify success
7. **Request verification after installation** - Ask agents to confirm skill is active
8. **Provide recovery guidance in failures** - Tell agents what happens next

## Message Type Quick Reference

| Message Type | When to Use | Requires Ack |
|--------------|-------------|--------------|
| `pre-operation` | Before any disruptive operation | Yes |
| `post-operation` | After successful operation | Optional |
| `reminder` | When awaiting acknowledgment | No |
| `timeout-notice` | When proceeding without ack | No |
| `failure` | When operation fails | No |
| `broadcast` | Notifying multiple agents | Yes |
| `acknowledgment` | Agent responding with "ok" | No |

## Next Steps

### 1. Read Pre-Operation Notifications
See [references/pre-operation-notifications.md](references/pre-operation-notifications.md) for complete pre-operation documentation.

### 2. Read Post-Operation Notifications
See [references/post-operation-notifications.md](references/post-operation-notifications.md) for confirmation procedures.

### 3. Read Acknowledgment Protocol
See [references/acknowledgment-protocol.md](references/acknowledgment-protocol.md) for detailed acknowledgment handling.

### 4. Read Failure Notifications
See [references/failure-notifications.md](references/failure-notifications.md) for error notification procedures.

---

## Resources

- [Pre-Operation Notifications](references/pre-operation-notifications.md)
- [Post-Operation Notifications](references/post-operation-notifications.md)
- [Acknowledgment Protocol](references/acknowledgment-protocol.md)
- [Failure Notifications](references/failure-notifications.md)

---

**Version:** 1.0
**Last Updated:** 2025-02-02
**Target Audience:** Chief of Staff Agents
**Difficulty Level:** Intermediate
