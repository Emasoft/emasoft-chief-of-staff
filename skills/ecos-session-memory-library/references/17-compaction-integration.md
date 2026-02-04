# Compaction Integration - Index

This document provides an index to the compaction integration documentation, which has been split into two parts for easier navigation.

## Document Parts

### Part 1: Concepts & Preparation
**File:** [17-compaction-integration-part1-concepts-preparation.md](17-compaction-integration-part1-concepts-preparation.md)

**Contents:**
- Overview of compaction integration
- Understanding context compaction (what, when, how)
- Compaction risks (memory loss, partial state, stale memory, failed reload)
- PROCEDURE 1: Prepare for Compaction
- PROCEDURE 2: Save State Before Compaction
- Compaction triggers and emergency saves

**When to read:** Start here to understand compaction concepts and learn how to prepare for and save state before compaction.

---

### Part 2: Recovery & Verification
**File:** [17-compaction-integration-part2-recovery-verification.md](17-compaction-integration-part2-recovery-verification.md)

**Contents:**
- PROCEDURE 3: Reload After Compaction
- PROCEDURE 4: Verify Post-Compaction State
- PROCEDURE 5: Recover from Compaction Issues (minor, major, critical)
- Practical examples of compaction handling
- Troubleshooting common issues

**When to read:** Reference this when you need to recover from compaction or verify state after compaction occurred.

---

## Quick Reference

| Procedure | Purpose | Location |
|-----------|---------|----------|
| PROCEDURE 1 | Prepare for Compaction | Part 1 |
| PROCEDURE 2 | Save State Before Compaction | Part 1 |
| PROCEDURE 3 | Reload After Compaction | Part 2 |
| PROCEDURE 4 | Verify Post-Compaction State | Part 2 |
| PROCEDURE 5 | Recover from Compaction Issues | Part 2 |

---

**Version:** 1.0
**Last Updated:** 2026-01-08
**Target Audience:** Chief of Staff Agents
