# Registry Sync and Multi-Project Coordination

## Contents

- [1.1 Initializing the Project Registry for First-Time Setup](#11-initializing-the-project-registry-for-first-time-setup)
- [1.2 Adding a New Project to the Multi-Project Registry](#12-adding-a-new-project-to-the-multi-project-registry)
- [1.3 Removing a Project from the Registry](#13-removing-a-project-from-the-registry)
- [1.4 Listing All Projects with Status Filtering](#14-listing-all-projects-with-status-filtering)
- [1.5 Syncing Project Registry with GitHub Projects Boards](#15-syncing-project-registry-with-github-projects-boards)
- [1.6 Managing Cross-Project Dependencies](#16-managing-cross-project-dependencies)
- [1.7 Assigning Agents to Projects](#17-assigning-agents-to-projects)
- [1.8 Updating Registry State Files Safely](#18-updating-registry-state-files-safely)
- [1.9 Resolving Agent Conflicts Across Multiple Projects](#19-resolving-agent-conflicts-across-multiple-projects)
- [1.10 Mapping GitHub Project Board Statuses to Internal States](#110-mapping-github-project-board-statuses-to-internal-states)

---

## 1.1 Initializing the Project Registry for First-Time Setup

**When to use**: When setting up the Chief of Staff system for the first time, or when the state file has been deleted or corrupted.

**State file location**: `.claude/chief-of-staff-state.local.md`

**Procedure**:

1. Check if the state file exists at `.claude/chief-of-staff-state.local.md`
2. If it does not exist, create the file with the following template:

```yaml
# Chief of Staff State File
# Auto-managed by ecos-project-coordinator
# Last updated: <timestamp>

projects: []

dependencies: []

agent_assignments: {}
```

3. Replace `<timestamp>` with the current ISO 8601 timestamp (e.g., `2025-02-05T14:30:00Z`)
4. Ensure the file is created in the project root under `.claude/` directory
5. Add `.claude/chief-of-staff-state.local.md` to `.gitignore` if not already present (this is a local-only state file)

**Expected result**: An empty but valid state file ready to accept project registrations.

---

## 1.2 Adding a New Project to the Multi-Project Registry

**When to use**: When starting to track a new repository or project that needs multi-agent coordination.

**Required information**:
- Project ID (unique, kebab-case identifier, e.g., `skill-factory`)
- Repository URL (GitHub repository URL)

**Optional information**:
- GitHub Projects board URL
- Local filesystem path to the repository
- Human-readable project name

**Procedure**:

1. Validate the project ID:
   - Must be unique (not already in registry)
   - Must be kebab-case (lowercase, hyphens only)
   - Must not contain spaces or special characters

2. Validate the repository URL:
   - Must be a valid GitHub URL
   - Check repository accessibility using `gh repo view <repo-url>`

3. Read the current state file at `.claude/chief-of-staff-state.local.md`

4. Parse the YAML structure

5. Add a new project entry to the `projects` array:

```yaml
projects:
  - id: "<project-id>"
    name: "<Project Name>"
    repo_url: "<repository-url>"
    github_project_board: "<board-url-or-null>"
    local_path: "<local-path-or-null>"
    active_agents: []
    status: "active"
    last_sync: "<current-timestamp>"
```

6. Update the `last_updated` timestamp at the top of the file

7. Write the updated YAML back to the state file

8. If this is a significant change (first project, or major milestone), commit the change to git

**Expected result**: The new project appears in the registry and can be queried with `/ecos-list-projects`.

---

## 1.3 Removing a Project from the Registry

**When to use**: When a project is completed, archived, or no longer needs coordination tracking.

**Safety checks required**:
1. Check if any agents are currently assigned to the project
2. Check if the project has pending tasks or dependencies
3. Warn the user if either condition is true
4. Require `--force` flag to override warnings

**Procedure**:

1. Read the current state file

2. Locate the project by ID in the `projects` array

3. If project not found, return error: "Project <id> not found in registry"

4. Check the project's `active_agents` array:
   - If not empty and `--force` is not provided, abort with warning
   - List the currently assigned agents

5. Check if the project appears in any `dependencies` entries:
   - Search both `from_project` and `to_project` fields
   - If found and `--force` is not provided, abort with warning

6. If all checks pass or `--force` is provided:
   - Remove the project entry from the `projects` array
   - Remove any dependencies referencing this project
   - Remove any agent assignments for this project from `agent_assignments`

7. Update the `last_updated` timestamp

8. Write the updated YAML back to the state file

**Expected result**: The project is removed from the registry and no longer appears in listings.

---

## 1.4 Listing All Projects with Status Filtering

**When to use**: To get an overview of all tracked projects, or to filter by specific status.

**Available filters**:
- `--status active`: Show only active projects
- `--status paused`: Show only paused projects
- `--status archived`: Show only archived projects

**Output formats**:
- `--format table`: Human-readable table (default)
- `--format json`: JSON array for programmatic processing

**Procedure**:

1. Read the current state file at `.claude/chief-of-staff-state.local.md`

2. Parse the YAML structure

3. Extract all entries from the `projects` array

4. If `--status` filter is provided:
   - Filter the projects array to only include entries where `status` matches the filter value

5. For each project, extract:
   - `id` - Project ID
   - `name` - Project name
   - `repo_url` - Repository URL
   - `github_project_board` - Board URL (may be null)
   - `active_agents` - Count the number of agents in the array
   - `status` - Current status
   - `last_sync` - Last sync timestamp

6. Format the output:
   - **Table format**: Create a table with columns: `Project ID`, `Name`, `Repository`, `Agents`, `Last Sync`
   - **JSON format**: Return an array of project objects

**Expected result**: A list of projects matching the filter criteria in the requested format.

---

## 1.5 Syncing Project Registry with GitHub Projects Boards

**When to use**: To update the local registry with the current state of GitHub Projects boards, or to push local changes to GitHub.

**Prerequisites**:
- `gh` CLI must be installed and authenticated
- The project must have a `github_project_board` URL configured

**Sync operations**:

### 1.5.1 Fetching Board Status from GitHub

**Procedure**:

1. Extract the project number and owner from the board URL
   - Example URL: `https://github.com/orgs/Emasoft/projects/1`
   - Owner: `Emasoft`
   - Project number: `1`

2. Use `gh` CLI to fetch project information:

```bash
gh project view <project-number> --owner <owner> --format json
```

3. Parse the JSON response to extract:
   - Project title
   - Project description
   - Number of items
   - Last updated timestamp

4. Use `gh` CLI to list all items in the project:

```bash
gh project item-list <project-number> --owner <owner> --format json
```

5. Parse the JSON response to extract all items with their:
   - Title
   - Status column
   - Assignees
   - Labels

6. Update the project entry in the state file:
   - Set `last_sync` to current timestamp
   - Optionally store a summary of item counts by status

**Expected result**: The local registry reflects the current state of the GitHub Projects board.

### 1.5.2 Bulk Sync Across All Projects

**When to use**: To update all projects in the registry at once.

**Procedure**:

1. Read the state file

2. Filter projects to only those with a non-null `github_project_board`

3. For each project, execute the fetch procedure in section 1.5.1

4. Track any errors or inaccessible boards

5. Update the `last_updated` timestamp in the state file

6. Write all changes back to the state file

7. Generate a summary report:
   - Number of projects synced successfully
   - Number of projects that failed
   - List of failed projects with error messages

**Expected result**: All accessible GitHub Projects boards are synced with the local registry.

---

## 1.6 Managing Cross-Project Dependencies

**When to use**: When one project requires deliverables from another, or when projects share common resources.

**Dependency types**:
- `requires`: Project A cannot proceed until Project B delivers something (blocking)
- `shares`: Projects use shared resources but are not blocked (non-blocking)
- `extends`: Project A extends functionality from Project B (non-blocking)
- `conflicts`: Projects have conflicting requirements that need coordination (blocking)

**Procedure**:

### 1.6.1 Adding a New Dependency

1. Read the current state file

2. Validate both project IDs exist in the registry

3. Check if a dependency already exists between these projects:
   - Search `dependencies` array for entries where `from_project` and `to_project` match

4. If no existing dependency, add a new entry to the `dependencies` array:

```yaml
dependencies:
  - from_project: "<from-project-id>"
    to_project: "<to-project-id>"
    type: "<requires|shares|extends|conflicts>"
    description: "<human-readable description of the dependency>"
    blocking: <true|false>
    created: "<timestamp>"
```

5. If the dependency is blocking, check if it creates a circular dependency:
   - Build a dependency graph
   - Use depth-first search to detect cycles
   - If cycle detected, abort and warn the user

6. Update the `last_updated` timestamp

7. Write the updated YAML back to the state file

**Expected result**: The dependency is recorded and can be queried when coordinating work across projects.

### 1.6.2 Querying Dependencies for a Project

**When to use**: Before starting work on a project, to identify which other projects must be completed first.

**Procedure**:

1. Read the current state file

2. Filter the `dependencies` array to find all entries where:
   - `from_project` matches the target project ID (what this project depends on)
   - `to_project` matches the target project ID (what depends on this project)

3. For dependencies where the target is `from_project` (upstream dependencies):
   - Check if the `to_project` is in a completed state
   - If blocking and not completed, flag as a blocker

4. For dependencies where the target is `to_project` (downstream dependencies):
   - List which projects are waiting on this project
   - If blocking, prioritize completion to unblock others

**Expected result**: A clear list of upstream blockers and downstream dependents.

---

## 1.7 Assigning Agents to Projects

**When to use**: To track which agents are actively working on which projects, enabling coordination and conflict resolution.

**Agent assignment rules**:
1. **One Primary Agent**: Each project should have one primary coordinating agent (typically `ecos-main` or `eoa-task-coordinator`)
2. **Specialist Agents**: Additional agents can be assigned for specific tasks (e.g., `eia-code-reviewer`, `eoa-debug-specialist`)
3. **Cross-Project Agents**: Some agents may work across multiple projects simultaneously
4. **Conflict Resolution**: When an agent is assigned to multiple projects, coordinate timing to avoid context switching

**Procedure**:

### 1.7.1 Assigning an Agent to a Project

1. Read the current state file

2. Validate the project ID exists in the registry

3. Locate the project entry in the `projects` array

4. Check if the agent is already assigned:
   - Search the `active_agents` array for the agent name
   - If already assigned, return a message "Agent already assigned to project"

5. Add the agent name to the `active_agents` array:

```yaml
projects:
  - id: "skill-factory"
    active_agents:
      - "ecos-main"
      - "eoa-task-coordinator"
      - "<new-agent-name>"
```

6. Update the `agent_assignments` section to track reverse mapping (optional but recommended):

```yaml
agent_assignments:
  "<agent-name>":
    - project: "skill-factory"
      role: "specialist"
      assigned_at: "<timestamp>"
```

7. Update the `last_updated` timestamp

8. Write the updated YAML back to the state file

**Expected result**: The agent is now tracked as working on the project.

### 1.7.2 Unassigning an Agent from a Project

1. Read the current state file

2. Validate the project ID exists in the registry

3. Locate the project entry in the `projects` array

4. Check if the agent is currently assigned:
   - Search the `active_agents` array for the agent name
   - If not found, return a message "Agent not assigned to project"

5. Remove the agent name from the `active_agents` array

6. Update the `agent_assignments` section to remove the project entry

7. Update the `last_updated` timestamp

8. Write the updated YAML back to the state file

**Expected result**: The agent is no longer tracked on the project.

---

## 1.8 Updating Registry State Files Safely

**When to use**: Every time you need to modify the state file, to prevent corruption and conflicts.

**Critical safety protocol**:

1. **Read current state**: Always read the entire state file before making changes
   - Use a file locking mechanism if available (e.g., `flock` on Linux/macOS)
   - If file lock is not available, use a timestamp-based conflict detection

2. **Validate YAML structure**: Parse the YAML to ensure it is valid
   - Catch and handle YAML parsing errors
   - If invalid, create a backup of the corrupted file and regenerate from template

3. **Apply changes**: Make the necessary modifications to the in-memory data structure
   - Never directly edit the file with text operations
   - Always work with the parsed YAML structure

4. **Update timestamp**: Set the `last_updated` field to the current ISO 8601 timestamp
   - Format: `YYYY-MM-DDTHH:MM:SSZ`
   - Always use UTC timezone

5. **Write back to file**: Serialize the updated YAML and write to the state file
   - Use atomic write operations if available (write to temp file, then rename)
   - Ensure proper newline handling and YAML formatting

6. **Release lock**: If using file locking, release the lock

7. **Verify write**: Read the file back and validate the changes were applied correctly

8. **Commit if significant**: If this is a major change (new project, removed project, significant dependency change), commit to git:
   - Add the state file: `git add .claude/chief-of-staff-state.local.md`
   - Commit with descriptive message: `git commit -m "chore: update chief of staff state - <description>"`

**Expected result**: State file is updated safely without corruption or data loss.

---

## 1.9 Resolving Agent Conflicts Across Multiple Projects

**When to use**: When an agent is assigned to multiple projects and needs to coordinate work without context thrashing.

**Conflict scenarios**:
1. **Time conflict**: Agent needs to work on two projects simultaneously
2. **Resource conflict**: Agent needs exclusive access to a shared resource
3. **Priority conflict**: Multiple projects have urgent tasks for the same agent
4. **Context conflict**: Switching between projects causes loss of context or state

**Resolution strategies**:

### 1.9.1 Detecting Agent Conflicts

**Procedure**:

1. Read the current state file

2. Build a reverse mapping of agents to projects:
   - Iterate through all projects
   - For each project, extract all agents in `active_agents`
   - Create a dictionary mapping agent name to list of projects

3. Identify agents assigned to multiple projects:
   - Filter the mapping to only agents with 2+ projects

4. For each multi-assigned agent:
   - List all projects they are assigned to
   - Check the status of each project (active, paused, archived)
   - Count how many are in `active` status

5. Flag conflicts:
   - If an agent has 3+ active projects, flag as high conflict risk
   - If an agent has 2 active projects, flag as medium conflict risk

**Expected result**: A list of agents with potential scheduling conflicts.

### 1.9.2 Coordinating Work Timing

**Strategy**: Time-slice agent work across projects to minimize context switching.

**Procedure**:

1. For each agent with multiple active assignments:
   - Identify the primary project (usually the first in the list, or marked explicitly)
   - Mark secondary projects

2. Create a work schedule:
   - Primary project: 60-80% of agent's time
   - Secondary projects: 20-40% of agent's time, batched into specific time blocks

3. Communicate the schedule to the agent via AI Maestro:

Use the `agent-messaging` skill to send:
- **Recipient**: the target agent session name
- **Subject**: `Multi-Project Schedule`
- **Priority**: `normal`
- **Content**: type `schedule`, message: "Primary focus: [project-a] (60%). Secondary: [project-b] (40%, batched work on Mondays/Wednesdays)."

**Expected result**: Agent has clear guidance on how to allocate time across projects.

### 1.9.3 Resource Allocation

**When to use**: When projects compete for exclusive access to a resource (e.g., deployment slot, test environment).

**Procedure**:

1. Identify the shared resource in the state file (add a `shared_resources` section if needed):

```yaml
shared_resources:
  - id: "staging-server"
    type: "deployment-target"
    currently_held_by: "project-a"
    queue:
      - project: "project-b"
        requested_at: "<timestamp>"
```

2. When a project needs the resource:
   - Check if `currently_held_by` is null
   - If null, assign to the requesting project
   - If not null, add the requesting project to the queue

3. When a project releases the resource:
   - Set `currently_held_by` to null
   - Check the queue
   - Assign to the first project in the queue
   - Notify the project agent via AI Maestro

**Expected result**: Orderly resource allocation without conflicts.

---

## 1.10 Mapping GitHub Project Board Statuses to Internal States

**When to use**: When syncing with GitHub Projects boards or interpreting kanban column names.

**Standard mapping table**:

| GitHub Column Name | Internal Status | Description |
|--------------------|-----------------|-------------|
| Backlog | `backlog` | Items not yet prioritized for work |
| Todo | `todo` | Items prioritized and ready to start |
| In Progress | `in_progress` | Items currently being worked on |
| In Review | `in_review` | Items completed and awaiting review |
| Done | `done` | Items fully completed and closed |

**Custom column handling**:

If a GitHub Projects board uses custom column names, create a mapping configuration:

```yaml
github_status_mappings:
  project-id: "skill-factory"
  mappings:
    "Planned": "todo"
    "Active": "in_progress"
    "Code Review": "in_review"
    "Deployed": "done"
```

**Procedure for mapping unknown columns**:

1. Fetch the column name from the GitHub Projects board

2. Check if a mapping exists in the state file under `github_status_mappings`

3. If no mapping exists:
   - Attempt fuzzy matching with standard names (e.g., "To Do" → `todo`)
   - If match confidence is low, default to `unknown`
   - Log a warning and prompt the user to define a mapping

4. Apply the mapped status when syncing items to the local registry

**Expected result**: Consistent internal status values regardless of GitHub board column naming.
