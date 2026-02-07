# Pre-Operation Notifications Reference

## Table of Contents

- 1.1 What are pre-operation notifications - Understanding warning messages
- 1.2 When to send pre-operation notifications - Notification triggers
  - 1.2.1 Skill installation - Agent will be hibernated and woken
  - 1.2.2 Plugin installation - Agent restart required
  - 1.2.3 Configuration changes - Settings will change
  - 1.2.4 System maintenance - Temporary disruption expected
- 1.3 Pre-operation notification procedure - Step-by-step process
  - 1.3.1 Identify affected agents - Who needs to know
  - 1.3.2 Compose notification - What to tell them
  - 1.3.3 Send notification - Using the agent-messaging skill
  - 1.3.4 Track acknowledgments - Monitor responses
  - 1.3.5 Handle timeouts - When agents don't respond
- 1.4 Notification message format - Standard message structure
- 1.5 Priority levels - When to use each priority
- 1.6 Examples - Pre-operation scenarios
- 1.7 Troubleshooting - Notification delivery issues

---

## 1.1 What are pre-operation notifications

Pre-operation notifications are warning messages sent to agents before performing operations that will affect them. The purpose is to:

1. Inform agents about upcoming disruption
2. Give agents time to save their current work
3. Allow agents to reach a safe stopping point
4. Request acknowledgment before proceeding
5. Establish a coordination protocol for multi-agent systems

Pre-operation notifications are the first step in the notification protocol flow. They are always sent before any operation that will interrupt, restart, or modify an agent.

---

## 1.2 When to send pre-operation notifications

### 1.2.1 Skill installation

**Trigger:** Installing a skill on an agent requires the agent to be hibernated and woken.

**Impact on agent:**
- Agent will be hibernated (context preserved)
- Agent will be woken with new skill available
- Agent may need to reload context
- Brief interruption (typically 30 seconds)

**Notification required:** Yes, with acknowledgment request.

**Message content should include:**
- Name of skill being installed
- Expected downtime duration
- Request to finish current work
- Request for "ok" acknowledgment

### 1.2.2 Plugin installation

**Trigger:** Installing a plugin on an agent requires a full agent restart.

**Impact on agent:**
- Agent session will be terminated
- Agent will be restarted with plugin enabled
- Agent context will be lost (unless checkpointed)
- Longer interruption (typically 60-90 seconds)

**Notification required:** Yes, with acknowledgment request.

**Message content should include:**
- Name of plugin being installed
- Warning about context loss
- Request to checkpoint current work
- Request for "ok" acknowledgment

### 1.2.3 Configuration changes

**Trigger:** Changing agent configuration that requires agent awareness.

**Impact on agent:**
- Settings will change
- Behavior may be affected
- May require acknowledgment of new settings

**Notification required:** Yes, acknowledgment optional.

**Message content should include:**
- What configuration is changing
- How behavior will be affected
- Any actions agent needs to take

### 1.2.4 System maintenance

**Trigger:** Scheduled or emergency maintenance affecting multiple agents.

**Impact on agent:**
- Temporary service disruption
- Possible hibernation of all agents
- System-wide effects

**Notification required:** Yes (broadcast), with acknowledgment request.

**Message content should include:**
- Maintenance window start time
- Expected duration
- Services affected
- Request for "ok" acknowledgment

---

## 1.3 Pre-operation notification procedure

### 1.3.1 Identify affected agents

**Purpose:** Determine which agents need to receive the notification.

**Steps:**
1. Identify the operation being performed
2. Determine which agents the operation affects
3. Use the `ai-maestro-agents-management` skill to list all agents and check their status (only notify RUNNING agents)
4. Build list of target agents by filtering for relevant agents (by role, project, or name pattern)

### 1.3.2 Compose notification

**Purpose:** Create a clear, informative notification message.

**Required elements:**
1. Subject line indicating operation type
2. Clear description of what will happen
3. Expected impact and duration
4. Request for acknowledgment (if required)
5. Deadline for response

**Message fields:**
- **Subject**: "[Operation Type] Pending"
- **Priority**: `high`
- **Content**: type `pre-operation`, message describing the operation and requesting "ok" acknowledgment. Include fields: `operation` (the operation type), `expected_downtime` (duration string), `requires_acknowledgment` (true or false).

### 1.3.3 Send notification

**Purpose:** Deliver the notification using the `agent-messaging` skill.

Use the `agent-messaging` skill to send the pre-operation notification:
- **Recipient**: the target agent session name
- **Subject**: "[Operation Type] Pending"
- **Priority**: `high`
- **Content**: type `pre-operation`, message: "I will [operation description]. This requires [impact description]. Please [action required] and reply with 'ok' when ready. I will wait up to 2 minutes." Include fields: `operation`, `expected_downtime`, `requires_acknowledgment` (true).

Capture the message ID from the response for tracking.

### 1.3.4 Track acknowledgments

**Purpose:** Monitor for agent responses to the notification.

Use the `agent-messaging` skill to periodically check for unread messages from the target agent. Poll every 10 seconds.

Look for messages from the target agent with type `acknowledgment` containing "ok".

If no response after 30 seconds, 60 seconds, and 90 seconds, send reminder messages (see [acknowledgment-protocol.md](acknowledgment-protocol.md) for reminder details).

### 1.3.5 Handle timeouts

**Purpose:** Define behavior when agents do not respond within the timeout period.

**Timeout handling rules:**
1. Send reminders at 30s, 60s, 90s
2. After 2 minutes, proceed with operation
3. Log the timeout occurrence
4. Send timeout notice to agent
5. Include timeout in operation report

Use the `agent-messaging` skill to send a timeout notice:
- **Recipient**: the target agent session name
- **Subject**: `Proceeding Without Acknowledgment`
- **Priority**: `high`
- **Content**: type `timeout-notice`, message: "No response received after 2 minutes. Proceeding with [operation] now." Include fields: `operation`, `timeout_occurred` (true).

---

## 1.4 Notification message format

**Standard pre-operation message fields:**

| Field | Required | Description |
|-------|----------|-------------|
| Recipient | Yes | Target agent session name |
| Subject | Yes | "[Operation Type] Pending" |
| Priority | Yes | `high`, `normal`, `low`, or `critical` |
| Content type | Yes | `pre-operation` |
| Content message | Yes | Human-readable description of operation and request |
| Content operation | Yes | Operation type: `skill-install`, `plugin-install`, `config-change`, `maintenance` |
| Content operation_details | No | Additional context (skill_name, plugin_name, etc.) |
| Content expected_downtime | Yes | Duration string: "30 seconds", "1 minute", "5 minutes" |
| Content requires_acknowledgment | Yes | true or false |
| Content acknowledgment_timeout | No | Timeout in seconds (default 120) |

---

## 1.5 Priority levels

| Priority | When to use | Example |
|----------|-------------|---------|
| `critical` | Immediate action required, system at risk | Emergency maintenance |
| `high` | Important, agent should respond promptly | Skill installation |
| `normal` | Standard notification, no urgency | Configuration update |
| `low` | Informational only | Scheduled maintenance notice |

**Priority selection rules:**
1. Use `high` for all disruptive operations requiring acknowledgment
2. Use `critical` only for emergency situations
3. Use `normal` for non-disruptive configuration changes
4. Use `low` for advance notices (more than 1 hour ahead)

---

## 1.6 Examples

### Example 1: Skill Installation Pre-Operation

Use the `agent-messaging` skill to send a pre-operation notification:
- **Recipient**: `code-impl-auth`
- **Subject**: `Skill Installation Pending`
- **Priority**: `high`
- **Content**: type `pre-operation`, message: "I will install the security-audit skill on your agent. This requires hibernating you for approximately 30 seconds. Please finish your current work and reply with 'ok' when ready. I will wait up to 2 minutes." Include fields: `operation`: "skill-install", `operation_details`: { `skill_name`: "security-audit", `skill_version`: "1.0.0" }, `expected_downtime`: "30 seconds", `requires_acknowledgment`: true, `acknowledgment_timeout`: 120.

### Example 2: Plugin Installation Pre-Operation

Use the `agent-messaging` skill to send:
- **Recipient**: `test-engineer-01`
- **Subject**: `Plugin Installation Pending`
- **Priority**: `high`
- **Content**: type `pre-operation`, message: "I will install the test-framework-integration plugin. This requires a full restart of your agent. Your current context will NOT be preserved. Please checkpoint any important work and reply with 'ok' when ready. I will wait up to 2 minutes." Include fields: `operation`: "plugin-install", `operation_details`: { `plugin_name`: "test-framework-integration", `plugin_version`: "2.1.0" }, `expected_downtime`: "90 seconds", `requires_acknowledgment`: true, `acknowledgment_timeout`: 120.

### Example 3: Broadcast Maintenance Pre-Operation

For each agent in the team (`code-impl-auth`, `test-engineer-01`, `docs-writer`, `devops-ci`), use the `agent-messaging` skill to send:
- **Recipient**: the agent session name
- **Subject**: `System Maintenance Scheduled`
- **Priority**: `high`
- **Content**: type `pre-operation`, message: "System maintenance will begin in 5 minutes. All agents will be hibernated for approximately 10 minutes while database migrations run. Please save your work and reply with 'ok' when ready." Include fields: `operation`: "maintenance", `operation_details`: { `maintenance_type`: "database-migration", `maintenance_window`: "10 minutes" }, `expected_downtime`: "10 minutes", `requires_acknowledgment`: true, `broadcast_id`: a unique ID for tracking this broadcast, `total_recipients`: the number of agents being notified.

---

## 1.7 Troubleshooting

### Issue: Notification not delivered

**Symptoms:** Agent reports no message received, message not in agent inbox.

**Resolution:**
1. Use the `ai-maestro-agents-management` skill to check if AI Maestro is running and healthy
2. Verify agent name is correct and the agent is online
3. Check the messaging skill response for errors
4. Review AI Maestro logs for delivery failures
5. Retry with correct agent session name

### Issue: Wrong agent receives notification

**Symptoms:** Unrelated agent responds, intended agent unaware.

**Resolution:**
1. Verify agent session name matches exactly
2. Check for agent name collisions
3. Use full session name (domain-subdomain-name)
4. Confirm agent list before sending

### Issue: Notification sent but acknowledgment not tracked

**Symptoms:** Agent responded but system shows timeout.

**Resolution:**
1. Check polling interval (should be 10 seconds)
2. Verify response message format matches expected
3. Check for typos in agent name in filter
4. Use the `agent-messaging` skill to manually check inbox for the response
5. Review message query filters

### Issue: Priority not respected

**Symptoms:** High-priority message not appearing prominently.

**Resolution:**
1. Verify priority field is set correctly in the message
2. Check AI Maestro configuration for priority handling
3. Ensure agent has notifications enabled
4. Consider using subject line prefix like "[URGENT]"
