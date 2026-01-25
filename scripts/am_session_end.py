#!/usr/bin/env python3
"""
atlas_session_end.py - Save Atlas memory context at session end.

SessionEnd hook that saves/updates Atlas memory files to preserve context
for future sessions.

Memory files managed:
- activeContext.md: Current focus, active decisions, in-flight errors
- progress.md: Session progress entries
- patterns.md: Discovered patterns and conventions

Dependencies: Python 3.8+ stdlib only

Usage (as Claude Code hook):
    Receives JSON via stdin from SessionEnd hook event.
    Updates .claude/atlas/ memory files with session context.

Exit codes:
    0 - Success (memory saved)
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def get_memory_root(cwd: str) -> Path:
    """Get the Atlas memory root directory.

    Args:
        cwd: Current working directory

    Returns:
        Path to .claude/atlas directory
    """
    return Path(cwd) / ".claude" / "atlas"


def get_timestamp() -> str:
    """Get current timestamp in standard format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def get_date() -> str:
    """Get current date in standard format."""
    return datetime.now().strftime("%Y-%m-%d")


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


def ensure_memory_files(memory_root: Path) -> bool:
    """Ensure all memory files exist with default structure.

    Args:
        memory_root: Path to .claude/atlas directory

    Returns:
        True if successful, False otherwise
    """
    try:
        memory_root.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"ERROR: Cannot create memory directory: {e}", file=sys.stderr)
        return False

    timestamp = get_timestamp()
    date = get_date()

    # Create activeContext.md if missing
    active_path = memory_root / "activeContext.md"
    if not active_path.exists():
        active_template = f"""# Active Context

## Current Focus

**Updated**: {timestamp}

No active focus set.

## Active Decisions

- No decisions recorded yet.

## In-Flight Errors

No errors recorded.
"""
        if not write_file_safely(active_path, active_template):
            return False

    # Create progress.md if missing
    progress_path = memory_root / "progress.md"
    if not progress_path.exists():
        progress_template = f"""# Progress Log

## {date}

- [{timestamp}] **System**: Session memory initialized
"""
        if not write_file_safely(progress_path, progress_template):
            return False

    # Create patterns.md if missing
    patterns_path = memory_root / "patterns.md"
    if not patterns_path.exists():
        patterns_template = """# Patterns & Conventions

## General

### Memory Update Pattern

**Category**: General
**Discovered**: System initialization

Always update activeContext.md after significant decisions.
Always log errors immediately to In-Flight Errors section.
"""
        if not write_file_safely(patterns_path, patterns_template):
            return False

    return True


def add_session_end_progress(memory_root: Path, session_context: dict) -> bool:
    """Add a session end entry to progress.md.

    Args:
        memory_root: Path to .claude/atlas directory
        session_context: Session context from hook input

    Returns:
        True if successful
    """
    progress_path = memory_root / "progress.md"
    content = read_file_safely(progress_path)

    timestamp = get_timestamp()
    date = get_date()
    date_header = f"## {date}"

    # Build session summary
    session_id = session_context.get("session_id", "unknown")[:8]
    entry = f"- [{timestamp}] **Session**: Session {session_id} ended\n"

    # Insert entry under today's date
    if date_header in content:
        # Find the date header and insert after it
        idx = content.find(date_header)
        header_end = content.find("\n", idx) + 1
        new_content = content[:header_end] + "\n" + entry + content[header_end:]
    else:
        # Add new date section at the top (after title)
        if content.startswith("# "):
            title_end = content.find("\n") + 1
            new_content = (
                content[:title_end]
                + f"\n{date_header}\n\n{entry}"
                + content[title_end:]
            )
        else:
            new_content = f"{date_header}\n\n{entry}" + content

    return write_file_safely(progress_path, new_content)


def update_session_end_marker(memory_root: Path) -> bool:
    """Update session end marker in activeContext.md.

    This helps track when the last session ended and ensures
    continuity checks work properly.

    Args:
        memory_root: Path to .claude/atlas directory

    Returns:
        True if successful
    """
    active_path = memory_root / "activeContext.md"
    content = read_file_safely(active_path)

    if not content:
        return True  # No content to update

    timestamp = get_timestamp()

    # Check if there's a session marker section
    session_marker = f"\n## Last Session\n\n**Ended**: {timestamp}\n"

    if "## Last Session" in content:
        # Update existing marker
        import re
        pattern = r"## Last Session\s*\n\*\*Ended\*\*: [^\n]+"
        new_content = re.sub(
            pattern,
            f"## Last Session\n\n**Ended**: {timestamp}",
            content,
            count=1
        )
    else:
        # Add marker at the end
        new_content = content.rstrip() + session_marker

    return write_file_safely(active_path, new_content)


def main() -> int:
    """Main entry point for SessionEnd hook.

    Reads session context from stdin, creates/updates Atlas memory files.

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
    memory_root = get_memory_root(cwd)

    # Ensure memory files exist (create if needed)
    if not ensure_memory_files(memory_root):
        # Failed to create memory structure - exit silently
        return 0

    # Add session end progress entry
    add_session_end_progress(memory_root, hook_input)

    # Update session end marker
    update_session_end_marker(memory_root)

    # Output confirmation (will be shown in verbose mode)
    print(f"Atlas memory saved to {memory_root}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
