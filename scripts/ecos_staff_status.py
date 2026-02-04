#!/usr/bin/env python3
"""
ecos_staff_status.py - Get status of all managed agents.

Reads the chief-of-staff state file and outputs JSON with agent status information
including session name, role, assigned project, status, and last heartbeat.

Dependencies: Python 3.8+ stdlib only

Usage:
    ecos_staff_status.py [--project PROJECT_ID]

Exit codes:
    0 - Success
    1 - Error (file not found, parse error)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def get_state_file_path(cwd: str | None = None) -> Path:
    """Get the chief-of-staff state file path.

    Args:
        cwd: Current working directory (defaults to os.getcwd())

    Returns:
        Path to .claude/chief-of-staff-state.local.md
    """
    if cwd is None:
        cwd = os.getcwd()
    return Path(cwd) / ".claude" / "chief-of-staff-state.local.md"


def read_file_safely(path: Path) -> str:
    """Read file content safely, return empty string if not found."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def parse_yaml_block(content: str, block_name: str) -> list[dict[str, Any]]:
    """Parse a YAML-like block from the state file.

    Args:
        content: Full content of the state file
        block_name: Name of the block to parse (e.g., 'agents', 'projects')

    Returns:
        List of dictionaries representing the block items
    """
    items: list[dict[str, Any]] = []

    # Find the block section
    pattern = rf"^## {block_name}\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    if not match:
        return items

    block_content = match.group(1)

    # Parse each item (indicated by ### or - with yaml-like structure)
    item_pattern = r"^### ([^\n]+)\n(.*?)(?=\n### |\Z)"
    for item_match in re.finditer(item_pattern, block_content, re.MULTILINE | re.DOTALL):
        item_name = item_match.group(1).strip()
        item_body = item_match.group(2)

        item: dict[str, Any] = {"name": item_name}

        # Parse key: value pairs
        for line in item_body.split("\n"):
            line = line.strip()
            if line.startswith("- **") and "**:" in line:
                # Format: - **Key**: Value
                kv_match = re.match(r"- \*\*([^*]+)\*\*:\s*(.+)", line)
                if kv_match:
                    key = kv_match.group(1).strip().lower().replace(" ", "_")
                    value = kv_match.group(2).strip()
                    item[key] = value
            elif ": " in line and not line.startswith("-"):
                # Simple key: value format
                parts = line.split(": ", 1)
                if len(parts) == 2:
                    key = parts[0].strip().lower().replace(" ", "_")
                    value = parts[1].strip()
                    item[key] = value

        items.append(item)

    return items


def parse_agents_from_state(content: str) -> list[dict[str, Any]]:
    """Parse agents section from state file.

    Args:
        content: Full content of the state file

    Returns:
        List of agent dictionaries
    """
    agents: list[dict[str, Any]] = []

    # Find agents section
    pattern = r"## Agents\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if not match:
        return agents

    agents_section = match.group(1)

    # Parse each agent entry
    # Format: ### session-name or - **Session**: session-name
    agent_pattern = r"### ([^\n]+)\n(.*?)(?=\n### |\n## |\Z)"
    for agent_match in re.finditer(agent_pattern, agents_section, re.DOTALL):
        session = agent_match.group(1).strip()
        body = agent_match.group(2)

        agent: dict[str, Any] = {
            "session": session,
            "role": "unknown",
            "project": None,
            "status": "unknown",
            "heartbeat": None,
        }

        # Parse fields from body
        for line in body.split("\n"):
            line = line.strip()
            if line.startswith("- **"):
                kv_match = re.match(r"- \*\*([^*]+)\*\*:\s*(.+)", line)
                if kv_match:
                    key = kv_match.group(1).strip().lower()
                    value = kv_match.group(2).strip()
                    if key == "role":
                        agent["role"] = value
                    elif key == "project":
                        agent["project"] = value if value.lower() != "none" else None
                    elif key == "status":
                        agent["status"] = value
                    elif key in ("heartbeat", "last_heartbeat", "last heartbeat"):
                        agent["heartbeat"] = value

        agents.append(agent)

    return agents


def filter_agents_by_project(
    agents: list[dict[str, Any]], project_id: str | None
) -> list[dict[str, Any]]:
    """Filter agents by project ID.

    Args:
        agents: List of agent dictionaries
        project_id: Project ID to filter by (None for all agents)

    Returns:
        Filtered list of agents
    """
    if project_id is None:
        return agents

    return [a for a in agents if a.get("project") == project_id]


def main() -> int:
    """Main entry point.

    Returns:
        Exit code: 0 for success, 1 for error
    """
    parser = argparse.ArgumentParser(
        description="Get status of all managed agents"
    )
    parser.add_argument(
        "--project",
        "-p",
        type=str,
        default=None,
        help="Filter agents by project ID",
    )
    parser.add_argument(
        "--cwd",
        type=str,
        default=None,
        help="Working directory (defaults to current directory)",
    )

    args = parser.parse_args()

    state_file = get_state_file_path(args.cwd)

    if not state_file.exists():
        result = {
            "success": False,
            "error": f"State file not found: {state_file}",
            "agents": [],
        }
        print(json.dumps(result, indent=2))
        return 1

    content = read_file_safely(state_file)
    if not content:
        result = {
            "success": False,
            "error": "Failed to read state file or file is empty",
            "agents": [],
        }
        print(json.dumps(result, indent=2))
        return 1

    agents = parse_agents_from_state(content)
    filtered_agents = filter_agents_by_project(agents, args.project)

    result = {
        "success": True,
        "timestamp": datetime.now().isoformat(),
        "filter": {"project": args.project},
        "count": len(filtered_agents),
        "agents": filtered_agents,
    }

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
