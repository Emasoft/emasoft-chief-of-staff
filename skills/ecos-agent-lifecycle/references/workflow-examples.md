# Agent Lifecycle Workflow Examples

## Table of Contents
- [1.1 Workflow 1: Setting Up a Development Team](#11-workflow-1-setting-up-a-development-team)
- [1.2 Workflow 2: Hibernating Idle Agents](#12-workflow-2-hibernating-idle-agents)
- [1.3 Workflow 3: Skill Reindex After Plugin Update](#13-workflow-3-skill-reindex-after-plugin-update)

## Use-Case TOC
- When setting up a new team for multi-service work -> [1.1 Workflow 1](#11-workflow-1-setting-up-a-development-team)
- When conserving resources by hibernating idle agents -> [1.2 Workflow 2](#12-workflow-2-hibernating-idle-agents)
- When plugins or skills have been updated -> [1.3 Workflow 3](#13-workflow-3-skill-reindex-after-plugin-update)

---

## 1.1 Workflow 1: Setting Up a Development Team

**Scenario:** User request: "I need to implement a new feature across 3 microservices. Set up a team."

**Step-by-Step Walkthrough:**

```
1. Route to ecos-staff-planner:
   - Input: "3 microservices, new feature implementation"
   - Output: "Recommend 3 developers + 1 reviewer, 4 agents total"

2. Check resources via ecos-resource-monitor:
   - Current: 1 active agent
   - Max: 5 agents
   - Available: 4 slots
   - Result: Approved

3. Route to ecos-lifecycle-manager:
   - Create 4 new agents with --agent flag:
     - svgbbox-impl-01 (--agent eoa-orchestrator-main-agent)
     - svgbbox-impl-02
     - svgbbox-impl-03
     - svgbbox-reviewer-01

4. Update team registry (.emasoft/team-registry.json)

5. Send role assignments via AI Maestro:
   - svgbbox-impl-01: "Implement auth-service feature"
   - svgbbox-impl-02: "Implement user-service feature"
   - svgbbox-impl-03: "Implement api-gateway feature"
   - svgbbox-reviewer-01: "Review PRs from dev agents"

6. Report team composition to EAMA
```

**Key Points:**
- Always check resource availability before spawning multiple agents
- Use --agent flag to inject main agent prompts
- Update team registry after all spawns
- Send role assignments via AI Maestro after agents are running

---

## 1.2 Workflow 2: Hibernating Idle Agents

**Scenario:** Resource monitor detects 3 agents idle for 30+ minutes.

**Step-by-Step Walkthrough:**

```
1. ecos-resource-monitor reports: ["svgbbox-impl-02", "svgbbox-impl-03", "svgbbox-reviewer-01"] idle

2. Send hibernation warnings via AI Maestro:
   - "You will be hibernated in 5 minutes unless active"

3. Wait 5 minutes, re-check activity

4. Route to ecos-lifecycle-manager:
   - Hibernate still-idle agents
   - Update tmux session states

5. Update team registry with hibernated status

6. Report hibernation to EAMA
```

**Key Points:**
- Always send warning before hibernation (grace period)
- Re-check activity after warning period
- Only hibernate agents that remain idle
- Update registry with hibernated status and timestamp

---

## 1.3 Workflow 3: Skill Reindex After Plugin Update

**Scenario:** User updated skills in emasoft-orchestrator-agent plugin.

**Step-by-Step Walkthrough:**

```
1. Route to ecos-skill-validator:
   - Validate all skills in ./OUTPUT_SKILLS/emasoft-orchestrator-agent/skills/

2. If validation passes, trigger PSS reindex:
   - Execute: /pss-reindex-skills (if PSS plugin available)
   - Or: Run pss_build_skill_index.py directly

3. Notify all active agents of skill update:
   - Send AI Maestro broadcast: "Skills updated. Reload if needed."

4. Report completion to EAMA
```

**Key Points:**
- Always validate skills before reindexing
- Only trigger PSS reindex if validation passes
- Notify all active agents of updates
- Report completion to EAMA for tracking

---

**Version:** 1.0
**Last Updated:** 2025-02-03
