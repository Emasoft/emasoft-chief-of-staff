# Session Memory Lifecycle

## Table of Contents

- [Overview](#overview) - The three phases of session memory
- [Phase 1: Session Initialization (Load)](#phase-1-session-initialization-load) - Loading memory at session start
- [Phase 2: Session Execution (Update)](#phase-2-session-execution-update) - Updating memory during work
- [Phase 3: Session Termination (Save)](#phase-3-session-termination-save) - Saving memory before exit

---

## Overview

Session memory follows a three-phase lifecycle: initialization (load), execution (update), and termination (save). Each phase has specific responsibilities and timing requirements.

## Phase 1: Session Initialization (Load)

**Order of operations:**
1. Check if `design/memory/` directory exists
2. Load `activeContext.md` if present
3. Load `patterns.md` if present
4. Load `progress.md` if present
5. Verify all loaded data is valid and consistent
6. Report session state to the user

**When to initialize:** At session start, when resuming work, after context compaction, or when recovering from interruptions.

## Phase 2: Session Execution (Update)

**During work, memory is updated:**
1. After completing each logical step
2. When discovering new patterns
3. When task status changes
4. When making architectural decisions
5. When encountering blockers

## Phase 3: Session Termination (Save)

**Order of operations:**
1. Ensure all updates have been written to disk
2. Verify the memory files are not corrupted
3. Check that all critical state is captured
4. Confirm the session can be resumed from this point

---

**Version:** 1.0
**Last Updated:** 2025-02-03
