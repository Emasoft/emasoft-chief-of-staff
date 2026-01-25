# Manage Active Context

## Table of Contents
1. [When you need to understand the purpose](#purpose)
2. [Understanding what active context is](#what-is-active-context)
3. [When to update context](#context-update-triggers)
4. [How to update context](#update-procedures) → [Part 1: Update Procedures](./03-manage-active-context-part1-update-procedures.md)
5. [Creating context snapshots](#context-snapshots) → [Part 2: Snapshots and Pruning](./03-manage-active-context-part2-snapshots-pruning.md)
6. [When pruning old context](#context-pruning) → [Part 2: Snapshots and Pruning](./03-manage-active-context-part2-snapshots-pruning.md)
7. [For implementation examples](#examples) → [Part 3: Examples](./03-manage-active-context-part3-examples.md)
8. [If issues occur](#troubleshooting) → [Part 4: Troubleshooting](./03-manage-active-context-part4-troubleshooting.md)

---

## Purpose

Active context management maintains a living record of the orchestrator's current focus, recent decisions, and open questions. This enables:
- Quick recovery after compaction
- Coherent decision-making across sessions
- Audit trail of major decisions
- Identification of unresolved blockers

---

## What is Active Context

Active context consists of four primary components:

### 1. Current Focus
**Definition**: The primary task or goal currently being worked on.

**Content**:
- Main objective
- Secondary objectives
- Immediate next steps
- Why this focus was chosen

**Example**:
```markdown
## Current Focus
- **Primary**: Implement user authentication system
  - OAuth2 integration with GitHub
  - Session management
  - Permission levels
- **Secondary**: Update documentation for new auth flow
- **Next Steps**: Complete OAuth callback handler
```

### 2. Recent Decisions
**Definition**: Important decisions made that affect ongoing work.

**Content**:
- What was decided
- Why it was decided (rationale)
- Alternatives considered
- Impact on other components

**Example**:
```markdown
## Recent Decisions
- **Decision**: Use JWT tokens instead of session cookies
  - **Rationale**: Better support for API clients and mobile apps
  - **Alternatives**: Server-side sessions (rejected - scaling concerns)
  - **Impact**: Requires token refresh mechanism
```

### 3. Open Questions
**Definition**: Unresolved questions or blockers awaiting input.

**Content**:
- The question
- Why it's important
- What's blocked by it
- Who can answer it

**Example**:
```markdown
## Open Questions
- **Q**: Should token expiry be 1 hour or 24 hours?
  - **Importance**: Security vs. UX tradeoff
  - **Blocked**: Token refresh implementation
  - **Needs**: User preference or security policy decision
```

### 4. Context Notes
**Definition**: Additional information important to preserve.

**Content**:
- Relevant file paths
- Key variable names
- External dependencies
- Important URLs or references

**Example**:
```markdown
## Context Notes
- Auth implementation: `src/auth/oauth.ts`
- Config file: `.env` (gitignored - has client secrets)
- GitHub OAuth docs: https://docs.github.com/en/apps/oauth-apps
- Test user: testuser@example.com (password in password manager)
```

---

## Context Update Triggers

Update active context when:

### Trigger 1: Starting New Task
**When**: Beginning work on a new task or switching focus

**Action**: Update Current Focus section

**Procedure**:
1. Read current active_context.md
2. Move old focus to Recent Decisions (if decision was made about it)
3. Write new focus
4. Update timestamp

### Trigger 2: Making Important Decision
**When**: Making a decision that affects future work

**Action**: Add to Recent Decisions section

**Procedure**:
1. Document the decision
2. Explain rationale
3. Note alternatives considered
4. Identify impact areas

### Trigger 3: Encountering Blocker
**When**: Hitting a blocker or question that requires external input

**Action**: Add to Open Questions section

**Procedure**:
1. Formulate the question clearly
2. Explain why it matters
3. Note what's blocked
4. Identify who can resolve it

### Trigger 4: Resolving Question
**When**: An open question gets answered

**Action**: Remove from Open Questions, add decision to Recent Decisions

**Procedure**:
1. Document the answer
2. Move from Open Questions to Recent Decisions
3. Note who provided the answer
4. Update affected tasks

### Trigger 5: Context Getting Large
**When**: active_context.md exceeds ~500 lines or becomes unwieldy

**Action**: Prune old content, create snapshot

**Procedure**:
1. Create snapshot of current context
2. Archive old decisions (>7 days old) to patterns
3. Remove resolved questions
4. Keep only recent focus and active decisions

---

## Update Procedures

For detailed bash scripts and procedures to update active context, see:

**[Part 1: Update Procedures](./03-manage-active-context-part1-update-procedures.md)**

Contents:
- Procedure 1: Update Current Focus - bash script to update focus section
- Procedure 2: Add Decision to Recent Decisions - append decision with timestamp
- Procedure 3: Add Open Question - add new question with status tracking
- Procedure 4: Resolve Open Question - move from questions to decisions

---

## Context Snapshots

For snapshot creation procedures and timing, see:

**[Part 2: Snapshots and Pruning](./03-manage-active-context-part2-snapshots-pruning.md)**

Contents:
- When to Create Snapshots - timing guidelines
- Snapshot Procedure - bash script for timestamped snapshots
- Automatic cleanup of old snapshots (keeps last 10)

---

## Context Pruning

For pruning procedures and safety checklists, see:

**[Part 2: Snapshots and Pruning](./03-manage-active-context-part2-snapshots-pruning.md)**

Contents:
- When to Prune - size and age thresholds
- Pruning Procedure - safe pruning with backup
- Safe Pruning Checklist - verification before pruning

---

## Examples

For complete workflow examples and templates, see:

**[Part 3: Examples](./03-manage-active-context-part3-examples.md)**

Contents:
- Example 1: Complete Context Update Workflow - full task lifecycle
- Example 2: Context Recovery After Compaction - restore from snapshot
- Example 3: Structured Context Template - copy-paste template for new contexts

---

## Troubleshooting

For common problems and solutions, see:

**[Part 4: Troubleshooting](./03-manage-active-context-part4-troubleshooting.md)**

Contents:
- Problem: Context File Too Large - archiving and pruning solutions
- Problem: Lost Context After Compaction - recovery from archives
- Problem: Duplicate Information in Context - consolidation steps
- Problem: Cannot Find Recent Decision - search procedures
- Problem: Open Questions Never Get Resolved - tracking improvements
- Problem: Context Updates Conflict with Active Work - atomic update pattern
