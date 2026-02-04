#!/usr/bin/env python3
"""
ecos_add_project.py - Add a project to chief-of-staff management.

Adds a new project entry to the chief-of-staff state file with repository URL,
optional GitHub project board URL, and project ID.

Dependencies: Python 3.8+ stdlib only

Usage:
    ecos_add_project.py REPO_URL --id PROJECT_ID [--github-project BOARD_URL]

Exit codes:
    0 - Success
    1 - Error (file not found, project already exists, write error)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


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


def project_exists(content: str, project_id: str) -> bool:
    """Check if a project already exists in the state file.

    Args:
        content: Full content of the state file
        project_id: Project ID to check

    Returns:
        True if project exists, False otherwise
    """
    pattern = rf"### {re.escape(project_id)}\s*\n"
    return bool(re.search(pattern, content, re.IGNORECASE))


def create_project_entry(
    project_id: str,
    repo_url: str,
    github_project: str | None,
    description: str | None,
) -> str:
    """Create a new project entry in markdown format.

    Args:
        project_id: Unique project identifier
        repo_url: Repository URL
        github_project: Optional GitHub project board URL
        description: Optional project description

    Returns:
        Formatted project entry string
    """
    timestamp = get_timestamp()
    lines = [
        f"### {project_id}",
        f"- **Repo**: {repo_url}",
    ]

    if github_project:
        lines.append(f"- **GitHub Project**: {github_project}")

    if description:
        lines.append(f"- **Description**: {description}")

    lines.extend(
        [
            "- **Status**: active",
            f"- **Created**: {timestamp}",
            "- **Agents**: none",
            "",
        ]
    )

    return "\n".join(lines)


def add_project_to_state(
    content: str,
    project_id: str,
    repo_url: str,
    github_project: str | None,
    description: str | None,
) -> str:
    """Add a project entry to the state file content.

    Args:
        content: Current state file content
        project_id: Unique project identifier
        repo_url: Repository URL
        github_project: Optional GitHub project board URL
        description: Optional project description

    Returns:
        Updated state file content
    """
    project_entry = create_project_entry(
        project_id, repo_url, github_project, description
    )

    # Find the Projects section
    projects_pattern = r"(## Projects\s*\n)"
    match = re.search(projects_pattern, content, re.IGNORECASE)

    if match:
        # Insert after the section header
        insert_pos = match.end()
        # Find if there's content after the header
        rest = content[insert_pos:]
        if rest.strip():
            # There's existing content, add before it
            return content[:insert_pos] + "\n" + project_entry + rest
        else:
            # No content after header
            return content[:insert_pos] + "\n" + project_entry
    else:
        # No Projects section exists, create one
        # Find where to insert (after Agents section or at end)
        agents_pattern = r"(## Agents.*?)(?=\n## |\Z)"
        agents_match = re.search(agents_pattern, content, re.DOTALL | re.IGNORECASE)

        if agents_match:
            insert_pos = agents_match.end()
            projects_section = f"\n\n## Projects\n\n{project_entry}"
            return content[:insert_pos] + projects_section + content[insert_pos:]
        else:
            # Add at the end
            if not content.endswith("\n"):
                content += "\n"
            return content + f"\n## Projects\n\n{project_entry}"


def initialize_state_file(path: Path) -> str:
    """Create initial state file content.

    Args:
        path: Path to the state file

    Returns:
        Initial state file content
    """
    timestamp = get_timestamp()
    content = f"""# Chief of Staff State
**Updated**: {timestamp}

## Agents

_No agents registered yet._

## Projects

_No projects registered yet._
"""
    return content


def main() -> int:
    """Main entry point.

    Returns:
        Exit code: 0 for success, 1 for error
    """
    parser = argparse.ArgumentParser(
        description="Add a project to chief-of-staff management"
    )
    parser.add_argument(
        "repo_url",
        type=str,
        help="Repository URL (e.g., https://github.com/user/repo)",
    )
    parser.add_argument(
        "--id",
        type=str,
        required=True,
        dest="project_id",
        help="Unique project identifier",
    )
    parser.add_argument(
        "--github-project",
        type=str,
        default=None,
        help="GitHub project board URL",
    )
    parser.add_argument(
        "--description",
        "-d",
        type=str,
        default=None,
        help="Project description",
    )
    parser.add_argument(
        "--cwd",
        type=str,
        default=None,
        help="Working directory (defaults to current directory)",
    )

    args = parser.parse_args()

    state_file = get_state_file_path(args.cwd)

    # Read existing content or create new
    if state_file.exists():
        content = read_file_safely(state_file)
        if not content:
            content = initialize_state_file(state_file)
    else:
        content = initialize_state_file(state_file)

    # Check if project already exists
    if project_exists(content, args.project_id):
        result = {
            "success": False,
            "error": f"Project '{args.project_id}' already exists",
            "project": None,
        }
        print(json.dumps(result, indent=2))
        return 1

    # Add the project
    updated_content = add_project_to_state(
        content,
        args.project_id,
        args.repo_url,
        args.github_project,
        args.description,
    )

    # Write back
    if not write_file_safely(state_file, updated_content):
        result = {
            "success": False,
            "error": f"Failed to write state file: {state_file}",
            "project": None,
        }
        print(json.dumps(result, indent=2))
        return 1

    result = {
        "success": True,
        "timestamp": get_timestamp(),
        "project": {
            "id": args.project_id,
            "repo_url": args.repo_url,
            "github_project": args.github_project,
            "description": args.description,
            "status": "active",
        },
    }

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
