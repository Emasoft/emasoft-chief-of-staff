# Progress Validation - Index

This document was split into multiple parts for better maintainability.

## Parts

### Part 1: Rules and Basic Procedures
**File:** [15-progress-validation-part1-rules-and-basic-procedures.md](15-progress-validation-part1-rules-and-basic-procedures.md)

**Contents:**
1. Overview
   - What Is Progress Validation
   - Why Validation Matters
2. Validation Rules
   - Rule 1: Task Status Integrity
   - Rule 2: Dependency Validity
   - Rule 3: Timestamp Ordering
   - Rule 4: Progress Consistency
   - Rule 5: Completeness Requirements
3. Basic Validation Procedures
   - PROCEDURE 1: Validate Task Status
   - PROCEDURE 2: Validate Dependencies
   - PROCEDURE 3: Validate Timestamps

### Part 2: Advanced Validation and Automation
**File:** [15-progress-validation-part2-advanced-and-automation.md](15-progress-validation-part2-advanced-and-automation.md)

**Contents:**
1. Advanced Validation Procedures
   - PROCEDURE 4: Validate Consistency
   - PROCEDURE 5: Validate Completeness
2. Common Validation Errors
   - Error 1: Task in Multiple States
   - Error 2: Non-existent Dependency
   - Error 3: Timestamp Out of Order
   - Error 4: Missing Completion Timestamp
3. Automated Validation
   - Validation Script
   - Script Usage
4. Examples
   - Validating After Task Completion
5. Troubleshooting
   - Script reports errors but file looks correct
   - Many validation errors after importing tasks

---

**Version:** 1.0
**Last Updated:** 2026-01-08
**Target Audience:** Chief of Staff Agents
**Related:** SKILL.md (PROCEDURE 4: Update Task Progress)
