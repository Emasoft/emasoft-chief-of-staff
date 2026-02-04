# Team Messaging Reference

## Table of Contents

- 2.1 [Team Message Types](#21-team-message-types)
- 2.2 [Message Priority Levels](#22-message-priority-levels)
- 2.3 [Sending Broadcast Messages](#23-sending-broadcast-messages)
- 2.4 [Sending Targeted Messages](#24-sending-targeted-messages)
- 2.5 [Message Routing Rules](#25-message-routing-rules)
- 2.6 [Confirming Message Delivery](#26-confirming-message-delivery)
- 2.7 [Team Messaging Examples](#27-team-messaging-examples)
- 2.8 [Troubleshooting](#28-troubleshooting)

---

## 2.1 Team Message Types

Team messages are categorized by their purpose and expected response:

### Announcement
One-way communication to inform the team. No response expected.

**Use cases:**
- Sprint planning complete
- New team member joined
- Policy or process changes
- Milestone reached

**Content format:**
```json
{
  "type": "announcement",
  "message": "Brief description of the announcement"
}
```

### Request
Two-way communication requesting action or information. Response expected.

**Use cases:**
- Task assignment
- Status request
- Information query
- Assistance request

**Content format:**
```json
{
  "type": "request",
  "message": "Description of what is needed",
  "deadline": "ISO timestamp (optional)"
}
```

### Alert
Urgent notification requiring immediate attention.

**Use cases:**
- Critical bug discovered
- System failure
- Security issue
- Blocking dependency

**Content format:**
```json
{
  "type": "alert",
  "severity": "critical|high|medium",
  "message": "Description of the alert"
}
```

### Status Update
Progress report from an agent about their current work.

**Use cases:**
- Task completion
- Task progress
- Blocker encountered
- Milestone update

**Content format:**
```json
{
  "type": "status-update",
  "task": "Task identifier",
  "status": "completed|in-progress|blocked|failed",
  "message": "Details about the status"
}
```

### Role Assignment
Special message type for assigning or modifying agent roles.

**Use cases:**
- New role assignment
- Role transition
- Role removal

**Content format:**
```json
{
  "type": "role-assignment",
  "role": "Role name",
  "message": "Responsibilities and expectations"
}
```

---

## 2.2 Message Priority Levels

AI Maestro supports three priority levels that affect delivery and processing:

### URGENT Priority

**When to use:**
- Critical blockers affecting multiple agents
- Security incidents
- System failures
- Deadlines at risk

**Behavior:**
- Delivered immediately
- Triggers notification banner in recipient session
- Recipient should stop current work to read

**Example:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "URGENT: Production deployment failed",
    "priority": "urgent",
    "content": {"type": "alert", "severity": "critical", "message": "Deployment rollback required immediately"}
  }'
```

### HIGH Priority

**When to use:**
- Important updates requiring prompt attention
- Task assignments with near-term deadlines
- Role assignments
- Blocking issues for single agent

**Behavior:**
- Delivered promptly
- Visible in inbox summary
- Recipient should read within current work cycle

**Example:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "helper-agent-generic",
    "subject": "High Priority Task Assignment",
    "priority": "high",
    "content": {"type": "request", "message": "Review PR #123 before end of day"}
  }'
```

### NORMAL Priority

**When to use:**
- Routine updates and announcements
- Non-urgent requests
- FYI messages
- Status reports

**Behavior:**
- Delivered in normal queue
- Processed when recipient checks inbox
- No interruption expected

**Example:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "team",
    "subject": "Weekly Status Meeting Notes",
    "priority": "normal",
    "content": {"type": "announcement", "message": "Meeting notes attached. No action required."}
  }'
```

---

## 2.3 Sending Broadcast Messages

Broadcast messages are sent to all active team members simultaneously.

### Broadcast Procedure

**Step 1: Compose the message**

Ensure the message is relevant to all recipients. Avoid broadcasting messages that only concern a subset of the team.

**Step 2: Set appropriate priority**

Most broadcasts should be NORMAL priority. Use HIGH only for time-sensitive team-wide updates. URGENT broadcasts should be rare.

**Step 3: Send via broadcast endpoint**

```bash
curl -X POST "http://localhost:23000/api/messages/broadcast" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Message subject",
    "priority": "normal",
    "content": {
      "type": "announcement",
      "message": "Message content"
    }
  }'
```

**Step 4: Log the broadcast**

Record the broadcast in coordination state for audit purposes.

### Broadcast Best Practices

- **Be concise**: Everyone receives the message; respect their context
- **Be clear**: State the purpose upfront
- **Include action items**: If action is needed, make it explicit
- **Avoid overuse**: Too many broadcasts cause notification fatigue

---

## 2.4 Sending Targeted Messages

Targeted messages are sent to specific agents.

### Single Recipient

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "helper-agent-generic",
    "subject": "Message subject",
    "priority": "normal",
    "content": {
      "type": "request",
      "message": "Message content"
    }
  }'
```

### Multiple Specific Recipients

Send separate messages to each recipient (AI Maestro does not support multi-recipient in single call):

```bash
# First recipient
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{"to": "agent-one", "subject": "Subject", "priority": "normal", "content": {"type": "request", "message": "Content"}}'

# Second recipient
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{"to": "agent-two", "subject": "Subject", "priority": "normal", "content": {"type": "request", "message": "Content"}}'
```

### Role-Based Targeting

To send to all agents with a specific role, query the team roster first, then send to each matching agent:

```bash
# Query roster for Code Reviewers (pseudo-code)
reviewers=$(get_agents_with_role "Code Reviewer")

# Send to each reviewer
for reviewer in $reviewers; do
  send_message "$reviewer" "subject" "content"
done
```

---

## 2.5 Message Routing Rules

The Chief of Staff follows these routing rules to determine message recipients:

### Task-Related Messages

| Message About | Route To |
|--------------|----------|
| Feature implementation | Developer assigned to feature |
| Code review request | Code Reviewer role |
| Test results | Test Engineer who ran tests |
| Deployment issue | DevOps role |
| Documentation update | Documentation Writer role |

### Status-Related Messages

| Message About | Route To |
|--------------|----------|
| Task completion | Orchestrator + dependent agents |
| Blocker encountered | Orchestrator + Chief of Staff |
| Milestone reached | Broadcast to team |
| Role change | Affected agent + team |

### Escalation Messages

| Escalation Level | Route To |
|-----------------|----------|
| Within role | Senior member of same role |
| Cross-role | Orchestrator |
| Orchestrator unable | Chief of Staff |
| Chief of Staff unable | User |

---

## 2.6 Confirming Message Delivery

### Checking Delivery Status

After sending a message, verify delivery:

```bash
# Get sent message status
curl -s "http://localhost:23000/api/messages?status=sent" | jq '.messages[] | {id: .id, to: .to, delivered: .delivered}'
```

### Read Receipts

Check if recipient has read the message:

```bash
# Check read status
curl -s "http://localhost:23000/api/messages/MESSAGE_ID/status" | jq '.read'
```

### Handling Undelivered Messages

If a message is not delivered within expected timeframe:

1. Check recipient session status
2. If session inactive, queue message for when agent returns
3. If critical, attempt alternative routing or escalate
4. Log delivery failure in coordination state

---

## 2.7 Team Messaging Examples

### Example: Broadcasting Sprint Start

```bash
curl -X POST "http://localhost:23000/api/messages/broadcast" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Sprint 5 Kickoff",
    "priority": "normal",
    "content": {
      "type": "announcement",
      "message": "Sprint 5 has started. Duration: 2 weeks. Goal: Complete user authentication module. Check your individual task assignments in your inbox."
    }
  }'
```

### Example: Requesting Status Update

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "libs-svg-svgbbox",
    "subject": "Status Request: SVG Parser Implementation",
    "priority": "high",
    "content": {
      "type": "request",
      "message": "Please provide current status on SVG parser implementation. Include: percent complete, blockers if any, estimated completion.",
      "deadline": "2025-02-01T18:00:00Z"
    }
  }'
```

### Example: Sending Alert

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "ALERT: Test Suite Failing",
    "priority": "urgent",
    "content": {
      "type": "alert",
      "severity": "high",
      "message": "Integration tests failing after latest merge. 15 tests affected. Blocking deployment pipeline."
    }
  }'
```

### Example: Sending Task Completion Update

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "orchestrator-master",
    "subject": "Task Complete: API Documentation",
    "priority": "normal",
    "content": {
      "type": "status-update",
      "task": "TASK-042",
      "status": "completed",
      "message": "API documentation updated. Added 12 new endpoints. PR #156 ready for review."
    }
  }'
```

---

## 2.8 Troubleshooting

### Issue: Messages not being delivered

**Symptoms:** Recipient never receives message, no delivery confirmation.

**Possible causes:**
- AI Maestro service not running
- Incorrect recipient session name
- Network connectivity issue

**Resolution:**
1. Verify AI Maestro is running: `curl http://localhost:23000/health`
2. Check recipient exists: `curl http://localhost:23000/api/sessions`
3. Verify session name spelling (case-sensitive)
4. Check AI Maestro logs for errors

### Issue: Messages delivered but not read

**Symptoms:** Delivery confirmed but read receipt never received.

**Possible causes:**
- Recipient not checking inbox
- Recipient session crashed after delivery
- Message buried in large inbox

**Resolution:**
1. Send follow-up with higher priority
2. Use URGENT priority if critical
3. Check recipient session health
4. Consider broadcasting if truly important

### Issue: Duplicate messages received

**Symptoms:** Recipient gets same message multiple times.

**Possible causes:**
- Retry logic sent duplicates
- Message queue reprocessed
- Sender script error

**Resolution:**
1. Include unique message ID in content
2. Recipients should dedupe by ID
3. Review sending logic for retry bugs
4. Check AI Maestro deduplication settings

### Issue: Message priority not respected

**Symptoms:** URGENT messages not prompting immediate attention.

**Possible causes:**
- Recipient not configured for priority handling
- Hook not triggering on priority
- Priority field misspelled

**Resolution:**
1. Verify priority field is exactly "urgent", "high", or "normal"
2. Check recipient's hook configuration
3. Test with known-working message

---

**Version:** 1.0
**Last Updated:** 2025-02-01
