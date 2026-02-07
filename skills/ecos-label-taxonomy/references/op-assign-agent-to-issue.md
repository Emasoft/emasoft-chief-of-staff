---
name: op-assign-agent-to-issue
description: Operation procedure for spawning an agent and assigning it to a GitHub issue using labels.
workflow-instruction: "support"
procedure: "support-skill"
---

# Operation: Assign Agent to Issue

## Purpose

Assign a newly spawned or existing agent to a GitHub issue by applying the appropriate assignment label and updating status.

## When to Use

- When ECOS spawns a new agent and needs to assign work
- When reassigning an issue from one agent to another
- When an agent becomes available and can take on new work

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Issue number to assign
- Agent name (session name) to assign
- Write access to `.emasoft/team-registry.json`

## Procedure

### Step 1: Verify Issue Exists

```bash
gh issue view $ISSUE_NUMBER --json number,title,labels
```

Confirm the issue exists and note any existing labels.

### Step 2: Remove Existing Assignment (if any)

```bash
# Check for existing assign:* labels
EXISTING=$(gh issue view $ISSUE_NUMBER --json labels --jq '.labels[].name | select(startswith("assign:"))')
if [ -n "$EXISTING" ]; then
  gh issue edit $ISSUE_NUMBER --remove-label "$EXISTING"
fi
```

### Step 3: Add Assignment Label

```bash
gh issue edit $ISSUE_NUMBER --add-label "assign:$AGENT_NAME"
```

### Step 4: Update Status from Backlog to Ready

```bash
gh issue edit $ISSUE_NUMBER --remove-label "status:backlog" --add-label "status:ready"
```

### Step 5: Update Team Registry

```bash
jq '.agents["'$AGENT_NAME'"].current_issues += ['$ISSUE_NUMBER']' .emasoft/team-registry.json > temp.json && mv temp.json .emasoft/team-registry.json
```

### Step 6: Verify Assignment

```bash
gh issue view $ISSUE_NUMBER --json labels --jq '.labels[].name'
# Expected output should include: assign:$AGENT_NAME, status:ready
```

## Example

**Scenario:** Assign issue #42 to agent `implementer-1`.

```bash
# Step 1: Add assignment label
gh issue edit 42 --add-label "assign:implementer-1"

# Step 2: Update status
gh issue edit 42 --remove-label "status:backlog" --add-label "status:ready"

# Step 3: Update registry
jq '.agents["implementer-1"].current_issues += [42]' .emasoft/team-registry.json > temp.json && mv temp.json .emasoft/team-registry.json

# Step 4: Verify
gh issue view 42 --json labels --jq '.labels[].name'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Label not found | `assign:*` label doesn't exist | Create with `gh label create "assign:$AGENT_NAME"` |
| Permission denied | Insufficient repo access | Verify GitHub token has repo scope |
| Issue not found | Invalid issue number | Verify with `gh issue list` |
| Registry update fails | Invalid JSON | Validate JSON with `jq . .emasoft/team-registry.json` |

## Rollback

If assignment fails midway:

```bash
# Remove the partial assignment
gh issue edit $ISSUE_NUMBER --remove-label "assign:$AGENT_NAME"
gh issue edit $ISSUE_NUMBER --add-label "status:backlog"
```
