# Skill Reindexing Reference

## Table of Contents

- 2.1 What is skill reindexing - Updating PSS index
- 2.2 When to reindex - Reindexing triggers
  - 2.2.1 New skills added - Fresh skills need indexing
  - 2.2.2 Skills modified - Content changes need re-extraction
  - 2.2.3 Keywords stale - Suggestions not matching
- 2.3 Reindexing procedure - Step-by-step reindexing
  - 2.3.1 Trigger reindex - Running the command
  - 2.3.2 Index generation - Two-pass extraction
  - 2.3.3 Verification - Confirming index updated
  - 2.3.4 Testing - Checking skill discovery
- 2.4 Two-pass generation - How indexing works
  - 2.4.1 Pass 1 - Factual data extraction
  - 2.4.2 Pass 2 - AI co-usage relationships
- 2.5 Index structure - What gets indexed
- 2.6 Examples - Reindexing scenarios
- 2.7 Troubleshooting - Reindexing issues

---

## 2.1 What is skill reindexing

Skill reindexing is the process of regenerating the Perfect Skill Suggester (PSS) index from skill files. The index contains:

- Skill metadata (name, description)
- Extracted keywords
- Categories
- Co-usage relationships

Reindexing ensures PSS has current information for skill discovery.

---

## 2.2 When to reindex

### 2.2.1 New skills added

Reindex when:
- New skill directory created
- Skill moved from development to production
- Skill imported from another source

### 2.2.2 Skills modified

Reindex when:
- Skill description updated
- New procedures added
- Keywords changed
- References reorganized

### 2.2.3 Keywords stale

Reindex when:
- Skill not suggested for expected queries
- Wrong skills being suggested
- Index file older than skill files

---

## 2.3 Reindexing procedure

### 2.3.1 Trigger reindex

**Using PSS slash command:**
```
/pss-reindex-skills
```

**Using script:**
```bash
python scripts/pss_reindex_skills.py --skills-dir /path/to/skills
```

**Using Python API:**
```python
from pss import reindex_skills
reindex_skills(skills_dir="/path/to/skills")
```

### 2.3.2 Index generation

The reindex process:

1. Scan skills directory for SKILL.md files
2. Parse frontmatter from each skill
3. Extract description and content
4. Run Pass 1: Factual data extraction
5. Run Pass 2: AI co-usage relationships
6. Generate index file
7. Save to index location

### 2.3.3 Verification

**Check index was updated:**
```bash
# Check index file timestamp
ls -la ~/.claude/skills-index.json

# Check skill count
cat ~/.claude/skills-index.json | jq '.skills | length'

# Check specific skill
cat ~/.claude/skills-index.json | jq '.skills["ecos-staff-planning"]'
```

### 2.3.4 Testing

**Test skill discovery:**
```bash
# Use PSS status command
/pss-status

# Or query directly
python -c "from pss import suggest_skills; print(suggest_skills('staffing'))"
```

---

## 2.4 Two-pass generation

### 2.4.1 Pass 1 - Factual data extraction

Extracts objective data from skill files:

| Data | Source |
|------|--------|
| Name | Frontmatter: name |
| Description | Frontmatter: description |
| Categories | Mapped from description keywords |
| Primary keywords | Extracted from description |
| Secondary keywords | Extracted from content headings |

**Output per skill:**
```json
{
  "name": "ecos-staff-planning",
  "description": "Use when analyzing staffing needs...",
  "categories": ["orchestration", "planning"],
  "keywords": ["staffing", "capacity", "roles", "agents"]
}
```

### 2.4.2 Pass 2 - AI co-usage relationships

Analyzes skills for relationships:

| Relationship | Description |
|--------------|-------------|
| Prerequisites | Skills that should be read first |
| Related | Skills often used together |
| Alternatives | Skills that solve similar problems |

**Output per skill:**
```json
{
  "name": "ecos-staff-planning",
  "co_usage": {
    "prerequisites": ["ecos-session-memory-library"],
    "related": ["ecos-agent-lifecycle", "ecos-multi-project"],
    "alternatives": []
  }
}
```

---

## 2.5 Index structure

**Complete index format:**

```json
{
  "version": "1.0",
  "generated_at": "2025-02-01T10:00:00Z",
  "skill_count": 10,
  "skills": {
    "ecos-staff-planning": {
      "name": "ecos-staff-planning",
      "description": "Use when analyzing staffing needs...",
      "location": "/path/to/ecos-staff-planning/SKILL.md",
      "categories": ["orchestration", "planning"],
      "keywords": {
        "primary": ["staffing", "capacity", "roles"],
        "secondary": ["agents", "templates", "allocation"]
      },
      "co_usage": {
        "prerequisites": ["ecos-session-memory-library"],
        "related": ["ecos-agent-lifecycle"],
        "alternatives": []
      },
      "metadata": {
        "author": "Emasoft",
        "version": "1.0.0"
      }
    }
  },
  "categories": {
    "orchestration": ["ecos-staff-planning", "ecos-agent-lifecycle"],
    "planning": ["ecos-staff-planning", "ecos-multi-project"]
  }
}
```

---

## 2.6 Examples

### Example 1: Reindex After Adding Skills

```bash
# Add new skills
cp -r new-skills/* /path/to/skills/

# Trigger reindex
/pss-reindex-skills

# Verify new skills indexed
cat ~/.claude/skills-index.json | jq '.skill_count'
# Should show increased count

# Test discovery
/pss-suggest "new skill topic"
```

### Example 2: Force Full Reindex

```bash
# Remove old index
rm ~/.claude/skills-index.json

# Regenerate from scratch
python scripts/pss_reindex_skills.py \
  --skills-dir /path/to/skills \
  --force

# Verify
cat ~/.claude/skills-index.json | jq '.generated_at'
```

### Example 3: Reindex Specific Plugin Skills

```bash
# Reindex only Chief of Staff skills
python scripts/pss_reindex_skills.py \
  --skills-dir /path/to/emasoft-chief-of-staff/skills \
  --prefix "ecos-"

# Verify
cat ~/.claude/skills-index.json | jq '.skills | keys | map(select(startswith("ecos-")))'
```

---

## 2.7 Troubleshooting

### Issue: Reindex produces empty index

**Symptoms:** skill_count is 0, no skills indexed.

**Resolution:**
1. Check skills directory path is correct
2. Verify SKILL.md files exist
3. Check files have valid frontmatter
4. Look for parse errors in output

### Issue: Skills missing from index

**Symptoms:** Some skills not appearing in index.

**Resolution:**
1. Check skill has SKILL.md with frontmatter
2. Verify no parse errors for that skill
3. Check skill name is unique
4. Run with verbose output for details

### Issue: Keywords not matching expectations

**Symptoms:** Skill not suggested for expected queries.

**Resolution:**
1. Check description includes relevant keywords
2. Add keywords naturally to content
3. Reindex after changes
4. Test with PSS suggest command

### Issue: Index file permissions

**Symptoms:** Cannot write index file.

**Resolution:**
1. Check write permissions on index directory
2. Verify disk space available
3. Check for file locks
4. Try writing to alternate location

### Issue: Pass 2 fails

**Symptoms:** Co-usage relationships not generated.

**Resolution:**
1. Check AI API is accessible
2. Verify API credentials
3. Run Pass 2 separately for debugging
4. Fall back to Pass 1 only if needed
