# Teammate Awareness Reference

## Table of Contents

- 3.1 [Managing The Team Roster](#31-managing-the-team-roster)
- 3.2 [Polling Agent Status](#32-polling-agent-status)
- 3.3 [Detecting Agent Activity](#33-detecting-agent-activity)
- 3.4 [Handling Inactive Agents](#34-handling-inactive-agents)
- 3.5 [Reporting Team Status](#35-reporting-team-status)
- 3.6 [Teammate Awareness Examples](#36-teammate-awareness-examples)
- 3.7 [Troubleshooting](#37-troubleshooting)

---

## 3.1 Managing The Team Roster

The team roster is the authoritative record of all agents in the coordinated team, their roles, and their current status.

### Roster Location

Store the team roster in the Chief of Staff's coordination state file:

```
design/memory/team-roster.md
```

### Roster Format

```markdown
# Team Roster

Last Updated: 2025-02-01T10:00:00Z

## Active Team Members

| Session Name | Role | Status | Last Seen | Current Task |
|--------------|------|--------|-----------|--------------|
| orchestrator-master | Orchestrator | active | 2025-02-01T10:00:00Z | Sprint planning |
| helper-agent-generic | Code Reviewer | active | 2025-02-01T09:55:00Z | Reviewing PR #123 |
| libs-svg-svgbbox | Developer | active | 2025-02-01T09:50:00Z | Implementing parser |

## Inactive Team Members

| Session Name | Role | Last Active | Reason |
|--------------|------|-------------|--------|
| helper-agent-backup | Developer | 2025-01-31T18:00:00Z | Session ended |
```

### Roster Update Triggers

Update the roster when:
- New agent joins the team
- Agent role changes
- Agent goes inactive
- Agent comes back online
- Current task changes significantly
- Periodic refresh (every 15 minutes)

### Roster Update Procedure

**Step 1:** Query AI Maestro for current session states
**Step 2:** Compare with existing roster
**Step 3:** Update changed entries with timestamp
**Step 4:** Move inactive agents to inactive section
**Step 5:** Write updated roster to disk

---

## 3.2 Polling Agent Status

Regular status polling ensures the Chief of Staff has accurate information about team state.

### Polling Frequency

| Situation | Frequency |
|-----------|-----------|
| Normal operations | Every 15 minutes |
| Active coordination | Every 5 minutes |
| Critical incident | Every 1 minute |
| Before task assignment | Immediately |

### Polling Procedure

**Step 1: Query all sessions**

```bash
curl -s "http://localhost:23000/api/sessions" | jq '.sessions'
```

**Step 2: Extract relevant information**

For each session, capture:
- Session name
- Status (active, idle, busy)
- Last activity timestamp
- Current task (if reported)

**Step 3: Update local roster**

Compare polled data with roster and update differences.

**Step 4: Identify concerns**

Flag any agents that:
- Have not been seen in expected timeframe
- Report unexpected status
- Show concerning patterns

### Individual Agent Status Query

```bash
# Get specific agent status
curl -s "http://localhost:23000/api/sessions/helper-agent-generic" | jq '.'
```

### Batch Status Query Script

```bash
#!/bin/bash
# poll-team-status.sh

SESSIONS=$(curl -s "http://localhost:23000/api/sessions" | jq -r '.sessions[].name')

for session in $SESSIONS; do
  STATUS=$(curl -s "http://localhost:23000/api/sessions/$session" | jq -r '.status')
  LAST_SEEN=$(curl -s "http://localhost:23000/api/sessions/$session" | jq -r '.lastSeen')
  echo "$session: $STATUS (last seen: $LAST_SEEN)"
done
```

---

## 3.3 Detecting Agent Activity

Activity detection helps distinguish between agents that are working and those that may be stuck or inactive.

### Activity Indicators

**Active indicators:**
- Message sent or received within last 5 minutes
- Tool execution within last 5 minutes
- Status update sent within last 15 minutes
- Acknowledged polling request

**Idle indicators:**
- No tool execution in 15+ minutes
- No messages in 30+ minutes
- Session still connected but quiet

**Inactive indicators:**
- Session disconnected
- No response to multiple polling attempts
- Last activity over 1 hour ago

### Activity Monitoring Procedure

**Step 1: Check message activity**

```bash
# Messages sent by agent in last hour
curl -s "http://localhost:23000/api/messages?from=helper-agent-generic&since=1h" | jq '.count'
```

**Step 2: Check session heartbeat**

```bash
# Session last activity
curl -s "http://localhost:23000/api/sessions/helper-agent-generic" | jq '.lastActivity'
```

**Step 3: Send ping if uncertain**

```bash
# Send a low-priority ping
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "helper-agent-generic",
    "subject": "Heartbeat Check",
    "priority": "normal",
    "content": {"type": "request", "message": "Please acknowledge you are active."}
  }'
```

**Step 4: Evaluate response**

If no response within 10 minutes, classify as potentially inactive.

---

## 3.4 Handling Inactive Agents

When an agent becomes inactive, the Chief of Staff must take action to prevent coordination failures.

### Inactivity Classification

| Duration | Classification | Action |
|----------|---------------|--------|
| 15-30 minutes | Possibly idle | Send ping |
| 30-60 minutes | Likely inactive | Send alert, check tasks |
| 1+ hours | Inactive | Reassign tasks, notify team |
| Session ended | Offline | Remove from active roster |

### Handling Procedure

**Step 1: Confirm inactivity**

Send a high-priority ping and wait 5 minutes for response.

**Step 2: Identify affected work**

Check what tasks were assigned to the inactive agent:
- In-progress tasks need reassignment
- Pending tasks can wait or be reassigned
- Completed tasks should be verified

**Step 3: Reassign critical tasks**

For any blocking or time-sensitive tasks, immediately reassign to available agent.

**Step 4: Notify relevant parties**

Inform orchestrator and any dependent agents of the situation.

**Step 5: Update roster**

Move agent to inactive section with timestamp and reason.

**Step 6: Document**

Record the inactivity event in coordination log for pattern analysis.

### Recovery When Agent Returns

When an inactive agent comes back online:

**Step 1:** Update roster status to active

**Step 2:** Brief the agent on what happened during absence

**Step 3:** Reassign any tasks that were transferred

**Step 4:** Verify agent is ready to resume work

---

## 3.5 Reporting Team Status

The Chief of Staff regularly reports team status to the orchestrator and user.

### Status Report Format

```markdown
# Team Status Report

Generated: 2025-02-01T10:00:00Z
Reporting Period: Last 24 hours

## Summary
- Total team members: 5
- Active: 4
- Inactive: 1

## Active Agents

### orchestrator-master
- Role: Orchestrator
- Status: Active
- Current Task: Sprint planning
- Tasks Completed (24h): 3
- Health: Good

### helper-agent-generic
- Role: Code Reviewer
- Status: Active
- Current Task: Reviewing PR #123
- Tasks Completed (24h): 7
- Health: Good

## Inactive Agents

### helper-agent-backup
- Role: Developer
- Last Active: 2025-01-31T18:00:00Z
- Reason: Session ended
- Affected Tasks: None

## Alerts
- None

## Recommendations
- Consider bringing helper-agent-backup back online for additional capacity
```

### Reporting Frequency

| Report Type | Frequency | Recipients |
|-------------|-----------|------------|
| Quick status | On request | Requester |
| Daily summary | Every 24 hours | Orchestrator |
| Incident report | On incident | All relevant parties |
| Weekly review | Every 7 days | User |

---

## 3.6 Teammate Awareness Examples

### Example: Updating Roster After Status Poll

```bash
# Poll all sessions
SESSIONS=$(curl -s "http://localhost:23000/api/sessions" | jq -r '.sessions[] | "\(.name)|\(.status)|\(.lastSeen)"')

# Update roster file
cat > design/memory/team-roster-update.md << 'EOF'
# Team Roster Update

Last Polled: $(date -u +%Y-%m-%dT%H:%M:%SZ)

| Session | Status | Last Seen |
|---------|--------|-----------|
EOF

for session in $SESSIONS; do
  echo "| $session |" >> design/memory/team-roster-update.md
done
```

### Example: Sending Team-Wide Status Request

```bash
# Request status from all active agents
curl -X POST "http://localhost:23000/api/messages/broadcast" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Status Check - Please Respond",
    "priority": "normal",
    "content": {
      "type": "request",
      "message": "Please respond with your current status: (1) Current task, (2) Percent complete, (3) Any blockers. Respond within 15 minutes."
    }
  }'
```

### Example: Handling Agent Going Offline

```bash
# Agent helper-agent-backup stopped responding

# Step 1: Confirm
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "helper-agent-backup",
    "subject": "URGENT: Status Check",
    "priority": "urgent",
    "content": {"type": "request", "message": "Please respond immediately if you are active."}
  }'

# Step 2: Wait 5 minutes, then check for response
sleep 300
RESPONSE=$(curl -s "http://localhost:23000/api/messages?from=helper-agent-backup&since=5m" | jq '.count')

if [ "$RESPONSE" -eq 0 ]; then
  # Step 3: Mark as inactive and notify team
  curl -X POST "http://localhost:23000/api/messages" \
    -H "Content-Type: application/json" \
    -d '{
      "to": "orchestrator-master",
      "subject": "Agent Offline: helper-agent-backup",
      "priority": "high",
      "content": {
        "type": "alert",
        "severity": "medium",
        "message": "helper-agent-backup is unresponsive. Any assigned tasks should be reassigned."
      }
    }'
fi
```

---

## 3.7 Troubleshooting

### Issue: Cannot query session status

**Symptoms:** API calls return errors or empty results.

**Possible causes:**
- AI Maestro service down
- Session registry corrupted
- Network issue

**Resolution:**
1. Check AI Maestro health: `curl http://localhost:23000/health`
2. Restart AI Maestro if needed
3. Verify network connectivity
4. Check AI Maestro logs for errors

### Issue: Roster gets out of sync with reality

**Symptoms:** Roster shows agents as active when they are not, or vice versa.

**Possible causes:**
- Polling too infrequent
- Roster not being written to disk
- Multiple processes updating roster

**Resolution:**
1. Increase polling frequency
2. Verify roster writes are successful
3. Ensure single process owns roster updates
4. Force full refresh from API

### Issue: Agent shows active but is not responding

**Symptoms:** Session appears active in API but agent does not respond to messages.

**Possible causes:**
- Agent in infinite loop
- Agent processing large task
- Claude Code session frozen
- Hook blocking messages

**Resolution:**
1. Wait reasonable time (10-15 minutes)
2. Check if agent is processing visible work
3. Escalate to user if session appears frozen
4. User may need to restart the Claude Code session

### Issue: Too many status queries causing overhead

**Symptoms:** High API traffic, slow responses, coordination delays.

**Possible causes:**
- Polling too frequently
- Not caching results
- Querying all agents for every decision

**Resolution:**
1. Implement caching with TTL (e.g., 5 minute cache)
2. Reduce polling frequency during quiet periods
3. Query specific agents instead of all
4. Batch queries where possible

---

**Version:** 1.0
**Last Updated:** 2025-02-01
