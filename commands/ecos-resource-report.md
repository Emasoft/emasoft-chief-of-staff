---
name: ecos-resource-report
description: "Generate system resource report with CPU, memory, disk, and active agents"
argument-hint: "[--format text|json] [--include-history]"
user-invocable: true
allowed-tools: ["Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/ecos_resource_monitor.py:*)"]
---

# Resource Report Command

Generate a comprehensive system resource report showing CPU usage, memory consumption, disk space, and active AI Maestro agents.

## Usage

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ecos_resource_monitor.py" $ARGUMENTS
```

## What This Command Does

1. **Collects System Metrics**
   - CPU usage (per-core and aggregate)
   - Memory usage (used, available, cached)
   - Disk usage for key directories
   - System load averages

2. **Queries Active Agents**
   - Lists all registered agents in AI Maestro
   - Shows agent status (active, idle, offline)
   - Reports agent resource consumption if available
   - Counts pending messages per agent

3. **Analyzes Resource Trends** (with `--include-history`)
   - CPU trend over last hour
   - Memory trend over last hour
   - Disk growth rate

4. **Generates Resource Warnings**
   - High CPU usage alerts (>80%)
   - Low memory warnings (<20% available)
   - Low disk space alerts (<10% free)
   - Agent overload warnings

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--format` | No | Output format: `text` (default) or `json` |
| `--include-history` | No | Include historical trends (last hour) |
| `--verbose` | No | Show detailed per-process information |
| `--watch SECONDS` | No | Continuously update every N seconds |

## Examples

### Generate basic resource report

```bash
/ecos-resource-report
```

### Get JSON output for automation

```bash
/ecos-resource-report --format json
```

### Include historical trends

```bash
/ecos-resource-report --include-history
```

### Watch mode (update every 5 seconds)

```bash
/ecos-resource-report --watch 5
```

## Output Example

```
╔════════════════════════════════════════════════════════════════╗
║                    SYSTEM RESOURCE REPORT                      ║
║                    2026-02-01 11:05:32 UTC                     ║
╠════════════════════════════════════════════════════════════════╣
║ CPU USAGE                                                      ║
╠════════════════════════════════════════════════════════════════╣
║ Aggregate: 42.3%                                               ║
║ Core 0: 38.1%  Core 1: 45.2%  Core 2: 41.8%  Core 3: 44.1%     ║
║ Core 4: 39.5%  Core 5: 48.3%  Core 6: 40.2%  Core 7: 42.6%     ║
║ Load Average: 3.21 / 2.85 / 2.64 (1m / 5m / 15m)               ║
╠════════════════════════════════════════════════════════════════╣
║ MEMORY                                                         ║
╠════════════════════════════════════════════════════════════════╣
║ Total: 32.0 GB                                                 ║
║ Used: 18.4 GB (57.5%)                                          ║
║ Available: 13.6 GB (42.5%)                                     ║
║ Cached: 8.2 GB                                                 ║
║ Swap: 2.1 GB / 8.0 GB (26.3%)                                  ║
╠════════════════════════════════════════════════════════════════╣
║ DISK USAGE                                                     ║
╠════════════════════════════════════════════════════════════════╣
║ Path                    │ Used    │ Free    │ Total   │ %      ║
║─────────────────────────────────────────────────────────────── ║
║ /                       │ 245 GB  │ 211 GB  │ 456 GB  │ 53.7%  ║
║ /Users                  │ 180 GB  │ 211 GB  │ 456 GB  │ 39.5%  ║
║ ~/.claude               │ 1.2 GB  │ 211 GB  │ 456 GB  │ 0.3%   ║
╠════════════════════════════════════════════════════════════════╣
║ AI MAESTRO AGENTS                                              ║
╠════════════════════════════════════════════════════════════════╣
║ Agent Name              │ Status  │ Messages │ Last Active     ║
║─────────────────────────────────────────────────────────────── ║
║ orchestrator-master     │ ACTIVE  │ 3        │ 2 min ago       ║
║ libs-svg-svgbbox        │ ACTIVE  │ 0        │ 15 min ago      ║
║ helper-agent-generic    │ IDLE    │ 0        │ 1 hour ago      ║
║ claude-skills-factory   │ ACTIVE  │ 1        │ just now        ║
╠════════════════════════════════════════════════════════════════╣
║ SUMMARY                                                        ║
╠════════════════════════════════════════════════════════════════╣
║ Total Agents: 4 | Active: 3 | Idle: 1 | Offline: 0             ║
║ Total Pending Messages: 4                                      ║
╠════════════════════════════════════════════════════════════════╣
║ WARNINGS                                                       ║
╠════════════════════════════════════════════════════════════════╣
║ (none)                                                         ║
╚════════════════════════════════════════════════════════════════╝
```

## Warning Thresholds

| Resource | Warning | Critical |
|----------|---------|----------|
| CPU | >80% sustained | >95% sustained |
| Memory | <20% available | <10% available |
| Disk | <10% free | <5% free |
| Swap | >50% used | >80% used |
| Agent Messages | >10 pending | >50 pending |

## JSON Output Format

```json
{
  "timestamp": "2026-02-01T11:05:32Z",
  "cpu": {
    "aggregate_percent": 42.3,
    "per_core": [38.1, 45.2, 41.8, 44.1, 39.5, 48.3, 40.2, 42.6],
    "load_average": {"1m": 3.21, "5m": 2.85, "15m": 2.64}
  },
  "memory": {
    "total_gb": 32.0,
    "used_gb": 18.4,
    "available_gb": 13.6,
    "percent_used": 57.5
  },
  "disk": [
    {"path": "/", "used_gb": 245, "free_gb": 211, "percent": 53.7}
  ],
  "agents": [
    {"name": "orchestrator-master", "status": "active", "pending_messages": 3}
  ],
  "warnings": []
}
```

## Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| "psutil not installed" | Python psutil missing | Install with `pip install psutil` |
| "AI Maestro unavailable" | API not running | Start AI Maestro service |
| "Permission denied" | Cannot read system metrics | Run with appropriate permissions |

## Prerequisites

- Python `psutil` package must be installed
- AI Maestro API must be running for agent information
- Appropriate permissions for reading system metrics

## Notes

- CPU usage is averaged over a 1-second sampling period
- Memory figures exclude OS-reserved memory
- Agent status is based on last heartbeat from AI Maestro
- Use `--watch` mode for continuous monitoring

## Related Commands

- `/ecos-performance-report` - Detailed agent performance metrics
- `/ecos-orchestration-status` - Orchestration-specific status
