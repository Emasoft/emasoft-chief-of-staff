# Initialize Session Memory

## Table of Contents
1. [When you need to understand the purpose](#purpose)
2. [When to initialize session memory](#when-to-initialize)
3. [How to perform initialization](#initialization-procedure)
4. [Understanding directory structure](#directory-structure)
5. [What files to create initially](#initial-files)
6. [How to verify initialization](#verification-steps)
7. [For implementation examples](#examples)
8. [If issues occur](#troubleshooting)

## Purpose

Session memory initialization creates the foundational structure for persistent memory management across session compactions and restarts. It establishes directories, creates initial tracking files, and validates the environment is ready for memory operations.

## When to Initialize

Initialize session memory when:
- Starting a new orchestrator session for the first time
- Session memory directory is missing or corrupted
- Recovering from a failed session
- Explicitly requested by user
- After detecting memory structure validation failures

## Initialization Procedure

### Step 1: Check Existing Structure

Before creating new directories, verify what already exists to avoid overwriting valid data.

```bash
# Check if memory directory exists
if [ -d ".session_memory" ]; then
    echo "Memory directory exists - validate first"
fi

# Check for essential files
ls -la .session_memory/ 2>/dev/null
```

### Step 2: Create Directory Structure

Create the canonical directory layout for session memory:

```bash
# Create root memory directory
mkdir -p .session_memory

# Create subdirectories
mkdir -p .session_memory/active_context
mkdir -p .session_memory/patterns
mkdir -p .session_memory/progress
mkdir -p .session_memory/snapshots
mkdir -p .session_memory/archived
```

### Step 3: Create Initial Tracking Files

Initialize essential tracking files with proper structure:

**active_context.md** - Current working context
```markdown
# Active Context

**Last Updated:** [Session Start]
**Compaction Count:** 0

## Current Focus
[No active tasks yet]

## Recent Decisions
- Session initialized

## Open Questions
[None]
```

**progress_tracker.md** - Task and goal tracking
```markdown
# Progress Tracker

## Active Tasks
[None]

## Completed Tasks
[None]

## Blocked Tasks
[None]

## Dependencies
[None]
```

**pattern_index.md** - Pattern catalog
```markdown
# Pattern Index

## Recorded Patterns
[None]

## Pattern Categories
- Problem-Solution
- Workflow
- Decision-Logic
- Error-Recovery
- Configuration
```

### Step 4: Create Session Metadata

Record session initialization metadata:

```bash
# Create session_info.md
cat > .session_memory/session_info.md << 'EOF'
# Session Information

**Session Start:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Initialization Method:** Automatic/Manual
**Memory Version:** 1.0
**Compaction Count:** 0

## Environment
- Project: [Project Name]
- Working Directory: $(pwd)
- Git Branch: $(git branch --show-current 2>/dev/null || echo "N/A")

## Status
- Initialized: ✓
- Validated: Pending
EOF
```

### Step 5: Add to .gitignore

Ensure session memory is properly excluded from version control:

```bash
# Check if .gitignore exists
if [ ! -f ".gitignore" ]; then
    touch .gitignore
fi

# Add session memory to gitignore if not present
if ! grep -q ".session_memory" .gitignore; then
    echo "" >> .gitignore
    echo "# Session Memory (ephemeral, not version controlled)" >> .gitignore
    echo ".session_memory/" >> .gitignore
fi
```

### Step 6: Validate Initialization

Run validation checks to ensure structure is correct:

```bash
# Verify all directories exist
required_dirs=(
    ".session_memory"
    ".session_memory/active_context"
    ".session_memory/patterns"
    ".session_memory/progress"
    ".session_memory/snapshots"
    ".session_memory/archived"
)

for dir in "${required_dirs[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "ERROR: Missing directory: $dir"
        exit 1
    fi
done

# Verify essential files exist
required_files=(
    ".session_memory/active_context.md"
    ".session_memory/progress_tracker.md"
    ".session_memory/pattern_index.md"
    ".session_memory/session_info.md"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "ERROR: Missing file: $file"
        exit 1
    fi
done

echo "✓ Session memory initialized successfully"
```

## Directory Structure

After initialization, the structure should be:

```
.session_memory/
├── session_info.md           # Session metadata
├── active_context.md         # Current working context
├── progress_tracker.md       # Task progress tracking
├── pattern_index.md          # Pattern catalog
├── active_context/           # Context snapshots
├── patterns/                 # Recorded patterns
├── progress/                 # Progress snapshots
├── snapshots/               # Full session snapshots
└── archived/                # Old snapshots (post-compaction)
```

## Initial Files

### active_context.md Structure

```markdown
# Active Context

**Last Updated:** [Timestamp]
**Compaction Count:** 0

## Current Focus
- [Primary task or goal]
- [Secondary tasks]

## Recent Decisions
- [Key decisions made]
- [Rationale for decisions]

## Open Questions
- [Questions needing resolution]
- [Blockers awaiting input]

## Context Notes
[Any additional context important to preserve]
```

### progress_tracker.md Structure

```markdown
# Progress Tracker

## Active Tasks
- [ ] Task 1 - Description
  - Dependencies: None
  - Status: In Progress
  - Started: [Date]

## Completed Tasks
- [x] Task 0 - Session initialization
  - Completed: [Date]

## Blocked Tasks
[None]

## Dependencies
[None - will be populated as tasks are added]
```

### pattern_index.md Structure

```markdown
# Pattern Index

## Recorded Patterns
[List of pattern files with brief descriptions]

## Pattern Categories
- **Problem-Solution**: Issues encountered and solutions found
- **Workflow**: Effective workflows for common tasks
- **Decision-Logic**: Decision trees and logic patterns
- **Error-Recovery**: Error handling and recovery procedures
- **Configuration**: Configuration patterns and best practices

## Pattern Statistics
- Total Patterns: 0
- Last Updated: [Session Start]
```

## Verification Steps

After initialization, verify:

1. **Directory Permissions**: All directories are readable/writable
2. **File Integrity**: All files are valid markdown
3. **Gitignore**: .session_memory/ is properly excluded
4. **Structure Completeness**: All required files and directories exist
5. **Initial Content**: Files contain valid initial structure

## Examples

### Example 1: Clean Initialization

```bash
#!/bin/bash
# Initialize session memory from scratch

echo "Initializing session memory..."

# Remove any existing structure (if corrupted)
rm -rf .session_memory

# Create structure
mkdir -p .session_memory/{active_context,patterns,progress,snapshots,archived}

# Create initial files
cat > .session_memory/active_context.md << 'EOF'
# Active Context

**Last Updated:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Compaction Count:** 0

## Current Focus
Project initialization

## Recent Decisions
- Session memory initialized

## Open Questions
None
EOF

# Validate
if [ -d ".session_memory" ] && [ -f ".session_memory/active_context.md" ]; then
    echo "✓ Initialization successful"
else
    echo "✗ Initialization failed"
    exit 1
fi
```

### Example 2: Initialization with Existing Data Recovery

```bash
#!/bin/bash
# Initialize while preserving existing data

if [ -d ".session_memory" ]; then
    # Backup existing data
    backup_dir=".session_memory_backup_$(date +%Y%m%d_%H%M%S)"
    mv .session_memory "$backup_dir"
    echo "Existing data backed up to: $backup_dir"
fi

# Create fresh structure
mkdir -p .session_memory/{active_context,patterns,progress,snapshots,archived}

# Restore preserved data if backup exists
if [ -d "$backup_dir" ]; then
    # Copy back valuable files
    cp "$backup_dir"/patterns/*.md .session_memory/patterns/ 2>/dev/null || true
    cp "$backup_dir"/active_context.md .session_memory/ 2>/dev/null || true
    echo "✓ Data restored from backup"
fi
```

### Example 3: Validation-First Initialization

```bash
#!/bin/bash
# Validate before initializing

validate_and_init() {
    # Check if already initialized
    if [ -f ".session_memory/session_info.md" ]; then
        echo "Session memory already initialized"

        # Validate existing structure
        if ./scripts/validate_memory.sh; then
            echo "✓ Existing structure is valid"
            return 0
        else
            echo "⚠ Existing structure is invalid - reinitializing"
        fi
    fi

    # Proceed with initialization
    mkdir -p .session_memory/{active_context,patterns,progress,snapshots,archived}

    # Create files...
    # [initialization code here]

    echo "✓ Initialization complete"
}

validate_and_init
```

## Troubleshooting

### Problem: "Permission Denied" When Creating Directories

**Cause**: Insufficient permissions in working directory

**Solution**:
```bash
# Check current permissions
ls -ld .

# If needed, adjust permissions
chmod u+w .

# Retry initialization
```

### Problem: "Directory Already Exists" Error

**Cause**: Previous session memory exists

**Solution**:
```bash
# Option 1: Validate existing structure
./scripts/validate_memory.sh

# Option 2: Backup and reinitialize
mv .session_memory .session_memory_backup
# Run initialization

# Option 3: Clean slate (CAUTION: loses data)
rm -rf .session_memory
# Run initialization
```

### Problem: Files Created but Empty

**Cause**: Heredoc syntax error or variable expansion issue

**Solution**:
```bash
# Use single quotes to prevent premature expansion
cat > file.md << 'EOF'
Content here
EOF

# Verify file contents
cat file.md
```

### Problem: .gitignore Not Updated

**Cause**: File permissions or syntax error

**Solution**:
```bash
# Check if .gitignore exists and is writable
ls -l .gitignore

# Add entry manually
echo ".session_memory/" >> .gitignore

# Verify
cat .gitignore | grep session_memory
```

### Problem: Initialization Appears Successful but Validation Fails

**Cause**: Missing files or incorrect structure

**Solution**:
```bash
# List all created files
find .session_memory -type f

# Compare against required files list
required=(
    "session_info.md"
    "active_context.md"
    "progress_tracker.md"
    "pattern_index.md"
)

# Check each file
for file in "${required[@]}"; do
    if [ ! -f ".session_memory/$file" ]; then
        echo "Missing: $file"
    fi
done
```

### Problem: Git Shows .session_memory/ in Status

**Cause**: .gitignore not properly configured or committed

**Solution**:
```bash
# Remove from git if tracked
git rm -r --cached .session_memory/

# Ensure .gitignore is correct
echo ".session_memory/" >> .gitignore

# Commit .gitignore
git add .gitignore
git commit -m "Add session memory to gitignore"
```
