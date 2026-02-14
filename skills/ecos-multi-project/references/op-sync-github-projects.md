---
name: op-sync-github-projects
description: Operation procedure for synchronizing project registry with GitHub Projects board.
workflow-instruction: "support"
procedure: "support-skill"
---

# Operation: Sync GitHub Projects


## Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Load Project Configuration](#step-1-load-project-configuration)
  - [Step 2: Find GitHub Project Board](#step-2-find-github-project-board)
  - [Step 3: Fetch Project Items](#step-3-fetch-project-items)
  - [Step 4: Compare with Local State](#step-4-compare-with-local-state)
  - [Step 5: Apply Sync Direction](#step-5-apply-sync-direction)
  - [Step 6: Update Last Sync Timestamp](#step-6-update-last-sync-timestamp)
  - [Step 7: Log Sync Results](#step-7-log-sync-results)
- [Example](#example)
- [Sync Strategies](#sync-strategies)
- [Error Handling](#error-handling)
- [Conflict Resolution](#conflict-resolution)
- [Notes](#notes)

## Purpose

Synchronize the local project registry with GitHub Projects board to maintain consistent state between local tracking and remote project management.

## When to Use

- Periodically during active work sessions (every 10-15 minutes)
- After external changes to GitHub Project board
- Before generating status reports
- After major project state changes

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Project registered in `.emasoft/project-registry.json`
- GitHub Project board exists for the project
- `jq` installed for JSON processing

## Procedure

### Step 1: Load Project Configuration

```bash
PROJECT_ID="skill-factory"
REGISTRY_FILE=".emasoft/project-registry.json"

GITHUB_REPO=$(jq -r '.projects["'"$PROJECT_ID"'"].github_repo' $REGISTRY_FILE)
GITHUB_PROJECT=$(jq -r '.projects["'"$PROJECT_ID"'"].github_project' $REGISTRY_FILE)

echo "Syncing: $GITHUB_REPO / $GITHUB_PROJECT"
```

### Step 2: Find GitHub Project Board

```bash
# Get project number
PROJECT_NUMBER=$(gh project list --owner ${GITHUB_REPO%%/*} --format json | jq -r '.projects[] | select(.title == "'"$GITHUB_PROJECT"'") | .number')

if [ -z "$PROJECT_NUMBER" ]; then
  echo "ERROR: Project board not found: $GITHUB_PROJECT"
  exit 1
fi
```

### Step 3: Fetch Project Items

```bash
# Get all items from project board
gh project item-list $PROJECT_NUMBER --owner ${GITHUB_REPO%%/*} --limit 100 --format json > /tmp/project_items.json

# Parse items
ITEMS=$(jq -r '.items[] | {id: .id, title: .title, status: .status, assignees: .assignees}' /tmp/project_items.json)
```

### Step 4: Compare with Local State

```bash
# Get local issue states from GitHub
LOCAL_ISSUES=$(gh issue list --repo $GITHUB_REPO --state open --json number,title,labels,assignees)

# Find discrepancies
# - Items in GitHub Project not in local
# - Items with different status
# - Items with different assignees
```

### Step 5: Apply Sync Direction

#### Pull (GitHub to Local)

```bash
# Update local registry with GitHub state
while read ITEM; do
  ISSUE_NUMBER=$(echo $ITEM | jq -r '.number')
  STATUS=$(echo $ITEM | jq -r '.status')

  # Update local tracking
  # (implementation depends on local tracking structure)
done <<< "$ITEMS"
```

#### Push (Local to GitHub)

```bash
# Update GitHub with local state changes
# gh project item-edit --project-id PVT_xxx --id PVTI_xxx --field-id PVTF_xxx --single-select-option-id "Done"
```

### Step 6: Update Last Sync Timestamp

```bash
jq '.projects["'"$PROJECT_ID"'"].last_sync = "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"' $REGISTRY_FILE > temp.json && mv temp.json $REGISTRY_FILE
```

### Step 7: Log Sync Results

```bash
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Synced $PROJECT_ID: $ITEM_COUNT items" >> docs_dev/sync-log.txt
```

## Example

**Scenario:** Sync SKILL_FACTORY project with its GitHub Project board.

```bash
# Step 1: Load config
PROJECT_ID="skill-factory"
GITHUB_REPO="Emasoft/SKILL_FACTORY"
GITHUB_PROJECT="SKILL_FACTORY Development"

# Step 2: Find project
PROJECT_NUMBER=$(gh project list --owner Emasoft --format json | jq -r '.projects[] | select(.title == "SKILL_FACTORY Development") | .number')

# Step 3: Fetch items
gh project item-list $PROJECT_NUMBER --owner Emasoft --limit 100 --format json > /tmp/project_items.json

# Step 4: Check for recent changes
RECENT_CHANGES=$(jq '[.items[] | select(.updatedAt > (now - 900 | strftime("%Y-%m-%dT%H:%M:%SZ")))]' /tmp/project_items.json)
echo "Recent changes: $(echo $RECENT_CHANGES | jq length) items"

# Step 5: Update timestamp
jq '.projects["skill-factory"].last_sync = "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"' .emasoft/project-registry.json > temp.json && mv temp.json .emasoft/project-registry.json
```

## Sync Strategies

| Strategy | When to Use |
|----------|-------------|
| Pull-only | Trust GitHub as source of truth |
| Push-only | Trust local as source of truth |
| Bidirectional | Merge changes from both sides |
| Pull-with-override | Pull but keep specific local overrides |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Rate limit exceeded | Too many API calls | Implement exponential backoff |
| Project not found | Wrong project name or number | Verify project exists |
| Auth error | Token expired | Re-authenticate with `gh auth login` |
| Sync conflict | Concurrent modifications | Use timestamp-based conflict resolution |

## Conflict Resolution

When both local and remote have changes:

1. **Timestamp wins**: Most recent update takes precedence
2. **Remote wins**: GitHub is source of truth for external changes
3. **Local wins**: Agent actions take precedence (rare)

## Notes

- Run sync before making major changes
- Log all syncs for debugging
- Handle partial syncs gracefully
- Consider GitHub API rate limits
