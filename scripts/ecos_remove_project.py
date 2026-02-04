#!/usr/bin/env python3
"""
ecos_remove_project.py - Remove a project from chief-of-staff management.

Removes a project entry from the chief-of-staff state file. By default, refuses
to remove projects with active agents assigned unless --force is specified.

Dependencies: Python 3.8+ stdlib only

Usage:
    ecos_remove_project.py PROJECT_ID [--force]

Exit codes:
    0 - Success
    1 - Error (file not found, project not found, agents assigned)
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


def write_file_safely(path: Path, content: str) -> bool:
    """Write content to file safely.

    Args:
        path: Path to write to
        content: Content to write

    Returns:
        True if successful, False otherwise
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return True
    except OSError:
        return False


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def get_project_info(content: str, project_id: str) -> dict[str, Any] | None:
    """Get project information from the state file.

    Args:
        content: Full content of the state file
        project_id: Project ID to look up

    Returns:
        Project info dictionary or None if not found
    """
    # Find projects section
    pattern = r"## Projects\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if not match:
        return None

    projects_section = match.group(1)

    # Find specific project
    project_pattern = rf"### {re.escape(project_id)}\s*\n(.*?)(?=\n### |\n## |\Z)"
    project_match = re.search(
        project_pattern, projects_section, re.DOTALL | re.IGNORECASE
    )
    if not project_match:
        return None

    body = project_match.group(1)
    project: dict[str, Any] = {
        "id": project_id,
        "repo_url": None,
        "github_project": None,
        "status": "active",
    }

    # Parse fields from body
    for line in body.split("\n"):
        line = line.strip()
        if line.startswith("- **"):
            kv_match = re.match(r"- \*\*([^*]+)\*\*:\s*(.+)", line)
            if kv_match:
                key = kv_match.group(1).strip().lower().replace(" ", "_")
                value = kv_match.group(2).strip()

                if key in ("repo", "repo_url", "repository"):
                    project["repo_url"] = value
                elif key in ("github_project", "project_board", "board"):
                    project["github_project"] = value
                elif key == "status":
                    project["status"] = value

    return project


def get_agents_for_project(content: str, project_id: str) -> list[str]:
    """Get list of agents assigned to a project.

    Args:
        content: Full content of the state file
        project_id: Project ID to check

    Returns:
        List of agent session names assigned to the project
    """
    agents: list[str] = []

    # Find agents section
    pattern = r"## Agents\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if not match:
        return agents

    agents_section = match.group(1)

    # Parse each agent
    current_agent: str | None = None
    for line in agents_section.split("\n"):
        if line.startswith("### "):
            current_agent = line[4:].strip()
        elif current_agent and "**Project**:" in line:
            kv_match = re.search(r"\*\*Project\*\*:\s*(\S+)", line, re.IGNORECASE)
            if kv_match:
                assigned_project = kv_match.group(1).strip()
                if assigned_project.lower() == project_id.lower():
                    agents.append(current_agent)

    return agents


def remove_project_from_state(content: str, project_id: str) -> str:
    """Remove a project entry from the state file content.

    Args:
        content: Current state file content
        project_id: Project ID to remove

    Returns:
        Updated state file content
    """
    # Find and remove the project entry from the ## Projects section
    # First find projects section
    projects_pattern = r"(## Projects\s*\n)(.*?)(?=\n## |\Z)"
    projects_match = re.search(projects_pattern, content, re.DOTALL | re.IGNORECASE)

    if not projects_match:
        return content

    projects_section = projects_match.group(2)

    # Remove the project from the section
    updated_section = re.sub(
        rf"### {re.escape(project_id)}\s*\n.*?(?=\n### |\Z)",
        "",
        projects_section,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # Clean up extra newlines
    updated_section = re.sub(r"\n{3,}", "\n\n", updated_section)

    # If section is now empty, add placeholder
    if (
        not updated_section.strip()
        or updated_section.strip() == "_No projects registered yet._"
    ):
        updated_section = "\n_No projects registered yet._\n"

    # Reconstruct content
    start = projects_match.start(2)
    end = projects_match.end(2)
    updated_content = content[:start] + updated_section + content[end:]

    return updated_content


def main() -> int:
    """Main entry point.

    Returns:
        Exit code: 0 for success, 1 for error
    """
    parser = argparse.ArgumentParser(
        description="Remove a project from chief-of-staff management"
    )
    parser.add_argument(
        "project_id",
        type=str,
        help="Project ID to remove",
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Force removal even if agents are assigned",
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
        }
        print(json.dumps(result, indent=2))
        return 1

    content = read_file_safely(state_file)
    if not content:
        result = {
            "success": False,
            "error": "Failed to read state file or file is empty",
        }
        print(json.dumps(result, indent=2))
        return 1

    # Check if project exists
    project_info = get_project_info(content, args.project_id)
    if not project_info:
        result = {
            "success": False,
            "error": f"Project '{args.project_id}' not found",
        }
        print(json.dumps(result, indent=2))
        return 1

    # Check for assigned agents
    assigned_agents = get_agents_for_project(content, args.project_id)
    if assigned_agents and not args.force:
        result = {
            "success": False,
            "error": f"Project has {len(assigned_agents)} agent(s) assigned. Use --force to override.",
            "assigned_agents": assigned_agents,
        }
        print(json.dumps(result, indent=2))
        return 1

    # Remove the project
    updated_content = remove_project_from_state(content, args.project_id)

    # Write back
    if not write_file_safely(state_file, updated_content):
        result = {
            "success": False,
            "error": f"Failed to write state file: {state_file}",
        }
        print(json.dumps(result, indent=2))
        return 1

    result = {
        "success": True,
        "timestamp": get_timestamp(),
        "removed_project": project_info,
        "force": args.force,
        "unassigned_agents": assigned_agents if args.force and assigned_agents else [],
    }

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
