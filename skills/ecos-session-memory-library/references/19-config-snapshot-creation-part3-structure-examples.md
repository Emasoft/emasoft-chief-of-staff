# Config Snapshot Creation - Part 3: Structure, Examples, and Troubleshooting

**Parent Document:** [19-config-snapshot-creation.md](./19-config-snapshot-creation.md)

## Table of Contents

- [Snapshot Structure](#snapshot-structure)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

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
Reading design/config/toolchain.md... Done    # (OPTIONAL: If EOA (Emasoft Orchestrator Agent) plugin is installed)
Reading design/config/standards.md... Done     # (OPTIONAL: If EOA (Emasoft Orchestrator Agent) plugin is installed)
Reading design/config/environment.md... Done   # (OPTIONAL: If EOA (Emasoft Orchestrator Agent) plugin is installed)
Reading design/config/decisions.md... Done     # (OPTIONAL: If EOA (Emasoft Orchestrator Agent) plugin is installed)

Writing snapshot to design/memory/config-snapshot.md... Done
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
# Check which configs exist (OPTIONAL: If EOA (Emasoft Orchestrator Agent) plugin is installed)
ls -la design/config/

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

### Issue: Snapshot content appears truncated

**Symptoms:**
- Config content in snapshot is incomplete
- Validation shows suspiciously short content

**Cause:** File read error or encoding issue

**Solution:**
```bash
# Check original config file (OPTIONAL: If EOA (Emasoft Orchestrator Agent) plugin is installed)
cat design/config/toolchain.md | wc -c

# Compare with snapshot content
# If mismatch, recreate snapshot
```

---

### Issue: Cannot create snapshot - permission denied

**Symptoms:**
- Snapshot creation fails with permission error
- Cannot write to design/memory/

**Cause:** Directory permissions or disk full

**Solution:**
```bash
# Check directory permissions
ls -la design/memory/

# Check disk space
df -h .

# Fix permissions if needed
chmod 755 design/memory/
```

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Related:** [19-config-snapshot-creation.md](./19-config-snapshot-creation.md)
