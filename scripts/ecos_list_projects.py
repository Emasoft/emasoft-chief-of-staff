#!/usr/bin/env python3
"""
ecos_list_projects.py - List all managed projects.

Reads the chief-of-staff state file and outputs JSON with project information
including project ID, repository URL, GitHub project board, and assigned agents.

Dependencies: Python 3.8+ stdlib only

Usage:
    ecos_list_projects.py [--verbose]

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


def parse_projects_from_state(content: str) -> list[dict[str, Any]]:
    """Parse projects section from state file.

    Args:
        content: Full content of the state file

    Returns:
        List of project dictionaries
    """
    projects: list[dict[str, Any]] = []

    # Find projects section
    pattern = r"## Projects\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if not match:
        return projects

    projects_section = match.group(1)

    # Parse each project entry
    project_pattern = r"### ([^\n]+)\n(.*?)(?=\n### |\n## |\Z)"
    for project_match in re.finditer(project_pattern, projects_section, re.DOTALL):
        project_id = project_match.group(1).strip()
        body = project_match.group(2)

        project: dict[str, Any] = {
            "id": project_id,
            "repo_url": None,
            "github_project": None,
            "description": None,
            "status": "active",
            "assigned_agents": [],
            "created": None,
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
                    elif key == "description":
                        project["description"] = value
                    elif key == "status":
                        project["status"] = value
                    elif key == "created":
                        project["created"] = value
                    elif key in ("agents", "assigned_agents"):
                        # Parse comma-separated agent list
                        if value.lower() != "none":
                            project["assigned_agents"] = [
                                a.strip() for a in value.split(",") if a.strip()
                            ]

        projects.append(project)

    return projects


def count_agents_per_project(content: str) -> dict[str, int]:
    """Count agents assigned to each project.

    Args:
        content: Full content of the state file

    Returns:
        Dictionary mapping project ID to agent count
    """
    counts: dict[str, int] = {}

    # Find agents section
    pattern = r"## Agents\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if not match:
        return counts

    agents_section = match.group(1)

    # Parse each agent's project
    for line in agents_section.split("\n"):
        if "**Project**:" in line or "**project**:" in line:
            kv_match = re.search(r"\*\*[Pp]roject\*\*:\s*(\S+)", line)
            if kv_match:
                project_id = kv_match.group(1).strip()
                if project_id.lower() != "none":
                    counts[project_id] = counts.get(project_id, 0) + 1

    return counts


def main() -> int:
    """Main entry point.

    Returns:
        Exit code: 0 for success, 1 for error
    """
    parser = argparse.ArgumentParser(
        description="List all managed projects"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Include additional project details",
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
            "projects": [],
        }
        print(json.dumps(result, indent=2))
        return 1

    content = read_file_safely(state_file)
    if not content:
        result = {
            "success": False,
            "error": "Failed to read state file or file is empty",
            "projects": [],
        }
        print(json.dumps(result, indent=2))
        return 1

    projects = parse_projects_from_state(content)
    agent_counts = count_agents_per_project(content)

    # Add agent counts to projects
    for project in projects:
        project["agent_count"] = agent_counts.get(project["id"], 0)

    # If not verbose, simplify output
    if not args.verbose:
        projects = [
            {
                "id": p["id"],
                "repo_url": p["repo_url"],
                "status": p["status"],
                "agent_count": p["agent_count"],
            }
            for p in projects
        ]

    result = {
        "success": True,
        "timestamp": datetime.now().isoformat(),
        "count": len(projects),
        "projects": projects,
    }

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
