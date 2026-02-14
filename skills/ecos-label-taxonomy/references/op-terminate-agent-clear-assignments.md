---
name: op-terminate-agent-clear-assignments
description: Operation procedure for terminating an agent and clearing all its issue assignments.
workflow-instruction: "support"
procedure: "support-skill"
---

# Operation: Terminate Agent and Clear Assignments


## Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Find All Issues Assigned to Agent](#step-1-find-all-issues-assigned-to-agent)
  - [Step 2: Remove Assignment and Update Status for Each Issue](#step-2-remove-assignment-and-update-status-for-each-issue)
  - [Step 3: Remove Agent from Team Registry](#step-3-remove-agent-from-team-registry)
  - [Step 4: Verify No Issues Remain Assigned](#step-4-verify-no-issues-remain-assigned)
  - [Step 5: Log Termination](#step-5-log-termination)
- [Example](#example)
- [Error Handling](#error-handling)
- [Considerations](#considerations)

## Purpose

When an agent is being terminated, clear all its issue assignments and return issues to backlog for reassignment.

## When to Use

- When ECOS terminates an agent (completion, failure, or resource constraints)
- When agent session becomes unresponsive
- When agent is being replaced

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Agent name (session name) being terminated
- Write access to `.emasoft/team-registry.json`

## Procedure

### Step 1: Find All Issues Assigned to Agent

```bash
AGENT_ISSUES=$(gh issue list --label "assign:$AGENT_NAME" --json number --jq '.[].number')
echo "Issues to clear: $AGENT_ISSUES"
```

### Step 2: Remove Assignment and Update Status for Each Issue

```bash
for ISSUE in $AGENT_ISSUES; do
  gh issue edit $ISSUE --remove-label "assign:$AGENT_NAME" --add-label "status:backlog"
  echo "Cleared assignment from issue #$ISSUE"
done
```

### Step 3: Remove Agent from Team Registry

```bash
jq 'del(.agents["'$AGENT_NAME'"])' .emasoft/team-registry.json > temp.json && mv temp.json .emasoft/team-registry.json
```

### Step 4: Verify No Issues Remain Assigned

```bash
gh issue list --label "assign:$AGENT_NAME"
# Output should be empty
```

### Step 5: Log Termination

Add a comment to each cleared issue explaining the reassignment:

```bash
for ISSUE in $AGENT_ISSUES; do
  gh issue comment $ISSUE --body "Agent '$AGENT_NAME' terminated. Issue returned to backlog for reassignment."
done
```

## Example

**Scenario:** Terminate agent `implementer-1` which was assigned to issues #42 and #43.

```bash
# Step 1: Find all issues
AGENT_ISSUES=$(gh issue list --label "assign:implementer-1" --json number --jq '.[].number')

# Step 2: Clear each issue
for ISSUE in $AGENT_ISSUES; do
  gh issue edit $ISSUE --remove-label "assign:implementer-1" --add-label "status:backlog"
  echo "Cleared assignment from issue #$ISSUE"
done

# Step 3: Remove from registry
jq 'del(.agents["implementer-1"])' .emasoft/team-registry.json > temp.json && mv temp.json .emasoft/team-registry.json

# Step 4: Verify
gh issue list --label "assign:implementer-1"
# Output: (empty)
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No issues found | Agent had no assignments | Continue with registry removal |
| Label removal fails | Network or permission issue | Retry after brief delay |
| Registry file missing | Path incorrect | Create registry if needed |

## Considerations

- If agent was mid-work, consider adding `status:blocked` instead of `status:backlog`
- Document any partial work in issue comments
- Notify EOA about freed issues for reassignment
