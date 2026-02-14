---
operation: generate-agent-prompt-xml
procedure: proc-create-team
workflow-instruction: Step 4 - Team Creation
parent-skill: ecos-skill-management
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Generate Agent Prompt XML


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Identify Skills to Include](#step-1-identify-skills-to-include)
  - [Step 2: Generate XML with skills-ref](#step-2-generate-xml-with-skills-ref)
  - [Step 3: Save to File (Optional)](#step-3-save-to-file-optional)
  - [Step 4: Integrate into Agent Prompt](#step-4-integrate-into-agent-prompt)
  - [Step 5: Verify Integration](#step-5-verify-integration)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Generate XML for ECOS Skills](#example-generate-xml-for-ecos-skills)
  - [Example: Save and Use in Agent Definition](#example-save-and-use-in-agent-definition)
  - [Example: Programmatic Generation](#example-programmatic-generation)
  - [Example: Dynamic Skill List](#example-dynamic-skill-list)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

- Creating agent system prompts that need skill awareness
- Building agent definition files
- Documenting available skills for agents
- Creating skill discovery documentation

## Prerequisites

- `skills-ref` is installed (`pip install skills-ref`)
- Skills are valid and accessible
- Write access to output location

## Procedure

### Step 1: Identify Skills to Include

Determine which skills should be included in the agent prompt:

```bash
# List available skills
ls /path/to/skills/

# Or list skills in a plugin
ls /path/to/plugin/skills/
```

### Step 2: Generate XML with skills-ref

```bash
skills-ref to-prompt /path/to/skill-a /path/to/skill-b /path/to/skill-c
```

**Output format:**
```xml
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

### Step 3: Save to File (Optional)

```bash
skills-ref to-prompt /path/to/skill-a /path/to/skill-b > available_skills.xml
```

### Step 4: Integrate into Agent Prompt

Add the generated XML to your agent definition or system prompt:

```markdown
# Agent System Prompt

You are a specialized agent with access to the following skills:

<available_skills>
...
</available_skills>

When you need to perform a task covered by a skill, read the skill's SKILL.md file at the provided location.
```

### Step 5: Verify Integration

Test that the agent can access the skill files at the specified locations.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify skills to include in prompt
- [ ] Verify all skills are valid
- [ ] Run skills-ref to-prompt command
- [ ] Review generated XML for accuracy
- [ ] Save to file if needed
- [ ] Integrate into agent definition
- [ ] Verify agent can access skill locations
- [ ] Test agent uses skills appropriately

## Examples

### Example: Generate XML for ECOS Skills

```bash
# Generate for all ECOS skills
skills-ref to-prompt \
  /path/to/skills/ecos-agent-lifecycle \
  /path/to/skills/ecos-plugin-management \
  /path/to/skills/ecos-skill-management \
  /path/to/skills/ecos-onboarding

# Output:
# <available_skills>
# <skill>
# <name>ecos-agent-lifecycle</name>
# <description>Use when spawning, terminating, hibernating, or waking agents...</description>
# <location>/path/to/skills/ecos-agent-lifecycle/SKILL.md</location>
# </skill>
# ...
# </available_skills>
```

### Example: Save and Use in Agent Definition

```bash
# Generate and save
PLUGIN_SKILLS="/path/to/emasoft-chief-of-staff/skills"
skills-ref to-prompt $PLUGIN_SKILLS/*/ > /tmp/ecos_skills.xml

# View result
cat /tmp/ecos_skills.xml

# Use in agent definition file
cat > /path/to/agents/ecos-main-agent.md << 'EOF'
---
name: ecos-main-agent
description: Chief of Staff main agent
---

# ECOS Main Agent

You have access to the following skills:

$(cat /tmp/ecos_skills.xml)

When a task matches a skill's description, read the SKILL.md file to learn the procedures.
EOF
```

### Example: Programmatic Generation

```python
from pathlib import Path
from skills_ref import to_prompt

# Generate prompt for skills
skills = [
    Path("/path/to/skill-a"),
    Path("/path/to/skill-b"),
    Path("/path/to/skill-c")
]

xml_output = to_prompt(skills)
print(xml_output)

# Save to file
with open("available_skills.xml", "w") as f:
    f.write(xml_output)
```

### Example: Dynamic Skill List

```bash
# Generate for all skills in a plugin dynamically
PLUGIN_PATH="/path/to/my-plugin"
SKILL_DIRS=$(find $PLUGIN_PATH/skills -mindepth 1 -maxdepth 1 -type d)

# Build command
CMD="skills-ref to-prompt"
for dir in $SKILL_DIRS; do
  CMD="$CMD $dir"
done

# Execute
$CMD > $PLUGIN_PATH/docs/available_skills.xml

echo "Generated XML for $(echo $SKILL_DIRS | wc -w) skills"
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| skills-ref not found | Not installed | Run `pip install skills-ref` |
| Invalid skill path | Directory doesn't exist | Verify path is correct |
| SKILL.md not found | Missing main file | Create SKILL.md in skill directory |
| Empty output | No valid skills | Check skills pass validation first |
| Paths incorrect in XML | Using relative paths | Use absolute paths to skill directories |
| Agent can't read skill | Path not accessible | Ensure agent has filesystem access to paths |

## Related Operations

- [op-validate-skill.md](op-validate-skill.md) - Validate before generating
- [op-reindex-skills-pss.md](op-reindex-skills-pss.md) - PSS uses similar data
- [op-configure-pss-integration.md](op-configure-pss-integration.md) - Optimize descriptions
