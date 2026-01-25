# Recovery Troubleshooting

**Parent Document**: [10-recovery-procedures.md](10-recovery-procedures.md)

## Table of Contents

1. [No Snapshots or Archives Available](#problem-no-snapshots-or-archives-available)
2. [Restored State is Outdated](#problem-restored-state-is-outdated)
3. [Validation Fails After Recovery](#problem-validation-fails-after-recovery)
4. [Multiple Recovery Sources Conflict](#problem-multiple-recovery-sources-conflict)
5. [Recovery Scripts Fail](#problem-recovery-scripts-fail)
6. [Permissions Issues](#problem-permissions-issues)
7. [Quick Diagnostic Commands](#quick-diagnostic-commands)

---

## Problem: No Snapshots or Archives Available

**Symptoms:**
- Recovery scripts cannot find any backup sources
- All snapshot directories empty
- No pre-compaction archives exist

**Solution:**

```bash
#!/bin/bash
# reconstruct_without_backups.sh

echo "=== Reconstruction Without Backups ==="

# 1. Mine git history
echo "1. Mining git history..."
if git rev-parse --git-dir > /dev/null 2>&1; then
    git log --all --pretty=format:"%h %s" --since="1 week ago" > /tmp/recent_commits.txt
    echo "Recent commits saved to /tmp/recent_commits.txt"
fi

# 2. Search documentation
echo ""
echo "2. Searching documentation..."
find docs docs_dev -name "*.md" -exec grep -l "progress\|task\|context" {} \; 2>/dev/null

# 3. Create minimal structure
echo ""
echo "3. Creating minimal structure..."
# Use emergency recovery procedure from Part 3
./emergency_recovery.sh

echo ""
echo "Manual reconstruction required from:"
echo "  - Git commit messages"
echo "  - Documentation files"
echo "  - User memory"
```

---

## Problem: Restored State is Outdated

**Symptoms:**
- Archive timestamp is old
- Missing recent changes
- Context doesn't match current work

**Solution:**

```markdown
# Updating Outdated Restored State

## Step 1: Identify the gap

1. Note archive timestamp
2. Note current time
3. Calculate time gap (e.g., "3 hours of work missing")

## Step 2: Fill the gap from sources

1. Review git commits in that period:
   ```bash
   git log --since="3 hours ago" --format="%h %s"
   ```

2. Check any external notes or documentation

3. Review terminal history for commands run

## Step 3: Manually update

1. Add missing decisions to active_context.md
2. Update task statuses in progress_tracker.md
3. Record any patterns discovered

## Step 4: Mark as reconstructed

Add note to context:
```
## Reconstruction Note
- Restored from: [archive path]
- Archive date: [timestamp]
- Gap: [time period]
- Reconstructed: [what was added manually]
```
```

---

## Problem: Validation Fails After Recovery

**Symptoms:**
- Validation script reports errors
- Missing sections in files
- Broken markdown syntax

**Solution:**

```bash
#!/bin/bash
# fix_validation_errors.sh

echo "=== Fixing Validation Errors ==="

# Run validation and capture errors
errors=$(./validate_all.sh 2>&1 | grep "ERROR\|MISSING\|INVALID")

echo "Detected errors:"
echo "$errors"
echo ""

# Fix each type of error
if echo "$errors" | grep -q "Missing section"; then
    echo "Fixing missing sections..."
    # Add missing sections
    if ! grep -q "## Recent Decisions" .session_memory/active_context.md; then
        echo -e "\n## Recent Decisions\n\n[To be filled]\n" >> .session_memory/active_context.md
    fi
fi

if echo "$errors" | grep -q "Broken links"; then
    echo "Fixing broken links..."
    # Remove or update broken links
    sed -i '' 's/\[broken link\](.*)/[removed]/g' .session_memory/*.md
fi

if echo "$errors" | grep -q "Invalid markdown"; then
    echo "Fixing markdown syntax..."
    # Close unclosed code blocks
    for file in .session_memory/*.md; do
        open_blocks=$(grep -c '```' "$file")
        if [ $((open_blocks % 2)) -ne 0 ]; then
            echo '```' >> "$file"
            echo "  Closed code block in $file"
        fi
    done
fi

# Re-run validation
echo ""
echo "Re-running validation..."
./validate_all.sh
```

---

## Problem: Multiple Recovery Sources Conflict

**Symptoms:**
- Snapshot and archive show different states
- Unclear which is more recent
- Different files have different "best" sources

**Solution:**

### Step 1: Compare timestamps

```bash
# Check snapshot timestamps
ls -la .session_memory/snapshots/snapshot_*/metadata.txt

# Check archive timestamps
ls -la .session_memory/archived/pre_compaction_*/timestamp.txt
```

### Step 2: Compare content

```bash
# Diff the sources
diff .session_memory/snapshots/snapshot_latest/active_context.md \
     .session_memory/archived/pre_compaction_3/active_context.md
```

### Step 3: Choose strategy

**Option A: Use most recent as base**
- Restore from most recent source
- Manually add unique information from older source

**Option B: Merge manually**
- Create new file combining both
- Resolve conflicts section by section

**Option C: Per-file selection**
- Use different source for different files
- Based on which file is more complete in each source

### Step 4: Document decision

```markdown
## Recovery Source Selection
- active_context.md: From snapshot_20240101_120000 (more recent)
- progress_tracker.md: From pre_compaction_3 (more complete)
- pattern_index.md: Rebuilt from pattern files
```

---

## Problem: Recovery Scripts Fail

**Symptoms:**
- Scripts exit with errors
- Permission denied
- Command not found

**Solution:**

```bash
#!/bin/bash
# diagnose_script_failure.sh

echo "=== Diagnosing Script Failures ==="

# Check script permissions
echo "1. Checking script permissions..."
for script in *.sh; do
    if [ -x "$script" ]; then
        echo "  OK: $script"
    else
        echo "  FIX: $script (adding execute permission)"
        chmod +x "$script"
    fi
done

# Check bash availability
echo ""
echo "2. Checking bash..."
which bash
bash --version | head -1

# Check required commands
echo ""
echo "3. Checking required commands..."
for cmd in grep sed awk date mkdir cp rm; do
    if command -v $cmd &> /dev/null; then
        echo "  OK: $cmd"
    else
        echo "  MISSING: $cmd"
    fi
done

# Check directory permissions
echo ""
echo "4. Checking directory permissions..."
if [ -w ".session_memory" ]; then
    echo "  OK: .session_memory writable"
else
    echo "  FIX: .session_memory not writable"
    chmod u+w .session_memory
fi
```

---

## Problem: Permissions Issues

**Symptoms:**
- Cannot read/write files
- Permission denied errors
- Files owned by wrong user

**Solution:**

```bash
#!/bin/bash
# fix_permissions.sh

echo "=== Fixing Permissions ==="

# Fix directory permissions
echo "1. Fixing directory permissions..."
find .session_memory -type d -exec chmod 755 {} \;

# Fix file permissions
echo "2. Fixing file permissions..."
find .session_memory -type f -name "*.md" -exec chmod 644 {} \;
find .session_memory -type f -name "*.sh" -exec chmod 755 {} \;

# Fix ownership (if needed)
echo "3. Current ownership..."
ls -la .session_memory/

echo ""
echo "Permissions fixed"
```

---

## Quick Diagnostic Commands

```bash
# Check overall health
ls -la .session_memory/

# Check file sizes (zero = problem)
wc -c .session_memory/*.md

# Check for valid headers
head -1 .session_memory/*.md

# Check available backups
ls -la .session_memory/snapshots/
ls -la .session_memory/archived/

# Check disk space
df -h .
```

---

## Related Documents

- [10-recovery-procedures.md](10-recovery-procedures.md) - Main recovery index
- [Part 4a: Examples](10-recovery-procedures-part4a-examples.md) - Recovery examples
- [Part 1: Failed Compaction](10-recovery-procedures-part1-failed-compaction.md) - Compaction recovery
- [Part 2: Corruption and Context](10-recovery-procedures-part2-corruption-context.md) - File recovery
- [Part 3: Emergency Recovery](10-recovery-procedures-part3-snapshot-emergency.md) - Complete rebuild
