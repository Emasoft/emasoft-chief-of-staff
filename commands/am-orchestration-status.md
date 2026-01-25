---
name: am-orchestration-status
description: "View Orchestration Phase progress - modules, agents, assignments, verification status"
argument-hint: "[--verbose] [--agents-only] [--modules-only]"
allowed-tools: ["Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/am_orchestration_status.py:*)"]
---

# Orchestration Status Command

View the current status of Orchestration Phase including module progress, agent assignments, and verification status.

## Usage

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/am_orchestration_status.py" $ARGUMENTS
```

## What This Command Shows

1. **Phase Status**: Current orchestration state
2. **Module Progress**: Completion status of each module
3. **Agent Registry**: Registered AI and human agents
4. **Active Assignments**: Current module-agent mappings
5. **Instruction Verification**: Status of understanding confirmation
6. **Progress Polling**: Last poll times and issue reports
7. **Verification Loops**: PR verification countdown

## Output Format

```
╔════════════════════════════════════════════════════════════════╗
║                 ORCHESTRATION PHASE STATUS                     ║
╠════════════════════════════════════════════════════════════════╣
║ Plan ID: plan-20260108-143022                                  ║
║ Status: executing                                              ║
║ Progress: 1/3 modules complete (33%)                           ║
╠════════════════════════════════════════════════════════════════╣
║ MODULE STATUS                                                  ║
╠════════════════════════════════════════════════════════════════╣
║ [✓] auth-core      #42  implementer-1  complete                ║
║ [→] oauth-google   #43  implementer-2  in_progress (Poll: 5m)  ║
║ [ ] auth-2fa       #44  -              pending                 ║
╠════════════════════════════════════════════════════════════════╣
║ REGISTERED AGENTS                                              ║
╠════════════════════════════════════════════════════════════════╣
║ AI Agents:                                                     ║
║   - implementer-1 (helper-agent-generic)                       ║
║   - implementer-2 (helper-agent-python)                        ║
║ Human Developers:                                              ║
║   - dev-alice (GitHub)                                         ║
╠════════════════════════════════════════════════════════════════╣
║ ACTIVE ASSIGNMENTS                                             ║
╠════════════════════════════════════════════════════════════════╣
║ oauth-google → implementer-2                                   ║
║   Status: working                                              ║
║   Instruction Verification: ✓ verified                         ║
║   Last Poll: 5 minutes ago                                     ║
║   Issues Reported: 0                                           ║
║   Next Poll Due: 10 minutes                                    ║
╚════════════════════════════════════════════════════════════════╝
```

## Options

| Option | Description |
|--------|-------------|
| `--verbose` | Show detailed polling history and criteria |
| `--agents-only` | Show only agent information |
| `--modules-only` | Show only module status |

## Key Metrics

- **Modules Completed**: X/Y (percentage)
- **Active Assignments**: Currently working agents
- **Verification Status**: Pre-implementation confirmation
- **Poll Compliance**: Time since last progress check
- **Issues Reported**: Problems raised during polling

## Related Commands

- `/start-orchestration` - Begin orchestration
- `/assign-module` - Assign module to agent
- `/check-agents` - Poll all active agents
- `/register-agent` - Register new agent
