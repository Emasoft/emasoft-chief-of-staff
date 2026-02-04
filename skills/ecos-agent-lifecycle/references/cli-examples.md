# Agent Lifecycle CLI Examples

## Table of Contents
- [1.1 Spawning a Code Implementer Agent](#11-spawning-a-code-implementer-agent)
- [1.2 Terminating a Completed Agent](#12-terminating-a-completed-agent)
- [1.3 Hibernating an Idle Agent](#13-hibernating-an-idle-agent)
- [1.4 End of Day - Hibernate All Non-Critical Agents](#14-end-of-day---hibernate-all-non-critical-agents)
- [1.5 Resume Work Next Day](#15-resume-work-next-day)

## Use-Case TOC
- When creating a new implementer agent -> [1.1 Spawning](#11-spawning-a-code-implementer-agent)
- When an agent's work is complete -> [1.2 Terminating](#12-terminating-a-completed-agent)
- When conserving resources for a single agent -> [1.3 Hibernating](#13-hibernating-an-idle-agent)
- When ending work session -> [1.4 End of Day](#14-end-of-day---hibernate-all-non-critical-agents)
- When starting a new work session -> [1.5 Resume Work](#15-resume-work-next-day)

---

## 1.1 Spawning a Code Implementer Agent

**Command:**
```bash
# Create agent using aimaestro-agent.sh CLI (macOS/Linux)
aimaestro-agent.sh create code-impl-auth \
  --dir {baseDir}/myproject/auth \
  --task "Implement user authentication module" \
  --tags "implementer,python,auth" \
  -- continue --dangerously-skip-permissions --chrome --add-dir /tmp
```

**Expected Output:**
```
 Directory created: {baseDir}/myproject/auth
 Git repository initialized
 Agent registered in AI Maestro
 tmux session created: code-impl-auth
Agent 'code-impl-auth' is now ONLINE
```

**Required Claude Code Arguments (pass after `--`):**
| Argument | Purpose |
|----------|---------|
| `continue` | Resume previous session context |
| `--dangerously-skip-permissions` | Skip permission dialogs |
| `--chrome` | Enable Chrome DevTools integration |
| `--add-dir /tmp` | Add temp directory (use `%TEMP%` on Windows) |

---

## 1.2 Terminating a Completed Agent

**Command:**
```bash
# Terminate agent using aimaestro-agent.sh CLI
aimaestro-agent.sh delete code-impl-auth --confirm
```

**Expected Output:**
```
 Agent validated: code-impl-auth
 tmux session killed
 Agent removed from registry
Agent 'code-impl-auth' has been DELETED
```

**Important Notes:**
- `--confirm` flag is REQUIRED for safety
- Consider hibernating instead if you may need the agent later
- Ensure all work is complete before termination

---

## 1.3 Hibernating an Idle Agent

**Hibernate Command:**
```bash
aimaestro-agent.sh hibernate test-engineer-01
```

**Hibernate Output:**
```
 Agent state saved
 tmux session terminated
 Registry updated: status = hibernated
Agent 'test-engineer-01' is now HIBERNATED
```

**Wake Command:**
```bash
aimaestro-agent.sh wake test-engineer-01
```

**Wake Output:**
```
 Agent state retrieved
 tmux session created: test-engineer-01
 Claude Code launched
Agent 'test-engineer-01' is now ONLINE
```

---

## 1.4 End of Day - Hibernate All Non-Critical Agents

**Workflow Commands:**
```bash
# Step 1: List all online agents
aimaestro-agent.sh list --status online

# Step 2: Hibernate non-critical agents
aimaestro-agent.sh hibernate frontend-ui
aimaestro-agent.sh hibernate data-processor
aimaestro-agent.sh hibernate docs-writer

# Step 3: Keep critical agent running
# (backend-api stays online)

# Step 4: Verify status
aimaestro-agent.sh list --status all
```

**Key Points:**
- List agents before bulk operations
- Hibernate in priority order (least critical first)
- Verify final state after operations

---

## 1.5 Resume Work Next Day

**Workflow Commands:**
```bash
# Wake needed agents
aimaestro-agent.sh wake frontend-ui
aimaestro-agent.sh wake data-processor

# Attach to a specific agent's session
aimaestro-agent.sh wake docs-writer --attach
```

**Key Points:**
- Wake agents in priority order (most needed first)
- Use `--attach` to immediately connect to an agent's tmux session
- Verify agent status after waking

---

## CLI Quick Reference

| Operation | Command |
|-----------|---------|
| List agents | `aimaestro-agent.sh list` |
| Show agent | `aimaestro-agent.sh show <name>` |
| Create agent | `aimaestro-agent.sh create <name> --dir <path>` |
| Delete agent | `aimaestro-agent.sh delete <name> --confirm` |
| Hibernate | `aimaestro-agent.sh hibernate <name>` |
| Wake | `aimaestro-agent.sh wake <name>` |
| Restart | `aimaestro-agent.sh restart <name>` |
| Update task | `aimaestro-agent.sh update <name> --task "..."` |
| Update tags | `aimaestro-agent.sh update <name> --tags "a,b,c"` |

---

**Version:** 1.0
**Last Updated:** 2025-02-03
