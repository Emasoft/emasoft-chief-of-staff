---
name: ecos-reindex-skills
description: "Trigger Perfect Skill Suggester reindex for an agent's skills"
argument-hint: "<SESSION_NAME> [--force] [--wait]"
user-invocable: true
allowed-tools: ["Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/ecos_reindex_skills.py:*)"]
---

# Reindex Skills Command

Trigger a Perfect Skill Suggester (PSS) reindex for a specific agent. This regenerates the skill index for improved skill matching.

## Usage

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ecos_reindex_skills.py" $ARGUMENTS
```

## What This Command Does

1. **Resolves Target Agent**
   - Resolves SESSION_NAME to agent identifier via AI Maestro API
   - Verifies agent has PSS plugin installed
   - Retrieves agent's project directory

2. **Sends Reindex Command via AI Maestro**
   - Sends `/pss-reindex-skills` command to target agent
   - Uses high-priority message for immediate processing
   - Includes reindex parameters if specified

3. **Monitors Reindex Progress** (with `--wait`)
   - Polls agent for reindex completion
   - Reports progress percentage
   - Times out after configurable period

4. **Reports Reindex Results**
   - Shows number of skills indexed
   - Lists any skills that failed indexing
   - Reports index generation time

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `SESSION_NAME` | Yes | Target agent session name (e.g., `orchestrator-master`) |
| `--force` | No | Force full reindex even if cache is fresh |
| `--wait` | No | Wait for reindex completion and report results |
| `--timeout SECONDS` | No | Maximum wait time (default: 300) |
| `--verbose` | No | Show detailed reindex progress |

## Examples

### Trigger reindex for an agent

```bash
/ecos-reindex-skills orchestrator-master
```

### Force full reindex and wait for completion

```bash
/ecos-reindex-skills orchestrator-master --force --wait
```

### Trigger with custom timeout

```bash
/ecos-reindex-skills libs-svg-svgbbox --wait --timeout 600
```

## Output Example

### Without --wait

```
╔════════════════════════════════════════════════════════════════╗
║                    REINDEX REQUEST SENT                        ║
╠════════════════════════════════════════════════════════════════╣
║ Agent: orchestrator-master                                     ║
║ Message ID: msg-20260201-110532                                ║
║ Command: /pss-reindex-skills --force                           ║
║ Priority: high                                                 ║
╠════════════════════════════════════════════════════════════════╣
║ STATUS: Request sent via AI Maestro                            ║
║ NOTE: Use --wait to monitor completion                         ║
╚════════════════════════════════════════════════════════════════╝
```

### With --wait

```
╔════════════════════════════════════════════════════════════════╗
║                    SKILL REINDEX COMPLETE                      ║
╠════════════════════════════════════════════════════════════════╣
║ Agent: orchestrator-master                                     ║
║ Duration: 45.2 seconds                                         ║
╠════════════════════════════════════════════════════════════════╣
║ REINDEX RESULTS                                                ║
╠════════════════════════════════════════════════════════════════╣
║ Skills Indexed: 47                                             ║
║ Skills Failed: 0                                               ║
║ Index Size: 128 KB                                             ║
║ Keywords Generated: 342                                        ║
║ Co-usage Relationships: 156                                    ║
╠════════════════════════════════════════════════════════════════╣
║ INDEX LOCATION                                                 ║
║ ~/.claude/cache/pss/skills-index.json                          ║
╚════════════════════════════════════════════════════════════════╝
```

## PSS Reindex Process

The Perfect Skill Suggester uses a two-pass indexing process:

### Pass 1: Factual Data Extraction
- Skill name and description
- Categories (16 predefined fields of competence)
- Keywords from skill content
- Script and reference inventory

### Pass 2: AI Co-usage Analysis
- Skill relationship mapping
- Usage pattern detection
- Weighted scoring calibration

## Error Conditions

| Error | Cause | Solution |
|-------|-------|----------|
| "Agent not found" | SESSION_NAME not registered | Check agent name |
| "PSS not installed" | Agent doesn't have PSS plugin | Install PSS plugin first |
| "Agent not responding" | Agent session inactive | Restart agent session |
| "Reindex timeout" | Reindex took too long | Increase timeout or check agent load |
| "AI Maestro unavailable" | API not running | Start AI Maestro service |

## Prerequisites

- AI Maestro must be running (use `ai-maestro-agents-management` skill to verify)
- Target agent must be registered in AI Maestro
- Target agent must have Perfect Skill Suggester plugin installed
- Target agent session must be active

## Notes

- Reindex is **non-blocking** by default - it sends the command and returns
- Use `--wait` for synchronous operation (blocking until complete)
- The index is the **superset** of all skills; agent filters against its available skills
- Regenerating index clears any cached skill suggestions

## When to Reindex

Trigger a reindex when:
- New skills are added to plugins
- Skill content is significantly updated
- Plugin configuration changes
- Skill matching seems inaccurate

## Related Commands

- `/ecos-validate-skills` - Validate skills before reindexing
- `/ecos-configure-plugins` - Configure plugins (may require reindex)
- `/pss-reindex-skills` - Direct PSS reindex command (on target agent)
