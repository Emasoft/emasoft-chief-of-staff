#!/usr/bin/env python3
"""
eama_session_start.py - Load Emasoft Assistant Manager memory context at session start.

SessionStart hook that loads existing Emasoft Assistant Manager memory files and outputs a system
message summarizing the loaded context to help Claude resume work seamlessly.

Memory files loaded:
- activeContext.md: Current focus, active decisions, in-flight errors
- progress.md: Recent progress entries
- patterns.md: Discovered patterns and conventions

Dependencies: Python 3.8+ stdlib only

Usage (as Claude Code hook):
    Receives JSON via stdin from SessionStart hook event.
    Outputs system message to stdout with loaded context summary.

Exit codes:
    0 - Success (context loaded or no context found)
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path


def get_memory_root(cwd: str) -> Path:
    """Get the Emasoft Assistant Manager memory root directory.

    Args:
        cwd: Current working directory

    Returns:
        Path to .claude/eama directory
    """
    return Path(cwd) / ".claude" / "eama"


def read_file_safely(path: Path) -> str:
    """Read file content safely, return empty string if not found."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def extract_current_focus(content: str) -> str | None:
    """Extract current focus from activeContext.md.

    Args:
        content: Full content of activeContext.md

    Returns:
        Current focus text or None if not found
    """
    pattern = r"## Current Focus\s*\n\*\*Updated\*\*: ([^\n]+)\n\n(.+?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        updated = match.group(1).strip()
        focus_text = match.group(2).strip()
        # Skip if it's the default "No active focus set"
        if focus_text != "No active focus set.":
            return f"{focus_text} (updated: {updated})"
    return None


def extract_recent_decisions(content: str, limit: int = 3) -> list[str]:
    """Extract recent decisions from activeContext.md.

    Args:
        content: Full content of activeContext.md
        limit: Maximum number of decisions to return

    Returns:
        List of recent decision strings
    """
    decisions = []
    pattern = r"- \[([^\]]+)\] \*\*(\w+)\*\*: (.+)"
    # Find the Active Decisions section
    section_match = re.search(
        r"## Active Decisions\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL
    )
    if section_match:
        section = section_match.group(1)
        for match in re.finditer(pattern, section):
            category = match.group(2)
            text = match.group(3).strip()
            if text != "No decisions recorded yet.":
                decisions.append(f"[{category}] {text}")
            if len(decisions) >= limit:
                break
    return decisions


def extract_inflight_errors(content: str, limit: int = 3) -> list[dict[str, str]]:
    """Extract in-flight errors from activeContext.md.

    Args:
        content: Full content of activeContext.md
        limit: Maximum number of errors to return

    Returns:
        List of error dictionaries with step, agent, error, impact keys
    """
    errors: list[dict[str, str]] = []
    pattern = r"### In-Flight Error: ([^\n]+)\n(.*?)(?=\n### |\n## |\Z)"
    for match in re.finditer(pattern, content, re.DOTALL):
        if len(errors) >= limit:
            break
        block = match.group(2)
        error: dict[str, str] = {}
        for line in block.strip().split("\n"):
            if line.startswith("- **"):
                field_match = re.match(r"- \*\*(\w+)\*\*: (.+)", line)
                if field_match:
                    key = field_match.group(1).lower()
                    error[key] = field_match.group(2)
        if error:
            errors.append(error)
    return errors


def extract_recent_progress(content: str, days: int = 3, limit: int = 5) -> list[str]:
    """Extract recent progress entries from progress.md.

    Args:
        content: Full content of progress.md
        days: Number of days to look back
        limit: Maximum number of entries to return

    Returns:
        List of recent progress strings
    """
    entries: list[str] = []
    cutoff = datetime.now() - timedelta(days=days)

    date_pattern = r"## (\d{4}-\d{2}-\d{2})\n(.*?)(?=\n## |\Z)"
    for match in re.finditer(date_pattern, content, re.DOTALL):
        try:
            date = datetime.strptime(match.group(1), "%Y-%m-%d")
            if date >= cutoff:
                section = match.group(2)
                entry_pattern = r"- \[([^\]]+)\] (.+)"
                for entry_match in re.finditer(entry_pattern, section):
                    text = entry_match.group(2).strip()
                    if text and len(entries) < limit:
                        entries.append(text)
        except ValueError:
            continue
    return entries


def extract_key_patterns(content: str, limit: int = 3) -> list[str]:
    """Extract key pattern names from patterns.md.

    Args:
        content: Full content of patterns.md
        limit: Maximum number of patterns to return

    Returns:
        List of pattern names
    """
    patterns: list[str] = []
    pattern = r"### ([^\n]+)"
    for match in re.finditer(pattern, content):
        name = match.group(1).strip()
        if name and len(patterns) < limit:
            patterns.append(name)
    return patterns


def format_context_summary(
    focus: str | None,
    decisions: list[str],
    errors: list[dict[str, str]],
    progress: list[str],
    patterns: list[str],
) -> str:
    """Format loaded context into a system message summary.

    Args:
        focus: Current focus text or None
        decisions: List of recent decisions
        errors: List of in-flight error dicts
        progress: List of recent progress entries
        patterns: List of pattern names

    Returns:
        Formatted summary string for system message
    """
    lines = []
    lines.append("=" * 60)
    lines.append("EMASOFT ASSISTANT MANAGER MEMORY CONTEXT LOADED")
    lines.append("=" * 60)

    if focus:
        lines.append("")
        lines.append("CURRENT FOCUS:")
        lines.append(f"  {focus}")

    if decisions:
        lines.append("")
        lines.append("RECENT DECISIONS:")
        for d in decisions:
            lines.append(f"  - {d}")

    if errors:
        lines.append("")
        lines.append("IN-FLIGHT ERRORS (unresolved):")
        for e in errors:
            step = e.get("step", "?")
            agent = e.get("agent", "?")
            error_text = e.get("error", "?")[:100]
            impact = e.get("impact", "?")
            lines.append(f"  [{impact}] {step}/{agent}: {error_text}")

    if progress:
        lines.append("")
        lines.append("RECENT PROGRESS (last 3 days):")
        for p in progress[:3]:
            lines.append(f"  - {p[:80]}...")

    if patterns:
        lines.append("")
        lines.append(f"KNOWN PATTERNS: {', '.join(patterns)}")

    lines.append("")
    lines.append("=" * 60)
    lines.append("Review .claude/eama/ files for full context")
    lines.append("=" * 60)

    return "\n".join(lines)


def main() -> int:
    """Main entry point for SessionStart hook.

    Reads session info from stdin, loads Emasoft Assistant Manager memory files,
    and outputs a context summary to stdout.

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
    memory_root = get_memory_root(cwd)

    # Check if memory directory exists
    if not memory_root.exists():
        # No Emasoft Assistant Manager memory initialized - exit silently
        return 0

    # Load memory files
    active_context = read_file_safely(memory_root / "activeContext.md")
    progress_content = read_file_safely(memory_root / "progress.md")
    patterns_content = read_file_safely(memory_root / "patterns.md")

    # Check if any memory exists
    if not any([active_context, progress_content, patterns_content]):
        return 0

    # Extract key information from each file
    focus = extract_current_focus(active_context) if active_context else None
    decisions = extract_recent_decisions(active_context) if active_context else []
    errors = extract_inflight_errors(active_context) if active_context else []
    progress = extract_recent_progress(progress_content) if progress_content else []
    patterns = extract_key_patterns(patterns_content) if patterns_content else []

    # Only output if there's something meaningful to show
    if any([focus, decisions, errors, progress, patterns]):
        summary = format_context_summary(focus, decisions, errors, progress, patterns)
        print(summary)

    return 0


if __name__ == "__main__":
    sys.exit(main())
