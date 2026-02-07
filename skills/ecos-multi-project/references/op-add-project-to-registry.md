---
name: op-add-project-to-registry
description: Operation procedure for adding a new project to the project registry.
workflow-instruction: "support"
procedure: "support-skill"
---

# Operation: Add Project to Registry

## Purpose

Register a new project in the Chief of Staff's project registry for multi-project management and tracking.

## When to Use

- When onboarding a new codebase
- When starting work on a previously untracked project
- When setting up a new repository

## Prerequisites

- Project registry file exists at `.emasoft/project-registry.json`
- GitHub repository exists and is accessible
- GitHub CLI (`gh`) installed and authenticated
- `jq` installed for JSON processing

## Procedure

### Step 1: Verify Registry File Exists

```bash
REGISTRY_FILE=".emasoft/project-registry.json"
if [ ! -f "$REGISTRY_FILE" ]; then
  mkdir -p .emasoft
  echo '{"projects": {}}' > $REGISTRY_FILE
fi
```

### Step 2: Gather Project Information

| Field | Description | Example |
|-------|-------------|---------|
| id | Unique identifier (kebab-case) | `skill-factory` |
| path | Local filesystem path | `{baseDir}/SKILL_FACTORY` |
| status | Current state | `active`, `paused`, `archived` |
| github_repo | GitHub owner/repo | `Emasoft/SKILL_FACTORY` |
| github_project | GitHub Project board name | `SKILL_FACTORY Development` |
| priority | Project priority | `high`, `normal`, `low` |

### Step 3: Validate GitHub Repository

```bash
gh repo view $GITHUB_REPO --json name,owner
# Should return valid repo info
```

### Step 4: Add Project Entry

```bash
PROJECT_ID="$ID"
PROJECT_PATH="$PATH"
GITHUB_REPO="$REPO"
GITHUB_PROJECT="$PROJECT_BOARD"
PRIORITY="$PRIORITY"

jq '.projects["'"$PROJECT_ID"'"] = {
  "id": "'"$PROJECT_ID"'",
  "path": "'"$PROJECT_PATH"'",
  "status": "active",
  "github_repo": "'"$GITHUB_REPO"'",
  "github_project": "'"$GITHUB_PROJECT"'",
  "last_sync": "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'",
  "agents_assigned": [],
  "priority": "'"$PRIORITY"'"
}' $REGISTRY_FILE > temp.json && mv temp.json $REGISTRY_FILE
```

### Step 5: Verify Entry Added

```bash
jq '.projects["'"$PROJECT_ID"'"]' $REGISTRY_FILE
```

### Step 6: Initialize Project Labels (if needed)

```bash
# Create standard labels in the project repo
cd $PROJECT_PATH
for LABEL in "status:backlog" "status:ready" "status:in-progress" "status:done" \
             "priority:critical" "priority:high" "priority:normal" "priority:low"; do
  gh label create "$LABEL" --force 2>/dev/null || true
done
```

## Example

**Scenario:** Add the SKILL_FACTORY project to the registry.

```bash
# Step 1: Ensure registry exists
REGISTRY_FILE=".emasoft/project-registry.json"
mkdir -p .emasoft
[ -f "$REGISTRY_FILE" ] || echo '{"projects": {}}' > $REGISTRY_FILE

# Step 2: Validate GitHub repo
gh repo view Emasoft/SKILL_FACTORY --json name
# Output: {"name":"SKILL_FACTORY"}

# Step 3: Add entry
jq '.projects["skill-factory"] = {
  "id": "skill-factory",
  "path": "{baseDir}/SKILL_FACTORY",
  "status": "active",
  "github_repo": "Emasoft/SKILL_FACTORY",
  "github_project": "SKILL_FACTORY Development",
  "last_sync": "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'",
  "agents_assigned": [],
  "priority": "high"
}' $REGISTRY_FILE > temp.json && mv temp.json $REGISTRY_FILE

# Step 4: Verify
jq '.projects["skill-factory"]' $REGISTRY_FILE
```

## Registry Entry Schema

```json
{
  "id": "string (required)",
  "path": "string (required)",
  "status": "active|paused|archived (required)",
  "github_repo": "string (optional)",
  "github_project": "string (optional)",
  "last_sync": "ISO-8601 timestamp",
  "agents_assigned": ["agent_name", ...],
  "priority": "critical|high|normal|low"
}
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| JSON parse error | Malformed registry | Restore from backup, fix JSON |
| Duplicate ID | Project already exists | Use update operation instead |
| GitHub repo not found | Wrong repo name or no access | Verify repo name and permissions |
| Path doesn't exist | Invalid local path | Create directory or fix path |

## Notes

- Project ID must be unique across all registered projects
- Use `{baseDir}` placeholder for portable paths
- Set appropriate priority to influence agent allocation
- Run GitHub sync after adding to populate issue data
