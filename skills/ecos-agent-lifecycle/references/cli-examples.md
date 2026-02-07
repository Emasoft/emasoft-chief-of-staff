# Agent Lifecycle Examples

## Table of Contents
- [1.1 Creating a Code Implementer Agent](#11-creating-a-code-implementer-agent)
- [1.2 Terminating a Completed Agent](#12-terminating-a-completed-agent)
- [1.3 Hibernating an Idle Agent](#13-hibernating-an-idle-agent)
- [1.4 End of Day - Hibernate All Non-Critical Agents](#14-end-of-day---hibernate-all-non-critical-agents)
- [1.5 Resume Work Next Day](#15-resume-work-next-day)

## Use-Case TOC
- When creating a new implementer agent -> [1.1 Creating](#11-creating-a-code-implementer-agent)
- When an agent's work is complete -> [1.2 Terminating](#12-terminating-a-completed-agent)
- When conserving resources for a single agent -> [1.3 Hibernating](#13-hibernating-an-idle-agent)
- When ending work session -> [1.4 End of Day](#14-end-of-day---hibernate-all-non-critical-agents)
- When starting a new work session -> [1.5 Resume Work](#15-resume-work-next-day)

---

## 1.1 Creating a Code Implementer Agent

Use the `ai-maestro-agents-management` skill to create a new agent:

- **Name**: `code-impl-auth`
- **Directory**: `{baseDir}/myproject/auth`
- **Task**: `Implement user authentication module`
- **Tags**: `implementer,python,auth`
- **Program args**: include `continue`, `--dangerously-skip-permissions`, `--chrome`, `--add-dir /tmp`

**Expected result:**
- Directory created at the specified path
- Git repository initialized
- Agent registered in AI Maestro
- tmux session created with the agent name
- Agent is now ONLINE

**Verify**: the new agent appears in the agent list with "online" status.

**Required Claude Code Arguments:**

| Argument | Purpose |
|----------|---------|
| `continue` | Resume previous session context |
| `--dangerously-skip-permissions` | Skip permission dialogs |
| `--chrome` | Enable Chrome DevTools integration |
| `--add-dir /tmp` | Add temp directory (use `%TEMP%` on Windows) |

---

## 1.2 Terminating a Completed Agent

Use the `ai-maestro-agents-management` skill to terminate agent `code-impl-auth` with confirmation.

**Expected result:**
- Agent validated
- tmux session killed
- Agent removed from registry
- Agent is now DELETED

**Important Notes:**
- Confirmation is REQUIRED for safety
- Consider hibernating instead if you may need the agent later
- Ensure all work is complete before termination

---

## 1.3 Hibernating an Idle Agent

**To hibernate:** Use the `ai-maestro-agents-management` skill to hibernate agent `test-engineer-01`.

**Expected result:**
- Agent state saved
- tmux session terminated
- Registry updated: status = hibernated
- Agent is now HIBERNATED

**To wake:** Use the `ai-maestro-agents-management` skill to wake agent `test-engineer-01`.

**Expected result:**
- Agent state retrieved
- tmux session created
- Claude Code launched
- Agent is now ONLINE

---

## 1.4 End of Day - Hibernate All Non-Critical Agents

**Workflow:**

1. Use the `ai-maestro-agents-management` skill to list all online agents
2. Hibernate non-critical agents (e.g., `frontend-ui`, `data-processor`, `docs-writer`) using the skill
3. Keep critical agents running (e.g., `backend-api` stays online)
4. Use the skill to list all agents and verify the final state

**Key Points:**
- List agents before bulk operations
- Hibernate in priority order (least critical first)
- Verify final state after operations

---

## 1.5 Resume Work Next Day

**Workflow:**

1. Use the `ai-maestro-agents-management` skill to wake needed agents (e.g., `frontend-ui`, `data-processor`)
2. For agents you want to interact with immediately, wake with the attach option (e.g., `docs-writer`)

**Key Points:**
- Wake agents in priority order (most needed first)
- Use the attach option to immediately connect to an agent's tmux session
- Verify agent status after waking

---

## Operations Quick Reference

All operations are performed using the `ai-maestro-agents-management` skill:

| Operation | Description |
|-----------|-------------|
| List agents | List all agents, optionally filtered by status |
| Show agent | Display detailed information about a specific agent |
| Create agent | Create a new agent with name, directory, and configuration |
| Terminate agent | Permanently remove an agent (requires confirmation) |
| Hibernate agent | Save state and suspend an agent |
| Wake agent | Restore state and resume a hibernated agent |
| Restart agent | Hibernate + wake cycle (for plugin changes) |
| Update agent | Modify task description or tags |

---

**Version:** 1.0
**Last Updated:** 2025-02-03
