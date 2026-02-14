---
operation: validate-skill
procedure: proc-create-team
workflow-instruction: Step 4 - Team Creation
parent-skill: ecos-skill-management
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Validate Skill Structure


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Install skills-ref (If Needed)](#step-1-install-skills-ref-if-needed)
  - [Step 2: Run skills-ref Validate](#step-2-run-skills-ref-validate)
  - [Step 3: Check YAML Frontmatter](#step-3-check-yaml-frontmatter)
  - [Step 4: Verify Directory Structure](#step-4-verify-directory-structure)
  - [Step 5: Check Reference Links](#step-5-check-reference-links)
  - [Step 6: Validate TOC Accuracy](#step-6-validate-toc-accuracy)
  - [Step 7: Read Skill Properties](#step-7-read-skill-properties)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Complete Skill Validation](#example-complete-skill-validation)
  - [Example: Fixing Common Validation Errors](#example-fixing-common-validation-errors)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

- Before publishing a skill
- After modifying skill files
- When skill fails to load
- When skill not appearing in PSS suggestions
- During plugin validation

## Prerequisites

- `skills-ref` validator installed (`pip install skills-ref`)
- Skill directory exists
- Python 3.8+ available

## Procedure

### Step 1: Install skills-ref (If Needed)

```bash
pip install skills-ref

# Or with uv
uv pip install skills-ref
```

### Step 2: Run skills-ref Validate

```bash
skills-ref validate /path/to/my-skill
```

**Expected output for valid skill:**
```
Skill: my-skill
Status: VALID
Warnings: 0
Errors: 0
```

### Step 3: Check YAML Frontmatter

Verify SKILL.md has required frontmatter fields:

```bash
# Extract frontmatter
head -20 /path/to/my-skill/SKILL.md
```

**Required fields:**
- `name` - Skill identifier (kebab-case)
- `description` - Use case description (triggers)
- `license` - License identifier (e.g., Apache-2.0)
- `compatibility` - Requirements and dependencies

**Optional Claude Code fields:**
- `context: fork` - Fork behavior
- `agent` - Target agent types
- `workflow-instruction` - Workflow step reference
- `procedure` - Procedure reference

### Step 4: Verify Directory Structure

```bash
ls -la /path/to/my-skill/
```

**Required structure:**
```
my-skill/
├── SKILL.md           # REQUIRED: Main skill file
└── references/        # Reference documentation
    └── *.md          # Detailed procedures
```

**Optional:**
```
my-skill/
├── scripts/          # Automation helpers
└── templates/        # Template files
```

### Step 5: Check Reference Links

```bash
# Extract links from SKILL.md
grep -E '\[.*\]\(references/.*\.md\)' /path/to/my-skill/SKILL.md

# Verify each referenced file exists
for link in $(grep -oE 'references/[^)]+\.md' /path/to/my-skill/SKILL.md | sort -u); do
  if [ -f "/path/to/my-skill/$link" ]; then
    echo "OK: $link"
  else
    echo "MISSING: $link"
  fi
done
```

### Step 6: Validate TOC Accuracy

Each reference file should have a TOC that matches its headings:

```bash
# For each reference file, compare TOC to actual headings
for ref in /path/to/my-skill/references/*.md; do
  echo "=== Checking $ref ==="
  # Extract headings
  grep -E '^#{1,3} ' "$ref" | head -20
done
```

### Step 7: Read Skill Properties

```bash
skills-ref read-properties /path/to/my-skill
```

This outputs JSON with extracted skill metadata.

## Checklist

Copy this checklist and track your progress:

- [ ] Install skills-ref validator
- [ ] Run skills-ref validate
- [ ] Check SKILL.md has required frontmatter
- [ ] Verify name is kebab-case
- [ ] Verify description includes trigger phrases
- [ ] Check references/ directory exists
- [ ] Verify all referenced files exist
- [ ] Check TOC matches actual headings
- [ ] Run read-properties to verify extraction

## Examples

### Example: Complete Skill Validation

```bash
SKILL_PATH="/path/to/ecos-agent-lifecycle"

# Step 1: Run validator
skills-ref validate $SKILL_PATH
# Output: Skill: ecos-agent-lifecycle | Status: VALID

# Step 2: Check frontmatter
head -15 $SKILL_PATH/SKILL.md
# Should show:
# ---
# name: ecos-agent-lifecycle
# description: Use when spawning, terminating...
# license: Apache-2.0
# ...
# ---

# Step 3: Check structure
ls $SKILL_PATH/
# Output: SKILL.md  references/

ls $SKILL_PATH/references/
# Output: spawn-procedures.md  termination-procedures.md  ...

# Step 4: Check links
grep -oE 'references/[^)]+\.md' $SKILL_PATH/SKILL.md | while read link; do
  test -f "$SKILL_PATH/$link" && echo "OK: $link" || echo "MISSING: $link"
done

# Step 5: Read properties
skills-ref read-properties $SKILL_PATH | jq '.'
```

### Example: Fixing Common Validation Errors

**Error: Missing name field**
```yaml
# Before (invalid)
---
description: My skill description
---

# After (valid)
---
name: my-skill-name
description: My skill description
license: Apache-2.0
compatibility: Requires X
---
```

**Error: Broken reference link**
```bash
# SKILL.md references: references/missing-file.md
# Fix: Create the missing file
touch /path/to/my-skill/references/missing-file.md
```

**Error: Name not kebab-case**
```yaml
# Before (invalid)
name: MySkillName

# After (valid)
name: my-skill-name
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| SKILL.md not found | Wrong directory | Ensure SKILL.md is at skill root |
| Missing required field | Incomplete frontmatter | Add missing field (name, description, license, compatibility) |
| Invalid YAML | Syntax error in frontmatter | Check YAML syntax, fix quotes/indentation |
| Reference file missing | Broken link | Create missing file or fix link |
| Name not kebab-case | Wrong naming convention | Convert to lowercase-with-hyphens |
| skills-ref not found | Not installed | Run `pip install skills-ref` |

## Related Operations

- [op-reindex-skills-pss.md](op-reindex-skills-pss.md) - Reindex after validation
- [op-configure-pss-integration.md](op-configure-pss-integration.md) - Optimize for PSS
- [op-generate-agent-prompt-xml.md](op-generate-agent-prompt-xml.md) - Generate XML
