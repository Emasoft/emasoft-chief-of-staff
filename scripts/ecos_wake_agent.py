#!/usr/bin/env python3
"""
ecos_wake_agent.py - Wake a hibernated AI Maestro agent session.

Waking restores a hibernated agent to active state, loading preserved
context, memory, and pending tasks.

Usage:
    python ecos_wake_agent.py SESSION_NAME

Example:
    python ecos_wake_agent.py dev-session-01
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Wake a hibernated AI Maestro agent session.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Wake a hibernated agent
    python ecos_wake_agent.py my-agent-session

Notes:
    Waking restores:
    - Agent context and conversation history
    - Pending tasks and their state
    - Inter-agent message queue

    The agent resumes from where it was hibernated.
        """,
    )
    parser.add_argument(
        "session_name",
        type=str,
        help="Session name of the agent to wake",
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
    Main entry point for waking a hibernated agent.

    Returns:
        0 on success, 1 on error.
    """
    args = parse_args()
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    # Step 1: Check if agent exists
    returncode, stdout, stderr = run_aimaestro_command(["show", args.session_name])

    if returncode != 0:
        result = {
            "status": "error",
            "message": f"Agent '{args.session_name}' not found or error occurred",
            "timestamp": timestamp,
            "error": stderr if stderr else "Agent does not exist",
        }
        print(json.dumps(result, indent=2))
        return 1

    # Step 2: Parse agent info to check status
    try:
        agent_info = json.loads(stdout)
        agent_status = agent_info.get("status", "").lower()

        # Step 3: Verify agent is hibernated
        if agent_status == "active":
            result = {
                "status": "error",
                "message": f"Agent '{args.session_name}' is already active",
                "timestamp": timestamp,
                "agent_status": agent_status,
            }
            print(json.dumps(result, indent=2))
            return 1

        if agent_status not in ["hibernated", "sleeping"]:
            result = {
                "status": "error",
                "message": f"Agent '{args.session_name}' cannot be woken (status: {agent_status})",
                "timestamp": timestamp,
                "agent_status": agent_status,
            }
            print(json.dumps(result, indent=2))
            return 1

    except (json.JSONDecodeError, KeyError) as e:
        result = {
            "status": "error",
            "message": f"Failed to parse agent status for '{args.session_name}'",
            "timestamp": timestamp,
            "error": str(e),
        }
        print(json.dumps(result, indent=2))
        return 1

    # Step 4: Execute wake command
    returncode, stdout, stderr = run_aimaestro_command(["wake", args.session_name])

    if returncode != 0:
        result = {
            "status": "error",
            "message": f"Failed to wake agent '{args.session_name}'",
            "timestamp": timestamp,
            "error": stderr if stderr else "Wake command failed",
        }
        print(json.dumps(result, indent=2))
        return 1

    # Success
    result = {
        "status": "success",
        "message": f"Agent '{args.session_name}' successfully woken",
        "timestamp": timestamp,
        "session_name": args.session_name,
        "previous_status": agent_status,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
