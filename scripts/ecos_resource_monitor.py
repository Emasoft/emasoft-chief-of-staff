#!/usr/bin/env python3
"""
Chief of Staff Resource Monitor Script

Monitors system resources to determine if new agents can be safely spawned.
Checks CPU, memory, disk usage, and active Claude Code processes.

NOTE: This script is designed for macOS. Other platforms are not supported.

Usage:
    python3 ecos_resource_monitor.py --check-spawn
    python3 ecos_resource_monitor.py --status
    python3 ecos_resource_monitor.py --json

Output:
    JSON with resource status including:
    - can_spawn: boolean indicating if a new agent can be spawned
    - cpu: CPU usage percentage and details
    - memory: Memory usage and availability
    - disk: Disk space usage
    - claude_processes: Count of active Claude Code processes
    - warnings: Any resource warnings
    - recommendations: Suggested actions if resources are constrained
"""

import argparse
import json
import subprocess
import sys


# Resource thresholds for spawning new agents
THRESHOLDS = {
    "max_cpu_percent": 80.0,
    "min_memory_available_gb": 2.0,
    "max_memory_percent": 85.0,
    "min_disk_available_gb": 5.0,
    "max_claude_processes": 10,
}


def get_cpu_usage() -> dict:
    """Get current CPU usage information (macOS only)."""
    try:
        result = subprocess.run(
            ["top", "-l", "1", "-n", "0"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        for line in result.stdout.split("\n"):
            if "CPU usage" in line:
                parts = line.split(",")
                idle = 0.0
                for part in parts:
                    if "idle" in part:
                        idle = float(part.split("%")[0].split()[-1])
                usage = 100.0 - idle
                return {
                    "usage_percent": round(usage, 1),
                    "available_percent": round(idle, 1),
                    "status": "ok" if usage < THRESHOLDS["max_cpu_percent"] else "high",
                }
        return {
            "usage_percent": 0.0,
            "status": "unknown",
            "error": "Could not parse CPU usage from top output",
        }
    except Exception as e:
        return {"usage_percent": 0.0, "status": "error", "error": str(e)}


def get_memory_usage() -> dict:
    """Get current memory usage information (macOS only)."""
    try:
        result = subprocess.run(["vm_stat"], capture_output=True, text=True, timeout=5)

        page_size = 4096
        stats: dict = {}

        for line in result.stdout.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip().lower().replace(" ", "_")
                value = value.strip().rstrip(".")
                try:
                    stats[key] = int(value)
                except ValueError:
                    pass

        pages_free = stats.get("pages_free", 0)
        pages_active = stats.get("pages_active", 0)
        pages_inactive = stats.get("pages_inactive", 0)
        pages_wired = stats.get("pages_wired_down", 0)
        pages_speculative = stats.get("pages_speculative", 0)

        free_bytes = (pages_free + pages_speculative) * page_size
        used_bytes = (pages_active + pages_inactive + pages_wired) * page_size
        total_bytes = free_bytes + used_bytes

        free_gb = free_bytes / (1024**3)
        total_gb = total_bytes / (1024**3)
        used_percent = (used_bytes / total_bytes) * 100 if total_bytes > 0 else 0

        return {
            "total_gb": round(total_gb, 2),
            "available_gb": round(free_gb, 2),
            "used_percent": round(used_percent, 1),
            "status": "ok" if free_gb >= THRESHOLDS["min_memory_available_gb"] else "low",
        }
    except Exception as e:
        return {"available_gb": 0.0, "status": "error", "error": str(e)}


def get_disk_usage() -> dict:
    """Get current disk usage information."""
    try:
        result = subprocess.run(
            ["df", "-h", "/"], capture_output=True, text=True, timeout=5
        )

        lines = result.stdout.strip().split("\n")
        if len(lines) >= 2:
            parts = lines[1].split()
            if len(parts) >= 4:
                available_str = parts[3]
                if available_str.endswith("G"):
                    available_gb = float(available_str[:-1])
                elif available_str.endswith("T"):
                    available_gb = float(available_str[:-1]) * 1024
                elif available_str.endswith("M"):
                    available_gb = float(available_str[:-1]) / 1024
                else:
                    available_gb = float(available_str) / (1024**3)

                used_percent_str = parts[4].rstrip("%")
                used_percent = float(used_percent_str)

                return {
                    "available_gb": round(available_gb, 2),
                    "used_percent": round(used_percent, 1),
                    "status": "ok" if available_gb >= THRESHOLDS["min_disk_available_gb"] else "low",
                }

        return {
            "available_gb": 0.0,
            "status": "unknown",
            "error": "Could not parse df output",
        }
    except Exception as e:
        return {"available_gb": 0.0, "status": "error", "error": str(e)}


def get_claude_processes() -> dict:
    """Get count of active Claude Code processes."""
    try:
        result = subprocess.run(
            ["pgrep", "-f", "claude"], capture_output=True, text=True, timeout=5
        )

        pids = [p.strip() for p in result.stdout.strip().split("\n") if p.strip()]
        count = len(pids)

        return {
            "count": count,
            "pids": pids[:10],
            "status": "ok" if count < THRESHOLDS["max_claude_processes"] else "high",
        }
    except Exception as e:
        return {"count": 0, "status": "error", "error": str(e)}


def can_spawn_agent(cpu: dict, memory: dict, disk: dict, processes: dict) -> tuple:
    """Determine if a new agent can be safely spawned."""
    reasons = []

    if cpu.get("usage_percent", 0) >= THRESHOLDS["max_cpu_percent"]:
        reasons.append(
            f"CPU usage too high: {cpu.get('usage_percent')}% >= {THRESHOLDS['max_cpu_percent']}%"
        )

    if memory.get("available_gb", 0) < THRESHOLDS["min_memory_available_gb"]:
        reasons.append(
            f"Insufficient memory: {memory.get('available_gb')}GB < {THRESHOLDS['min_memory_available_gb']}GB"
        )
    if memory.get("used_percent", 0) >= THRESHOLDS["max_memory_percent"]:
        reasons.append(
            f"Memory usage too high: {memory.get('used_percent')}% >= {THRESHOLDS['max_memory_percent']}%"
        )

    if disk.get("available_gb", 0) < THRESHOLDS["min_disk_available_gb"]:
        reasons.append(
            f"Insufficient disk space: {disk.get('available_gb')}GB < {THRESHOLDS['min_disk_available_gb']}GB"
        )

    if processes.get("count", 0) >= THRESHOLDS["max_claude_processes"]:
        reasons.append(
            f"Too many Claude processes: {processes.get('count')} >= {THRESHOLDS['max_claude_processes']}"
        )

    return len(reasons) == 0, reasons


def generate_recommendations(can_spawn: bool, reasons: list) -> list:
    """Generate recommendations based on resource status."""
    recommendations = []

    if not can_spawn:
        for reason in reasons:
            if "CPU" in reason:
                recommendations.append(
                    "Wait for CPU-intensive tasks to complete or reduce concurrent workloads"
                )
            elif "memory" in reason.lower():
                recommendations.append(
                    "Close unused applications or terminate idle Claude sessions"
                )
            elif "disk" in reason.lower():
                recommendations.append(
                    "Clear temporary files or move large files to external storage"
                )
            elif "processes" in reason:
                recommendations.append(
                    "Terminate idle Claude sessions before spawning new agents"
                )

    return recommendations


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Monitor system resources for agent spawning decisions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python3 ecos_resource_monitor.py --check-spawn
    python3 ecos_resource_monitor.py --status
    python3 ecos_resource_monitor.py --status --compact
        """,
    )

    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument(
        "--check-spawn",
        action="store_true",
        help="Check if a new agent can be spawned (focused output)",
    )
    action_group.add_argument(
        "--status", action="store_true", help="Get full resource status (default)"
    )

    parser.add_argument(
        "--compact", action="store_true", help="Output compact JSON (no indentation)"
    )

    args = parser.parse_args()

    if not args.check_spawn and not args.status:
        args.status = True

    cpu = get_cpu_usage()
    memory = get_memory_usage()
    disk = get_disk_usage()
    processes = get_claude_processes()

    can_spawn, reasons = can_spawn_agent(cpu, memory, disk, processes)
    recommendations = generate_recommendations(can_spawn, reasons)

    if args.check_spawn:
        result = {
            "can_spawn": can_spawn,
            "reasons": reasons if not can_spawn else [],
            "recommendations": recommendations,
        }
    else:
        result = {
            "can_spawn": can_spawn,
            "cpu": cpu,
            "memory": memory,
            "disk": disk,
            "claude_processes": processes,
            "thresholds": THRESHOLDS,
            "warnings": reasons,
            "recommendations": recommendations,
        }

    indent = None if args.compact else 2
    print(json.dumps(result, indent=indent))

    return 0 if can_spawn else 1


if __name__ == "__main__":
    sys.exit(main())
