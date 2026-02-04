# Config Snapshot Creation

## Table of Contents

1. [When you need to understand the overview](#overview)
2. [Understanding config snapshots](#what-is-a-config-snapshot)
3. [Why snapshots matter](#why-snapshots-matter)
4. [How to create snapshots](#creation-procedures)
   - [Creating initial snapshot](#procedure-1-create-initial-snapshot) → [Part 1](./19-config-snapshot-creation-part1-create-procedure.md)
   - [Updating snapshot](#procedure-2-update-snapshot) → [Part 2](./19-config-snapshot-creation-part2-update-validate.md)
   - [Validating snapshot](#procedure-3-validate-snapshot) → [Part 2](./19-config-snapshot-creation-part2-update-validate.md)
5. [Understanding snapshot structure](#snapshot-structure) → [Part 3](./19-config-snapshot-creation-part3-structure-examples.md)
6. [For implementation examples](#examples) → [Part 3](./19-config-snapshot-creation-part3-structure-examples.md)
7. [If issues occur](#troubleshooting) → [Part 3](./19-config-snapshot-creation-part3-structure-examples.md)

---

## Part Files

| Part | Content | Location |
|------|---------|----------|
| Part 1 | PROCEDURE 1: Create Initial Snapshot | [19-config-snapshot-creation-part1-create-procedure.md](./19-config-snapshot-creation-part1-create-procedure.md) |
| Part 2 | PROCEDURE 2: Update Snapshot, PROCEDURE 3: Validate Snapshot | [19-config-snapshot-creation-part2-update-validate.md](./19-config-snapshot-creation-part2-update-validate.md) |
| Part 3 | Snapshot Structure, Examples, Troubleshooting | [19-config-snapshot-creation-part3-structure-examples.md](./19-config-snapshot-creation-part3-structure-examples.md) |

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

This file is SEPARATE from authoritative configs in `design/config/` (OPTIONAL: If Atlas Orchestrator plugin is installed). It's a **read-only capture** for comparison purposes.

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

For detailed step-by-step procedures, see the part files:

### PROCEDURE 1: Create Initial Snapshot

**When to use:** At session initialization (Phase 1)

**Full procedure:** [Part 1 - Create Procedure](./19-config-snapshot-creation-part1-create-procedure.md)

**Contents of Part 1:**
- Step-by-step creation process
- Bash and Python code examples
- Example snapshot file format
- Validation steps

---

### PROCEDURE 2: Update Snapshot

**When to use:** After applying config changes during session (rare)

**Full procedure:** [Part 2 - Update and Validate](./19-config-snapshot-creation-part2-update-validate.md)

**Contents of Part 2 (Update section):**
- Verification steps before update
- Backup procedures
- Documentation requirements
- Orchestrator notification

---

### PROCEDURE 3: Validate Snapshot

**When to use:** After creating snapshot, during initialization, before drift detection

**Full procedure:** [Part 2 - Update and Validate](./19-config-snapshot-creation-part2-update-validate.md)

**Contents of Part 2 (Validate section):**
- Structure validation
- Timestamp verification
- Content verification
- Validation report format

---

## Snapshot Structure

For detailed structure documentation, see [Part 3 - Structure, Examples, Troubleshooting](./19-config-snapshot-creation-part3-structure-examples.md).

**Contents of Part 3 (Structure section):**
- File format specification
- Required header elements
- Config section requirements

---

## Examples

For implementation examples, see [Part 3 - Structure, Examples, Troubleshooting](./19-config-snapshot-creation-part3-structure-examples.md).

**Contents of Part 3 (Examples section):**
- Example 1: Creating initial snapshot
- Example 2: Updating snapshot after config change

---

## Troubleshooting

For troubleshooting guidance, see [Part 3 - Structure, Examples, Troubleshooting](./19-config-snapshot-creation-part3-structure-examples.md).

**Contents of Part 3 (Troubleshooting section):**
- Issue: Snapshot missing required config
- Issue: Snapshot has future timestamp
- Issue: Snapshot content appears truncated
- Issue: Cannot create snapshot - permission denied

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Target Audience:** Chief of Staff Agents
**Related:** SKILL.md (PROCEDURE 7: Capture Config Snapshot at Session Start)
