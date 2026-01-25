# Config Change Detection: Classification, Examples, and Troubleshooting

**Parent Document:** [20-config-change-detection.md](./20-config-change-detection.md)

---

## Table of Contents

1. [Change Classification](#change-classification)
   - [Change Severity Levels](#change-severity-levels)
2. [Examples](#examples)
   - [Example 1: Detecting Toolchain Update](#example-1-detecting-toolchain-update)
   - [Example 2: Handling Change Notification](#example-2-handling-change-notification)
3. [Troubleshooting](#troubleshooting)

---

## Change Classification

### Change Severity Levels

**MINOR Changes:**
- Documentation updates
- Formatting improvements
- Comment additions
- Minor version bumps (patch releases)

**Action:** Can adopt immediately with minimal impact

---

**MODERATE Changes:**
- Minor version updates (3.11 → 3.12)
- New optional dependencies
- Standard clarifications
- Process improvements

**Action:** Adopt after current task completion

---

**MAJOR Changes:**
- Breaking API changes
- Major version updates (Python 2 → 3)
- Incompatible standards
- Architectural shifts

**Action:** Pause work, review impact, decide with user

---

**CRITICAL Changes:**
- Security patches
- Urgent bug fixes
- Emergency standards updates

**Action:** Adopt immediately, restart affected work

---

## Examples

### Example 1: Detecting Toolchain Update

**Periodic check detects change:**
```python
# During 14:30 scheduled check
changes = detect_config_changes_timestamp()
# Returns: ['toolchain']

# Analyze changes
diff = analyze_config_changes('toolchain')
# Shows: Python 3.11.7 → 3.12.1
```

**Output:**
```
Config Change Detected (14:30:00)
==================================

Config: toolchain.md
Method: Timestamp comparison + content diff

Changes:
- Python version: 3.11.7 → 3.12.1
- Added: Type checking with mypy

Classification: MODERATE
Recommendation: Adopt after current task
```

---

### Example 2: Handling Change Notification

**Notification received:**
```json
{
  "from": "orchestrator-master",
  "subject": "URGENT: Security update required",
  "priority": "critical",
  "content": {
    "type": "config-update",
    "config_files": ["toolchain.md"],
    "change_type": "critical",
    "reason": "CVE-2025-12345 requires Python 3.12.2",
    "breaking": true,
    "action": "adopt-immediately"
  }
}
```

**Response:**
```
CRITICAL CONFIG UPDATE RECEIVED
================================

Pausing current work...
Saving progress... Done

Analyzing change:
- Current: Python 3.12.1
- Required: Python 3.12.2
- Reason: Security CVE-2025-12345

Adopting new config immediately...
Updating config snapshot... Done

Resuming work with Python 3.12.2
```

---

## Troubleshooting

### Issue: False positive - timestamp changed but content unchanged

**Cause:** Timestamp updated manually or by script

**Solution:**
```python
# Always verify with content comparison
if timestamp_indicates_change:
    content_changed = compare_content_hash(snapshot, current)
    if not content_changed:
        print("False positive: timestamp changed but content identical")
        # Ignore change
```

---

### Issue: Change detected but notification not received

**Cause:** Notification system failure or delay

**Solution:**
1. Proceed with detected change
2. Log missing notification
3. Report to orchestrator
4. Don't wait for notification

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Related:** [20-config-change-detection.md](./20-config-change-detection.md)
