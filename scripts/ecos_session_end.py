#!/usr/bin/env python3
"""
ecos_session_end.py - Save Chief of Staff state on session end.

SessionEnd hook that saves/updates the Chief of Staff state file to preserve
context for future sessions.

State file: .claude/chief-of-staff-state.local.md

Dependencies: Python 3.8+ stdlib only

Usage (as Claude Code hook):
    Receives JSON via stdin from SessionEnd hook event.
    Updates state file with last_updated timestamp and session end entry.

Exit codes:
    0 - Success (state saved)
"""

from __future__ import annotations

import json
import os
import re
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


def create_default_state() -> str:
    """Create default state file content.

    Returns:
        Default state file content as markdown
    """
    timestamp = get_timestamp()
    return f"""# Chief of Staff State

**Last Updated**: {timestamp}
**Session Count**: 0

## Active Agents

| Agent | Role | Status | Last Heartbeat |
|-------|------|--------|----------------|
| _No agents registered_ | - | - | - |

## Pending Tasks

- No pending tasks

## Resource Alerts

- None

## Session History

"""


def update_timestamp(content: str) -> str:
    """Update the last_updated timestamp in state file.

    Args:
        content: State file content

    Returns:
        Updated content with new timestamp
    """
    timestamp = get_timestamp()
    return re.sub(
        r"\*\*Last Updated\*\*:\s*[^\n]+",
        f"**Last Updated**: {timestamp}",
        content
    )


def add_session_end_entry(content: str, session_id: str) -> str:
    """Add a session end entry to the session history.

    Args:
        content: State file content
        session_id: Session identifier (if available)

    Returns:
        Updated content with session end entry
    """
    timestamp = get_timestamp()
    session_short = session_id[:8] if session_id else "unknown"

    # Find Session History section
    history_marker = "## Session History"
    if history_marker in content:
        # Insert entry after the header
        idx = content.find(history_marker)
        header_end = content.find("\n", idx) + 1

        # Find next section or end of file
        next_section = content.find("\n## ", header_end)
        if next_section == -1:
            next_section = len(content)

        # Get existing history
        existing_history = content[header_end:next_section].strip()

        # Create new entry
        new_entry = f"\n### {timestamp}\n- Session {session_short} ended\n"

        # Combine
        if existing_history:
            new_history = new_entry + "\n" + existing_history
        else:
            new_history = new_entry

        content = (
            content[:header_end] +
            new_history + "\n" +
            content[next_section:]
        )
    else:
        # Add Session History section at the end
        content = content.rstrip() + f"\n\n## Session History\n\n### {timestamp}\n- Session {session_short} ended\n"

    return content


def clear_stale_alerts(content: str) -> str:
    """Clear any stale resource alerts from previous session.

    This is done at session end to ensure fresh alerts on next start.

    Args:
        content: State file content

    Returns:
        Updated content with cleared alerts
    """
    # Find Resource Alerts section
    alerts_marker = "## Resource Alerts"
    if alerts_marker in content:
        idx = content.find(alerts_marker)
        header_end = content.find("\n", idx) + 1

        # Find next section
        next_section = content.find("\n## ", header_end)
        if next_section == -1:
            next_section = len(content)

        # Replace with "None"
        content = (
            content[:header_end] +
            "\n- None\n" +
            content[next_section:]
        )

    return content


def update_agent_statuses(content: str) -> str:
    """Mark all agents as 'session_ended' at session end.

    Args:
        content: State file content

    Returns:
        Updated content with agent statuses updated
    """
    # Find Active Agents section
    agents_marker = "## Active Agents"
    if agents_marker not in content:
        return content

    idx = content.find(agents_marker)
    header_end = content.find("\n", idx) + 1

    # Find next section
    next_section = content.find("\n## ", header_end)
    if next_section == -1:
        next_section = len(content)

    # Get the agents table section
    agents_section = content[header_end:next_section]

    # Replace 'active' with 'session_ended' in the status column
    lines = agents_section.split("\n")
    updated_lines = []
    for line in lines:
        if line.startswith("|") and "active" in line.lower():
            # This is a data row, update status
            parts = line.split("|")
            if len(parts) >= 4:
                # Status is typically the 3rd column (index 3)
                if "active" in parts[3].lower():
                    parts[3] = " session_ended "
                line = "|".join(parts)
        updated_lines.append(line)

    updated_section = "\n".join(updated_lines)
    content = content[:header_end] + updated_section + content[next_section:]

    return content


def main() -> int:
    """Main entry point for SessionEnd hook.

    Reads session context from stdin, updates Chief of Staff state file.

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

    # Get working directory from input or environment
    cwd = hook_input.get("cwd", os.getcwd())
    state_file = get_state_file(cwd)

    # Read existing state or create default
    if state_file.exists():
        content = read_file_safely(state_file)
        if not content:
            content = create_default_state()
    else:
        content = create_default_state()

    # Get session ID if available
    session_id = hook_input.get("session_id", hook_input.get("sessionId", ""))

    # Update state file
    content = update_timestamp(content)
    content = add_session_end_entry(content, session_id)
    content = clear_stale_alerts(content)
    content = update_agent_statuses(content)

    # Save updated state
    if write_file_safely(state_file, content):
        print(f"Chief of Staff state saved to {state_file}")
    else:
        print("WARNING: Failed to save Chief of Staff state", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
