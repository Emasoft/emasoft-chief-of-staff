# PSS Integration Reference

## Table of Contents

- 3.1 What is PSS integration - AI-analyzed skill activation
- 3.2 How PSS works - Discovery algorithm
  - 3.2.1 Index as superset - All skills indexed
  - 3.2.2 Agent filtering - Available skills filter
  - 3.2.3 Weighted scoring - Keyword relevance
- 3.3 Integration procedure - Optimizing for PSS
  - 3.3.1 Description optimization - Clear use cases
  - 3.3.2 Keyword embedding - Natural keyword inclusion
  - 3.3.3 Co-usage hints - Related skill references
- 3.4 Categories vs keywords - Understanding the difference
  - 3.4.1 Categories (16) - Fields of competence
  - 3.4.2 Keywords - Tools, actions, concepts
- 3.5 Testing discovery - Verifying activation
- 3.6 Examples - PSS integration scenarios
- 3.7 Troubleshooting - Discovery issues

---

## 3.1 What is PSS integration

PSS (Perfect Skill Suggester) integration is the configuration of skills to be discovered and activated by the AI-powered skill suggestion system. Integration involves:

- Writing descriptions for discovery
- Embedding relevant keywords
- Defining category mappings
- Setting co-usage relationships

---

## 3.2 How PSS works

### 3.2.1 Index as superset

The PSS index contains ALL skills from all sources:
- Plugin skills
- Global skills
- Project skills
- User skills

The index is the superset; agents filter to their available skills.

### 3.2.2 Agent filtering

When an agent queries PSS:
1. PSS searches full index for matches
2. Results filtered to agent's available skills
3. Only accessible skills returned

**Example:**
```
Index: [skill-a, skill-b, skill-c, skill-d]
Agent available: [skill-a, skill-c]
Query matches: [skill-a, skill-b, skill-c]
Returned: [skill-a, skill-c]  # Filtered
```

### 3.2.3 Weighted scoring

PSS scores skills by relevance:

| Factor | Weight | Description |
|--------|--------|-------------|
| Primary keyword match | 1.0 | Keyword in description |
| Secondary keyword match | 0.5 | Keyword in content |
| Category match | 0.3 | Category alignment |
| Co-usage boost | 0.2 | Used with already-active skill |

---

## 3.3 Integration procedure

### 3.3.1 Description optimization

**Purpose:** Write descriptions that trigger correct discovery.

**Best Practices:**
- Start with "Use when..."
- List specific use cases
- Include action verbs
- Mention key concepts

**Good Example:**
```yaml
description: Use when analyzing staffing needs, assessing role requirements, planning agent capacity, or creating staffing templates for multi-agent orchestration
```

**Bad Example:**
```yaml
description: Staff planning skill
```

### 3.3.2 Keyword embedding

**Purpose:** Include keywords naturally in content.

**Keyword Locations:**
1. Description (highest weight)
2. Section headings (medium weight)
3. Procedure names (medium weight)
4. Body text (lower weight)

**Example - Keywords in Headings:**
```markdown
## PROCEDURE 1: Assess Role Requirements
## PROCEDURE 2: Plan Agent Capacity
## PROCEDURE 3: Create Staffing Templates
```

Keywords "role", "capacity", "staffing", "templates" now indexed.

### 3.3.3 Co-usage hints

**Purpose:** Help PSS suggest related skills.

**In SKILL.md:**
```markdown
## Related Skills

- **ecos-agent-lifecycle** - For spawning assessed agents
- **ecos-multi-project** - For cross-project staffing
```

PSS extracts these relationships during indexing.

---

## 3.4 Categories vs keywords

### 3.4.1 Categories (16)

Categories are high-level fields of competence:

| Category | Description |
|----------|-------------|
| orchestration | Multi-agent coordination |
| planning | Task and resource planning |
| development | Code implementation |
| testing | Test creation and execution |
| documentation | Writing docs |
| deployment | CI/CD and releases |
| security | Security practices |
| debugging | Error investigation |
| configuration | Settings and config |
| monitoring | Status and metrics |
| communication | Agent messaging |
| memory | State persistence |
| validation | Checking correctness |
| integration | External service connection |
| performance | Optimization |
| lifecycle | Agent state management |

### 3.4.2 Keywords

Keywords are specific terms:

| Type | Examples |
|------|----------|
| Tools | pytest, ruff, git, gh |
| Actions | spawn, terminate, validate, sync |
| Concepts | capacity, dependency, registry |
| Entities | agent, project, skill, plugin |

**Categories** answer: "What domain is this skill in?"
**Keywords** answer: "What specific things does this skill help with?"

---

## 3.5 Testing discovery

### Test 1: Direct PSS Query

```bash
# Using PSS command
/pss-suggest "staffing and capacity planning"

# Expected: ecos-staff-planning in results
```

### Test 2: Check Index Entry

```bash
# Verify skill is indexed
cat ~/.claude/skills-index.json | jq '.skills["ecos-staff-planning"]'

# Check keywords
cat ~/.claude/skills-index.json | jq '.skills["ecos-staff-planning"].keywords'
```

### Test 3: Category Mapping

```bash
# Check skill appears in expected category
cat ~/.claude/skills-index.json | jq '.categories["planning"]'

# Should include: "ecos-staff-planning"
```

### Test 4: Negative Test

```bash
# Skill should NOT appear for unrelated queries
/pss-suggest "database migrations"

# ecos-staff-planning should NOT be in results
```

---

## 3.6 Examples

### Example 1: Optimizing Description

**Before:**
```yaml
description: Skill for staff planning
```

**After:**
```yaml
description: Use when analyzing staffing needs, assessing role requirements, planning agent capacity, or creating staffing templates for multi-agent orchestration
```

**Improvement:**
- Added "Use when" pattern
- Listed specific use cases
- Included key terms: "capacity", "templates", "orchestration"

### Example 2: Adding Keyword Headings

**Before:**
```markdown
## Step 1
## Step 2
## Step 3
```

**After:**
```markdown
## PROCEDURE 1: Assess Role Requirements
## PROCEDURE 2: Plan Agent Capacity
## PROCEDURE 3: Create Staffing Templates
```

**Improvement:**
- Headings now contain searchable keywords
- Procedures are clearly named
- Keywords indexed from headings

### Example 3: Category Alignment

**Skill:** ecos-staff-planning

**Expected Categories:**
- orchestration (multi-agent coordination)
- planning (resource planning)
- lifecycle (agent management related)

**Verification:**
```bash
cat ~/.claude/skills-index.json | jq '.skills["ecos-staff-planning"].categories'
# ["orchestration", "planning", "lifecycle"]
```

---

## 3.7 Troubleshooting

### Issue: Skill not suggested for expected query

**Symptoms:** Query should match but skill not returned.

**Resolution:**
1. Check description includes query keywords
2. Verify skill is in index
3. Check agent has skill available
4. Add keywords to description
5. Reindex after changes

### Issue: Skill suggested for wrong queries

**Symptoms:** Skill appears for unrelated searches.

**Resolution:**
1. Check for overly generic keywords
2. Make description more specific
3. Remove ambiguous terms
4. Reindex after changes

### Issue: Category mismatch

**Symptoms:** Skill in wrong category.

**Resolution:**
1. Update description to clarify domain
2. Check category mapping rules
3. May need manual category override
4. Reindex after changes

### Issue: Co-usage not working

**Symptoms:** Related skills not suggested together.

**Resolution:**
1. Add explicit links to related skills
2. Check Pass 2 ran successfully
3. Verify relationship in index
4. May need explicit co-usage config

### Issue: Low relevance score

**Symptoms:** Skill ranked low in results.

**Resolution:**
1. Add more keywords to description
2. Use primary keywords in headings
3. Increase specificity
4. Check competing skills
