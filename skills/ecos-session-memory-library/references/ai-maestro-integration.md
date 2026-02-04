# AI Maestro Integration Reference

## Table of Contents

- 1.1 [What Is AI Maestro](#11-what-is-ai-maestro)
- 1.2 [Core API Endpoints](#12-core-api-endpoints)
- 1.3 [Session Management](#13-session-management)
- 1.4 [Message Operations](#14-message-operations)
- 1.5 [Broadcast Operations](#15-broadcast-operations)
- 1.6 [Health and Status](#16-health-and-status)
- 1.7 [Integration Examples](#17-integration-examples)
- 1.8 [Troubleshooting](#18-troubleshooting)

---

## 1.1 What Is AI Maestro

AI Maestro is an inter-agent messaging system that enables Claude Code sessions to communicate with each other. It provides a REST API for sending messages, querying sessions, and coordinating multi-agent workflows.

**Core capabilities:**
- Message routing between named sessions
- Session registry and status tracking
- Broadcast messaging to all agents
- Message priority handling
- Delivery confirmation

**Architecture:**
- Runs as a local service (default port 23000)
- REST API for all operations
- Session identification by name
- Message queuing with persistence

**Base URL:**
```
http://localhost:23000
```

**Environment variable:**
```bash
AIMAESTRO_API=http://localhost:23000
```

---

## 1.2 Core API Endpoints

### Session Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/sessions` | List all registered sessions |
| GET | `/api/sessions/{name}` | Get specific session details |
| POST | `/api/sessions` | Register a new session |
| DELETE | `/api/sessions/{name}` | Unregister a session |

### Message Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/messages` | List messages (with filters) |
| POST | `/api/messages` | Send a new message |
| GET | `/api/messages/{id}` | Get specific message |
| PUT | `/api/messages/{id}/read` | Mark message as read |
| DELETE | `/api/messages/{id}` | Delete a message |

### Broadcast Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/messages/broadcast` | Send to all sessions |

### Utility Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/api/stats` | Service statistics |

---

## 1.3 Session Management

### Listing Sessions

```bash
# Get all registered sessions
curl -s "http://localhost:23000/api/sessions" | jq '.'

# Response format
{
  "sessions": [
    {
      "name": "orchestrator-master",
      "status": "active",
      "lastSeen": "2025-02-01T10:00:00Z",
      "metadata": {}
    }
  ]
}
```

### Getting Session Details

```bash
# Get specific session
curl -s "http://localhost:23000/api/sessions/helper-agent-generic" | jq '.'

# Response format
{
  "name": "helper-agent-generic",
  "status": "active",
  "lastSeen": "2025-02-01T10:00:00Z",
  "metadata": {
    "role": "Developer"
  }
}
```

### Session Status Values

| Status | Meaning |
|--------|---------|
| `active` | Session is running and responsive |
| `idle` | Session is running but not actively working |
| `busy` | Session is processing a task |
| `offline` | Session is not running |

### Checking Session Existence

```bash
# Check if session exists
curl -s -o /dev/null -w "%{http_code}" "http://localhost:23000/api/sessions/helper-agent-generic"
# Returns 200 if exists, 404 if not
```

---

## 1.4 Message Operations

### Sending a Message

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "helper-agent-generic",
    "subject": "Task Assignment",
    "priority": "high",
    "content": {
      "type": "request",
      "message": "Please review PR #123"
    }
  }'
```

### Message Fields

| Field | Required | Description |
|-------|----------|-------------|
| `to` | Yes | Recipient session name |
| `subject` | Yes | Message subject line |
| `priority` | No | "urgent", "high", "normal" (default) |
| `content` | Yes | Message body (object) |

### Content Object Format

```json
{
  "type": "request|announcement|alert|status-update|role-assignment",
  "message": "The message text",
  "additional_field": "Optional additional data"
}
```

### Listing Messages

```bash
# List all messages for an agent
curl -s "http://localhost:23000/api/messages?agent=helper-agent-generic" | jq '.'

# List unread messages only
curl -s "http://localhost:23000/api/messages?agent=helper-agent-generic&status=unread" | jq '.'

# List messages since a time
curl -s "http://localhost:23000/api/messages?agent=helper-agent-generic&since=1h" | jq '.'
```

### Query Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `agent` | Filter by recipient | `agent=helper-agent-generic` |
| `status` | Filter by status | `status=unread` |
| `since` | Time filter | `since=1h`, `since=24h` |
| `from` | Filter by sender | `from=orchestrator-master` |
| `priority` | Filter by priority | `priority=urgent` |

### Marking as Read

```bash
curl -X PUT "http://localhost:23000/api/messages/{message_id}/read"
```

### Checking Unread Count

```bash
curl -s "http://localhost:23000/api/messages?agent=helper-agent-generic&action=unread-count" | jq '.count'
```

---

## 1.5 Broadcast Operations

### Sending Broadcast

```bash
curl -X POST "http://localhost:23000/api/messages/broadcast" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Team Announcement",
    "priority": "normal",
    "content": {
      "type": "announcement",
      "message": "Sprint planning complete. Check inbox for assignments."
    }
  }'
```

### Broadcast Fields

| Field | Required | Description |
|-------|----------|-------------|
| `subject` | Yes | Message subject |
| `priority` | No | Priority level |
| `content` | Yes | Message body |

Note: Broadcasts do not have a `to` field - they go to all active sessions.

### Broadcast Best Practices

- Use sparingly to avoid notification fatigue
- Keep broadcasts short and informative
- Use normal priority unless truly urgent
- Include clear action items if any required

---

## 1.6 Health and Status

### Health Check

```bash
curl -s "http://localhost:23000/health"

# Response
{"status": "healthy"}
```

### Service Statistics

```bash
curl -s "http://localhost:23000/api/stats" | jq '.'

# Response format
{
  "sessions": {
    "total": 8,
    "active": 6,
    "idle": 2
  },
  "messages": {
    "total": 1234,
    "pending": 12,
    "delivered": 1222
  },
  "uptime": "4h32m"
}
```

### Checking AI Maestro Availability

```bash
#!/bin/bash
# check-aimaestro.sh

if curl -s "http://localhost:23000/health" > /dev/null 2>&1; then
  echo "AI Maestro is running"
else
  echo "AI Maestro is NOT available"
  exit 1
fi
```

---

## 1.7 Integration Examples

### Example: Send and Confirm Delivery

```bash
#!/bin/bash
# send-with-confirmation.sh

# Send message
RESPONSE=$(curl -s -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "helper-agent-generic",
    "subject": "Task Assignment",
    "priority": "high",
    "content": {"type": "request", "message": "Review PR #123"}
  }')

# Extract message ID
MSG_ID=$(echo $RESPONSE | jq -r '.id')
echo "Message sent: $MSG_ID"

# Wait and check delivery
sleep 5
STATUS=$(curl -s "http://localhost:23000/api/messages/$MSG_ID" | jq -r '.delivered')
echo "Delivered: $STATUS"
```

### Example: Poll for Unread Messages

```bash
#!/bin/bash
# poll-inbox.sh

AGENT="helper-agent-generic"

while true; do
  UNREAD=$(curl -s "http://localhost:23000/api/messages?agent=$AGENT&status=unread" | jq '.messages | length')

  if [ "$UNREAD" -gt 0 ]; then
    echo "You have $UNREAD unread messages"
    # Process messages here
  fi

  sleep 30
done
```

### Example: Team Status Query

```bash
#!/bin/bash
# team-status.sh

echo "=== Team Status ==="

SESSIONS=$(curl -s "http://localhost:23000/api/sessions" | jq -r '.sessions[].name')

for session in $SESSIONS; do
  STATUS=$(curl -s "http://localhost:23000/api/sessions/$session" | jq -r '.status')
  LAST=$(curl -s "http://localhost:23000/api/sessions/$session" | jq -r '.lastSeen')
  echo "$session: $STATUS (last seen: $LAST)"
done
```

### Example: Error Handling in API Calls

```bash
#!/bin/bash
# robust-send.sh

send_message() {
  local to=$1
  local subject=$2
  local message=$3
  local retries=3

  for i in $(seq 1 $retries); do
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "http://localhost:23000/api/messages" \
      -H "Content-Type: application/json" \
      -d "{\"to\": \"$to\", \"subject\": \"$subject\", \"content\": {\"type\": \"request\", \"message\": \"$message\"}}")

    HTTP_CODE=$(echo "$RESPONSE" | tail -1)
    BODY=$(echo "$RESPONSE" | head -1)

    if [ "$HTTP_CODE" -eq 200 ] || [ "$HTTP_CODE" -eq 201 ]; then
      echo "Message sent successfully"
      return 0
    else
      echo "Attempt $i failed (HTTP $HTTP_CODE), retrying..."
      sleep 2
    fi
  done

  echo "Failed to send message after $retries attempts"
  return 1
}

send_message "helper-agent-generic" "Test" "This is a test message"
```

---

## 1.8 Troubleshooting

### Issue: AI Maestro not responding

**Symptoms:** Connection refused, timeout errors.

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
2. Check if recipient is registered: `curl .../api/sessions`
3. Check message status: `curl .../api/messages/{id}`
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

### Issue: High latency on API calls

**Symptoms:** API calls take several seconds.

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
