# Memory Archival Procedures - Detailed Steps

**Parent Document:** [16-memory-archival.md](16-memory-archival.md)

---

## Table of Contents

1. [PROCEDURE 1: Archive Completed Tasks](#procedure-1-archive-completed-tasks)
2. [PROCEDURE 2: Archive Old Patterns](#procedure-2-archive-old-patterns)
3. [PROCEDURE 3: Consolidate Active Context](#procedure-3-consolidate-active-context)
4. [PROCEDURE 4: Create Archival Snapshot](#procedure-4-create-archival-snapshot)
5. [PROCEDURE 5: Restore from Archive](#procedure-5-restore-from-archive)

---

## PROCEDURE 1: Archive Completed Tasks

**When to use:**
- Completed tasks section has > 50 tasks
- Oldest completed task is > 30 days old
- progress.md file size exceeds 200KB

**Steps:**

1. **Create archive directory if needed**
   ```bash
   mkdir -p .atlas/memory/archive/$(date +%Y)
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
   archive_file=".atlas/memory/archive/$(date +%Y)/completed-tasks-$(date +%Y%m).md"

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
   new_count=$(grep -c "^- \[x\]" .atlas/memory/progress.md)
   echo "Completed tasks remaining: $new_count"

   # Check file size reduced
   du -h .atlas/memory/progress.md
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
   archive_file=".atlas/memory/archive/$(date +%Y)/patterns-$(date +%Y%m).md"

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
   du -h .atlas/memory/patterns.md

   # Check pattern count
   grep -c "^### Pattern:" .atlas/memory/patterns.md
   ```

---

## PROCEDURE 3: Consolidate Active Context

**When to use:**
- activeContext.md exceeds 100KB
- Many old decisions accumulated
- File navigation history is very long

**Steps:**

1. **Extract current active information**
   ```python
   current_task = extract_current_task(activeContext_md)
   current_file = extract_current_file(activeContext_md)
   recent_decisions = extract_decisions_since(activeContext_md, days=60)
   recent_files = extract_file_history(activeContext_md, limit=10)
   ```

2. **Archive old decisions**
   ```python
   all_decisions = extract_all_decisions(activeContext_md)
   cutoff = datetime.now() - timedelta(days=60)

   old_decisions = [
       decision for decision in all_decisions
       if datetime.fromisoformat(decision.made_at) < cutoff
   ]
   ```

3. **Create decision archive**
   ```bash
   archive_file=".atlas/memory/archive/$(date +%Y)/decisions-$(date +%Y%m).md"

   cat > "$archive_file" << 'EOF'
   # Archived Decisions

   **Archive Date:** $(date -Iseconds)
   **Archive Period:** Decisions older than 60 days
   **Decision Count:** ${#old_decisions[@]}

   ## Archived Decisions
   EOF
   ```

4. **Write archived decisions**
   ```python
   with open(archive_file, 'a') as f:
       for decision in old_decisions:
           f.write(f"\n### Decision: {decision.title} ({decision.made_at})\n")
           f.write(f"**Context:** {decision.context}\n")
           f.write(f"**Rationale:** {decision.rationale}\n")
           f.write(f"**Impact:** {decision.impact}\n\n")
   ```

5. **Rewrite activeContext.md with only current info**
   ```markdown
   # Active Context

   **Last Updated:** 2025-12-31 16:00:00
   **Last Consolidated:** 2025-12-31 16:00:00
   **Archived Decisions:** See archive/2025/decisions-202512.md

   ## Current Task
   [current task only]

   ## Current File
   [current file only]

   ## Recent Decisions (last 60 days)
   [only recent decisions]

   ## Recent Files (last 10)
   [only recent files]
   ```

6. **Verify consolidation**
   ```bash
   # Check file size reduced
   du -h .atlas/memory/activeContext.md

   # Should be under 50KB
   ```

---

## PROCEDURE 4: Create Archival Snapshot

**When to use:**
- Before major project milestone
- Before long project hiatus
- Before major memory restructuring
- For complete historical record

**Steps:**

1. **Create snapshot directory**
   ```bash
   snapshot_date=$(date +%Y%m%d-%H%M%S)
   snapshot_dir=".atlas/memory/snapshots/$snapshot_date"
   mkdir -p "$snapshot_dir"
   ```

2. **Copy all current memory files**
   ```bash
   cp .atlas/memory/activeContext.md "$snapshot_dir/"
   cp .atlas/memory/patterns.md "$snapshot_dir/"
   cp .atlas/memory/progress.md "$snapshot_dir/"
   cp .atlas/memory/config-snapshot.md "$snapshot_dir/" 2>/dev/null || true
   ```

3. **Create snapshot metadata**
   ```bash
   cat > "$snapshot_dir/SNAPSHOT_INFO.md" << EOF
   # Memory Snapshot

   **Snapshot Date:** $(date -Iseconds)
   **Snapshot Reason:** [milestone/hiatus/restructure]
   **Project Phase:** [current phase]

   ## Snapshot Contents

   - activeContext.md ($(du -h $snapshot_dir/activeContext.md | cut -f1))
   - patterns.md ($(du -h $snapshot_dir/patterns.md | cut -f1))
   - progress.md ($(du -h $snapshot_dir/progress.md | cut -f1))

   ## Project State at Snapshot

   **Current Task:** $(grep "**Current Task:**" $snapshot_dir/activeContext.md)
   **Total Tasks:** $(grep -c "^- \[" $snapshot_dir/progress.md)
   **Completed Tasks:** $(grep -c "^- \[x\]" $snapshot_dir/progress.md)
   **Active Patterns:** $(grep -c "^### Pattern:" $snapshot_dir/patterns.md)
   EOF
   ```

4. **Create compressed archive**
   ```bash
   cd .atlas/memory/snapshots
   tar czf "$snapshot_date.tar.gz" "$snapshot_date/"
   ```

5. **Verify snapshot**
   ```bash
   tar tzf "$snapshot_date.tar.gz"
   ls -lh "$snapshot_date.tar.gz"
   ```

---

## PROCEDURE 5: Restore from Archive

**When to use:**
- Need to review old decisions
- Need to understand past patterns
- Investigating historical task completion
- Recovering from data loss

**Steps:**

1. **Locate relevant archive**
   ```bash
   # List available archives
   ls -lh .atlas/memory/archive/2025/

   # List available snapshots
   ls -lh .atlas/memory/snapshots/
   ```

2. **Extract snapshot if needed**
   ```bash
   snapshot=".atlas/memory/snapshots/20251201-153000.tar.gz"
   extract_dir="/tmp/snapshot-restore"

   mkdir -p "$extract_dir"
   tar xzf "$snapshot" -C "$extract_dir"
   ```

3. **Review archived content**
   ```bash
   # View archived completed tasks
   cat .atlas/memory/archive/2025/completed-tasks-202511.md

   # View archived patterns
   cat .atlas/memory/archive/2025/patterns-202511.md

   # View archived decisions
   cat .atlas/memory/archive/2025/decisions-202511.md
   ```

4. **Extract specific information if needed**
   ```bash
   # Find specific archived task
   grep -A 5 "Implement authentication" .atlas/memory/archive/2025/completed-tasks-*.md

   # Find specific archived pattern
   grep -A 20 "Decorator-based" .atlas/memory/archive/2025/patterns-*.md
   ```

5. **Restore to current memory if needed** (rarely necessary)
   ```bash
   # Only if current memory is lost and archive is most recent
   # Create backup first
   cp .atlas/memory/progress.md .atlas/memory/progress.md.backup

   # Restore archived tasks to current progress.md
   cat .atlas/memory/archive/2025/completed-tasks-202512.md >> .atlas/memory/progress.md
   ```

---

**Version:** 1.0
**Last Updated:** 2026-01-01
**Parent:** [16-memory-archival.md](16-memory-archival.md)
