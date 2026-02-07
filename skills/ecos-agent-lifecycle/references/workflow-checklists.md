# Agent Lifecycle Workflow Checklists

## Contents

### When You Need to Create a New Agent
- [1.1 Spawning New Agent Checklist](#checklist-spawning-new-agent) - Complete checklist for spawning a new agent from approval to post-spawn tasks

### When You Need to Stop an Agent
- [2.1 Terminating Agent Checklist](#checklist-terminating-agent) - Complete checklist for safely terminating an agent

### When You Need to Put an Inactive Agent to Sleep
- [3.1 Hibernating Agent Checklist](#checklist-hibernating-agent) - Checklist for hibernating an idle agent to save resources

### When You Need to Resume a Hibernated Agent
- [4.1 Waking Agent Checklist](#checklist-waking-agent) - Checklist for waking a hibernated agent and restoring its state

### When You Need to Create a New Project Team
- [5.1 Forming Team Checklist](#checklist-forming-team) - Complete checklist for creating a new team and assigning agents

### When You Need to Modify Team Membership or Agent Status
- [6.1 Updating Team Registry Checklist](#checklist-updating-team-registry) - Checklist for adding/removing agents or updating their status

---

## Checklist: Spawning New Agent

**Before submitting approval request:**
- [ ] Verify agent name not already in use: Use the `ai-maestro-agents-management` skill to list all agents and check the name is not taken
- [ ] Select appropriate role from available main-agents (e.g., `eoa-orchestrator-main-agent`, `eia-integrator-main-agent`)
- [ ] Identify required plugins/skills for role
- [ ] Determine working directory (project-specific or shared)
- [ ] Prepare rollback plan (terminate agent, clean up directory)

**Submit approval request:**
- [ ] Request approval from EAMA via ecos-approval-coordinator sub-agent
- [ ] Wait for approval decision (timeout: 120s)
- [ ] If rejected, notify requester and STOP
- [ ] If approved, continue

**Execute spawn operation:**
- [ ] Use the `ai-maestro-agents-management` skill to create the agent with the specified name, working directory, task description, and main agent configuration
- [ ] Verify tmux session created
- [ ] Verify agent registered in AI Maestro
- [ ] Send health check message to new agent
- [ ] Wait for response (30s timeout)
- [ ] If no response, initiate rollback

**Post-spawn tasks:**
- [ ] Update team registry (if assigning to team)
- [ ] Notify EOA of new agent availability (if project has EOA)
- [ ] Log spawn in lifecycle log: `docs_dev/chief-of-staff/agent-lifecycle.log`
- [ ] Update cross-project tracking (if applicable)
- [ ] Notify requester of success

---

## Checklist: Terminating Agent

**Before submitting approval request:**
- [ ] Verify agent exists and status: Use the `ai-maestro-agents-management` skill to list agents and check the target agent's current status
- [ ] Check for in-progress tasks: Send message to agent asking for current task status
- [ ] Wait for agent response (30s timeout)
- [ ] If agent has critical work in progress, coordinate handoff first
- [ ] Prepare rollback plan (re-spawn agent with same configuration)

**Submit approval request:**
- [ ] Request approval from EAMA via ecos-approval-coordinator
- [ ] Wait for approval decision (timeout: 120s)
- [ ] If rejected, notify requester and STOP
- [ ] If approved, continue

**Notify agent of termination:**
- [ ] Send notification to agent: "You will be terminated in 30 seconds. Save state and prepare for shutdown."
- [ ] Wait 30 seconds for agent to save state

**Execute termination:**
- [ ] Use the `ai-maestro-agents-management` skill to terminate the agent by name
- [ ] Verify tmux session removed
- [ ] Verify agent deregistered from AI Maestro
- [ ] Check for orphaned processes: `ps aux | grep <name>`
- [ ] Clean up working directory (if temporary)

**Post-termination tasks:**
- [ ] Remove agent from all team registries
- [ ] Log termination in lifecycle log
- [ ] Notify EOA of agent removal (if project has EOA)
- [ ] Update cross-project tracking
- [ ] Notify requester of success

---

## Checklist: Hibernating Agent

**Pre-hibernation checks:**
- [ ] Verify agent exists and is active
- [ ] Check agent idle time: Review AI Maestro message history
- [ ] Ensure agent has no critical tasks in progress
- [ ] Create hibernation directory: `mkdir -p $CLAUDE_PROJECT_DIR/.emasoft/hibernated-agents/<agent-name>/`

**Notify agent:**
- [ ] Send message to agent: "You will be hibernated due to inactivity. Save state."
- [ ] Wait 30 seconds for agent to prepare

**Execute hibernation:**
- [ ] Save agent context to disk
- [ ] Update agent status in AI Maestro to `hibernated`
- [ ] Update team registry status to `hibernated`
- [ ] Configure agent to ignore messages (sleep mode)

**Post-hibernation:**
- [ ] Log hibernation in lifecycle log
- [ ] Notify EOA of agent status change (if applicable)
- [ ] Set wake condition (time-based or event-based)

---

## Checklist: Waking Agent

**Pre-wake checks:**
- [ ] Verify agent exists and is hibernated
- [ ] Check hibernation snapshot exists: `test -f $CLAUDE_PROJECT_DIR/.emasoft/hibernated-agents/<agent-name>/context.json`
- [ ] Ensure working directory still accessible

**Execute wake:**
- [ ] Restore agent context from snapshot
- [ ] Update agent status in AI Maestro to `active`
- [ ] Update team registry status to `active`
- [ ] Re-enable message processing

**Verify wake:**
- [ ] Send health check message
- [ ] Wait for response (30s timeout)
- [ ] Verify agent resumes from last known state

**Post-wake:**
- [ ] Log wake in lifecycle log
- [ ] Notify EOA of agent availability (if applicable)
- [ ] Remove hibernation snapshot (cleanup)

---

## Checklist: Forming Team

**Preparation:**
- [ ] Verify project directory exists
- [ ] Verify project has `.emasoft/` directory (create if missing)
- [ ] Identify team lead (typically EOA - Emasoft Orchestrator Agent)
- [ ] Identify team members and their roles

**Create team registry:**
- [ ] Run `uv run python scripts/ecos_team_registry.py create <project-dir> --team-lead <agent-name>`
- [ ] Verify `.emasoft/team-registry.json` created

**Assign agents to team:**
- [ ] For each agent: `uv run python scripts/ecos_team_registry.py add-agent <project-dir> <agent-name> --role <role>`
- [ ] Verify each agent added to registry

**Notify team members:**
- [ ] Send message to each agent: "You have been assigned to <team-name> with role <role>. Team registry: <path>"
- [ ] Wait for acknowledgment from each agent

**Notify team lead (EOA):**
- [ ] Send message to EOA: "Team formed. Members: <list>. Registry: <path>"

**Finalize:**
- [ ] Log team formation in lifecycle log
- [ ] Update cross-project tracking
- [ ] Publish team registry (if shared team)

---

## Checklist: Updating Team Registry

**Before update:**
- [ ] Verify team registry exists
- [ ] Verify agent exists (if adding agent)
- [ ] Backup current registry: `cp .emasoft/team-registry.json .emasoft/team-registry.json.bak`

**Execute update:**
- [ ] Run appropriate command:
  - Add agent: `uv run python scripts/ecos_team_registry.py add-agent <project-dir> <agent-name> --role <role>`
  - Remove agent: `uv run python scripts/ecos_team_registry.py remove-agent <project-dir> <agent-name>`
  - Update status: `uv run python scripts/ecos_team_registry.py update-status <project-dir> <agent-name> <status>`
- [ ] Verify registry updated correctly: `uv run python scripts/ecos_team_registry.py list <project-dir>`

**Notify affected agents:**
- [ ] Notify agent of registry change
- [ ] Notify EOA of registry change

**Finalize:**
- [ ] Log update in lifecycle log
- [ ] Remove backup if successful
