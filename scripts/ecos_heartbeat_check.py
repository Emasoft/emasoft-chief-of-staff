#!/usr/bin/env python3
"""
ecos_heartbeat_check.py - UserPromptSubmit hook for agent health monitoring.

Checks last heartbeat of all registered agents and warns if any are unresponsive
(no heartbeat for >5 minutes).

Light-weight check designed to complete within 5 seconds.

Dependencies: Python 3.8+ stdlib only

Usage (as Claude Code hook):
    Receives JSON via stdin from UserPromptSubmit hook event.
    Outputs warning system message if any agents are unresponsive.

Exit codes:
    0 - Success (all agents healthy or warning issued)
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


# Heartbeat timeout in seconds (5 minutes)
HEARTBEAT_TIMEOUT = 300


def get_state_file(cwd: str) -> Path:
    """Get the Chief of Staff state file path."""
    return Path(cwd) / ".claude" / "chief-of-staff-state.local.md"


def read_file_safely(path: Path) -> str:
    """Read file content safely, return empty string if not found."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def parse_timestamp(ts_str: str) -> datetime | None:
    """Parse a timestamp string into datetime.

    Supports multiple formats:
    - ISO format: 2025-02-01T10:30:00
    - Simple format: 2025-02-01 10:30:00
    - Time only: 10:30:00 (assumes today)

    Args:
        ts_str: Timestamp string

    Returns:
        datetime object or None if parsing fails
    """
    ts_str = ts_str.strip()

    formats = [
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%d %H:%M",
        "%H:%M:%S",
        "%H:%M",
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(ts_str, fmt)
            # If no date, assume today
            if fmt in ("%H:%M:%S", "%H:%M"):
                today = datetime.now().date()
                dt = dt.replace(year=today.year, month=today.month, day=today.day)
            return dt
        except ValueError:
            continue

    return None


def parse_agents_heartbeats(content: str) -> list[dict[str, Any]]:
    """Parse agent heartbeats from state file.

    Args:
        content: State file content

    Returns:
        List of agent dicts with name, role, status, heartbeat, heartbeat_dt
    """
    agents: list[dict[str, Any]] = []

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
                    if len(parts) >= 4:
                        heartbeat_str = parts[3]
                        heartbeat_dt = parse_timestamp(heartbeat_str)

                        agents.append({
                            "name": parts[0],
                            "role": parts[1],
                            "status": parts[2],
                            "heartbeat": heartbeat_str,
                            "heartbeat_dt": heartbeat_dt
                        })

    return agents


def check_unresponsive_agents(agents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Check for agents that have not sent a heartbeat recently.

    Args:
        agents: List of agent dictionaries

    Returns:
        List of unresponsive agent dicts
    """
    unresponsive: list[dict[str, Any]] = []
    now = datetime.now()

    for agent in agents:
        # Skip agents marked as done or idle
        status = agent.get("status", "").lower()
        if status in ("done", "completed", "idle", "session_ended", "-"):
            continue

        heartbeat_dt = agent.get("heartbeat_dt")
        if heartbeat_dt is None:
            # No valid heartbeat timestamp - consider unresponsive
            unresponsive.append({
                "name": agent["name"],
                "role": agent["role"],
                "status": agent["status"],
                "last_heartbeat": agent["heartbeat"],
                "seconds_since": "unknown"
            })
        else:
            # Check if heartbeat is stale
            delta = (now - heartbeat_dt).total_seconds()
            if delta > HEARTBEAT_TIMEOUT:
                minutes = int(delta / 60)
                unresponsive.append({
                    "name": agent["name"],
                    "role": agent["role"],
                    "status": agent["status"],
                    "last_heartbeat": agent["heartbeat"],
                    "seconds_since": int(delta),
                    "minutes_since": minutes
                })

    return unresponsive


def format_unresponsive_warning(unresponsive: list[dict[str, Any]]) -> str:
    """Format unresponsive agents warning message.

    Args:
        unresponsive: List of unresponsive agent dicts

    Returns:
        Formatted warning string
    """
    lines = []
    lines.append("")
    lines.append("!!! AGENT HEALTH WARNING !!!")
    lines.append("-" * 40)
    lines.append(f"The following {len(unresponsive)} agent(s) are unresponsive:")
    lines.append("")

    for agent in unresponsive:
        name = agent["name"]
        role = agent["role"]
        status = agent["status"]
        minutes = agent.get("minutes_since", "?")
        lines.append(f"  - {name} ({role})")
        lines.append(f"    Status: {status}")
        lines.append(f"    Last heartbeat: {minutes} minutes ago")

    lines.append("")
    lines.append("-" * 40)
    lines.append("Consider checking agent status or restarting unresponsive agents.")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    """Main entry point for UserPromptSubmit hook.

    Checks agent heartbeats and outputs warning if any are unresponsive.

    Returns:
        Exit code: 0 for success
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

    # Get working directory
    cwd = hook_input.get("cwd", os.getcwd())
    state_file = get_state_file(cwd)

    # Read state file
    if not state_file.exists():
        # No state file - nothing to check
        return 0

    content = read_file_safely(state_file)
    if not content:
        return 0

    # Parse agents and check heartbeats
    agents = parse_agents_heartbeats(content)
    if not agents:
        return 0

    unresponsive = check_unresponsive_agents(agents)

    # Output warning if any unresponsive agents
    if unresponsive:
        warning = format_unresponsive_warning(unresponsive)
        # Output as JSON with systemMessage for Claude to see
        output = {
            "systemMessage": warning,
            "continue": True  # Don't block, just warn
        }
        print(json.dumps(output))

    return 0


if __name__ == "__main__":
    sys.exit(main())
