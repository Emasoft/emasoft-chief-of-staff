# Success Criteria for Agent Lifecycle Operations

**How to verify each operation completed successfully:**

## Agent Spawned Successfully

Verify ALL criteria met:
- [ ] tmux session exists: `tmux has-session -t <agent-name> 2>/dev/null && echo "EXISTS"`
- [ ] Agent registered in AI Maestro: `curl -s "http://localhost:23000/api/agents" | jq -r '.agents[] | select(.name == "<agent-name>")'`
- [ ] Agent responds to health check message within 30s
- [ ] Agent's working directory exists and accessible
- [ ] Team registry updated (if assigned to team)
- [ ] Lifecycle log entry written

**Evidence Required:**
- tmux session list output showing agent session
- AI Maestro agents list showing agent registration
- Health check message response with timestamp
- Directory existence verification
- Team registry JSON showing agent in members array
- Lifecycle log entry with spawn timestamp

**Self-Check Commands:**
```bash
# Verify tmux session
tmux has-session -t <agent-name> 2>/dev/null && echo "EXISTS" || echo "MISSING"

# Verify AI Maestro registration
curl -s "http://localhost:23000/api/agents" | jq -r '.agents[] | select(.name == "<agent-name>")'

# Verify working directory
ls -ld <working-directory>

# Send health check
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{"to": "<agent-name>", "subject": "Health Check", "content": {"type": "system", "message": "ping"}}'

# Check lifecycle log
tail -n 20 docs_dev/chief-of-staff/agent-lifecycle.log | grep "<agent-name>"
```

---

## Agent Terminated Cleanly

Verify ALL criteria met:
- [ ] tmux session removed: `tmux has-session -t <agent-name> 2>/dev/null || echo "REMOVED"`
- [ ] Agent deregistered from AI Maestro
- [ ] Agent removed from all team registries
- [ ] No orphaned processes (check with `ps aux | grep <agent-name>`)
- [ ] Working directory cleaned up (if temporary)
- [ ] Lifecycle log entry written

**Evidence Required:**
- tmux session list showing agent session no longer exists
- AI Maestro agents list showing agent not present
- Team registries showing agent removed from all teams
- Process list showing no processes matching agent name
- Directory removal confirmation (if temporary)
- Lifecycle log entry with termination timestamp

**Self-Check Commands:**
```bash
# Verify tmux session removed
tmux has-session -t <agent-name> 2>/dev/null && echo "STILL EXISTS" || echo "REMOVED"

# Verify AI Maestro deregistration
curl -s "http://localhost:23000/api/agents" | jq -r '.agents[] | select(.name == "<agent-name>")' | grep -q . && echo "STILL REGISTERED" || echo "DEREGISTERED"

# Check for orphaned processes
ps aux | grep <agent-name> | grep -v grep

# Check team registries
find . -name "team-registry.json" -exec jq -r '.teams[].members[] | select(.name == "<agent-name>")' {} \;

# Check lifecycle log
tail -n 20 docs_dev/chief-of-staff/agent-lifecycle.log | grep "<agent-name>"
```

---

## Agent Hibernated Successfully

Verify ALL criteria met:
- [ ] tmux session still exists (not terminated)
- [ ] Agent marked as `hibernated` in AI Maestro
- [ ] Agent status in team registry updated to `hibernated`
- [ ] Context saved to disk: `$CLAUDE_PROJECT_DIR/.emasoft/hibernated-agents/<agent-name>/context.json`
- [ ] Agent does NOT respond to messages (sleeping)
- [ ] Lifecycle log entry written

**Evidence Required:**
- tmux session list showing agent session still exists
- AI Maestro agents list showing agent status as `hibernated`
- Team registry showing agent status as `hibernated`
- Context JSON file with valid structure and timestamp
- No response to health check message within 30s
- Lifecycle log entry with hibernation timestamp

**Self-Check Commands:**
```bash
# Verify tmux session exists
tmux has-session -t <agent-name> 2>/dev/null && echo "EXISTS" || echo "TERMINATED"

# Verify hibernation status in AI Maestro
curl -s "http://localhost:23000/api/agents" | jq -r '.agents[] | select(.name == "<agent-name>") | .status'

# Verify context saved
ls -l $CLAUDE_PROJECT_DIR/.emasoft/hibernated-agents/<agent-name>/context.json

# Verify context JSON valid
jq . $CLAUDE_PROJECT_DIR/.emasoft/hibernated-agents/<agent-name>/context.json

# Send health check (should timeout)
timeout 30 curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{"to": "<agent-name>", "subject": "Health Check", "content": {"type": "system", "message": "ping"}}'

# Check lifecycle log
tail -n 20 docs_dev/chief-of-staff/agent-lifecycle.log | grep "<agent-name>"
```

---

## Agent Woken Successfully

Verify ALL criteria met:
- [ ] Agent responds to health check message within 30s
- [ ] Agent status in AI Maestro updated to `active`
- [ ] Agent status in team registry updated to `active`
- [ ] Context restored from hibernation snapshot
- [ ] Agent resumes work from last known state
- [ ] Lifecycle log entry written

**Evidence Required:**
- Health check message response with timestamp
- AI Maestro agents list showing agent status as `active`
- Team registry showing agent status as `active`
- Agent conversation showing context continuity from before hibernation
- Agent acknowledges resuming from saved state
- Lifecycle log entry with wake timestamp

**Self-Check Commands:**
```bash
# Send health check
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{"to": "<agent-name>", "subject": "Health Check", "content": {"type": "system", "message": "ping"}}'

# Verify active status in AI Maestro
curl -s "http://localhost:23000/api/agents" | jq -r '.agents[] | select(.name == "<agent-name>") | .status'

# Verify team registry status
jq -r '.teams[].members[] | select(.name == "<agent-name>") | .status' .emasoft/team-registry.json

# Check lifecycle log
tail -n 20 docs_dev/chief-of-staff/agent-lifecycle.log | grep "<agent-name>"

# Verify context file still exists (not deleted after restore)
ls -l $CLAUDE_PROJECT_DIR/.emasoft/hibernated-agents/<agent-name>/context.json
```

---

## Team Assignment Complete

Verify ALL criteria met:
- [ ] Team registry exists: `.emasoft/team-registry.json` in project directory
- [ ] Agent listed in team's `members` array
- [ ] Agent's role correctly specified in registry
- [ ] Agent notified of team assignment via AI Maestro message
- [ ] EOA (if exists) notified of new team member
- [ ] Team directory structure created (if new team)

**Evidence Required:**
- Team registry JSON file with valid structure
- Agent entry in team's members array with correct role
- AI Maestro message sent to agent confirming assignment
- EOA notification message (if EOA exists)
- Team directories created under `.emasoft/teams/<team-name>/`
- Lifecycle log entry with team assignment timestamp

**Self-Check Commands:**
```bash
# Verify team registry exists
ls -l .emasoft/team-registry.json

# Verify agent in team
jq -r '.teams[] | select(.name == "<team-name>") | .members[] | select(.name == "<agent-name>")' .emasoft/team-registry.json

# Verify team structure
ls -ld .emasoft/teams/<team-name>/

# Check AI Maestro message log (if available)
curl -s "http://localhost:23000/api/messages?agent=<agent-name>&status=unread" | jq '.messages[] | select(.subject | contains("Team Assignment"))'

# Check lifecycle log
tail -n 20 docs_dev/chief-of-staff/agent-lifecycle.log | grep "<agent-name>"
```

---

## Approval Obtained

Verify ALL criteria met:
- [ ] Approval request submitted to EAMA
- [ ] Request ID generated and logged
- [ ] Manager decision received within timeout
- [ ] Decision is `approved` (not `rejected` or `revision_needed`)
- [ ] Decision logged to audit trail
- [ ] Requester notified of approval

**Evidence Required:**
- AI Maestro message to EAMA with request details
- Request ID in approval log
- Manager response message with decision
- Decision is explicitly `approved`
- Audit trail entry with request ID, operation, decision, timestamp
- Confirmation message sent to requester

**Self-Check Commands:**
```bash
# Check approval log
grep "<request-id>" docs_dev/chief-of-staff/approval-requests.log

# Verify audit trail entry
tail -n 50 docs_dev/chief-of-staff/approval-audit.log | grep "<request-id>"

# Check AI Maestro messages (if available)
curl -s "http://localhost:23000/api/messages?agent=eama-assistant-manager&status=read" | jq '.messages[] | select(.subject | contains("Approval Request"))'

# Verify decision is approved
grep "<request-id>" docs_dev/chief-of-staff/approval-audit.log | grep -o '"decision":"[^"]*"'
```

---

## Common Self-Check Failures and Solutions

### Agent Does Not Respond to Health Check

**Symptom**: Health check message times out after 30s

**Possible Causes**:
1. Agent tmux session crashed
2. AI Maestro connection lost
3. Agent is processing long-running task
4. Agent is hibernated but status not updated

**Verification Steps**:
```bash
# Check tmux session status
tmux has-session -t <agent-name> 2>/dev/null && echo "EXISTS" || echo "CRASHED"

# Check AI Maestro connection
curl -s "http://localhost:23000/health" | jq .

# Check agent's last activity
curl -s "http://localhost:23000/api/agents" | jq -r '.agents[] | select(.name == "<agent-name>") | .lastSeen'

# Attach to tmux session to see agent state
tmux attach -t <agent-name>
```

### Team Registry Not Updated

**Symptom**: Agent not appearing in team registry after assignment

**Possible Causes**:
1. Team does not exist in registry
2. Registry file permissions issue
3. JSON syntax error in registry
4. Assignment operation failed silently

**Verification Steps**:
```bash
# Verify registry file exists and readable
ls -l .emasoft/team-registry.json

# Validate JSON syntax
jq . .emasoft/team-registry.json

# Check for team existence
jq -r '.teams[] | .name' .emasoft/team-registry.json

# Check file permissions
stat -f "%A %u %g" .emasoft/team-registry.json
```

### Context Not Saved During Hibernation

**Symptom**: Context file missing or empty after hibernation

**Possible Causes**:
1. Directory permissions issue
2. Disk space full
3. Agent crashed during hibernation
4. Context serialization failed

**Verification Steps**:
```bash
# Check directory permissions
ls -ld $CLAUDE_PROJECT_DIR/.emasoft/hibernated-agents/<agent-name>/

# Check disk space
df -h $CLAUDE_PROJECT_DIR

# Check file size
ls -lh $CLAUDE_PROJECT_DIR/.emasoft/hibernated-agents/<agent-name>/context.json

# Validate JSON structure
jq . $CLAUDE_PROJECT_DIR/.emasoft/hibernated-agents/<agent-name>/context.json

# Check for write errors in logs
grep "hibernation" docs_dev/chief-of-staff/agent-lifecycle.log | grep -i error
```

---

## Completion Criteria Summary

**Operation is considered COMPLETE when:**
1. All verification criteria checkboxes marked as complete
2. All self-check commands return expected results
3. All evidence collected and logged
4. No errors or warnings in lifecycle log
5. Operation logged to audit trail (if applicable)
6. Relevant parties notified (requester, EOA, team members)

**Operation is considered FAILED when:**
1. Any critical verification criteria fails
2. Self-check commands return unexpected results
3. Timeout exceeded without completion
4. Error messages in lifecycle log
5. Rollback required

**Partial Success (Requires Investigation):**
1. Some verification criteria met, others failed
2. Self-check commands return inconsistent results
3. Operation completed but warnings logged
4. Notifications sent but not acknowledged
