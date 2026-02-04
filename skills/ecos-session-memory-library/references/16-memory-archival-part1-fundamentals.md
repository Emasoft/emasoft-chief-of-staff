# Memory Archival Fundamentals

## Table of Contents

1. [When you need to understand the overview](#overview)
2. [When to archive](#when-to-archive)
   - [File size threshold](#trigger-1-file-size-threshold)
   - [Completed task accumulation](#trigger-2-completed-task-accumulation)
   - [Pattern obsolescence](#trigger-3-pattern-obsolescence)
   - [Session milestones](#trigger-4-session-milestone)
   - [Performance degradation](#trigger-5-performance-degradation)
3. [What to archive](#what-to-archive)
   - [Archive candidates from progress.md](#archive-candidates-from-progressmd)
   - [Archive candidates from patterns.md](#archive-candidates-from-patternsmd)
   - [Archive candidates from activeContext.md](#archive-candidates-from-activecontextmd)
4. [How to archive completed tasks](#procedure-1-archive-completed-tasks)
5. [How to archive old patterns](#procedure-2-archive-old-patterns)

**Related:** See [16-memory-archival-part2-examples.md](16-memory-archival-part2-examples.md) for advanced operations, snapshots, restoration, and troubleshooting.

---

## Overview

### What Is Memory Archival?

Memory archival is the process of moving completed, outdated, or no-longer-active session memory content to separate archive files. This keeps the active memory files (activeContext.md, patterns.md, progress.md) lean and fast-loading while preserving historical information for future reference.

### Why Archive?

**Without archival:**
- Memory files grow to hundreds of kilobytes
- Session initialization becomes slow
- Finding current information is difficult
- Memory operations are sluggish
- Historical data is lost when files are cleaned

**With archival:**
- Active memory stays under 50KB per file
- Fast session initialization
- Current information is easy to find
- Historical data is preserved
- Can review past decisions and patterns

---

## When to Archive

### Trigger 1: File Size Threshold

**Archive when:**
- activeContext.md exceeds 100KB
- patterns.md exceeds 150KB
- progress.md exceeds 200KB

**How to check:**
```bash
du -k design/memory/*.md | while read size file; do
  if [ $size -gt 100 ]; then
    echo "Archive needed: $file is ${size}KB"
  fi
done
```

---

### Trigger 2: Completed Task Accumulation

**Archive when:**
- More than 50 tasks in Completed Tasks section
- Completed tasks are older than 30 days
- Completed tasks section is longer than Todo List section

**How to check:**
```bash
completed_count=$(grep -c "^- \[x\]" design/memory/progress.md)
if [ $completed_count -gt 50 ]; then
  echo "Archive needed: $completed_count completed tasks"
fi
```

---

### Trigger 3: Pattern Obsolescence

**Archive when:**
- Patterns are no longer relevant to current work
- Patterns are over 90 days old
- Patterns contradict newer patterns

**How to check:**
```python
from datetime import datetime, timedelta

patterns = extract_patterns(patterns_md)
now = datetime.now()

for pattern in patterns:
    age = now - datetime.fromisoformat(pattern.discovered_at)
    if age > timedelta(days=90):
        print(f"Archive candidate: {pattern.name} (age: {age.days} days)")
```

---

### Trigger 4: Session Milestone

**Archive when:**
- Major project milestone reached
- Before starting new major feature
- After project phase completion
- Before long project hiatus

---

### Trigger 5: Performance Degradation

**Archive when:**
- Session initialization takes > 5 seconds
- Memory updates take > 2 seconds
- File operations are noticeably slow

---

## What to Archive

### Archive Candidates from progress.md

**Archive:**
- Completed tasks older than 30 days
- Cancelled tasks older than 14 days
- Tasks from completed milestones
- Historical task metadata

**Keep:**
- Active tasks (pending, in progress, blocked)
- Recently completed tasks (last 30 days)
- Tasks needed for dependency tracking
- Current milestone tasks

---

### Archive Candidates from patterns.md

**Archive:**
- Patterns not referenced in last 60 days
- Patterns superseded by newer patterns
- Patterns from completed project phases
- Deprecated patterns

**Keep:**
- Actively used patterns
- Recent patterns (last 60 days)
- Patterns referenced by current work
- Core architectural patterns

---

### Archive Candidates from activeContext.md

**Archive:**
- Decisions older than 60 days
- Historical context no longer relevant
- Old file navigation history
- Superseded decisions

**Keep:**
- Current task information
- Recent decisions (last 60 days)
- Active context needed for current work
- Recent file history

---

## PROCEDURE 1: Archive Completed Tasks

**When to use:**
- Completed tasks section has > 50 tasks
- Oldest completed task is > 30 days old
- progress.md file size exceeds 200KB

**Steps:**

1. **Create archive directory if needed**
   ```bash
   mkdir -p design/memory/archive/$(date +%Y)
   ```

2. **Extract tasks to archive**
   ```python
   from datetime import datetime, timedelta

   completed_tasks = extract_completed_tasks(progress_md)
   cutoff_date = datetime.now() - timedelta(days=30)

   tasks_to_archive = [
       task for task in completed_tasks
       if datetime.fromisoformat(task.completed_at) < cutoff_date
   ]
   ```

3. **Create archive file with metadata**
   ```bash
   archive_file="design/memory/archive/$(date +%Y)/completed-tasks-$(date +%Y%m).md"

   cat > "$archive_file" << 'EOF'
   # Archived Completed Tasks

   **Archive Date:** $(date -Iseconds)
   **Archive Period:** Tasks completed before $(date -d "30 days ago" +%Y-%m-%d)
   **Task Count:** ${#tasks_to_archive[@]}

   ## Archived Tasks
   EOF
   ```

4. **Write archived tasks to archive file**
   ```python
   with open(archive_file, 'a') as f:
       for task in tasks_to_archive:
           f.write(f"\n- [x] {task.name} (completed {task.completed_at})\n")
           if task.completion_note:
               f.write(f"  - {task.completion_note}\n")
   ```

5. **Remove archived tasks from progress.md**
   ```python
   # Keep only recent completed tasks
   recent_tasks = [
       task for task in completed_tasks
       if datetime.fromisoformat(task.completed_at) >= cutoff_date
   ]

   # Rewrite Completed Tasks section
   update_completed_tasks_section(progress_md, recent_tasks)
   ```

6. **Update progress.md header with archive note**
   ```markdown
   # Progress

   **Last Updated:** 2025-12-31 15:00:00
   **Last Archived:** 2025-12-31 15:00:00 (moved 45 tasks to archive/2025/completed-tasks-202512.md)
   ```

7. **Verify archival**
   ```bash
   # Check archive file was created
   ls -lh "$archive_file"

   # Check tasks were removed from progress.md
   new_count=$(grep -c "^- \[x\]" design/memory/progress.md)
   echo "Completed tasks remaining: $new_count"

   # Check file size reduced
   du -h design/memory/progress.md
   ```

**Example archived file:**
```markdown
# Archived Completed Tasks

**Archive Date:** 2025-12-31T15:00:00
**Archive Period:** Tasks completed before 2025-12-01
**Task Count:** 45

## Archived Tasks

- [x] Implement login endpoint (completed 2025-11-15T10:30:00)
  - Added JWT token generation, validation, and refresh logic
- [x] Add unit tests for authentication (completed 2025-11-15T14:00:00)
  - Created 15 test cases covering all auth scenarios
- [x] Implement password reset flow (completed 2025-11-18T09:15:00)
  - Email-based reset with secure token generation
```

---

## PROCEDURE 2: Archive Old Patterns

**When to use:**
- patterns.md exceeds 150KB
- Many patterns are no longer referenced
- Patterns from old project phases exist

**Steps:**

1. **Analyze pattern usage**
   ```python
   patterns = extract_patterns(patterns_md)
   codebase_files = glob('src/**/*.py', recursive=True)

   for pattern in patterns:
       references = 0
       for file in codebase_files:
           content = read_file(file)
           if pattern.name in content or pattern.keywords in content:
               references += 1

       pattern.reference_count = references
       pattern.last_referenced = find_last_reference(pattern)
   ```

2. **Identify patterns to archive**
   ```python
   from datetime import datetime, timedelta

   cutoff_date = datetime.now() - timedelta(days=60)

   patterns_to_archive = [
       pattern for pattern in patterns
       if pattern.reference_count == 0
       or datetime.fromisoformat(pattern.last_referenced) < cutoff_date
   ]
   ```

3. **Create pattern archive**
   ```bash
   archive_file="design/memory/archive/$(date +%Y)/patterns-$(date +%Y%m).md"

   cat > "$archive_file" << 'EOF'
   # Archived Patterns

   **Archive Date:** $(date -Iseconds)
   **Archive Reason:** Patterns no longer actively referenced
   **Pattern Count:** ${#patterns_to_archive[@]}

   ## Archived Patterns
   EOF
   ```

4. **Write archived patterns**
   ```python
   with open(archive_file, 'a') as f:
       for pattern in patterns_to_archive:
           f.write(f"\n### Pattern: {pattern.name}\n")
           f.write(f"**Discovered:** {pattern.discovered_at}\n")
           f.write(f"**Last Referenced:** {pattern.last_referenced}\n")
           f.write(f"**Reference Count:** {pattern.reference_count}\n\n")
           f.write(f"{pattern.description}\n\n")
           if pattern.example:
               f.write(f"```{pattern.language}\n{pattern.example}\n```\n\n")
   ```

5. **Remove archived patterns from patterns.md**
   ```python
   active_patterns = [
       pattern for pattern in patterns
       if pattern not in patterns_to_archive
   ]

   rewrite_patterns_file(patterns_md, active_patterns)
   ```

6. **Update patterns.md header**
   ```markdown
   # Patterns

   **Last Updated:** 2025-12-31 15:30:00
   **Last Archived:** 2025-12-31 15:30:00 (moved 12 patterns to archive/2025/patterns-202512.md)
   **Active Patterns:** 8
   ```

7. **Verify archival**
   ```bash
   # Check archive created
   ls -lh "$archive_file"

   # Check file size reduced
   du -h design/memory/patterns.md

   # Check pattern count
   grep -c "^### Pattern:" design/memory/patterns.md
   ```

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Target Audience:** Chief of Staff Agents
**Related:** [16-memory-archival-part2-examples.md](16-memory-archival-part2-examples.md)
