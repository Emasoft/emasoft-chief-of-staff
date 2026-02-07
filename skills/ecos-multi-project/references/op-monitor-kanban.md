---
name: op-monitor-kanban
description: Operation procedure for proactively monitoring GitHub Project Kanban board for external changes.
workflow-instruction: "support"
procedure: "support-skill"
---

# Operation: Monitor Kanban Board

## Purpose

Proactively poll the GitHub Project Kanban board to detect external changes (by humans or other systems) and respond appropriately.

## When to Use

- During active work sessions (poll every 5 minutes)
- When multiple actors are updating the board
- When external stakeholders use GitHub directly
- For real-time coordination awareness

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- GitHub Project board configured for the repository
- AI Maestro available for agent notifications
- Project registered in registry with `github_project` field

## Procedure

### Step 1: Load Project Configuration

```bash
PROJECT_ID="skill-factory"
REGISTRY_FILE=".emasoft/project-registry.json"

GITHUB_OWNER=$(jq -r '.projects["'"$PROJECT_ID"'"].github_repo' $REGISTRY_FILE | cut -d'/' -f1)
PROJECT_NUMBER=$(gh project list --owner $GITHUB_OWNER --format json | jq -r '.projects[] | select(.title == "'"$(jq -r '.projects["'"$PROJECT_ID"'"].github_project' $REGISTRY_FILE)"'") | .number')
```

### Step 2: Fetch Recent Changes

```bash
# Get items updated in last 5 minutes (300 seconds)
CUTOFF=$(date -u -v-5M +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '5 minutes ago' +%Y-%m-%dT%H:%M:%SZ)

gh project item-list $PROJECT_NUMBER --owner $GITHUB_OWNER --limit 100 --format json > /tmp/current_state.json

# Compare with cached state (if exists)
if [ -f "/tmp/previous_state_$PROJECT_ID.json" ]; then
  # Find differences
  CHANGES=$(diff <(jq -S . /tmp/previous_state_$PROJECT_ID.json) <(jq -S . /tmp/current_state.json) || true)
else
  CHANGES=""
fi

# Cache current state for next comparison
cp /tmp/current_state.json /tmp/previous_state_$PROJECT_ID.json
```

### Step 3: Detect Change Types

```bash
# Parse for specific change types
while read ITEM; do
  ITEM_ID=$(echo $ITEM | jq -r '.id')
  TITLE=$(echo $ITEM | jq -r '.title')
  STATUS=$(echo $ITEM | jq -r '.status')
  ASSIGNEES=$(echo $ITEM | jq -r '.assignees')

  # Compare with previous state
  PREV_STATUS=$(jq -r '.items[] | select(.id == "'"$ITEM_ID"'") | .status' /tmp/previous_state_$PROJECT_ID.json 2>/dev/null)

  if [ "$STATUS" != "$PREV_STATUS" ] && [ -n "$PREV_STATUS" ]; then
    echo "STATUS CHANGE: $TITLE moved from $PREV_STATUS to $STATUS"
    # Handle status change
  fi
done <<< "$(jq -c '.items[]' /tmp/current_state.json)"
```

### Step 4: Respond to External Changes

#### Card Moved to Different Column

Use the `agent-messaging` skill to send:
- **Recipient**: the assigned agent session name
- **Subject**: `[EXTERNAL CHANGE] Card moved`
- **Priority**: `high`
- **Content**: type `external-change-notification`, message: "Card [title] was moved from [old_status] to [new_status] by external user." Include `change_type`: "card_moved", `task_id`, `old_status`, `new_status`.

#### New Card Added

Use the `agent-messaging` skill to send:
- **Recipient**: `eoa-main`
- **Subject**: `[NEW CARD] External addition`
- **Priority**: `normal`
- **Content**: type `new-task-notification`, message: "New card added to Kanban: [title]. Please review and assign." Include `task_title` and `task_id`.

### Step 5: Update Local Registry

```bash
# Sync local state with detected changes
jq '.projects["'"$PROJECT_ID"'"].last_kanban_poll = "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"' $REGISTRY_FILE > temp.json && mv temp.json $REGISTRY_FILE
```

### Step 6: Log Monitoring Results

```bash
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Kanban poll for $PROJECT_ID: $CHANGE_COUNT changes detected" >> docs_dev/kanban-monitor.log
```

## Change Types to Monitor

| Change Type | Detection | Response |
|-------------|-----------|----------|
| Card moved | Status field changed | Notify assigned agent |
| New card added | Item not in previous state | Alert EOA for assignment |
| Card removed/closed | Item missing from current state | Update local tracking |
| Assignee changed | Assignees field changed | Notify old and new assignees |
| Priority changed | Priority field changed | Notify assigned agent |
| New comment | Comment count increased | Forward to assigned agent |

## Example

**Scenario:** Detect that a card was moved from "In Progress" to "Review" by external user.

**Detected change:** Card "Implement user login" moved from "In Progress" to "Review" by external user.

1. Log the change with timestamp
2. Use the `agent-messaging` skill to send:
   - **Recipient**: `implementer-1`
   - **Subject**: `[EXTERNAL CHANGE] Your card moved to Review`
   - **Priority**: `high`
   - **Content**: type `external-change-notification`, message: "Card 'Implement user login' was moved from In Progress to Review by external user. Please ensure work is ready for review." Include `change_type`: "card_moved", `old_status`: "In Progress", `new_status`: "Review".

## Polling Schedule

| Session State | Poll Interval | Reason |
|---------------|---------------|--------|
| Active work | 5 minutes | Real-time awareness |
| Idle/monitoring | 15 minutes | Reduced API usage |
| Background | 30 minutes | Minimal overhead |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Rate limit | Too frequent polling | Increase interval |
| Project not found | Number changed | Re-query project list |
| Auth error | Token expired | Re-authenticate |
| State file missing | First poll | Initialize empty state |

## Notes

- Balance polling frequency with API limits
- Only poll during active work sessions
- Cache state to minimize API calls
- Alert humans only for significant changes
