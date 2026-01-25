# Config Snapshot Creation - Part 2: Validation and Reference

## Table of Contents

1. [How to update snapshots](#procedure-2-update-snapshot)
2. [How to validate snapshots](#procedure-3-validate-snapshot)
3. [Understanding snapshot structure](#snapshot-structure)
4. [For implementation examples](#examples)
5. [If issues occur](#troubleshooting)

**Related Parts:**
- [Part 1: Fundamentals and Creation](./19-config-snapshot-creation-part1-fundamentals-and-creation.md) - Overview, concepts, initial creation

---

## PROCEDURE 2: Update Snapshot

**When to use:**
- After applying config changes during session
- After resolving config conflicts
- When orchestrator explicitly requests update

**IMPORTANT:** This is rare. Normally snapshots are NOT updated during session.

**Steps:**

1. **Verify update is intentional**
   ```
   Agent: Config snapshot update requested. This should only happen after:
   - Resolving config conflict and adopting new config
   - Explicit request from orchestrator
   - Config change explicitly approved for current session

   Confirm snapshot update? [yes/no]
   ```

2. **Backup current snapshot**
   ```bash
   timestamp=$(date +%Y%m%d-%H%M%S)
   cp .atlas/memory/config-snapshot.md \
      .atlas/memory/backups/config-snapshot.md.backup.$timestamp
   ```

3. **Create new snapshot (same as PROCEDURE 1)**
   ```python
   create_config_snapshot()  # Recreate entire snapshot
   ```

4. **Document update in activeContext.md**
   ```markdown
   ## Config Snapshot Updates

   ### Update 1: 2025-12-31 14:30:00
   **Reason:** Adopted new toolchain version after conflict resolution
   **Changed Configs:** toolchain.md
   **Previous Snapshot:** Backed up to backups/config-snapshot.md.backup.20251231-143000
   ```

5. **Notify orchestrator if required**
   ```json
   {
     "to": "orchestrator-master",
     "subject": "Config snapshot updated",
     "content": {
       "type": "config-snapshot-update",
       "session_id": "orchestrator-master-20251231-102345",
       "updated_at": "2025-12-31T14:30:00",
       "changed_configs": ["toolchain.md"],
       "reason": "Adopted new toolchain version"
     }
   }
   ```

---

## PROCEDURE 3: Validate Snapshot

**When to use:**
- After creating snapshot
- During session initialization
- Before config drift detection
- When troubleshooting config issues

**Steps:**

1. **Check snapshot file exists**
   ```bash
   if [ ! -f .atlas/memory/config-snapshot.md ]; then
     echo "ERROR: Config snapshot missing"
     exit 1
   fi
   ```

2. **Verify snapshot structure**
   ```python
   def validate_snapshot_structure(snapshot_file):
       with open(snapshot_file) as f:
           content = f.read()

       # Required headers
       required = [
           '# Configuration Snapshot',
           '**Session Started:**',
           '**Session ID:**',
           '**Snapshot Created:**'
       ]

       for req in required:
           if req not in content:
               print(f"ERROR: Snapshot missing required header: {req}")
               return False

       # Required config sections
       configs = ['toolchain', 'standards', 'environment', 'decisions']
       for config in configs:
           if f"### {config}.md" not in content:
               print(f"ERROR: Snapshot missing config: {config}")
               return False

       return True
   ```

3. **Extract and verify timestamps**
   ```python
   # Extract snapshot timestamp
   match = re.search(r'\*\*Snapshot Created:\*\* (.+)', content)
   snapshot_time = datetime.fromisoformat(match.group(1))

   # Extract session start timestamp
   match = re.search(r'\*\*Session Started:\*\* (.+)', content)
   session_start = datetime.fromisoformat(match.group(1))

   # Snapshot should be created shortly after session start
   if snapshot_time < session_start:
       print("ERROR: Snapshot created before session start")
       return False

   time_diff = (snapshot_time - session_start).total_seconds()
   if time_diff > 60:  # More than 1 minute
       print(f"WARNING: Snapshot created {time_diff}s after session start")
   ```

4. **Verify config content is captured**
   ```python
   for config in configs:
       # Find config section
       pattern = f"### {config}.md.*?```markdown(.*?)```"
       match = re.search(pattern, content, re.DOTALL)

       if not match:
           print(f"ERROR: Config {config} content not captured")
           return False

       config_content = match.group(1)
       if len(config_content) < 100:  # Too short to be valid config
           print(f"WARNING: Config {config} content suspiciously short")
   ```

5. **Verify timestamps are in past**
   ```python
   now = datetime.now()

   if snapshot_time > now:
       print("ERROR: Snapshot has future timestamp")
       return False
   ```

6. **Report validation results**
   ```
   Config Snapshot Validation Report
   ==================================

   File: .atlas/memory/config-snapshot.md
   Size: 45 KB

   Structure:
   ✓ Required headers present
   ✓ All config sections present
   ✓ Session ID valid

   Timestamps:
   ✓ Snapshot created: 2025-12-31 10:23:47
   ✓ Session started: 2025-12-31 10:23:45
   ✓ Time difference: 2 seconds (OK)

   Content:
   ✓ toolchain.md captured (8 KB)
   ✓ standards.md captured (12 KB)
   ✓ environment.md captured (5 KB)
   ✓ decisions.md captured (20 KB)

   Validation: PASSED
   ```

---

## Snapshot Structure

### File Format

```markdown
# Configuration Snapshot

**Session Started:** [ISO timestamp]
**Session ID:** [unique session identifier]
**Snapshot Created:** [ISO timestamp]
**Purpose:** [description]

## Captured Configurations

### [config-name].md
**Last Updated:** [from config file]
**File Timestamp:** [filesystem timestamp]

```markdown
[full config file content]
```

### [next-config].md
...
```

### Required Elements

**Header:**
- Session Started timestamp
- Session ID
- Snapshot Created timestamp
- Purpose statement

**Each Config Section:**
- Config name (### heading)
- Last Updated metadata
- File Timestamp metadata
- Full config content in code block

---

## Examples

### Example 1: Creating Initial Snapshot

**At session start:**
```python
# In session initialization

def initialize_session():
    # Load core memory
    load_memory_files()

    # Create config snapshot
    create_config_snapshot()

    # Ready to begin work
```

**Snapshot creation output:**
```
Creating config snapshot...
Reading .atlas/config/toolchain.md... Done
Reading .atlas/config/standards.md... Done
Reading .atlas/config/environment.md... Done
Reading .atlas/config/decisions.md... Done

Writing snapshot to .atlas/memory/config-snapshot.md... Done
Validating snapshot... PASSED

Config snapshot created successfully.
```

---

### Example 2: Updating Snapshot After Config Change

**Scenario:** Toolchain version updated mid-session

**Update process:**
```
Agent: Config change detected: toolchain.md updated to Python 3.12

User approved adopting new config for current session.

Updating config snapshot...
Backing up current snapshot... Done
Creating new snapshot with updated toolchain.md... Done

Snapshot updated. Session now using:
- Python 3.12 (updated from 3.11)
- All other configs unchanged
```

---

## Troubleshooting

### Issue: Snapshot missing required config

**Symptoms:**
- Validation reports missing config section
- Snapshot appears incomplete

**Cause:** Config file missing when snapshot created

**Solution:**
```bash
# Check which configs exist
ls -la .atlas/config/

# If config is missing, cannot create valid snapshot
# Either restore missing config or proceed without it (not recommended)
```

---

### Issue: Snapshot has future timestamp

**Symptoms:**
- Validation reports future timestamp
- Snapshot timestamp > current time

**Cause:** System clock incorrect when snapshot created

**Solution:**
1. Check system time is correct
2. Recreate snapshot with correct timestamp
3. Do not attempt to fix timestamp manually

---

### Issue: Snapshot content mismatch

**Symptoms:**
- Snapshot shows different content than expected
- Config drift detection gives false positives

**Cause:** Snapshot created from wrong config files or outdated copy

**Solution:**
1. Verify `.atlas/config/` contains authoritative configs
2. Delete corrupt snapshot
3. Recreate snapshot from correct source files
4. Validate new snapshot immediately after creation

---

### Issue: Snapshot file corrupted

**Symptoms:**
- Validation fails with parse errors
- File contains garbled or incomplete content

**Cause:** Write interrupted or disk error

**Solution:**
```bash
# Check for backup
ls .atlas/memory/backups/config-snapshot.md.backup.*

# If backup exists, restore it
cp .atlas/memory/backups/config-snapshot.md.backup.LATEST \
   .atlas/memory/config-snapshot.md

# If no backup, recreate snapshot
rm .atlas/memory/config-snapshot.md
# Then run PROCEDURE 1 to create fresh snapshot
```

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Target Audience:** Atlas Orchestrator Agents
**Related:** SKILL.md (PROCEDURE 7: Capture Config Snapshot at Session Start)
**Previous:** [Part 1: Fundamentals and Creation](./19-config-snapshot-creation-part1-fundamentals-and-creation.md)
