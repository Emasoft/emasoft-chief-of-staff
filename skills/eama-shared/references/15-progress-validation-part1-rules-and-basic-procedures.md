# Progress Validation - Part 1: Rules and Basic Procedures

## Table of Contents

1. [When you need to understand the overview](#overview)
   - 1.1 [What Is Progress Validation](#what-is-progress-validation)
   - 1.2 [Why Validation Matters](#why-validation-matters)
2. [Understanding validation rules](#validation-rules) - See [Section 1: Validation Rules](15-progress-validation-part1-rules-and-basic-procedures-section1-validation-rules.md)
   - 2.1 Rule 1: Task Status Integrity
   - 2.2 Rule 2: Dependency Validity
   - 2.3 Rule 3: Timestamp Ordering
   - 2.4 Rule 4: Progress Consistency
   - 2.5 Rule 5: Completeness Requirements
3. [Basic validation procedures](#validation-procedures) - See [Section 2: Validation Procedures](15-progress-validation-part1-rules-and-basic-procedures-section2-validation-procedures.md)
   - 3.1 Validating task status
   - 3.2 Validating dependencies
   - 3.3 Validating timestamps

**Related files:**
- [Part 2: Advanced Validation and Automation](15-progress-validation-part2-advanced-and-automation.md) - Consistency/completeness procedures, common errors, automation

---

## Overview

### What Is Progress Validation?

Progress validation is the systematic verification that the task tracking information in progress.md accurately reflects reality. This includes checking task statuses, dependency relationships, timestamps, and consistency with actual work completed.

### Why Validation Matters

**Without validation:**
- Tasks marked complete but work not done
- Dependencies show as resolved but still blocked
- Timestamps are out of order or invalid
- Duplicate tasks in different states
- Contradictions between todo list and completed list

**With validation:**
- Progress tracking is trustworthy
- Dependencies are correctly managed
- Task history is accurate
- No contradictions or inconsistencies
- Work can be reliably resumed

---

## Validation Rules

For detailed validation rules with code examples, see:
**[Section 1: Validation Rules](15-progress-validation-part1-rules-and-basic-procedures-section1-validation-rules.md)**

Contents:
- Rule 1: Task Status Integrity - A task can be in exactly one state at a time
- Rule 2: Dependency Validity - All task dependencies must reference existing tasks
- Rule 3: Timestamp Ordering - Timestamps must be in chronological order
- Rule 4: Progress Consistency - Overall progress must be consistent with individual task states
- Rule 5: Completeness Requirements - Completed tasks must have all required information

---

## Validation Procedures

For detailed validation procedures with step-by-step instructions, see:
**[Section 2: Validation Procedures](15-progress-validation-part1-rules-and-basic-procedures-section2-validation-procedures.md)**

Contents:
- PROCEDURE 1: Validate Task Status - Extract tasks, check duplicates, verify markers
- PROCEDURE 2: Validate Dependencies - Check existence, cycles, blocked tasks
- PROCEDURE 3: Validate Timestamps - Format validation, chronological order, future/old timestamps

---

**Version:** 1.0
**Last Updated:** 2026-01-08
**Target Audience:** Atlas Orchestrator Agents
**Related:** [Part 2: Advanced Validation and Automation](15-progress-validation-part2-advanced-and-automation.md)
