---
procedure: support-skill
workflow-instruction: support
operation: capture-config-snapshot
parent-skill: ecos-session-memory-library
---

# Operation: Capture Config Snapshot at Session Start

## Purpose

Capture configuration state at session start to detect drift and maintain consistency throughout the session.

## When To Use This Operation

- During session initialization (after loading core memory files)
- Before any work begins
- When config files are known to have changed

## Config Snapshot Purpose

The config snapshot:
- Detects drift during long sessions
- Maintains consistency
- Enables conflict resolution
- Supports audit trails

**Location:** `design/memory/config-snapshot.md`

## Steps

### Step 1: Identify Config Files

Config files may be in:
- `design/config/` (if EOA plugin installed)
- Project root configuration files
- Environment-specific settings

```bash
CONFIG_DIR="$CLAUDE_PROJECT_DIR/design/config"
if [ -d "$CONFIG_DIR" ]; then
  ls -la "$CONFIG_DIR"
fi
```

### Step 2: Create Snapshot Header

```markdown
# Config Snapshot

Session ID: [session-id]
Created: [ISO8601]
Last Verified: [ISO8601]

## Source Files
| File | Modified | Hash |
|------|----------|------|
| [file1] | [timestamp] | [hash] |
| [file2] | [timestamp] | [hash] |
```

### Step 3: Copy Config Content

For each config file, capture:

```markdown
## [Config File Name]

**Path:** [full path]
**Modified:** [file modification timestamp]
**Hash:** [MD5 or SHA256 of content]

### Content
```yaml
[YAML/JSON/TOML content of the config file]
```
```

### Step 4: Calculate File Hashes

```bash
# Calculate hash for each config file
for file in "$CONFIG_DIR"/*; do
  hash=$(md5 -q "$file" 2>/dev/null || md5sum "$file" | cut -d' ' -f1)
  echo "$file: $hash"
done
```

### Step 5: Save Snapshot

```bash
SNAPSHOT_FILE="$CLAUDE_PROJECT_DIR/design/memory/config-snapshot.md"
# Write snapshot content
```

### Step 6: Record in activeContext.md

Add to activeContext.md:

```markdown
## Session Notes
- Config snapshot captured at [ISO8601]
- Source files: [count]
- Snapshot location: design/memory/config-snapshot.md
```

## Checklist

Copy this checklist and track your progress:

- [ ] Config directory identified
- [ ] Config files listed
- [ ] Snapshot header created
- [ ] File timestamps recorded
- [ ] File hashes calculated
- [ ] Content copied to snapshot
- [ ] Snapshot saved to config-snapshot.md
- [ ] activeContext.md updated

## Snapshot Structure

```markdown
# Config Snapshot

Session ID: session-20250205-1
Created: 2025-02-05T08:00:00Z
Last Verified: 2025-02-05T08:00:00Z

## Source Files
| File | Modified | Hash |
|------|----------|------|
| team-config.yaml | 2025-02-04T10:00:00Z | abc123... |
| project-rules.md | 2025-02-03T14:30:00Z | def456... |

## team-config.yaml

**Path:** design/config/team-config.yaml
**Modified:** 2025-02-04T10:00:00Z
**Hash:** abc123...

### Content
```yaml
project: my-project
team_size: 5
coding_standards: strict
```

## project-rules.md

**Path:** design/config/project-rules.md
**Modified:** 2025-02-03T14:30:00Z
**Hash:** def456...

### Content
[content of file]
```

## Output

After completing this operation:
- Config snapshot created
- File hashes recorded for change detection
- Ready to detect drift during session

## Related References

- [19-config-snapshot-creation.md](19-config-snapshot-creation.md) - Complete snapshot guide
- [20-config-change-detection.md](20-config-change-detection.md) - Change detection

## Next Operation

During session: [op-detect-config-changes.md](op-detect-config-changes.md) (periodically)
