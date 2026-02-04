#!/usr/bin/env python3
"""
Chief of Staff Skills Reindex Script

Triggers a PSS (Perfect Skill Suggester) reindex for an agent session.

This script is a STUB that will be implemented once the AI Maestro command
forwarding mechanism is established. The intended behavior is to send
the /pss-reindex-skills command to the target agent via AI Maestro.

Usage:
    python3 ecos_reindex_skills.py SESSION_NAME
    python3 ecos_reindex_skills.py SESSION_NAME --force
    python3 ecos_reindex_skills.py SESSION_NAME --dry-run

Output:
    JSON with reindex request status including:
    - success: boolean indicating if request was sent
    - session: target session name
    - status: current status (stub/pending/sent/completed)
    - message: human-readable status message

TODO:
    - Implement AI Maestro command forwarding
    - Add support for /pss-reindex-skills command via message
    - Add status tracking for reindex completion
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone


def send_ai_maestro_message(
    to_session: str,
    subject: str,
    message: str,
    priority: str = "normal",
    msg_type: str = "command",
) -> tuple[bool, str]:
    """
    Send a message via AI Maestro API.

    Args:
        to_session: Target session name
        subject: Message subject
        message: Message content
        priority: Message priority
        msg_type: Message type

    Returns:
        Tuple of (success, response_or_error)
    """
    try:
        payload = {
            "to": to_session,
            "subject": subject,
            "priority": priority,
            "content": {"type": msg_type, "message": message},
        }

        api_url = os.getenv("AIMAESTRO_API", "http://localhost:23000")

        result = subprocess.run(
            [
                "curl",
                "-s",
                "-X",
                "POST",
                f"{api_url}/api/messages",
                "-H",
                "Content-Type: application/json",
                "-d",
                json.dumps(payload),
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode == 0:
            try:
                response = json.loads(result.stdout)
                if response.get("success"):
                    return True, response.get("message_id", "unknown")
                else:
                    return False, response.get("error", "Unknown error")
            except json.JSONDecodeError:
                return False, f"Invalid JSON response: {result.stdout}"
        else:
            return False, result.stderr or "curl command failed"

    except subprocess.TimeoutExpired:
        return False, "Request timed out"
    except FileNotFoundError:
        return False, "curl not found in PATH"
    except Exception as e:
        return False, str(e)


def check_ai_maestro_available() -> bool:
    """
    Check if AI Maestro API is available.

    Returns:
        True if API is reachable, False otherwise
    """
    try:
        api_url = os.getenv("AIMAESTRO_API", "http://localhost:23000")
        result = subprocess.run(
            [
                "curl",
                "-s",
                "-o",
                "/dev/null",
                "-w",
                "%{http_code}",
                f"{api_url}/api/health",
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0 and result.stdout.strip() == "200"
    except Exception:
        return False


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Trigger PSS skill reindex for an agent session",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Request reindex for a session
    python3 ecos_reindex_skills.py my-session

    # Force reindex (bypass any caching)
    python3 ecos_reindex_skills.py my-session --force

    # Dry run - show what would be done
    python3 ecos_reindex_skills.py my-session --dry-run

Note:
    This script is currently a STUB. The actual implementation
    requires AI Maestro command forwarding to be established.
        """,
    )

    parser.add_argument(
        "session_name", help="Name of the agent session to reindex skills for"
    )

    parser.add_argument(
        "--force", action="store_true", help="Force reindex, bypassing any caching"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually sending the request",
    )

    args = parser.parse_args()

    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    # Build the command message
    command = "/pss-reindex-skills"
    if args.force:
        command += " --force"

    result: dict = {
        "session": args.session_name,
        "command": command,
        "timestamp": timestamp,
    }

    if args.dry_run:
        result.update(
            {
                "success": True,
                "status": "dry_run",
                "message": f"Would send reindex command to session '{args.session_name}'",
                "command_to_send": command,
            }
        )
        print(json.dumps(result, indent=2))
        return 0

    # Check if AI Maestro is available
    if not check_ai_maestro_available():
        result.update(
            {
                "success": False,
                "status": "stub",
                "message": "AI Maestro API not available. This is a STUB implementation.",
                "todo": [
                    "Implement AI Maestro command forwarding",
                    "Add support for /pss-reindex-skills command via message",
                    "Add status tracking for reindex completion",
                ],
            }
        )
        print(json.dumps(result, indent=2))
        return 1

    # Send the reindex request via AI Maestro
    subject = "PSS Reindex Request"
    message = f"Please execute: {command}"

    success, response = send_ai_maestro_message(
        args.session_name,
        subject,
        message,
        priority="normal",
        msg_type="command_request",
    )

    if success:
        result.update(
            {
                "success": True,
                "status": "sent",
                "message": f"Reindex request sent to session '{args.session_name}'",
                "message_id": response,
                "note": "The target session must process the command manually. "
                "Automated command execution is not yet implemented.",
            }
        )
    else:
        result.update(
            {
                "success": False,
                "status": "failed",
                "message": f"Failed to send reindex request: {response}",
                "error": response,
            }
        )

    print(json.dumps(result, indent=2))
    return 0 if result.get("success", False) else 1


if __name__ == "__main__":
    sys.exit(main())
