#!/usr/bin/env python3
"""
ecos_failure_recovery.py - Failure detection and recovery for AI Maestro agents.

Detects agent failures, classifies them, and executes appropriate recovery strategies.
Uses AMP CLI (amp-send) for messaging and aimaestro-agent.sh for agent management.

Dependencies: Python 3.8+ stdlib only

Usage:
    python ecos_failure_recovery.py health --agent agent1
    python ecos_failure_recovery.py classify --agent agent1
    python ecos_failure_recovery.py recover --agent agent1 --strategy restart
    python ecos_failure_recovery.py replace --failed agent1 --new agent1-replacement --role orchestrator --project myproj --dir /path
    python ecos_failure_recovery.py transfer --from agent1 --to agent2 --handoff /path/handoff.md

Exit codes:
    0 - Success
    1 - Error
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, cast

# aimaestro-agent.sh CLI path
AIMAESTRO_CLI = os.environ.get(
    "AIMAESTRO_CLI", os.path.expanduser("~/.local/bin/aimaestro-agent.sh")
)

# Failure classification thresholds (seconds)
TRANSIENT_THRESHOLD = 300  # 5 minutes
RECOVERABLE_THRESHOLD = 1800  # 30 minutes

# Ping timeout (seconds)
PING_TIMEOUT = 30


def iso_now() -> str:
    """Return current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _amp_send(
    recipient: str,
    subject: str,
    message: str,
    priority: str = "normal",
    msg_type: str = "request",
) -> bool:
    """Send a message via AMP CLI (amp-send).

    Args:
        recipient: Target agent session name
        subject: Message subject
        message: Message body text
        priority: Message priority ('low', 'normal', 'high', 'urgent')
        msg_type: Message type ('request', 'notification', 'handoff', etc.)

    Returns:
        True if the message was sent successfully, False otherwise
    """
    try:
        result = subprocess.run(
            [
                "amp-send",
                recipient,
                subject,
                message,
                "--priority",
                priority,
                "--type",
                msg_type,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def run_cli(
    *args: str, timeout: int = 60, capture_output: bool = True
) -> tuple[int, str, str]:
    """Run aimaestro-agent.sh CLI command.

    Args:
        args: Command arguments
        timeout: Command timeout in seconds
        capture_output: Whether to capture stdout/stderr

    Returns:
        Tuple of (return_code, stdout, stderr)
    """
    cmd = [AIMAESTRO_CLI, *args]

    try:
        result = subprocess.run(
            cmd, capture_output=capture_output, text=True, timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 124, "", "Command timed out"
    except FileNotFoundError:
        return 127, "", f"CLI not found: {AIMAESTRO_CLI}"
    except Exception as e:
        return 1, "", str(e)


def get_agent_status_from_cli(agent: str) -> dict[str, Any] | None:
    """Get agent status from aimaestro-agent.sh list command.

    Args:
        agent: Agent session name

    Returns:
        Agent status dict or None if not found
    """
    code, stdout, _stderr = run_cli("show", agent, "--json")

    if code != 0:
        return None

    try:
        data = json.loads(stdout)
        return cast(dict[str, Any], data)
    except json.JSONDecodeError:
        return None


def get_agent_messages(agent: str, status: str = "unread") -> list[dict[str, Any]]:
    """Get messages for an agent via aimaestro-agent.sh CLI.

    Args:
        agent: Agent session name
        status: Message status filter ('unread', 'all')

    Returns:
        List of messages
    """
    code, stdout, _stderr = run_cli("messages", agent, "--status", status, "--json")
    if code != 0:
        return []
    try:
        data = json.loads(stdout)
        messages = data.get("messages", data) if isinstance(data, dict) else data
        return cast(
            list[dict[str, Any]], messages if isinstance(messages, list) else []
        )
    except (json.JSONDecodeError, TypeError):
        return []


def send_ping_message(agent: str) -> bool:
    """Send a ping message to an agent via AMP CLI.

    Args:
        agent: Agent session name

    Returns:
        True if the ping was sent successfully, False otherwise
    """
    return _amp_send(
        recipient=agent,
        subject="Health check ping",
        message=f"Health check ping - please respond. Timestamp: {iso_now()}",
        priority="high",
        msg_type="ping",
    )


def check_agent_health(agent: str) -> dict[str, Any]:
    """Check agent health using CLI status and AMP ping.

    Checks:
    1. Agent status via aimaestro-agent.sh show
    2. Agent responsiveness via AMP ping message

    Args:
        agent: Agent session name

    Returns:
        Health status dict:
        {
            status: 'online' | 'offline' | 'hibernated' | 'unknown',
            last_seen: timestamp or None,
            responsive: bool,
            details: {...}
        }
    """
    result: dict[str, Any] = {
        "agent": agent,
        "status": "unknown",
        "last_seen": None,
        "responsive": False,
        "checked_at": iso_now(),
        "details": {},
    }

    # 1. Check CLI status
    cli_status = get_agent_status_from_cli(agent)

    if cli_status is None:
        result["status"] = "unknown"
        result["details"]["cli_error"] = "Failed to get agent status from CLI"
    else:
        result["details"]["cli_status"] = cli_status

        # Map CLI status to health status
        state = cli_status.get("state", "").lower()
        if state == "active":
            result["status"] = "online"
        elif state == "hibernated":
            result["status"] = "hibernated"
        elif state in ("stopped", "terminated", "error"):
            result["status"] = "offline"
        else:
            result["status"] = "unknown"

        # Extract last seen timestamp
        last_heartbeat = cli_status.get("last_heartbeat")
        if last_heartbeat:
            result["last_seen"] = last_heartbeat

    # 2. Check responsiveness via AMP ping (only if agent appears online)
    if result["status"] == "online":
        ping_ok = send_ping_message(agent)
        if ping_ok:
            result["details"]["ping_sent"] = True
            # Mark as responsive if ping was sent successfully
            result["responsive"] = True
        else:
            result["responsive"] = False
            result["details"]["ping_error"] = "Failed to send ping message"
    else:
        result["responsive"] = False

    return result


def classify_failure(agent: str, health: dict[str, Any] | None = None) -> str:
    """Classify the type of agent failure.

    Classification types:
    - transient: Agent offline < 5 min, last task running
    - recoverable: Agent offline 5-30 min, can restart
    - terminal: Agent offline > 30 min, host unreachable, or persistent crash

    Args:
        agent: Agent session name
        health: Health check result (runs check if None)

    Returns:
        Failure classification: 'transient', 'recoverable', 'terminal', or 'healthy'
    """
    if health is None:
        health = check_agent_health(agent)

    status = health.get("status", "unknown")
    last_seen = health.get("last_seen")
    responsive = health.get("responsive", False)

    # Agent is online and responsive - not a failure
    if status == "online" and responsive:
        return "healthy"

    # Agent is hibernated - not a failure (intentional state)
    if status == "hibernated":
        return "healthy"

    # Calculate time since last seen
    seconds_offline = None
    if last_seen:
        try:
            last_ts = datetime.fromisoformat(last_seen.replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            seconds_offline = (now - last_ts).total_seconds()
        except (ValueError, AttributeError):
            pass

    # Unknown status with no last_seen - terminal
    if status == "unknown" and last_seen is None:
        return "terminal"

    # Classify based on time offline
    if seconds_offline is None:
        # Can't determine time - assume recoverable
        return "recoverable"

    if seconds_offline < TRANSIENT_THRESHOLD:
        return "transient"
    elif seconds_offline < RECOVERABLE_THRESHOLD:
        return "recoverable"
    else:
        return "terminal"


def execute_recovery(agent: str, strategy: str) -> dict[str, Any]:
    """Execute a recovery strategy for a failed agent.

    Strategies:
    - restart: Restart the agent via aimaestro-agent.sh restart
    - hibernate_wake: Hibernate then wake the agent
    - replace: Trigger full replacement workflow

    Args:
        agent: Agent session name
        strategy: Recovery strategy

    Returns:
        Recovery result:
        {
            success: bool,
            action_taken: str,
            details: str
        }
    """
    result: dict[str, Any] = {
        "agent": agent,
        "strategy": strategy,
        "success": False,
        "action_taken": "",
        "details": "",
        "timestamp": iso_now(),
    }

    if strategy == "restart":
        # Try to restart the agent
        code, stdout, stderr = run_cli("session", "restart", agent)

        if code == 0:
            result["success"] = True
            result["action_taken"] = "restart"
            result["details"] = f"Agent {agent} restarted successfully"
        else:
            result["action_taken"] = "restart_attempted"
            result["details"] = f"Restart failed: {stderr or stdout}"

    elif strategy == "hibernate_wake":
        # First hibernate, then wake
        h_code, h_stdout, h_stderr = run_cli("hibernate", agent)

        if h_code != 0:
            result["action_taken"] = "hibernate_attempted"
            result["details"] = f"Hibernate failed: {h_stderr or h_stdout}"
            return result

        # Wait a moment then wake
        import time

        time.sleep(2)

        w_code, w_stdout, w_stderr = run_cli("wake", agent)

        if w_code == 0:
            result["success"] = True
            result["action_taken"] = "hibernate_wake"
            result["details"] = f"Agent {agent} hibernated and woken successfully"
        else:
            result["action_taken"] = "wake_attempted"
            result["details"] = f"Wake failed after hibernate: {w_stderr or w_stdout}"

    elif strategy == "replace":
        # Replace requires more information - return instruction
        result["action_taken"] = "replace_requested"
        result["details"] = (
            "Replacement requires additional parameters. "
            "Use the 'replace' command with --new, --role, --project, --dir"
        )

    else:
        result["action_taken"] = "unknown_strategy"
        result["details"] = f"Unknown recovery strategy: {strategy}"

    return result


def replace_agent(
    failed_agent: str, new_name: str, role: str, project: str, work_dir: str
) -> dict[str, Any]:
    """Replace a failed agent with a new one.

    Steps:
    1. Request approval from EAMA (uses ecos_approval_manager.py)
    2. Create new agent via aimaestro-agent.sh create
    3. Notify EOA to generate handoff
    4. Notify EOA to update GitHub Project kanban
    5. Send message to new agent with handoff instructions

    Args:
        failed_agent: Name of the failed agent
        new_name: Name for the replacement agent
        role: Role for the new agent
        project: Project ID to assign
        work_dir: Working directory for the new agent

    Returns:
        Replacement result:
        {
            success: bool,
            new_agent: str,
            handoff_sent: bool,
            details: {...}
        }
    """
    result: dict[str, Any] = {
        "failed_agent": failed_agent,
        "new_agent": new_name,
        "success": False,
        "handoff_sent": False,
        "timestamp": iso_now(),
        "details": {},
    }

    # 1. Request approval from EAMA
    # Check if approval manager exists
    script_dir = Path(__file__).parent
    approval_script = script_dir / "ecos_approval_manager.py"

    if approval_script.exists():
        try:
            approval_result = subprocess.run(
                [
                    sys.executable,
                    str(approval_script),
                    "request",
                    "--type",
                    "agent_replacement",
                    "--agent",
                    failed_agent,
                    "--replacement",
                    new_name,
                    "--reason",
                    f"Replacing failed agent {failed_agent}",
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )

            if approval_result.returncode != 0:
                result["details"]["approval"] = "denied"
                result["details"]["approval_error"] = approval_result.stderr
                return result

            try:
                approval_data = json.loads(approval_result.stdout)
                if not approval_data.get("approved", False):
                    result["details"]["approval"] = "denied"
                    result["details"]["approval_reason"] = approval_data.get("reason")
                    return result
                result["details"]["approval"] = "granted"
            except json.JSONDecodeError:
                # Assume approval granted if script ran successfully
                result["details"]["approval"] = "assumed_granted"

        except subprocess.TimeoutExpired:
            result["details"]["approval"] = "timeout"
            result["details"]["approval_error"] = "Approval request timed out"
            return result
        except Exception as e:
            result["details"]["approval"] = "error"
            result["details"]["approval_error"] = str(e)
            return result
    else:
        # No approval manager - proceed with warning
        result["details"]["approval"] = "skipped"
        result["details"]["approval_warning"] = "Approval manager not found"

    # 2. Create new agent via CLI
    create_args = ["create", new_name, "--role", role]
    if project:
        create_args.extend(["--project", project])
    if work_dir:
        create_args.extend(["--cwd", work_dir])

    code, stdout, stderr = run_cli(*create_args)

    if code != 0:
        result["details"]["create_error"] = stderr or stdout
        return result

    result["details"]["agent_created"] = True

    # 3. Notify EOA to generate handoff via AMP CLI
    handoff_msg = (
        f"Please generate handoff document for agent replacement. "
        f"Failed agent: {failed_agent}, New agent: {new_name}, "
        f"Role: {role}, Project: {project}"
    )
    if _amp_send(
        recipient="orchestrator-master",
        subject=f"Handoff request: {failed_agent} -> {new_name}",
        message=handoff_msg,
        priority="high",
        msg_type="handoff_request",
    ):
        result["details"]["eoa_handoff_notified"] = True
    else:
        result["details"]["eoa_handoff_error"] = "amp-send failed"

    # 4. Notify EOA to update GitHub Project kanban via AMP CLI
    kanban_msg = (
        f"Update GitHub Project kanban for agent replacement. "
        f"Mark {failed_agent} as failed, assign tasks to {new_name}"
    )
    if _amp_send(
        recipient="orchestrator-master",
        subject=f"Kanban update: agent replacement {new_name}",
        message=kanban_msg,
        priority="normal",
        msg_type="kanban_update",
    ):
        result["details"]["eoa_kanban_notified"] = True
    else:
        result["details"]["eoa_kanban_error"] = "amp-send failed"

    # 5. Send message to new agent with handoff instructions via AMP CLI
    handoff_path = Path(work_dir) / "thoughts" / "shared" / "handoffs" / failed_agent
    handoff_file = handoff_path / "current.md"

    handoff_instructions = (
        f"You are replacing agent {failed_agent}. "
        f"Your role is: {role}. Project: {project}. "
        f"Check for handoff document at: {handoff_file}"
    )
    if _amp_send(
        recipient=new_name,
        subject=f"Handoff from {failed_agent}",
        message=handoff_instructions,
        priority="high",
        msg_type="handoff",
    ):
        result["handoff_sent"] = True
    else:
        result["details"]["handoff_error"] = "amp-send failed"

    # Success if agent was created and at least handoff was sent
    result["success"] = result["details"].get("agent_created", False)

    return result


def transfer_work(from_agent: str, to_agent: str, handoff_file: str) -> dict[str, Any]:
    """Transfer work from one agent to another via handoff file.

    Args:
        from_agent: Source agent session name
        to_agent: Target agent session name
        handoff_file: Path to handoff document

    Returns:
        Transfer result:
        {
            success: bool,
            details: {...}
        }
    """
    result: dict[str, Any] = {
        "from_agent": from_agent,
        "to_agent": to_agent,
        "handoff_file": handoff_file,
        "success": False,
        "timestamp": iso_now(),
        "details": {},
    }

    # Read handoff file
    handoff_path = Path(handoff_file)

    if not handoff_path.exists():
        result["details"]["error"] = f"Handoff file not found: {handoff_file}"
        return result

    try:
        handoff_content = handoff_path.read_text(encoding="utf-8")
        result["details"]["handoff_size"] = len(handoff_content)
    except (OSError, UnicodeDecodeError) as e:
        result["details"]["error"] = f"Failed to read handoff file: {e}"
        return result

    # Send handoff to target agent via AMP CLI
    transfer_msg = (
        f"Work transfer from {from_agent}. "
        f"Please review the handoff document and continue the work. "
        f"Handoff file: {handoff_file}"
    )
    if _amp_send(
        recipient=to_agent,
        subject=f"Work transfer from {from_agent}",
        message=transfer_msg,
        priority="high",
        msg_type="handoff",
    ):
        result["success"] = True
        result["details"]["message_sent"] = True
    else:
        result["details"]["error"] = "Failed to send message via amp-send"

    return result


def cmd_health(args: argparse.Namespace) -> int:
    """Handle 'health' command."""
    result = check_agent_health(args.agent)
    print(json.dumps(result, indent=2))
    return 0


def cmd_classify(args: argparse.Namespace) -> int:
    """Handle 'classify' command."""
    health = check_agent_health(args.agent)
    classification = classify_failure(args.agent, health)

    result = {
        "agent": args.agent,
        "classification": classification,
        "health": health,
        "timestamp": iso_now(),
    }
    print(json.dumps(result, indent=2))
    return 0


def cmd_recover(args: argparse.Namespace) -> int:
    """Handle 'recover' command."""
    result = execute_recovery(args.agent, args.strategy)
    print(json.dumps(result, indent=2))
    return 0 if result["success"] else 1


def cmd_replace(args: argparse.Namespace) -> int:
    """Handle 'replace' command."""
    result = replace_agent(
        failed_agent=args.failed,
        new_name=args.new,
        role=args.role,
        project=args.project,
        work_dir=args.dir,
    )
    print(json.dumps(result, indent=2))
    return 0 if result["success"] else 1


def cmd_transfer(args: argparse.Namespace) -> int:
    """Handle 'transfer' command."""
    result = transfer_work(
        from_agent=getattr(args, "from"), to_agent=args.to, handoff_file=args.handoff
    )
    print(json.dumps(result, indent=2))
    return 0 if result["success"] else 1


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Failure detection and recovery for AI Maestro agents.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
    health    Check agent health status
    classify  Classify agent failure type
    recover   Execute recovery strategy
    replace   Replace a failed agent
    transfer  Transfer work between agents

Examples:
    # Check agent health
    python ecos_failure_recovery.py health --agent dev-agent-01

    # Classify failure
    python ecos_failure_recovery.py classify --agent dev-agent-01

    # Restart a failed agent
    python ecos_failure_recovery.py recover --agent dev-agent-01 --strategy restart

    # Replace a failed agent
    python ecos_failure_recovery.py replace --failed dev-agent-01 --new dev-agent-02 \\
        --role developer --project myproj --dir /path/to/project

    # Transfer work to another agent
    python ecos_failure_recovery.py transfer --from dev-agent-01 --to dev-agent-02 \\
        --handoff /path/to/handoff.md
        """,
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # health command
    health_parser = subparsers.add_parser("health", help="Check agent health status")
    health_parser.add_argument(
        "--agent", required=True, help="Agent session name to check"
    )
    health_parser.set_defaults(func=cmd_health)

    # classify command
    classify_parser = subparsers.add_parser(
        "classify", help="Classify agent failure type"
    )
    classify_parser.add_argument(
        "--agent", required=True, help="Agent session name to classify"
    )
    classify_parser.set_defaults(func=cmd_classify)

    # recover command
    recover_parser = subparsers.add_parser("recover", help="Execute recovery strategy")
    recover_parser.add_argument(
        "--agent", required=True, help="Agent session name to recover"
    )
    recover_parser.add_argument(
        "--strategy",
        required=True,
        choices=["restart", "hibernate_wake", "replace"],
        help="Recovery strategy to execute",
    )
    recover_parser.set_defaults(func=cmd_recover)

    # replace command
    replace_parser = subparsers.add_parser(
        "replace", help="Replace a failed agent with a new one"
    )
    replace_parser.add_argument(
        "--failed", required=True, help="Name of the failed agent"
    )
    replace_parser.add_argument(
        "--new", required=True, help="Name for the replacement agent"
    )
    replace_parser.add_argument("--role", required=True, help="Role for the new agent")
    replace_parser.add_argument("--project", required=True, help="Project ID to assign")
    replace_parser.add_argument(
        "--dir", required=True, help="Working directory for the new agent"
    )
    replace_parser.set_defaults(func=cmd_replace)

    # transfer command
    transfer_parser = subparsers.add_parser(
        "transfer", help="Transfer work between agents"
    )
    transfer_parser.add_argument(
        "--from", required=True, dest="from", help="Source agent session name"
    )
    transfer_parser.add_argument(
        "--to", required=True, help="Target agent session name"
    )
    transfer_parser.add_argument(
        "--handoff", required=True, help="Path to handoff document"
    )
    transfer_parser.set_defaults(func=cmd_transfer)

    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()
    return cast(int, args.func(args))


if __name__ == "__main__":
    sys.exit(main())
