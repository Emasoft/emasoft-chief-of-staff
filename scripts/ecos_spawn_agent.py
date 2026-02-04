#!/usr/bin/env python3
"""
ecos_spawn_agent.py - Spawn a new AI Maestro agent session.

Usage:
    python ecos_spawn_agent.py ROLE SESSION_NAME [--project PROJECT_ID] [--plugins PLUGIN1,PLUGIN2] [--agent AGENT_NAME]

Example:
    python ecos_spawn_agent.py orchestrator svgbbox-orchestrator --project svgbbox \
        --plugins emasoft-orchestrator-agent --agent eoa-orchestrator-main-agent
"""

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def get_marketplace_plugin_path(plugin_name: str) -> Path | None:
    """Get the path to a marketplace-installed plugin.

    Plugins are installed from emasoft-plugins marketplace to:
    ~/.claude/plugins/cache/emasoft-plugins/<plugin-name>/<version>/

    Returns the latest version path, or None if not installed.
    """
    cache_dir = (
        Path.home() / ".claude" / "plugins" / "cache" / "emasoft-plugins" / plugin_name
    )
    if not cache_dir.exists():
        return None

    # Find latest version directory
    versions = sorted(cache_dir.iterdir(), reverse=True)
    if versions:
        return versions[0]
    return None


def install_marketplace_plugin(plugin_name: str, agent_dir: Path) -> bool:
    """Install a plugin from emasoft-plugins marketplace to agent's local folder.

    Args:
        plugin_name: Name of the plugin (e.g., 'emasoft-orchestrator-agent')
        agent_dir: Path to the agent's directory (e.g., ~/agents/eoa-svgbbox/)

    Returns:
        True if successful, False if plugin not found in marketplace cache
    """
    source_path = get_marketplace_plugin_path(plugin_name)
    if not source_path:
        return False

    dest_path = agent_dir / ".claude" / "plugins" / plugin_name
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    if dest_path.exists():
        shutil.rmtree(dest_path)

    shutil.copytree(source_path, dest_path)
    return True


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Spawn a new AI Maestro agent session.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Spawn a code reviewer agent
    python ecos_spawn_agent.py code-reviewer cr-session-01

    # Spawn with project context
    python ecos_spawn_agent.py architect arch-01 --project my-app

    # Spawn with plugins
    python ecos_spawn_agent.py developer dev-01 --plugins linter,formatter
        """,
    )
    parser.add_argument(
        "role",
        type=str,
        help="Role for the agent (e.g., code-reviewer, architect, developer)",
    )
    parser.add_argument(
        "session_name",
        type=str,
        help="Unique session name (becomes AI Maestro registry identity, e.g., eoa-svgbbox-orchestrator)",
    )
    parser.add_argument(
        "--project",
        type=str,
        default=None,
        help="Project ID to associate with the agent",
    )
    parser.add_argument(
        "--plugins",
        type=str,
        default=None,
        help="Comma-separated list of plugins to load",
    )
    parser.add_argument(
        "--agent",
        type=str,
        default=None,
        help="Main agent name to inject via --agent CLI flag (e.g., eoa-orchestrator-main-agent)",
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
    Main entry point for spawning an agent.

    Returns:
        0 on success, 1 on error, 2 if agent exists, 127 if CLI not found.
    """
    args = parse_args()

    # Build agent directory path (FLAT structure)
    agent_dir = Path.home() / "agents" / args.session_name

    # Check if agent already exists
    returncode, stdout, stderr = run_aimaestro_command(["show", args.session_name])
    if returncode == 127:
        result: dict[str, Any] = {
            "status": "error",
            "message": "aimaestro-agent.sh not found in PATH",
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }
        print(json.dumps(result, indent=2), file=sys.stderr)
        return 127
    elif returncode == 0 and stdout:
        # Agent exists
        result = {
            "status": "exists",
            "message": f"Agent '{args.session_name}' already exists",
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "session_name": args.session_name,
        }
        print(json.dumps(result, indent=2), file=sys.stderr)
        return 2

    # Parse plugins list if provided
    plugins_list = []
    if args.plugins:
        plugins_list = [p.strip() for p in args.plugins.split(",") if p.strip()]

    # Install plugins from emasoft-plugins marketplace to agent's local folder
    # Plugins are fetched from: ~/.claude/plugins/cache/emasoft-plugins/<plugin-name>/<version>/
    plugins_installed = []
    plugins_failed = []
    for plugin in plugins_list:
        if install_marketplace_plugin(plugin, agent_dir):
            plugins_installed.append(plugin)
        else:
            plugins_failed.append(plugin)

    if plugins_failed:
        result = {
            "status": "error",
            "message": f"Failed to install plugins from marketplace: {plugins_failed}",
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "hint": "Ensure plugins are installed via: claude plugin install <name>@emasoft-plugins",
            "plugins_installed": plugins_installed,
            "plugins_failed": plugins_failed,
        }
        print(json.dumps(result, indent=2), file=sys.stderr)
        return 1

    # Build create command
    create_args = ["create", args.session_name]

    # Add agent directory
    create_args.extend(["--dir", str(agent_dir)])

    # Add task description
    if args.project:
        create_args.extend(["--task", f"Work on {args.project}"])
        # Add tags
        create_args.extend(["--tags", f"project:{args.project},role:{args.role}"])
    else:
        create_args.extend(["--task", f"Agent with role {args.role}"])
        create_args.extend(["--tags", f"role:{args.role}"])

    # Add Claude Code flags after --
    # Note: --continue is NOT used for new spawns (only for waking hibernated agents)
    create_args.append("--")
    create_args.extend(
        ["--dangerously-skip-permissions", "--chrome", "--add-dir", "/tmp"]
    )

    # Add plugin directories from local agent folder (not development folder)
    # Plugins must be copied to ~/agents/<session-name>/.claude/plugins/<plugin-name>/
    for plugin in plugins_list:
        create_args.extend(["--plugin-dir", f"{agent_dir}/.claude/plugins/{plugin}"])

    # Add the --agent flag if specified (CRITICAL for main-agent injection)
    if args.agent:
        create_args.extend(["--agent", args.agent])

    # Execute the create command
    returncode, stdout, stderr = run_aimaestro_command(create_args, timeout=120)

    if returncode != 0:
        result = {
            "status": "error",
            "message": f"Failed to create agent '{args.session_name}'",
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "error": stderr or stdout,
            "parameters": {
                "role": args.role,
                "session_name": args.session_name,
                "project": args.project,
                "plugins": plugins_list,
                "agent": args.agent,
            },
        }
        print(json.dumps(result, indent=2), file=sys.stderr)
        return 1

    # Success
    result = {
        "status": "success",
        "message": f"Agent '{args.session_name}' spawned successfully",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "parameters": {
            "role": args.role,
            "session_name": args.session_name,
            "project": args.project,
            "plugins": plugins_list,
            "agent": args.agent,
            "agent_dir": str(agent_dir),
        },
        "output": stdout,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
