#!/usr/bin/env python3
"""
Chief of Staff Notify Agent Script

Sends an AI Maestro message to a registered agent.

Usage:
    python3 am_notify_agent.py implementer-1 --subject "Update" --message "Requirements changed"
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

# State file location
EXEC_STATE_FILE = Path("design/exec-phase.local.md")


def parse_frontmatter(file_path: Path) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter and return (data, body)."""
    if not file_path.exists():
        return {}, ""

    content = file_path.read_text(encoding="utf-8")

    if not content.startswith("---"):
        return {}, content

    end_index = content.find("---", 3)
    if end_index == -1:
        return {}, content

    yaml_content = content[3:end_index].strip()
    body = content[end_index + 3 :].strip()

    try:
        data = yaml.safe_load(yaml_content) or {}
        return data, body
    except yaml.YAMLError:
        return {}, content


def find_agent_session(data: dict[str, Any], agent_id: str) -> str | None:
    """Find the session name for an AI agent."""
    agents = data.get("registered_agents", {})
    for agent in agents.get("ai_agents", []):
        if agent.get("agent_id") == agent_id:
            session = agent.get("session_name")
            return str(session) if session else None
    return None


def send_ai_maestro_message(
    session_name: str,
    subject: str,
    message: str,
    priority: str = "normal",
    msg_type: str = "notification",
) -> bool:
    """Send a message via AI Maestro using the AMP CLI."""
    try:
        result = subprocess.run(
            [
                "amp-send",
                session_name,
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
    except Exception as e:
        print(f"Error: {e}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Send AI Maestro message to a registered agent"
    )
    parser.add_argument("agent_id", help="ID of the registered AI agent")
    parser.add_argument("--subject", "-s", required=True, help="Message subject")
    parser.add_argument("--message", "-m", required=True, help="Message content")
    parser.add_argument(
        "--priority",
        "-p",
        choices=["low", "normal", "high", "urgent"],
        default="normal",
        help="Message priority",
    )
    parser.add_argument(
        "--type",
        "-t",
        dest="msg_type",
        default="notification",
        help="Message type (notification, task_assignment, progress_poll, etc.)",
    )

    args = parser.parse_args()

    # Check if in orchestration phase
    if not EXEC_STATE_FILE.exists():
        print("ERROR: Not in Orchestration Phase")
        return 1

    data, _ = parse_frontmatter(EXEC_STATE_FILE)
    if not data:
        print("ERROR: Could not parse orchestration state file")
        return 1

    # Find agent session
    session = find_agent_session(data, args.agent_id)
    if not session:
        # Check if it's a human agent
        agents = data.get("registered_agents", {})
        for dev in agents.get("human_developers", []):
            if dev.get("github_username") == args.agent_id:
                print(f"ERROR: '{args.agent_id}' is a human developer")
                print("Use GitHub notifications for human agents")
                return 1

        print(f"ERROR: Agent '{args.agent_id}' not registered")
        return 1

    # Send message
    print(f"Sending message to {args.agent_id} ({session})...")
    sent = send_ai_maestro_message(
        session, args.subject, args.message, args.priority, args.msg_type
    )

    if sent:
        print("✓ Message sent successfully")
        print(f"  Subject: {args.subject}")
        print(f"  Priority: {args.priority}")
        return 0
    else:
        print("✗ Failed to send message")
        print("  Check AI Maestro service status")
        return 1


if __name__ == "__main__":
    sys.exit(main())
