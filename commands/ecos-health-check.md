---
name: ecos-health-check
description: "Check health status of agents including heartbeat, responsiveness, and resource usage"
argument-hint: "[--agent <NAME>] [--all] [--verbose] [--format table|json]"
allowed-tools: ["Bash", "Task"]
user-invocable: true
---

# Health Check Command

Check the health status of one or more agents managed by AI Maestro, including last heartbeat, responsiveness, and resource usage.

## Usage

Use the `ai-maestro-agents-management` skill to check agent health with the provided arguments.

## What This Command Does

This command checks agent health. The operation queries:
1. Agent registry for heartbeat timestamps
2. tmux session status for online/offline/hibernated detection
3. System metrics for resource usage (CPU, memory)
4. Agent responsiveness via ping mechanism

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--agent <name>` | No | Check specific agent by name |
| `--all` | No | Check all registered agents (default if no agent specified) |
| `--verbose` | No | Show detailed health metrics |
| `--format <format>` | No | Output format: `table` (default), `json` |
| `--timeout <seconds>` | No | Ping timeout in seconds (default: 5) |

## Examples

```bash
# Check all agents (default)
/ecos-health-check

# Check specific agent
/ecos-health-check --agent helper-python

# Verbose output for all agents
/ecos-health-check --all --verbose

# JSON output for scripting
/ecos-health-check --format json

# Check with custom timeout
/ecos-health-check --agent helper-api --timeout 10
```

## Health Check Workflow

1. **Query Agent Registry**: Fetch agent metadata from AI Maestro API
2. **Check tmux Session**: Verify session exists and is responsive
3. **Check Heartbeat**: Compare last heartbeat timestamp against threshold
4. **Measure Response Time**: Send ping message and measure response latency
5. **Gather Resource Usage**: Query system metrics (if available)

## Output Format (Table)

```
┌────────────────────┬──────────┬───────────────────┬──────────────┬────────────┐
│ Agent              │ Status   │ Last Heartbeat    │ Response (ms)│ Health     │
├────────────────────┼──────────┼───────────────────┼──────────────┼────────────┤
│ backend-api        │ online   │ 2 seconds ago     │ 45           │ HEALTHY    │
│ frontend-dev       │ online   │ 15 seconds ago    │ 120          │ HEALTHY    │
│ test-runner        │ offline  │ 5 minutes ago     │ -            │ OFFLINE    │
│ data-processor     │ hibernated│ N/A              │ -            │ HIBERNATED │
│ slow-agent         │ online   │ 90 seconds ago    │ timeout      │ DEGRADED   │
└────────────────────┴──────────┴───────────────────┴──────────────┴────────────┘
```

## Verbose Output

With `--verbose` flag, additional metrics are shown:

```
═══════════════════════════════════════════════════════════════
  Health Check: backend-api
═══════════════════════════════════════════════════════════════

  Status:           online
  Health:           HEALTHY

  Heartbeat:
    Last:           2024-01-15 10:30:45 UTC
    Age:            2 seconds ago
    Threshold:      60 seconds

  Response:
    Ping Latency:   45 ms
    Timeout:        5000 ms

  Resources:
    CPU:            12%
    Memory:         256 MB
    Session PID:    12345
    Working Dir:    /Users/dev/projects/backend

═══════════════════════════════════════════════════════════════
```

## Health Status Values

| Health Status | Description | Criteria |
|---------------|-------------|----------|
| `HEALTHY` | Agent is functioning normally | Online, recent heartbeat, responsive |
| `DEGRADED` | Agent has issues but is running | Online but slow response or stale heartbeat |
| `OFFLINE` | Agent session is not running | tmux session not found |
| `HIBERNATED` | Agent is explicitly hibernated | Marked as hibernated in registry |
| `UNRESPONSIVE` | Agent is not responding | Online but fails to respond to ping |
| `UNKNOWN` | Cannot determine health | Agent not found or API error |

## Thresholds

| Metric | Healthy | Degraded | Critical |
|--------|---------|----------|----------|
| Heartbeat Age | < 60s | 60s - 300s | > 300s |
| Response Time | < 200ms | 200ms - 1000ms | > 1000ms or timeout |
| CPU Usage | < 70% | 70% - 90% | > 90% |
| Memory | < 80% | 80% - 95% | > 95% |

## JSON Output

```json
{
  "timestamp": "2024-01-15T10:30:47Z",
  "agents": [
    {
      "name": "backend-api",
      "status": "online",
      "health": "HEALTHY",
      "lastHeartbeat": "2024-01-15T10:30:45Z",
      "heartbeatAge": 2,
      "responseMs": 45,
      "resources": {
        "cpu": 12,
        "memory": 256,
        "pid": 12345
      },
      "workingDir": "/Users/dev/projects/backend"
    }
  ],
  "summary": {
    "total": 4,
    "healthy": 2,
    "degraded": 1,
    "offline": 1,
    "hibernated": 0
  }
}
```

## Programmatic Access

For programmatic health checks, use the `ai-maestro-agents-management` skill to query agent health status for a specific agent or all agents.

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Agent not found" | Agent not registered | Check agent name with `/ecos-staff-status` |
| "API unreachable" | AI Maestro not running | Start AI Maestro service |
| "Ping timeout" | Agent unresponsive | Consider `/ecos-recovery-workflow` |

## Related Commands

- `/ecos-staff-status` - View all remote agents
- `/ecos-recovery-workflow` - Execute recovery for unhealthy agent
- `/ecos-replace-agent` - Replace failed agent
- `/ecos-hibernate-agent` - Put an agent to sleep

## CLI Reference

Full documentation: `ai-maestro-agents-management` skill
