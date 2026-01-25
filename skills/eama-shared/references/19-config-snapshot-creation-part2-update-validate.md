# Config Snapshot Creation - Part 2: Update and Validate Procedures

**Parent Document:** [19-config-snapshot-creation.md](./19-config-snapshot-creation.md)

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

**Version:** 1.0
**Last Updated:** 2026-01-01
**Related:** [19-config-snapshot-creation.md](./19-config-snapshot-creation.md)
