# Context Synchronization - Index

## Overview

Context synchronization ensures session memory files accurately reflect the agent's actual work state. This document has been split into two parts for easier navigation and reduced token consumption.

---

## Document Parts

### Part 1: Foundations and Core Procedures
**File:** [14-context-sync-part1-foundations.md](14-context-sync-part1-foundations.md)
**Lines:** ~390

**Contents:**
- 1. Overview
  - 1.1 What Is Context Synchronization?
  - 1.2 Why Synchronization Matters
- 2. Understanding Context Drift
  - 2.1 Definition
  - 2.2 Common Causes (Infrequent Updates, Failed Updates, Manual Interventions, External Changes, Missed Events)
- 3. Synchronization Points
  - 3.1 When to Synchronize (7 trigger points)
- 4. Core Synchronization Procedures
  - 4.1 Procedure 1: Detect Context Drift
  - 4.2 Procedure 2: Sync After Task Completion
  - 4.3 Procedure 3: Sync After File Switch
  - 4.4 Procedure 4: Sync After Decision

**When to read Part 1:**
- Understanding what context sync is and why it matters
- Learning how to detect drift
- Performing routine sync after task/file/decision changes

---

### Part 2: Advanced Procedures and Troubleshooting
**File:** [14-context-sync-part2-advanced.md](14-context-sync-part2-advanced.md)
**Lines:** ~290

**Contents:**
- 1. Emergency Full Resync (Procedure 5)
  - 1.1 When to Use Emergency Resync
  - 1.2 Step-by-Step Procedure
- 2. Consistency Checks
  - 2.1 Check 1: Task Status Consistency
  - 2.2 Check 2: File Path Validity
  - 2.3 Check 3: Decision Recency
  - 2.4 Check 4: Pattern Relevance
- 3. Synchronization Examples
  - 3.1 Example 1: Syncing After Unexpected Task Completion
  - 3.2 Example 2: Syncing After File Moved
  - 3.3 Example 3: Syncing After Decision Changes Direction
- 4. Troubleshooting
  - 4.1 Cannot Determine Actual State
  - 4.2 Frequent Drift Detected
  - 4.3 Sync Creates New Inconsistencies

**When to read Part 2:**
- Severe context drift requiring emergency resync
- Running consistency validation checks
- Seeing practical examples of sync procedures
- Debugging sync problems

---

## Quick Reference

| Scenario | Read This |
|----------|-----------|
| What is context sync? | Part 1, Section 1 |
| Why is my agent on wrong task? | Part 1, Section 2 (Context Drift) |
| When should I sync? | Part 1, Section 3 |
| Task just completed | Part 1, Section 4.2 |
| Switched to new file | Part 1, Section 4.3 |
| Made a decision | Part 1, Section 4.4 |
| Everything is wrong, need full reset | Part 2, Section 1 |
| How to validate sync worked | Part 2, Section 2 |
| Show me an example | Part 2, Section 3 |
| Sync keeps failing | Part 2, Section 4 |

---

**Version:** 1.0
**Last Updated:** 2026-01-08
**Original File:** 14-context-sync.md (789 lines, now split)
