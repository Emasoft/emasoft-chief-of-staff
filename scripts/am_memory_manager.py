#!/usr/bin/env python3
"""
am_memory_manager.py - Automated Memory File Management for Assistant Manager.

Automates updates to Assistant Manager memory files (activeContext.md, progress.md, patterns.md).
Dependencies: Python 3.8+ stdlib only
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path

from am_memory_operations import (
    add_decision,
    add_pattern,
    add_progress,
    backup_file,
    clear_errors,
    ensure_memory_root,
    get_date,
    get_recent_errors,
    get_timestamp,
    log_error,
    read_file_safely,
    search_patterns,
    set_focus,
    write_file_safely,
)


@dataclass
class MemoryConfig:
    """Configuration for memory file locations."""

    memory_root: Path = field(default_factory=lambda: Path(".claude/am"))
    active_context_file: str = "activeContext.md"
    progress_file: str = "progress.md"
    patterns_file: str = "patterns.md"
    backup_dir: str = "backups"
    max_entries_before_compact: int = 200
    keep_entries_on_compact: int = 100

    @property
    def active_context_path(self) -> Path:
        return self.memory_root / self.active_context_file

    @property
    def progress_path(self) -> Path:
        return self.memory_root / self.progress_file

    @property
    def patterns_path(self) -> Path:
        return self.memory_root / self.patterns_file

    @property
    def backup_path(self) -> Path:
        return self.memory_root / self.backup_dir


@dataclass
class MemoryHealth:
    """Health status of memory files."""

    active_context_exists: bool = False
    progress_exists: bool = False
    patterns_exists: bool = False
    active_context_size_kb: float = 0.0
    progress_size_kb: float = 0.0
    patterns_size_kb: float = 0.0
    active_context_entries: int = 0
    progress_entries: int = 0
    patterns_entries: int = 0
    needs_compact: bool = False
    issues: list[str] = field(default_factory=list)


def compact_memory(
    config: MemoryConfig, keep_entries: int = 100, backup: bool = True
) -> dict[str, dict[str, int]]:
    """Compact memory files by archiving old entries."""
    results: dict[str, dict[str, int]] = {
        "active_context": {"before": 0, "after": 0, "archived": 0},
        "progress": {"before": 0, "after": 0, "archived": 0},
    }
    if backup:
        backup_file(config.active_context_path, config.backup_path)
        backup_file(config.progress_path, config.backup_path)

    progress_content = read_file_safely(config.progress_path)
    if progress_content:
        date_pattern = r"## (\d{4}-\d{2}-\d{2})\n(.*?)(?=\n## |\Z)"
        matches = list(re.finditer(date_pattern, progress_content, re.DOTALL))
        results["progress"]["before"] = len(matches)
        days_to_keep = max(7, keep_entries // 10)
        cutoff = datetime.now() - timedelta(days=days_to_keep)
        new_sections = []
        for match in matches:
            try:
                date = datetime.strptime(match.group(1), "%Y-%m-%d")
                if date >= cutoff:
                    new_sections.append(match.group(0))
            except ValueError:
                continue
        results["progress"]["after"] = len(new_sections)
        results["progress"]["archived"] = (
            results["progress"]["before"] - results["progress"]["after"]
        )
        if new_sections:
            header = ""
            if progress_content.startswith("# "):
                header = progress_content[: progress_content.find("\n") + 1] + "\n"
            write_file_safely(config.progress_path, header + "\n".join(new_sections))

    active_content = read_file_safely(config.active_context_path)
    if active_content and "## In-Flight Errors" in active_content:
        error_pattern = r"### In-Flight Error: ([^\n]+)\n(.*?)(?=\n### |\n## |\Z)"
        matches = list(re.finditer(error_pattern, active_content, re.DOTALL))
        results["active_context"]["before"] = len(matches)
        if len(matches) > 10:
            errors_to_keep = matches[:10]
            if errors_to_keep:
                last_keep_end = errors_to_keep[-1].end()
                next_section = re.search(
                    r"\n## (?!In-Flight)", active_content[last_keep_end:]
                )
                if next_section:
                    new_content = (
                        active_content[:last_keep_end]
                        + active_content[last_keep_end + next_section.start() :]
                    )
                else:
                    new_content = active_content[:last_keep_end]
                results["active_context"]["after"] = 10
                results["active_context"]["archived"] = len(matches) - 10
                write_file_safely(config.active_context_path, new_content)
        else:
            results["active_context"]["after"] = len(matches)
    return results


def validate_memory(config: MemoryConfig) -> tuple[bool, list[str]]:
    """Validate memory file structure."""
    issues: list[str] = []
    if not config.memory_root.exists():
        issues.append(f"Memory root does not exist: {config.memory_root}")
        return False, issues
    if config.active_context_path.exists():
        content = read_file_safely(config.active_context_path)
        if "## Current Focus" not in content:
            issues.append("activeContext.md missing '## Current Focus' section")
        if "## Active Decisions" not in content:
            issues.append("activeContext.md missing '## Active Decisions' section")
    else:
        issues.append(f"activeContext.md not found at {config.active_context_path}")
    if not config.progress_path.exists():
        issues.append(f"progress.md not found at {config.progress_path}")
    if not config.patterns_path.exists():
        issues.append(f"patterns.md not found at {config.patterns_path}")
    return len(issues) == 0, issues


def get_memory_health(config: MemoryConfig) -> MemoryHealth:
    """Get health status of memory files."""
    health = MemoryHealth()
    for name, path in [
        ("active_context", config.active_context_path),
        ("progress", config.progress_path),
        ("patterns", config.patterns_path),
    ]:
        if path.exists():
            setattr(health, f"{name}_exists", True)
            setattr(health, f"{name}_size_kb", path.stat().st_size / 1024)
            content = read_file_safely(path)
            if name == "active_context":
                health.active_context_entries = content.count("### In-Flight Error")
            elif name == "progress":
                health.progress_entries = content.count("## 20")
            elif name == "patterns":
                health.patterns_entries = content.count("### ")
    if health.active_context_size_kb > 50 or health.progress_size_kb > 100:
        health.needs_compact = True
        health.issues.append("Memory files are large, consider running compact")
    valid, issues = validate_memory(config)
    health.issues.extend(issues)
    return health


def initialize_memory(config: MemoryConfig) -> bool:
    """Initialize memory files with default structure."""
    if not ensure_memory_root(config):
        return False
    if not config.active_context_path.exists():
        active_template = f"""# Active Context

## Current Focus

**Updated**: {get_timestamp()}

No active focus set.

## Active Decisions

- No decisions recorded yet.

## In-Flight Errors

No errors recorded.
"""
        write_file_safely(config.active_context_path, active_template)
        print(f"CREATED: {config.active_context_path}")
    if not config.progress_path.exists():
        progress_template = f"""# Progress Log

## {get_date()}

- [{get_timestamp()}] **System**: Memory initialized
"""
        write_file_safely(config.progress_path, progress_template)
        print(f"CREATED: {config.progress_path}")
    if not config.patterns_path.exists():
        patterns_template = """# Patterns & Conventions

## General

### Memory Update Pattern

**Category**: General
**Discovered**: System initialization

Always update activeContext.md after significant decisions.
Always log errors immediately to In-Flight Errors.
"""
        write_file_safely(config.patterns_path, patterns_template)
        print(f"CREATED: {config.patterns_path}")
    return True


def _create_parser() -> argparse.ArgumentParser:
    """Create argument parser for CLI."""
    parser = argparse.ArgumentParser(description="Assistant Manager Memory File Management")
    parser.add_argument("--memory-root", type=Path, default=Path(".claude/am"))
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add-decision", help="Add decision")
    p.add_argument("--text", "-t", required=True)
    p.add_argument("--category", "-c", default="Architecture")

    p = sub.add_parser("set-focus", help="Set focus")
    p.add_argument("--text", "-t", required=True)

    p = sub.add_parser("log-error", help="Log error")
    p.add_argument("--step", "-s", required=True)
    p.add_argument("--agent", "-a", required=True)
    p.add_argument("--error", "-e", required=True)
    p.add_argument(
        "--impact", "-i", default="NON-BLOCKING", choices=["BLOCKING", "NON-BLOCKING"]
    )
    p.add_argument("--context", "-c", default="")

    sub.add_parser("clear-errors", help="Clear errors")

    p = sub.add_parser("get-errors", help="Get errors")
    p.add_argument("--limit", "-l", type=int, default=5)
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("add-progress", help="Add progress")
    p.add_argument("--text", "-t", required=True)
    p.add_argument("--category", "-c", default="Progress")
    p.add_argument("--workflow", "-w", default="")

    p = sub.add_parser("add-pattern", help="Add pattern")
    p.add_argument("--name", "-n", required=True)
    p.add_argument("--text", "-t", required=True)
    p.add_argument("--category", "-c", default="General")

    p = sub.add_parser("search-patterns", help="Search patterns")
    p.add_argument("--query", "-q", required=True)
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("compact", help="Compact files")
    p.add_argument("--keep-entries", "-k", type=int, default=100)
    p.add_argument("--no-backup", action="store_true")

    sub.add_parser("validate", help="Validate structure")

    p = sub.add_parser("health", help="Health report")
    p.add_argument("--json", action="store_true")

    sub.add_parser("init", help="Initialize memory")

    return parser


def _print_health(health: MemoryHealth, as_json: bool) -> None:
    """Print health report."""
    if as_json:
        print(
            json.dumps(
                {
                    "files": {
                        "activeContext": {
                            "exists": health.active_context_exists,
                            "size_kb": health.active_context_size_kb,
                            "entries": health.active_context_entries,
                        },
                        "progress": {
                            "exists": health.progress_exists,
                            "size_kb": health.progress_size_kb,
                            "entries": health.progress_entries,
                        },
                        "patterns": {
                            "exists": health.patterns_exists,
                            "size_kb": health.patterns_size_kb,
                            "entries": health.patterns_entries,
                        },
                    },
                    "needs_compact": health.needs_compact,
                    "issues": health.issues,
                },
                indent=2,
            )
        )
    else:
        print("Memory Health Report\n" + "=" * 40)
        for name, exists, size, entries in [
            (
                "activeContext.md",
                health.active_context_exists,
                health.active_context_size_kb,
                health.active_context_entries,
            ),
            (
                "progress.md     ",
                health.progress_exists,
                health.progress_size_kb,
                health.progress_entries,
            ),
            (
                "patterns.md     ",
                health.patterns_exists,
                health.patterns_size_kb,
                health.patterns_entries,
            ),
        ]:
            status = "OK" if exists else "MISSING"
            print(f"{name}: {status} ({size:.1f} KB, {entries} entries)")
        if health.needs_compact:
            print("\nWARNING: Compact recommended")
        if health.issues:
            print("Issues:" + "".join(f"\n  - {i}" for i in health.issues))


def main() -> int:
    """Main entry point."""
    args = _create_parser().parse_args()
    config = MemoryConfig(memory_root=args.memory_root)

    if args.command == "add-decision":
        return 0 if add_decision(config, args.text, args.category) else 1
    if args.command == "set-focus":
        return 0 if set_focus(config, args.text) else 1
    if args.command == "log-error":
        return (
            0
            if log_error(
                config, args.step, args.agent, args.error, args.impact, args.context
            )
            else 1
        )
    if args.command == "clear-errors":
        return 0 if clear_errors(config) else 1
    if args.command == "get-errors":
        errors = get_recent_errors(config, args.limit)
        if args.json:
            print(json.dumps(errors, indent=2))
        elif not errors:
            print("No in-flight errors")
        else:
            for e in errors:
                print(
                    f"[{e.get('timestamp', '?')}] {e.get('step', '?')}/{e.get('agent', '?')}: {e.get('error', '?')}"
                )
        return 0
    if args.command == "add-progress":
        return 0 if add_progress(config, args.text, args.category, args.workflow) else 1
    if args.command == "add-pattern":
        return 0 if add_pattern(config, args.name, args.text, args.category) else 1
    if args.command == "search-patterns":
        results = search_patterns(config, args.query)
        if args.json:
            print(json.dumps(results, indent=2))
        elif not results:
            print("No patterns found")
        else:
            for r in results:
                print(f"### {r['name']}\n{r['content'][:200]}...\n")
        return 0
    if args.command == "compact":
        res = compact_memory(config, args.keep_entries, backup=not args.no_backup)
        print("Compact results:")
        for fname, stats in res.items():
            print(
                f"  {fname}: {stats['before']} -> {stats['after']} ({stats['archived']} archived)"
            )
        return 0
    if args.command == "validate":
        valid, issues = validate_memory(config)
        if valid:
            print("OK: Memory structure is valid")
            return 0
        print("ERROR: Memory structure has issues:")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    if args.command == "health":
        _print_health(get_memory_health(config), args.json)
        return 0
    if args.command == "init":
        return 0 if initialize_memory(config) else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
