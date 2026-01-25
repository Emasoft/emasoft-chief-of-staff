# Config Snapshot Creation - Part 1: Create Initial Snapshot

**Parent Document:** [19-config-snapshot-creation.md](./19-config-snapshot-creation.md)

---

## PROCEDURE 1: Create Initial Snapshot

**When to use:**
- At session initialization (Phase 1)
- After loading activeContext/patterns/progress
- Before beginning any work

**Steps:**

1. **Check if snapshot already exists**
   ```bash
   if [ -f .atlas/memory/config-snapshot.md ]; then
     echo "WARNING: Snapshot already exists"
     echo "This should only happen if resuming session"
     # Use existing snapshot, do not recreate
     exit 0
   fi
   ```

2. **Read all central config files**
   ```bash
   configs=(
     ".atlas/config/toolchain.md"
     ".atlas/config/standards.md"
     ".atlas/config/environment.md"
     ".atlas/config/decisions.md"
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

   # Each config
   for config_name in ['toolchain', 'standards', 'environment', 'decisions']:
       config_file = f".atlas/config/{config_name}.md"
       metadata = extract_config_metadata(config_file)

       snapshot_content.append(f"### {config_name}.md\n")
       snapshot_content.append(f"**Last Updated:** {metadata['last_updated']}\n")
       snapshot_content.append(f"**File Timestamp:** {metadata['file_timestamp']}\n\n")
       snapshot_content.append("```markdown\n")
       snapshot_content.append(metadata['content'])
       snapshot_content.append("\n```\n\n")

   # Write snapshot
   with open('.atlas/memory/config-snapshot.md', 'w') as f:
       f.write(''.join(snapshot_content))
   ```

6. **Record snapshot creation in activeContext.md**
   ```markdown
   ## Config Snapshot
   **Created:** 2025-12-31 10:23:47
   **Configs Captured:** toolchain, standards, environment, decisions
   **Location:** .atlas/memory/config-snapshot.md
   ```

7. **Validate snapshot**
   ```bash
   # Verify snapshot file exists
   if [ ! -f .atlas/memory/config-snapshot.md ]; then
     echo "ERROR: Snapshot creation failed"
     exit 1
   fi

   # Verify snapshot contains all configs
   for config in toolchain standards environment decisions; do
     if ! grep -q "### ${config}.md" .atlas/memory/config-snapshot.md; then
       echo "ERROR: Snapshot missing $config"
       exit 1
     fi
   done

   echo "Snapshot created and validated successfully"
   ```

---

## Example Snapshot File

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
**Related:** [19-config-snapshot-creation.md](./19-config-snapshot-creation.md)
