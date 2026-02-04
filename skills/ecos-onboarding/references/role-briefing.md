# Role Briefing Reference

## Table of Contents

- 2.1 [Role Briefing Components](#21-role-briefing-components)
- 2.2 [Explaining Role Responsibilities](#22-explaining-role-responsibilities)
- 2.3 [Clarifying Reporting Structure](#23-clarifying-reporting-structure)
- 2.4 [Setting Performance Expectations](#24-setting-performance-expectations)
- 2.5 [Handling Agent Questions](#25-handling-agent-questions)
- 2.6 [Confirming Role Understanding](#26-confirming-role-understanding)
- 2.7 [Role Briefing Examples](#27-role-briefing-examples)
- 2.8 [Troubleshooting](#28-troubleshooting)

---

## 2.1 Role Briefing Components

A complete role briefing contains five essential components:

### Component 1: Role Identity

The name and classification of the role:
- Official role title (Developer, Code Reviewer, Test Engineer, etc.)
- Role category (technical, coordination, quality, etc.)
- Seniority or specialization if applicable

### Component 2: Responsibilities

Specific duties the agent is expected to perform:
- Primary responsibilities (must do)
- Secondary responsibilities (may do when primary is complete)
- Out-of-scope activities (must not do without approval)

### Component 3: Reporting Structure

Who the agent communicates with and for what purpose:
- Direct reports (who gives assignments)
- Coordination partners (who to work with)
- Escalation path (who to go to for help)

### Component 4: Performance Expectations

How the agent's work will be evaluated:
- Quality standards
- Timeliness expectations
- Communication requirements
- Success metrics

### Component 5: Resources and Access

What the agent needs and can use:
- Required tools and their locations
- Documentation resources
- Access permissions
- Support channels

---

## 2.2 Explaining Role Responsibilities

Responsibilities must be explained clearly and specifically.

### Primary Responsibilities

These are the core duties the agent must prioritize:

**Format:**
```markdown
## Primary Responsibilities

You MUST perform these duties:

1. **[Responsibility Name]**: [Detailed description of what this means]
   - Example: [Concrete example of doing this correctly]
   - Frequency: [How often this is done]

2. **[Responsibility Name]**: [Detailed description]
   - Example: [Concrete example]
   - Frequency: [How often]
```

**Example for Developer:**
```markdown
## Primary Responsibilities

1. **Implement Features**: Write code that implements features from the assigned backlog
   - Example: Create the login endpoint as specified in TASK-042
   - Frequency: Continuously, as tasks are assigned

2. **Write Tests**: Create unit tests for all new code you write
   - Example: For login endpoint, write tests covering success, invalid password, user not found
   - Frequency: Before marking any implementation complete
```

### Secondary Responsibilities

These are duties the agent may take on when primary work allows:

**Format:**
```markdown
## Secondary Responsibilities

You MAY perform these duties when primary work is complete:

1. **[Responsibility Name]**: [Description]
```

### Out-of-Scope Activities

These are activities the agent must NOT perform without explicit approval:

**Format:**
```markdown
## Out of Scope

You MUST NOT do these without explicit approval:

1. **[Activity]**: [Why this is out of scope]
```

**Example:**
```markdown
## Out of Scope

1. **Deploy to Production**: Only DevOps agents handle production deployments
2. **Modify CI/CD Pipeline**: Requires orchestrator approval
3. **Merge PRs**: Only designated reviewers can merge
```

---

## 2.3 Clarifying Reporting Structure

The reporting structure tells the agent who to communicate with and for what.

### Direct Report (Task Assignment)

Who assigns work to this agent:

```markdown
## Task Assignments

You receive task assignments from: **orchestrator-master**

When you receive a task:
1. Acknowledge receipt promptly
2. Ask clarifying questions before starting
3. Provide regular status updates
4. Report completion when done
```

### Coordination Partners

Who the agent works alongside:

```markdown
## Coordination Partners

You coordinate with these team members:

- **code-reviewer-agent**: Send PRs for review, respond to review feedback
- **test-engineer-agent**: Coordinate on integration tests
- **documentation-agent**: Ensure docs are updated for your changes
```

### Escalation Path

Who to contact when issues arise:

```markdown
## Escalation Path

When you encounter issues:

1. **Technical Blockers**: Contact orchestrator-master
2. **Role Conflicts**: Contact chief-of-staff-agent
3. **Resource Issues**: Contact chief-of-staff-agent
4. **Unable to Reach Above**: If no response, message user directly
```

---

## 2.4 Setting Performance Expectations

Performance expectations tell the agent how their work will be evaluated.

### Quality Standards

What constitutes acceptable work:

```markdown
## Quality Standards

Your work must meet these standards:

- **Code**: Passes linting, has tests, follows conventions
- **Tests**: Minimum 80% coverage, all edge cases handled
- **Documentation**: Updated for all public interfaces
- **Communication**: Clear, concise, professional
```

### Timeliness Expectations

How quickly work should be completed:

```markdown
## Responsiveness

Expected behavior:

- **Message Acknowledgment**: Promptly acknowledge receipt
- **Task Start**: Begin work reasonably soon after assignment
- **Status Updates**: Provide regular updates during active work
- **Task Completion**: Complete when the work meets quality standards
```

### Communication Requirements

How the agent should communicate:

```markdown
## Communication Requirements

- **Priority**: Always include appropriate priority level
- **Status Updates**: Include: task ID, percent complete, blockers if any
- **Completion Reports**: Include: what was done, where to find it, what to verify
- **Issues**: Include: what happened, what you tried, what you need
```

### Success Metrics

How success is measured:

```markdown
## Success Metrics

You are succeeding if:

- Tasks are completed and meet quality standards
- Code reviews pass with minimal revision requests
- Team members find your communication clear and timely
- Escalations are rare and well-justified
```

---

## 2.5 Handling Agent Questions

Agents may have questions during or after the briefing.

### Common Questions

**Q: What if I am assigned a task outside my role?**
A: Acknowledge receipt, then message Chief of Staff to clarify role boundaries. Do not refuse outright.

**Q: What if I encounter a blocker that prevents completion?**
A: Report the issue as soon as you know. Include: what is blocking, what you've tried, options to consider.

**Q: What if I disagree with a decision or direction?**
A: Complete the assigned work unless it would cause harm. Raise concerns through appropriate channels afterward.

**Q: What if two people give me conflicting instructions?**
A: Pause, acknowledge both, and escalate to Chief of Staff for resolution. Do not proceed until clarified.

### Handling Unknown Questions

If an agent asks something not covered:
1. Acknowledge the question
2. If you know the answer, provide it
3. If you don't know, say so clearly
4. Escalate to user if the question is important and unanswered

---

## 2.6 Confirming Role Understanding

Before completing the briefing, confirm the agent understands.

### Understanding Confirmation Protocol

**Step 1: Ask for summary**

Request the agent to summarize their understanding:

"Please summarize your role in your own words, including:
1. Your role title and primary responsibilities
2. Who you report to for assignments
3. How you should handle blockers
4. Your first assigned task"

**Step 2: Evaluate the summary**

Check for:
- Correct role title
- Accurate listing of primary responsibilities
- Correct reporting structure
- Understanding of escalation

**Step 3: Correct any errors**

If the summary is incorrect:
- Point out specific errors
- Re-explain the correct information
- Ask for corrected summary

**Step 4: Confirm readiness**

Once summary is correct:
- Ask agent to confirm they are ready to begin
- Assign first task
- Document confirmation

### Example Confirmation Exchange

```
Chief of Staff: "Please summarize your role as you understand it."

Agent: "I am a Developer on the Authentication module. My primary
responsibilities are implementing features, writing tests, and updating
docs. I receive assignments from orchestrator-master and coordinate
with auth-code-reviewer for reviews. If I'm blocked, I contact
orchestrator-master. My first task is to implement the logout endpoint."

Chief of Staff: "Correct. You are cleared to begin. Proceed with the
logout endpoint implementation. Send your first status update within
2 hours."

Agent: "Understood. Beginning work on logout endpoint now."
```

---

## 2.7 Role Briefing Examples

### Example: Full Developer Role Briefing

```markdown
# Role Briefing: Developer

## Role Identity
- **Title:** Developer
- **Category:** Technical
- **Specialization:** Backend (Python)

## Primary Responsibilities

You MUST perform these duties:

1. **Implement Features**: Write code implementing features from the backlog
   - Example: Create API endpoints as specified in task tickets
   - Frequency: Continuously, as assigned

2. **Write Unit Tests**: Create tests for all new code
   - Example: For each endpoint, tests for success and error cases
   - Frequency: Before marking any task complete

3. **Update Documentation**: Keep docs current for your changes
   - Example: Update API docs when adding new endpoints
   - Frequency: As part of each implementation

## Secondary Responsibilities

You MAY perform these when primary work is complete:

1. **Refactoring**: Improve code quality when opportunity arises
2. **Bug Fixes**: Address bugs discovered during development

## Out of Scope

You MUST NOT do these without explicit approval:

1. **Deploy to Production**: DevOps only
2. **Merge PRs**: Reviewers only
3. **Change Database Schema**: Requires architecture approval

## Reporting Structure

- **Task Assignments From:** orchestrator-master
- **Coordinate With:** code-reviewer (PR reviews), test-engineer (integration)
- **Escalate To:** orchestrator-master (technical), chief-of-staff (role/resource)

## Performance Expectations

- **Acknowledgment:** Promptly after assignment
- **Status Updates:** Regularly during active work
- **Quality:** Code passes lint, has tests, follows conventions
- **Completion:** Report when done with PR link

## Resources

- **Code Repository:** /src/auth/
- **Tests Location:** /tests/unit/auth/
- **Style Guide:** /docs/CONVENTIONS.md
- **Team Roster:** design/memory/team-roster.md
```

### Example: Abbreviated Briefing for Role Change

```markdown
# Role Briefing Update: Code Reviewer (was Developer)

## Changes from Previous Role

- **New Primary Duty:** Review PRs instead of writing code
- **New Reports To:** Still orchestrator-master
- **New Success Metric:** Review quality and turnaround time

## New Responsibilities

1. **Review PRs**: Evaluate code for quality, conventions, and correctness
2. **Provide Feedback**: Give constructive comments with specific suggestions
3. **Approve/Request Changes**: Use GitHub review system appropriately

## Removed from Scope

- Writing production code (except review test cases)
- Implementation tasks
- Documentation writing (except review feedback)

## Expectations

- Review turnaround: Promptly after assignment
- Provide at least 3 substantive comments per review
- Clear approve/request-changes decision on each review

Please confirm you understand the role change.
```

---

## 2.8 Troubleshooting

### Issue: Agent keeps performing out-of-scope activities

**Symptoms:** Agent does work not assigned to their role.

**Possible causes:**
- Briefing was unclear about scope
- Agent has carryover from previous role
- Agent is trying to be helpful

**Resolution:**
1. Immediately clarify the scope violation
2. Re-explain out-of-scope boundaries
3. If repeated, add explicit "do not do" examples
4. If persistent, escalate to user

### Issue: Agent claims role is too narrow

**Symptoms:** Agent expresses frustration with limited scope, asks for more responsibilities.

**Possible causes:**
- Role genuinely too narrow for agent capabilities
- Agent misunderstands team structure
- Workload imbalance

**Resolution:**
1. Acknowledge the feedback
2. Explain why role boundaries exist
3. If valid concern, escalate to orchestrator for role adjustment
4. Consider assigning secondary responsibilities

### Issue: Agent does not understand reporting structure

**Symptoms:** Agent messages wrong people, skips escalation levels.

**Possible causes:**
- Briefing was unclear
- Multiple similar names causing confusion
- Agent context mixed with prior session

**Resolution:**
1. Re-explain reporting structure with names and purposes
2. Provide decision tree: "If X happens, contact Y"
3. Practice with hypothetical scenarios
4. Verify understanding before proceeding

### Issue: Agent cannot meet performance expectations

**Symptoms:** Unresponsive behavior, quality issues, incomplete work.

**Possible causes:**
- Expectations too high for role
- Agent overloaded
- Capability mismatch

**Resolution:**
1. Identify specific expectation being missed
2. Determine if adjustment is needed or agent needs coaching
3. If expectations unrealistic, revise with orchestrator
4. If capability issue, consider role reassignment

---

**Version:** 1.0
**Last Updated:** 2025-02-01
