#!/usr/bin/env python3
"""
ecos_session_start.py - Initialize Chief of Staff state on session start.

SessionStart hook that loads the Chief of Staff state file and outputs a system
message summarizing the staff status to help Claude resume work seamlessly.

State file: .claude/chief-of-staff-state.local.md

Dependencies: Python 3.8+ stdlib only

Usage (as Claude Code hook):
    Receives JSON via stdin from SessionStart hook event.
    Outputs system message to stdout with staff status summary.
    Creates state file if not exists.

Exit codes:
    0 - Success (state loaded or created)
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def get_state_file(cwd: str) -> Path:
    """Get the Chief of Staff state file path.

    Args:
        cwd: Current working directory

    Returns:
        Path to .claude/chief-of-staff-state.local.md
    """
    return Path(cwd) / ".claude" / "chief-of-staff-state.local.md"


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def create_default_state() -> str:
    """Create default state file content.

    Returns:
        Default state file content as markdown
    """
    timestamp = get_timestamp()
    return f"""# Chief of Staff State

**Last Updated**: {timestamp}
**Session Count**: 1

## Active Agents

| Agent | Role | Status | Last Heartbeat |
|-------|------|--------|----------------|
| _No agents registered_ | - | - | - |

## Pending Tasks

- No pending tasks

## Resource Alerts

- None

## Session History

### {timestamp}
- Session started
- State file initialized
"""


def read_file_safely(path: Path) -> str:
    """Read file content safely, return empty string if not found."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def write_file_safely(path: Path, content: str) -> bool:
    """Write file content safely with error handling."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return True
    except OSError as e:
        print(f"ERROR: Cannot write file {path}: {e}", file=sys.stderr)
        return False


def parse_active_agents(content: str) -> list[dict[str, str]]:
    """Parse active agents from state file.

    Args:
        content: State file content

    Returns:
        List of agent dictionaries with name, role, status, heartbeat
    """
    agents: list[dict[str, str]] = []

    # Find the Active Agents table
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
                    header_passed = False
                    continue
                if "---" in line:
                    header_passed = True
                    continue
                if header_passed and "_No agents" not in line:
                    parts = [p.strip() for p in line.split("|")[1:-1]]
                    if len(parts) >= 4:
                        agents.append({
                            "name": parts[0],
                            "role": parts[1],
                            "status": parts[2],
                            "heartbeat": parts[3]
                        })

    return agents


def parse_pending_tasks(content: str) -> list[str]:
    """Parse pending tasks from state file.

    Args:
        content: State file content

    Returns:
        List of pending task descriptions
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
                    tasks.append(task)

    return tasks


def parse_resource_alerts(content: str) -> list[str]:
    """Parse resource alerts from state file.

    Args:
        content: State file content

    Returns:
        List of resource alert descriptions
    """
    alerts: list[str] = []

    in_section = False
    for line in content.split("\n"):
        if "## Resource Alerts" in line:
            in_section = True
            continue
        if in_section:
            if line.startswith("##"):
                break
            if line.strip().startswith("-"):
                alert = line.strip().lstrip("-").strip()
                if alert and alert != "None":
                    alerts.append(alert)

    return alerts


def format_status_summary(
    agents: list[dict[str, str]],
    tasks: list[str],
    alerts: list[str],
    session_count: int
) -> str:
    """Format staff status into a system message summary.

    Args:
        agents: List of active agent dicts
        tasks: List of pending tasks
        alerts: List of resource alerts
        session_count: Number of sessions

    Returns:
        Formatted summary string for system message
    """
    lines = []
    lines.append("=" * 60)
    lines.append("CHIEF OF STAFF - SESSION START")
    lines.append("=" * 60)

    lines.append(f"\nSession #{session_count}")

    if agents:
        lines.append("\nACTIVE AGENTS:")
        for agent in agents:
            status_icon = "+" if agent["status"].lower() == "active" else "?"
            lines.append(f"  [{status_icon}] {agent['name']} ({agent['role']}) - {agent['status']}")
    else:
        lines.append("\nNo active agents registered.")

    if tasks:
        lines.append(f"\nPENDING TASKS ({len(tasks)}):")
        for task in tasks[:5]:
            lines.append(f"  - {task[:70]}")
        if len(tasks) > 5:
            lines.append(f"  ... and {len(tasks) - 5} more")

    if alerts:
        lines.append("\n!!! RESOURCE ALERTS !!!")
        for alert in alerts:
            lines.append(f"  ! {alert}")

    lines.append("")
    lines.append("=" * 60)
    lines.append("State file: .claude/chief-of-staff-state.local.md")
    lines.append("=" * 60)

    return "\n".join(lines)


def increment_session_count(content: str) -> str:
    """Increment session count in state file content.

    Args:
        content: State file content

    Returns:
        Updated content with incremented session count
    """
    import re

    # Find and increment session count
    match = re.search(r"\*\*Session Count\*\*:\s*(\d+)", content)
    if match:
        old_count = int(match.group(1))
        new_count = old_count + 1
        content = content.replace(
            f"**Session Count**: {old_count}",
            f"**Session Count**: {new_count}"
        )
    else:
        # Add session count if missing
        content = content.replace(
            "# Chief of Staff State\n",
            "# Chief of Staff State\n\n**Session Count**: 1\n"
        )

    return content


def get_session_count(content: str) -> int:
    """Get session count from state file content.

    Args:
        content: State file content

    Returns:
        Session count integer
    """
    import re

    match = re.search(r"\*\*Session Count\*\*:\s*(\d+)", content)
    if match:
        return int(match.group(1))
    return 1


def main() -> int:
    """Main entry point for SessionStart hook.

    Reads session info from stdin, loads or creates Chief of Staff state file,
    and outputs a status summary to stdout.

    Returns:
        Exit code: 0 for success
    """
    # Read hook input from stdin (may be empty for SessionStart)
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

    # Create state file if not exists
    if not state_file.exists():
        default_content = create_default_state()
        if not write_file_safely(state_file, default_content):
            return 0  # Silent failure
        content = default_content
    else:
        content = read_file_safely(state_file)
        if not content:
            content = create_default_state()
            write_file_safely(state_file, content)

    # Increment session count and update timestamp
    content = increment_session_count(content)
    timestamp = get_timestamp()

    # Update last updated timestamp
    import re
    content = re.sub(
        r"\*\*Last Updated\*\*:\s*[^\n]+",
        f"**Last Updated**: {timestamp}",
        content
    )

    # Save updated state
    write_file_safely(state_file, content)

    # Parse state
    agents = parse_active_agents(content)
    tasks = parse_pending_tasks(content)
    alerts = parse_resource_alerts(content)
    session_count = get_session_count(content)

    # Output status summary
    summary = format_status_summary(agents, tasks, alerts, session_count)
    print(summary)

    return 0


if __name__ == "__main__":
    sys.exit(main())
