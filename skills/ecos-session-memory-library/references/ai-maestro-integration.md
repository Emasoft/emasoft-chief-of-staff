# AI Maestro Integration Reference

## Table of Contents

- 1.1 [What Is AI Maestro](#11-what-is-ai-maestro)
- 1.2 [Core Capabilities](#12-core-capabilities)
- 1.3 [Session Management](#13-session-management)
- 1.4 [Message Operations](#14-message-operations)
- 1.5 [Broadcast Operations](#15-broadcast-operations)
- 1.6 [Health and Status](#16-health-and-status)
- 1.7 [Integration Examples](#17-integration-examples)
- 1.8 [Troubleshooting](#18-troubleshooting)

---

## 1.1 What Is AI Maestro

AI Maestro is an inter-agent messaging system that enables Claude Code sessions to communicate with each other. It provides capabilities for sending messages, querying sessions, and coordinating multi-agent workflows.

**Core capabilities:**
- Message routing between named sessions
- Session registry and status tracking
- Broadcast messaging to all agents
- Message priority handling
- Delivery confirmation

**Architecture:**
- Runs as a local service
- Session identification by name
- Message queuing with persistence

---

## 1.2 Core Capabilities

All messaging operations are performed using the `agent-messaging` skill. All agent management operations are performed using the `ai-maestro-agents-management` skill.

### Session Operations

| Operation | Description | Skill |
|-----------|-------------|-------|
| List sessions | List all registered sessions | `ai-maestro-agents-management` |
| Get session details | Get specific session details | `ai-maestro-agents-management` |
| Check session existence | Verify if a session is registered | `ai-maestro-agents-management` |

### Message Operations

| Operation | Description | Skill |
|-----------|-------------|-------|
| Send message | Send a message to a recipient | `agent-messaging` |
| List messages | List messages with filters | `agent-messaging` |
| Check unread count | Count unread messages | `agent-messaging` |
| Mark as read | Mark a message as read | `agent-messaging` |
| Broadcast | Send to all sessions | `agent-messaging` |

### Utility Operations

| Operation | Description | Skill |
|-----------|-------------|-------|
| Health check | Verify AI Maestro is running | `ai-maestro-agents-management` |
| Service statistics | Get session and message counts | `ai-maestro-agents-management` |

---

## 1.3 Session Management

### Listing Sessions

Use the `ai-maestro-agents-management` skill to list all registered sessions. Each session includes:
- Session name
- Status (active, idle, busy, offline)
- Last seen timestamp
- Optional metadata

### Getting Session Details

Use the `ai-maestro-agents-management` skill to get details for a specific session by name.

### Session Status Values

| Status | Meaning |
|--------|---------|
| `active` | Session is running and responsive |
| `idle` | Session is running but not actively working |
| `busy` | Session is processing a task |
| `offline` | Session is not running |

### Checking Session Existence

Use the `ai-maestro-agents-management` skill to check if a specific session exists. The response indicates whether the session is registered.

---

## 1.4 Message Operations

### Sending a Message

Use the `agent-messaging` skill to send a message:
- **Recipient**: the target session name
- **Subject**: descriptive subject line
- **Priority**: `urgent`, `high`, or `normal` (default)
- **Content**: structured message with type and body

### Message Fields

| Field | Required | Description |
|-------|----------|-------------|
| Recipient | Yes | Target session name |
| Subject | Yes | Message subject line |
| Priority | No | "urgent", "high", "normal" (default) |
| Content | Yes | Message body (structured object) |

### Content Object Format

The content must include:
- **type**: category of message (e.g., `request`, `announcement`, `alert`, `status-update`, `role-assignment`)
- **message**: the actual message text
- Any additional fields as needed

### Listing Messages

Use the `agent-messaging` skill to list messages, with optional filters:
- Filter by status (unread, read, all)
- Filter by sender
- Filter by time window (e.g., last hour, last 24 hours)
- Filter by priority

### Marking as Read

Use the `agent-messaging` skill to mark a specific message as read (by message ID).

### Checking Unread Count

Use the `agent-messaging` skill to check the number of unread messages for a specific agent.

---

## 1.5 Broadcast Operations

### Sending Broadcast

Use the `agent-messaging` skill to broadcast a message to all active sessions:
- **Subject**: message subject
- **Priority**: priority level
- **Content**: structured message body

Note: Broadcasts go to all active sessions (no specific recipient).

### Broadcast Best Practices

- Use sparingly to avoid notification fatigue
- Keep broadcasts short and informative
- Use normal priority unless truly urgent
- Include clear action items if any required

---

## 1.6 Health and Status

### Health Check

Use the `ai-maestro-agents-management` skill to check if AI Maestro is running and healthy.

### Service Statistics

Use the `ai-maestro-agents-management` skill to get service statistics including:
- Total, active, and idle session counts
- Total, pending, and delivered message counts
- Service uptime

### Checking AI Maestro Availability

Before performing messaging operations, verify AI Maestro is available using the health check operation. If unavailable, fall back to file-based communication.

---

## 1.7 Integration Examples

### Example: Send and Confirm Delivery

1. Use the `agent-messaging` skill to send a message to the target agent
2. Note the message ID from the response
3. After a brief wait, use the `agent-messaging` skill to check the message status by ID
4. Confirm delivery

### Example: Poll for Unread Messages

Periodically use the `agent-messaging` skill to check for unread messages:
1. Query unread messages for your agent name
2. If unread messages exist, process them
3. Mark processed messages as read
4. Repeat at the configured polling interval

### Example: Team Status Query

1. Use the `ai-maestro-agents-management` skill to list all sessions
2. For each session, note the name, status, and last seen timestamp
3. Report the team status summary

### Example: Error Handling in Messaging

When sending messages, implement retry logic:
1. Attempt to send the message using the `agent-messaging` skill
2. If delivery fails, wait briefly and retry (up to 3 attempts)
3. If all retries fail, log the failure and escalate

---

## 1.8 Troubleshooting

### Issue: AI Maestro not responding

**Symptoms:** Connection failures, timeout errors.

**Possible causes:**
- Service not running
- Wrong port
- Network issue

**Resolution:**
1. Check if service is running: `lsof -i :23000`
2. Verify port configuration
3. Check service logs
4. Restart AI Maestro if needed

### Issue: Messages not delivered

**Symptoms:** Messages sent but recipient never receives.

**Possible causes:**
- Recipient session name incorrect
- Recipient not registered
- Message queue full

**Resolution:**
1. Verify recipient session name (case-sensitive)
2. Use the `ai-maestro-agents-management` skill to check if recipient is registered
3. Use the `agent-messaging` skill to check message status
4. Review AI Maestro logs

### Issue: Session shows offline but agent is running

**Symptoms:** Session status is "offline" despite agent running.

**Possible causes:**
- Session not registered
- Heartbeat not sent
- Registration expired

**Resolution:**
1. Re-register the session
2. Verify registration hook is running
3. Check heartbeat configuration
4. Review session registration logs

### Issue: High latency on messaging

**Symptoms:** Message operations take several seconds.

**Possible causes:**
- Service overloaded
- Network congestion
- Large message queue

**Resolution:**
1. Check service stats for queue size
2. Reduce message frequency
3. Increase service resources
4. Implement request batching

### Issue: Duplicate messages received

**Symptoms:** Same message appears multiple times.

**Possible causes:**
- Retry logic sending duplicates
- Message ID not being tracked
- Consumer not marking as read

**Resolution:**
1. Track processed message IDs
2. Mark messages as read after processing
3. Review retry logic
4. Check for duplicate sends

---

**Version:** 1.0
**Last Updated:** 2025-02-01
