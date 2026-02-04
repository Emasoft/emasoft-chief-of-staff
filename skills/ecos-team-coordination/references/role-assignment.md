# Role Assignment Reference

## Table of Contents

- 1.1 [What Are Agent Roles](#11-what-are-agent-roles)
- 1.2 [Standard Role Definitions](#12-standard-role-definitions)
- 1.3 [Matching Agents To Roles](#13-matching-agents-to-roles)
- 1.4 [Role Assignment Procedure](#14-role-assignment-procedure)
- 1.5 [Confirming Role Acceptance](#15-confirming-role-acceptance)
- 1.6 [Managing Role Transitions](#16-managing-role-transitions)
- 1.7 [Role Assignment Examples](#17-role-assignment-examples)
- 1.8 [Troubleshooting](#18-troubleshooting)

---

## 1.1 What Are Agent Roles

An agent role is a defined set of responsibilities, capabilities, and expectations assigned to an agent within a coordinated team. Roles provide structure to multi-agent workflows by clarifying who does what, preventing duplication of effort, and enabling the Chief of Staff to route tasks appropriately.

**Role characteristics:**
- **Defined scope**: Clear boundaries on what the role handles
- **Required capabilities**: Skills and access the agent needs
- **Expected behaviors**: How the agent should act in various situations
- **Reporting structure**: Who the agent reports to and coordinates with

**Why roles matter:**
- Prevents task collision where multiple agents try the same work
- Enables efficient task routing based on capability
- Provides clear escalation paths when issues arise
- Supports workload balancing across the team

---

## 1.2 Standard Role Definitions

The following standard roles are commonly used in Chief of Staff coordinated teams:

### Developer Role
**Responsibilities:**
- Implement features and bug fixes
- Write unit tests for new code
- Refactor existing code
- Update documentation for code changes

**Required capabilities:**
- Code editing tools (Write, Edit)
- Test execution (Bash)
- Version control (git commands)

**Reporting to:** Code Reviewer, Orchestrator

### Code Reviewer Role
**Responsibilities:**
- Review pull requests for quality and standards
- Provide constructive feedback to developers
- Enforce coding conventions
- Approve or request changes on PRs

**Required capabilities:**
- File reading (Read, Grep, Glob)
- GitHub CLI (gh commands)
- Code analysis tools

**Reporting to:** Orchestrator, Chief of Staff

### Test Engineer Role
**Responsibilities:**
- Write integration and end-to-end tests
- Execute test suites and report results
- Identify and document test gaps
- Maintain test infrastructure

**Required capabilities:**
- Test framework execution
- Test result parsing
- Coverage analysis

**Reporting to:** Orchestrator

### DevOps Role
**Responsibilities:**
- Manage CI/CD pipelines
- Handle deployments and releases
- Monitor system health
- Manage infrastructure as code

**Required capabilities:**
- Docker and container tools
- Cloud provider CLIs
- Monitoring dashboards

**Reporting to:** Chief of Staff

### Documentation Writer Role
**Responsibilities:**
- Write and update project documentation
- Create user guides and tutorials
- Maintain API documentation
- Generate change logs

**Required capabilities:**
- Markdown editing
- Documentation generators
- Diagram creation

**Reporting to:** Orchestrator

---

## 1.3 Matching Agents To Roles

When assigning an agent to a role, evaluate the following criteria:

### Capability Assessment

Check if the agent has access to required tools:

```bash
# Example: Check if agent can access git
curl -s "http://localhost:23000/api/sessions/helper-agent-generic/capabilities" | jq '.tools'
```

### Experience Matching

Consider the agent's prior experience with similar tasks:
- Has the agent completed similar work before?
- Did prior work meet quality standards?
- Were there issues that suggest capability gaps?

### Workload Consideration

Check the agent's current task load:
- How many tasks are currently assigned?
- What is the priority of current work?
- Is the agent blocked on anything?

### Availability Check

Verify the agent is active and responsive:
- When was the agent's last activity?
- Has the agent acknowledged recent messages?
- Is the session still running?

---

## 1.4 Role Assignment Procedure

**Step 1: Identify the role to assign**

Determine which role is needed based on the current task requirements. Review the standard role definitions to select the appropriate match.

**Step 2: Select the target agent**

Choose an agent based on capability matching, experience, workload, and availability as described in section 1.3.

**Step 3: Compose the assignment message**

Create a message containing:
- Role name being assigned
- List of specific responsibilities
- Expected reporting structure
- Any immediate tasks
- Acknowledgment request

**Step 4: Send the assignment via AI Maestro**

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "TARGET_AGENT_SESSION_NAME",
    "subject": "Role Assignment: ROLE_NAME",
    "priority": "high",
    "content": {
      "type": "role-assignment",
      "message": "You are assigned the ROLE_NAME role. Responsibilities: [LIST]. Report to: [AGENTS]. Please acknowledge receipt."
    }
  }'
```

**Step 5: Wait for acknowledgment**

The target agent should respond within a reasonable timeframe (5-10 minutes for active agents). If no response, proceed to troubleshooting.

**Step 6: Update team roster**

Record the role assignment in the coordination state file:

```markdown
## Team Roster
| Agent | Role | Assigned | Status |
|-------|------|----------|--------|
| helper-agent-generic | Code Reviewer | 2025-02-01T10:00:00Z | Active |
```

---

## 1.5 Confirming Role Acceptance

Role assignment is not complete until the agent confirms acceptance. This prevents assumptions that lead to coordination failures.

### Expected Acknowledgment Format

The assigned agent should respond with:
- Confirmation of role understanding
- Acknowledgment of responsibilities
- Any questions or concerns
- Ready status

### Example Acknowledgment

```json
{
  "type": "role-acknowledgment",
  "role": "Code Reviewer",
  "status": "accepted",
  "message": "Role accepted. I understand my responsibilities: review PRs, enforce standards, provide feedback. Ready to begin."
}
```

### Handling Non-Acknowledgment

If no acknowledgment is received:
1. Wait 5 minutes
2. Send a reminder with higher priority
3. If still no response after 10 minutes, check agent status
4. If agent is inactive, reassign role to another agent
5. If agent is active but unresponsive, escalate to user

---

## 1.6 Managing Role Transitions

When an agent's role needs to change, follow this transition procedure:

### Planned Transition

**Step 1:** Notify the current agent of the upcoming change

**Step 2:** Allow the agent to complete or hand off current work

**Step 3:** Send the role removal message

**Step 4:** Send the new role assignment to the replacement agent

**Step 5:** Update team roster

### Emergency Transition

For urgent transitions (agent failure, critical issue):

**Step 1:** Immediately assign role to backup agent

**Step 2:** Notify original agent of role removal (if still active)

**Step 3:** Review any incomplete work from original agent

**Step 4:** Update team roster

**Step 5:** Document the transition reason

---

## 1.7 Role Assignment Examples

### Example: Assigning Developer Role

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "libs-svg-svgbbox",
    "subject": "Role Assignment: Developer",
    "priority": "high",
    "content": {
      "type": "role-assignment",
      "message": "You are assigned the Developer role for the SVG library project. Responsibilities: implement features from backlog, write unit tests, update documentation. Report to: orchestrator-master for task assignments, libs-svg-reviewer for code reviews. Please acknowledge receipt and confirm you are ready to begin."
    }
  }'
```

### Example: Reassigning Role Due to Workload

```bash
# Step 1: Notify original agent
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "helper-agent-generic",
    "subject": "Role Transition: Code Reviewer",
    "priority": "normal",
    "content": {
      "type": "role-transition",
      "message": "Due to high workload, the Code Reviewer role will be transferred to helper-agent-backup. Please complete any in-progress reviews within 1 hour and hand off remaining items."
    }
  }'

# Step 2: Assign to new agent
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "helper-agent-backup",
    "subject": "Role Assignment: Code Reviewer",
    "priority": "high",
    "content": {
      "type": "role-assignment",
      "message": "You are assigned the Code Reviewer role. helper-agent-generic is handing off. Check for pending reviews in the queue."
    }
  }'
```

---

## 1.8 Troubleshooting

### Issue: Agent rejects role assignment

**Symptoms:** Agent responds with rejection or indicates inability to perform role.

**Possible causes:**
- Agent lacks required capabilities
- Agent has conflicting responsibilities
- Role requirements are unclear

**Resolution:**
1. Review the rejection reason
2. If capability issue, assign to a different agent
3. If conflict issue, resolve the conflict or reassign other work
4. If clarity issue, resend with more detailed instructions

### Issue: Agent does not acknowledge assignment

**Symptoms:** No response received within expected timeframe.

**Possible causes:**
- Agent session is inactive
- Message was not delivered
- Agent is overloaded and not processing inbox

**Resolution:**
1. Check agent status via AI Maestro
2. If inactive, assign role to backup agent
3. If active, send reminder with URGENT priority
4. If still no response, escalate to user

### Issue: Multiple agents claim same role

**Symptoms:** Role confusion, duplicate work, coordination conflicts.

**Possible causes:**
- Role assignment messages crossed
- Roster not updated correctly
- Agents not checking roster before claiming work

**Resolution:**
1. Immediately clarify which agent has the role
2. Update roster with single owner
3. Notify all agents of the correction
4. Review how the conflict occurred to prevent recurrence

### Issue: Role assignment conflicts with existing role

**Symptoms:** Agent cannot fulfill new role due to existing commitments.

**Possible causes:**
- Agent already has incompatible role
- Workload exceeds capacity
- Time conflicts between roles

**Resolution:**
1. Evaluate which role takes priority
2. Either remove old role or do not assign new role
3. Find alternative agent for the role that cannot be assigned
4. Update roster to reflect final state

---

**Version:** 1.0
**Last Updated:** 2025-02-01
