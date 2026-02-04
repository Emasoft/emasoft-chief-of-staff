# Proactive Handoff Protocol

## Automatic Handoff Triggers

## Table of Contents

1. [Automatic Handoff Triggers](#automatic-handoff-triggers)
2. [Handoff Document Location](#handoff-document-location)
3. [Mandatory Handoff Sections](#mandatory-handoff-sections)
4. [Proactive Writing Rules](#proactive-writing-rules)
5. [Handoff Quality Checklist](#handoff-quality-checklist)
6. [Protocol for Handing Off GitHub Operations](#protocol-for-handing-off-github-operations)
   - 6.1 [When to Hand Off GitHub Operations](#when-to-hand-off-github-operations)
   - 6.2 [GitHub Handoff Template](#github-handoff-template)
   - 6.3 [GitHub Handoff Decision Flow](#github-handoff-decision-flow)
7. [Protocol for Handing Off Design Operations](#protocol-for-handing-off-design-operations)
   - 7.1 [When to Hand Off Design Operations](#when-to-hand-off-design-operations)
   - 7.2 [Design Handoff Template](#design-handoff-template)
   - 7.3 [Design Handoff Decision Flow](#design-handoff-decision-flow)
8. [UUID Tracking Across Handoffs](#uuid-tracking-across-handoffs)
   - 8.1 [UUID Chain Concept](#uuid-chain-concept)
   - 8.2 [UUID Format Standards](#uuid-format-standards)
   - 8.3 [UUID Registry Location](#uuid-registry-location)
   - 8.4 [UUID Propagation Rules](#uuid-propagation-rules)
   - 8.5 [UUID Lookup Before Handoff](#uuid-lookup-before-handoff)

---


This agent MUST automatically write a handoff document when:

1. **Task Completion**: Before reporting task done
2. **Session End**: When session is about to end (PreCompact, Stop)
3. **Role Transition**: When work moves to another role
4. **Context Limit**: When approaching context window limit
5. **Blocking Issue**: When blocked and escalating

## Handoff Document Location

Write handoffs to: `$CLAUDE_PROJECT_DIR/docs_dev/handoffs/`

**Filename format**: `handoff-{uuid}-{from_role}-to-{to_role}-{timestamp}.md`

## Mandatory Handoff Sections

```yaml
---
uuid: <generated-uuid>
from: <agent-name>
to: <target-agent-or-user>
timestamp: <ISO-8601>
priority: normal|high|urgent
requires_ack: true|false
---

## Context
What was being worked on? Why was it started?

## Progress
- [x] Completed steps
- [ ] Pending steps

## Current State
Where exactly did work stop? What files are affected?

## Blockers (if any)
What's preventing progress?

## Next Steps
Exactly what the next agent should do first.

## References
- File paths
- Issue/PR numbers
- Previous handoff links
```

## Proactive Writing Rules

1. **ALWAYS write handoff before reporting completion** via AI Maestro
2. **ALWAYS write handoff before session ends** (hook should block if missing)
3. **NEVER assume next agent knows context** - be explicit
4. **ALWAYS include file paths** with line numbers when relevant
5. **ALWAYS send AI Maestro message** after writing handoff with file path

## Handoff Quality Checklist

Before sending handoff:
- [ ] UUID is unique and recorded
- [ ] Context explains WHY work was started
- [ ] All affected files listed with paths
- [ ] Current state is specific (not "almost done")
- [ ] Next steps are actionable (first action is clear)
- [ ] AI Maestro notification prepared

## Protocol for Handing Off GitHub Operations

### When to Hand Off GitHub Operations

GitHub operations require handoff when:
1. **Issue creation/update** involving multiple agents' domains
2. **PR operations** requiring design validation or implementation verification
3. **Kanban sync** affecting tracked designs or modules
4. **Release preparation** requiring multi-agent coordination

### GitHub Handoff Template

```yaml
---
uuid: <generated-uuid>
from: <agent-name>
to: <target-agent>
timestamp: <ISO-8601>
priority: normal|high|urgent
operation_type: github
github_type: issue|pr|kanban|release
---

## GitHub Operation Context

**Repository**: <owner/repo>
**Target**: <issue number, PR number, or project ID>
**Action**: <create|update|close|merge|sync|etc.>

## Linked References

### Design Links (if applicable)
- Design UUID: <uuid>
- Design Path: <path>
- Relevant Section: <section heading or line range>

### Module Links (if applicable)
- Module UUID: <uuid>
- Parent Design: <design UUID>
- Implementation Status: <not started|in progress|complete>

## Operation Details

<Specific details of the GitHub operation>

## Expected Outcome

<What success looks like>

## UUID Tracking Note

Include in GitHub item body:
<!-- ECOS-LINK: handoff-uuid=<this-handoff-uuid> -->
<!-- ECOS-LINK: design-uuid=<design-uuid-if-applicable> -->
<!-- ECOS-LINK: module-uuid=<module-uuid-if-applicable> -->
```

### GitHub Handoff Decision Flow

```
GitHub operation requested
         │
         ▼
┌─────────────────────────┐
│ Search for linked       │
│ design/module using     │
│ ecos_design_search.py   │
└───────────┬─────────────┘
            │
    ┌───────┴───────┐
    │ Found?        │
    ▼               ▼
   YES              NO
    │               │
    ▼               ▼
┌──────────┐  ┌──────────────┐
│ Include  │  │ Route to EIA │
│ UUIDs in │  │ directly     │
│ handoff  │  └──────────────┘
└────┬─────┘
     │
     ▼
┌──────────────────────────┐
│ Determine target agent   │
│ based on operation type  │
│ (see GitHub routing)     │
└──────────────────────────┘
```

## Protocol for Handing Off Design Operations

### When to Hand Off Design Operations

Design operations require handoff when:
1. **Creating new design** from user requirements
2. **Updating existing design** with changes
3. **Linking design to GitHub** items
4. **Starting implementation** from approved design

### Design Handoff Template

```yaml
---
uuid: <generated-uuid>
from: <agent-name>
to: EAA
timestamp: <ISO-8601>
priority: normal|high|urgent
operation_type: design
design_action: create|update|review|link|implement
---

## Design Context

**Design UUID**: <existing-uuid or "NEW">
**Design Path**: <path or "TBD">
**Design Title**: <title>
**Current Status**: <draft|review|approved|deprecated>

## Request Details

### For New Design
- **Requirements**: <what needs to be designed>
- **Constraints**: <technical/business constraints>
- **Scope**: <what's in/out of scope>

### For Update
- **Reason for Update**: <why change is needed>
- **Affected Sections**: <which parts change>
- **Change Summary**: <brief description>

### For Linking
- **GitHub Target**: <issue/PR/card number>
- **Link Type**: <implements|tracks|relates-to>
- **Link Context**: <why this link exists>

## Pre-Handoff Search Results

Before creating this handoff, ECOS searched for existing designs:
```
Search command: ecos_design_search.py --keyword "<keywords>"
Results: <number> documents found
Relevant matches:
- <path> (UUID: <uuid>, status: <status>)
```

## Expected Deliverable

<What the receiving agent should produce>

## UUID Tracking

This handoff UUID: <uuid>
Related design UUIDs: <list>
Related module UUIDs: <list>
Related GitHub items: <list>
```

### Design Handoff Decision Flow

```
User requests design-related work
              │
              ▼
┌───────────────────────────────┐
│ Run ecos_design_search.py    │
│ with relevant keywords       │
└─────────────┬─────────────────┘
              │
      ┌───────┴───────┐
      │ Existing      │
      │ design found? │
      └───────┬───────┘
              │
      ┌───────┴───────┐
      ▼               ▼
     YES              NO
      │               │
      ▼               ▼
┌───────────────┐ ┌───────────────┐
│ Is it update  │ │ Create NEW    │
│ or link?      │ │ design        │
└───────┬───────┘ │ handoff       │
        │         └───────────────┘
    ┌───┴───┐
    ▼       ▼
 UPDATE   LINK
    │       │
    ▼       ▼
┌────────────────────────────┐
│ Include existing design    │
│ UUID in handoff            │
└────────────────────────────┘
```

## UUID Tracking Across Handoffs

### UUID Chain Concept

Every handoff creates a chain of UUIDs that enables:
1. **Traceability**: Follow work from request to completion
2. **Recovery**: Resume work after session loss
3. **Audit**: Review decision history
4. **Linking**: Connect related GitHub items and designs

### UUID Format Standards

| Type | Format | Example |
|------|--------|---------|
| Handoff UUID | `hoff-{timestamp}-{random}` | `hoff-20250129-a1b2c3` |
| Design UUID | `dsgn-{project}-{random}` | `dsgn-skillf-x4y5z6` |
| Module UUID | `mod-{design}-{random}` | `mod-dsgn-a1b2c3-m7n8` |

### UUID Registry Location

All UUIDs are registered in: `$CLAUDE_PROJECT_DIR/docs_dev/.uuid-registry.json`

```json
{
  "handoffs": {
    "hoff-20250129-a1b2c3": {
      "from": "ecos",
      "to": "eaa",
      "timestamp": "2025-01-29T10:00:00Z",
      "type": "design",
      "related_uuids": ["dsgn-skillf-x4y5z6"]
    }
  },
  "designs": {
    "dsgn-skillf-x4y5z6": {
      "path": "design/feature-x/DESIGN.md",
      "status": "approved",
      "created": "2025-01-29T10:00:00Z",
      "modules": ["mod-dsgn-a1b2c3-m7n8"]
    }
  },
  "modules": {
    "mod-dsgn-a1b2c3-m7n8": {
      "design_uuid": "dsgn-skillf-x4y5z6",
      "name": "component-a",
      "status": "in_progress"
    }
  }
}
```

### UUID Propagation Rules

1. **Handoff creates new UUID**: Every handoff gets a unique UUID
2. **Include parent UUIDs**: Reference triggering handoff UUID
3. **Include sibling UUIDs**: Reference related designs/modules
4. **Update registry**: Register new UUIDs immediately
5. **Cross-reference in GitHub**: Include UUIDs in GitHub item bodies

### UUID Lookup Before Handoff

Before creating any handoff:

```bash
# Search for related designs
python scripts/ecos_design_search.py --keyword "feature-name" --json

# Check existing UUIDs in registry
cat docs_dev/.uuid-registry.json | jq '.designs | keys'
```

Include search results in handoff to prevent duplicate work.
