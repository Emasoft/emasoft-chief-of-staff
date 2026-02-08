# Resource Monitoring Commands and Procedures

## Contents

- 1.1 Checking current system resource status before spawning agents
  - 1.1.1 CPU usage check command (macOS)
  - 1.1.2 Memory usage check command (macOS)
  - 1.1.3 Disk space check command (macOS)
  - 1.1.4 Counting active Claude Code instances
- 1.2 Executing the complete resource check procedure before agent spawn
  - 1.2.1 CPU threshold validation (80% limit)
  - 1.2.2 Memory threshold validation (2GB minimum free)
  - 1.2.3 Disk threshold validation (90% limit)
  - 1.2.4 Instance count validation (10 agent limit)
- 1.3 Configuring resource thresholds for spawn control
  - 1.3.1 Default threshold values
  - 1.3.2 Actions when thresholds are exceeded
- 1.4 Generating resource status reports
  - 1.4.1 Standard report format when resources are normal
  - 1.4.2 Critical report format when thresholds exceeded
  - 1.4.3 Command usage and output options
- 1.5 Implementing continuous resource monitoring
  - 1.5.1 60-second monitoring loop procedure
  - 1.5.2 Metrics logging location and format
  - 1.5.3 Spawn flag management based on resource state
- 1.6 Escalating alerts based on resource levels
  - 1.6.1 INFO level alerts (>50% usage)
  - 1.6.2 WARNING level alerts (>70% usage)
  - 1.6.3 CRITICAL level alerts (threshold exceeded)
  - 1.6.4 EMERGENCY level alerts (>95% usage)
- 1.7 Handling emergency resource situations
  - 1.7.1 High memory situation response (>90%)
  - 1.7.2 High CPU situation response (>90%)
  - 1.7.3 Low disk space situation response (<10% free)

---

## 1.1 Checking Current System Resource Status Before Spawning Agents

### 1.1.1 CPU Usage Check Command (macOS)

Get the current CPU usage percentage:

```bash
# macOS: Get CPU usage percentage
top -l 1 | grep "CPU usage" | awk '{print $3}' | sed 's/%//'
```

**Output**: Returns numeric percentage (e.g., `45`)

**Purpose**: Check if CPU is available for new agent work before spawning.

---

### 1.1.2 Memory Usage Check Command (macOS)

Get current memory statistics:

```bash
# macOS: Get physical memory usage summary
top -l 1 | grep PhysMem | awk '{print $2, $6}'
```

**Alternative method using vm_stat for free pages**:

```bash
# Get free pages count
vm_stat | grep "Pages free" | awk '{print $3}' | sed 's/\.//'
```

**Advanced method to calculate free memory in GB**:

```bash
# Get free memory in GB (includes speculative pages)
FREE_MEM=$(vm_stat | awk '/Pages free/ {free=$3} /Pages speculative/ {spec=$3} END {print (free+spec)*4096/1073741824}')
echo $FREE_MEM
```

**Output**: Returns free memory in GB (e.g., `8.2`)

**Purpose**: Ensure sufficient RAM is available before spawning new agents.

---

### 1.1.3 Disk Space Check Command (macOS)

Check root filesystem usage:

```bash
# Check root filesystem usage percentage
df -h / | tail -1 | awk '{print $5}' | sed 's/%//'
```

**Output**: Returns numeric percentage (e.g., `65`)

**Purpose**: Verify disk space is available for agent logs and cache files.

---

### 1.1.4 Counting Active Claude Code Instances

Count running Claude Code processes:

```bash
# Count running Claude Code processes
pgrep -f "claude" | wc -l | tr -d ' '
```

**Output**: Returns count of active instances (e.g., `4`)

**Purpose**: Track how many agents are already running to enforce the limit.

---

## 1.2 Executing the Complete Resource Check Procedure Before Agent Spawn

Execute this procedure **before any agent spawn** to determine if spawn should be allowed.

### 1.2.1 CPU Threshold Validation (80% Limit)

```bash
CPU_USAGE=$(top -l 1 | grep "CPU usage" | awk '{print $3}' | sed 's/%//')
if [ "$CPU_USAGE" -gt 80 ]; then
    echo "BLOCKED: CPU usage at ${CPU_USAGE}% exceeds 80% threshold"
    exit 1
fi
```

**Exit code 1**: CPU threshold exceeded - spawn blocked
**Exit code 0**: CPU within limits - continue checks

---

### 1.2.2 Memory Threshold Validation (2GB Minimum Free)

```bash
# Get free memory in GB
FREE_MEM=$(vm_stat | awk '/Pages free/ {free=$3} /Pages speculative/ {spec=$3} END {print (free+spec)*4096/1073741824}')
if (( $(echo "$FREE_MEM < 2.0" | bc -l) )); then
    echo "BLOCKED: Free memory ${FREE_MEM}GB below 2GB minimum"
    exit 1
fi
```

**Exit code 1**: Memory below minimum - spawn blocked
**Exit code 0**: Memory sufficient - continue checks

---

### 1.2.3 Disk Threshold Validation (90% Limit)

```bash
DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 90 ]; then
    echo "BLOCKED: Disk usage at ${DISK_USAGE}% exceeds 90% threshold"
    exit 1
fi
```

**Exit code 1**: Disk threshold exceeded - spawn blocked
**Exit code 0**: Disk within limits - continue checks

---

### 1.2.4 Instance Count Validation (10 Agent Limit)

```bash
INSTANCE_COUNT=$(pgrep -f "claude" | wc -l | tr -d ' ')
if [ "$INSTANCE_COUNT" -ge 10 ]; then
    echo "BLOCKED: ${INSTANCE_COUNT} Claude instances running, limit is 10"
    exit 1
fi
```

**Exit code 1**: Instance limit reached - spawn blocked
**Exit code 0**: Under limit - spawn allowed

---

## 1.3 Configuring Resource Thresholds for Spawn Control

### 1.3.1 Default Threshold Values

Default thresholds (configurable in `shared/thresholds.py`):

| Resource | Threshold | Description |
|----------|-----------|-------------|
| **max_concurrent_agents** | 10 | Maximum number of Claude Code instances allowed |
| **cpu_threshold_percent** | 80% | CPU usage percentage limit |
| **memory_threshold_percent** | 85% | Memory usage percentage limit |
| **disk_threshold_percent** | 90% | Disk usage percentage limit |

---

### 1.3.2 Actions When Thresholds Are Exceeded

| Resource Exceeds Threshold | Immediate Action | Additional Action |
|---------------------------|------------------|-------------------|
| **max_concurrent_agents** | Block new agent spawns | None |
| **cpu_threshold_percent** | Block new agent spawns | Send alert to Chief of Staff |
| **memory_threshold_percent** | Block new agent spawns | Send alert to Chief of Staff |
| **disk_threshold_percent** | Block new agent spawns | Send alert to Chief of Staff |

**Note**: All thresholds must be within limits for spawn to be allowed.

---

## 1.4 Generating Resource Status Reports

### 1.4.1 Standard Report Format When Resources Are Normal

When all resources within acceptable limits:

```
=== SYSTEM RESOURCE REPORT ===
Timestamp: 2025-02-01T11:00:00Z

CPU Usage:      45% [OK]
Memory Used:    12.5GB / 32GB (39%) [OK]
Memory Free:    19.5GB [OK]
Disk Usage:     65% of 500GB [OK]
Disk Free:      175GB [OK]

Claude Instances: 4 / 10 [OK]

Status: ALL_CLEAR - Ready for new agent spawns
```

**Status indicators**:
- `[OK]` - Within acceptable limits
- `Status: ALL_CLEAR` - New agents can be spawned

---

### 1.4.2 Critical Report Format When Thresholds Exceeded

When resources exceed thresholds:

```
=== SYSTEM RESOURCE REPORT ===
Timestamp: 2025-02-01T11:00:00Z

CPU Usage:      92% [CRITICAL]
Memory Used:    28GB / 32GB (87%) [WARNING]
Memory Free:    4GB [WARNING]
Disk Usage:     75% of 500GB [OK]
Disk Free:      125GB [OK]

Claude Instances: 8 / 10 [WARNING]

Status: SPAWN_BLOCKED - Cannot spawn new agents
Reasons:
  - CPU usage exceeds 80% threshold
  - Memory usage exceeds 85% threshold
  - Approaching instance limit (8/10)
```

**Status indicators**:
- `[WARNING]` - Near threshold (70-79%)
- `[CRITICAL]` - Threshold exceeded (≥80%)
- `Status: SPAWN_BLOCKED` - New agents cannot be spawned

---

### 1.4.3 Command Usage and Output Options

Generate resource report using the command:

```bash
# Standard human-readable report
/ecos-resource-report

# JSON output for programmatic use
/ecos-resource-report --json

# Verbose report with detailed process information
/ecos-resource-report --verbose
```

**Use cases**:
- **Standard**: Quick check of system status
- **--json**: Integration with monitoring tools or scripts
- **--verbose**: Debugging resource issues, includes per-process details

---

## 1.5 Implementing Continuous Resource Monitoring

### 1.5.1 60-Second Monitoring Loop Procedure

Run resource checks every 60 seconds following this procedure:

1. **Execute all resource checks** (CPU, Memory, Disk, Instance Count)
2. **Log metrics** to `~/.claude/metrics/resources/`
3. **If any threshold exceeded**:
   - Update `spawn_allowed` flag to `false`
   - Send alert to Chief of Staff via AI Maestro
4. **If all resources normal and spawn was blocked**:
   - Update `spawn_allowed` flag to `true`
   - Send recovery notification

**Loop structure**:
```bash
while true; do
    # Execute checks
    # Log results
    # Update spawn flag
    # Send notifications if needed
    sleep 60
done
```

---

### 1.5.2 Metrics Logging Location and Format

**Log directory**: `~/.claude/metrics/resources/`

**Log files**:
- `cpu_usage.log` - CPU percentage over time
- `memory_usage.log` - Memory statistics over time
- `disk_usage.log` - Disk usage over time
- `instance_count.log` - Claude Code instance counts over time

**Log format** (timestamp, value, status):
```
2025-02-01T11:00:00Z,45,OK
2025-02-01T11:01:00Z,82,EXCEEDED
2025-02-01T11:02:00Z,78,OK
```

---

### 1.5.3 Spawn Flag Management Based on Resource State

**Flag location**: In-memory state managed by Resource Monitor

**Flag states**:
- `spawn_allowed = true` - All resources within limits, new agents can spawn
- `spawn_allowed = false` - One or more resources exceeded, block spawns

**State transitions**:
- `true → false`: When **any** resource exceeds threshold
- `false → true`: When **all** resources return to normal

**Notifications**:
- Send alert to Chief of Staff using the `agent-messaging` skill when transitioning to `false`
- Send recovery notification using the `agent-messaging` skill when transitioning to `true`

---

## 1.6 Escalating Alerts Based on Resource Levels

### 1.6.1 INFO Level Alerts (>50% Usage)

**Condition**: Any resource exceeds 50% usage

**Action**: Log to metrics only (no notifications)

**Purpose**: Historical tracking, trend analysis

---

### 1.6.2 WARNING Level Alerts (>70% Usage)

**Condition**: Any resource exceeds 70% usage

**Actions**:
1. Log to metrics
2. Notify Chief of Staff via AI Maestro

**Purpose**: Early warning before threshold reached

---

### 1.6.3 CRITICAL Level Alerts (Threshold Exceeded)

**Condition**: Any resource exceeds configured threshold (80% CPU, 85% Memory, 90% Disk)

**Actions**:
1. Block new agent spawns
2. Alert all relevant agents via AI Maestro

**Purpose**: Prevent system overload

---

### 1.6.4 EMERGENCY Level Alerts (>95% Usage)

**Condition**: Disk >95% **OR** Memory >95%

**Actions**:
1. Block new agent spawns
2. Force hibernate non-essential agents
3. Send emergency alert to Chief of Staff and user

**Purpose**: Prevent system crash or data loss

---

## 1.7 Handling Emergency Resource Situations

### 1.7.1 High Memory Situation Response (>90%)

**Trigger**: Memory usage exceeds 90%

**Response procedure**:

1. **Identify non-essential agents** (not orchestrator, not actively running tasks)
2. **Send hibernate request** to least recently active agent via AI Maestro
3. **Wait 30 seconds** for graceful hibernation
4. **Re-check memory** after hibernation
5. **If memory still critical** (>90%), hibernate next agent
6. **Continue** until memory drops below 80%

**Hibernate message format**:
> **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.
```json
{
  "to": "agent-name",
  "subject": "EMERGENCY: Hibernate Required",
  "priority": "urgent",
  "content": {
    "type": "command",
    "message": "Memory critical (>90%). Save state and hibernate immediately."
  }
}
```

---

### 1.7.2 High CPU Situation Response (>90%)

**Trigger**: CPU usage exceeds 90%

**Response procedure**:

1. **Identify CPU-intensive agents** via process monitoring (`ps aux | grep claude`)
2. **Send throttle request** to busiest agent
3. **Monitor CPU** for 5 minutes
4. **If persists**, hibernate non-essential agents
5. **Report to Chief of Staff** for investigation

**Throttle message format**:
> **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.
```json
{
  "to": "agent-name",
  "subject": "CRITICAL: Throttle Required",
  "priority": "high",
  "content": {
    "type": "command",
    "message": "CPU critical (>90%). You are using 45.2% CPU. Reduce processing intensity."
  }
}
```

**Investigation needed**: Determine if workload is legitimate or if agent is stuck in loop.

---

### 1.7.3 Low Disk Space Situation Response (<10% Free)

**Trigger**: Disk free space drops below 10%

**Response procedure**:

1. **Identify largest log files** in `~/.claude/logs/`
   ```bash
   du -h ~/.claude/logs/* | sort -rh | head -20
   ```

2. **Archive old logs** to compressed storage
   ```bash
   tar -czf ~/.claude/logs/archive-$(date +%Y%m%d).tar.gz ~/.claude/logs/*.log
   rm ~/.claude/logs/*.log
   ```

3. **Clear safe cache directories**
   ```bash
   rm -rf ~/.claude/cache/temp/*
   rm -rf ~/.claude/plugins/cache/*/temp/*
   ```

4. **Report to user** for manual intervention (large files, package cleanup)

**Alert message to user**:
```
CRITICAL: Disk space below 10% (only XXX GB free)

Actions taken:
- Archived logs to ~/.claude/logs/archive-YYYYMMDD.tar.gz
- Cleared temp cache directories
- Freed ~X.X GB

Manual action required:
- Review large files in project directories
- Consider removing unused dependencies
- Move large datasets to external storage
```

---

## Summary

This document provides all commands, thresholds, and procedures for resource monitoring in the Emasoft Chief of Staff plugin. Use these procedures to:

- Check resources before spawning agents
- Monitor system health continuously
- Respond to resource emergencies
- Generate reports for users and other agents

**Key principle**: Always check resources before spawning. When thresholds are exceeded, block spawns and alert Chief of Staff.
