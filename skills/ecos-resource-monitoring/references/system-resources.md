# System Resources Reference

## Table of Contents

- 1.1 [Types Of System Resources](#11-types-of-system-resources)
- 1.2 [Monitoring CPU Usage](#12-monitoring-cpu-usage)
- 1.3 [Monitoring Memory](#13-monitoring-memory)
- 1.4 [Monitoring Disk Space](#14-monitoring-disk-space)
- 1.5 [Monitoring Network](#15-monitoring-network)
- 1.6 [Resource Thresholds](#16-resource-thresholds)
- 1.7 [System Resource Examples](#17-system-resource-examples)
- 1.8 [Troubleshooting](#18-troubleshooting)

---

## 1.1 Types Of System Resources

System resources are the underlying compute capacity that agents depend on.

### CPU

Central Processing Unit capacity affects:
- Agent response time
- Tool execution speed
- Concurrent operations

**Metrics:**
- Usage percentage (0-100%)
- Load average (1, 5, 15 minute)
- Per-process consumption

### Memory

Random Access Memory affects:
- Number of agents that can run
- Context window sizes
- Data processing capacity

**Metrics:**
- Total memory
- Used memory
- Available memory
- Swap usage

### Disk

Storage capacity affects:
- Log file growth
- Session memory persistence
- Artifact storage

**Metrics:**
- Total space
- Used space
- Available space
- Inode usage

### Network

Network connectivity affects:
- AI Maestro communication
- External API calls
- Message delivery latency

**Metrics:**
- Connectivity status
- Latency to key endpoints
- Bandwidth utilization

---

## 1.2 Monitoring CPU Usage

### Basic CPU Check

```bash
# macOS: Get CPU usage percentage
cpu_usage=$(top -l 1 | grep "CPU usage" | awk '{print $3}' | tr -d '%')
echo "CPU usage: ${cpu_usage}%"

# Linux: Get CPU usage
cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | tr -d '%id,')
echo "CPU usage: ${cpu_usage}%"
```

### Load Average Check

```bash
# Get 1, 5, 15 minute load averages
load=$(uptime | awk -F'load average:' '{print $2}')
echo "Load average: $load"

# Parse individual values
load_1=$(echo $load | cut -d',' -f1 | tr -d ' ')
load_5=$(echo $load | cut -d',' -f2 | tr -d ' ')
load_15=$(echo $load | cut -d',' -f3 | tr -d ' ')
```

### CPU-Intensive Process Detection

```bash
# Find top CPU consumers
ps aux --sort=-%cpu | head -10

# Find processes using more than 50% CPU
ps aux | awk '$3 > 50 {print $0}'
```

### CPU Health Assessment

```markdown
## CPU Health Levels

| Load Average (vs cores) | Status | Action |
|------------------------|--------|--------|
| < 0.7 per core | Healthy | Normal operations |
| 0.7-1.0 per core | Elevated | Monitor closely |
| 1.0-2.0 per core | High | Reduce concurrency |
| > 2.0 per core | Critical | Pause new agents |
```

---

## 1.3 Monitoring Memory

### Basic Memory Check

```bash
# macOS: Get memory statistics
vm_stat | head -10

# Calculate free memory in MB (macOS)
pages_free=$(vm_stat | grep "Pages free" | awk '{print $3}' | tr -d '.')
mem_free_mb=$((pages_free * 4096 / 1024 / 1024))
echo "Free memory: ${mem_free_mb}MB"

# Linux: Get memory info
free -m
mem_free_mb=$(free -m | awk '/^Mem:/ {print $4}')
echo "Free memory: ${mem_free_mb}MB"
```

### Memory Percentage Calculation

```bash
# macOS
total_mem=$(sysctl -n hw.memsize)
total_mem_mb=$((total_mem / 1024 / 1024))
used_mem_mb=$((total_mem_mb - mem_free_mb))
mem_percent=$((used_mem_mb * 100 / total_mem_mb))
echo "Memory usage: ${mem_percent}%"

# Linux
mem_percent=$(free | awk '/^Mem:/ {printf("%.0f", $3/$2 * 100)}')
echo "Memory usage: ${mem_percent}%"
```

### Per-Process Memory

```bash
# Top memory consumers
ps aux --sort=-%mem | head -10

# Memory used by Claude Code processes
ps aux | grep -i claude | awk '{sum += $6} END {print sum/1024 " MB"}'
```

### Memory Health Assessment

```markdown
## Memory Health Levels

| Usage Percentage | Status | Action |
|-----------------|--------|--------|
| < 60% | Healthy | Normal operations |
| 60-75% | Elevated | Prepare for compaction |
| 75-85% | High | Request compactions |
| 85-95% | Critical | Stop new agents, force compaction |
| > 95% | Emergency | Terminate non-essential agents |
```

---

## 1.4 Monitoring Disk Space

### Basic Disk Check

```bash
# Check disk space on all mounted filesystems
df -h

# Check specific mount point
df -h / | tail -1

# Get free space in GB
disk_free=$(df -h / | tail -1 | awk '{print $4}')
echo "Free disk space: $disk_free"
```

### Disk Usage Percentage

```bash
# Get usage percentage
disk_percent=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
echo "Disk usage: ${disk_percent}%"
```

### Large File Detection

```bash
# Find files larger than 100MB
find /Users -size +100M -type f 2>/dev/null | head -20

# Find large log files
find /var/log -size +50M -type f 2>/dev/null
find ~/.claude -name "*.log" -size +10M 2>/dev/null
```

### Inode Usage

```bash
# Check inode usage (many small files can exhaust inodes)
df -i / | tail -1
```

### Disk Health Assessment

```markdown
## Disk Health Levels

| Usage Percentage | Status | Action |
|-----------------|--------|--------|
| < 70% | Healthy | Normal operations |
| 70-80% | Elevated | Plan cleanup |
| 80-90% | High | Execute cleanup |
| 90-95% | Critical | Emergency cleanup |
| > 95% | Emergency | Stop writes, urgent cleanup |
```

---

## 1.5 Monitoring Network

### Connectivity Check

```bash
# Check internet connectivity
ping -c 3 8.8.8.8 > /dev/null 2>&1 && echo "Internet: OK" || echo "Internet: FAILED"

# Check AI Maestro connectivity
curl -s http://localhost:23000/health > /dev/null && echo "AI Maestro: OK" || echo "AI Maestro: FAILED"

# Check DNS resolution
nslookup api.anthropic.com > /dev/null 2>&1 && echo "DNS: OK" || echo "DNS: FAILED"
```

### Latency Check

```bash
# Measure latency to key endpoints
ping -c 5 api.anthropic.com | tail -1 | awk -F'/' '{print "API latency: " $5 "ms"}'

# AI Maestro latency
time_ms=$(curl -s -w "%{time_total}" -o /dev/null http://localhost:23000/health)
echo "AI Maestro latency: ${time_ms}s"
```

### Port Availability

```bash
# Check if key ports are listening
lsof -i :23000 > /dev/null && echo "Port 23000: OPEN" || echo "Port 23000: CLOSED"
```

### Network Health Assessment

```markdown
## Network Health Levels

| Condition | Status | Action |
|-----------|--------|--------|
| All endpoints reachable, <100ms latency | Healthy | Normal operations |
| Some latency, <500ms | Elevated | Monitor |
| High latency, >500ms | Degraded | Reduce API calls |
| Intermittent connectivity | Critical | Pause remote operations |
| No connectivity | Emergency | Alert user, pause coordination |
```

---

## 1.6 Resource Thresholds

### Recommended Thresholds

| Resource | Warning | Critical | Emergency |
|----------|---------|----------|-----------|
| CPU (load/core) | 0.7 | 1.0 | 2.0 |
| Memory | 70% | 85% | 95% |
| Disk | 75% | 90% | 95% |
| Network Latency | 200ms | 500ms | 1000ms |

### Threshold Configuration

Store thresholds in configuration:

```markdown
# design/memory/resource-thresholds.md

## Resource Thresholds

Last Updated: 2025-02-01

### CPU
- Warning: 0.7 load per core
- Critical: 1.0 load per core
- Emergency: 2.0 load per core

### Memory
- Warning: 70%
- Critical: 85%
- Emergency: 95%

### Disk
- Warning: 75%
- Critical: 90%
- Emergency: 95%

### Network (latency)
- Warning: 200ms
- Critical: 500ms
- Emergency: 1000ms
```

### Dynamic Threshold Adjustment

Thresholds may need adjustment based on:
- Number of active agents (more agents = lower thresholds)
- Time of day (peak hours = lower thresholds)
- Current workload (critical work = lower thresholds)

---

## 1.7 System Resource Examples

### Example: Complete Resource Check Script

```bash
#!/bin/bash
# check-resources.sh

echo "=== System Resource Check ==="
echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

# CPU
echo "--- CPU ---"
load=$(uptime | awk -F'load average:' '{print $2}' | tr -d ' ')
echo "Load average: $load"

# Memory
echo "--- Memory ---"
if [[ "$OSTYPE" == "darwin"* ]]; then
  pages_free=$(vm_stat | grep "Pages free" | awk '{print $3}' | tr -d '.')
  mem_free_mb=$((pages_free * 4096 / 1024 / 1024))
  total_mem=$(($(sysctl -n hw.memsize) / 1024 / 1024))
  mem_used=$((total_mem - mem_free_mb))
  mem_percent=$((mem_used * 100 / total_mem))
else
  mem_percent=$(free | awk '/^Mem:/ {printf("%.0f", $3/$2 * 100)}')
fi
echo "Memory usage: ${mem_percent}%"

# Disk
echo "--- Disk ---"
disk_percent=$(df / | tail -1 | awk '{print $5}')
disk_free=$(df -h / | tail -1 | awk '{print $4}')
echo "Disk usage: $disk_percent (Free: $disk_free)"

# Network
echo "--- Network ---"
curl -s http://localhost:23000/health > /dev/null && echo "AI Maestro: OK" || echo "AI Maestro: FAILED"

echo ""
echo "=== Check Complete ==="
```

### Example: Resource Alert Generation

```bash
#!/bin/bash
# generate-resource-alert.sh

resource=$1
current_value=$2
threshold=$3
severity=$4

cat << EOF
# Resource Alert

**Timestamp:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Resource:** $resource
**Current Value:** $current_value
**Threshold:** $threshold
**Severity:** $severity

## Recommended Actions

$(case $resource in
  "memory")
    echo "1. Request context compaction from agents"
    echo "2. Pause new agent spawning"
    echo "3. Identify memory-heavy processes"
    ;;
  "disk")
    echo "1. Clean up log files"
    echo "2. Archive old session memories"
    echo "3. Remove temporary files"
    ;;
  "cpu")
    echo "1. Reduce agent concurrency"
    echo "2. Pause non-critical tasks"
    echo "3. Identify CPU-heavy processes"
    ;;
esac)
EOF
```

---

## 1.8 Troubleshooting

### Issue: Resource commands not working

**Symptoms:** Commands return errors, missing utilities.

**Possible causes:**
- Different OS than expected
- Missing system utilities
- Insufficient permissions

**Resolution:**
1. Check OS type: `uname -s`
2. Use OS-appropriate commands
3. Verify utility availability: `which top vm_stat df`
4. Request elevated permissions if needed

### Issue: Memory metrics seem incorrect

**Symptoms:** Reported memory does not match observed behavior.

**Possible causes:**
- Cached memory counted as used
- Swap included/excluded inconsistently
- Different measurement methods

**Resolution:**
1. Understand what "available" means vs "free"
2. Check if swap is being used
3. Use consistent measurement method
4. Compare with Activity Monitor/htop for validation

### Issue: Disk space not freed after deletion

**Symptoms:** Files deleted but space not recovered.

**Possible causes:**
- Files still open by processes
- Trash not emptied
- Hard links remaining

**Resolution:**
1. Check for open file handles: `lsof +D /path`
2. Empty trash if applicable
3. Force filesystem sync
4. Restart processes holding files

### Issue: Network checks pass but communication fails

**Symptoms:** Ping works but API calls fail.

**Possible causes:**
- Firewall blocking specific ports
- DNS issues for specific domains
- TLS/SSL problems
- Proxy configuration

**Resolution:**
1. Test specific port: `nc -zv host port`
2. Check DNS: `nslookup domain`
3. Test with curl verbose: `curl -v url`
4. Check proxy settings

---

**Version:** 1.0
**Last Updated:** 2025-02-01
