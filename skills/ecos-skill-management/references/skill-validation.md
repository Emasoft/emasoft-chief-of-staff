# Skill Validation Reference

## Table of Contents

- 1.1 What is skill validation - Checking skill correctness
- 1.2 Validation requirements - Agent Skills specification
  - 1.2.1 Directory structure - Required layout
  - 1.2.2 SKILL.md format - Frontmatter and content
  - 1.2.3 References structure - Reference file format
- 1.3 Validation procedure - Step-by-step validation
  - 1.3.1 Using skills-ref - CLI validation tool
  - 1.3.2 Frontmatter check - YAML syntax and fields
  - 1.3.3 References check - File existence and links
  - 1.3.4 TOC verification - Heading accuracy
- 1.4 Required frontmatter fields - Mandatory YAML fields
  - 1.4.1 name - Skill identifier
  - 1.4.2 description - Use case description
  - 1.4.3 license - License identifier
  - 1.4.4 compatibility - Requirements
- 1.5 Optional Claude Code fields - Extended metadata
  - 1.5.1 context - Fork behavior (value: fork)
  - 1.5.2 agent - Target agent types
  - 1.5.3 user-invocable - Direct user activation
- 1.6 Examples - Validation scenarios
- 1.7 Troubleshooting - Validation issues

---

## 1.1 What is skill validation

Skill validation is the process of verifying that a skill directory conforms to the Agent Skills specification. Validation ensures:

- Correct directory structure
- Valid SKILL.md frontmatter
- All references exist
- Links are not broken

---

## 1.2 Validation requirements

### 1.2.1 Directory structure

```
my-skill/
├── SKILL.md              # REQUIRED: Main skill file
├── references/           # OPTIONAL: Reference documents
│   ├── procedure-1.md
│   ├── procedure-2.md
│   └── troubleshooting.md
└── scripts/              # OPTIONAL: Automation scripts
    └── helper.py
```

### 1.2.2 SKILL.md format

```markdown
---
name: my-skill
description: Use when [specific use case]
license: Apache-2.0
compatibility: Requires [requirements]
metadata:
  author: Author Name
  version: 1.0.0
---

# Skill Title

Content following progressive disclosure...
```

### 1.2.3 References structure

Each reference file should have:
- Table of Contents at top
- Clear section headings
- Use-case oriented titles

---

## 1.3 Validation procedure

### 1.3.1 Using skills-ref

**Installation:**
```bash
pip install skills-ref
```

**Validation:**
```bash
# Validate single skill
skills-ref validate /path/to/my-skill

# Output
Skill: my-skill
Status: VALID
Warnings: 0
Errors: 0
```

### 1.3.2 Frontmatter check

Verify YAML frontmatter:

```bash
# Extract and validate frontmatter
head -50 SKILL.md | grep -A 100 '^---$' | head -n -1 | tail -n +2 > /tmp/fm.yaml
python -c "import yaml; yaml.safe_load(open('/tmp/fm.yaml'))"
```

**Check required fields:**
- name: Must be present, kebab-case
- description: Must be present, describes use case
- license: Must be valid SPDX identifier
- compatibility: Must describe requirements

### 1.3.3 References check

Verify all referenced files exist:

```bash
# Find all reference links in SKILL.md
grep -oE '\[.*\]\(references/[^)]+\)' SKILL.md | while read link; do
  path=$(echo "$link" | sed 's/.*(\(.*\))/\1/')
  if [ ! -f "$path" ]; then
    echo "Missing: $path"
  fi
done
```

### 1.3.4 TOC verification

Verify TOC entries match headings:

```bash
# Extract TOC from reference file
grep -E '^- [0-9]+\.' references/procedure-1.md

# Compare with actual headings
grep -E '^#+ ' references/procedure-1.md
```

---

## 1.4 Required frontmatter fields

### 1.4.1 name

**Purpose:** Unique identifier for the skill.

**Format:** Kebab-case, lowercase, no spaces.

**Example:**
```yaml
name: ecos-staff-planning
```

### 1.4.2 description

**Purpose:** Describe WHEN to use this skill.

**Format:** Start with "Use when..." for clarity.

**Example:**
```yaml
description: Use when analyzing staffing needs, assessing role requirements, or creating staffing templates
```

### 1.4.3 license

**Purpose:** Specify the license for the skill.

**Format:** SPDX license identifier.

**Example:**
```yaml
license: Apache-2.0
```

### 1.4.4 compatibility

**Purpose:** Describe requirements for using the skill.

**Format:** Free text describing dependencies.

**Example:**
```yaml
compatibility: Requires access to agent registry and understanding of agent capabilities.
```

---

## 1.5 Optional Claude Code fields

These fields are Claude Code specific and may generate warnings from generic validators.

### 1.5.1 context

**Purpose:** Control agent context behavior.

**Valid values:** `fork`

**Example:**
```yaml
context: fork
```

### 1.5.2 agent

**Purpose:** Specify target agent types.

**Valid values:** Agent type identifiers.

**Example:**
```yaml
agent: code-reviewer
```

### 1.5.3 user-invocable

**Purpose:** Allow direct user activation.

**Valid values:** `true` or `false`

**Example:**
```yaml
user-invocable: true
```

---

## 1.6 Examples

### Example 1: Valid Skill

```yaml
---
name: ecos-staff-planning
description: Use when analyzing staffing needs, assessing role requirements, planning agent capacity, or creating staffing templates for multi-agent orchestration
license: Apache-2.0
compatibility: Requires access to agent registry, project configuration files, and understanding of agent capabilities and workload patterns.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
---
```

**Validation result:**
```
Skill: ecos-staff-planning
Status: VALID
Warnings: 0
Errors: 0
```

### Example 2: Invalid Skill (Missing Fields)

```yaml
---
name: my-skill
---
```

**Validation result:**
```
Skill: my-skill
Status: INVALID
Errors:
  - Missing required field: description
  - Missing required field: license
  - Missing required field: compatibility
```

### Example 3: Generating Prompt XML

```bash
# Generate available_skills XML for agent prompts
skills-ref to-prompt /path/to/skill-a /path/to/skill-b

# Output
<available_skills>
<skill>
<name>skill-a</name>
<description>What skill-a does</description>
<location>/path/to/skill-a/SKILL.md</location>
</skill>
<skill>
<name>skill-b</name>
<description>What skill-b does</description>
<location>/path/to/skill-b/SKILL.md</location>
</skill>
</available_skills>
```

---

## 1.7 Troubleshooting

### Issue: YAML parse error

**Symptoms:** Validation fails with YAML error.

**Resolution:**
1. Check for proper YAML indentation
2. Ensure colons are followed by space
3. Quote strings with special characters
4. Use YAML linter to find issues

### Issue: Missing description

**Symptoms:** Validation reports missing description.

**Resolution:**
1. Add description field to frontmatter
2. Start with "Use when..." pattern
3. Describe specific use cases

### Issue: Invalid license

**Symptoms:** License not recognized.

**Resolution:**
1. Use valid SPDX identifier
2. Common licenses: Apache-2.0, MIT, GPL-3.0
3. Check SPDX license list

### Issue: References not found

**Symptoms:** Validation reports broken links.

**Resolution:**
1. Check file paths are correct
2. Verify files exist in references/
3. Check for typos in filenames
4. Use relative paths from SKILL.md

### Issue: Claude Code fields cause warnings

**Symptoms:** Warnings about unknown fields (context, agent).

**Resolution:**
1. These are valid for Claude Code
2. Generic validators do not know them
3. Warnings can be ignored
4. Add to validator exceptions if available
