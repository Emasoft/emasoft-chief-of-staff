# Success Criteria for Agent Lifecycle Operations


## Contents

- [Agent Spawned Successfully](#agent-spawned-successfully)
- [Agent Terminated Cleanly](#agent-terminated-cleanly)
- [Agent Hibernated Successfully](#agent-hibernated-successfully)
- [Agent Woken Successfully](#agent-woken-successfully)
- [Team Assignment Complete](#team-assignment-complete)
- [Approval Obtained](#approval-obtained)
- [Common Self-Check Failures and Solutions](#common-self-check-failures-and-solutions)
  - [Agent Does Not Respond to Health Check](#agent-does-not-respond-to-health-check)
  - [Team Registry Not Updated](#team-registry-not-updated)
  - [Context Not Saved During Hibernation](#context-not-saved-during-hibernation)
- [Completion Criteria Summary](#completion-criteria-summary)

**How to verify each operation completed successfully:**

## Agent Spawned Successfully

Verify ALL criteria met:
- [ ] Agent session exists and is running
- [ ] Agent registered in AI Maestro
- [ ] Agent responds to health check message within 30s
- [ ] Agent's working directory exists and is accessible
- [ ] Team registry updated (if assigned to team)
- [ ] Lifecycle log entry written

**Evidence Required:**
- Session exists (use the `ai-maestro-agents-management` skill to list agents and confirm the new agent appears)
- Agent responds to a health check (use the `agent-messaging` skill to send a health check message and receive a response)
- Directory existence verification
- Team registry JSON showing agent in members array
- Lifecycle log entry with spawn timestamp

**Verification Steps:**

1. Use the `ai-maestro-agents-management` skill to list all agents and confirm the newly spawned agent appears with status `active` or `online`.
2. Use the `agent-messaging` skill to send a health check message to the agent:
   - **Recipient**: the new agent session name
   - **Subject**: `Health Check`
   - **Priority**: `normal`
   - **Content**: type `system`, message: "ping"
3. Verify the agent responds within 30 seconds.
4. Check the working directory exists: `ls -ld <working-directory>`
5. Check team registry (if applicable): `jq '.teams[].members[] | select(.name == "<agent-name>")' .emasoft/team-registry.json`
6. Check lifecycle log: `tail -n 20 docs_dev/chief-of-staff/agent-lifecycle.log | grep "<agent-name>"`

---

## Agent Terminated Cleanly

Verify ALL criteria met:
- [ ] Agent session no longer exists
- [ ] Agent deregistered from AI Maestro
- [ ] Agent removed from all team registries
- [ ] No orphaned processes (check with `ps aux | grep <agent-name>`)
- [ ] Working directory cleaned up (if temporary)
- [ ] Lifecycle log entry written

**Evidence Required:**
- AI Maestro agents list showing agent not present
- Team registries showing agent removed from all teams
- Process list showing no processes matching agent name
- Directory removal confirmation (if temporary)
- Lifecycle log entry with termination timestamp

**Verification Steps:**

1. Use the `ai-maestro-agents-management` skill to list all agents and confirm the terminated agent does NOT appear.
2. Verify no orphaned processes: `ps aux | grep <agent-name> | grep -v grep`
3. Check team registries: `find . -name "team-registry.json" -exec jq -r '.teams[].members[] | select(.name == "<agent-name>")' {} \;`
4. Check lifecycle log: `tail -n 20 docs_dev/chief-of-staff/agent-lifecycle.log | grep "<agent-name>"`

---

## Agent Hibernated Successfully

Verify ALL criteria met:
- [ ] Agent session still exists (not terminated)
- [ ] Agent marked as `hibernated` in AI Maestro
- [ ] Agent status in team registry updated to `hibernated`
- [ ] Context saved to disk: `$CLAUDE_PROJECT_DIR/.emasoft/hibernated-agents/<agent-name>/context.json`
- [ ] Agent does NOT respond to messages (sleeping)
- [ ] Lifecycle log entry written

**Evidence Required:**
- AI Maestro agents list showing agent status as `hibernated`
- Team registry showing agent status as `hibernated`
- Context JSON file with valid structure and timestamp
- No response to health check message within 30s
- Lifecycle log entry with hibernation timestamp

**Verification Steps:**

1. Use the `ai-maestro-agents-management` skill to get the agent's details and confirm status is `hibernated`.
2. Verify context saved: `ls -l $CLAUDE_PROJECT_DIR/.emasoft/hibernated-agents/<agent-name>/context.json`
3. Validate context JSON: `jq . $CLAUDE_PROJECT_DIR/.emasoft/hibernated-agents/<agent-name>/context.json`
4. Use the `agent-messaging` skill to send a health check message. It should timeout after 30 seconds (agent is sleeping).
5. Check lifecycle log: `tail -n 20 docs_dev/chief-of-staff/agent-lifecycle.log | grep "<agent-name>"`

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

**Verification Steps:**

1. Use the `agent-messaging` skill to send a health check message:
   - **Recipient**: the agent session name
   - **Subject**: `Health Check`
   - **Priority**: `normal`
   - **Content**: type `system`, message: "ping"
2. Confirm the agent responds within 30 seconds.
3. Use the `ai-maestro-agents-management` skill to get the agent's details and confirm status is `active`.
4. Check team registry: `jq -r '.teams[].members[] | select(.name == "<agent-name>") | .status' .emasoft/team-registry.json`
5. Check lifecycle log: `tail -n 20 docs_dev/chief-of-staff/agent-lifecycle.log | grep "<agent-name>"`
6. Verify context file still exists: `ls -l $CLAUDE_PROJECT_DIR/.emasoft/hibernated-agents/<agent-name>/context.json`

---

## Team Assignment Complete

Verify ALL criteria met:
- [ ] Team registry exists: `.emasoft/team-registry.json` in project directory
- [ ] Agent listed in team's `members` array
- [ ] Agent's role correctly specified in registry
- [ ] Agent notified of team assignment via messaging
- [ ] EOA (if exists) notified of new team member
- [ ] Team directory structure created (if new team)

**Evidence Required:**
- Team registry JSON file with valid structure
- Agent entry in team's members array with correct role
- Message sent to agent confirming assignment
- EOA notification message (if EOA exists)
- Team directories created under `.emasoft/teams/<team-name>/`
- Lifecycle log entry with team assignment timestamp

**Verification Steps:**

1. Verify team registry exists: `ls -l .emasoft/team-registry.json`
2. Verify agent in team: `jq -r '.teams[] | select(.name == "<team-name>") | .members[] | select(.name == "<agent-name>")' .emasoft/team-registry.json`
3. Verify team structure: `ls -ld .emasoft/teams/<team-name>/`
4. Use the `agent-messaging` skill to check inbox for the agent and confirm a team assignment message was delivered:
   - Filter by subject containing "Team Assignment"
5. Check lifecycle log: `tail -n 20 docs_dev/chief-of-staff/agent-lifecycle.log | grep "<agent-name>"`

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
- Message to EAMA with request details
- Request ID in approval log
- Manager response message with decision
- Decision is explicitly `approved`
- Audit trail entry with request ID, operation, decision, timestamp
- Confirmation message sent to requester

**Verification Steps:**

1. Check approval log: `grep "<request-id>" docs_dev/chief-of-staff/approval-requests.log`
2. Verify audit trail entry: `tail -n 50 docs_dev/chief-of-staff/approval-audit.log | grep "<request-id>"`
3. Use the `agent-messaging` skill to check inbox for messages from EAMA containing approval decisions related to the request ID.
4. Verify decision is approved: `grep "<request-id>" docs_dev/chief-of-staff/approval-audit.log | grep -o '"decision":"[^"]*"'`

---

## Common Self-Check Failures and Solutions

### Agent Does Not Respond to Health Check

**Symptom**: Health check message times out after 30s

**Possible Causes**:
1. Agent session crashed
2. AI Maestro connection lost
3. Agent is processing long-running task
4. Agent is hibernated but status not updated

**Verification Steps**:
1. Use the `ai-maestro-agents-management` skill to check if the agent is listed and its status.
2. Use the `ai-maestro-agents-management` skill to perform a health check on the AI Maestro service itself.
3. Check if the agent's session still exists by reviewing the agent list.
4. If agent is listed as active but not responding, consider restarting the agent.

### Team Registry Not Updated

**Symptom**: Agent not appearing in team registry after assignment

**Possible Causes**:
1. Team does not exist in registry
2. Registry file permissions issue
3. JSON syntax error in registry
4. Assignment operation failed silently

**Verification Steps**:
1. Verify registry file exists and is readable: `ls -l .emasoft/team-registry.json`
2. Validate JSON syntax: `jq . .emasoft/team-registry.json`
3. Check for team existence: `jq -r '.teams[] | .name' .emasoft/team-registry.json`
4. Check file permissions: `stat -f "%A %u %g" .emasoft/team-registry.json`

### Context Not Saved During Hibernation

**Symptom**: Context file missing or empty after hibernation

**Possible Causes**:
1. Directory permissions issue
2. Disk space full
3. Agent crashed during hibernation
4. Context serialization failed

**Verification Steps**:
1. Check directory permissions: `ls -ld $CLAUDE_PROJECT_DIR/.emasoft/hibernated-agents/<agent-name>/`
2. Check disk space: `df -h $CLAUDE_PROJECT_DIR`
3. Check file size: `ls -lh $CLAUDE_PROJECT_DIR/.emasoft/hibernated-agents/<agent-name>/context.json`
4. Validate JSON structure: `jq . $CLAUDE_PROJECT_DIR/.emasoft/hibernated-agents/<agent-name>/context.json`
5. Check for write errors in logs: `grep "hibernation" docs_dev/chief-of-staff/agent-lifecycle.log | grep -i error`

---

## Completion Criteria Summary

**Operation is considered COMPLETE when:**
1. All verification criteria checkboxes marked as complete
2. All verification steps return expected results
3. All evidence collected and logged
4. No errors or warnings in lifecycle log
5. Operation logged to audit trail (if applicable)
6. Relevant parties notified (requester, EOA, team members)

**Operation is considered FAILED when:**
1. Any critical verification criteria fails
2. Verification steps return unexpected results
3. Timeout exceeded without completion
4. Error messages in lifecycle log
5. Rollback required

**Partial Success (Requires Investigation):**
1. Some verification criteria met, others failed
2. Verification steps return inconsistent results
3. Operation completed but warnings logged
4. Notifications sent but not acknowledged
