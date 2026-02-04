# GitHub Projects Sync Reference

## Table of Contents

- 2.1 What is GitHub Projects sync - Bidirectional synchronization
- 2.2 Sync architecture - How sync works
  - 2.2.1 Local registry - Source of truth for agents
  - 2.2.2 GitHub Projects - Remote project boards
  - 2.2.3 Sync direction - Pull, push, or bidirectional
- 2.3 Sync procedure - Step-by-step synchronization
  - 2.3.1 Authentication - Using gh CLI credentials
  - 2.3.2 Fetch remote state - Reading GitHub Projects
  - 2.3.3 State comparison - Diff local vs remote
  - 2.3.4 Conflict resolution - Handling discrepancies
  - 2.3.5 Apply updates - Writing changes
- 2.4 Field mapping - Local fields to GitHub fields
- 2.5 Sync scheduling - Automatic sync triggers
- 2.6 Examples - Sync scenarios
- 2.7 Troubleshooting - Sync failures

---

## 2.1 What is GitHub Projects sync

GitHub Projects sync is the bidirectional synchronization between the local project registry and GitHub Projects boards. It ensures:

- Project status visible in GitHub UI
- Changes in GitHub reflected locally
- Team members can update status from GitHub
- Automation can track project progress

---

## 2.2 Sync architecture

### 2.2.1 Local registry

The local project registry is the source of truth for agent operations:
- Contains detailed agent assignments
- Has full project metadata
- Includes local-only fields

### 2.2.2 GitHub Projects

GitHub Projects provides:
- Web-based project visibility
- Team collaboration features
- Issue and PR integration
- Automation via Actions

### 2.2.3 Sync direction

| Direction | Description | Use Case |
|-----------|-------------|----------|
| Pull | GitHub -> Local | Get external updates |
| Push | Local -> GitHub | Share agent progress |
| Bidirectional | Both ways | Full sync |

---

## 2.3 Sync procedure

### 2.3.1 Authentication

**Prerequisites:**
- GitHub CLI (gh) installed
- Authenticated via `gh auth login`

**Verify Authentication:**
```bash
gh auth status
# Should show: Logged in to github.com as <username>
```

### 2.3.2 Fetch remote state

**Purpose:** Read current state from GitHub Projects.

**Commands:**

**List Projects:**
```bash
gh project list --owner Emasoft --format json
```

**Get Project Items:**
```bash
gh project item-list <project-number> --owner Emasoft --format json
```

**Get Project Fields:**
```bash
gh project field-list <project-number> --owner Emasoft --format json
```

### 2.3.3 State comparison

**Purpose:** Identify differences between local and remote.

**Comparison Points:**
- Project status
- Priority
- Assigned issues
- Last updated timestamps

**Diff Output Format:**
```json
{
  "project_id": "skill-factory",
  "changes": [
    {
      "field": "status",
      "local": "active",
      "remote": "paused",
      "action": "conflict"
    }
  ]
}
```

### 2.3.4 Conflict resolution

**Conflict Types:**

| Type | Description | Resolution |
|------|-------------|------------|
| Local newer | Local updated after remote | Push local to remote |
| Remote newer | Remote updated after local | Pull remote to local |
| Simultaneous | Both updated | Manual resolution |

**Resolution Strategy:**
1. Compare timestamps
2. Apply newer value
3. If timestamps equal, prefer remote (human input)
4. Log resolution for audit

### 2.3.5 Apply updates

**Push to GitHub:**
```bash
# Update item status
gh project item-edit \
  --project-id PVT_xxx \
  --id PVTI_xxx \
  --field-id PVTF_xxx \
  --single-select-option-id <option-id>
```

**Pull to Local:**
```python
update_project(
    project_id="skill-factory",
    updates={"status": remote_status}
)
```

---

## 2.4 Field mapping

| Local Field | GitHub Field | Sync |
|-------------|--------------|------|
| `status` | Status field | Bidirectional |
| `priority` | Priority field | Bidirectional |
| `agents_assigned` | (not synced) | Local only |
| `path` | (not synced) | Local only |
| `github.project_id` | Project ID | Read only |
| `updated_at` | Updated at | Read only |

**GitHub Status to Local Status Mapping:**

| GitHub Status | Local Status |
|---------------|--------------|
| Todo | active |
| In Progress | active |
| Blocked | blocked |
| Done | completed |

---

## 2.5 Sync scheduling

**Trigger Types:**

| Trigger | Description |
|---------|-------------|
| Manual | User runs sync command |
| Periodic | Every 30 minutes (configurable) |
| On change | After local status change |
| On start | At session start |

**Configuration:**
```yaml
sync:
  enabled: true
  interval_minutes: 30
  on_change: true
  on_start: true
```

---

## 2.6 Examples

### Example 1: Full Sync Workflow

```bash
# Step 1: Check auth
gh auth status

# Step 2: Fetch remote projects
gh project list --owner Emasoft --format json > /tmp/projects.json

# Step 3: Compare with local
python scripts/ecos_compare_projects.py /tmp/projects.json

# Step 4: Apply changes
python scripts/ecos_sync_github_projects.py --direction bidirectional

# Step 5: Verify
python scripts/ecos_verify_sync.py
```

### Example 2: Push Status Update

```python
# After completing a task locally
project_id = "skill-factory"

# Update local status
update_project(project_id, {"status": "completed"})

# Push to GitHub
sync_to_github(project_id)

# Verify sync
github_status = get_github_project_status(project_id)
assert github_status == "Done"
```

### Example 3: Pull External Updates

```python
# Someone updated status in GitHub
project_id = "skill-factory"

# Pull from GitHub
sync_from_github(project_id)

# Check local status updated
local_status = get_project(project_id)["status"]
# Now reflects GitHub status
```

---

## 2.7 Troubleshooting

### Issue: Authentication fails

**Symptoms:** `gh auth status` shows not logged in.

**Resolution:**
1. Run `gh auth login`
2. Follow prompts to authenticate
3. Verify with `gh auth status`
4. Retry sync

### Issue: Rate limit exceeded

**Symptoms:** API errors mentioning rate limit.

**Resolution:**
1. Wait for rate limit reset (usually 1 hour)
2. Reduce sync frequency
3. Use caching to reduce API calls
4. Consider using a GitHub token with higher limits

### Issue: Project not found

**Symptoms:** Sync fails with "project not found" error.

**Resolution:**
1. Verify project exists in GitHub
2. Check owner name is correct
3. Verify project number/ID is correct
4. Check if project was deleted or renamed

### Issue: Field mapping fails

**Symptoms:** Status not syncing correctly.

**Resolution:**
1. Check field IDs in GitHub Project
2. Update field mapping in sync config
3. Verify single-select option IDs match
4. Create missing fields in GitHub if needed

### Issue: Conflicts not resolving

**Symptoms:** Same change keeps bouncing back and forth.

**Resolution:**
1. Manually resolve the conflict
2. Add timestamp to force resolution direction
3. Check for automation loops (GitHub Action triggering local sync triggering GitHub Action)
4. Temporarily disable one direction
