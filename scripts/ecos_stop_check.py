#!/usr/bin/env python3
"""
ecos_stop_check.py - Block exit if agents have pending tasks.

Stop hook that prevents Chief of Staff from exiting with incomplete work:
1. Active agents with incomplete work (status != 'done')
2. Pending tasks in the state file
3. Unread AI Maestro messages requiring response
4. Unacknowledged handoffs

Dependencies: Python 3.8+ stdlib only

Usage (as Claude Code hook):
    Receives JSON via stdin from Stop hook event.
    Returns JSON with decision to allow or block exit.

Exit codes:
    0 - Allow exit (no blocking issues found)
    2 - Block exit (JSON output with block decision and reason)
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


def get_state_file(cwd: str) -> Path:
    """Get the Chief of Staff state file path."""
    return Path(cwd) / ".claude" / "chief-of-staff-state.local.md"


def read_file_safely(path: Path) -> str:
    """Read file content safely, return empty string if not found."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def check_active_agents(content: str) -> tuple[int, list[str]]:
    """Check for active agents with incomplete work.

    Args:
        content: State file content

    Returns:
        Tuple of (count, list of agent descriptions with incomplete work)
    """
    incomplete: list[str] = []

    # Find Active Agents table
    in_table = False
    header_passed = False

    for line in content.split("\n"):
        if "## Active Agents" in line:
            in_table = True
            continue
        if in_table:
            if line.startswith("##"):
                break
            if line.startswith("|"):
                if "Agent" in line and "Role" in line:
                    continue
                if "---" in line:
                    header_passed = True
                    continue
                if header_passed and "_No agents" not in line:
                    parts = [p.strip() for p in line.split("|")[1:-1]]
                    if len(parts) >= 3:
                        name = parts[0]
                        role = parts[1]
                        status = parts[2].lower()
                        # Check if agent has incomplete work
                        if status not in ("done", "completed", "idle", "session_ended", "-"):
                            incomplete.append(f"{name} ({role}): {status}")

    return len(incomplete), incomplete


def check_pending_tasks(content: str) -> tuple[int, list[str]]:
    """Check for pending tasks in state file.

    Args:
        content: State file content

    Returns:
        Tuple of (count, list of task descriptions)
    """
    tasks: list[str] = []

    in_section = False
    for line in content.split("\n"):
        if "## Pending Tasks" in line:
            in_section = True
            continue
        if in_section:
            if line.startswith("##"):
                break
            if line.strip().startswith("-"):
                task = line.strip().lstrip("-").strip()
                if task and "No pending tasks" not in task:
                    tasks.append(task[:80])

    return len(tasks), tasks


def check_ai_maestro_inbox() -> tuple[int, list[str]]:
    """Check AI Maestro inbox for unread messages.

    Returns:
        Tuple of (unread_count, list of message subjects)
    """
    api_url = os.environ.get("AIMAESTRO_API", "http://localhost:23000")
    agent_name = os.environ.get("SESSION_NAME", "chief-of-staff")

    try:
        result = subprocess.run(
            ["curl", "-s", "-m", "3",
             f"{api_url}/api/messages?agent={agent_name}&action=list&status=unread"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            messages = data.get("messages", [])
            subjects = [msg.get("subject", "No subject")[:60] for msg in messages]
            return len(messages), subjects
    except (subprocess.TimeoutExpired, json.JSONDecodeError, subprocess.SubprocessError):
        pass
    return 0, []


def check_handoffs(cwd: str) -> tuple[int, list[str]]:
    """Check for unacknowledged handoffs.

    Args:
        cwd: Current working directory

    Returns:
        Tuple of (count, list of handoff descriptions)
    """
    pending: list[str] = []
    handoffs_dir = Path(cwd) / ".claude" / "ecos" / "handoffs"

    if handoffs_dir.exists() and handoffs_dir.is_dir():
        for handoff_file in handoffs_dir.glob("*.md"):
            try:
                content = handoff_file.read_text(encoding="utf-8")
                content_lower = content.lower()
                if "status: pending" in content_lower or "acknowledged: false" in content_lower:
                    pending.append(f"Handoff: {handoff_file.stem}")
            except (OSError, UnicodeDecodeError):
                pass

    return len(pending), pending


def build_blocking_response(issues: dict[str, Any]) -> dict[str, Any]:
    """Build the JSON response for blocking exit.

    Args:
        issues: Dictionary of issue categories and their details

    Returns:
        JSON-serializable dict with block decision
    """
    reason_parts = []

    if issues.get("active_agents", 0) > 0:
        reason_parts.append(f"{issues['active_agents']} agent(s) with incomplete work")
    if issues.get("pending_tasks", 0) > 0:
        reason_parts.append(f"{issues['pending_tasks']} pending task(s)")
    if issues.get("unread_messages", 0) > 0:
        reason_parts.append(f"{issues['unread_messages']} unread message(s)")
    if issues.get("pending_handoffs", 0) > 0:
        reason_parts.append(f"{issues['pending_handoffs']} unacknowledged handoff(s)")

    reason = "Cannot exit: " + ", ".join(reason_parts)

    # Build details section for display
    details_lines = []
    if issues.get("active_agents_list"):
        details_lines.append("\nAgents with incomplete work:")
        for agent in issues["active_agents_list"][:5]:
            details_lines.append(f"  - {agent}")
    if issues.get("pending_tasks_list"):
        details_lines.append("\nPending tasks:")
        for task in issues["pending_tasks_list"][:5]:
            details_lines.append(f"  - {task}")
    if issues.get("unread_subjects"):
        details_lines.append("\nUnread messages:")
        for subj in issues["unread_subjects"][:3]:
            details_lines.append(f"  - {subj}")

    return {
        "decision": "block",
        "reason": reason + "\n" + "\n".join(details_lines),
        "hookSpecificOutput": {
            "hookEventName": "Stop",
            "permissionDecision": "deny",
            "permissionDecisionReason": "Incomplete coordination work"
        }
    }


def main() -> int:
    """Main entry point for Stop hook.

    Checks for incomplete coordination work and blocks exit if found.

    Returns:
        Exit code: 0 for allow, 2 for block
    """
    # Read hook input from stdin
    try:
        stdin_data = sys.stdin.read()
        if stdin_data.strip():
            hook_input = json.loads(stdin_data)
        else:
            hook_input = {}
    except json.JSONDecodeError:
        hook_input = {}

    # Get working directory from input or environment
    cwd = hook_input.get("cwd", os.getcwd())
    state_file = get_state_file(cwd)

    # Read state file
    content = read_file_safely(state_file) if state_file.exists() else ""

    # Collect all blocking issues
    issues: dict[str, Any] = {}

    # 1. Check active agents with incomplete work
    agents_count, agents_list = check_active_agents(content)
    if agents_count > 0:
        issues["active_agents"] = agents_count
        issues["active_agents_list"] = agents_list

    # 2. Check pending tasks
    tasks_count, tasks_list = check_pending_tasks(content)
    if tasks_count > 0:
        issues["pending_tasks"] = tasks_count
        issues["pending_tasks_list"] = tasks_list

    # 3. Check AI Maestro inbox
    unread_count, unread_subjects = check_ai_maestro_inbox()
    if unread_count > 0:
        issues["unread_messages"] = unread_count
        issues["unread_subjects"] = unread_subjects

    # 4. Check handoffs
    handoffs_count, handoffs_list = check_handoffs(cwd)
    if handoffs_count > 0:
        issues["pending_handoffs"] = handoffs_count
        issues["pending_handoffs_list"] = handoffs_list

    # Decision: block if any issues found
    if issues:
        response = build_blocking_response(issues)
        print(json.dumps(response, indent=2))
        return 2  # Block exit

    # No issues - allow exit
    return 0


if __name__ == "__main__":
    sys.exit(main())
