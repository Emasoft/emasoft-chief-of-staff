---
operation: reindex-skills-pss
procedure: proc-create-team
workflow-instruction: Step 4 - Team Creation
parent-skill: ecos-skill-management
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Reindex Skills for PSS


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Validate Skills First](#step-1-validate-skills-first)
  - [Step 2: Trigger Reindex](#step-2-trigger-reindex)
  - [Step 3: Verify Index Updated](#step-3-verify-index-updated)
  - [Step 4: Test Discovery](#step-4-test-discovery)
  - [Step 5: Check Keywords Extracted](#step-5-check-keywords-extracted)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Full Reindex After Plugin Update](#example-full-reindex-after-plugin-update)
  - [Example: Checking Why Skill Not Discovered](#example-checking-why-skill-not-discovered)
  - [Example: Two-Pass Index Generation](#example-two-pass-index-generation)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

- After adding new skills to a plugin
- After modifying skill content or keywords
- When PSS suggestions are stale or incorrect
- After plugin installation or update
- When skills are not being discovered

## Prerequisites

- Perfect Skill Suggester (PSS) plugin is installed
- Skills are valid (run validation first)
- PSS reindex command or script is available

## Procedure

### Step 1: Validate Skills First

Before reindexing, ensure skills are valid:

```bash
# Validate all skills in a directory
for skill in /path/to/skills/*/; do
  skills-ref validate "$skill"
done
```

### Step 2: Trigger Reindex

**Method 1: PSS Slash Command**
```bash
# In Claude Code session
/pss-reindex-skills
```

**Method 2: Direct Script**
```bash
uv run python scripts/pss_reindex_skills.py --skills-dir /path/to/skills
```

**Method 3: Full Path Specification**
```bash
uv run python scripts/pss_reindex_skills.py \
  --skills-dir /path/to/skills \
  --output ~/.claude/skills-index.json
```

### Step 3: Verify Index Updated

```bash
# Check index file timestamp
ls -la ~/.claude/skills-index.json

# Check skill count
cat ~/.claude/skills-index.json | jq '.skills | length'

# Check specific skill is indexed
cat ~/.claude/skills-index.json | jq '.skills[] | select(.name == "my-skill")'
```

### Step 4: Test Discovery

Try queries that should activate your skill:

```bash
# In Claude Code, type a prompt that should trigger skill
# For example, if skill is about "agent spawning":
# "I need to spawn a new agent"

# PSS should suggest the relevant skill
```

### Step 5: Check Keywords Extracted

```bash
# View extracted keywords for a skill
cat ~/.claude/skills-index.json | jq '.skills[] | select(.name == "my-skill") | .keywords'
```

## Checklist

Copy this checklist and track your progress:

- [ ] Validate all skills before reindexing
- [ ] Note current index timestamp
- [ ] Execute reindex command
- [ ] Verify index file updated
- [ ] Check skill count matches expected
- [ ] Verify specific skills are in index
- [ ] Test discovery with relevant queries
- [ ] Verify keywords extracted correctly

## Examples

### Example: Full Reindex After Plugin Update

```bash
# Step 1: Validate all skills
echo "=== Validating Skills ==="
SKILL_DIR="/path/to/my-plugin/skills"
for skill in $SKILL_DIR/*/; do
  echo "Validating: $skill"
  skills-ref validate "$skill"
done

# Step 2: Note current index state
echo "=== Current Index ==="
ls -la ~/.claude/skills-index.json
OLD_COUNT=$(cat ~/.claude/skills-index.json | jq '.skills | length')
echo "Current skill count: $OLD_COUNT"

# Step 3: Reindex
echo "=== Reindexing ==="
/pss-reindex-skills
# or: uv run python scripts/pss_reindex_skills.py --skills-dir $SKILL_DIR

# Step 4: Verify update
echo "=== Verification ==="
ls -la ~/.claude/skills-index.json
NEW_COUNT=$(cat ~/.claude/skills-index.json | jq '.skills | length')
echo "New skill count: $NEW_COUNT"

# Step 5: Check specific skill
echo "=== Checking ecos-agent-lifecycle ==="
cat ~/.claude/skills-index.json | jq '.skills[] | select(.name == "ecos-agent-lifecycle")'
```

### Example: Checking Why Skill Not Discovered

```bash
SKILL_NAME="my-missing-skill"

# Is it in the index?
FOUND=$(cat ~/.claude/skills-index.json | jq -r ".skills[] | select(.name == \"$SKILL_NAME\") | .name")

if [ -z "$FOUND" ]; then
  echo "Skill not in index. Check:"
  echo "1. Skill exists and is valid"
  echo "2. Skill directory is in scan path"
  echo "3. Reindex was run after adding skill"
else
  echo "Skill IS in index. Check keywords:"
  cat ~/.claude/skills-index.json | jq ".skills[] | select(.name == \"$SKILL_NAME\") | .keywords"
  echo ""
  echo "If keywords don't match your query, update skill description"
fi
```

### Example: Two-Pass Index Generation

PSS uses two passes for comprehensive indexing:

**Pass 1: Factual Data Extraction**
- Skill name, description, path
- Direct keywords from frontmatter
- Categories from explicit metadata

**Pass 2: AI Co-usage Relationships**
- Skills often used together
- Related skill suggestions
- Weighted scoring refinement

```bash
# The reindex script handles both passes automatically
# You can verify co-usage relationships:
cat ~/.claude/skills-index.json | jq '.skills[] | select(.name == "ecos-agent-lifecycle") | .co_usage_skills'
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Reindex command not found | PSS not installed | Install PSS plugin |
| Skills not appearing | Not in scan path | Check --skills-dir points to correct location |
| Index not updating | Permission issue | Check write permission on ~/.claude/ |
| Keywords wrong | Description not optimized | Update skill description with better keywords |
| Co-usage empty | Single skill indexed | Index multiple skills for relationships |
| Index file corrupt | Interrupted write | Delete and regenerate index |

## Related Operations

- [op-validate-skill.md](op-validate-skill.md) - Validate before reindex
- [op-configure-pss-integration.md](op-configure-pss-integration.md) - Optimize for discovery
- [op-generate-agent-prompt-xml.md](op-generate-agent-prompt-xml.md) - Generate skills XML
