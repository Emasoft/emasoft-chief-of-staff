---
procedure: support-skill
workflow-instruction: support
operation: check-system-resources
parent-skill: ecos-resource-monitoring
---

# Operation: Check System Resources


## Contents

- [Purpose](#purpose)
- [When To Use This Operation](#when-to-use-this-operation)
- [Steps](#steps)
  - [Step 1: Check CPU Usage](#step-1-check-cpu-usage)
  - [Step 2: Check Memory Availability](#step-2-check-memory-availability)
  - [Step 3: Check Disk Space](#step-3-check-disk-space)
  - [Step 4: Check Network Connectivity](#step-4-check-network-connectivity)
  - [Step 5: Report Findings](#step-5-report-findings)
- [System Resource Check](#system-resource-check)
- [Checklist](#checklist)
- [Output](#output)
- [Automated Script](#automated-script)
- [Related References](#related-references)
- [Next Operation](#next-operation)

## Purpose

Monitor CPU, memory, disk, and network resources that affect agent operations.

## When To Use This Operation

- Regularly (every 15 minutes)
- Before spawning new agents
- When performance issues are reported
- When agents report slowdowns
- During capacity planning

## Steps

### Step 1: Check CPU Usage

```bash
# macOS
cpu_usage=$(top -l 1 | grep "CPU usage" | awk '{print $3}' | sed 's/%//')

# Linux
cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | sed 's/%//')

echo "CPU Usage: ${cpu_usage}%"
```

**Thresholds:**
- Normal: < 70%
- Warning: 70-85%
- Critical: > 85%

### Step 2: Check Memory Availability

```bash
# macOS
mem_free=$(vm_stat | grep "Pages free" | awk '{print $3}' | sed 's/\.//')
mem_free_mb=$((mem_free * 4096 / 1024 / 1024))

# Linux
mem_free_mb=$(free -m | awk '/^Mem:/{print $4}')

echo "Memory Free: ${mem_free_mb}MB"
```

**Thresholds:**
- Normal: > 2GB free
- Warning: 1-2GB free
- Critical: < 1GB free

### Step 3: Check Disk Space

```bash
# Check root filesystem
disk_free=$(df -h / | tail -1 | awk '{print $4}')
disk_percent=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')

echo "Disk Free: ${disk_free} (${disk_percent}% used)"
```

**Thresholds:**
- Normal: < 70% used
- Warning: 70-85% used
- Critical: > 85% used

### Step 4: Check Network Connectivity

```bash
# Check AI Maestro connectivity
aimaestro_status=$(check_aimaestro_health)  # Use ai-maestro-agents-management skill to check health

if [ "$aimaestro_status" = "200" ]; then
  echo "AI Maestro: Connected"
else
  echo "AI Maestro: Disconnected (HTTP $aimaestro_status)"
fi
```

### Step 5: Report Findings

```markdown
## System Resource Check
Timestamp: [ISO8601]

| Resource | Value | Status |
|----------|-------|--------|
| CPU | [X]% | [normal/warning/critical] |
| Memory Free | [X]MB | [normal/warning/critical] |
| Disk Used | [X]% | [normal/warning/critical] |
| Network | [connected/disconnected] | [normal/critical] |

Actions Taken: [if any]
```

## Checklist

Copy this checklist and track your progress:

- [ ] CPU usage checked
- [ ] Memory availability checked
- [ ] Disk space checked
- [ ] Network connectivity verified
- [ ] Findings documented
- [ ] Alerts triggered if thresholds exceeded
- [ ] Report saved to monitoring log

## Output

After completing this operation:
- Current resource state documented
- Alerts triggered if needed
- Ready to proceed with agent operations

## Automated Script

```bash
#!/bin/bash
# System resource check script

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# CPU
cpu=$(top -l 1 | grep "CPU usage" | awk '{print $3}' | sed 's/%//')

# Memory
mem_free_mb=$(vm_stat | grep "Pages free" | awk '{print $3}' | sed 's/\.//')
mem_free_mb=$((mem_free_mb * 4096 / 1024 / 1024))

# Disk
disk_percent=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')

# AI Maestro
aimaestro=$(check_aimaestro_health 2>/dev/null || echo "000")  # Use ai-maestro-agents-management skill

echo "{\"timestamp\": \"$TIMESTAMP\", \"cpu\": $cpu, \"memory_free_mb\": $mem_free_mb, \"disk_percent\": $disk_percent, \"aimaestro\": $aimaestro}"
```

## Related References

- [system-resources.md](system-resources.md) - Complete resource monitoring guide
- [resource-alerts.md](resource-alerts.md) - Alert handling
- [monitoring-commands.md](monitoring-commands.md) - Command reference

## Next Operation

If thresholds exceeded: [op-handle-resource-alert.md](op-handle-resource-alert.md)
