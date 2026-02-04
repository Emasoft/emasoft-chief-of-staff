#!/usr/bin/env python3
"""
ecos_terminate_agent.py - Terminate an AI Maestro agent session.

Usage:
    python ecos_terminate_agent.py SESSION_NAME [--force]

Example:
    python ecos_terminate_agent.py cr-session-01
    python ecos_terminate_agent.py cr-session-01 --force
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
        description="Terminate an AI Maestro agent session.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Graceful termination
    python ecos_terminate_agent.py my-agent-session

    # Force termination (skip cleanup)
    python ecos_terminate_agent.py my-agent-session --force
        """,
    )
    parser.add_argument(
        "session_name",
        type=str,
        help="Session name of the agent to terminate",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force termination without graceful shutdown",
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
    Main entry point for terminating an agent.

    Returns:
        0 on success, 1 on error.
    """
    args = parse_args()

    # Step 1: Check if agent exists
    returncode, stdout, stderr = run_aimaestro_command(["show", args.session_name])

    if returncode != 0:
        # Agent doesn't exist or command failed
        result: dict[str, Any] = {
            "status": "error",
            "message": f"Agent '{args.session_name}' not found or command failed",
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "error": stderr if stderr else "Agent not found",
        }
        print(json.dumps(result, indent=2), file=sys.stderr)
        return 1

    # Step 2: Terminate the agent
    delete_args = ["delete", args.session_name, "--confirm"]
    if args.force:
        delete_args.append("--force")

    returncode, stdout, stderr = run_aimaestro_command(delete_args)

    if returncode != 0:
        # Termination failed
        result = {
            "status": "error",
            "message": f"Failed to terminate agent '{args.session_name}'",
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "error": stderr if stderr else "Unknown error",
        }
        print(json.dumps(result, indent=2), file=sys.stderr)
        return 1

    # Success
    result = {
        "status": "success",
        "message": f"Agent '{args.session_name}' terminated successfully",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "parameters": {
            "session_name": args.session_name,
            "force": args.force,
        },
        "output": stdout,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
