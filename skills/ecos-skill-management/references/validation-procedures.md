# Skill Validation Procedures

## Contents

- 1.0 When validating a single skill directory
  - 1.1 Required skill structure components
  - 1.2 SKILL.md frontmatter validation rules
  - 1.3 Single skill validation step-by-step procedure
  - 1.4 Using skills-ref for validation
- 2.0 When validating all skills in a plugin
  - 2.1 Plugin-wide skill discovery
  - 2.2 Batch validation procedure
  - 2.3 Cross-reference verification
  - 2.4 Generating validation summary reports
- 3.0 When triggering PSS skill reindexing
  - 3.1 Pre-reindex validation checks
  - 3.2 Remote PSS reindex via AI Maestro
  - 3.3 Local PSS reindex via command
  - 3.4 Waiting for reindex completion
- 4.0 When validation errors occur
  - 4.1 Error severity categories
  - 4.2 Critical errors requiring immediate fix
  - 4.3 Major errors affecting skill quality
  - 4.4 Minor issues and style warnings
  - 4.5 Error handling strategies
- 5.0 When using validation scripts
  - 5.1 validate_skill_comprehensive.py for single validation
  - 5.2 validate_plugin.py for batch validation
  - 5.3 ecos_trigger_pss_reindex.py for reindexing
- 6.0 When using validation commands
  - 6.1 /ecos-validate-skills command options
  - 6.2 /ecos-reindex-skills command options
- 7.0 When handling validation tools errors
  - 7.1 skills-ref not installed
  - 7.2 PSS unavailable or not responding
  - 7.3 Network timeout during reindex
  - 7.4 Skill directory not found

---

## 1.0 When validating a single skill directory

### 1.1 Required skill structure components

Every skill must follow this minimum structure:

```
skill-name/
  SKILL.md          # REQUIRED: Main skill document with frontmatter
```

Optional but recommended structure:

```
skill-name/
  SKILL.md
  references/       # Supporting documentation
  scripts/          # Utility scripts
  assets/           # Images, diagrams, etc.
```

**Why this matters**: SKILL.md is the entry point for agents. Without it, the skill is not discoverable or usable.

### 1.2 SKILL.md frontmatter validation rules

**Required YAML frontmatter fields:**

```yaml
---
name: skill-name           # kebab-case, lowercase, no spaces
description: What this skill teaches
---
```

**Optional frontmatter fields:**

```yaml
---
name: skill-name
description: What this skill teaches
keywords:                  # For PSS indexing
  - keyword1
  - keyword2
categories:               # Competence categories
  - category1
dependencies:             # Required skills
  - other-skill
---
```

**Validation rules:**
- `name` field is REQUIRED and must be kebab-case
- `description` field is REQUIRED and must be non-empty
- `keywords` (if present) must be a YAML list
- `categories` (if present) must be a YAML list
- `dependencies` (if present) must be a YAML list of valid skill names
- Frontmatter must be valid YAML (proper indentation, colons, quotes)

### 1.3 Single skill validation step-by-step procedure

Follow this sequence when validating a skill:

**Step 1: Verify skill directory exists**
```bash
# Check if directory exists and is accessible
ls -la /path/to/skill
```

**Step 2: Check for SKILL.md at root**
```bash
# Must be at root of skill directory, not in subdirectory
test -f /path/to/skill/SKILL.md && echo "Found" || echo "Missing"
```

**Step 3: Parse and validate YAML frontmatter**
```bash
# Extract frontmatter and check YAML validity
head -n 20 /path/to/skill/SKILL.md | grep -A 10 "^---$"
```

**Step 4: Run skills-ref validate**
```bash
skills-ref validate /path/to/skill
```

**Step 5: Check for referenced files**
```bash
# Verify that files mentioned in SKILL.md actually exist
# Example: if SKILL.md links to ./references/foo.md, verify it exists
test -d /path/to/skill/references && ls /path/to/skill/references/
test -d /path/to/skill/scripts && ls /path/to/skill/scripts/
```

**Step 6: Report results**

Generate a validation report containing:
- Skill name and location
- Validation status (PASSED/FAILED/WARNING)
- List of errors (if any)
- List of warnings (if any)
- Remediation steps for failures

### 1.4 Using skills-ref for validation

The `skills-ref` package is the reference validator for AgentSkills OpenSpec.

**Installation:**
```bash
# Using pip
python -m venv .venv
source .venv/bin/activate
pip install skills-ref

# Using uv
uv sync
source .venv/bin/activate
```

**Basic validation:**
```bash
# Validate a single skill
skills-ref validate /path/to/skill

# Expected output on success:
# Validation passed for /path/to/skill

# Expected output on failure:
# Validation failed for /path/to/skill:
# - Missing required field: description
# - Invalid frontmatter format
```

**Read skill properties:**
```bash
# Outputs JSON with skill metadata
skills-ref read-properties /path/to/skill
```

**Generate prompt XML:**
```bash
# Generate <available_skills> XML for agent prompts
skills-ref to-prompt /path/to/skill-a /path/to/skill-b
```

---

## 2.0 When validating all skills in a plugin

### 2.1 Plugin-wide skill discovery

Skills are typically organized in a plugin's `skills/` directory. Each skill has its own subdirectory.

**Discovery command:**
```bash
# Find all SKILL.md files (each represents a skill)
find /path/to/plugin/skills -name "SKILL.md" -exec dirname {} \;
```

**Expected directory structure:**
```
plugin-root/
  skills/
    skill-one/
      SKILL.md
    skill-two/
      SKILL.md
    skill-three/
      SKILL.md
```

### 2.2 Batch validation procedure

**Step 1: Locate all skills**
```bash
skill_dirs=$(find /path/to/plugin/skills -name "SKILL.md" -exec dirname {} \;)
```

**Step 2: Validate each skill individually**
```bash
for skill_dir in $skill_dirs; do
    echo "Validating: $skill_dir"
    skills-ref validate "$skill_dir"
done
```

**Step 3: Collect validation results**

Track for each skill:
- Name
- Validation status (PASSED/FAILED/WARNING)
- Error count
- Warning count
- Specific issues

**Step 4: Check for naming conflicts**

Ensure no two skills have the same `name` in their frontmatter:

```bash
# Extract all skill names
for skill_dir in $skill_dirs; do
    grep "^name:" "$skill_dir/SKILL.md" | head -1
done | sort | uniq -d
# If output is non-empty, there are duplicate names
```

### 2.3 Cross-reference verification

Skills often reference other skills in `dependencies` frontmatter field or in content links.

**Verify dependency existence:**
1. Extract `dependencies` list from each skill's frontmatter
2. For each dependency, verify a skill with that name exists
3. Report missing dependencies

**Verify content links:**
1. Parse SKILL.md for links to other skills (e.g., `[other-skill](../other-skill/SKILL.md)`)
2. Verify linked paths exist
3. Report broken links

### 2.4 Generating validation summary reports

A good summary report includes:

**Header:**
- Plugin name
- Total skills found
- Validation timestamp

**Summary statistics:**
- Total skills validated
- Passed count
- Failed count
- Warning count

**Table of results:**

| Skill Name | Status | Issues |
|------------|--------|--------|
| skill-one | PASSED | - |
| skill-two | WARNING | Missing TOC |
| skill-three | FAILED | Invalid frontmatter |

**Error details:**

For each failed skill:
- Skill name and path
- List of errors with severity
- Remediation steps

**Example report format:**
```
Validation Summary for emasoft-architect-agent
Validated: 39 skills
Passed: 37
Warnings: 2
Failed: 0

Skills with Warnings:
1. eaa-system-modeling
   - [MINOR] Missing TOC in SKILL.md
   Remediation: Add table of contents at top of SKILL.md

2. eaa-component-design
   - [INFO] SKILL.md exceeds 500 lines, consider splitting
   Remediation: Move detailed procedures to references/
```

---

## 3.0 When triggering PSS skill reindexing

Perfect Skill Suggester (PSS) maintains an index of all available skills. When skills are added, modified, or deleted, PSS must be notified to rebuild its index.

### 3.1 Pre-reindex validation checks

Before triggering a reindex, always validate skills first:

**Step 1: Validate modified skills**
```bash
# Validate only skills that changed
for skill_dir in $modified_skills; do
    skills-ref validate "$skill_dir"
done
```

**Step 2: Check validation results**

Only trigger reindex if validation passes:
- If all skills PASSED: Proceed to reindex
- If any skill FAILED: Fix errors first, then validate again
- If only warnings: Proceed but note warnings in reindex message

**Step 3: Verify PSS availability**

Check that PSS is running and reachable:

```bash
# Check for /pss-reindex-skills command (local PSS)
claude --help | grep pss-reindex-skills
```

Alternatively, use the `ai-maestro-agents-management` skill to check if a PSS agent is registered and running remotely.

### 3.2 Remote PSS reindex via AI Maestro

When PSS runs in a separate Claude Code session (recommended for development):

**Step 1: Send reindex request**

Use the `agent-messaging` skill to send:
- **Recipient**: `perfect-skill-suggester`
- **Subject**: `Reindex Skills Request`
- **Priority**: `normal`
- **Content**: type `command`, message: "/pss-reindex-skills"

**Step 2: Wait for acknowledgment**

PSS will respond via AI Maestro message when reindex completes.

Use the `agent-messaging` skill to check for unread messages. Look for a response from `perfect-skill-suggester` containing reindex results.

**Step 3: Parse reindex results**

PSS response includes:
- Total skills indexed
- New skills count
- Updated skills count
- Deleted skills count
- Index generation time
- Any errors encountered

### 3.3 Local PSS reindex via command

When PSS is loaded in the same Claude Code session:

```bash
# Direct command execution
/pss-reindex-skills
```

**Why this matters**: Local reindex is faster but blocks the current session during indexing. Remote reindex allows the current session to continue working while PSS rebuilds its index.

### 3.4 Waiting for reindex completion

Reindexing can take several seconds for large skill sets.

**Options:**
1. **Blocking wait**: Wait for reindex to complete before proceeding
2. **Non-blocking**: Continue work, check status later
3. **Polling**: Check reindex status periodically

**Blocking wait example:**
```bash
# Send reindex request with --wait flag
/ecos-reindex-skills --wait

# Script waits for PSS confirmation before returning
```

**Non-blocking example:**
```bash
# Send reindex request, continue immediately
/ecos-reindex-skills

# Check status later
/pss-index-status
```

---

## 4.0 When validation errors occur

### 4.1 Error severity categories

Validation errors are categorized by severity:

| Category | Severity | Description | Action Required |
|----------|----------|-------------|-----------------|
| MISSING_SKILL_MD | Critical | SKILL.md file not found | Create SKILL.md with required frontmatter |
| INVALID_FRONTMATTER | Critical | YAML frontmatter parse error | Fix YAML syntax errors |
| MISSING_NAME | Critical | name field missing in frontmatter | Add name field |
| MISSING_DESCRIPTION | Major | description field missing | Add description field |
| INVALID_REFERENCE | Major | Referenced file does not exist | Create file or fix link |
| MISSING_TOC | Minor | SKILL.md lacks table of contents | Add TOC section |
| STYLE_ISSUE | Info | Formatting or style suggestion | Optional improvement |

### 4.2 Critical errors requiring immediate fix

**MISSING_SKILL_MD:**

The skill directory has no SKILL.md file. This makes the skill unusable.

**Remediation:**
```bash
# Create minimal SKILL.md
cat > /path/to/skill/SKILL.md <<'EOF'
---
name: skill-name
description: Brief description of what this skill teaches
---

# Skill Name

## Purpose

[Describe the skill's purpose and when to use it]

## Procedures

[List step-by-step procedures]
EOF
```

**INVALID_FRONTMATTER:**

The YAML frontmatter cannot be parsed. Common causes:
- Missing closing `---`
- Incorrect indentation
- Missing colons after keys
- Unclosed quotes

**Remediation:**
1. Identify the line number from error message
2. Check YAML syntax at that line
3. Common fixes:
   - Ensure proper indentation (2 spaces per level)
   - Add colon after key: `description:` not `description`
   - Close quotes: `"value"` not `"value`
   - End frontmatter with `---`

**Example fix:**
```yaml
# WRONG (missing colon)
---
name skill-name
description Brief description
---

# CORRECT
---
name: skill-name
description: Brief description
---
```

**MISSING_NAME:**

The frontmatter lacks a `name` field.

**Remediation:**
```yaml
# Add name field to frontmatter
---
name: skill-name    # Use directory name or descriptive kebab-case name
description: Existing description
---
```

### 4.3 Major errors affecting skill quality

**MISSING_DESCRIPTION:**

The frontmatter lacks a `description` field.

**Remediation:**
```yaml
# Add description field
---
name: existing-name
description: Clear, concise description of skill's purpose and use case
---
```

**INVALID_REFERENCE:**

A file referenced in SKILL.md does not exist.

**Example error:**
```
[MAJOR] INVALID_REFERENCE at line 45
- Referenced: ./references/test-patterns.md
- Status: File not found
```

**Remediation options:**

Option 1: Create the missing file
```bash
mkdir -p /path/to/skill/references
touch /path/to/skill/references/test-patterns.md
# Then add content to the file
```

Option 2: Fix the reference link
```markdown
# If the file exists elsewhere
# Change: [Test Patterns](./references/test-patterns.md)
# To: [Test Patterns](./references/patterns/test.md)
```

Option 3: Remove the reference
```markdown
# If the reference is no longer needed, remove the link
```

### 4.4 Minor issues and style warnings

**MISSING_TOC:**

SKILL.md does not have a table of contents at the top.

**Why this matters**: TOC enables progressive disclosure. Agents can scan the TOC to decide which sections to read without loading the entire file.

**Remediation:**
```markdown
---
name: skill-name
description: Description here
---

# Skill Name

## Contents

- 1.0 When starting a new task
  - 1.1 Task initialization procedure
  - 1.2 Context gathering steps
- 2.0 When executing the main workflow
  - 2.1 Step-by-step execution
  - 2.2 Error handling during execution
- 3.0 When completing the task
  - 3.1 Verification procedures
  - 3.2 Reporting results

---

[Rest of SKILL.md content]
```

**STYLE_ISSUE:**

Non-critical formatting or style suggestions.

Examples:
- Line too long
- Inconsistent heading levels
- Missing code block language specifier
- No blank line before heading

**Remediation**: Optional, but improves readability.

### 4.5 Error handling strategies

| Error | Action |
|-------|--------|
| skills-ref not installed | Report installation instructions, exit validation |
| Skill directory not found | Report path error, suggest corrections (check typos, relative vs absolute path) |
| Frontmatter parse error | Show line number, parsing error, example of correct syntax |
| PSS unavailable | Queue reindex request for later, continue with validation |
| Network timeout (AI Maestro) | Retry 3 times with exponential backoff (1s, 2s, 4s) |

**Exponential backoff example:**
```python
import time

def send_reindex_request_with_retry(max_retries=3):
    for attempt in range(max_retries):
        try:
            # Send request
            response = send_ai_maestro_message(...)
            return response
        except NetworkTimeout:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"Timeout, retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print("Max retries reached, giving up")
                raise
```

---

## 5.0 When using validation scripts

The ecos-skill-management skill includes Python scripts for validation automation.

### 5.1 validate_skill_comprehensive.py for single validation

Validates a single skill directory.

**Usage:**
```bash
# Basic validation
uv run --with pyyaml python scripts/validate_skill_comprehensive.py /path/to/skill

# With verbose output
uv run --with pyyaml python scripts/validate_skill_comprehensive.py /path/to/skill --verbose

# With auto-fix for minor issues
uv run --with pyyaml python scripts/validate_skill_comprehensive.py /path/to/skill --fix
```

**What it does:**
1. Checks SKILL.md exists
2. Parses and validates frontmatter
3. Runs skills-ref validate
4. Checks referenced files exist
5. Reports results in structured format

**Exit codes:**
- `0`: Validation passed
- `1`: Critical errors found
- `2`: Major errors found
- `3`: Minor issues only

### 5.2 validate_plugin.py for batch validation

Validates all skills in a plugin or directory. This is the universal plugin validator that discovers and validates all skills within a plugin directory.

**Usage:**
```bash
# Validate all skills in current directory
uv run --with pyyaml python scripts/validate_plugin.py .

# Validate all skills in a plugin
uv run --with pyyaml python scripts/validate_plugin.py /path/to/plugin/skills

# With verbose output
uv run --with pyyaml python scripts/validate_plugin.py /path/to/plugin/skills --verbose

# Generate JSON report
uv run --with pyyaml python scripts/validate_plugin.py /path/to/plugin/skills --json
```

**What it does:**
1. Discovers all skills in directory
2. Validates each skill individually
3. Checks for naming conflicts
4. Verifies cross-references
5. Generates summary report

**Output format (text):**
```
Scanning /path/to/plugin/skills/ for skills...
Found 39 skills. Validating each...

| Skill | Status | Issues |
|-------|--------|--------|
| skill-one | PASSED | - |
| skill-two | WARNING | Missing TOC |
| skill-three | PASSED | - |

Summary:
- Total: 39 skills
- Passed: 37
- Warnings: 2
- Failed: 0
```

**Output format (JSON):**
```json
{
  "total_skills": 39,
  "passed": 37,
  "warnings": 2,
  "failed": 0,
  "results": [
    {
      "name": "skill-one",
      "path": "/path/to/skill-one",
      "status": "PASSED",
      "errors": [],
      "warnings": []
    },
    {
      "name": "skill-two",
      "path": "/path/to/skill-two",
      "status": "WARNING",
      "errors": [],
      "warnings": ["MISSING_TOC"]
    }
  ]
}
```

### 5.3 ecos_trigger_pss_reindex.py for reindexing

Sends a reindex request to PSS via AI Maestro.

**Usage:**
```bash
# Basic reindex
uv run python scripts/ecos_trigger_pss_reindex.py

# Force full reindex
uv run python scripts/ecos_trigger_pss_reindex.py --force

# Wait for completion
uv run python scripts/ecos_trigger_pss_reindex.py --wait

# Specify AI Maestro endpoint
uv run python scripts/ecos_trigger_pss_reindex.py  # Uses default AI Maestro endpoint
```

**What it does:**
1. Checks AI Maestro is available
2. Sends reindex command to PSS
3. Optionally waits for completion
4. Reports results

**Exit codes:**
- `0`: Reindex request sent successfully
- `1`: AI Maestro unavailable
- `2`: PSS not found
- `3`: Network error

---

## 6.0 When using validation commands

The ecos-skill-validator agent provides two commands for skill validation.

### 6.1 /ecos-validate-skills command options

Validates skills in a directory or plugin.

**Basic usage:**
```
/ecos-validate-skills [path]
```

**Arguments:**
- `path`: Path to skill directory or plugin (default: current directory)

**Flags:**
- `--all`: Validate all skills in directory recursively
- `--fix`: Attempt to auto-fix minor issues
- `--verbose`: Show detailed validation output

**Examples:**
```
# Validate single skill in current directory
/ecos-validate-skills

# Validate specific skill
/ecos-validate-skills ./skills/code-review

# Validate all skills in plugin
/ecos-validate-skills ./OUTPUT_SKILLS/emasoft-architect-agent --all

# Validate with auto-fix
/ecos-validate-skills ./skills/debugging --fix

# Verbose output
/ecos-validate-skills ./skills/testing --verbose
```

**What auto-fix handles:**
- Adding missing TOC section
- Fixing minor YAML indentation issues
- Creating empty referenced directories
- Standardizing heading levels

**What auto-fix does NOT handle:**
- Missing required frontmatter fields (manual fix required)
- Invalid YAML syntax (manual fix required)
- Broken content references (manual decision required)

### 6.2 /ecos-reindex-skills command options

Triggers PSS skill reindexing.

**Basic usage:**
```
/ecos-reindex-skills
```

**Flags:**
- `--force`: Force full reindex even if no changes detected
- `--wait`: Wait for reindex completion before returning

**Examples:**
```
# Basic reindex (only if changes detected)
/ecos-reindex-skills

# Force full reindex
/ecos-reindex-skills --force

# Wait for completion
/ecos-reindex-skills --wait

# Force and wait
/ecos-reindex-skills --force --wait
```

**When to use `--force`:**
- PSS index is corrupted
- Skills were modified outside of validation workflow
- Testing PSS indexing behavior
- After bulk skill updates

**When to use `--wait`:**
- Next step depends on updated index
- Testing validation-reindex workflow
- Need confirmation before proceeding

**When to use neither:**
- Skills updated frequently, only latest state matters
- Working on other tasks while PSS reindexes
- Batch validation where reindex is final step

---

## 7.0 When handling validation tools errors

### 7.1 skills-ref not installed

**Error message:**
```
Command 'skills-ref' not found
```

**Cause**: The skills-ref package is not installed or not on PATH.

**Remediation:**

Step 1: Check if Python virtual environment is activated:
```bash
which python
# Should show: /path/to/.venv/bin/python
# If not, activate venv:
source .venv/bin/activate
```

Step 2: Install skills-ref:
```bash
# Using pip
pip install skills-ref

# Using uv
uv sync  # If pyproject.toml includes skills-ref
# OR
uv pip install skills-ref
```

Step 3: Verify installation:
```bash
skills-ref --version
```

### 7.2 PSS unavailable or not responding

**Error message:**
```
Failed to reach PSS for reindexing
AI Maestro connection refused
```

**Cause**: Perfect Skill Suggester is not running or AI Maestro is down.

**Remediation:**

Step 1: Use the `ai-maestro-agents-management` skill to check AI Maestro health status. It should report healthy.

Step 2: Use the `ai-maestro-agents-management` skill to check if a PSS agent (containing "perfect-skill-suggester" in its name) is registered.

Step 3: If PSS is not running:
- Start a Claude Code session with PSS plugin loaded
- Verify PSS loaded: `/pss-index-status`

Step 4: If AI Maestro is not running:
```bash
# Check if AI Maestro server is running
ps aux | grep ai-maestro
# If not, start it (consult AI Maestro docs)
```

Step 5: Queue reindex for later:
```bash
# Validation can proceed, reindex later when PSS is available
/ecos-validate-skills --all
# Then manually trigger reindex when PSS is back:
/ecos-reindex-skills
```

### 7.3 Network timeout during reindex

**Error message:**
```
Timeout waiting for PSS reindex response
Request timed out after 30 seconds
```

**Cause**: PSS is taking too long to respond (large skill set, slow system).

**Remediation:**

Step 1: Retry with exponential backoff:
```bash
# Script automatically retries 3 times
uv run python scripts/ecos_trigger_pss_reindex.py
```

Step 2: Check PSS logs for indexing progress:
```bash
# If PSS writes logs, check them
tail -f ~/.claude/logs/pss-indexing.log
```

Step 3: Increase timeout:
```bash
# If you control the reindex script, increase timeout
# Example: from 30s to 60s
uv run python scripts/ecos_trigger_pss_reindex.py --timeout 60
```

Step 4: If timeouts persist:
- PSS may be processing a very large skill set
- Check system resources (CPU, memory)
- Consider reindexing in smaller batches

### 7.4 Skill directory not found

**Error message:**
```
Error: Skill directory not found: /path/to/skill
```

**Cause**: The specified path does not exist or is not accessible.

**Remediation:**

Step 1: Verify the path:
```bash
ls -la /path/to/skill
```

Step 2: Check for typos:
- Skill name spelling
- Relative vs absolute path
- Hidden characters in path

Step 3: Check current working directory:
```bash
pwd
# If using relative path, ensure you're in the correct directory
```

Step 4: Use absolute paths:
```bash
# Instead of: ./skills/code-review
# Use: /Users/username/project/skills/code-review
```

Step 5: Check permissions:
```bash
# Ensure directory is readable
ls -ld /path/to/skill
# Should show: drwxr-xr-x or similar (r permission required)
```

Step 6: Verify skill structure:
```bash
# Even if directory exists, check for SKILL.md
ls /path/to/skill/SKILL.md
```
