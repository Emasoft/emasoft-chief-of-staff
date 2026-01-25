#!/usr/bin/env python3
"""
atlas_memory_operations.py - Core memory file operations for Atlas.

This module provides the core operations for manipulating Atlas memory files:
- Utility functions for file I/O and timestamps
- Active Context operations (decisions, focus, errors)
- Progress log operations
- Pattern discovery operations

Used by atlas_memory_manager.py for CLI interface.
"""

from __future__ import annotations

import re
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from atlas_memory_manager import MemoryConfig

__all__ = [
    "get_timestamp",
    "get_date",
    "ensure_memory_root",
    "read_file_safely",
    "write_file_safely",
    "backup_file",
    "add_decision",
    "set_focus",
    "log_error",
    "clear_errors",
    "get_recent_errors",
    "add_progress",
    "get_progress_entries",
    "add_pattern",
    "search_patterns",
]


# =============================================================================
# Utility Functions
# =============================================================================


def get_timestamp() -> str:
    """Get current timestamp in standard format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def get_date() -> str:
    """Get current date in standard format."""
    return datetime.now().strftime("%Y-%m-%d")


def ensure_memory_root(config: MemoryConfig) -> bool:
    """Ensure memory root directory exists."""
    try:
        config.memory_root.mkdir(parents=True, exist_ok=True)
        return True
    except OSError as e:
        print(f"ERROR: Cannot create memory root: {e}", file=sys.stderr)
        return False


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


def backup_file(path: Path, backup_dir: Path) -> Path | None:
    """Create timestamped backup of a file."""
    if not path.exists():
        return None

    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"{path.stem}_{timestamp}{path.suffix}"

    try:
        shutil.copy2(path, backup_path)
        return backup_path
    except OSError as e:
        print(f"ERROR: Backup failed: {e}", file=sys.stderr)
        return None


# =============================================================================
# Active Context Operations
# =============================================================================


def add_decision(
    config: MemoryConfig, decision_text: str, category: str = "Architecture"
) -> bool:
    """Add a decision to activeContext.md."""
    content = read_file_safely(config.active_context_path)
    timestamp = get_timestamp()

    decision_entry = f"- [{timestamp}] **{category}**: {decision_text}\n"

    if "## Active Decisions" in content:
        pattern = r"(## Active Decisions\s*\n)"
        replacement = rf"\1{decision_entry}"
        new_content = re.sub(pattern, replacement, content, count=1)
    else:
        if "## Current Focus" in content:
            pattern = r"(## Current Focus.*?)(\n## |\Z)"
            match = re.search(pattern, content, re.DOTALL)
            if match:
                insert_pos = match.end(1)
                new_content = (
                    content[:insert_pos]
                    + f"\n\n## Active Decisions\n\n{decision_entry}"
                    + content[insert_pos:]
                )
            else:
                new_content = content + f"\n\n## Active Decisions\n\n{decision_entry}"
        else:
            new_content = f"## Active Decisions\n\n{decision_entry}\n" + content

    if write_file_safely(config.active_context_path, new_content):
        print("ADDED: Decision -> activeContext.md")
        return True
    return False


def set_focus(config: MemoryConfig, focus_text: str) -> bool:
    """Set or update the Current Focus in activeContext.md."""
    content = read_file_safely(config.active_context_path)
    timestamp = get_timestamp()

    focus_section = f"""## Current Focus

**Updated**: {timestamp}

{focus_text}
"""

    if "## Current Focus" in content:
        pattern = r"## Current Focus.*?(?=\n## |\Z)"
        new_content = re.sub(
            pattern, focus_section.rstrip(), content, count=1, flags=re.DOTALL
        )
    else:
        new_content = focus_section + "\n" + content

    if write_file_safely(config.active_context_path, new_content):
        print("UPDATED: Current Focus -> activeContext.md")
        return True
    return False


def log_error(
    config: MemoryConfig,
    step: str,
    agent: str,
    error_text: str,
    impact: str = "NON-BLOCKING",
    context: str = "",
) -> bool:
    """Log an in-flight error to activeContext.md."""
    content = read_file_safely(config.active_context_path)
    timestamp = get_timestamp()

    error_entry = f"""
### In-Flight Error: {timestamp}
- **Step**: {step}
- **Agent**: {agent}
- **Error**: {error_text[:500]}
- **Context**: {context or "N/A"}
- **Impact**: {impact}
"""

    if "## In-Flight Errors" in content:
        pattern = r"(## In-Flight Errors\s*\n)"
        replacement = rf"\1{error_entry}"
        new_content = re.sub(pattern, replacement, content, count=1)
    else:
        new_content = content.rstrip() + f"\n\n## In-Flight Errors\n{error_entry}"

    if write_file_safely(config.active_context_path, new_content):
        print(f"LOGGED: Error ({impact}) -> activeContext.md")
        return True
    return False


def clear_errors(config: MemoryConfig) -> bool:
    """Clear all in-flight errors from activeContext.md."""
    content = read_file_safely(config.active_context_path)

    if "## In-Flight Errors" not in content:
        print("No In-Flight Errors section found")
        return True

    pattern = r"\n## In-Flight Errors.*?(?=\n## |\Z)"
    new_content = re.sub(pattern, "", content, flags=re.DOTALL)

    if write_file_safely(config.active_context_path, new_content.strip() + "\n"):
        print("CLEARED: All In-Flight Errors")
        return True
    return False


def get_recent_errors(config: MemoryConfig, limit: int = 5) -> list[dict[str, str]]:
    """Get recent in-flight errors from activeContext.md."""
    content = read_file_safely(config.active_context_path)
    errors: list[dict[str, str]] = []

    pattern = r"### In-Flight Error: ([^\n]+)\n(.*?)(?=\n### |\n## |\Z)"
    matches = re.findall(pattern, content, re.DOTALL)

    for timestamp, block in matches[:limit]:
        error: dict[str, str] = {"timestamp": timestamp.strip()}

        for line in block.strip().split("\n"):
            if line.startswith("- **"):
                match = re.match(r"- \*\*(\w+)\*\*: (.+)", line)
                if match:
                    key = match.group(1).lower()
                    error[key] = match.group(2)

        errors.append(error)

    return errors


# =============================================================================
# Progress Operations
# =============================================================================


def add_progress(
    config: MemoryConfig,
    text: str,
    category: str = "Progress",
    workflow: str = "",
) -> bool:
    """Add a progress entry to progress.md."""
    content = read_file_safely(config.progress_path)
    timestamp = get_timestamp()
    date = get_date()

    workflow_tag = f"[{workflow}] " if workflow else ""
    entry = f"- [{timestamp}] {workflow_tag}**{category}**: {text}\n"

    date_header = f"## {date}"

    if date_header in content:
        pattern = rf"({re.escape(date_header)}\s*\n)"
        replacement = rf"\1\n{entry}"
        new_content = re.sub(pattern, replacement, content, count=1)
    else:
        if content.startswith("# "):
            title_end = content.find("\n") + 1
            new_content = (
                content[:title_end]
                + f"\n{date_header}\n\n{entry}"
                + content[title_end:]
            )
        else:
            new_content = f"{date_header}\n\n{entry}" + content

    if write_file_safely(config.progress_path, new_content):
        print("ADDED: Progress entry -> progress.md")
        return True
    return False


def get_progress_entries(config: MemoryConfig, days: int = 7) -> list[dict[str, str]]:
    """Get progress entries from the last N days."""
    content = read_file_safely(config.progress_path)
    entries: list[dict[str, str]] = []

    date_pattern = r"## (\d{4}-\d{2}-\d{2})\n(.*?)(?=\n## |\Z)"
    matches = re.findall(date_pattern, content, re.DOTALL)

    cutoff = datetime.now() - timedelta(days=days)

    for date_str, section in matches:
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            if date >= cutoff:
                entry_pattern = r"- \[([^\]]+)\] (.+)"
                for match in re.finditer(entry_pattern, section):
                    entries.append(
                        {
                            "date": date_str,
                            "timestamp": match.group(1),
                            "text": match.group(2),
                        }
                    )
        except ValueError:
            continue

    return entries


# =============================================================================
# Patterns Operations
# =============================================================================


def add_pattern(
    config: MemoryConfig,
    name: str,
    description: str,
    category: str = "General",
) -> bool:
    """Add a pattern to patterns.md."""
    content = read_file_safely(config.patterns_path)
    timestamp = get_timestamp()

    pattern_entry = f"""
### {name}

**Category**: {category}
**Discovered**: {timestamp}

{description}
"""

    category_header = f"## {category}"

    if category_header in content:
        pattern = rf"({re.escape(category_header)}\s*\n)"
        replacement = rf"\1{pattern_entry}"
        new_content = re.sub(pattern, replacement, content, count=1)
    else:
        new_content = content.rstrip() + f"\n\n{category_header}\n{pattern_entry}"

    if write_file_safely(config.patterns_path, new_content):
        print(f"ADDED: Pattern '{name}' -> patterns.md")
        return True
    return False


def search_patterns(config: MemoryConfig, query: str) -> list[dict[str, str]]:
    """Search patterns by name or content."""
    content = read_file_safely(config.patterns_path)
    results: list[dict[str, str]] = []

    pattern = r"### ([^\n]+)\n(.*?)(?=\n### |\n## |\Z)"
    matches = re.findall(pattern, content, re.DOTALL)

    query_lower = query.lower()
    for name, body in matches:
        if query_lower in name.lower() or query_lower in body.lower():
            results.append(
                {
                    "name": name.strip(),
                    "content": body.strip(),
                }
            )

    return results
