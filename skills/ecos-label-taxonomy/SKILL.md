---
name: ecos-label-taxonomy
description: "Use when applying or checking GitHub labels for agent assignment and status tracking. GitHub label taxonomy reference for the Chief of Staff Agent. Trigger with `/ecos-label-taxonomy`."
license: Apache-2.0
compatibility: Requires AI Maestro installed.
version: 1.0.0
metadata:
  author: Emasoft
---

# ECOS Label Taxonomy

## Overview

This skill provides the label taxonomy relevant to the Chief of Staff Agent (ECOS) role. Each role plugin has its own label-taxonomy skill covering the labels that role manages.

---

## Prerequisites

1. GitHub repository with label support
2. Understanding of agent role prefixes (ecos-, eoa-, eia-, eaa-, eama-)
3. Read **AGENT_OPERATIONS.md** in docs/ folder for session naming
4. GitHub CLI (`gh`) installed and authenticated
5. Access to team registry at `.emasoft/team-registry.json`

---

## Instructions

1. Identify the label category needed (assign, status, priority)
2. Check if label exists on the issue/PR
3. Apply or modify label using gh CLI or GitHub API
4. Verify label was applied correctly
5. Update team registry if assignment labels changed

### Checklist

Copy this checklist and track your progress:

- [ ] Identify label category (assign/status/priority)
- [ ] Check existing labels on issue with `gh issue view <number>`
- [ ] Remove conflicting labels if needed
- [ ] Apply new label via `gh issue edit --add-label`
- [ ] Verify label appears correctly
- [ ] Update `.emasoft/team-registry.json` if agent assignment changed

---

## Output

| Output Type | Description | Example |
|-------------|-------------|---------|
| Label Applied | Label successfully added to issue | `assign:eoa-svgbbox-orchestrator` |
| Label Removed | Old label removed before new one | `status:pending` removed |
| Status Updated | Issue status changed via label | `status:in-progress` applied |
| Verification | Confirmation of label state | Labels: assign:implementer-1, status:ready, priority:high |
| Registry Synced | Team registry updated to match labels | `current_issues: [42, 43]` in team-registry.json |

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Label not found | Label doesn't exist in repo | Create label first with `gh label create` |
| Permission denied | Insufficient repo access | Verify GitHub token has repo scope |
| Duplicate assign labels | Multiple assign:* labels on issue | Remove old assign label before adding new |
| Registry out of sync | Labels don't match team-registry.json | Run sync check script to reconcile |
| gh CLI not authenticated | GitHub token expired or missing | Run `gh auth login` |
| Issue not found | Invalid issue number | Verify issue exists with `gh issue list` |

---

## Examples

### Example 1: Spawning Agent and Assigning to Issue

**Scenario**: ECOS spawns a new agent "implementer-1" and assigns it to issue #42.

```bash
# Step 1: Add assignment label
gh issue edit 42 --add-label "assign:implementer-1"

# Step 2: Update status from backlog to ready
gh issue edit 42 --remove-label "status:backlog" --add-label "status:ready"

# Step 3: Update team registry
jq '.agents["implementer-1"].current_issues += [42]' .emasoft/team-registry.json > temp.json && mv temp.json .emasoft/team-registry.json

# Step 4: Verify
gh issue view 42 --json labels --jq '.labels[].name'
# Output: assign:implementer-1, status:ready
```

### Example 2: Terminating Agent and Clearing Assignments

**Scenario**: Agent "implementer-1" is being terminated. Clear all its assignments.

```bash
# Step 1: Find all issues assigned to agent
AGENT_ISSUES=$(gh issue list --label "assign:implementer-1" --json number --jq '.[].number')

# Step 2: Remove assignment and update status
for ISSUE in $AGENT_ISSUES; do
  gh issue edit $ISSUE --remove-label "assign:implementer-1" --add-label "status:backlog"
  echo "Cleared assignment from issue #$ISSUE"
done

# Step 3: Update team registry
jq 'del(.agents["implementer-1"])' .emasoft/team-registry.json > temp.json && mv temp.json .emasoft/team-registry.json

# Step 4: Verify no issues remain assigned
gh issue list --label "assign:implementer-1"
# Output: (empty)
```

### Example 3: Handling Blocked Agent

**Scenario**: Agent reports it's blocked on issue #43. ECOS updates status and notifies.

```bash
# Step 1: Update status to blocked
gh issue edit 43 --remove-label "status:in-progress" --add-label "status:blocked"

# Step 2: Add comment explaining blocker
gh issue comment 43 --body "Agent blocked: waiting for external API credentials. Assigned to human for resolution."

# Step 3: Escalate to human if needed
gh issue edit 43 --add-label "assign:human"

# Step 4: Verify
gh issue view 43 --json labels --jq '.labels[].name'
# Output: assign:human, status:blocked, priority:high
```

---

## Labels ECOS Manages

### Assignment Labels (`assign:*`)

**ECOS coordinates with EOA on agent assignments.**

| Label | Description | When ECOS Is Involved |
|-------|-------------|----------------------|
| `assign:<agent-name>` | Specific agent | When spawning/managing agents |
| `assign:orchestrator` | EOA handling | When escalating to EOA |
| `assign:human` | Human needed | When human intervention required |

**ECOS Assignment Responsibilities:**
- Track which agents are assigned to which issues
- Reassign when agent becomes unavailable
- Clear assignments when agents are terminated

### Status Labels ECOS Updates

| Label | When ECOS Sets It |
|-------|------------------|
| `status:on-hold` | When pausing work (resource constraints) |
| `status:blocked` | When agent reports blocker |
| `status:ready` | When blocker resolved |

---

## Labels ECOS Monitors

### Priority Labels (`priority:*`)

ECOS uses priority for resource allocation:
- `priority:critical` - Ensure agent assigned immediately
- `priority:high` - Prioritize in staffing decisions
- `priority:normal` - Standard allocation
- `priority:low` - Can wait for resources

### Status Labels (`status:*`)

ECOS monitors all status changes:
- `status:blocked` - May need to reassign or escalate
- `status:in-progress` - Track for timeout/health monitoring
- `status:needs-review` - Route to EIA if not already

---

## ECOS Label Commands

### When Agent Spawned

```bash
# Assign new agent to issue
gh issue edit $ISSUE_NUMBER --add-label "assign:$NEW_AGENT_NAME"
gh issue edit $ISSUE_NUMBER --remove-label "status:backlog" --add-label "status:ready"
```

### When Agent Terminated

```bash
# Clear assignment from all agent's issues
AGENT_ISSUES=$(gh issue list --label "assign:$AGENT_NAME" --json number --jq '.[].number')
for ISSUE in $AGENT_ISSUES; do
  gh issue edit $ISSUE --remove-label "assign:$AGENT_NAME" --add-label "status:backlog"
done
```

### When Agent Blocked

```bash
# Mark issue blocked
gh issue edit $ISSUE_NUMBER --remove-label "status:in-progress" --add-label "status:blocked"
```

### When Escalating to Human

```bash
# Reassign to human
gh issue edit $ISSUE_NUMBER --remove-label "assign:$AGENT_NAME" --add-label "assign:human"
```

---

## Agent Registry and Labels

ECOS maintains the team registry at `.emasoft/team-registry.json`. Labels should be synchronized:

```json
{
  "agents": {
    "implementer-1": {
      "session_name": "code-impl-01",
      "status": "active",
      "current_issues": [42, 43]  // Should match assign:implementer-1 labels
    }
  }
}
```

### Sync Check

```bash
# Find issues assigned to agent
LABELED=$(gh issue list --label "assign:implementer-1" --json number --jq '.[].number' | sort)

# Compare with registry
REGISTERED=$(jq -r '.agents["implementer-1"].current_issues | sort | .[]' .emasoft/team-registry.json)

# Should match
```

---

## Quick Reference

### ECOS Label Responsibilities

| Action | Labels Involved |
|--------|-----------------|
| Spawn agent | Add `assign:<agent>`, update `status:ready` |
| Terminate agent | Remove `assign:<agent>`, set `status:backlog` |
| Agent blocked | Update to `status:blocked` |
| Resolve blocker | Update to `status:ready` or `status:in-progress` |
| Escalate to human | Add `assign:human` |
| Put on hold | Add `status:on-hold` |

### Labels ECOS Never Sets

- `type:*` - Set at issue creation
- `effort:*` - Set during triage by EOA
- `review:*` - Managed by EIA
- `priority:*` - Set by EOA or EAMA (ECOS can suggest changes)

---

## Resources

- **AGENT_OPERATIONS.md** - Canonical operations reference (in docs/ folder)
- **ecos-agent-lifecycle** - Agent spawn/terminate procedures
- **ecos-team-registry** - Team registry management skill
- [GitHub Labels Documentation](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels)
- [GitHub CLI Labels Reference](https://cli.github.com/manual/gh_label)
