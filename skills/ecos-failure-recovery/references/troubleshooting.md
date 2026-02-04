# Troubleshooting: Failure Recovery

## Table of Contents

- [Agent shows online but unresponsive](#agent-shows-online-but-is-unresponsive)
- [Cannot determine failure type](#cannot-determine-failure-type)
- [Manager does not respond](#manager-does-not-respond-to-urgent-request)
- [New replacement agent fails to register](#new-replacement-agent-fails-to-register)
- [Emergency handoff deadline missed](#emergency-handoff-deadline-still-missed)

## Use-Case TOC

- When agent appears online but ignores messages -> [Agent shows online but is unresponsive](#agent-shows-online-but-is-unresponsive)
- When failure symptoms are ambiguous -> [Cannot determine failure type](#cannot-determine-failure-type)
- When EAMA does not respond to urgent request -> [Manager does not respond to urgent request](#manager-does-not-respond-to-urgent-request)
- When new agent does not appear in AI Maestro -> [New replacement agent fails to register](#new-replacement-agent-fails-to-register)
- When deadline was missed despite emergency handoff -> [Emergency handoff deadline still missed](#emergency-handoff-deadline-still-missed)

---

## Agent shows "online" but is unresponsive

**Symptom**: AI Maestro shows agent online, but it does not respond to messages.

**Cause**: Agent's message polling hook may be disabled or failing.

**Solution**:
1. Check if agent has AI Maestro hooks in `~/.claude/settings.json`
2. Send a high-priority status inquiry
3. If no response in 5 minutes, classify as recoverable and attempt restart

**Verification command**:
```bash
# Send high-priority status inquiry
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "AGENT_NAME",
    "subject": "[URGENT] Status inquiry",
    "priority": "urgent",
    "content": {"type": "status-inquiry", "message": "Please acknowledge this message."}
  }'
```

---

## Cannot determine failure type

**Symptom**: Symptoms are ambiguous, not clearly transient, recoverable, or terminal.

**Solution**:
1. Default to most conservative classification (recoverable)
2. Attempt recovery strategies in order
3. Escalate to terminal only after 3 failed recovery attempts
4. Document uncertainty in incident log

**Decision process**:
```
Unknown failure type?
         │
         ▼
Classify as RECOVERABLE (conservative)
         │
         ▼
Attempt recovery strategies 1-4 in order
         │
         ├─► Success? Done
         │
         └─► 3 failures? Escalate to TERMINAL
```

---

## Manager does not respond to urgent request

**Symptom**: Sent urgent replacement request, no response from EAMA.

**Solution**:
1. Wait 15 minutes
2. Send reminder with increased urgency
3. If user contact is configured, escalate to user
4. Do NOT proceed with replacement without approval

**Reminder message**:
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eama-assistant-manager",
    "subject": "[REMINDER] Agent replacement still awaiting approval",
    "priority": "urgent",
    "content": {
      "type": "reminder",
      "message": "Original request sent 15 minutes ago. Agent AGENT_NAME replacement requires approval.",
      "original_subject": "[APPROVAL REQUIRED] Agent replacement request"
    }
  }'
```

**CRITICAL**: Never proceed with replacement without manager approval.

---

## New replacement agent fails to register

**Symptom**: New Claude Code session started but AI Maestro shows no agent.

**Solution**:
1. Verify AI Maestro server is running: `curl http://localhost:23000/health`
2. Verify hooks configured in new agent's environment
3. Check for errors in Claude Code startup output
4. Restart Claude Code session

**Diagnostic commands**:
```bash
# Check AI Maestro health
curl -s http://localhost:23000/health | jq .

# List all registered agents
curl -s "http://localhost:23000/api/agents" | jq '.agents[].name'

# Check if specific agent is registered
curl -s "http://localhost:23000/api/agents/NEW_AGENT_NAME/status" | jq .
```

**Common causes**:
- AI Maestro server not running
- Hooks not configured in `~/.claude/settings.json`
- Network/port issues (check port 23000)
- Session name collision with existing agent

---

## Emergency handoff deadline still missed

**Symptom**: Despite emergency handoff, the deadline passed.

**Solution**:
1. Document timeline and bottlenecks
2. Notify stakeholders immediately
3. Complete work as soon as possible
4. Conduct post-mortem
5. Adjust escalation thresholds for future incidents

**Post-incident documentation template**:
```markdown
## Post-Incident Report

**Incident ID**: INC-YYYYMMDD-XXX
**Failed Agent**: AGENT_NAME
**Missed Deadline**: YYYY-MM-DD HH:MM:SS

### Timeline
- [HH:MM] Failure detected
- [HH:MM] Emergency handoff initiated
- [HH:MM] Receiving agent assigned
- [HH:MM] Deadline passed
- [HH:MM] Work completed (late)

### Bottlenecks Identified
- [ ] Slow failure detection
- [ ] Slow manager approval
- [ ] No available agents
- [ ] Incomplete handoff documentation
- [ ] Other: _______________

### Recommendations
1. _____________
2. _____________
```

**Notify stakeholders**:
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "ecos-chief-of-staff",
    "to": "eama-assistant-manager",
    "subject": "[INCIDENT] Deadline missed - post-mortem required",
    "priority": "high",
    "content": {
      "type": "incident-report",
      "message": "Emergency handoff for AGENT_NAME did not prevent deadline miss. Post-mortem recommended.",
      "deadline_missed": "YYYY-MM-DDTHH:MM:SSZ",
      "work_completed_at": "YYYY-MM-DDTHH:MM:SSZ"
    }
  }'
```
