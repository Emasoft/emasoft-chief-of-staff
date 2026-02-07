---
procedure: support-skill
workflow-instruction: support
operation: detect-config-changes
parent-skill: ecos-session-memory-library
---

# Operation: Detect Config Changes During Session

## Purpose

Detect when configuration files have changed during a session to identify drift and trigger conflict resolution if needed.

## When To Use This Operation

- Periodically during long sessions (every 30 minutes)
- After config change notifications
- Before major tasks
- When unexpected behavior occurs

## Steps

### Step 1: Read Current Config Files

```bash
CONFIG_DIR="$CLAUDE_PROJECT_DIR/design/config"
SNAPSHOT_FILE="$CLAUDE_PROJECT_DIR/design/memory/config-snapshot.md"
```

### Step 2: Compare Timestamps

For each config file in snapshot:

```bash
# Get snapshot timestamp from file
snapshot_time="[from snapshot]"

# Get current file timestamp
current_time=$(stat -f "%Sm" -t "%Y-%m-%dT%H:%M:%SZ" "$CONFIG_DIR/file.yaml")

if [ "$current_time" != "$snapshot_time" ]; then
  echo "CONFIG CHANGED: file.yaml"
fi
```

### Step 3: Perform Content Comparison (if timestamps differ)

```bash
# Calculate current hash
current_hash=$(md5 -q "$CONFIG_DIR/file.yaml")

# Compare with snapshot hash
if [ "$current_hash" != "$snapshot_hash" ]; then
  echo "CONTENT CHANGED: file.yaml"
fi
```

### Step 4: Identify Changed Sections

If content changed:
- Diff the current file against snapshot
- Identify specific sections changed
- Classify change type

```markdown
## Config Change Detected

File: team-config.yaml
Previous: [timestamp]
Current: [timestamp]

### Changed Sections
- `coding_standards`: strict -> relaxed
- `team_size`: 5 -> 6
```

### Step 5: Log in activeContext.md

```markdown
## Session Notes
- [ISO8601] Config drift detected: team-config.yaml
- Changes: coding_standards, team_size
- Action: [pending conflict resolution]
```

### Step 6: Trigger Conflict Resolution if Critical

For critical changes, proceed to [op-handle-config-conflicts.md](op-handle-config-conflicts.md)

## Change Classification

| Type | Examples | Action |
|------|----------|--------|
| Non-critical | Comments, formatting | Log only |
| Notable | Team size, thresholds | Log, notify |
| Critical | Security, auth config | Pause, resolve |
| Breaking | API versions, protocols | Stop, escalate |

## Detection Methods

### Method 1: Timestamp-Based (Fast)

```bash
# Compare modification times
for file in $(cat "$SNAPSHOT_FILE" | grep "Path:" | cut -d' ' -f2); do
  snapshot_mtime="[from snapshot]"
  current_mtime=$(stat -f "%m" "$file")
  if [ "$current_mtime" -gt "$snapshot_mtime" ]; then
    echo "MODIFIED: $file"
  fi
done
```

### Method 2: Hash-Based (Accurate)

```bash
# Compare content hashes
for file in $(cat "$SNAPSHOT_FILE" | grep "Path:" | cut -d' ' -f2); do
  snapshot_hash="[from snapshot]"
  current_hash=$(md5 -q "$file")
  if [ "$current_hash" != "$snapshot_hash" ]; then
    echo "CHANGED: $file"
  fi
done
```

## Checklist

Copy this checklist and track your progress:

- [ ] Snapshot file located
- [ ] Current config files accessed
- [ ] Timestamps compared
- [ ] Content compared (if timestamps differ)
- [ ] Changes identified and classified
- [ ] Changes logged in activeContext.md
- [ ] Conflict resolution triggered (if critical)
- [ ] Snapshot "Last Verified" updated

## Periodic Check Schedule

| Session Duration | Check Interval |
|------------------|----------------|
| < 1 hour | End of session |
| 1-4 hours | Every 30 minutes |
| > 4 hours | Every 15 minutes |

## Output

After completing this operation:
- Drift detected and classified (or confirmed no drift)
- Changes logged
- Conflict resolution triggered if needed
- Snapshot verification timestamp updated

## Related References

- [20-config-change-detection.md](20-config-change-detection.md) - Complete detection guide
- [21-config-conflict-resolution.md](21-config-conflict-resolution.md) - Conflict resolution

## Next Operation

If changes detected: [op-handle-config-conflicts.md](op-handle-config-conflicts.md)
