#!/usr/bin/env python3
"""
ecos_hibernate_agent.py - Hibernate an AI Maestro agent session.

Hibernation preserves agent state (context, memory, pending tasks) while
freeing system resources. The agent can be woken later to resume work.

Usage:
    python ecos_hibernate_agent.py SESSION_NAME

Example:
    python ecos_hibernate_agent.py dev-session-01
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Hibernate an AI Maestro agent session.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Hibernate an agent to save resources
    python ecos_hibernate_agent.py my-agent-session

Notes:
    Hibernation preserves:
    - Agent context and conversation history
    - Pending tasks and their state
    - Inter-agent message queue

    Use ecos_wake_agent.py to resume the agent.
        """,
    )
    parser.add_argument(
        "session_name",
        type=str,
        help="Session name of the agent to hibernate",
    )
    return parser.parse_args()


def run_aimaestro_command(args: list[str], timeout: int = 60) -> tuple[int, str, str]:
    """Run aimaestro-agent.sh command."""
    cmd = ["aimaestro-agent.sh"] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return (result.returncode, result.stdout.strip(), result.stderr.strip())
    except subprocess.TimeoutExpired:
        return (124, "", f"Command timed out after {timeout}s")
    except FileNotFoundError:
        return (127, "", "aimaestro-agent.sh not found in PATH")
    except Exception as e:
        return (1, "", str(e))


def main() -> int:
    """
    Main entry point for hibernating an agent.

    Returns:
        0 on success, 1 on error.
    """
    args = parse_args()
    result: dict[str, Any]

    # Step 1: Check if agent exists
    returncode, stdout, stderr = run_aimaestro_command(["show", args.session_name])

    if returncode != 0:
        # Agent doesn't exist or command failed
        result = {
            "status": "error",
            "message": f"Agent '{args.session_name}' not found or command failed",
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "error": stderr if stderr else "Agent not found",
        }
        print(json.dumps(result, indent=2), file=sys.stderr)
        return 1

    # Step 2: Check if agent is already hibernated
    # The 'show' output might indicate hibernation status, but we'll proceed anyway
    # and let aimaestro-agent.sh handle duplicate hibernation attempts

    # Step 3: Hibernate the agent
    returncode, stdout, stderr = run_aimaestro_command(["hibernate", args.session_name])

    if returncode != 0:
        # Hibernation failed
        result = {
            "status": "error",
            "message": f"Failed to hibernate agent '{args.session_name}'",
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "error": stderr if stderr else "Unknown error",
        }
        print(json.dumps(result, indent=2), file=sys.stderr)
        return 1

    # Success
    result = {
        "status": "success",
        "message": f"Agent '{args.session_name}' hibernated successfully",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "parameters": {
            "session_name": args.session_name,
        },
        "output": stdout,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
