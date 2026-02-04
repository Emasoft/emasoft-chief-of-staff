---
name: ecos-install-skill-notify
description: "Install skill with full notification protocol: notify, wait for ok, install, verify"
argument-hint: "--agent <name> | --global --skill <name> | --marketplace <marketplace>/<skill> [--wait-for-ok]"
allowed-tools: ["Bash(aimaestro-agent.sh:*)", "Bash(curl:*)"]
user-invocable: true
---

# Install Skill with Notification Protocol

Install a skill to an agent (or globally) with a complete notification workflow: notify the agent about upcoming hibernation/wake cycle, wait for acknowledgment, perform installation, then verify skill activation.

## Usage

```!
# Full notification protocol for skill installation
# Arguments: $ARGUMENTS

# Target (choose one):
# --agent <name>                Install to specific agent
# --global                      Install globally (all agents)

# Skill source (choose one):
# --skill <name>                Local skill name
# --marketplace <mkt>/<skill>   Skill from marketplace

# Options:
# --wait-for-ok                 Wait for agent acknowledgment before proceeding
```

## AI Maestro CLI & API Integration

This command combines:
1. **AI Maestro Messaging API** - For notifications and acknowledgments
2. **aimaestro-agent.sh CLI** - For plugin/skill installation

**API Endpoint**: `http://localhost:23000/api/messages`
**CLI Tool**: `aimaestro-agent.sh plugin install`

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--agent <name>` | Yes* | Target agent for skill installation |
| `--global` | Yes* | Install skill globally (all agents) |
| `--skill <name>` | Yes** | Local skill name |
| `--marketplace <mkt/skill>` | Yes** | Marketplace skill (format: `marketplace-name/skill-name`) |
| `--wait-for-ok` | No | Wait for agent acknowledgment before proceeding (up to 2 minutes) |

*One of `--agent` or `--global` is required.
**One of `--skill` or `--marketplace` is required.

## Complete Installation Workflow

```
================================================================================
                    SKILL INSTALLATION PROTOCOL
================================================================================

Phase 1: PRE-INSTALLATION NOTIFICATION
----------------------------------------
1. Send notification to agent about upcoming install
2. Inform agent: will hibernate -> install -> wake
3. Request agent to finish current work

Phase 2: ACKNOWLEDGMENT (if --wait-for-ok)
----------------------------------------
4. Wait for agent to send "ok" message
5. Send reminders every 30 seconds
6. Timeout after 120 seconds (proceed with warning)

Phase 3: INSTALLATION
----------------------------------------
7. Execute: aimaestro-agent.sh plugin install <agent> <skill>
   (This automatically: hibernates -> installs -> wakes)

Phase 4: POST-INSTALLATION VERIFICATION
----------------------------------------
8. Send notification to agent to verify skill
9. Agent should confirm skill is active

================================================================================
```

## Examples

```bash
# Install skill to specific agent with wait
/ecos-install-skill-notify --agent helper-python --skill data-validation --wait-for-ok

# Install marketplace skill without waiting
/ecos-install-skill-notify --agent frontend-ui --marketplace emasoft-plugins/perfect-skill-suggester

# Global installation with wait
/ecos-install-skill-notify --global --marketplace emasoft-plugins/code-quality --wait-for-ok

# Quick install (no wait)
/ecos-install-skill-notify --agent data-processor --skill formatting-tools
```

## Implementation

Execute the full workflow:

```bash
#!/bin/bash
# Full skill installation with notification protocol

API_BASE="http://localhost:23000"
SELF_AGENT="${SESSION_NAME:-orchestrator}"
TARGET_AGENT=""
GLOBAL=false
SKILL=""
MARKETPLACE_SKILL=""
WAIT_FOR_OK=false
TIMEOUT=120
REMIND_INTERVAL=30

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --agent) TARGET_AGENT="$2"; shift 2 ;;
    --global) GLOBAL=true; shift ;;
    --skill) SKILL="$2"; shift 2 ;;
    --marketplace) MARKETPLACE_SKILL="$2"; shift 2 ;;
    --wait-for-ok) WAIT_FOR_OK=true; shift ;;
    *) shift ;;
  esac
done

# Determine skill identifier
if [ -n "$MARKETPLACE_SKILL" ]; then
  SKILL_ID="$MARKETPLACE_SKILL"
else
  SKILL_ID="$SKILL"
fi

echo "========================================"
echo "  SKILL INSTALLATION PROTOCOL"
echo "========================================"
echo ""

# Phase 1: Pre-installation notification
echo "Phase 1: Pre-installation Notification"
echo "---------------------------------------"

if [ "$GLOBAL" = true ]; then
  # Get all agents
  AGENTS=$(curl -s "${API_BASE}/api/agents" | jq -r '.agents[].session_name')
else
  AGENTS="$TARGET_AGENT"
fi

for agent in $AGENTS; do
  echo "Notifying: $agent"
  curl -s -X POST "${API_BASE}/api/messages" \
    -H "Content-Type: application/json" \
    -d "{
      \"to\": \"$agent\",
      \"subject\": \"[SKILL INSTALL] $SKILL_ID\",
      \"priority\": \"high\",
      \"content\": {
        \"type\": \"notification\",
        \"operation\": \"skill-install\",
        \"skill\": \"$SKILL_ID\",
        \"message\": \"Skill installation starting. Your session will hibernate -> install -> wake. Please finish current work and reply 'ok' when ready.\"
      }
    }"
  echo " - Notification sent"
done

# Phase 2: Wait for acknowledgment (if --wait-for-ok)
if [ "$WAIT_FOR_OK" = true ]; then
  echo ""
  echo "Phase 2: Waiting for Acknowledgment"
  echo "------------------------------------"

  for agent in $AGENTS; do
    echo "Waiting for: $agent (timeout: ${TIMEOUT}s)"

    start_time=$(date +%s)
    last_remind=$start_time
    ack_received=false

    while true; do
      current_time=$(date +%s)
      elapsed=$((current_time - start_time))

      # Check timeout
      if [ $elapsed -ge $TIMEOUT ]; then
        echo "  [WARNING] Timeout waiting for $agent - proceeding anyway"
        break
      fi

      # Poll for acknowledgment
      ack=$(curl -s "${API_BASE}/api/messages?agent=${SELF_AGENT}&action=list&status=unread" | \
        jq -r ".messages[] | select(.from == \"$agent\" and .content.status == \"ready\") | .content.status" | head -1)

      if [ "$ack" = "ready" ]; then
        echo "  [OK] Agent $agent acknowledged (${elapsed}s)"
        ack_received=true
        break
      fi

      # Send reminder
      time_since_remind=$((current_time - last_remind))
      if [ $time_since_remind -ge $REMIND_INTERVAL ]; then
        echo "  [REMINDER] Sending reminder to $agent (${elapsed}s elapsed)"
        curl -s -X POST "${API_BASE}/api/messages" \
          -H "Content-Type: application/json" \
          -d "{
            \"to\": \"$agent\",
            \"subject\": \"[REMINDER] Skill install waiting\",
            \"priority\": \"high\",
            \"content\": {
              \"type\": \"reminder\",
              \"message\": \"Waiting for your acknowledgment. Please save work and reply 'ok'. (${elapsed}s of ${TIMEOUT}s)\"
            }
          }"
        last_remind=$current_time
      fi

      sleep 5
    done
  done
fi

# Phase 3: Installation
echo ""
echo "Phase 3: Installation"
echo "---------------------"

if [ "$GLOBAL" = true ]; then
  echo "Installing globally..."
  aimaestro-agent.sh plugin install --global "$SKILL_ID"
else
  echo "Installing to: $TARGET_AGENT"
  aimaestro-agent.sh plugin install "$TARGET_AGENT" "$SKILL_ID"
fi

echo "Installation complete"

# Phase 4: Post-installation verification notification
echo ""
echo "Phase 4: Verification Notification"
echo "-----------------------------------"

for agent in $AGENTS; do
  echo "Notifying: $agent"
  curl -s -X POST "${API_BASE}/api/messages" \
    -H "Content-Type: application/json" \
    -d "{
      \"to\": \"$agent\",
      \"subject\": \"[VERIFY] Skill installed: $SKILL_ID\",
      \"priority\": \"normal\",
      \"content\": {
        \"type\": \"notification\",
        \"operation\": \"verify-skill\",
        \"skill\": \"$SKILL_ID\",
        \"message\": \"Skill installation complete. Please verify the skill is active and working correctly.\"
      }
    }"
  echo " - Verification request sent"
done

echo ""
echo "========================================"
echo "  INSTALLATION PROTOCOL COMPLETE"
echo "========================================"
```

## Output Format

```
========================================
  SKILL INSTALLATION PROTOCOL
========================================

Phase 1: Pre-installation Notification
---------------------------------------
Notifying: helper-python
 - Notification sent

Phase 2: Waiting for Acknowledgment
------------------------------------
Waiting for: helper-python (timeout: 120s)
  [REMINDER] Sending reminder to helper-python (30s elapsed)
  [OK] Agent helper-python acknowledged (42s)

Phase 3: Installation
---------------------
Installing to: helper-python
  - Hibernating agent...
  - Installing skill: data-validation
  - Waking agent...
Installation complete

Phase 4: Verification Notification
-----------------------------------
Notifying: helper-python
 - Verification request sent

========================================
  INSTALLATION PROTOCOL COMPLETE
========================================
```

## Agent Acknowledgment Format

Agents should respond with:

```json
{
  "to": "<orchestrator>",
  "subject": "ACK: Ready for skill install",
  "content": {
    "type": "ack",
    "status": "ready",
    "message": "Work saved, ready for hibernation"
  }
}
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Agent not found" | Invalid agent name | Check with `/ecos-staff-status` |
| "Skill not found" | Invalid skill name | Verify skill exists |
| "Marketplace not found" | Invalid marketplace | Check marketplace name |
| "Installation failed" | CLI error | Check CLI output |
| "Timeout waiting for ack" | Agent busy | Proceeded with warning |

## Without --wait-for-ok

If `--wait-for-ok` is not specified:
- Notification is sent but workflow proceeds immediately
- Agent may be interrupted mid-task
- Use for non-critical skill installations
- Agent receives verification request after wake

## Global Installation Notes

When using `--global`:
- All registered agents receive notification
- Each agent's acknowledgment is tracked separately
- Installation applies to global scope
- All agents receive verification notification

## Related Commands

- `/ecos-notify-agents` - Send notifications without installation
- `/ecos-wait-for-agent-ok` - Wait for single acknowledgment
- `/ecos-broadcast-notification` - Broadcast messages
- `/ecos-staff-status` - Check agent status
- `/ecos-hibernate-agent` - Hibernate without install
- `/ecos-wake-agent` - Wake without install
