#!/usr/bin/env python3
"""
Chief of Staff Performance Report Script

Generates performance reports for agents by reading state files
and aggregating metrics over a specified time period.

Usage:
    python3 ecos_performance_report.py --agent SESSION_NAME
    python3 ecos_performance_report.py --agent SESSION_NAME --period 7
    python3 ecos_performance_report.py --project PROJECT_ID
    python3 ecos_performance_report.py --all --period 30

Output:
    JSON with performance metrics including:
    - agent: agent session name
    - period_days: reporting period
    - metrics: aggregated performance metrics
    - tasks: task completion statistics
    - efficiency: efficiency indicators
"""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, TypedDict


class TimelineEntry(TypedDict):
    """Type for timeline entries."""

    timestamp: str
    entry: str


class PerformanceData(TypedDict):
    """Type for performance data dictionary."""

    tasks_completed: int
    tasks_failed: int
    tasks_in_progress: int
    messages_sent: int
    messages_received: int
    agents_spawned: int
    errors_encountered: int
    sessions: list[str]
    timeline: list[TimelineEntry]


# Default state file location patterns
STATE_FILE_PATTERNS = [
    ".claude/chief-of-staff-state.local.md",
    ".claude/performance-log.local.md",
    "design/exec-phase.local.md",
]


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """
    Parse YAML-like frontmatter from markdown content.

    Uses stdlib only - simple key: value parsing.

    Args:
        content: Markdown content with optional frontmatter

    Returns:
        Tuple of (frontmatter_dict, body)
    """
    if not content.startswith("---"):
        return {}, content

    end_index = content.find("---", 3)
    if end_index == -1:
        return {}, content

    frontmatter_text = content[3:end_index].strip()
    body = content[end_index + 3 :].strip()

    # Simple YAML-like parsing (key: value)
    data = {}
    current_key = None
    current_value = []

    for line in frontmatter_text.split("\n"):
        if ":" in line and not line.startswith(" ") and not line.startswith("\t"):
            # Save previous key-value
            if current_key is not None:
                value = "\n".join(current_value).strip()
                data[current_key] = value

            # Start new key-value
            key, _, value = line.partition(":")
            current_key = key.strip()
            current_value = [value.strip()]
        elif current_key is not None:
            current_value.append(line)

    # Save last key-value
    if current_key is not None:
        value = "\n".join(current_value).strip()
        data[current_key] = value

    return data, body


def find_state_files(project_dir: Optional[Path] = None) -> list[Path]:
    """
    Find state files in the project directory.

    Args:
        project_dir: Project directory to search (defaults to current)

    Returns:
        List of found state file paths
    """
    if project_dir is None:
        project_dir = Path.cwd()

    found_files = []

    for pattern in STATE_FILE_PATTERNS:
        file_path = project_dir / pattern
        if file_path.exists():
            found_files.append(file_path)

    return found_files


def parse_performance_data(state_files: list[Path]) -> PerformanceData:
    """
    Parse performance data from state files.

    Args:
        state_files: List of state file paths to parse

    Returns:
        Dictionary with aggregated performance data
    """
    performance: PerformanceData = {
        "tasks_completed": 0,
        "tasks_failed": 0,
        "tasks_in_progress": 0,
        "messages_sent": 0,
        "messages_received": 0,
        "agents_spawned": 0,
        "errors_encountered": 0,
        "sessions": [],
        "timeline": [],
    }

    for file_path in state_files:
        try:
            content = file_path.read_text(encoding="utf-8")
            data, body = parse_frontmatter(content)

            # Extract metrics from frontmatter
            if "tasks_completed" in data:
                try:
                    performance["tasks_completed"] += int(data["tasks_completed"])
                except (ValueError, TypeError):
                    pass

            if "tasks_failed" in data:
                try:
                    performance["tasks_failed"] += int(data["tasks_failed"])
                except (ValueError, TypeError):
                    pass

            if "active_tasks" in data:
                try:
                    performance["tasks_in_progress"] += int(data["active_tasks"])
                except (ValueError, TypeError):
                    pass

            if "messages_sent" in data:
                try:
                    performance["messages_sent"] += int(data["messages_sent"])
                except (ValueError, TypeError):
                    pass

            if "agents_spawned" in data:
                try:
                    performance["agents_spawned"] += int(data["agents_spawned"])
                except (ValueError, TypeError):
                    pass

            # Parse timeline from body (look for dated entries)
            date_pattern = re.compile(r"(\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2})")
            for match in date_pattern.finditer(body):
                # Get context around the date
                start = max(0, match.start() - 10)
                end = min(len(body), match.end() + 100)
                context = body[start:end].strip()

                # Extract first line of context
                first_line = context.split("\n")[0][:80]

                performance["timeline"].append(
                    {"timestamp": match.group(1), "entry": first_line}
                )

        except Exception:
            performance["errors_encountered"] += 1

    # Sort timeline by timestamp
    performance["timeline"].sort(key=lambda x: x["timestamp"], reverse=True)
    # Limit timeline entries
    performance["timeline"] = performance["timeline"][:20]

    return performance


def calculate_efficiency(
    performance: PerformanceData, period_days: int
) -> dict[str, float]:
    """
    Calculate efficiency metrics from performance data.

    Args:
        performance: Aggregated performance data
        period_days: Number of days in the reporting period

    Returns:
        Dictionary with efficiency metrics
    """
    total_tasks = performance["tasks_completed"] + performance["tasks_failed"]

    efficiency = {
        "completion_rate": 0.0,
        "tasks_per_day": 0.0,
        "agents_per_task": 0.0,
        "message_ratio": 0.0,
    }

    if total_tasks > 0:
        efficiency["completion_rate"] = round(
            (performance["tasks_completed"] / total_tasks) * 100, 1
        )

    if period_days > 0:
        efficiency["tasks_per_day"] = round(
            performance["tasks_completed"] / period_days, 2
        )

    if performance["tasks_completed"] > 0:
        efficiency["agents_per_task"] = round(
            performance["agents_spawned"] / performance["tasks_completed"], 2
        )

    if performance["messages_received"] > 0:
        efficiency["message_ratio"] = round(
            performance["messages_sent"] / performance["messages_received"], 2
        )

    return efficiency


def generate_report(
    agent_name: Optional[str],
    project_id: Optional[str],
    period_days: int,
    project_dir: Optional[Path],
) -> dict:
    """
    Generate a performance report.

    Args:
        agent_name: Optional agent session name filter
        project_id: Optional project ID filter
        period_days: Reporting period in days
        project_dir: Project directory to search

    Returns:
        Dictionary with the performance report
    """
    # Find state files
    state_files = find_state_files(project_dir)

    if not state_files:
        return {
            "success": False,
            "error": "No state files found",
            "searched_patterns": STATE_FILE_PATTERNS,
            "searched_directory": str(project_dir or Path.cwd()),
        }

    # Parse performance data
    performance = parse_performance_data(state_files)

    # Calculate efficiency
    efficiency = calculate_efficiency(performance, period_days)

    # Calculate date range
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=period_days)

    report = {
        "success": True,
        "generated_at": end_date.isoformat().replace("+00:00", "Z"),
        "period": {
            "days": period_days,
            "start": start_date.strftime("%Y-%m-%d"),
            "end": end_date.strftime("%Y-%m-%d"),
        },
        "filters": {"agent": agent_name, "project": project_id},
        "metrics": {
            "tasks": {
                "completed": performance["tasks_completed"],
                "failed": performance["tasks_failed"],
                "in_progress": performance["tasks_in_progress"],
                "total": performance["tasks_completed"] + performance["tasks_failed"],
            },
            "communication": {
                "messages_sent": performance["messages_sent"],
                "messages_received": performance["messages_received"],
            },
            "resources": {
                "agents_spawned": performance["agents_spawned"],
                "errors_encountered": performance["errors_encountered"],
            },
        },
        "efficiency": efficiency,
        "recent_activity": performance["timeline"][:10],
        "sources": [str(f) for f in state_files],
    }

    return report


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate performance reports for agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Report for a specific agent (last 7 days)
    python3 ecos_performance_report.py --agent my-session

    # Report for a specific project (last 30 days)
    python3 ecos_performance_report.py --project my-project --period 30

    # Report for all agents
    python3 ecos_performance_report.py --all

    # Specify custom project directory
    python3 ecos_performance_report.py --agent my-session --project-dir /path/to/project
        """,
    )

    filter_group = parser.add_mutually_exclusive_group(required=True)
    filter_group.add_argument(
        "--agent", metavar="SESSION_NAME", help="Agent session name to report on"
    )
    filter_group.add_argument(
        "--project", metavar="PROJECT_ID", help="Project ID to report on"
    )
    filter_group.add_argument("--all", action="store_true", help="Report on all agents")

    parser.add_argument(
        "--period",
        type=int,
        default=7,
        metavar="DAYS",
        help="Reporting period in days (default: 7)",
    )

    parser.add_argument(
        "--project-dir",
        metavar="PATH",
        help="Project directory to search for state files",
    )

    parser.add_argument(
        "--compact", action="store_true", help="Output compact JSON (no indentation)"
    )

    args = parser.parse_args()

    # Validate period
    if args.period < 1:
        print(
            json.dumps(
                {"success": False, "error": "Period must be at least 1 day"}, indent=2
            )
        )
        return 1

    if args.period > 365:
        print(
            json.dumps(
                {"success": False, "error": "Period cannot exceed 365 days"}, indent=2
            )
        )
        return 1

    # Determine project directory
    project_dir = Path(args.project_dir) if args.project_dir else None

    # Generate report
    agent_name = args.agent if args.agent else None
    project_id = args.project if args.project else None

    report = generate_report(agent_name, project_id, args.period, project_dir)

    # Output JSON
    indent = None if args.compact else 2
    print(json.dumps(report, indent=indent))

    return 0 if report.get("success", False) else 1


if __name__ == "__main__":
    sys.exit(main())
