# Recovery Procedures

## Table of Contents

1. [When you need to understand the purpose](#purpose)
2. [Understanding recovery scenarios](#recovery-scenarios)
3. [Recovering from failed compaction](#recovery-from-failed-compaction) - See [Part 1](10-recovery-procedures-part1-failed-compaction.md)
4. [Recovering from corrupted memory](#recovery-from-corrupted-memory) - See [Part 2](10-recovery-procedures-part2-corruption-context.md)
5. [Recovering from lost context](#recovery-from-lost-context) - See [Part 2](10-recovery-procedures-part2-corruption-context.md)
6. [Recovering from snapshot failure](#recovery-from-snapshot-failure) - See [Part 3](10-recovery-procedures-part3-snapshot-emergency.md)
7. [Emergency recovery procedures](#emergency-recovery) - See [Part 3](10-recovery-procedures-part3-snapshot-emergency.md)
8. [For implementation examples](#examples) - See [Part 4a](10-recovery-procedures-part4a-examples.md)
9. [If issues occur](#troubleshooting) - See [Part 4b](10-recovery-procedures-part4b-troubleshooting.md)

## Part Files

This document is split into multiple parts for easier navigation:

| Part | File | Contents |
|------|------|----------|
| Index | This file | Purpose, Scenario Matrix, Overview |
| Part 1 | [10-recovery-procedures-part1-failed-compaction.md](10-recovery-procedures-part1-failed-compaction.md) | Recovery from failed compaction (Step-by-step procedure) |
| Part 2 | [10-recovery-procedures-part2-corruption-context.md](10-recovery-procedures-part2-corruption-context.md) | Recovery from corrupted memory and lost context |
| Part 3 | [10-recovery-procedures-part3-snapshot-emergency.md](10-recovery-procedures-part3-snapshot-emergency.md) | Snapshot failure recovery and emergency procedures |
| Part 4a | [10-recovery-procedures-part4a-examples.md](10-recovery-procedures-part4a-examples.md) | Recovery workflow examples |
| Part 4b | [10-recovery-procedures-part4b-troubleshooting.md](10-recovery-procedures-part4b-troubleshooting.md) | Troubleshooting common problems |

---

## Purpose

Recovery procedures restore session memory to a working state after failures. Effective recovery procedures:
- Minimize data loss
- Restore functionality quickly
- Prevent recurring failures
- Maintain data integrity
- Document recovery actions

## Recovery Scenarios

### Scenario Matrix

| Scenario | Severity | Recovery Time | Data Loss Risk | Primary Method |
|----------|----------|---------------|----------------|----------------|
| Failed compaction | High | 5-15 min | Medium | Restore from pre-compaction archive |
| Corrupted file | Medium | 2-5 min | Low | Restore from snapshot |
| Lost context | Medium | 5-10 min | Medium | Reconstruct from snapshots |
| Snapshot failure | Low | 1-2 min | Low | Create new snapshot |
| Complete memory loss | Critical | 15-30 min | High | Rebuild from git/docs |
| Broken symlinks | Low | 1 min | None | Recreate symlinks |

### Quick Reference: Which Part to Read

**If you need to recover from failed compaction:**
- Read [Part 1: Failed Compaction Recovery](10-recovery-procedures-part1-failed-compaction.md)
- Contains: Stop operations, identify last good state, restore from archive, validate, document

**If you have corrupted files or lost context:**
- Read [Part 2: Corruption and Context Recovery](10-recovery-procedures-part2-corruption-context.md)
- Contains: File corruption recovery, context reconstruction, source mining

**If snapshots fail or you need emergency recovery:**
- Read [Part 3: Snapshot and Emergency Recovery](10-recovery-procedures-part3-snapshot-emergency.md)
- Contains: Disk space checks, permission fixes, complete memory rebuild

**If you need examples:**
- Read [Part 4a: Examples](10-recovery-procedures-part4a-examples.md)
- Contains: Complete workflow examples, partial recovery examples

**If you need troubleshooting:**
- Read [Part 4b: Troubleshooting](10-recovery-procedures-part4b-troubleshooting.md)
- Contains: Common problems and solutions, diagnostic commands

---

## Recovery Decision Tree

```
┌─────────────────────────────────────┐
│ Session Memory Issue Detected       │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│ Can you read the memory files?      │
└─────────────────┬───────────────────┘
                  │
        ┌─────────┴─────────┐
        │ YES               │ NO
        ▼                   ▼
┌───────────────┐   ┌───────────────────┐
│ Files corrupt?│   │ Directory exists? │
└───────┬───────┘   └─────────┬─────────┘
        │                     │
   ┌────┴────┐          ┌─────┴─────┐
   │ YES     │ NO       │ YES       │ NO
   ▼         ▼          ▼           ▼
┌──────┐  ┌──────┐   ┌──────┐   ┌──────┐
│Part 2│  │Part 1│   │Part 3│   │Part 3│
│Corr. │  │Comp. │   │Snap. │   │Emerg.│
└──────┘  └──────┘   └──────┘   └──────┘
```

## General Recovery Principles

### Before Any Recovery

1. **Stop all operations** - Don't make changes during recovery
2. **Assess the damage** - Understand what's broken
3. **Backup current state** - Even corrupted state might have useful data
4. **Identify sources** - What backups/snapshots are available?

### During Recovery

1. **Follow the procedure** - Don't skip steps
2. **Document actions** - Record what you do
3. **Validate after each step** - Verify changes worked
4. **Don't rush** - Careful recovery prevents additional problems

### After Recovery

1. **Full validation** - Run all validation scripts
2. **Create new snapshot** - Protect the restored state
3. **Document the incident** - What happened, why, how fixed
4. **Review and prevent** - How to avoid recurrence

---

## Next Steps

Choose the appropriate part file based on your recovery scenario:

1. **[Part 1: Failed Compaction Recovery](10-recovery-procedures-part1-failed-compaction.md)**
   - Step 1: Stop All Operations
   - Step 2: Identify Last Good State
   - Step 3: Restore from Archive
   - Step 4: Validate Restored State
   - Step 5: Document Recovery

2. **[Part 2: Corruption and Context Recovery](10-recovery-procedures-part2-corruption-context.md)**
   - Recovery from Corrupted Memory
   - Recovery from Lost Context
   - Source Mining Techniques

3. **[Part 3: Snapshot and Emergency Recovery](10-recovery-procedures-part3-snapshot-emergency.md)**
   - Recovery from Snapshot Failure
   - Emergency Recovery Procedures
   - Complete Memory Rebuild

4. **[Part 4a: Examples](10-recovery-procedures-part4a-examples.md)**
   - Complete Recovery Workflow Example
   - Partial Recovery Example

5. **[Part 4b: Troubleshooting](10-recovery-procedures-part4b-troubleshooting.md)**
   - Common Problems and Solutions
   - Quick Diagnostic Commands
