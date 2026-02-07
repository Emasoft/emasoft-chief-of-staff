---
name: op-handle-blocked-agent
description: Operation procedure for handling a blocked agent by updating issue status and optionally escalating.
workflow-instruction: "support"
procedure: "support-skill"
---

# Operation: Handle Blocked Agent

## Purpose

When an agent reports it's blocked on an issue, update the issue status and determine next steps (escalate to human or wait for resolution).

## When to Use

- When agent reports a blocker (missing credentials, external dependency, unclear requirements)
- When agent cannot proceed without human intervention
- When external factors prevent progress

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Issue number that is blocked
- Blocker description from agent

## Procedure

### Step 1: Update Status to Blocked

```bash
gh issue edit $ISSUE_NUMBER --remove-label "status:in-progress" --add-label "status:blocked"
```

### Step 2: Add Comment Explaining Blocker

```bash
gh issue comment $ISSUE_NUMBER --body "Agent blocked: $BLOCKER_REASON. Assigned to human for resolution."
```

### Step 3: Determine Escalation Level

| Blocker Type | Action |
|--------------|--------|
| Missing credentials | Escalate to human immediately |
| External API unavailable | Wait and retry |
| Unclear requirements | Escalate to EAMA |
| Technical dependency | Coordinate with EAA |

### Step 4: Escalate to Human (if needed)

```bash
# Add human assignment while keeping original agent assigned
gh issue edit $ISSUE_NUMBER --add-label "assign:human"
```

### Step 5: Notify via AI Maestro

Use the `agent-messaging` skill to send:
- **Recipient**: `eama-main`
- **Subject**: `Agent blocked on issue #[ISSUE_NUMBER]`
- **Priority**: `high`
- **Content**: type `blocker-escalation`, message: "Agent is blocked: [BLOCKER_REASON]. Human intervention required." Include `issue_number`.

### Step 6: Verify Labels

```bash
gh issue view $ISSUE_NUMBER --json labels --jq '.labels[].name'
# Should show: assign:$AGENT_NAME, assign:human, status:blocked
```

## Example

**Scenario:** Agent reports it's blocked on issue #43 waiting for API credentials.

```bash
# Step 1: Update status
gh issue edit 43 --remove-label "status:in-progress" --add-label "status:blocked"

# Step 2: Add comment
gh issue comment 43 --body "Agent blocked: waiting for external API credentials. Assigned to human for resolution."

# Step 3: Escalate to human
gh issue edit 43 --add-label "assign:human"

# Step 4: Verify
gh issue view 43 --json labels --jq '.labels[].name'
# Output: assign:implementer-1, assign:human, status:blocked, priority:high
```

## Resolving a Blocker

When the blocker is resolved:

```bash
# Remove human assignment if added
gh issue edit $ISSUE_NUMBER --remove-label "assign:human"

# Update status back to in-progress or ready
gh issue edit $ISSUE_NUMBER --remove-label "status:blocked" --add-label "status:in-progress"

# Comment about resolution
gh issue comment $ISSUE_NUMBER --body "Blocker resolved. Agent can proceed."

# Notify agent via AI Maestro
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Label conflict | Multiple status labels | Remove all status labels first, then add blocked |
| AI Maestro unreachable | Service down | Log message and retry later |
| Human not available | No human monitoring | Add priority:critical and create GitHub notification |
