# Pre-Compaction Checklist

## Table of Contents
1. [Purpose](#purpose)
2. [Master Checklist Template](#master-checklist-template)
3. [Preparation Phase](#preparation-phase)
4. [Backup Phase](#backup-phase)
5. [Validation Phase](#validation-phase)
6. [Final Verification](#final-verification)
7. [Go/No-Go Decision](#gono-go-decision)
8. [Examples](#examples)

---

## Purpose

The pre-compaction checklist ensures all safety measures are in place before compaction. Following this checklist:
- Prevents data loss
- Enables recovery if compaction fails
- Validates readiness
- Documents pre-compaction state
- Provides go/no-go decision criteria

---

## Master Checklist Template

**See:** [12-pre-compaction-checklist-part1-master-checklist.md](12-pre-compaction-checklist-part1-master-checklist.md)

Contents:
- Complete fillable checklist template with all phases
- Preparation phase checklist items
- Backup phase checklist items
- Validation phase checklist items
- Final verification checklist items
- Go/No-Go decision criteria
- Signatures section
- How to use the checklist

---

## Preparation Phase

**See:** [12-pre-compaction-checklist-part2-preparation-phase.md](12-pre-compaction-checklist-part2-preparation-phase.md)

Contents:
- Step 1: Context Preparation Script (`prepare_context.sh`)
  - Check current focus is documented
  - Verify decisions are recorded
  - Confirm open questions documented
- Step 2: Pattern Extraction Script (`extract_patterns.sh`)
  - Review context for extractable patterns
  - Count existing patterns
  - Manual review prompts
- Step 3: Progress Review Script (`review_progress.sh`)
  - Count tasks by status (active, completed, blocked)
  - Check for critical work in progress
  - Approval prompt for active tasks

---

## Backup Phase

**See:** [12-pre-compaction-checklist-part3-backup-validation.md](12-pre-compaction-checklist-part3-backup-validation.md)

Contents:
- Backup Creation Script (`create_all_backups.sh`)
  - Context snapshot creation
  - Progress snapshot creation
  - Full session snapshot with metadata
  - Pre-compaction archive creation
  - Summary of all backup locations

---

## Validation Phase

**See:** [12-pre-compaction-checklist-part3-backup-validation.md](12-pre-compaction-checklist-part3-backup-validation.md)

Contents:
- Complete Validation Script (`run_all_validations.sh`)
  - Structure validation
  - Content validation
  - Consistency validation
  - Recovery validation
  - Validation summary with error count

---

## Final Verification

**See:** [12-pre-compaction-checklist-part4-verification-decision.md](12-pre-compaction-checklist-part4-verification-decision.md)

Contents:
- Restoration Test Script (`test_restoration.sh`)
  - Get latest snapshot
  - Create test directory
  - Copy and read file tests
  - Validate file content
  - Cleanup and result reporting

---

## Go/No-Go Decision

**See:** [12-pre-compaction-checklist-part4-verification-decision.md](12-pre-compaction-checklist-part4-verification-decision.md)

Contents:
- Decision Matrix Template
  - Critical criteria (all must be YES)
  - Warning conditions (review but may proceed)
  - No-go conditions (stop if present)
  - Final decision format

---

## Examples

**See:** [12-pre-compaction-checklist-part4-verification-decision.md](12-pre-compaction-checklist-part4-verification-decision.md)

Contents:
- Example 1: Complete Checklist Execution (`execute_checklist.sh`)
  - Full automated execution of all phases
  - Phase-by-phase execution with stop on failure
- Example 2: Checklist with Stop Points (`checklist_with_stops.sh`)
  - Manual approval between each phase
  - Interactive confirmation prompts

---

## Quick Reference

| Phase | Script | Purpose |
|-------|--------|---------|
| Preparation | `prepare_context.sh` | Document current context |
| Preparation | `extract_patterns.sh` | Save patterns before compaction |
| Preparation | `review_progress.sh` | Review task status |
| Backup | `create_all_backups.sh` | Create all required backups |
| Validation | `run_all_validations.sh` | Run all validation checks |
| Verification | `test_restoration.sh` | Test restoration capability |
| Execution | `execute_checklist.sh` | Run complete checklist |
| Execution | `checklist_with_stops.sh` | Run with manual approvals |

---

## Critical Rules

1. **NEVER skip the checklist** - Every compaction requires full checklist completion
2. **STOP on any failure** - Do not proceed if any critical check fails
3. **Document everything** - Fill in all checklist fields
4. **Test restoration** - Always verify recovery capability before proceeding
5. **Archive completed checklists** - Keep records of all compaction events
