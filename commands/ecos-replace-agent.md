---
name: ecos-replace-agent
description: "Replace a failed or terminated agent with a new one, including manager approval, handoff generation, and kanban update"
argument-hint: "--failed-agent <NAME> --new-name <NAME> --role <ROLE> --project <PROJECT> --dir <PATH>"
allowed-tools: ["Bash(aimaestro-agent.sh:*)", "Read", "Task"]
user-invocable: true
---

# Replace Agent Command

Replace a failed, terminated, or unhealthy agent with a new one. This command orchestrates a full replacement workflow including approval, handoff generation, and work transfer.

## Usage

```!
# This is an orchestrated workflow command
# Execute the replacement workflow with the provided arguments
```

## Replacement Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    REPLACEMENT WORKFLOW                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. REQUEST APPROVAL                                        │
│     └─> Send request to EAMA (Assistant Manager)            │
│     └─> Wait for approval/rejection                         │
│                                                             │
│  2. CREATE NEW AGENT (if approved)                          │
│     └─> Run aimaestro-agent.sh create                       │
│     └─> Configure same role/project as failed agent         │
│                                                             │
│  3. GENERATE HANDOFF                                        │
│     └─> Request EOA (Orchestrator) to create handoff docs   │
│     └─> Include: task state, context, pending work          │
│                                                             │
│  4. UPDATE KANBAN                                           │
│     └─> Request EOA to update GitHub Project board          │
│     └─> Reassign cards from old agent to new agent          │
│                                                             │
│  5. TRANSFER HANDOFF                                        │
│     └─> Send handoff documents to new agent                 │
│     └─> Verify new agent received and acknowledged          │
│                                                             │
│  6. VERIFY READY                                            │
│     └─> Health check on new agent                           │
│     └─> Confirm new agent is operational                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--failed-agent <name>` | Yes | Name of the agent being replaced |
| `--new-name <name>` | Yes | Name for the new replacement agent |
| `--role <role>` | Yes | Role for the new agent (e.g., implementer, tester, documenter) |
| `--project <project>` | Yes | Project name/identifier the agent works on |
| `--dir <path>` | Yes | Working directory path for the new agent |
| `--reason <text>` | No | Reason for replacement (shown in approval request) |
| `--skip-approval` | No | Skip manager approval (use with caution) |
| `--skip-kanban` | No | Skip GitHub Project kanban update |
| `--force` | No | Force replacement even if failed agent is still online |

## Examples

```bash
# Replace a crashed backend agent
/ecos-replace-agent \
  --failed-agent helper-backend \
  --new-name helper-backend-v2 \
  --role implementer \
  --project myapp-api \
  --dir ~/projects/myapp \
  --reason "Agent became unresponsive after memory exhaustion"

# Replace with skip approval (for urgent cases)
/ecos-replace-agent \
  --failed-agent test-runner \
  --new-name test-runner-new \
  --role tester \
  --project myapp-tests \
  --dir ~/projects/tests \
  --skip-approval

# Force replacement of online but degraded agent
/ecos-replace-agent \
  --failed-agent slow-processor \
  --new-name fast-processor \
  --role worker \
  --project data-pipeline \
  --dir ~/projects/data \
  --force \
  --reason "Performance degradation below acceptable threshold"
```

## Workflow Steps in Detail

### Step 1: Request Approval from EAMA

Send an approval request to the EAMA using the `agent-messaging` skill:
- **Recipient**: `eama-assistant-manager`
- **Subject**: `[APPROVAL REQUEST] Replace Agent: <failed-agent>`
- **Content**: approval request with failed agent details, new agent name, role, project, and reason
- **Priority**: `high`

**Verify**: approval response received from EAMA.

### Step 2: Create New Agent

After approval, use the `ai-maestro-agents-management` skill to create a new agent:
- **Name**: the new agent name (e.g., `helper-backend-v2`)
- **Directory**: the project working directory
- **Task**: "Continue work from <failed-agent>"
- **Tags**: role, project, and `replacement` tag
- **Program args**: include standard Claude Code flags

**Verify**: the new agent appears in the agent list with "online" status.

### Step 3: Request Handoff from EOA

Send a handoff generation request to EOA using the `agent-messaging` skill:
- **Recipient**: `eoa-orchestrator`
- **Subject**: `[HANDOFF REQUEST] Generate handoff for <failed-agent> replacement`
- **Content**: request to generate handoff documentation including failed and new agent names
- **Priority**: `high`

**Verify**: EOA responds with handoff document location.

### Step 4: Update GitHub Project Kanban

Send a kanban update request to EOA using the `agent-messaging` skill:
- **Recipient**: `eoa-orchestrator`
- **Subject**: `[KANBAN UPDATE] Reassign cards from <old-agent> to <new-agent>`
- **Content**: request to reassign all kanban cards
- **Priority**: `normal`

**Verify**: EOA confirms cards have been reassigned.

### Step 5: Transfer Handoff to New Agent

Send the handoff documentation to the new agent using the `agent-messaging` skill:
- **Recipient**: the new agent
- **Subject**: `[HANDOFF] Work transfer from <failed-agent>`
- **Content**: handoff document with instructions to review and continue work
- **Priority**: `urgent`

**Verify**: new agent acknowledges receipt of handoff.

### Step 6: Verify New Agent Ready

Use the `ai-maestro-agents-management` skill to check health of the new agent:
- **Agent**: the new agent name
- **Mode**: verbose health check

**Verify**: health check reports "HEALTHY" with acceptable response time.

## Output Format

```
═══════════════════════════════════════════════════════════════
  Agent Replacement: helper-backend -> helper-backend-v2
═══════════════════════════════════════════════════════════════

  Step 1: Request Approval
    ✓ Sent approval request to eama-assistant-manager
    ✓ Approval received (approved by: user)

  Step 2: Create New Agent
    ✓ Agent helper-backend-v2 created
    ✓ Working directory: /Users/dev/projects/myapp
    ✓ tmux session: helper-backend-v2

  Step 3: Generate Handoff
    ✓ Handoff request sent to eoa-orchestrator
    ✓ Handoff generated: /tmp/handoffs/helper-backend-20240115.md

  Step 4: Update Kanban
    ✓ Kanban update request sent to eoa-orchestrator
    ✓ 3 cards reassigned to helper-backend-v2

  Step 5: Transfer Handoff
    ✓ Handoff sent to helper-backend-v2
    ✓ Acknowledgment received

  Step 6: Verify Ready
    ✓ Health check: HEALTHY
    ✓ Response time: 45ms

═══════════════════════════════════════════════════════════════
  REPLACEMENT COMPLETE
  New agent 'helper-backend-v2' is ready and working
═══════════════════════════════════════════════════════════════
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Approval rejected" | Manager denied replacement | Review reason, adjust request |
| "Failed agent still online" | Agent is running | Use `--force` flag if intended |
| "New agent name exists" | Duplicate name | Choose different name |
| "Handoff generation failed" | EOA error | Check EOA status, retry |
| "Kanban update failed" | GitHub API error | Use `--skip-kanban`, update manually |

## Related Commands

- `/ecos-health-check` - Check agent health before replacement
- `/ecos-recovery-workflow` - Try recovery before replacement
- `/ecos-transfer-work` - Transfer work without full replacement
- `/ecos-terminate-agent` - Terminate the failed agent after replacement
- `/ecos-spawn-agent` - Create agent without replacement workflow

## CLI Reference

Full documentation: `ai-maestro-agents-management` skill
