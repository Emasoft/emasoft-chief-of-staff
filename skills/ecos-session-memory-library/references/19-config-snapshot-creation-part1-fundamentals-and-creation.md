# Config Snapshot Creation - Part 1: Fundamentals and Creation

## Table of Contents

1. [When you need to understand the overview](#overview)
2. [Understanding config snapshots](#what-is-a-config-snapshot)
3. [Why snapshots matter](#why-snapshots-matter)
4. [How to create initial snapshots](#procedure-1-create-initial-snapshot)

**Related Parts:**
- [Part 2: Validation and Reference](./19-config-snapshot-creation-part2-validation-and-reference.md) - Updating, validating, structure, examples, troubleshooting

---

## Overview

### What Is a Config Snapshot?

A config snapshot is a point-in-time capture of all central configuration files (toolchain.md, standards.md, environment.md, decisions.md) stored in session memory. It preserves the config state when the session started to detect drift and manage version conflicts.

### When to Create Snapshots

**Create snapshot:**
- At session initialization (before any work)
- After major config updates from orchestrator
- When explicitly requested by orchestrator
- Before major project milestones

**Do NOT create snapshot:**
- During normal session work (use initial snapshot)
- Multiple times per session (only at start)
- For minor config tweaks

---

## What Is a Config Snapshot?

### Location

```
design/memory/config-snapshot.md
```

This file is SEPARATE from authoritative configs in `design/config/` (OPTIONAL: If EOA (Emasoft Orchestrator Agent) plugin is installed). It's a **read-only capture** for comparison purposes.

### Purpose

**What snapshots enable:**
1. **Drift detection** - Compare session config vs current config
2. **Consistency** - Ensure session operates with stable config
3. **Conflict resolution** - Decide how to handle config changes
4. **Audit trail** - Record which config version was active

**What snapshots DO NOT do:**
- Replace authoritative configs
- Get updated during session
- Control config versioning

---

## Why Snapshots Matter

### Without Snapshots

**Problem 1: Invisible drift**
- Central config changes during session
- Agent unaware of changes
- Work becomes incompatible with new config

**Problem 2: No baseline**
- Cannot determine what changed
- Cannot decide if changes are breaking
- No reference for conflict resolution

### With Snapshots

**Benefit 1: Drift detection**
- Compare snapshot vs current config
- Identify exactly what changed
- Assess impact of changes

**Benefit 2: Stable baseline**
- Session operates with consistent config
- Changes are deliberate, not accidental
- Can rollback or adopt new config intentionally

---

## Creation Procedures

### PROCEDURE 1: Create Initial Snapshot

**When to use:**
- At session initialization (Phase 1)
- After loading activeContext/patterns/progress
- Before beginning any work

**Steps:**

1. **Check if snapshot already exists**
   ```bash
   if [ -f design/memory/config-snapshot.md ]; then
     echo "WARNING: Snapshot already exists"
     echo "This should only happen if resuming session"
     # Use existing snapshot, do not recreate
     exit 0
   fi
   ```

2. **Read all central config files** (OPTIONAL: If EOA (Emasoft Orchestrator Agent) plugin is installed)
   ```bash
   configs=(
     "design/config/toolchain.md"
     "design/config/standards.md"
     "design/config/environment.md"
     "design/config/decisions.md"
   )

   for config in "${configs[@]}"; do
     if [ ! -f "$config" ]; then
       echo "ERROR: Required config not found: $config"
       exit 1
     fi
   done
   ```

3. **Extract metadata from each config**
   ```python
   def extract_config_metadata(config_file):
       with open(config_file) as f:
           content = f.read()

       # Extract "Last Updated" from config
       match = re.search(r'\*\*Last Updated:\*\* (.+)', content)
       last_updated = match.group(1) if match else "Unknown"

       # Get file timestamp
       stat = os.stat(config_file)
       file_timestamp = datetime.fromtimestamp(stat.st_mtime).isoformat()

       return {
           'last_updated': last_updated,
           'file_timestamp': file_timestamp,
           'content': content
       }
   ```

4. **Create snapshot file with header**
   ```markdown
   # Configuration Snapshot

   **Session Started:** 2025-12-31 10:23:45
   **Session ID:** orchestrator-master-20251231-102345
   **Snapshot Created:** 2025-12-31 10:23:47

   **Purpose:** Point-in-time capture of central configs at session start

   ## Captured Configurations
   ```

5. **Write each config to snapshot**
   ```python
   snapshot_content = []

   # Header
   snapshot_content.append("# Configuration Snapshot\n")
   snapshot_content.append(f"**Session Started:** {session_start_time}\n")
   snapshot_content.append(f"**Session ID:** {session_id}\n")
   snapshot_content.append(f"**Snapshot Created:** {datetime.now().isoformat()}\n\n")

   # Each config (OPTIONAL: If EOA (Emasoft Orchestrator Agent) plugin is installed)
   for config_name in ['toolchain', 'standards', 'environment', 'decisions']:
       config_file = f"design/config/{config_name}.md"  # EOA (Emasoft Orchestrator Agent) config path
       metadata = extract_config_metadata(config_file)

       snapshot_content.append(f"### {config_name}.md\n")
       snapshot_content.append(f"**Last Updated:** {metadata['last_updated']}\n")
       snapshot_content.append(f"**File Timestamp:** {metadata['file_timestamp']}\n\n")
       snapshot_content.append("```markdown\n")
       snapshot_content.append(metadata['content'])
       snapshot_content.append("\n```\n\n")

   # Write snapshot
   with open('design/memory/config-snapshot.md', 'w') as f:
       f.write(''.join(snapshot_content))
   ```

6. **Record snapshot creation in activeContext.md**
   ```markdown
   ## Config Snapshot
   **Created:** 2025-12-31 10:23:47
   **Configs Captured:** toolchain, standards, environment, decisions
   **Location:** design/memory/config-snapshot.md
   ```

7. **Validate snapshot**
   ```bash
   # Verify snapshot file exists
   if [ ! -f design/memory/config-snapshot.md ]; then
     echo "ERROR: Snapshot creation failed"
     exit 1
   fi

   # Verify snapshot contains all configs
   for config in toolchain standards environment decisions; do
     if ! grep -q "### ${config}.md" design/memory/config-snapshot.md; then
       echo "ERROR: Snapshot missing $config"
       exit 1
     fi
   done

   echo "Snapshot created and validated successfully"
   ```

**Example snapshot file:**

```markdown
# Configuration Snapshot

**Session Started:** 2025-12-31 10:23:45
**Session ID:** orchestrator-master-20251231-102345
**Snapshot Created:** 2025-12-31 10:23:47

**Purpose:** Point-in-time capture of central configs at session start

## Captured Configurations

### toolchain.md
**Last Updated:** 2025-12-30 15:20:00
**File Timestamp:** 2025-12-30T15:20:12

```markdown
# Toolchain Configuration

**Version:** 2.1
**Last Updated:** 2025-12-30 15:20:00

## Python
- Version: 3.11.7
- Package Manager: uv

## Node.js
- Version: 20.10.0
- Package Manager: pnpm
```

### standards.md
**Last Updated:** 2025-12-29 09:15:30
**File Timestamp:** 2025-12-29T09:15:45

```markdown
# Coding Standards

**Version:** 1.5
**Last Updated:** 2025-12-29 09:15:30

## Python
- Line length: 88 characters
- Formatter: ruff
```

[... additional configs ...]
```

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Target Audience:** Chief of Staff Agents
**Related:** SKILL.md (PROCEDURE 7: Capture Config Snapshot at Session Start)
**Next:** [Part 2: Validation and Reference](./19-config-snapshot-creation-part2-validation-and-reference.md)
