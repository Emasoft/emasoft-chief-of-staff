#!/usr/bin/env python3
"""
ecos_approval_manager.py - Approval Request Manager for ECOS

Manages approval requests for operations that require authorization.
Uses AI Maestro API for inter-agent communication and YAML files for state persistence.

Part of the emasoft-chief-of-staff plugin.
"""

import argparse
import json
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

APPROVALS_DIR = ".claude/approvals"
PENDING_DIR = f"{APPROVALS_DIR}/pending"
COMPLETED_DIR = f"{APPROVALS_DIR}/completed"


def get_project_root() -> Path:
    """Get the project root directory from environment or current directory."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    return Path(project_dir)


def ensure_directories() -> None:
    """Ensure approval directories exist."""
    root = get_project_root()
    (root / PENDING_DIR).mkdir(parents=True, exist_ok=True)
    (root / COMPLETED_DIR).mkdir(parents=True, exist_ok=True)


def generate_request_id() -> str:
    """Generate a unique request ID using UUID4."""
    return str(uuid.uuid4())


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def dict_to_yaml(data: dict[str, Any], indent: int = 0) -> str:
    """
    Convert a dictionary to YAML format string.
    Simple implementation using only stdlib - handles basic types.
    """
    lines = []
    prefix = "  " * indent

    for key, value in data.items():
        if value is None:
            lines.append(f"{prefix}{key}: null")
        elif isinstance(value, bool):
            lines.append(f"{prefix}{key}: {str(value).lower()}")
        elif isinstance(value, (int, float)):
            lines.append(f"{prefix}{key}: {value}")
        elif isinstance(value, str):
            # Handle multiline strings
            if "\n" in value:
                lines.append(f"{prefix}{key}: |")
                for line in value.split("\n"):
                    lines.append(f"{prefix}  {line}")
            elif any(c in value for c in [":", "#", "'", '"', "[", "]", "{", "}"]):
                # Quote strings with special characters
                escaped = value.replace('"', '\\"')
                lines.append(f'{prefix}{key}: "{escaped}"')
            else:
                lines.append(f"{prefix}{key}: {value}")
        elif isinstance(value, list):
            if not value:
                lines.append(f"{prefix}{key}: []")
            else:
                lines.append(f"{prefix}{key}:")
                for item in value:
                    if isinstance(item, dict):
                        lines.append(f"{prefix}  -")
                        nested = dict_to_yaml(item, indent + 2)
                        lines.append(nested)
                    else:
                        lines.append(f"{prefix}  - {item}")
        elif isinstance(value, dict):
            if not value:
                lines.append(f"{prefix}{key}: {{}}")
            else:
                lines.append(f"{prefix}{key}:")
                nested = dict_to_yaml(value, indent + 1)
                lines.append(nested)
        else:
            lines.append(f"{prefix}{key}: {value}")

    return "\n".join(lines)


def yaml_to_dict(yaml_str: str) -> dict[str, Any]:
    """
    Parse a simple YAML string to dictionary.
    Simple implementation using only stdlib - handles basic types.
    """
    result: dict[str, Any] = {}
    _current_key: Optional[str] = None
    current_indent = 0
    multiline_key: Optional[str] = None
    multiline_lines: list[str] = []
    list_key: Optional[str] = None
    list_items: list[Any] = []

    lines = yaml_str.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip empty lines and comments
        if not stripped or stripped.startswith("#"):
            i += 1
            continue

        # Handle multiline continuation
        if multiline_key is not None:
            indent = len(line) - len(line.lstrip())
            if indent > current_indent and stripped:
                multiline_lines.append(stripped)
                i += 1
                continue
            else:
                result[multiline_key] = "\n".join(multiline_lines)
                multiline_key = None
                multiline_lines = []

        # Handle list items
        if stripped.startswith("- "):
            if list_key is not None:
                item = stripped[2:].strip()
                # Try to parse the value
                list_items.append(parse_yaml_value(item))
            i += 1
            continue

        # End list if we're no longer in list items
        if list_key is not None and not stripped.startswith("-"):
            result[list_key] = list_items
            list_key = None
            list_items = []

        # Parse key: value pairs
        if ":" in stripped:
            colon_idx = stripped.index(":")
            key = stripped[:colon_idx].strip()
            value_part = stripped[colon_idx + 1 :].strip()

            if value_part == "":
                # Could be start of a nested structure or list
                list_key = key
                list_items = []
            elif value_part == "|":
                # Multiline string
                multiline_key = key
                current_indent = len(line) - len(line.lstrip())
            elif value_part == "[]":
                result[key] = []
            elif value_part == "{}":
                result[key] = {}
            else:
                result[key] = parse_yaml_value(value_part)

        i += 1

    # Handle any remaining list
    if list_key is not None:
        result[list_key] = list_items

    # Handle any remaining multiline
    if multiline_key is not None:
        result[multiline_key] = "\n".join(multiline_lines)

    return result


def parse_yaml_value(value: str) -> Any:
    """Parse a YAML value string to appropriate Python type."""
    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]

    # Handle special values
    if value.lower() == "null" or value == "~":
        return None
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False

    # Try integer
    try:
        return int(value)
    except ValueError:
        pass

    # Try float
    try:
        return float(value)
    except ValueError:
        pass

    return value


def save_approval_request(
    request_id: str, data: dict[str, Any], pending: bool = True
) -> Path:
    """Save an approval request to YAML file."""
    ensure_directories()
    root = get_project_root()

    directory = PENDING_DIR if pending else COMPLETED_DIR
    filepath = root / directory / f"{request_id}.yaml"

    yaml_content = dict_to_yaml(data)
    filepath.write_text(yaml_content, encoding="utf-8")

    return filepath


def load_approval_request(request_id: str) -> Optional[dict[str, Any]]:
    """Load an approval request from YAML file."""
    root = get_project_root()

    # Check pending first, then completed
    for directory in [PENDING_DIR, COMPLETED_DIR]:
        filepath = root / directory / f"{request_id}.yaml"
        if filepath.exists():
            yaml_content = filepath.read_text(encoding="utf-8")
            data = yaml_to_dict(yaml_content)
            data["_location"] = "pending" if directory == PENDING_DIR else "completed"
            return data

    return None


def send_aimaestro_message(
    to: str, subject: str, content: dict[str, Any], priority: str = "normal"
) -> bool:
    """Send a message via AMP CLI (amp-send)."""
    msg_type = "request"
    if isinstance(content, dict):
        msg_type = content.get("type", "request")
    message = (
        content.get("message", json.dumps(content))
        if isinstance(content, dict)
        else str(content)
    )

    try:
        result = subprocess.run(
            [
                "amp-send",
                to,
                subject,
                message,
                "--priority",
                priority,
                "--type",
                str(msg_type),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def get_aimaestro_messages(agent: str, status: str = "unread") -> list[dict[str, Any]]:
    """Get messages from AI Maestro via amp-send CLI.

    Note: amp-send is a send-only CLI. Message retrieval relies on
    file-based polling in wait_for_approval. This function returns an
    empty list as the AMP CLI does not support reading messages.
    """
    _ = agent
    _ = status
    return []


def create_approval_request(
    operation_type: str, agent_name: str, reason: str, requester: str
) -> dict[str, Any]:
    """
    Create a new approval request.

    Args:
        operation_type: Type of operation requiring approval (e.g., 'spawn', 'deploy', 'modify')
        agent_name: Name of the agent or resource involved
        reason: Reason for the request
        requester: Name of the requesting agent

    Returns:
        Dictionary with request_id and status
    """
    request_id = generate_request_id()
    timestamp = get_timestamp()

    request_data = {
        "request_id": request_id,
        "operation_type": operation_type,
        "agent_name": agent_name,
        "reason": reason,
        "requester": requester,
        "status": "pending",
        "created_at": timestamp,
        "updated_at": timestamp,
        "decision": None,
        "decision_comment": None,
        "decided_by": None,
        "decided_at": None,
    }

    # Save to pending directory
    filepath = save_approval_request(request_id, request_data, pending=True)

    # Send AI Maestro message to EAMA (Emasoft Assistant Manager Agent)
    message_content = {
        "type": "approval_request",
        "message": f"Approval requested for {operation_type} operation.\n\n"
        f"Request ID: {request_id}\n"
        f"Operation: {operation_type}\n"
        f"Agent/Resource: {agent_name}\n"
        f"Reason: {reason}\n"
        f"Requester: {requester}\n\n"
        f"Please respond with: ecos_approval_manager.py respond --id {request_id} --decision <approved|rejected> --comment <reason>",
        "request_id": request_id,
        "operation_type": operation_type,
        "agent_name": agent_name,
        "reason": reason,
        "requester": requester,
    }

    # Send to EAMA for approval routing
    message_sent = send_aimaestro_message(
        to="emasoft-assistant-manager-agent",
        subject=f"[APPROVAL] {operation_type}: {agent_name}",
        content=message_content,
        priority="high",
    )

    return {
        "success": True,
        "request_id": request_id,
        "status": "pending",
        "filepath": str(filepath),
        "message_sent": message_sent,
    }


def check_approval_status(request_id: str) -> dict[str, Any]:
    """
    Check the status of an approval request.

    Args:
        request_id: The UUID of the approval request

    Returns:
        Dictionary with status and request details
    """
    request_data = load_approval_request(request_id)

    if request_data is None:
        return {
            "success": False,
            "error": f"Request {request_id} not found",
            "status": "not_found",
        }

    return {
        "success": True,
        "request_id": request_id,
        "status": request_data.get("status", "unknown"),
        "operation_type": request_data.get("operation_type"),
        "agent_name": request_data.get("agent_name"),
        "reason": request_data.get("reason"),
        "requester": request_data.get("requester"),
        "created_at": request_data.get("created_at"),
        "decision": request_data.get("decision"),
        "decision_comment": request_data.get("decision_comment"),
        "decided_by": request_data.get("decided_by"),
        "decided_at": request_data.get("decided_at"),
        "location": request_data.get("_location", "unknown"),
    }


def list_pending_approvals() -> dict[str, Any]:
    """
    List all pending approval requests.

    Returns:
        Dictionary with list of pending requests
    """
    ensure_directories()
    root = get_project_root()
    pending_dir = root / PENDING_DIR

    pending_requests = []

    for filepath in pending_dir.glob("*.yaml"):
        try:
            yaml_content = filepath.read_text(encoding="utf-8")
            data = yaml_to_dict(yaml_content)
            pending_requests.append(
                {
                    "request_id": data.get("request_id", filepath.stem),
                    "operation_type": data.get("operation_type"),
                    "agent_name": data.get("agent_name"),
                    "reason": data.get("reason"),
                    "requester": data.get("requester"),
                    "created_at": data.get("created_at"),
                    "status": data.get("status", "pending"),
                }
            )
        except Exception as e:
            pending_requests.append({"request_id": filepath.stem, "error": str(e)})

    # Sort by created_at (newest first)
    pending_requests.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    return {
        "success": True,
        "count": len(pending_requests),
        "pending": pending_requests,
    }


def respond_to_approval(
    request_id: str, decision: str, comment: str, decided_by: str = "user"
) -> dict[str, Any]:
    """
    Respond to an approval request.

    Args:
        request_id: The UUID of the approval request
        decision: 'approved' or 'rejected'
        comment: Comment explaining the decision
        decided_by: Who made the decision

    Returns:
        Dictionary with result status
    """
    if decision not in ("approved", "rejected"):
        return {
            "success": False,
            "error": f"Invalid decision: {decision}. Must be 'approved' or 'rejected'.",
        }

    root = get_project_root()
    pending_path = root / PENDING_DIR / f"{request_id}.yaml"

    if not pending_path.exists():
        # Check if already completed
        completed_path = root / COMPLETED_DIR / f"{request_id}.yaml"
        if completed_path.exists():
            return {
                "success": False,
                "error": f"Request {request_id} has already been processed",
            }
        return {
            "success": False,
            "error": f"Request {request_id} not found in pending requests",
        }

    # Load existing request
    yaml_content = pending_path.read_text(encoding="utf-8")
    request_data = yaml_to_dict(yaml_content)

    # Update with decision
    timestamp = get_timestamp()
    request_data["status"] = decision
    request_data["decision"] = decision
    request_data["decision_comment"] = comment
    request_data["decided_by"] = decided_by
    request_data["decided_at"] = timestamp
    request_data["updated_at"] = timestamp

    # Save to completed directory
    completed_path = save_approval_request(request_id, request_data, pending=False)

    # Remove from pending
    pending_path.unlink()

    # Send notification to requester
    requester = request_data.get("requester", "unknown")
    operation_type = request_data.get("operation_type", "unknown")
    agent_name = request_data.get("agent_name", "unknown")

    message_content = {
        "type": "approval_response",
        "message": f"Your approval request has been {decision}.\n\n"
        f"Request ID: {request_id}\n"
        f"Operation: {operation_type}\n"
        f"Agent/Resource: {agent_name}\n"
        f"Decision: {decision.upper()}\n"
        f"Comment: {comment}\n"
        f"Decided by: {decided_by}",
        "request_id": request_id,
        "decision": decision,
        "comment": comment,
    }

    # Try to send to requester (may fail if requester is not a valid agent)
    notification_sent = send_aimaestro_message(
        to=requester,
        subject=f"[APPROVAL {decision.upper()}] {operation_type}: {agent_name}",
        content=message_content,
        priority="high",
    )

    return {
        "success": True,
        "request_id": request_id,
        "decision": decision,
        "comment": comment,
        "decided_by": decided_by,
        "filepath": str(completed_path),
        "notification_sent": notification_sent,
    }


def wait_for_approval(request_id: str, timeout_seconds: int = 120) -> dict[str, Any]:
    """
    Wait for an approval decision, polling AI Maestro for responses.

    Args:
        request_id: The UUID of the approval request
        timeout_seconds: Maximum time to wait (default 120 seconds)

    Returns:
        Dictionary with decision or timeout status
    """
    start_time = time.time()
    poll_interval = 5  # Check every 5 seconds

    # First verify the request exists
    request_data = load_approval_request(request_id)
    if request_data is None:
        return {
            "success": False,
            "error": f"Request {request_id} not found",
            "status": "not_found",
        }

    # If already decided, return immediately
    if request_data.get("status") in ("approved", "rejected"):
        return {
            "success": True,
            "request_id": request_id,
            "status": request_data.get("status"),
            "decision": request_data.get("decision"),
            "decision_comment": request_data.get("decision_comment"),
            "decided_by": request_data.get("decided_by"),
            "waited_seconds": 0,
        }

    requester = request_data.get("requester", "unknown")

    while True:
        elapsed = time.time() - start_time

        if elapsed >= timeout_seconds:
            return {
                "success": False,
                "request_id": request_id,
                "status": "timeout",
                "waited_seconds": int(elapsed),
                "message": f"No response received within {timeout_seconds} seconds",
            }

        # Check if status changed (someone responded via respond_to_approval)
        request_data = load_approval_request(request_id)
        if request_data and request_data.get("status") in ("approved", "rejected"):
            return {
                "success": True,
                "request_id": request_id,
                "status": request_data.get("status"),
                "decision": request_data.get("decision"),
                "decision_comment": request_data.get("decision_comment"),
                "decided_by": request_data.get("decided_by"),
                "waited_seconds": int(elapsed),
            }

        # Also check AI Maestro messages for direct responses
        messages = get_aimaestro_messages(requester, status="unread")
        for msg in messages:
            content = msg.get("content", {})
            if isinstance(content, dict):
                msg_request_id = content.get("request_id")
                if msg_request_id == request_id:
                    decision = content.get("decision")
                    if decision in ("approved", "rejected"):
                        # Process the response
                        comment = content.get("comment", "")
                        decided_by = msg.get("from", "unknown")

                        result = respond_to_approval(
                            request_id, decision, comment, decided_by
                        )
                        result["waited_seconds"] = int(elapsed)
                        return result

        time.sleep(poll_interval)


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="ECOS Approval Manager - Manage approval requests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s create --type spawn --agent my-agent --reason "Need for task X" --requester ecos
  %(prog)s status --id 12345678-1234-1234-1234-123456789abc
  %(prog)s list --status pending
  %(prog)s respond --id 12345678-1234-1234-1234-123456789abc --decision approved --comment "Go ahead"
  %(prog)s wait --id 12345678-1234-1234-1234-123456789abc --timeout 120
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create command
    create_parser = subparsers.add_parser(
        "create", help="Create a new approval request"
    )
    create_parser.add_argument(
        "--type", required=True, help="Operation type (e.g., spawn, deploy, modify)"
    )
    create_parser.add_argument("--agent", required=True, help="Agent or resource name")
    create_parser.add_argument("--reason", required=True, help="Reason for the request")
    create_parser.add_argument(
        "--requester", default="ecos", help="Requesting agent name (default: ecos)"
    )

    # Status command
    status_parser = subparsers.add_parser(
        "status", help="Check status of an approval request"
    )
    status_parser.add_argument("--id", required=True, help="Request UUID")

    # List command
    list_parser = subparsers.add_parser("list", help="List approval requests")
    list_parser.add_argument(
        "--status",
        default="pending",
        choices=["pending", "all"],
        help="Filter by status (default: pending)",
    )

    # Respond command
    respond_parser = subparsers.add_parser(
        "respond", help="Respond to an approval request"
    )
    respond_parser.add_argument("--id", required=True, help="Request UUID")
    respond_parser.add_argument(
        "--decision",
        required=True,
        choices=["approved", "rejected"],
        help="Approval decision",
    )
    respond_parser.add_argument(
        "--comment", required=True, help="Comment explaining the decision"
    )
    respond_parser.add_argument(
        "--decided-by", default="user", help="Who made the decision (default: user)"
    )

    # Wait command
    wait_parser = subparsers.add_parser("wait", help="Wait for approval decision")
    wait_parser.add_argument("--id", required=True, help="Request UUID")
    wait_parser.add_argument(
        "--timeout", type=int, default=120, help="Timeout in seconds (default: 120)"
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    result: dict[str, Any] = {}

    if args.command == "create":
        result = create_approval_request(
            operation_type=args.type,
            agent_name=args.agent,
            reason=args.reason,
            requester=args.requester,
        )

    elif args.command == "status":
        result = check_approval_status(args.id)

    elif args.command == "list":
        if args.status == "pending":
            result = list_pending_approvals()
        else:
            # List all (pending + completed)
            pending = list_pending_approvals()
            root = get_project_root()
            completed_dir = root / COMPLETED_DIR
            completed_requests = []

            if completed_dir.exists():
                for filepath in completed_dir.glob("*.yaml"):
                    try:
                        yaml_content = filepath.read_text(encoding="utf-8")
                        data = yaml_to_dict(yaml_content)
                        completed_requests.append(
                            {
                                "request_id": data.get("request_id", filepath.stem),
                                "operation_type": data.get("operation_type"),
                                "agent_name": data.get("agent_name"),
                                "status": data.get("status"),
                                "decision": data.get("decision"),
                                "created_at": data.get("created_at"),
                                "decided_at": data.get("decided_at"),
                            }
                        )
                    except Exception as e:
                        completed_requests.append(
                            {"request_id": filepath.stem, "error": str(e)}
                        )

            result = {
                "success": True,
                "pending_count": pending.get("count", 0),
                "completed_count": len(completed_requests),
                "pending": pending.get("pending", []),
                "completed": completed_requests,
            }

    elif args.command == "respond":
        result = respond_to_approval(
            request_id=args.id,
            decision=args.decision,
            comment=args.comment,
            decided_by=args.decided_by,
        )

    elif args.command == "wait":
        result = wait_for_approval(request_id=args.id, timeout_seconds=args.timeout)

    # Output JSON
    print(json.dumps(result, indent=2))

    # Exit with appropriate code
    if result.get("success", True):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
