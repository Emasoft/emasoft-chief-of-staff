# Session Memory File Recovery: Advanced Recovery and Prevention

## Table of Contents

1. [Advanced Recovery Procedures](#advanced-recovery-procedures)
   - 1.1 [PROCEDURE 4: Partial Recovery](#procedure-4-partial-recovery)
   - 1.2 [PROCEDURE 5: Emergency Manual Reconstruction](#procedure-5-emergency-manual-reconstruction)
2. [Prevention Strategies](#prevention-strategies)
   - 2.1 [Strategy 1: Automatic Backups](#strategy-1-automatic-backups)
   - 2.2 [Strategy 2: Atomic Writes](#strategy-2-atomic-writes)
   - 2.3 [Strategy 3: Validation After Write](#strategy-3-validation-after-write)
   - 2.4 [Strategy 4: Keep Multiple Backup Generations](#strategy-4-keep-multiple-backup-generations)
3. [Examples](#examples)
   - 3.1 [Example 1: Detecting and Recovering from Truncation](#example-1-detecting-and-recovering-from-truncation)
   - 3.2 [Example 2: Reconstructing from Conversation History](#example-2-reconstructing-from-conversation-history)
   - 3.3 [Example 3: Partial Recovery with Section Merge](#example-3-partial-recovery-with-section-merge)
4. [Troubleshooting](#troubleshooting)
   - 4.1 [All backups are also corrupted](#issue-all-backups-are-also-corrupted)
   - 4.2 [Cannot determine which sections are valid](#issue-cannot-determine-which-sections-are-valid)
   - 4.3 [Recovered file missing recent work](#issue-recovered-file-missing-recent-work)
   - 4.4 [Conversation history is not available](#issue-conversation-history-is-not-available)

**Related Parts:**
- [Part 1: Detection and Basic Recovery](13-file-recovery-part1-detection-and-basic-recovery.md) - Overview, corruption types, procedures 1-3

---

## Advanced Recovery Procedures

### PROCEDURE 4: Partial Recovery

**When to use:**
- File is partially corrupted
- Some sections are recoverable
- Other sections are corrupted or truncated

**Steps:**

1. **Identify corrupted sections**
   ```bash
   # Open file and scan for corruption
   cat .atlas/memory/activeContext.md
   ```

2. **Extract valid sections**
   ```bash
   # Copy file to temp location
   cp .atlas/memory/activeContext.md /tmp/activeContext.partial
   ```

3. **Remove corrupted sections**
   - Edit file to remove garbled text
   - Remove incomplete sentences
   - Remove sections with encoding errors

4. **Reconstruct missing sections**
   - Use PROCEDURE 3 for missing parts
   - Or use backup for specific sections
   - Or add placeholder sections

5. **Merge valid and reconstructed sections**
   ```markdown
   # Active Context

   **Last Updated:** 2025-12-31 10:23:45
   **Recovery Note:** Sections 1-2 recovered from original, sections 3-4 reconstructed

   ## Current Task
   [recovered from original file]

   ## Current File
   [reconstructed from conversation]

   ## Recent Decisions
   [recovered from original file]
   ```

6. **Validate merged file**
   ```bash
   mdl .atlas/memory/activeContext.md
   ```

7. **Document recovery process**
   - Note which sections were recovered
   - Note which sections were reconstructed
   - Note any gaps in information

---

### PROCEDURE 5: Emergency Manual Reconstruction

**When to use:**
- All automated recovery methods failed
- No backup exists
- No conversation history available
- Critical to continue work

**Steps:**

1. **Create minimal valid activeContext.md**
   ```markdown
   # Active Context

   **Last Updated:** [current timestamp]
   **Recovery Note:** Emergency reconstruction - ask user for current state

   ## Current Task
   Unknown - awaiting user input

   ## Current File
   Unknown - awaiting user input

   ## Recent Decisions
   None recorded - starting fresh

   ## Pending Operations
   None recorded
   ```

2. **Create minimal valid patterns.md**
   ```markdown
   # Patterns

   **Last Updated:** [current timestamp]
   **Recovery Note:** Emergency reconstruction - patterns will be rediscovered

   ## Code Patterns
   No patterns recorded yet

   ## Architecture Insights
   No insights recorded yet
   ```

3. **Create minimal valid progress.md**
   ```markdown
   # Progress

   **Last Updated:** [current timestamp]
   **Recovery Note:** Emergency reconstruction - ask user for current progress

   ## Todo List
   - [ ] Determine current task status
   - [ ] Rebuild progress tracking

   ## Completed Tasks
   Unknown - awaiting user input

   ## Blocked Tasks
   None recorded
   ```

4. **Ask user for current state**
   - "I've detected corrupted session memory and had to recreate it."
   - "Can you tell me what task you were working on?"
   - "What file were you editing?"
   - "What progress have you made so far?"

5. **Update memory files with user input**
   - Update activeContext.md with current task
   - Update progress.md with current status
   - Document that this is a fresh start

6. **Create backup of reconstructed files**
   ```bash
   timestamp=$(date +%Y%m%d-%H%M%S)
   cp .atlas/memory/activeContext.md .atlas/memory/backups/activeContext.md.backup.$timestamp
   cp .atlas/memory/patterns.md .atlas/memory/backups/patterns.md.backup.$timestamp
   cp .atlas/memory/progress.md .atlas/memory/backups/progress.md.backup.$timestamp
   ```

---

## Prevention Strategies

### Strategy 1: Automatic Backups

**Implementation:**
```bash
# Create backup before every write
backup_before_write() {
  file=$1
  timestamp=$(date +%Y%m%d-%H%M%S)
  cp "$file" "$file.backup.$timestamp"
}

# Use in update procedures
backup_before_write .atlas/memory/activeContext.md
# Then write new content
```

**Schedule:** Before every memory update

---

### Strategy 2: Atomic Writes

**Implementation:**
```bash
# Write to temp file first, then move
write_atomic() {
  file=$1
  content=$2

  # Write to temp file
  echo "$content" > "$file.tmp"

  # Validate temp file
  if mdl "$file.tmp"; then
    # Move to final location (atomic operation)
    mv "$file.tmp" "$file"
  else
    echo "ERROR: Invalid content, not writing"
    rm "$file.tmp"
  fi
}
```

**Benefit:** Prevents partial writes from corruption

---

### Strategy 3: Validation After Write

**Implementation:**
```bash
# Always validate after writing
write_and_validate() {
  file=$1
  content=$2

  echo "$content" > "$file"

  if ! mdl "$file"; then
    echo "ERROR: Written file is invalid, restoring backup"
    latest_backup=$(ls -t "$file.backup."* | head -1)
    cp "$latest_backup" "$file"
  fi
}
```

---

### Strategy 4: Keep Multiple Backup Generations

**Implementation:**
```bash
# Keep last 10 backups, delete older ones
manage_backups() {
  file=$1
  max_backups=10

  # Create new backup
  timestamp=$(date +%Y%m%d-%H%M%S)
  cp "$file" "$file.backup.$timestamp"

  # Delete old backups
  ls -t "$file.backup."* | tail -n +$((max_backups + 1)) | xargs rm -f
}
```

---

## Examples

### Example 1: Detecting and Recovering from Truncation

**Scenario:** Agent was interrupted while writing activeContext.md

**Detection:**
```bash
$ cat .atlas/memory/activeContext.md
# Active Context

**Current Task:** Implement authentication system

## Recent Decisions

1. Use JWT tokens
2. Store in httpOnly
```

**Recovery:**
```bash
# File ends abruptly - truncation detected
# Find backup
$ ls -t .atlas/memory/backups/activeContext.md.backup.* | head -1
.atlas/memory/backups/activeContext.md.backup.20251231-102300

# Restore
$ cp .atlas/memory/backups/activeContext.md.backup.20251231-102300 \
     .atlas/memory/activeContext.md

# Verify
$ tail -20 .atlas/memory/activeContext.md
# Should show complete file
```

---

### Example 2: Reconstructing from Conversation History

**Scenario:** No backup exists, need to rebuild from conversation

**Conversation excerpt:**
```
User: Implement the login endpoint
Agent: I'll create the login endpoint in src/auth/routes.py
Agent: I've added JWT token generation using the PyJWT library
Agent: Testing the endpoint now...
```

**Reconstruction:**
```markdown
# Active Context

**Last Updated:** 2025-12-31 10:45:00
**Recovery Note:** Reconstructed from conversation history

## Current Task
Implement login endpoint in auth system

## Current File
src/auth/routes.py

## Recent Decisions
- Use JWT tokens for authentication
- Use PyJWT library for token generation
- Endpoint is /api/auth/login

## Pending Operations
- Testing login endpoint
```

---

### Example 3: Partial Recovery with Section Merge

**Scenario:** Some sections corrupted, others valid

**Corrupted file:**
```markdown
# Active Context

**Current Task:** �����������

## Current File
src/api/users.py

## Recent Decisions
Valid content here about using SQLAlchemy
```

**Recovery:**
```bash
# Keep valid sections
valid_decisions=$(sed -n '/## Recent Decisions/,/## /p' .atlas/memory/activeContext.md)

# Reconstruct corrupted sections from conversation
current_task="Implement user CRUD endpoints"

# Merge
cat > .atlas/memory/activeContext.md << EOF
# Active Context

**Last Updated:** $(date -Iseconds)
**Recovery Note:** Task section reconstructed, decisions section recovered

## Current Task
$current_task

## Current File
src/api/users.py

$valid_decisions
EOF
```

---

## Troubleshooting

### Issue: All backups are also corrupted

**Symptoms:**
- Every backup file has the same corruption
- Cannot find any valid backup

**Cause:** Corruption happened long ago and propagated to all backups

**Solution:**
1. Use PROCEDURE 3 (reconstruct from conversation)
2. Or use PROCEDURE 5 (emergency reconstruction)
3. Ask user for current state
4. Start fresh session memory

---

### Issue: Cannot determine which sections are valid

**Symptoms:**
- File appears to have content but it's nonsensical
- Cannot tell what is real vs corrupted

**Cause:** Content corruption rather than syntax corruption

**Solution:**
1. Assume entire file is corrupted
2. Use PROCEDURE 2 (restore from backup)
3. If no backup, use PROCEDURE 5 (emergency reconstruction)
4. Do not try to salvage corrupted content

---

### Issue: Recovered file missing recent work

**Symptoms:**
- Backup restored successfully
- But last 2 hours of work is not in backup

**Cause:** Backup was created before recent work

**Solution:**
1. Accept data loss for work after backup
2. Use PROCEDURE 3 to reconstruct recent work from conversation
3. Ask user what was done after backup timestamp
4. Implement more frequent backups going forward

---

### Issue: Conversation history is not available

**Symptoms:**
- No backup exists
- Cannot access conversation history
- PROCEDURE 3 cannot be used

**Cause:** Conversation was cleared or is not persisted

**Solution:**
1. Use PROCEDURE 5 (emergency reconstruction)
2. Ask user directly for current state
3. Start fresh session memory
4. Document that previous session was lost

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Target Audience:** Atlas Orchestrator Agents
**Related:** [Part 1: Detection and Basic Recovery](13-file-recovery-part1-detection-and-basic-recovery.md), SKILL.md (Troubleshooting section)
