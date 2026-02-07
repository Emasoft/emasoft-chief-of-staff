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
2. Use the `agent-messaging` skill to send a high-priority status inquiry:
   - **Recipient**: the unresponsive agent session name
   - **Subject**: `[URGENT] Status inquiry`
   - **Priority**: `urgent`
   - **Content**: type `status-inquiry`, message: "Please acknowledge this message."
3. If no response in 5 minutes, classify as recoverable and attempt restart

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
         |
         v
Classify as RECOVERABLE (conservative)
         |
         v
Attempt recovery strategies 1-4 in order
         |
         +-- Success? Done
         |
         +-- 3 failures? Escalate to TERMINAL
```

---

## Manager does not respond to urgent request

**Symptom**: Sent urgent replacement request, no response from EAMA.

**Solution**:
1. Wait 15 minutes
2. Use the `agent-messaging` skill to send a reminder:
   - **Recipient**: `eama-assistant-manager` (or the manager session name)
   - **Subject**: `[REMINDER] Agent replacement still awaiting approval`
   - **Priority**: `urgent`
   - **Content**: type `reminder`, message: "Original request sent 15 minutes ago. Agent [agent-name] replacement requires approval." Include `original_subject`: "[APPROVAL REQUIRED] Agent replacement request".
3. If user contact is configured, escalate to user
4. Do NOT proceed with replacement without approval

**CRITICAL**: Never proceed with replacement without manager approval.

---

## New replacement agent fails to register

**Symptom**: New Claude Code session started but AI Maestro shows no agent.

**Solution**:
1. Use the `ai-maestro-agents-management` skill to check service health
2. Verify hooks configured in new agent's environment
3. Check for errors in Claude Code startup output
4. Restart Claude Code session

**Diagnostic steps**:
1. Use the `ai-maestro-agents-management` skill to check if AI Maestro is healthy
2. Use the `ai-maestro-agents-management` skill to list all registered agents
3. Use the `ai-maestro-agents-management` skill to check if the specific new agent session name appears

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

**Notify stakeholders** using the `agent-messaging` skill:
- **Recipient**: `eama-assistant-manager` (or the manager session name)
- **Subject**: `[INCIDENT] Deadline missed - post-mortem required`
- **Priority**: `high`
- **Content**: type `incident-report`, message: "Emergency handoff for [agent-name] did not prevent deadline miss. Post-mortem recommended." Include `deadline_missed` timestamp and `work_completed_at` timestamp.
