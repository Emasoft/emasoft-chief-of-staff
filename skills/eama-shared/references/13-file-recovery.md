# Session Memory File Recovery - Index

This document was split into multiple parts for easier navigation. Each part covers specific aspects of memory file recovery.

---

## Part 1: Detection and Basic Recovery

**File:** [13-file-recovery-part1-detection-and-basic-recovery.md](13-file-recovery-part1-detection-and-basic-recovery.md)

**Contents:**
1. Overview
   - 1.1 What Is Memory File Recovery?
   - 1.2 Why Recovery Matters
2. Types of Memory File Corruption
   - 2.1 Type 1: Syntax Corruption
   - 2.2 Type 2: Content Corruption
   - 2.3 Type 3: Truncation Corruption
   - 2.4 Type 4: Complete Loss
3. Basic Recovery Procedures
   - 3.1 PROCEDURE 1: Detect Corruption
   - 3.2 PROCEDURE 2: Restore from Backup
   - 3.3 PROCEDURE 3: Reconstruct from Conversation History

**When to read:** Start here to understand corruption types and basic recovery methods.

---

## Part 2: Advanced Recovery and Prevention

**File:** [13-file-recovery-part2-advanced-recovery-and-prevention.md](13-file-recovery-part2-advanced-recovery-and-prevention.md)

**Contents:**
1. Advanced Recovery Procedures
   - 1.1 PROCEDURE 4: Partial Recovery
   - 1.2 PROCEDURE 5: Emergency Manual Reconstruction
2. Prevention Strategies
   - 2.1 Strategy 1: Automatic Backups
   - 2.2 Strategy 2: Atomic Writes
   - 2.3 Strategy 3: Validation After Write
   - 2.4 Strategy 4: Keep Multiple Backup Generations
3. Examples
   - 3.1 Example 1: Detecting and Recovering from Truncation
   - 3.2 Example 2: Reconstructing from Conversation History
   - 3.3 Example 3: Partial Recovery with Section Merge
4. Troubleshooting
   - 4.1 All backups are also corrupted
   - 4.2 Cannot determine which sections are valid
   - 4.3 Recovered file missing recent work
   - 4.4 Conversation history is not available

**When to read:** When basic recovery fails or you need prevention strategies.

---

## Quick Reference: Which Procedure to Use

| Situation | Procedure | Part |
|-----------|-----------|------|
| Need to check if files are corrupted | PROCEDURE 1: Detect Corruption | Part 1 |
| Backup files exist | PROCEDURE 2: Restore from Backup | Part 1 |
| No backup, but have conversation history | PROCEDURE 3: Reconstruct from History | Part 1 |
| File is partially corrupted | PROCEDURE 4: Partial Recovery | Part 2 |
| All recovery methods failed | PROCEDURE 5: Emergency Reconstruction | Part 2 |

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Target Audience:** Atlas Orchestrator Agents
