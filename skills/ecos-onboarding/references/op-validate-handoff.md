---
operation: validate-handoff
procedure: proc-create-team
workflow-instruction: Step 4 - Team Creation
parent-skill: ecos-onboarding
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Validate Handoff Document


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Check Required Fields](#step-1-check-required-fields)
  - [Step 2: Verify UUID Is Unique](#step-2-verify-uuid-is-unique)
  - [Step 3: Verify Target Agent Exists](#step-3-verify-target-agent-exists)
  - [Step 4: Verify Referenced Files Exist](#step-4-verify-referenced-files-exist)
  - [Step 5: Check for Placeholder Markers](#step-5-check-for-placeholder-markers)
  - [Step 6: Validate Markdown Format](#step-6-validate-markdown-format)
  - [Step 7: Verify Current State Is Accurate](#step-7-verify-current-state-is-accurate)
  - [Step 8: Run Validation Script (If Available)](#step-8-run-validation-script-if-available)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Complete Handoff Validation](#example-complete-handoff-validation)
  - [Example: Fixing Common Validation Issues](#example-fixing-common-validation-issues)
  - [Example: Validation Script Usage](#example-validation-script-usage)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

- Before sending any handoff document to an agent
- When reviewing handoffs created by other agents
- During handoff quality audits
- When handoff-related issues occur

## Prerequisites

- Handoff document exists
- Target agent is identified
- Referenced files are accessible
- AI Maestro is running (for agent verification)

## Procedure

### Step 1: Check Required Fields

Every handoff document must have:

| Field | Description | Example |
|-------|-------------|---------|
| `from` | Sending agent name | `ecos-chief-of-staff` |
| `to` | Target agent name | `dev-backend-alice` |
| `type` | Handoff type | `project-handoff`, `role-briefing`, `emergency-handoff` |
| `UUID` | Unique handoff identifier | `HO-20250204-backend-001` |
| `task` | Task or role being handed off | `Backend API Development` |

```bash
# Check if document has required fields
grep -E "^(from|to|type|UUID|task):" /path/to/handoff.md
```

### Step 2: Verify UUID Is Unique

```bash
# Check existing handoffs
ls $CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/

# Ensure UUID doesn't already exist
grep -r "<UUID>" $CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/
# Should return nothing for new handoffs
```

### Step 3: Verify Target Agent Exists

Use the `ai-maestro-agents-management` skill to:
1. List all agents and verify the target agent name exists
2. Check the target agent's status (running or hibernated)

### Step 4: Verify Referenced Files Exist

```bash
# Extract file references from handoff
grep -oE '[-a-zA-Z0-9_/]+\.(py|md|json|yaml|yml|js|ts)' /path/to/handoff.md | while read filepath; do
  if [ -f "$filepath" ]; then
    echo "OK: $filepath"
  else
    echo "MISSING: $filepath"
  fi
done
```

### Step 5: Check for Placeholder Markers

```bash
# Find [TBD], TODO, FIXME, or placeholder text
grep -E '\[TBD\]|\[TODO\]|FIXME|<.*placeholder.*>|<REPLACE' /path/to/handoff.md

# Should return nothing for complete handoffs
```

### Step 6: Validate Markdown Format

```bash
# Check for broken links
grep -oE '\[.*\]\(.*\)' /path/to/handoff.md | while read link; do
  echo "Checking: $link"
done

# Check for unclosed formatting
grep -E '^\*[^*]+$|^_[^_]+$' /path/to/handoff.md
```

### Step 7: Verify Current State Is Accurate

Manual verification:
- Check stated progress percentages match actual state
- Verify "current line" references are still valid
- Confirm blockers list is up to date

### Step 8: Run Validation Script (If Available)

```bash
python scripts/ecos_validate_handoff.py --file /path/to/handoff.md
```

## Checklist

Copy this checklist and track your progress:

**Required Fields:**
- [ ] `from` field present and valid
- [ ] `to` field present and matches target agent
- [ ] `type` field present and valid
- [ ] `UUID` field present and unique
- [ ] `task` field present and descriptive

**Agent Verification:**
- [ ] Target agent exists in AI Maestro
- [ ] Target agent is alive (running/hibernated)

**Content Verification:**
- [ ] All referenced files exist
- [ ] No [TBD] or placeholder markers
- [ ] Markdown formatting is correct
- [ ] No broken internal links

**Accuracy Verification:**
- [ ] Progress percentages are accurate
- [ ] Line number references are current
- [ ] Blocker list is up to date
- [ ] Contact information is correct

**Documentation:**
- [ ] Acceptance criteria clearly defined
- [ ] Contact for questions provided

## Examples

### Example: Complete Handoff Validation

```bash
HANDOFF="/tmp/handoff-backend-api.md"

echo "=== Validating Handoff ==="

# Step 1: Required fields
echo "Checking required fields..."
for field in from to type UUID task; do
  if grep -q "^$field:" "$HANDOFF"; then
    echo "OK: $field present"
  else
    echo "MISSING: $field"
  fi
done

# Step 2: UUID uniqueness
UUID=$(grep "^UUID:" "$HANDOFF" | cut -d: -f2 | tr -d ' ')
echo "Checking UUID uniqueness: $UUID"
EXISTING=$(grep -r "$UUID" $CLAUDE_PROJECT_DIR/thoughts/shared/handoffs/ 2>/dev/null | wc -l)
if [ "$EXISTING" -eq 0 ]; then
  echo "OK: UUID is unique"
else
  echo "ERROR: UUID already exists"
fi

# Step 3: Target agent exists
TARGET=$(grep "^to:" "$HANDOFF" | cut -d: -f2 | tr -d ' ')
echo "Checking target agent: $TARGET"
if check_agent_status "$TARGET"; then  # Use ai-maestro-agents-management skill
  echo "OK: Agent exists and is accessible"
else
  echo "ERROR: Agent not found"
fi

# Step 4: Referenced files
echo "Checking referenced files..."
grep -oE '~/[^ ]+|/[a-zA-Z0-9/_.-]+\.(py|md|json)' "$HANDOFF" | sort -u | while read f; do
  expanded=$(eval echo $f)
  if [ -f "$expanded" ]; then
    echo "OK: $f"
  else
    echo "MISSING: $f"
  fi
done

# Step 5: Placeholders
echo "Checking for placeholders..."
PLACEHOLDERS=$(grep -cE '\[TBD\]|\[TODO\]|FIXME|<REPLACE' "$HANDOFF" || echo 0)
if [ "$PLACEHOLDERS" -eq 0 ]; then
  echo "OK: No placeholders found"
else
  echo "ERROR: Found $PLACEHOLDERS placeholders"
  grep -nE '\[TBD\]|\[TODO\]|FIXME|<REPLACE' "$HANDOFF"
fi

echo "=== Validation Complete ==="
```

### Example: Fixing Common Validation Issues

**Issue: Missing UUID**
```markdown
# Before (invalid)
from: ecos-chief-of-staff
to: dev-backend-alice
type: project-handoff
task: Backend API

# After (valid)
from: ecos-chief-of-staff
to: dev-backend-alice
type: project-handoff
UUID: HO-20250204-backend-001
task: Backend API Development
```

**Issue: Placeholder not replaced**
```markdown
# Before (invalid)
Current work: [TBD - fill in current task]

# After (valid)
Current work: Implementing user update endpoint at src/api/users.py line 145
```

**Issue: Broken file reference**
```markdown
# Before (invalid)
Key file: src/api/usres.py  # typo

# After (valid)
Key file: src/api/users.py
```

### Example: Validation Script Usage

```bash
# Full validation with verbose output
python scripts/ecos_validate_handoff.py --file /tmp/handoff.md --verbose

# Expected output:
# Validating: /tmp/handoff.md
# [OK] Required field: from
# [OK] Required field: to
# [OK] Required field: type
# [OK] Required field: UUID
# [OK] Required field: task
# [OK] Target agent exists: dev-backend-alice
# [OK] UUID is unique: HO-20250204-backend-001
# [OK] File exists: ~/projects/backend-api/src/api/users.py
# [OK] No placeholders found
#
# Validation PASSED
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Required field missing | Incomplete handoff template | Add missing field |
| UUID not unique | Reused identifier | Generate new UUID |
| Target agent not found | Wrong name or agent terminated | Verify agent name, spawn if needed |
| Referenced file missing | Path changed or file deleted | Update path or note file absence |
| Placeholders present | Incomplete drafting | Replace all placeholders with actual content |
| Agent cannot read files | Path not in agent's access | Use accessible paths or copy files |

## Related Operations

- [op-conduct-project-handoff.md](op-conduct-project-handoff.md) - Create handoffs
- [op-deliver-role-briefing.md](op-deliver-role-briefing.md) - Role briefings
- [op-execute-onboarding-checklist.md](op-execute-onboarding-checklist.md) - Full onboarding
