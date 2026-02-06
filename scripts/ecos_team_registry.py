#!/usr/bin/env python3
"""
ECOS Team Registry Manager

Manages team registries for multi-project agent coordination.
Creates, updates, and publishes team-registry.json files.

Usage:
    python ecos_team_registry.py create --team <name> --repo <url> [--project-board <url>]
    python ecos_team_registry.py add-agent --team <name> --agent <agent-json>
    python ecos_team_registry.py remove-agent --team <name> --agent-name <name>
    python ecos_team_registry.py update-status --team <name> --agent-name <name> --status <status>
    python ecos_team_registry.py list --team <name>
    python ecos_team_registry.py publish --team <name> --repo-path <path>
    python ecos_team_registry.py validate --team <name>
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, cast

# Organization-wide agents (not team-specific)
ORGANIZATION_AGENTS = [
    {
        "name": "eama-assistant-manager",
        "role": "manager",
        "plugin": "emasoft-assistant-manager-agent",
        "host": "macbook-main",
        "ai_maestro_address": "eama-assistant-manager",
        "note": "Organization-wide, not team-specific"
    },
    {
        "name": "ecos-chief-of-staff",
        "role": "chief-of-staff",
        "plugin": "emasoft-chief-of-staff",
        "host": "macbook-main",
        "ai_maestro_address": "ecos-chief-of-staff",
        "note": "Organization-wide, not team-specific"
    }
]

# Default shared agents
DEFAULT_SHARED_AGENTS = [
    {
        "name": "emasoft-integrator",
        "role": "integrator",
        "plugin": "emasoft-integrator-agent",
        "host": "server-ci-01",
        "ai_maestro_address": "emasoft-integrator",
        "note": "Shared across multiple teams"
    }
]

# Role constraints - typed for mypy
class RoleConstraint:
    """Role constraint data."""
    def __init__(self, min_count: int, max_count: int, plugin: str):
        self.min = min_count
        self.max = max_count
        self.plugin = plugin

ROLE_CONSTRAINTS: dict[str, RoleConstraint] = {
    "orchestrator": RoleConstraint(1, 1, "emasoft-orchestrator-agent"),
    "architect": RoleConstraint(1, 1, "emasoft-architect-agent"),
    "integrator": RoleConstraint(0, 10, "emasoft-integrator-agent"),
    "programmer": RoleConstraint(1, 20, "emasoft-programmer-agent"),
}

# ECOS state directory
ECOS_STATE_DIR = Path.home() / ".ecos"
TEAMS_REGISTRY_FILE = ECOS_STATE_DIR / "all-teams.json"


def get_timestamp() -> str:
    """Get current ISO8601 timestamp."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_all_teams() -> dict[str, Any]:
    """Load the master list of all teams."""
    ECOS_STATE_DIR.mkdir(parents=True, exist_ok=True)
    if TEAMS_REGISTRY_FILE.exists():
        with open(TEAMS_REGISTRY_FILE) as f:
            return cast(dict[str, Any], json.load(f))
    return {"teams": {}, "last_updated": get_timestamp()}


def save_all_teams(data: dict[str, Any]) -> None:
    """Save the master list of all teams."""
    data["last_updated"] = get_timestamp()
    with open(TEAMS_REGISTRY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def validate_team_name(name: str) -> tuple[bool, str]:
    """Validate team name format: <repo>-<type>-team."""
    if not name.endswith("-team"):
        return False, "Team name must end with '-team'"

    parts = name.rsplit("-", 2)
    if len(parts) < 3:
        return False, "Team name must be: <repo-name>-<project-type>-team"

    # Check uniqueness
    all_teams = load_all_teams()
    if name in all_teams["teams"]:
        return False, f"Team name '{name}' already exists"

    return True, "Valid"


def create_team_registry(
    team_name: str,
    repo_url: str,
    project_board_url: str | None = None
) -> dict[str, Any]:
    """Create a new team registry."""

    # Validate team name
    valid, msg = validate_team_name(team_name)
    if not valid:
        raise ValueError(msg)

    timestamp = get_timestamp()

    registry = {
        "$schema": "https://emasoft.github.io/schemas/team-registry.v1.json",
        "version": "1.0.0",
        "team": {
            "name": team_name,
            "project": {
                "repository": repo_url,
                "github_project": project_board_url,
                "created_by": "eama-assistant-manager",
                "created_at": timestamp
            },
            "created_by": "ecos-chief-of-staff",
            "created_at": timestamp
        },
        "agents": [],
        "shared_agents": DEFAULT_SHARED_AGENTS.copy(),
        "organization_agents": ORGANIZATION_AGENTS.copy(),
        "github_bot": {
            "username": "emasoft-bot",
            "type": "shared-bot-account",
            "note": "All GitHub operations use this account. Real agent identity tracked in commit messages and PR bodies."
        },
        "contacts_last_updated": timestamp,
        "contacts_updated_by": "ecos-chief-of-staff"
    }

    # Register in master list
    all_teams = load_all_teams()
    all_teams["teams"][team_name] = {
        "repository": repo_url,
        "created_at": timestamp,
        "agent_count": 0
    }
    save_all_teams(all_teams)

    return registry


def add_agent_to_registry(
    registry: dict[str, Any],
    agent_name: str,
    role: str,
    plugin: str,
    host: str,
    ai_maestro_address: str | None = None
) -> dict[str, Any]:
    """Add an agent to the team registry."""

    # Validate role
    if role not in ROLE_CONSTRAINTS:
        raise ValueError(f"Invalid role: {role}. Valid roles: {list(ROLE_CONSTRAINTS.keys())}")

    # Check plugin matches role
    expected_plugin = ROLE_CONSTRAINTS[role].plugin
    if plugin != expected_plugin:
        raise ValueError(f"Role '{role}' requires plugin '{expected_plugin}', got '{plugin}'")

    # Check role count constraints
    current_count = sum(1 for a in registry["agents"] if a["role"] == role)
    max_count = ROLE_CONSTRAINTS[role].max
    if current_count >= max_count:
        raise ValueError(f"Cannot add more '{role}' agents. Max: {max_count}, Current: {current_count}")

    # Check agent name uniqueness
    existing_names = [a["name"] for a in registry["agents"]]
    if agent_name in existing_names:
        raise ValueError(f"Agent name '{agent_name}' already exists in team")

    # Default AI Maestro address to agent name
    if ai_maestro_address is None:
        ai_maestro_address = agent_name

    agent_entry = {
        "name": agent_name,
        "role": role,
        "plugin": plugin,
        "host": host,
        "ai_maestro_address": ai_maestro_address,
        "status": "active",
        "assigned_at": get_timestamp()
    }

    registry["agents"].append(agent_entry)
    registry["contacts_last_updated"] = get_timestamp()
    registry["contacts_updated_by"] = "ecos-chief-of-staff"

    return registry


def remove_agent_from_registry(
    registry: dict[str, Any],
    agent_name: str
) -> dict[str, Any]:
    """Remove an agent from the team registry."""

    # Find agent
    agent_idx = None
    for i, agent in enumerate(registry["agents"]):
        if agent["name"] == agent_name:
            agent_idx = i
            break

    if agent_idx is None:
        raise ValueError(f"Agent '{agent_name}' not found in team")

    # Check role constraints
    role = registry["agents"][agent_idx]["role"]
    current_count = sum(1 for a in registry["agents"] if a["role"] == role)
    min_count = ROLE_CONSTRAINTS[role].min

    if current_count <= min_count:
        raise ValueError(f"Cannot remove '{role}' agent. Min required: {min_count}, Current: {current_count}")

    # Remove
    registry["agents"].pop(agent_idx)
    registry["contacts_last_updated"] = get_timestamp()
    registry["contacts_updated_by"] = "ecos-chief-of-staff"

    return registry


def update_agent_status(
    registry: dict[str, Any],
    agent_name: str,
    new_status: str
) -> dict[str, Any]:
    """Update agent status in the registry."""

    valid_statuses = ["active", "hibernated", "offline", "terminated"]
    if new_status not in valid_statuses:
        raise ValueError(f"Invalid status: {new_status}. Valid: {valid_statuses}")

    # Find agent
    found = False
    for agent in registry["agents"]:
        if agent["name"] == agent_name:
            agent["status"] = new_status
            agent["status_updated_at"] = get_timestamp()
            found = True
            break

    if not found:
        raise ValueError(f"Agent '{agent_name}' not found in team")

    registry["contacts_last_updated"] = get_timestamp()
    registry["contacts_updated_by"] = "ecos-chief-of-staff"

    return registry


def validate_registry(registry: dict[str, Any]) -> list[str]:
    """Validate a team registry for completeness and constraints."""
    errors: list[str] = []

    # Check required fields
    if "team" not in registry:
        errors.append("Missing 'team' section")
    elif "name" not in registry["team"]:
        errors.append("Missing team name")

    if "agents" not in registry:
        errors.append("Missing 'agents' section")
        return errors

    # Check role constraints
    role_counts: dict[str, int] = {}
    for agent in registry["agents"]:
        role = agent.get("role", "unknown")
        role_counts[role] = role_counts.get(role, 0) + 1

        # Check required fields
        required_fields = ["name", "role", "plugin", "host", "ai_maestro_address", "status"]
        for field in required_fields:
            if field not in agent:
                errors.append(f"Agent '{agent.get('name', 'unknown')}' missing field: {field}")

    # Check min/max constraints
    for role, constraints in ROLE_CONSTRAINTS.items():
        count = role_counts.get(role, 0)
        min_required = constraints.min
        max_allowed = constraints.max
        if count < min_required:
            errors.append(f"Too few '{role}' agents: {count} < {min_required} (min)")
        if count > max_allowed:
            errors.append(f"Too many '{role}' agents: {count} > {max_allowed} (max)")

    return errors


def publish_registry_to_repo(registry: dict[str, Any], repo_path: str) -> str:
    """Publish team registry to the git repository."""

    repo_path_obj = Path(repo_path)
    emasoft_dir = repo_path_obj / ".emasoft"
    emasoft_dir.mkdir(parents=True, exist_ok=True)

    registry_file = emasoft_dir / "team-registry.json"

    with open(registry_file, "w") as f:
        json.dump(registry, f, indent=2)

    # Git add and commit
    try:
        subprocess.run(
            ["git", "add", str(registry_file)],
            cwd=repo_path,
            check=True,
            capture_output=True
        )

        team_name = registry["team"]["name"]
        subprocess.run(
            ["git", "commit", "-m", f"[ECOS] Update team registry for {team_name}"],
            cwd=repo_path,
            check=True,
            capture_output=True
        )

        return f"Published to {registry_file} and committed"
    except subprocess.CalledProcessError as e:
        return f"Saved to {registry_file} but git commit failed: {e.stderr.decode()}"


def list_team_agents(registry: dict[str, Any]) -> str:
    """Format team agents as a readable list."""

    lines = []
    team_name = registry["team"]["name"]
    lines.append(f"Team: {team_name}")
    lines.append(f"Repository: {registry['team']['project']['repository']}")
    lines.append("")
    lines.append("Team Agents:")
    lines.append("-" * 80)
    lines.append(f"{'Name':<25} {'Role':<15} {'Host':<20} {'Status':<10}")
    lines.append("-" * 80)

    for agent in registry["agents"]:
        lines.append(
            f"{agent['name']:<25} {agent['role']:<15} {agent['host']:<20} {agent['status']:<10}"
        )

    lines.append("")
    lines.append("Shared Agents:")
    lines.append("-" * 80)
    for agent in registry.get("shared_agents", []):
        lines.append(
            f"{agent['name']:<25} {agent['role']:<15} {agent['host']:<20} (shared)"
        )

    lines.append("")
    lines.append("Organization Agents:")
    lines.append("-" * 80)
    for agent in registry.get("organization_agents", []):
        lines.append(
            f"{agent['name']:<25} {agent['role']:<15} {agent['host']:<20} (org-wide)"
        )

    lines.append("")
    lines.append(f"Last Updated: {registry['contacts_last_updated']}")
    lines.append(f"Updated By: {registry['contacts_updated_by']}")

    return "\n".join(lines)


def notify_team_of_registry_update(
    registry: dict[str, Any],
    changes: list[dict[str, str]]
) -> None:
    """Send AI Maestro notifications to all team agents about registry update."""

    import urllib.request

    AI_MAESTRO_API = os.environ.get("AIMAESTRO_API", "http://localhost:23000")

    for agent in registry["agents"]:
        if agent["status"] != "active":
            continue

        message = {
            "from": "ecos-chief-of-staff",
            "to": agent["ai_maestro_address"],
            "subject": "[REGISTRY UPDATE] Team contacts updated",
            "priority": "normal",
            "content": {
                "type": "registry-update",
                "message": "Team registry has been updated. Please pull latest changes.",
                "team": registry["team"]["name"],
                "changes": changes
            }
        }

        try:
            req = urllib.request.Request(
                f"{AI_MAESTRO_API}/api/messages",
                data=json.dumps(message).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            urllib.request.urlopen(req, timeout=5)
        except Exception as e:
            print(f"Warning: Failed to notify {agent['name']}: {e}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="ECOS Team Registry Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Create a new team
    python ecos_team_registry.py create --team svgbbox-library-team \\
        --repo https://github.com/Emasoft/svgbbox \\
        --project-board https://github.com/orgs/Emasoft/projects/12

    # Add an agent
    python ecos_team_registry.py add-agent --team svgbbox-library-team \\
        --agent-name svgbbox-programmer-001 --role programmer \\
        --plugin emasoft-programmer-agent --host macbook-dev-01

    # Update agent status
    python ecos_team_registry.py update-status --team svgbbox-library-team \\
        --agent-name svgbbox-impl-01 --status hibernated

    # List team
    python ecos_team_registry.py list --team svgbbox-library-team

    # Validate
    python ecos_team_registry.py validate --team svgbbox-library-team

    # Publish to repo
    python ecos_team_registry.py publish --team svgbbox-library-team \\
        --repo-path /path/to/repo
        """
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new team registry")
    create_parser.add_argument("--team", required=True, help="Team name")
    create_parser.add_argument("--repo", required=True, help="GitHub repository URL")
    create_parser.add_argument("--project-board", help="GitHub Projects board URL")
    create_parser.add_argument("--output", help="Output file path")

    # Add agent command
    add_parser = subparsers.add_parser("add-agent", help="Add agent to team")
    add_parser.add_argument("--team", required=True, help="Team name")
    add_parser.add_argument("--agent-name", required=True, help="Agent name")
    add_parser.add_argument("--role", required=True, help="Agent role")
    add_parser.add_argument("--plugin", required=True, help="Plugin name")
    add_parser.add_argument("--host", required=True, help="Host machine")
    add_parser.add_argument("--address", help="AI Maestro address (default: agent name)")
    add_parser.add_argument("--registry-file", required=True, help="Path to registry file")

    # Remove agent command
    remove_parser = subparsers.add_parser("remove-agent", help="Remove agent from team")
    remove_parser.add_argument("--team", required=True, help="Team name")
    remove_parser.add_argument("--agent-name", required=True, help="Agent name to remove")
    remove_parser.add_argument("--registry-file", required=True, help="Path to registry file")

    # Update status command
    status_parser = subparsers.add_parser("update-status", help="Update agent status")
    status_parser.add_argument("--team", required=True, help="Team name")
    status_parser.add_argument("--agent-name", required=True, help="Agent name")
    status_parser.add_argument("--status", required=True, help="New status")
    status_parser.add_argument("--registry-file", required=True, help="Path to registry file")

    # List command
    list_parser = subparsers.add_parser("list", help="List team agents")
    list_parser.add_argument("--registry-file", required=True, help="Path to registry file")

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate team registry")
    validate_parser.add_argument("--registry-file", required=True, help="Path to registry file")

    # Publish command
    publish_parser = subparsers.add_parser("publish", help="Publish registry to repo")
    publish_parser.add_argument("--registry-file", required=True, help="Path to registry file")
    publish_parser.add_argument("--repo-path", required=True, help="Path to git repository")
    publish_parser.add_argument("--notify", action="store_true", help="Notify team agents")

    args = parser.parse_args()

    try:
        if args.command == "create":
            registry = create_team_registry(
                args.team,
                args.repo,
                args.project_board
            )
            output = args.output or f"{args.team}-registry.json"
            with open(output, "w") as f:
                json.dump(registry, f, indent=2)
            print(f"Created team registry: {output}")
            return 0

        elif args.command == "add-agent":
            with open(args.registry_file) as f:
                registry = json.load(f)

            registry = add_agent_to_registry(
                registry,
                args.agent_name,
                args.role,
                args.plugin,
                args.host,
                args.address
            )

            with open(args.registry_file, "w") as f:
                json.dump(registry, f, indent=2)
            print(f"Added agent {args.agent_name} to team")
            return 0

        elif args.command == "remove-agent":
            with open(args.registry_file) as f:
                registry = json.load(f)

            registry = remove_agent_from_registry(registry, args.agent_name)

            with open(args.registry_file, "w") as f:
                json.dump(registry, f, indent=2)
            print(f"Removed agent {args.agent_name} from team")
            return 0

        elif args.command == "update-status":
            with open(args.registry_file) as f:
                registry = json.load(f)

            registry = update_agent_status(registry, args.agent_name, args.status)

            with open(args.registry_file, "w") as f:
                json.dump(registry, f, indent=2)
            print(f"Updated {args.agent_name} status to {args.status}")
            return 0

        elif args.command == "list":
            with open(args.registry_file) as f:
                registry = json.load(f)
            print(list_team_agents(registry))
            return 0

        elif args.command == "validate":
            with open(args.registry_file) as f:
                registry = json.load(f)

            errors = validate_registry(registry)
            if errors:
                print("Validation FAILED:")
                for error in errors:
                    print(f"  - {error}")
                return 1
            else:
                print("Validation PASSED")
                return 0

        elif args.command == "publish":
            with open(args.registry_file) as f:
                registry = json.load(f)

            result = publish_registry_to_repo(registry, args.repo_path)
            print(result)

            if args.notify:
                notify_team_of_registry_update(registry, [{"action": "registry_published"}])
                print("Notified team agents")

            return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
