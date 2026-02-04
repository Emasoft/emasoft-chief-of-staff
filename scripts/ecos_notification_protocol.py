#!/usr/bin/env python3
"""
Emasoft Chief of Staff - Notification Protocol Script

Implements notification protocols for agent communication via AI Maestro API.

Features:
- Send notifications to multiple agents with optional acknowledgment
- Wait for acknowledgments with reminder messages
- Broadcast notifications based on agent attributes (role, project)
- Skill installation with multi-phase notification workflow

Usage:
    python ecos_notification_protocol.py notify --agents agent1,agent2 --operation install --message "Installing skill X"
    python ecos_notification_protocol.py wait-ack --agent agent1 --timeout 120 --remind 30
    python ecos_notification_protocol.py broadcast --subject "Update" --message "..." --priority high --agents a,b,c
    python ecos_notification_protocol.py install-skill --agent agent1 --skill my-skill --wait-for-ok

Output: JSON format
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from typing import Any, cast
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


# AI Maestro API base URL
AIMAESTRO_API = os.getenv("AIMAESTRO_API", "http://localhost:23000")

# Default timeouts and intervals
DEFAULT_TIMEOUT = 120
DEFAULT_REMIND_INTERVAL = 30
DEFAULT_POLL_INTERVAL = 5


def _make_request(endpoint: str, method: str = "GET", data: dict | None = None) -> dict:
    """
    Make an HTTP request to the AI Maestro API.

    Args:
        endpoint: API endpoint (e.g., "/api/messages")
        method: HTTP method (GET, POST)
        data: JSON payload for POST requests

    Returns:
        Parsed JSON response as dict

    Raises:
        RuntimeError: If the request fails
    """
    url = f"{AIMAESTRO_API}{endpoint}"
    headers = {"Content-Type": "application/json"}

    request_data = None
    if data is not None:
        request_data = json.dumps(data).encode("utf-8")

    req = Request(url, data=request_data, headers=headers, method=method)

    try:
        with urlopen(req, timeout=10) as response:
            return cast(dict[str, Any], json.loads(response.read().decode("utf-8")))
    except HTTPError as e:
        raise RuntimeError(f"HTTP error {e.code}: {e.reason}")
    except URLError as e:
        raise RuntimeError(f"URL error: {e.reason}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON response: {e}")


def _send_message(
    to: str,
    subject: str,
    message: str,
    priority: str = "normal",
    msg_type: str = "notification",
    require_ack: bool = False,
) -> dict:
    """
    Send a single message via AI Maestro API.

    Args:
        to: Target agent session name
        subject: Message subject
        message: Message content
        priority: Message priority (low, normal, high, urgent)
        msg_type: Message type (notification, request, acknowledgment, etc.)
        require_ack: Whether to request acknowledgment

    Returns:
        API response dict
    """
    # Build message content with optional ack request
    content = {"type": msg_type, "message": message}
    if require_ack:
        content["require_acknowledgment"] = "true"
        content["ack_instructions"] = (
            "Please acknowledge this message by sending a reply with type='acknowledgment'"
        )

    payload = {"to": to, "subject": subject, "priority": priority, "content": content}

    return _make_request("/api/messages", method="POST", data=payload)


def _get_messages(agent: str, status: str = "unread") -> list[dict]:
    """
    Get messages for an agent from AI Maestro API.

    Args:
        agent: Agent session name
        status: Message status filter (unread, all)

    Returns:
        List of message dicts
    """
    endpoint = f"/api/messages?agent={agent}&action=list&status={status}"
    response = _make_request(endpoint)
    return cast(list[dict[str, Any]], response.get("messages", []))


def _list_agents_via_script() -> list[dict]:
    """
    List agents using aimaestro-agent.sh script.

    Returns:
        List of agent info dicts with keys: session_name, role, project, status
    """
    script_path = os.path.expanduser("~/.local/bin/aimaestro-agent.sh")

    if not os.path.exists(script_path):
        # Fallback: try to get agents from API directly
        try:
            response = _make_request("/api/agents")
            return cast(list[dict[str, Any]], response.get("agents", []))
        except RuntimeError:
            return []

    try:
        result = subprocess.run(
            [script_path, "list", "--json"], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            return cast(list[dict[str, Any]], data.get("agents", []))
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        pass

    return []


def notify_agents(
    agents: list[str], operation: str, message: str, require_ack: bool = False
) -> dict:
    """
    Send notification to each agent via AI Maestro.

    Sends a notification message to multiple agents about an operation.
    If require_ack is True, the message includes acknowledgment request instructions.

    Args:
        agents: List of agent session names to notify
        operation: Operation name (e.g., "install", "update", "restart")
        message: Notification message content
        require_ack: Whether to request acknowledgment from agents

    Returns:
        Dict mapping agent names to status:
        {
            "agent1": "sent",
            "agent2": "sent",
            "agent3": "error: connection refused"
        }
    """
    results = {}
    subject = f"[{operation.upper()}] Notification"

    for agent in agents:
        try:
            response = _send_message(
                to=agent,
                subject=subject,
                message=message,
                priority="normal",
                msg_type="notification",
                require_ack=require_ack,
            )

            if response.get("success", False):
                results[agent] = "sent"
            else:
                error = response.get("error", "unknown error")
                results[agent] = f"error: {error}"

        except RuntimeError as e:
            results[agent] = f"error: {e}"

    return results


def wait_for_acknowledgment(
    agent: str,
    timeout: int = DEFAULT_TIMEOUT,
    remind_interval: int = DEFAULT_REMIND_INTERVAL,
) -> bool:
    """
    Poll AI Maestro for acknowledgment message from agent.

    Continuously polls for an acknowledgment message from the specified agent.
    Sends reminder messages at the specified interval if no ack received.

    Args:
        agent: Agent session name to wait for
        timeout: Maximum seconds to wait (default: 120)
        remind_interval: Seconds between reminder messages (default: 30)

    Returns:
        True if acknowledgment received, False if timeout reached
    """
    start_time = time.time()
    last_remind_time = start_time

    # Get our session name for filtering incoming messages
    our_session = os.getenv("SESSION_NAME", "chief-of-staff")

    while True:
        elapsed = time.time() - start_time

        # Check for timeout
        if elapsed >= timeout:
            return False

        # Poll for messages from the target agent
        try:
            messages = _get_messages(our_session, status="unread")

            for msg in messages:
                # Check if this is an acknowledgment from our target agent
                sender = msg.get("from", "")
                content = msg.get("content", {})
                msg_type = content.get("type", "")

                if sender == agent and msg_type == "acknowledgment":
                    return True

        except RuntimeError:
            # API error, continue waiting
            pass

        # Send reminder if interval elapsed
        since_remind = time.time() - last_remind_time
        if since_remind >= remind_interval:
            try:
                _send_message(
                    to=agent,
                    subject="[REMINDER] Acknowledgment Required",
                    message=(
                        f"Reminder: Please acknowledge the previous notification. "
                        f"Waiting for {int(elapsed)} seconds. "
                        f"Timeout in {int(timeout - elapsed)} seconds."
                    ),
                    priority="high",
                    msg_type="reminder",
                )
                last_remind_time = time.time()
            except RuntimeError:
                pass

        # Wait before next poll
        time.sleep(DEFAULT_POLL_INTERVAL)


def broadcast_notification(
    subject: str,
    message: str,
    priority: str = "normal",
    agents: list[str] | None = None,
    role: str | None = None,
    project: str | None = None,
) -> dict:
    """
    Broadcast notification to agents matching criteria.

    Sends to specified agents list, or finds agents matching role/project filters.
    If no filters provided, sends to all available agents.

    Args:
        subject: Message subject
        message: Message content
        priority: Message priority (low, normal, high, urgent)
        agents: Explicit list of agent session names (takes precedence)
        role: Filter agents by role (e.g., "implementer", "reviewer")
        project: Filter agents by project assignment

    Returns:
        Dict with results:
        {
            "total_agents": 5,
            "sent": 4,
            "failed": 1,
            "results": {"agent1": "sent", "agent2": "error: ..."}
        }
    """
    target_agents = []

    if agents:
        # Use explicit agent list
        target_agents = agents
    else:
        # Find agents matching criteria
        all_agents = _list_agents_via_script()

        for agent_info in all_agents:
            session = agent_info.get("session_name", "")
            if not session:
                continue

            # Filter by role if specified
            if role and agent_info.get("role", "") != role:
                continue

            # Filter by project if specified
            if project and agent_info.get("project", "") != project:
                continue

            target_agents.append(session)

    # Send to all target agents
    results = {}
    sent_count = 0
    failed_count = 0

    for agent in target_agents:
        try:
            response = _send_message(
                to=agent,
                subject=subject,
                message=message,
                priority=priority,
                msg_type="broadcast",
            )

            if response.get("success", False):
                results[agent] = "sent"
                sent_count += 1
            else:
                error = response.get("error", "unknown error")
                results[agent] = f"error: {error}"
                failed_count += 1

        except RuntimeError as e:
            results[agent] = f"error: {e}"
            failed_count += 1

    return {
        "total_agents": len(target_agents),
        "sent": sent_count,
        "failed": failed_count,
        "results": results,
    }


def skill_install_with_notification(
    agent: str, skill: str, marketplace: str | None = None, wait_for_ok: bool = True
) -> dict:
    """
    Install skill with multi-phase notification workflow.

    Executes a 4-phase skill installation process:
    1. Notify agent about upcoming install
    2. Wait for acknowledgment (if wait_for_ok=True)
    3. Execute skill installation via aimaestro-agent.sh
    4. Notify agent to verify skill is active

    Args:
        agent: Target agent session name
        skill: Skill name to install
        marketplace: Marketplace name (optional, uses default if not specified)
        wait_for_ok: Whether to wait for acknowledgment before proceeding

    Returns:
        Dict with phase results:
        {
            "phases": [
                {"phase": 1, "name": "notify", "status": "success"},
                {"phase": 2, "name": "wait_ack", "status": "success"},
                {"phase": 3, "name": "install", "status": "success"},
                {"phase": 4, "name": "verify_notify", "status": "success"}
            ],
            "success": true,
            "warnings": []
        }
    """
    phases: list[dict] = []
    warnings: list[str] = []
    overall_success = True

    skill_ref = f"{skill}@{marketplace}" if marketplace else skill

    # Phase 1: Notify agent about upcoming install
    phase1_result = {"phase": 1, "name": "notify", "status": "pending"}
    try:
        response = _send_message(
            to=agent,
            subject=f"[SKILL INSTALL] Preparing to install: {skill_ref}",
            message=(
                f"Chief of Staff is preparing to install skill '{skill_ref}' for your session.\n\n"
                f"This may require a Claude Code restart to take effect.\n"
                f"Please save any pending work and acknowledge when ready."
            ),
            priority="high",
            msg_type="skill_install_notification",
            require_ack=wait_for_ok,
        )

        if response.get("success", False):
            phase1_result["status"] = "success"
        else:
            phase1_result["status"] = "failed"
            phase1_result["error"] = response.get("error", "unknown")
            overall_success = False

    except RuntimeError as e:
        phase1_result["status"] = "failed"
        phase1_result["error"] = str(e)
        overall_success = False

    phases.append(phase1_result)

    # Early exit if Phase 1 failed
    if phase1_result["status"] == "failed":
        return {
            "phases": phases,
            "success": False,
            "warnings": warnings,
            "error": "Failed to send initial notification",
        }

    # Phase 2: Wait for acknowledgment (if required)
    phase2_result = {"phase": 2, "name": "wait_ack", "status": "skipped"}

    if wait_for_ok:
        phase2_result["status"] = "pending"

        ack_received = wait_for_acknowledgment(
            agent=agent,
            timeout=DEFAULT_TIMEOUT,
            remind_interval=DEFAULT_REMIND_INTERVAL,
        )

        if ack_received:
            phase2_result["status"] = "success"
        else:
            phase2_result["status"] = "timeout"
            warnings.append(
                f"Acknowledgment timeout after {DEFAULT_TIMEOUT}s - proceeding anyway"
            )

    phases.append(phase2_result)

    # Phase 3: Execute skill installation
    phase3_result = {"phase": 3, "name": "install", "status": "pending"}

    script_path = os.path.expanduser("~/.local/bin/aimaestro-agent.sh")

    try:
        # Build install command
        install_args = [script_path, "plugin", "install", skill]
        if marketplace:
            install_args.extend(["--marketplace", marketplace])
        install_args.extend(["--agent", agent])

        # Check if script exists
        if not os.path.exists(script_path):
            # Fallback: use claude CLI directly
            install_args = ["claude", "plugin", "install", skill_ref]
            warnings.append("Using fallback claude CLI (aimaestro-agent.sh not found)")

        result = subprocess.run(
            install_args, capture_output=True, text=True, timeout=60
        )

        if result.returncode == 0:
            phase3_result["status"] = "success"
            phase3_result["output"] = result.stdout.strip()[:200]  # Truncate output
        else:
            phase3_result["status"] = "failed"
            phase3_result["error"] = result.stderr.strip()[:200]
            overall_success = False

    except subprocess.TimeoutExpired:
        phase3_result["status"] = "failed"
        phase3_result["error"] = "Installation timed out after 60s"
        overall_success = False
    except FileNotFoundError:
        phase3_result["status"] = "failed"
        phase3_result["error"] = "Installation script not found"
        overall_success = False
    except Exception as e:
        phase3_result["status"] = "failed"
        phase3_result["error"] = str(e)
        overall_success = False

    phases.append(phase3_result)

    # Phase 4: Notify agent to verify skill is active
    phase4_result = {"phase": 4, "name": "verify_notify", "status": "pending"}

    if phase3_result["status"] == "success":
        try:
            response = _send_message(
                to=agent,
                subject=f"[SKILL INSTALLED] Please verify: {skill_ref}",
                message=(
                    f"Skill '{skill_ref}' has been installed.\n\n"
                    f"IMPORTANT: You may need to restart your Claude Code session for the skill to activate.\n\n"
                    f"After restart, verify the skill is active by checking /skills or running a skill-specific command."
                ),
                priority="high",
                msg_type="skill_verify_notification",
            )

            if response.get("success", False):
                phase4_result["status"] = "success"
            else:
                phase4_result["status"] = "failed"
                phase4_result["error"] = response.get("error", "unknown")
                warnings.append("Failed to send verification notification")

        except RuntimeError as e:
            phase4_result["status"] = "failed"
            phase4_result["error"] = str(e)
            warnings.append("Failed to send verification notification")
    else:
        phase4_result["status"] = "skipped"
        phase4_result["reason"] = "Installation failed"

    phases.append(phase4_result)

    return {"phases": phases, "success": overall_success, "warnings": warnings}


def _cmd_notify(args: argparse.Namespace) -> dict:
    """Handle 'notify' subcommand."""
    agents = [a.strip() for a in args.agents.split(",") if a.strip()]

    if not agents:
        return {"error": "No agents specified"}

    return notify_agents(
        agents=agents,
        operation=args.operation,
        message=args.message,
        require_ack=args.require_ack,
    )


def _cmd_wait_ack(args: argparse.Namespace) -> dict:
    """Handle 'wait-ack' subcommand."""
    start = datetime.now(timezone.utc).isoformat()

    result = wait_for_acknowledgment(
        agent=args.agent, timeout=args.timeout, remind_interval=args.remind
    )

    end = datetime.now(timezone.utc).isoformat()

    return {
        "agent": args.agent,
        "acknowledged": result,
        "timeout_seconds": args.timeout,
        "remind_interval_seconds": args.remind,
        "started": start,
        "completed": end,
    }


def _cmd_broadcast(args: argparse.Namespace) -> dict:
    """Handle 'broadcast' subcommand."""
    agents = None
    if args.agents:
        agents = [a.strip() for a in args.agents.split(",") if a.strip()]

    return broadcast_notification(
        subject=args.subject,
        message=args.message,
        priority=args.priority,
        agents=agents,
        role=args.role,
        project=args.project,
    )


def _cmd_install_skill(args: argparse.Namespace) -> dict:
    """Handle 'install-skill' subcommand."""
    return skill_install_with_notification(
        agent=args.agent,
        skill=args.skill,
        marketplace=args.marketplace,
        wait_for_ok=args.wait_for_ok,
    )


def main() -> int:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Notification Protocol for Chief of Staff - Agent Communication via AI Maestro",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Notify multiple agents about an operation
  python ecos_notification_protocol.py notify --agents agent1,agent2 --operation install --message "Installing skill X"

  # Wait for acknowledgment from an agent
  python ecos_notification_protocol.py wait-ack --agent agent1 --timeout 120 --remind 30

  # Broadcast to all agents matching criteria
  python ecos_notification_protocol.py broadcast --subject "Update" --message "System maintenance" --priority high

  # Install skill with notification workflow
  python ecos_notification_protocol.py install-skill --agent agent1 --skill my-skill --marketplace emasoft-plugins
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 'notify' subcommand
    notify_parser = subparsers.add_parser(
        "notify", help="Send notification to multiple agents"
    )
    notify_parser.add_argument(
        "--agents",
        "-a",
        required=True,
        help="Comma-separated list of agent session names",
    )
    notify_parser.add_argument(
        "--operation",
        "-o",
        required=True,
        help="Operation name (e.g., install, update, restart)",
    )
    notify_parser.add_argument(
        "--message", "-m", required=True, help="Notification message content"
    )
    notify_parser.add_argument(
        "--require-ack", action="store_true", help="Request acknowledgment from agents"
    )

    # 'wait-ack' subcommand
    wait_parser = subparsers.add_parser(
        "wait-ack", help="Wait for acknowledgment from an agent"
    )
    wait_parser.add_argument(
        "--agent", "-a", required=True, help="Agent session name to wait for"
    )
    wait_parser.add_argument(
        "--timeout",
        "-t",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Timeout in seconds (default: {DEFAULT_TIMEOUT})",
    )
    wait_parser.add_argument(
        "--remind",
        "-r",
        type=int,
        default=DEFAULT_REMIND_INTERVAL,
        help=f"Reminder interval in seconds (default: {DEFAULT_REMIND_INTERVAL})",
    )

    # 'broadcast' subcommand
    broadcast_parser = subparsers.add_parser(
        "broadcast", help="Broadcast notification to agents"
    )
    broadcast_parser.add_argument(
        "--subject", "-s", required=True, help="Message subject"
    )
    broadcast_parser.add_argument(
        "--message", "-m", required=True, help="Message content"
    )
    broadcast_parser.add_argument(
        "--priority",
        "-p",
        choices=["low", "normal", "high", "urgent"],
        default="normal",
        help="Message priority (default: normal)",
    )
    broadcast_parser.add_argument(
        "--agents",
        "-a",
        help="Comma-separated list of specific agents (overrides role/project filters)",
    )
    broadcast_parser.add_argument("--role", help="Filter agents by role")
    broadcast_parser.add_argument("--project", help="Filter agents by project")

    # 'install-skill' subcommand
    install_parser = subparsers.add_parser(
        "install-skill", help="Install skill with notification workflow"
    )
    install_parser.add_argument(
        "--agent", "-a", required=True, help="Target agent session name"
    )
    install_parser.add_argument(
        "--skill", "-s", required=True, help="Skill name to install"
    )
    install_parser.add_argument(
        "--marketplace", "-k", help="Marketplace name (optional)"
    )
    install_parser.add_argument(
        "--wait-for-ok",
        action="store_true",
        default=True,
        help="Wait for acknowledgment before installing (default: True)",
    )
    install_parser.add_argument(
        "--no-wait",
        dest="wait_for_ok",
        action="store_false",
        help="Do not wait for acknowledgment",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Execute the appropriate command
    try:
        if args.command == "notify":
            result = _cmd_notify(args)
        elif args.command == "wait-ack":
            result = _cmd_wait_ack(args)
        elif args.command == "broadcast":
            result = _cmd_broadcast(args)
        elif args.command == "install-skill":
            result = _cmd_install_skill(args)
        else:
            result = {"error": f"Unknown command: {args.command}"}

        # Output JSON result
        print(json.dumps(result, indent=2))

        # Return appropriate exit code
        if "error" in result:
            return 1
        if result.get("success") is False:
            return 1
        return 0

    except KeyboardInterrupt:
        print(json.dumps({"error": "Interrupted by user"}))
        return 130
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
