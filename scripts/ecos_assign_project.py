#!/usr/bin/env python3
"""
ecos_assign_project.py - Assign an agent to a project.

Updates the chief-of-staff state file to assign an agent session to a project.
Optionally sends an onboarding message via AI Maestro.

Dependencies: Python 3.8+ stdlib only

Usage:
    ecos_assign_project.py SESSION_NAME PROJECT_ID [--unassign]

Exit codes:
    0 - Success
    1 - Error (file not found, agent/project not found, write error)
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


def agent_exists(content: str, session_name: str) -> bool:
    """Check if an agent exists in the state file.

    Args:
        content: Full content of the state file
        session_name: Agent session name

    Returns:
        True if agent exists, False otherwise
    """
    pattern = rf"### {re.escape(session_name)}\s*\n"
    return bool(re.search(pattern, content, re.IGNORECASE))


def project_exists(content: str, project_id: str) -> bool:
    """Check if a project exists in the state file.

    Args:
        content: Full content of the state file
        project_id: Project ID

    Returns:
        True if project exists, False otherwise
    """
    # Find projects section
    pattern = r"## Projects\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if not match:
        return False

    project_pattern = rf"### {re.escape(project_id)}\s*\n"
    return bool(re.search(project_pattern, match.group(1), re.IGNORECASE))


def get_agent_current_project(content: str, session_name: str) -> str | None:
    """Get the current project assigned to an agent.

    Args:
        content: Full content of the state file
        session_name: Agent session name

    Returns:
        Project ID or None if not assigned
    """
    # Find agents section
    pattern = r"## Agents\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if not match:
        return None

    agents_section = match.group(1)

    # Find the specific agent
    agent_pattern = rf"### {re.escape(session_name)}\s*\n(.*?)(?=\n### |\n## |\Z)"
    agent_match = re.search(agent_pattern, agents_section, re.DOTALL | re.IGNORECASE)
    if not agent_match:
        return None

    agent_body = agent_match.group(1)

    # Find project field
    project_match = re.search(r"\*\*Project\*\*:\s*(\S+)", agent_body, re.IGNORECASE)
    if project_match:
        project = project_match.group(1).strip()
        return None if project.lower() == "none" else project

    return None


def update_agent_project(
    content: str, session_name: str, project_id: str | None
) -> str:
    """Update the project assignment for an agent.

    Args:
        content: Current state file content
        session_name: Agent session name
        project_id: Project ID to assign (None to unassign)

    Returns:
        Updated state file content
    """
    # Find agents section
    pattern = r"(## Agents\s*\n)(.*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if not match:
        return content

    agents_section = match.group(2)
    section_start = match.start(2)
    section_end = match.end(2)

    # Find the specific agent block
    agent_pattern = rf"(### {re.escape(session_name)}\s*\n)(.*?)(?=\n### |\n## |\Z)"
    agent_match = re.search(agent_pattern, agents_section, re.DOTALL | re.IGNORECASE)
    if not agent_match:
        return content

    agent_header = agent_match.group(1)
    agent_body = agent_match.group(2)
    agent_start = agent_match.start()
    agent_end = agent_match.end()

    # Update or add project field
    project_value = project_id if project_id else "none"

    if re.search(r"\*\*Project\*\*:", agent_body, re.IGNORECASE):
        # Update existing field
        updated_body = re.sub(
            r"(\*\*Project\*\*:\s*)\S+",
            rf"\g<1>{project_value}",
            agent_body,
            flags=re.IGNORECASE,
        )
    else:
        # Add new field
        lines = agent_body.rstrip().split("\n")
        lines.append(f"- **Project**: {project_value}")
        updated_body = "\n".join(lines) + "\n"

    # Reconstruct agents section
    updated_agents = (
        agents_section[:agent_start]
        + agent_header
        + updated_body
        + agents_section[agent_end:]
    )

    # Reconstruct full content
    updated_content = content[:section_start] + updated_agents + content[section_end:]

    return updated_content


def register_agent_if_missing(content: str, session_name: str) -> str:
    """Register an agent if not already in the state file.

    Args:
        content: Current state file content
        session_name: Agent session name

    Returns:
        Updated state file content with agent registered
    """
    if agent_exists(content, session_name):
        return content

    timestamp = get_timestamp()
    agent_entry = f"""### {session_name}
- **Role**: unknown
- **Status**: registered
- **Project**: none
- **Heartbeat**: {timestamp}

"""

    # Find agents section
    pattern = r"(## Agents\s*\n)"
    match = re.search(pattern, content, re.IGNORECASE)

    if match:
        insert_pos = match.end()
        # Remove placeholder if present
        placeholder = "_No agents registered yet._"
        rest = content[insert_pos:]
        if rest.strip().startswith(placeholder):
            rest = rest.replace(placeholder, "", 1).lstrip()
        return content[:insert_pos] + "\n" + agent_entry + rest
    else:
        # Add agents section at the end
        if not content.endswith("\n"):
            content += "\n"
        return content + f"\n## Agents\n\n{agent_entry}"


def main() -> int:
    """Main entry point.

    Returns:
        Exit code: 0 for success, 1 for error
    """
    parser = argparse.ArgumentParser(description="Assign an agent to a project")
    parser.add_argument(
        "session_name",
        type=str,
        help="Agent session name",
    )
    parser.add_argument(
        "project_id",
        type=str,
        help="Project ID to assign",
    )
    parser.add_argument(
        "--unassign",
        "-u",
        action="store_true",
        help="Unassign agent from project instead of assigning",
    )
    parser.add_argument(
        "--register",
        "-r",
        action="store_true",
        help="Register agent if not already in state file",
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

    # Register agent if requested and missing
    if args.register:
        content = register_agent_if_missing(content, args.session_name)

    # Check if agent exists
    if not agent_exists(content, args.session_name):
        result = {
            "success": False,
            "error": f"Agent '{args.session_name}' not found. Use --register to auto-register.",
        }
        print(json.dumps(result, indent=2))
        return 1

    # Check if project exists (unless unassigning)
    if not args.unassign and not project_exists(content, args.project_id):
        result = {
            "success": False,
            "error": f"Project '{args.project_id}' not found",
        }
        print(json.dumps(result, indent=2))
        return 1

    # Get current assignment
    current_project = get_agent_current_project(content, args.session_name)

    # Determine new assignment
    new_project = None if args.unassign else args.project_id

    # Update the assignment
    updated_content = update_agent_project(content, args.session_name, new_project)

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
        "agent": args.session_name,
        "previous_project": current_project,
        "new_project": new_project,
        "action": "unassigned" if args.unassign else "assigned",
        "todo": "Send onboarding message via AI Maestro" if not args.unassign else None,
    }

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
