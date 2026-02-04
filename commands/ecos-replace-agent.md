---
name: ecos-replace-agent
description: "Replace a failed or terminated agent with a new one, including manager approval, handoff generation, and kanban update"
argument-hint: "--failed-agent <NAME> --new-name <NAME> --role <ROLE> --project <PROJECT> --dir <PATH>"
allowed-tools: ["Bash(aimaestro-agent.sh:*)", "Bash(curl:*)", "Read", "Task"]
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

The command sends an approval request to the EAMA (Emasoft Assistant Manager Agent):

```bash
# Internal: Send approval request via AI Maestro API
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "eama-assistant-manager",
    "subject": "[APPROVAL REQUEST] Replace Agent: helper-backend",
    "priority": "high",
    "content": {
      "type": "approval_request",
      "action": "replace_agent",
      "failed_agent": "helper-backend",
      "new_agent": "helper-backend-v2",
      "role": "implementer",
      "project": "myapp-api",
      "reason": "Agent became unresponsive",
      "message": "Requesting approval to replace failed agent"
    }
  }'
```

### Step 2: Create New Agent

After approval, creates the new agent using the AI Maestro CLI:

```bash
# Internal: Create new agent
aimaestro-agent.sh create helper-backend-v2 \
  --dir ~/projects/myapp \
  --task "Continue work from helper-backend" \
  --tags "implementer,myapp-api,replacement" \
  -- continue --dangerously-skip-permissions --chrome --add-dir /tmp
```

### Step 3: Request Handoff from EOA

Request the EOA (Emasoft Orchestrator Agent) to generate handoff documentation:

```bash
# Internal: Request handoff generation
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "eoa-orchestrator",
    "subject": "[HANDOFF REQUEST] Generate handoff for helper-backend replacement",
    "priority": "high",
    "content": {
      "type": "request",
      "action": "generate_handoff",
      "failed_agent": "helper-backend",
      "new_agent": "helper-backend-v2",
      "message": "Please generate handoff documentation for agent replacement"
    }
  }'
```

### Step 4: Update GitHub Project Kanban

Request EOA to update the GitHub Project board:

```bash
# Internal: Request kanban update
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "eoa-orchestrator",
    "subject": "[KANBAN UPDATE] Reassign cards from helper-backend to helper-backend-v2",
    "priority": "normal",
    "content": {
      "type": "request",
      "action": "update_kanban",
      "old_agent": "helper-backend",
      "new_agent": "helper-backend-v2",
      "message": "Reassign all kanban cards from old agent to new agent"
    }
  }'
```

### Step 5: Transfer Handoff to New Agent

Send the handoff documentation to the new agent:

```bash
# Internal: Send handoff to new agent
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "helper-backend-v2",
    "subject": "[HANDOFF] Work transfer from helper-backend",
    "priority": "urgent",
    "content": {
      "type": "handoff",
      "from_agent": "helper-backend",
      "handoff_file": "/path/to/handoff.md",
      "message": "You are replacing helper-backend. Please review the handoff and continue the work."
    }
  }'
```

### Step 6: Verify New Agent Ready

Health check and verification:

```bash
# Internal: Verify new agent
aimaestro-agent.sh health --agent helper-backend-v2 --verbose
```

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
