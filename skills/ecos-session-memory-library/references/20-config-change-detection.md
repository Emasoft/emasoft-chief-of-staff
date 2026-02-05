# Detecting Config Changes

## Table of Contents

1. [When you need to understand the overview](#overview)
2. [Understanding detection methods](#detection-methods)
3. [How to detect changes](#detection-procedures)
   - [Timestamp-based detection](#procedure-1-timestamp-based-detection) - See [Part 1](./20-config-change-detection-part1-timestamp-content-detection.md)
   - [Content-based detection](#procedure-2-content-based-detection) - See [Part 1](./20-config-change-detection-part1-timestamp-content-detection.md)
   - [Handling change notifications](#procedure-3-change-notification-handling) - See [Part 2](./20-config-change-detection-part2-notifications-drift.md)
   - [Periodic drift checking](#procedure-4-periodic-drift-check) - See [Part 2](./20-config-change-detection-part2-notifications-drift.md)
4. [Classifying changes](#change-classification) - See [Part 3](./20-config-change-detection-part3-classification-examples.md)
5. [For implementation examples](#examples) - See [Part 3](./20-config-change-detection-part3-classification-examples.md)
6. [If issues occur](#troubleshooting) - See [Part 3](./20-config-change-detection-part3-classification-examples.md)

---

## Part Files

This document has been split for readability. Detailed procedures are in:

| Part | File | Contents |
|------|------|----------|
| 1 | [20-config-change-detection-part1-timestamp-content-detection.md](./20-config-change-detection-part1-timestamp-content-detection.md) | Timestamp-based detection, Content-based detection |
| 2 | [20-config-change-detection-part2-notifications-drift.md](./20-config-change-detection-part2-notifications-drift.md) | Change notification handling, Periodic drift checks |
| 3 | [20-config-change-detection-part3-classification-examples.md](./20-config-change-detection-part3-classification-examples.md) | Change classification, Examples, Troubleshooting |

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

For detailed step-by-step procedures, see the part files:

### PROCEDURE 1: Timestamp-Based Detection

**When to use:** Periodic checks, lightweight detection, first-pass detection

**Full procedure:** [Part 1 - Timestamp-Based Detection](./20-config-change-detection-part1-timestamp-content-detection.md#procedure-1-timestamp-based-detection)

**Summary:**
1. Read snapshot timestamp for each config
2. Read current timestamp for each config
3. Compare timestamps
4. Report detected changes
5. Log changes to activeContext.md

---

### PROCEDURE 2: Content-Based Detection

**When to use:** After timestamp detection indicates change, to determine what specifically changed

**Full procedure:** [Part 1 - Content-Based Detection](./20-config-change-detection-part1-timestamp-content-detection.md#procedure-2-content-based-detection)

**Summary:**
1. Extract snapshot content for changed config
2. Read current config content
3. Compute content diff
4. Analyze changes
5. Report detailed changes
6. Update activeContext.md with analysis

---

### PROCEDURE 3: Change Notification Handling

**When to use:** When orchestrator sends config change notification, immediate response needed

**Full procedure:** [Part 2 - Change Notification Handling](./20-config-change-detection-part2-notifications-drift.md#procedure-3-change-notification-handling)

**Summary:**
1. Receive notification message
2. Parse notification
3. Validate notification against actual changes
4. Log notification
5. Trigger appropriate response

---

### PROCEDURE 4: Periodic Drift Check

**When to use:** During long-running sessions, proactive drift detection

**Full procedure:** [Part 2 - Periodic Drift Check](./20-config-change-detection-part2-notifications-drift.md#procedure-4-periodic-drift-check)

**Summary:**
1. Define check schedule
2. Perform scheduled check
3. Integrate into agent main loop
4. Log drift checks

---

## Change Classification

For full classification details, see [Part 3 - Change Classification](./20-config-change-detection-part3-classification-examples.md#change-classification).

| Severity | Examples | Action |
|----------|----------|--------|
| **MINOR** | Docs updates, formatting, patch releases | Adopt immediately |
| **MODERATE** | Minor version updates, new optional deps | Adopt after current task |
| **MAJOR** | Breaking API changes, major version updates | Pause work, review with user |
| **CRITICAL** | Security patches, urgent bug fixes | Adopt immediately, restart work |

---

## Examples

For full examples with code, see [Part 3 - Examples](./20-config-change-detection-part3-classification-examples.md#examples).

- **Example 1:** Detecting Toolchain Update via periodic check
- **Example 2:** Handling urgent change notification

---

## Troubleshooting

For troubleshooting details, see [Part 3 - Troubleshooting](./20-config-change-detection-part3-classification-examples.md#troubleshooting).

| Issue | Solution |
|-------|----------|
| False positive (timestamp changed, content unchanged) | Verify with content comparison |
| Change detected but notification not received | Proceed with detected change, log missing notification |

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Target Audience:** Chief of Staff Agents
**Related:** SKILL.md (PROCEDURE 8: Detect Config Changes During Session)
