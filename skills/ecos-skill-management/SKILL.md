---
name: ecos-skill-management
description: Use when validating skill directory structure, reindexing skills for Perfect Skill Suggester, or managing skill activation and discovery. Trigger with skill validation, indexing, or update requests.
user-invocable: false
license: Apache-2.0
compatibility: Requires access to skill directories, skills-ref validator, and Perfect Skill Suggester (PSS) if using reindexing features. Requires AI Maestro installed.
metadata:
  author: Emasoft
  version: 1.0.0
context: fork
agent: ecos-main
workflow-instruction: "Step 4"
procedure: "proc-create-team"
---

# Emasoft Chief of Staff - Skill Management Skill

## Overview

Skill management enables the Chief of Staff to validate, index, and maintain agent skills across plugins and projects. This skill teaches you how to validate skill directory structure, trigger skill reindexing for Perfect Skill Suggester, and manage skill activation and discovery.

## Prerequisites

Before using this skill, ensure:
1. Skill validation scripts are available
2. PSS (Perfect Skill Suggester) is configured if reindexing
3. Skill directories are accessible

## Instructions

1. Identify skill operation needed (validate, reindex, update)
2. Execute the operation
3. Verify skill integrity
4. Notify agents of skill changes

## Output

| Operation | Output |
|-----------|--------|
| Validate | Validation report with issues |
| Reindex | PSS index updated |
| Update | Skill content modified, agents notified |

## What Is Skill Management?

Skill management is the administration of agent skills that provide specialized knowledge and procedures. It includes:

- **Validation**: Ensuring skills conform to the Agent Skills specification
- **Reindexing**: Updating the skill index for PSS discovery
- **PSS Integration**: Configuring skills for AI-analyzed keyword matching

## Skill Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    SKILL DIRECTORY                       │
│  ┌─────────────────────────────────────────────────┐    │
│  │  SKILL.md                                        │    │
│  │  - YAML frontmatter (name, description, etc.)   │    │
│  │  - Procedures with TOC                          │    │
│  │  - References links                             │    │
│  └─────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────┐    │
│  │  references/                                     │    │
│  │  - Detailed procedure documentation             │    │
│  │  - Each file has own TOC                        │    │
│  └─────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────┐    │
│  │  scripts/   (optional)                          │    │
│  │  - Automation helpers                           │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              PERFECT SKILL SUGGESTER                     │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Skill Index                                     │    │
│  │  - Keywords extracted from skills               │    │
│  │  - Co-usage relationships                       │    │
│  │  - Weighted scoring for activation              │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

## Core Procedures

### PROCEDURE 1: Validate Skill Structure

**When to use:** Before publishing a skill, after modifying skill files, or when skill fails to load.

**Steps:** Run skills-ref validate, check YAML frontmatter, verify references exist, confirm TOC accuracy.

**Related documentation:**

#### Skill Validation ([references/skill-validation.md](references/skill-validation.md))
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

### PROCEDURE 2: Reindex Skills for PSS

**When to use:** After adding new skills, after modifying skill content, or when PSS suggestions are stale.

**Steps:** Run pss-reindex-skills command, verify index updated, test skill discovery.

**Related documentation:**

#### Skill Reindexing ([references/skill-reindexing.md](references/skill-reindexing.md))
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

### PROCEDURE 3: Configure PSS Integration

**When to use:** When optimizing skill discovery, adjusting keyword weights, or customizing activation behavior.

**Steps:** Review skill descriptions, add activation keywords, configure weights, test discovery.

**Related documentation:**

#### PSS Integration ([references/pss-integration.md](references/pss-integration.md))
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

## Task Checklist

Copy this checklist and track your progress:

- [ ] Understand skill architecture and PSS integration
- [ ] Learn PROCEDURE 1: Validate skill structure
- [ ] Learn PROCEDURE 2: Reindex skills for PSS
- [ ] Learn PROCEDURE 3: Configure PSS integration
- [ ] Practice validating a skill with skills-ref
- [ ] Practice triggering a skill reindex
- [ ] Practice optimizing a skill for PSS discovery
- [ ] Verify skill appears in PSS suggestions

## Examples

### Example 1: Validating a Skill

```bash
# Install skills-ref if not present
pip install skills-ref

# Validate a skill directory
skills-ref validate /path/to/my-skill

# Expected output for valid skill
# Skill: my-skill
# Status: VALID
# Warnings: 0
# Errors: 0

# Read skill properties
skills-ref read-properties /path/to/my-skill
```

### Example 2: SKILL.md Frontmatter

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

### Example 3: Triggering PSS Reindex

```bash
# Using PSS slash command
/pss-reindex-skills

# Or via script
python scripts/pss_reindex_skills.py --skills-dir /path/to/skills

# Verify index updated
cat ~/.claude/skills-index.json | jq '.skills | length'
```

### Example 4: Generating Agent Prompt XML

```bash
# Generate available_skills XML for agent prompts
skills-ref to-prompt /path/to/skill-a /path/to/skill-b

# Output
# <available_skills>
# <skill>
# <name>skill-a</name>
# <description>What skill-a does</description>
# <location>/path/to/skill-a/SKILL.md</location>
# </skill>
# ...
# </available_skills>
```

## Error Handling

### Issue: Skill validation fails

**Symptoms:** skills-ref reports errors, missing fields, broken links.

See [references/skill-validation.md](references/skill-validation.md) Section 1.7 Troubleshooting for resolution.

### Issue: Skill not appearing in PSS suggestions

**Symptoms:** Skill indexed but not suggested, wrong skills activated.

See [references/skill-reindexing.md](references/skill-reindexing.md) Section 2.7 Troubleshooting for resolution.

### Issue: PSS keyword matching is poor

**Symptoms:** Irrelevant skills suggested, relevant skills missed.

See [references/pss-integration.md](references/pss-integration.md) Section 3.7 Troubleshooting for resolution.

## Key Takeaways

1. **Validate before publish** - Catch errors early with skills-ref
2. **Reindex after changes** - PSS needs fresh index to discover updates
3. **Description is key** - PSS extracts keywords from description
4. **Use natural language** - Keywords should appear naturally in content
5. **Test discovery** - Verify skills activate for expected queries

## Next Steps

### 1. Read Skill Validation
See [references/skill-validation.md](references/skill-validation.md) for validation procedures.

### 2. Read Skill Reindexing
See [references/skill-reindexing.md](references/skill-reindexing.md) for reindexing procedures.

### 3. Read PSS Integration
See [references/pss-integration.md](references/pss-integration.md) for discovery optimization.

---

## Resources

- [Skill Validation](references/skill-validation.md)
- [Validation Procedures](references/validation-procedures.md) - Skill validation procedures
- [Skill Reindexing](references/skill-reindexing.md)
- [PSS Integration](references/pss-integration.md)

---

**Version:** 1.0
**Last Updated:** 2025-02-01
**Target Audience:** Chief of Staff Agents
**Difficulty Level:** Intermediate
