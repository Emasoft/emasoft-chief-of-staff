# Session Memory File Recovery: Detection and Basic Recovery

## Table of Contents

1. [Overview](#overview)
   - 1.1 [What Is Memory File Recovery?](#what-is-memory-file-recovery)
   - 1.2 [Why Recovery Matters](#why-recovery-matters)
2. [Types of Memory File Corruption](#types-of-memory-file-corruption)
   - 2.1 [Type 1: Syntax Corruption](#type-1-syntax-corruption)
   - 2.2 [Type 2: Content Corruption](#type-2-content-corruption)
   - 2.3 [Type 3: Truncation Corruption](#type-3-truncation-corruption)
   - 2.4 [Type 4: Complete Loss](#type-4-complete-loss)
3. [Basic Recovery Procedures](#recovery-procedures)
   - 3.1 [PROCEDURE 1: Detect Corruption](#procedure-1-detect-corruption)
   - 3.2 [PROCEDURE 2: Restore from Backup](#procedure-2-restore-from-backup)
   - 3.3 [PROCEDURE 3: Reconstruct from Conversation History](#procedure-3-reconstruct-from-conversation-history)

**Related Parts:**
- [Part 2: Advanced Recovery and Prevention](13-file-recovery-part2-advanced-recovery-and-prevention.md) - Partial recovery, emergency reconstruction, prevention strategies, examples, troubleshooting

---

## Overview

### What Is Memory File Recovery?

Memory file recovery is the process of restoring corrupted, deleted, or invalid session memory files back to a usable state. Session memory files (activeContext.md, patterns.md, progress.md) can become corrupted due to interrupted writes, invalid content, or filesystem errors.

### Why Recovery Matters

**Without recovery:**
- Agent cannot resume work from previous session
- All discovered patterns are lost
- Task progress tracking is reset
- Work continuity is broken

**With recovery:**
- Work resumes from last known good state
- Minimal data loss
- Session continuity maintained
- Patterns and progress preserved

---

## Types of Memory File Corruption

### Type 1: Syntax Corruption

**Description:** File has invalid Markdown syntax or malformed structure.

**Symptoms:**
- Markdown parser errors
- Missing headers
- Unclosed code blocks
- Broken list formatting

**Example:**
```markdown
# Active Context

**Current Task:** Implement authentication
Missing closing quote: "incomplete string
```

**Severity:** Medium - File is readable but sections may be lost

---

### Type 2: Content Corruption

**Description:** File has valid syntax but invalid or nonsensical content.

**Symptoms:**
- Garbled text
- Mixed character encodings
- Placeholder text like "undefined" or "null"
- Incomplete sentences

**Example:**
```markdown
# Active Context

**Current Task:** �������
**Current File:** /path/to/undefined
**Last Decision:** null
```

**Severity:** High - File is untrustworthy

---

### Type 3: Truncation Corruption

**Description:** File was partially written before interruption.

**Symptoms:**
- Abrupt end mid-sentence
- Missing sections
- File size smaller than expected
- Last modified timestamp during known interruption

**Example:**
```markdown
# Active Context

**Current Task:** Implement authentication system

## Recent Decisions

1. Use JWT tokens for auth
2. Store tokens in httpOnly cookies
3. Implement refresh
```

**Severity:** Medium - Partial data is recoverable

---

### Type 4: Complete Loss

**Description:** File is deleted, empty, or completely unreadable.

**Symptoms:**
- File not found error
- Zero-byte file
- Binary corruption (file shows binary content)

**Severity:** Critical - Full reconstruction required

---

## Recovery Procedures

### PROCEDURE 1: Detect Corruption

**When to use:**
- At session initialization
- After unexpected agent termination
- When memory operations fail
- After filesystem errors

**Steps:**

1. **Check file existence**
   ```bash
   ls -la design/memory/*.md
   ```
   If any file is missing, proceed to PROCEDURE 2

2. **Check file size**
   ```bash
   du -h design/memory/*.md
   ```
   If any file is 0 bytes, it is corrupted

3. **Validate Markdown syntax**
   ```bash
   # Using a Markdown validator
   mdl design/memory/activeContext.md
   mdl design/memory/patterns.md
   mdl design/memory/progress.md
   ```

4. **Check for required sections**
   - activeContext.md must have: "Current Task", "Current File", "Recent Decisions"
   - patterns.md must have: "Code Patterns", "Architecture Insights"
   - progress.md must have: "Todo List", "Completed Tasks"

5. **Validate content coherence**
   - Read first 10 lines and last 10 lines
   - Check for garbled text or encoding errors
   - Verify timestamps are valid ISO format

6. **Report findings**
   - Document which files are corrupted
   - Document corruption type
   - Document last known good state

**Example validation check:**
```bash
#!/bin/bash
for file in design/memory/{activeContext,patterns,progress}.md; do
  if [ ! -f "$file" ]; then
    echo "ERROR: $file is missing"
  elif [ ! -s "$file" ]; then
    echo "ERROR: $file is empty"
  elif ! head -1 "$file" | grep -q "^#"; then
    echo "ERROR: $file has invalid header"
  else
    echo "OK: $file appears valid"
  fi
done
```

---

### PROCEDURE 2: Restore from Backup

**When to use:**
- Corruption detected in PROCEDURE 1
- Backup files exist
- Backup is more recent than last known good state

**Steps:**

1. **Locate backup files**
   ```bash
   ls -lt design/memory/backups/
   ```
   Backups should be named: `activeContext.md.backup.TIMESTAMP`

2. **Identify most recent backup**
   ```bash
   latest_backup=$(ls -t design/memory/backups/activeContext.md.backup.* | head -1)
   echo "Most recent backup: $latest_backup"
   ```

3. **Verify backup integrity**
   ```bash
   # Check backup file is not corrupted
   head -10 "$latest_backup"
   tail -10 "$latest_backup"
   ```

4. **Restore from backup**
   ```bash
   cp "$latest_backup" design/memory/activeContext.md
   ```

5. **Verify restoration**
   ```bash
   # Re-run validation from PROCEDURE 1
   mdl design/memory/activeContext.md
   ```

6. **Repeat for other corrupted files**
   ```bash
   # Restore patterns.md if needed
   latest_patterns=$(ls -t design/memory/backups/patterns.md.backup.* | head -1)
   cp "$latest_patterns" design/memory/patterns.md

   # Restore progress.md if needed
   latest_progress=$(ls -t design/memory/backups/progress.md.backup.* | head -1)
   cp "$latest_progress" design/memory/progress.md
   ```

7. **Update session state**
   - Load restored files
   - Review what work was captured in backup
   - Identify any work done after backup that is now lost
   - Document recovery in activeContext.md

**Example restoration script:**
```bash
#!/bin/bash
for file in activeContext patterns progress; do
  if [ ! -s "design/memory/$file.md" ]; then
    latest=$(ls -t design/memory/backups/$file.md.backup.* 2>/dev/null | head -1)
    if [ -n "$latest" ]; then
      echo "Restoring $file.md from $latest"
      cp "$latest" "design/memory/$file.md"
    else
      echo "ERROR: No backup found for $file.md"
    fi
  fi
done
```

---

### PROCEDURE 3: Reconstruct from Conversation History

**When to use:**
- No backup exists
- Backup is too old to be useful
- Need to recover recent work not in backup

**Steps:**

1. **Locate conversation history**
   - Conversation history is maintained by Claude Code
   - May be in session logs or context window

2. **Identify relevant information**
   - Search for mentions of current task
   - Search for file paths being edited
   - Search for decisions made
   - Search for discovered patterns

3. **Extract task information for progress.md**
   - Find all "completed" or "working on" statements
   - Extract task names and status
   - Build todo list from conversation

4. **Extract context information for activeContext.md**
   - Find most recent file being edited
   - Find most recent decision made
   - Find current line number if mentioned
   - Find any pending operations

5. **Extract pattern information for patterns.md**
   - Find statements like "I noticed a pattern..."
   - Find code examples shared
   - Find architecture decisions discussed

6. **Write reconstructed files**
   ```bash
   # Create new activeContext.md with extracted info
   cat > design/memory/activeContext.md << 'EOF'
   # Active Context

   **Last Updated:** [current timestamp]
   **Recovery Note:** Reconstructed from conversation history

   ## Current Task
   [extracted task]

   ## Current File
   [extracted file path]

   ## Recent Decisions
   [extracted decisions]
   EOF
   ```

7. **Verify reconstruction**
   - Ask user to confirm extracted information is correct
   - Update any incorrect information
   - Document what could not be recovered

**Example conversation parsing:**
```python
# Pseudo-code for extracting information
conversation_text = read_conversation_history()

# Extract tasks
tasks = []
for line in conversation_text.split('\n'):
    if 'completed' in line.lower() or 'finished' in line.lower():
        tasks.append(extract_task_from(line))

# Extract current file
current_file = None
for line in reversed(conversation_text.split('\n')):
    if '/path/' in line or '.py' in line or '.md' in line:
        current_file = extract_filepath_from(line)
        break

# Build progress.md from extracted tasks
write_progress_md(tasks)
```

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Target Audience:** Chief of Staff Agents
**Related:** [Part 2: Advanced Recovery and Prevention](13-file-recovery-part2-advanced-recovery-and-prevention.md)
