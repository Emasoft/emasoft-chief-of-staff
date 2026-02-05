# Detecting Config Changes - Part 1: Methods and Basic Detection

## Table of Contents

1. [Overview](#overview)
   - [What Is Config Change Detection?](#what-is-config-change-detection)
   - [Why Detection Matters](#why-detection-matters)
2. [Detection Methods](#detection-methods)
   - [Method 1: Timestamp Comparison](#method-1-timestamp-comparison)
   - [Method 2: Content Hash Comparison](#method-2-content-hash-comparison)
   - [Method 3: Line-by-Line Diff](#method-3-line-by-line-diff)
   - [Method 4: Notification-Based](#method-4-notification-based)
3. [Basic Detection Procedures](#detection-procedures)
   - [PROCEDURE 1: Timestamp-Based Detection](#procedure-1-timestamp-based-detection)
   - [PROCEDURE 2: Content-Based Detection](#procedure-2-content-based-detection)

**Related documents:**
- [Part 2: Advanced Procedures and Classification](./20-config-change-detection-part2-advanced.md)

---

## Overview

### What Is Config Change Detection?

Config change detection is the process of identifying when central configuration files (in `design/config/` - OPTIONAL: If EOA (Emasoft Orchestrator Agent) plugin is installed) have been modified since the session config snapshot was created. This allows the agent to respond appropriately to config updates from the orchestrator.

### Why Detection Matters

**Without detection:**
- Agent uses outdated config
- Work becomes incompatible with standards
- Conflicts arise when changes are discovered late

**With detection:**
- Timely awareness of config changes
- Can assess impact and decide on adoption
- Prevents incompatible work

---

## Detection Methods

### Method 1: Timestamp Comparison

**How it works:**
Compare "Last Updated" timestamp in current config vs snapshot config.

**Pros:**
- Fast and lightweight
- Clear change indicator
- No content parsing needed

**Cons:**
- Doesn't show what changed
- False positives if timestamp updated but content unchanged
- Requires consistent timestamp format

---

### Method 2: Content Hash Comparison

**How it works:**
Compute hash of current config content vs snapshot content.

**Pros:**
- Detects actual content changes
- No false positives from timestamp updates
- Reliable change detection

**Cons:**
- Doesn't show what changed
- Requires full content comparison
- More computationally expensive

---

### Method 3: Line-by-Line Diff

**How it works:**
Compare current config line-by-line with snapshot config.

**Pros:**
- Shows exactly what changed
- Can classify changes (major/minor)
- Detailed change information

**Cons:**
- Most expensive method
- Complex for large configs
- Requires diff algorithm

---

### Method 4: Notification-Based

**How it works:**
Orchestrator sends notification when config changes.

**Pros:**
- Immediate awareness
- No polling needed
- Includes context from orchestrator

**Cons:**
- Depends on notification system
- May miss changes if notification fails
- Requires message handling infrastructure

---

## Detection Procedures

### PROCEDURE 1: Timestamp-Based Detection

**When to use:**
- Periodic checks during session
- Lightweight detection needed
- First-pass change detection

**Steps:**

1. **Read snapshot timestamp for each config**
   ```python
   def extract_snapshot_timestamps(snapshot_file):
       with open(snapshot_file) as f:
           content = f.read()

       timestamps = {}
       configs = ['toolchain', 'standards', 'environment', 'decisions']

       for config in configs:
           # Find section for this config
           pattern = f"### {config}.md.*?\\*\\*Last Updated:\\*\\* (.+)"
           match = re.search(pattern, content, re.DOTALL)

           if match:
               timestamps[config] = match.group(1).strip()

       return timestamps
   ```

2. **Read current timestamp for each config**
   ```python
   def extract_current_timestamps():
       timestamps = {}
       configs = ['toolchain', 'standards', 'environment', 'decisions']

       for config in configs:
           # OPTIONAL: If EOA (Emasoft Orchestrator Agent) plugin is installed
           config_file = f"design/config/{config}.md"

           with open(config_file) as f:
               content = f.read()

           # Extract "Last Updated" from current config
           match = re.search(r'\*\*Last Updated:\*\* (.+)', content)
           if match:
               timestamps[config] = match.group(1).strip()

       return timestamps
   ```

3. **Compare timestamps**
   ```python
   snapshot_timestamps = extract_snapshot_timestamps('design/memory/config-snapshot.md')
   current_timestamps = extract_current_timestamps()

   changes_detected = []

   for config in snapshot_timestamps:
       snapshot_ts = snapshot_timestamps[config]
       current_ts = current_timestamps.get(config)

       if current_ts != snapshot_ts:
           changes_detected.append({
               'config': config,
               'snapshot_timestamp': snapshot_ts,
               'current_timestamp': current_ts
           })
   ```

4. **Report detected changes**
   ```markdown
   ## Config Change Detection Report (Timestamp Method)

   **Detection Time:** 2025-12-31 14:30:00
   **Method:** Timestamp comparison

   **Changes Detected:**
   - toolchain.md
     - Snapshot: 2025-12-30 15:20:00
     - Current:  2025-12-31 09:00:00
     - **STATUS:** Changed

   - standards.md
     - Snapshot: 2025-12-29 09:15:30
     - Current:  2025-12-29 09:15:30
     - **STATUS:** Unchanged

   **Summary:** 1 config changed, 3 unchanged
   ```

5. **Log changes to activeContext.md**
   ```markdown
   ## Config Change Log

   ### Change Detected: 2025-12-31 14:30:00
   **Config:** toolchain.md
   **Detection Method:** Timestamp comparison
   **Snapshot Timestamp:** 2025-12-30 15:20:00
   **Current Timestamp:** 2025-12-31 09:00:00
   **Status:** Pending review
   ```

---

### PROCEDURE 2: Content-Based Detection

**When to use:**
- After timestamp detection indicates change
- To determine what specifically changed
- Before deciding on conflict resolution

**Steps:**

1. **Extract snapshot content for changed config**
   ```python
   def extract_snapshot_config(snapshot_file, config_name):
       with open(snapshot_file) as f:
           content = f.read()

       # Find config section
       pattern = f"### {config_name}.md.*?```markdown(.*?)```"
       match = re.search(pattern, content, re.DOTALL)

       if match:
           return match.group(1).strip()

       return None
   ```

2. **Read current config content** (OPTIONAL: If EOA (Emasoft Orchestrator Agent) plugin is installed)
   ```python
   def read_current_config(config_name):
       # EOA (Emasoft Orchestrator Agent) config path
       config_file = f"design/config/{config_name}.md"

       with open(config_file) as f:
           return f.read()
   ```

3. **Compute content diff**
   ```python
   import difflib

   snapshot_content = extract_snapshot_config('design/memory/config-snapshot.md', 'toolchain')
   current_content = read_current_config('toolchain')

   diff = list(difflib.unified_diff(
       snapshot_content.splitlines(),
       current_content.splitlines(),
       fromfile='snapshot/toolchain.md',
       tofile='current/toolchain.md',
       lineterm=''
   ))
   ```

4. **Analyze changes**
   ```python
   additions = [line for line in diff if line.startswith('+') and not line.startswith('+++')]
   deletions = [line for line in diff if line.startswith('-') and not line.startswith('---')]

   change_summary = {
       'lines_added': len(additions),
       'lines_removed': len(deletions),
       'additions': additions,
       'deletions': deletions
   }
   ```

5. **Report detailed changes**
   ```markdown
   ## Config Content Changes: toolchain.md

   **Lines Added:** 3
   **Lines Removed:** 1

   ### Additions:
   ```
   + - Version: 3.12.1 (updated)
   + ## Type Checking
   + - Tool: mypy
   ```

   ### Deletions:
   ```
   - - Version: 3.11.7
   ```

   ### Change Classification: MINOR
   - Python version bumped 3.11 → 3.12
   - Added type checking section
   ```

6. **Update activeContext.md with analysis**
   ```markdown
   ## Config Change Analysis

   ### toolchain.md (2025-12-31 14:35:00)
   **Change Type:** Minor version update
   **Impact:** Python 3.11 → 3.12, added mypy requirement
   **Breaking:** Potentially (new Python version)
   **Action Required:** Review compatibility
   ```

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Target Audience:** Chief of Staff Agents
**Related:** SKILL.md (PROCEDURE 8: Detect Config Changes During Session)
