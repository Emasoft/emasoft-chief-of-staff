#!/usr/bin/env python3
"""
ecos_resource_check.py - UserPromptSubmit hook for resource warning.

Checks system resources before spawning new agents and warns if thresholds exceeded:
- CPU usage > 80%
- Memory usage > 85%
- Disk usage > 90%

Light-weight check designed to complete within 5 seconds.

Dependencies: Python 3.8+ stdlib only

Usage (as Claude Code hook):
    Receives JSON via stdin from UserPromptSubmit hook event.
    Outputs warning system message if resources are low.

Exit codes:
    0 - Success (resources OK or warning issued)
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import Any


# Resource thresholds (percentage)
CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 85
DISK_THRESHOLD = 90


def get_cpu_usage() -> float | None:
    """Get current CPU usage percentage.

    Returns:
        CPU usage percentage or None if unavailable
    """
    try:
        # Use top command for macOS/Linux
        if sys.platform == "darwin":
            # macOS: use top -l 1
            result = subprocess.run(
                ["top", "-l", "1", "-n", "0"], capture_output=True, text=True, timeout=3
            )
            if result.returncode == 0:
                for line in result.stdout.split("\n"):
                    if "CPU usage" in line:
                        # Parse: CPU usage: X.X% user, Y.Y% sys, Z.Z% idle
                        parts = line.split(",")
                        idle_part = parts[-1] if parts else ""
                        if "idle" in idle_part:
                            idle_str = (
                                idle_part.replace("idle", "").replace("%", "").strip()
                            )
                            idle = float(idle_str)
                            return 100.0 - idle
        else:
            # Linux: use /proc/stat
            with open("/proc/stat") as f:
                line = f.readline()
                if line.startswith("cpu "):
                    parts = line.split()
                    if len(parts) >= 5:
                        user = int(parts[1])
                        nice = int(parts[2])
                        system = int(parts[3])
                        idle = int(parts[4])
                        total = user + nice + system + idle
                        if total > 0:
                            return ((user + nice + system) / total) * 100.0
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError, ValueError):
        pass
    return None


def get_memory_usage() -> float | None:
    """Get current memory usage percentage.

    Returns:
        Memory usage percentage or None if unavailable
    """
    try:
        if sys.platform == "darwin":
            # macOS: use vm_stat
            result = subprocess.run(
                ["vm_stat"], capture_output=True, text=True, timeout=2
            )
            if result.returncode == 0:
                stats: dict[str, int] = {}
                for line in result.stdout.split("\n"):
                    if ":" in line:
                        key, value = line.split(":", 1)
                        value = value.strip().rstrip(".")
                        try:
                            stats[key.strip()] = int(value)
                        except ValueError:
                            pass

                # Calculate usage (pages are 4096 bytes)
                page_size = 4096
                free_pages = stats.get("Pages free", 0)
                inactive_pages = stats.get("Pages inactive", 0)
                speculative_pages = stats.get("Pages speculative", 0)

                # Get total memory
                result2 = subprocess.run(
                    ["sysctl", "-n", "hw.memsize"],
                    capture_output=True,
                    text=True,
                    timeout=2,
                )
                if result2.returncode == 0:
                    total_mem = int(result2.stdout.strip())
                    available = (
                        free_pages + inactive_pages + speculative_pages
                    ) * page_size
                    used = total_mem - available
                    return (used / total_mem) * 100.0
        else:
            # Linux: use /proc/meminfo
            with open("/proc/meminfo") as f:
                meminfo: dict[str, int] = {}
                for line in f:
                    if ":" in line:
                        key, value = line.split(":", 1)
                        value = value.strip().split()[0]  # Get the number part
                        try:
                            meminfo[key.strip()] = int(value)
                        except ValueError:
                            pass

                total = meminfo.get("MemTotal", 0)
                available = meminfo.get("MemAvailable", 0)
                if total > 0 and available > 0:
                    return ((total - available) / total) * 100.0
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError, ValueError):
        pass
    return None


def get_disk_usage(path: str = "/") -> float | None:
    """Get disk usage percentage for given path.

    Args:
        path: Path to check disk usage for

    Returns:
        Disk usage percentage or None if unavailable
    """
    try:
        result = subprocess.run(
            ["df", "-P", path], capture_output=True, text=True, timeout=2
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            if len(lines) >= 2:
                parts = lines[1].split()
                if len(parts) >= 5:
                    usage_str = parts[4].rstrip("%")
                    return float(usage_str)
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, ValueError):
        pass
    return None


def format_resource_warning(alerts: list[dict[str, Any]]) -> str:
    """Format resource alerts into a warning message.

    Args:
        alerts: List of alert dictionaries

    Returns:
        Formatted warning string
    """
    lines = []
    lines.append("")
    lines.append("!!! RESOURCE WARNING !!!")
    lines.append("-" * 40)

    for alert in alerts:
        resource = alert["resource"]
        current = alert["current"]
        threshold = alert["threshold"]
        lines.append(f"  {resource}: {current:.1f}% (threshold: {threshold}%)")

    lines.append("-" * 40)
    lines.append(
        "Consider closing unused applications or waiting before spawning new agents."
    )
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    """Main entry point for UserPromptSubmit hook.

    Checks system resources and outputs warning if thresholds exceeded.

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

    # Get working directory for disk check
    cwd = hook_input.get("cwd", os.getcwd())

    # Collect resource alerts
    alerts: list[dict[str, Any]] = []

    # Check CPU
    cpu = get_cpu_usage()
    if cpu is not None and cpu > CPU_THRESHOLD:
        alerts.append({"resource": "CPU", "current": cpu, "threshold": CPU_THRESHOLD})

    # Check memory
    memory = get_memory_usage()
    if memory is not None and memory > MEMORY_THRESHOLD:
        alerts.append(
            {"resource": "Memory", "current": memory, "threshold": MEMORY_THRESHOLD}
        )

    # Check disk
    disk = get_disk_usage(cwd)
    if disk is not None and disk > DISK_THRESHOLD:
        alerts.append(
            {"resource": "Disk", "current": disk, "threshold": DISK_THRESHOLD}
        )

    # Output warning if any alerts
    if alerts:
        warning = format_resource_warning(alerts)
        # Output as JSON with systemMessage for Claude to see
        output = {
            "systemMessage": warning,
            "continue": True,  # Don't block, just warn
        }
        print(json.dumps(output))

    return 0


if __name__ == "__main__":
    sys.exit(main())
