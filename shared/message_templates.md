# AI Maestro Message Templates

Standard message formats for inter-role communication via AI Maestro.

> All message templates below should be sent using the `agent-messaging` skill, which handles the AI Maestro API format automatically.

## Chief of Staff Specific Message Types

### 1. Onboarding Message

Sent to newly spawned agents to establish their role and task.

> **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

```json
{
  "to": "{agent-session-name}",
  "subject": "[ONBOARDING] {role} assigned for {project}",
  "priority": "high",
  "content": {
    "type": "onboarding",
    "message": "You have been assigned as {role} for {project}. Please acknowledge receipt and begin work.",
    "session_name": "{agent-session-name}",
    "coordinator": "{ecos-session-name}",
    "handoff_document": "docs_dev/handoffs/handoff-{uuid}-ecos-to-{role}.md",
    "github_issue": "#{issue_number}",
    "constraints": {
      "max_duration_minutes": 60,
      "requires_approval_for": ["push", "merge", "publish"],
      "scope": "{scope_description}"
    },
    "success_criteria": [
      "{criterion_1}",
      "{criterion_2}"
    ],
    "ack_required": true
  }
}
```

### 2. Role Briefing Message

Detailed briefing sent after agent acknowledges onboarding.

> **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

```json
{
  "to": "{agent-session-name}",
  "subject": "[BRIEFING] Detailed instructions for {task_name}",
  "priority": "high",
  "content": {
    "type": "role_briefing",
    "message": "{detailed_task_description}",
    "context": {
      "project_state": "{current_project_state}",
      "prior_work": "{relevant_prior_work}",
      "related_issues": ["#issue1", "#issue2"]
    },
    "deliverables": [
      {"name": "{deliverable_1}", "format": "{format}", "location": "{path}"},
      {"name": "{deliverable_2}", "format": "{format}", "location": "{path}"}
    ],
    "resources": {
      "documentation": ["{doc_path_1}", "{doc_path_2}"],
      "examples": ["{example_path}"],
      "tools": ["{tool_1}", "{tool_2}"]
    },
    "workflow": "{recommended_workflow}",
    "checkpoints": [
      {"at": "25%", "report": "initial_assessment"},
      {"at": "50%", "report": "progress_update"},
      {"at": "75%", "report": "pre_completion"},
      {"at": "100%", "report": "completion"}
    ]
  }
}
```

### 3. Termination Warning Message

Sent when agent will be terminated due to timeout or resource constraints.

> **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

```json
{
  "to": "{agent-session-name}",
  "subject": "[WARNING] Termination in {seconds} seconds",
  "priority": "urgent",
  "content": {
    "type": "termination_warning",
    "message": "Your session will be terminated in {seconds} seconds. Reason: {reason}",
    "reason": "heartbeat_timeout" | "resource_exhaustion" | "user_request" | "scope_violation",
    "grace_period_seconds": 30,
    "actions_required": [
      "Save current work state",
      "Create handoff document",
      "Report final status"
    ],
    "handoff_path": "docs_dev/handoffs/handoff-{uuid}-{role}-emergency.md"
  }
}
```

### 4. Heartbeat Poll Message

Periodic message to verify agent responsiveness.

> **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

```json
{
  "to": "{agent-session-name}",
  "subject": "[HEARTBEAT] Status check",
  "priority": "normal",
  "content": {
    "type": "heartbeat_poll",
    "message": "Please confirm you are active and responsive.",
    "poll_id": "{uuid}",
    "timeout_seconds": 60,
    "response_required": {
      "status": "active" | "busy" | "blocked" | "completing",
      "current_task": "{brief_description}",
      "progress_percent": 0-100,
      "eta_minutes": 0-999
    }
  }
}
```

### 5. Performance Report Request

Request for detailed performance metrics from an agent.

> **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

```json
{
  "to": "{agent-session-name}",
  "subject": "[REPORT] Performance metrics requested",
  "priority": "normal",
  "content": {
    "type": "performance_report_request",
    "message": "Please provide a detailed performance report.",
    "report_type": "full" | "summary" | "metrics_only",
    "time_period": {
      "start": "{ISO-8601}",
      "end": "{ISO-8601}"
    },
    "metrics_requested": [
      "tasks_completed",
      "tasks_failed",
      "average_task_duration",
      "resource_usage",
      "blockers_encountered",
      "approvals_requested"
    ],
    "output_path": "docs_dev/reports/perf-{agent}-{date}.md"
  }
}
```

---

## General Message Types

### 6. Task Assignment

> **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

```json
{
  "to": "{target-agent-session}",
  "subject": "[TASK] {brief_description}",
  "priority": "high",
  "content": {
    "type": "task_assignment",
    "message": "{detailed_instructions}",
    "handoff_file": "docs_dev/handoffs/handoff-{uuid}-ecos-to-{role}.md",
    "github_issue": "#{issue_number}",
    "deadline": "{ISO-8601 timestamp or null}"
  }
}
```

### 7. Status Request

> **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

```json
{
  "to": "{target-agent-session}",
  "subject": "[STATUS] Request for {project/task}",
  "priority": "normal",
  "content": {
    "type": "status_request",
    "message": "Please provide status update on {task_description}",
    "fields_requested": ["progress_percent", "blockers", "eta", "next_steps"]
  }
}
```

### 8. Status Update

> **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

```json
{
  "to": "ecos-session",
  "subject": "[UPDATE] {task_name} - {status}",
  "priority": "normal",
  "content": {
    "type": "status_update",
    "message": "{summary}",
    "progress_percent": 75,
    "blockers": ["blocker1", "blocker2"],
    "completed_items": ["item1", "item2"],
    "next_steps": ["step1", "step2"],
    "eta": "{ISO-8601 timestamp}"
  }
}
```

### 9. Completion Signal

> **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

```json
{
  "to": "ecos-session",
  "subject": "[COMPLETE] {task_name}",
  "priority": "high",
  "content": {
    "type": "completion",
    "message": "{summary_of_deliverables}",
    "handoff_file": "docs_dev/handoffs/handoff-{uuid}-{role}-to-ecos.md",
    "github_issue": "#{issue_number}",
    "artifacts": ["path/to/artifact1", "path/to/artifact2"],
    "verification_status": "passed" | "failed" | "partial"
  }
}
```

### 10. Approval Request

> **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

```json
{
  "to": "ecos-session",
  "subject": "[APPROVAL] {approval_type} for {item}",
  "priority": "high",
  "content": {
    "type": "approval_request",
    "message": "{description_of_what_needs_approval}",
    "approval_type": "push" | "merge" | "publish" | "security" | "release",
    "affected_items": ["item1", "item2"],
    "risk_assessment": "low" | "medium" | "high",
    "rollback_plan": "{description}"
  }
}
```

### 11. Approval Response

> **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

```json
{
  "to": "{requesting-agent-session}",
  "subject": "[APPROVED/REJECTED] {approval_type} for {item}",
  "priority": "high",
  "content": {
    "type": "approval_response",
    "message": "{user_feedback_if_any}",
    "decision": "approved" | "rejected" | "needs_revision",
    "conditions": ["condition1", "condition2"],
    "user_comment": "{optional_user_comment}"
  }
}
```

### 12. Question / Clarification

> **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

```json
{
  "to": "ecos-session",
  "subject": "[QUESTION] {brief_topic}",
  "priority": "normal",
  "content": {
    "type": "question",
    "message": "{detailed_question}",
    "context": "{relevant_context}",
    "options": ["option1", "option2"],
    "blocking": true | false
  }
}
```

### 13. Error / Issue Report

> **Note**: Use the `agent-messaging` skill to send messages. The JSON structure below shows the message content.

```json
{
  "to": "ecos-session",
  "subject": "[ERROR] {error_type} in {component}",
  "priority": "urgent",
  "content": {
    "type": "error_report",
    "message": "{error_description}",
    "error_type": "build_failure" | "test_failure" | "integration_issue" | "blocker",
    "affected_components": ["component1", "component2"],
    "attempted_solutions": ["solution1", "solution2"],
    "needs_user_input": true | false
  }
}
```

---

## Session Name Convention

| Role | Prefix | Session Name Pattern |
|------|--------|---------------------|
| Chief of Staff | `ecos-` | `ecos-{project}-session` |
| Architect | `eaa-` | `eaa-{project}-session` |
| Orchestrator | `eoa-` | `eoa-{project}-session` |
| Integrator | `eia-` | `eia-{project}-session` |

**Prefix Legend:**
- `e` = Emasoft (author identifier)
- `cos` = Chief of Staff
- `aa` = Architect Agent
- `oa` = Orchestrator Agent
- `ia` = Integrator Agent

---

## Priority Levels

| Priority | Use Case |
|----------|----------|
| `urgent` | Blocking issues, critical errors, security issues, termination warnings |
| `high` | Onboarding, completion signals, approval requests, important updates |
| `normal` | Status updates, heartbeat polls, questions, routine communication |
| `low` | Non-blocking information, FYI messages, performance reports |
