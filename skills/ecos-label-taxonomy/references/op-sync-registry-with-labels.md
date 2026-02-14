---
name: op-sync-registry-with-labels
description: Operation procedure for synchronizing team registry with GitHub issue labels.
workflow-instruction: "support"
procedure: "support-skill"
---

# Operation: Sync Registry with Labels


## Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Load Current Registry](#step-1-load-current-registry)
  - [Step 2: For Each Agent, Compare Registry vs Labels](#step-2-for-each-agent-compare-registry-vs-labels)
  - [Step 3: Identify Discrepancies](#step-3-identify-discrepancies)
  - [Step 4: Reconcile Registry to Match Labels](#step-4-reconcile-registry-to-match-labels)
  - [Step 5: Handle Orphaned Labels](#step-5-handle-orphaned-labels)
  - [Step 6: Log Sync Results](#step-6-log-sync-results)
- [Example](#example)
- [Automated Sync Script](#automated-sync-script)
- [Error Handling](#error-handling)

## Purpose

Ensure the team registry at `.emasoft/team-registry.json` stays synchronized with GitHub issue assignment labels. Detect and resolve discrepancies.

## When to Use

- Periodically (recommended: every 10 minutes during active work)
- After agent spawn or termination
- When inconsistencies are suspected
- Before generating status reports

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Write access to `.emasoft/team-registry.json`
- `jq` installed for JSON processing

## Procedure

### Step 1: Load Current Registry

```bash
REGISTRY=$(cat .emasoft/team-registry.json)
AGENTS=$(echo $REGISTRY | jq -r '.agents | keys[]')
```

### Step 2: For Each Agent, Compare Registry vs Labels

```bash
for AGENT in $AGENTS; do
  # Get issues from registry
  REGISTERED=$(echo $REGISTRY | jq -r '.agents["'$AGENT'"].current_issues | sort | .[]' 2>/dev/null)

  # Get issues from GitHub labels
  LABELED=$(gh issue list --label "assign:$AGENT" --json number --jq '.[].number' | sort)

  echo "Agent: $AGENT"
  echo "  Registry: $REGISTERED"
  echo "  Labeled:  $LABELED"
done
```

### Step 3: Identify Discrepancies

For each agent:

| Situation | Meaning | Action |
|-----------|---------|--------|
| In registry, not labeled | Registry stale | Remove from registry |
| Labeled, not in registry | Registry outdated | Add to registry |
| Both match | Synchronized | No action needed |

### Step 4: Reconcile Registry to Match Labels

Labels are source of truth. Update registry:

```bash
for AGENT in $AGENTS; do
  # Get actual labeled issues
  LABELED_ISSUES=$(gh issue list --label "assign:$AGENT" --state open --json number --jq '[.[].number]')

  # Update registry
  jq '.agents["'$AGENT'"].current_issues = '"$LABELED_ISSUES"'' .emasoft/team-registry.json > temp.json && mv temp.json .emasoft/team-registry.json
done
```

### Step 5: Handle Orphaned Labels

Find labels for agents not in registry:

```bash
# Get all assign:* labels in repo
ALL_ASSIGN_LABELS=$(gh label list --json name --jq '.[] | select(.name | startswith("assign:")) | .name')

for LABEL in $ALL_ASSIGN_LABELS; do
  AGENT_NAME=$(echo $LABEL | sed 's/assign://')

  # Check if agent exists in registry
  EXISTS=$(jq '.agents["'$AGENT_NAME'"]' .emasoft/team-registry.json)

  if [ "$EXISTS" = "null" ]; then
    echo "WARNING: Label '$LABEL' exists but agent not in registry"
    # Either add agent to registry or remove labels
  fi
done
```

### Step 6: Log Sync Results

```bash
echo "Sync completed at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> docs_dev/sync-log.txt
```

## Example

**Scenario:** Check sync for agent `implementer-1`.

```bash
# Get labeled issues
LABELED=$(gh issue list --label "assign:implementer-1" --json number --jq '.[].number' | sort)
echo "Labeled: $LABELED"

# Get registered issues
REGISTERED=$(jq -r '.agents["implementer-1"].current_issues | sort | .[]' .emasoft/team-registry.json)
echo "Registered: $REGISTERED"

# Compare
if [ "$LABELED" = "$REGISTERED" ]; then
  echo "SYNC OK: Registry matches labels"
else
  echo "SYNC NEEDED: Discrepancy detected"
  # Update registry
  LABELED_JSON=$(gh issue list --label "assign:implementer-1" --state open --json number --jq '[.[].number]')
  jq '.agents["implementer-1"].current_issues = '"$LABELED_JSON"'' .emasoft/team-registry.json > temp.json && mv temp.json .emasoft/team-registry.json
fi
```

## Automated Sync Script

For scheduled sync, create a script:

```bash
#!/bin/bash
# scripts/ecos_sync_labels.sh

REGISTRY_FILE=".emasoft/team-registry.json"

# Backup current registry
cp $REGISTRY_FILE "${REGISTRY_FILE}.bak"

# Get all agents
AGENTS=$(jq -r '.agents | keys[]' $REGISTRY_FILE)

for AGENT in $AGENTS; do
  # Get labeled issues (open only)
  LABELED=$(gh issue list --label "assign:$AGENT" --state open --json number --jq '[.[].number]')

  # Update registry
  jq '.agents["'"$AGENT"'"].current_issues = '"$LABELED"'' $REGISTRY_FILE > temp.json && mv temp.json $REGISTRY_FILE
done

echo "Sync complete: $(date)"
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| jq parse error | Malformed JSON | Restore from backup, fix manually |
| gh rate limited | Too many API calls | Wait and retry with exponential backoff |
| Registry file missing | Path incorrect or deleted | Create new registry from labels |
| Permission denied | File not writable | Check file permissions |
