# Project Registry Reference

## Table of Contents

- 1.1 What is the project registry - Central project tracking
- 1.2 Registry structure - Data model and schema
  - 1.2.1 Project entry format - Fields per project
  - 1.2.2 Status values - Valid project states
  - 1.2.3 Metadata fields - Additional project info
- 1.3 Registry operations - CRUD procedures
  - 1.3.1 Add project - Registering new projects
  - 1.3.2 Update project - Modifying project data
  - 1.3.3 Query projects - Searching and filtering
  - 1.3.4 Remove project - Archiving or deleting
- 1.4 Registry persistence - Storage and loading
- 1.5 Registry validation - Ensuring data integrity
- 1.6 Examples - Registry operation scenarios
- 1.7 Troubleshooting - Registry issues

---

## 1.1 What is the project registry

The project registry is a central data store that tracks all projects managed by the Chief of Staff. It provides:

- Single source of truth for project information
- Quick lookup of project status and metadata
- Foundation for multi-project coordination
- Integration point for GitHub Projects sync

---

## 1.2 Registry structure

### 1.2.1 Project entry format

```json
{
  "project_id": "skill-factory",
  "name": "SKILL_FACTORY",
  "path": "/Users/dev/Code/SKILL_FACTORY",
  "status": "active",
  "priority": "high",
  "github": {
    "owner": "Emasoft",
    "repo": "SKILL_FACTORY",
    "project_board": "SKILL_FACTORY Development",
    "project_id": "PVT_xxx"
  },
  "agents_assigned": ["code-impl-01", "test-eng-01"],
  "created_at": "2025-01-15T00:00:00Z",
  "updated_at": "2025-02-01T10:00:00Z",
  "last_sync": "2025-02-01T09:30:00Z",
  "metadata": {
    "language": "python",
    "framework": "claude-code-plugins",
    "tags": ["plugin", "skill", "development"]
  }
}
```

### 1.2.2 Status values

| Status | Description |
|--------|-------------|
| `active` | Project is currently being worked on |
| `paused` | Work temporarily suspended |
| `blocked` | Waiting on external dependency |
| `completed` | All work finished |
| `archived` | No longer active, kept for reference |

### 1.2.3 Metadata fields

| Field | Type | Description |
|-------|------|-------------|
| `language` | string | Primary programming language |
| `framework` | string | Main framework or platform |
| `tags` | list | Searchable tags |
| `description` | string | Project description |
| `contacts` | list | Team contacts |
| `dependencies` | list | Other project IDs this depends on |

---

## 1.3 Registry operations

### 1.3.1 Add project

**Purpose:** Register a new project in the registry.

**Required Fields:**
- `project_id`: Unique identifier (kebab-case)
- `name`: Human-readable name
- `path`: Absolute filesystem path
- `status`: Initial status (usually "active")

**Procedure:**
1. Validate project ID is unique
2. Verify path exists
3. Create project entry
4. Set timestamps
5. Persist registry

**Example:**
```python
add_project({
    "project_id": "my-new-project",
    "name": "My New Project",
    "path": "/Users/dev/my-new-project",
    "status": "active",
    "priority": "normal"
})
```

### 1.3.2 Update project

**Purpose:** Modify existing project data.

**Updatable Fields:**
- `status`
- `priority`
- `agents_assigned`
- `metadata`
- `github` settings

**Procedure:**
1. Load current project entry
2. Apply updates
3. Update `updated_at` timestamp
4. Validate changes
5. Persist registry

### 1.3.3 Query projects

**Purpose:** Search and filter projects.

**Query Types:**

**By ID:**
```python
project = get_project("skill-factory")
```

**By Status:**
```python
active_projects = query_projects(status="active")
```

**By Tag:**
```python
plugin_projects = query_projects(tags=["plugin"])
```

**By Priority:**
```python
high_priority = query_projects(priority="high")
```

### 1.3.4 Remove project

**Purpose:** Archive or delete a project from registry.

**Archive (Recommended):**
1. Set status to "archived"
2. Keep entry for reference
3. Update timestamp

**Delete (Permanent):**
1. Remove entry from registry
2. Optionally backup entry first
3. Persist changes

---

## 1.4 Registry persistence

**Storage Location:**
```
design/config/
└── project-registry.json
```

**Load Procedure:**
1. Read JSON file
2. Parse into memory
3. Validate schema
4. Build lookup indices

**Save Procedure:**
1. Serialize registry to JSON
2. Validate output
3. Write to file atomically (temp + rename)
4. Verify write success

**Backup:**
```
design/config/backups/
└── project-registry.{timestamp}.json
```

---

## 1.5 Registry validation

**Validation Rules:**

- [ ] All project IDs are unique
- [ ] All paths are absolute and exist
- [ ] All status values are valid
- [ ] All timestamps are valid ISO 8601
- [ ] GitHub project IDs match GitHub API
- [ ] No circular dependencies

**Validation Command:**
```bash
python scripts/ecos_validate_registry.py
```

---

## 1.6 Examples

### Example 1: Adding Multiple Projects

```python
# Add three related projects
projects = [
    {
        "project_id": "perfect-skill-suggester",
        "name": "Perfect Skill Suggester",
        "path": "/Users/dev/Code/SKILL_FACTORY/OUTPUT_SKILLS/perfect-skill-suggester",
        "status": "active",
        "priority": "high",
        "metadata": {"tags": ["plugin", "pss"]}
    },
    {
        "project_id": "claude-plugins-validation",
        "name": "Claude Plugins Validation",
        "path": "/Users/dev/Code/SKILL_FACTORY/OUTPUT_SKILLS/claude-plugins-validation",
        "status": "active",
        "priority": "medium",
        "metadata": {"tags": ["plugin", "validation"]}
    },
    {
        "project_id": "emasoft-plugins-marketplace",
        "name": "Emasoft Plugins Marketplace",
        "path": "/Users/dev/Code/SKILL_FACTORY/OUTPUT_SKILLS/emasoft-plugins-marketplace",
        "status": "active",
        "priority": "medium",
        "metadata": {
            "tags": ["marketplace"],
            "dependencies": ["perfect-skill-suggester", "claude-plugins-validation"]
        }
    }
]

for project in projects:
    add_project(project)
```

### Example 2: Querying and Updating

```python
# Find all high-priority active projects
high_priority_active = query_projects(
    status="active",
    priority="high"
)

# Update each to add an agent
for project in high_priority_active:
    update_project(
        project_id=project["project_id"],
        updates={
            "agents_assigned": project.get("agents_assigned", []) + ["code-impl-new"]
        }
    )
```

---

## 1.7 Troubleshooting

### Issue: Project ID already exists

**Symptoms:** Add operation fails with duplicate error.

**Resolution:**
1. Check if existing entry should be updated instead
2. Use a different project ID
3. Archive the old entry if it's obsolete

### Issue: Registry file corrupted

**Symptoms:** JSON parse errors, missing data.

**Resolution:**
1. Restore from backup in design/config/backups/
2. Manually reconstruct from known projects
3. Validate after restoration

### Issue: Path does not exist

**Symptoms:** Project path validation fails.

**Resolution:**
1. Verify the path is correct
2. Check if project was moved
3. Update path in registry
4. Ensure path is absolute, not relative

### Issue: Sync with GitHub fails

**Symptoms:** GitHub project info is stale.

**Resolution:**
1. Verify GitHub authentication (gh auth status)
2. Check GitHub API rate limits
3. Verify project board exists
4. Update GitHub project ID if changed
