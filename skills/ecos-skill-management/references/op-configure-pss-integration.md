---
operation: configure-pss-integration
procedure: proc-create-team
workflow-instruction: Step 4 - Team Creation
parent-skill: ecos-skill-management
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Configure PSS Integration

## When to Use

- Optimizing skill discovery for specific queries
- Adjusting keyword weights for better matching
- Improving skill activation accuracy
- When skills activate for wrong queries
- When relevant skills are not suggested

## Prerequisites

- Perfect Skill Suggester (PSS) is installed
- Skill is valid and indexed
- Understanding of PSS keyword matching

## Procedure

### Step 1: Understand PSS Algorithm

PSS uses weighted scoring based on:
- **Description keywords** - Primary matching source
- **Categories** (16 predefined) - Fields of competence
- **Co-usage relationships** - Skills often used together
- **Agent availability** - Filter against agent's skill list

**Index is Superset Principle:** Index contains ALL skills; each agent filters against its available skills list.

### Step 2: Optimize Skill Description

The `description` field in SKILL.md frontmatter is the PRIMARY source for keyword extraction.

**Best practices:**
- Use action verbs: "Use when spawning", "Trigger with agent creation"
- Include tool names: "AI Maestro", "agent-messaging skill"
- Include concepts: "lifecycle management", "team coordination"
- Use natural language that matches user queries

**Before:**
```yaml
description: Agent lifecycle operations
```

**After:**
```yaml
description: Use when spawning, terminating, hibernating, or waking agents. Trigger with agent spawn, termination, or hibernation requests.
```

### Step 3: Add Activation Keywords Naturally

Keywords should appear naturally in:
- Frontmatter description
- SKILL.md overview section
- Procedure names
- Reference file TOCs

**Example keyword embedding:**
```markdown
## Overview

Agent lifecycle management is a critical responsibility...
This skill teaches you how to properly **spawn agents**,
manage their **running state**, **hibernate idle agents** to
conserve resources, and **terminate agents** when complete.
```

### Step 4: Configure Categories (If Using)

PSS recognizes 16 categories (fields of competence):

| Category | Keywords |
|----------|----------|
| orchestration | coordination, delegation, workflow |
| lifecycle | spawn, terminate, hibernate, state |
| communication | messaging, notification, broadcast |
| validation | check, verify, validate, audit |
| configuration | setup, install, configure |
| ... | ... |

Add relevant category in frontmatter:
```yaml
metadata:
  categories:
    - lifecycle
    - orchestration
```

### Step 5: Add Co-usage Hints

Reference related skills in your SKILL.md:

```markdown
## Related Skills

If you also need to:
- Manage plugins -> See ecos-plugin-management skill
- Onboard agents -> See ecos-onboarding skill
```

This helps PSS build co-usage relationships.

### Step 6: Reindex and Test

```bash
# Reindex to apply changes
/pss-reindex-skills

# Test with various queries
# Query 1: "spawn new agent"
# Query 2: "create team member"
# Query 3: "terminate idle agent"

# Verify your skill is suggested for relevant queries
```

### Step 7: Iterate Based on Results

If skill not suggested for expected query:
1. Check index has skill: `jq '.skills[] | select(.name == "my-skill")' ~/.claude/skills-index.json`
2. Check extracted keywords: `jq '.skills[] | select(.name == "my-skill") | .keywords'`
3. Add missing keywords to description
4. Reindex and retest

## Checklist

Copy this checklist and track your progress:

- [ ] Understand PSS matching algorithm
- [ ] Review current skill description
- [ ] Add action verbs to description
- [ ] Include tool/command names
- [ ] Include key concepts naturally
- [ ] Configure categories in metadata
- [ ] Add related skill references
- [ ] Reindex skills
- [ ] Test with multiple query variations
- [ ] Iterate if needed

## Examples

### Example: Optimizing Agent Lifecycle Skill

**Before (poor discovery):**
```yaml
---
name: ecos-agent-lifecycle
description: Manages agent states
---
```

**After (good discovery):**
```yaml
---
name: ecos-agent-lifecycle
description: Use when spawning, terminating, hibernating, or waking agents. Trigger with agent spawn, termination, hibernation, or wake requests. Covers agent creation via the ai-maestro-agents-management skill, team registry updates, and AI Maestro messaging for lifecycle events.
license: Apache-2.0
compatibility: Requires AI Maestro, ai-maestro-agents-management skill, tmux
metadata:
  categories:
    - lifecycle
    - orchestration
---
```

### Example: Testing Discovery

```bash
# Test queries and expected skills
echo "Query: spawn new agent"
echo "Expected: ecos-agent-lifecycle"

echo "Query: install plugin"
echo "Expected: ecos-plugin-management"

echo "Query: validate skill structure"
echo "Expected: ecos-skill-management"

# In Claude Code, try each query and verify PSS suggests correct skill
```

### Example: Debugging Poor Discovery

```bash
SKILL_NAME="ecos-agent-lifecycle"

# Step 1: Is it indexed?
jq ".skills[] | select(.name == \"$SKILL_NAME\")" ~/.claude/skills-index.json

# Step 2: What keywords extracted?
jq ".skills[] | select(.name == \"$SKILL_NAME\") | .keywords" ~/.claude/skills-index.json

# Step 3: What description is stored?
jq ".skills[] | select(.name == \"$SKILL_NAME\") | .description" ~/.claude/skills-index.json

# If keywords missing, update description and reindex
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Skill never suggested | Keywords don't match user queries | Update description with query-matching terms |
| Wrong skill suggested | Description too generic | Be more specific, add unique keywords |
| Multiple skills suggested | Overlapping keywords | Differentiate descriptions, use specific terms |
| Keywords not extracted | Description too short | Expand description with more natural language |
| Categories ignored | Not in recognized list | Use only the 16 predefined categories |

## Related Operations

- [op-validate-skill.md](op-validate-skill.md) - Validate skill structure
- [op-reindex-skills-pss.md](op-reindex-skills-pss.md) - Reindex after changes
- [op-generate-agent-prompt-xml.md](op-generate-agent-prompt-xml.md) - Generate skills XML
