---
name: ecos-install-skill-notify
description: "Install skill with full notification protocol: notify, wait for ok, install, verify"
argument-hint: "--agent <name> | --global --skill <name> | --marketplace <marketplace>/<skill> [--wait-for-ok]"
allowed-tools: ["Bash(aimaestro-agent.sh:*)", "Task"]
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

## Skill Integration

This command combines two skills:
1. **`agent-messaging` skill** - For notifications and acknowledgments
2. **`ai-maestro-agents-management` skill** - For plugin/skill installation

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

This command executes a 4-phase workflow:

**Phase 1: Pre-installation Notification**
- If `--global`, use the `ai-maestro-agents-management` skill to list all agents
- For each target agent, send a notification using the `agent-messaging` skill:
  - **Recipient**: the target agent
  - **Subject**: `[SKILL INSTALL] <skill-id>`
  - **Content**: "Skill installation starting. Your session will hibernate -> install -> wake. Please finish current work and reply 'ok' when ready."
  - **Priority**: `high`

**Phase 2: Wait for Acknowledgment (if --wait-for-ok)**
- For each agent, use the `agent-messaging` skill to poll for acknowledgment messages (timeout: 120s)
- Send reminder messages every 30 seconds using the `agent-messaging` skill
- If timeout reached, proceed with warning

**Phase 3: Installation**
- Use the `ai-maestro-agents-management` skill to install the plugin on the target agent (or globally)
- This automatically handles hibernate -> install -> wake cycle

**Phase 4: Post-installation Verification**
- For each agent, send a verification notification using the `agent-messaging` skill:
  - **Subject**: `[VERIFY] Skill installed: <skill-id>`
  - **Content**: "Skill installation complete. Please verify the skill is active and working correctly."

**Verify**: all phases complete successfully, agents acknowledge and verify skill activation.

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
