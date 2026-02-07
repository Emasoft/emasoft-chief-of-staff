---
operation: update-team-registry
procedure: proc-create-team
workflow-instruction: Step 4 - Team Creation
parent-skill: ecos-agent-lifecycle
parent-plugin: emasoft-chief-of-staff
version: 1.0.0
---

# Update Team Registry

## When to Use

- After spawning a new agent
- After terminating an agent
- After hibernating or waking an agent
- When agent role or project assignment changes
- When publishing registry updates to teammates
- During team audit or reconciliation

## Prerequisites

- Team registry file exists at `.emasoft/team-registry.json`
- `ecos_team_registry.py` script is available
- Write permissions to registry file
- AI Maestro is running (for broadcasting updates)

## Procedure

### Step 1: Identify Update Type

Determine which registry operation is needed:

| Event | Command |
|-------|---------|
| New agent | `add-agent` |
| Agent removed | `remove-agent` |
| Status change | `update-status` |
| Role change | `update-role` |
| Log event | `log` |

### Step 2: Execute Registry Update

**Add new agent:**
```bash
uv run python scripts/ecos_team_registry.py add-agent \
  --name "<agent-session-name>" \
  --role "<role>" \
  --project "<project>" \
  --status "running"
```

**Remove agent:**
```bash
uv run python scripts/ecos_team_registry.py remove-agent \
  --name "<agent-session-name>"
```

**Update status:**
```bash
uv run python scripts/ecos_team_registry.py update-status \
  --name "<agent-session-name>" \
  --status "<running|hibernated|terminated>" \
  --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

**Log event:**
```bash
uv run python scripts/ecos_team_registry.py log \
  --event "<event-type>" \
  --agent "<agent-session-name>" \
  --reason "<reason>" \
  --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

### Step 3: Verify Update

```bash
# View updated registry
uv run python scripts/ecos_team_registry.py list

# Check specific agent
uv run python scripts/ecos_team_registry.py list --filter-name "<agent-session-name>"
```

### Step 4: Publish Update to Team (Optional)

If teammates need to know about the change:

```bash
uv run python scripts/ecos_team_registry.py publish \
  --broadcast-to "all" \
  --message "Team registry updated: <description of change>"
```

This sends a `registry-update` message to all registered agents.

### Step 5: Backup Registry (Recommended)

After significant changes:

```bash
cp .emasoft/team-registry.json .emasoft/team-registry.backup.$(date +%Y%m%d%H%M%S).json
```

## Checklist

Copy this checklist and track your progress:

- [ ] Identify the registry operation needed
- [ ] Prepare all required parameters
- [ ] Execute the registry command
- [ ] Verify update was applied correctly
- [ ] Publish update to team if needed
- [ ] Create backup after significant changes
- [ ] Log the registry operation

## Examples

### Example: Complete Agent Addition Flow

```bash
SESSION_NAME="dev-api-charlie"

# Add to registry
uv run python scripts/ecos_team_registry.py add-agent \
  --name "$SESSION_NAME" \
  --role "developer" \
  --project "backend-api" \
  --status "running"

# Verify
uv run python scripts/ecos_team_registry.py list --filter-name "$SESSION_NAME"
# Output: dev-api-charlie | running | developer | backend-api

# Log the addition
uv run python scripts/ecos_team_registry.py log \
  --event "spawn" \
  --agent "$SESSION_NAME" \
  --reason "New developer for API work" \
  --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Notify team
uv run python scripts/ecos_team_registry.py publish \
  --broadcast-to "all" \
  --message "New team member: $SESSION_NAME (developer on backend-api)"
```

### Example: Status Change After Hibernation

```bash
SESSION_NAME="dev-frontend-bob"

# Update status
uv run python scripts/ecos_team_registry.py update-status \
  --name "$SESSION_NAME" \
  --status "hibernated" \
  --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Log hibernation
uv run python scripts/ecos_team_registry.py log \
  --event "hibernation" \
  --agent "$SESSION_NAME" \
  --reason "Idle timeout exceeded (30 min)" \
  --timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Verify
uv run python scripts/ecos_team_registry.py list --filter-name "$SESSION_NAME"
# Output: dev-frontend-bob | hibernated | developer | webapp
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Registry file not found | First run or file deleted | Run `create` command to initialize registry |
| Agent already exists | Duplicate add-agent call | Use update-status instead or remove first |
| Agent not found | Wrong name or already removed | Check agent name with `list` command |
| Permission denied | File permissions issue | Check write permissions on .emasoft directory |
| JSON parse error | Corrupt registry file | Restore from backup or recreate |
| Broadcast failed | AI Maestro not running | Start AI Maestro or skip broadcast |

## Related Operations

- [op-spawn-agent.md](op-spawn-agent.md) - Spawn agent (calls add-agent)
- [op-terminate-agent.md](op-terminate-agent.md) - Terminate agent (calls remove-agent)
- [op-hibernate-agent.md](op-hibernate-agent.md) - Hibernate agent (calls update-status)
- [op-wake-agent.md](op-wake-agent.md) - Wake agent (calls update-status)
