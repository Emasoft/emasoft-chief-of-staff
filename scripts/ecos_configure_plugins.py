#!/usr/bin/env python3
"""
Chief of Staff Plugin Configuration Script

Configures Claude Code plugins for a specified agent session by running
claude plugin install/enable/disable commands.

Usage:
    python3 ecos_configure_plugins.py SESSION_NAME --add plugin-name
    python3 ecos_configure_plugins.py SESSION_NAME --remove plugin-name
    python3 ecos_configure_plugins.py SESSION_NAME --list
    python3 ecos_configure_plugins.py SESSION_NAME --add plugin-name --scope project

Output:
    JSON with configuration result including:
    - success: boolean indicating operation success
    - operation: the operation performed
    - plugin: the plugin name (if applicable)
    - scope: the scope used
    - message: human-readable result message
    - error: error message if failed
"""

import argparse
import json
import subprocess
import sys


def run_claude_command(args: list[str], timeout: int = 30) -> tuple[bool, str, str]:
    """
    Run a claude CLI command and return (success, stdout, stderr).

    Args:
        args: Command arguments to pass to claude CLI
        timeout: Command timeout in seconds

    Returns:
        Tuple of (success, stdout, stderr)
    """
    try:
        result = subprocess.run(
            ["claude"] + args, capture_output=True, text=True, timeout=timeout
        )
        return (result.returncode == 0, result.stdout.strip(), result.stderr.strip())
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except FileNotFoundError:
        return False, "", "claude CLI not found in PATH"
    except Exception as e:
        return False, "", str(e)


def list_plugins() -> dict:
    """
    List currently installed/enabled plugins.

    Returns:
        Dictionary with plugin list information
    """
    success, stdout, stderr = run_claude_command(["plugin", "list"])

    if not success:
        return {
            "success": False,
            "operation": "list",
            "error": stderr or "Failed to list plugins",
        }

    # Parse the output to extract plugin information
    plugins = []
    for line in stdout.split("\n"):
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("-"):
            # Try to extract plugin name from the line
            plugins.append(line)

    return {
        "success": True,
        "operation": "list",
        "plugins": plugins,
        "raw_output": stdout,
    }


def add_plugin(plugin_name: str, scope: str) -> dict:
    """
    Install and enable a plugin.

    Args:
        plugin_name: Name of the plugin to add
        scope: Installation scope (local, project, user)

    Returns:
        Dictionary with operation result
    """
    # First try to install the plugin
    install_args = ["plugin", "install", plugin_name]
    if scope:
        install_args.extend(["--scope", scope])

    success, _, stderr = run_claude_command(install_args)

    if not success:
        # Plugin might already be installed, try to enable it
        enable_args = ["plugin", "enable", plugin_name]
        if scope:
            enable_args.extend(["--scope", scope])

        success, _, stderr = run_claude_command(enable_args)

        if not success:
            return {
                "success": False,
                "operation": "add",
                "plugin": plugin_name,
                "scope": scope,
                "error": stderr or "Failed to install or enable plugin",
            }

        return {
            "success": True,
            "operation": "enable",
            "plugin": plugin_name,
            "scope": scope,
            "message": f"Plugin '{plugin_name}' enabled (was already installed)",
        }

    return {
        "success": True,
        "operation": "install",
        "plugin": plugin_name,
        "scope": scope,
        "message": f"Plugin '{plugin_name}' installed and enabled",
    }


def remove_plugin(plugin_name: str, scope: str) -> dict:
    """
    Disable a plugin.

    Args:
        plugin_name: Name of the plugin to remove
        scope: Installation scope (local, project, user)

    Returns:
        Dictionary with operation result
    """
    disable_args = ["plugin", "disable", plugin_name]
    if scope:
        disable_args.extend(["--scope", scope])

    success, _, stderr = run_claude_command(disable_args)

    if not success:
        return {
            "success": False,
            "operation": "remove",
            "plugin": plugin_name,
            "scope": scope,
            "error": stderr or "Failed to disable plugin",
        }

    return {
        "success": True,
        "operation": "disable",
        "plugin": plugin_name,
        "scope": scope,
        "message": f"Plugin '{plugin_name}' disabled",
    }


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Configure Claude Code plugins for an agent session",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # List installed plugins
    python3 ecos_configure_plugins.py my-session --list

    # Add a plugin with local scope
    python3 ecos_configure_plugins.py my-session --add my-plugin --scope local

    # Remove a plugin
    python3 ecos_configure_plugins.py my-session --remove my-plugin
        """,
    )

    parser.add_argument("session_name", help="Name of the agent session to configure")

    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument(
        "--add", metavar="PLUGIN", help="Plugin name to install/enable"
    )
    action_group.add_argument(
        "--remove", metavar="PLUGIN", help="Plugin name to disable"
    )
    action_group.add_argument(
        "--list", action="store_true", help="List currently installed plugins"
    )

    parser.add_argument(
        "--scope",
        choices=["local", "project", "user"],
        default="local",
        help="Installation scope (default: local)",
    )

    args = parser.parse_args()

    # Build result with session context
    result: dict = {"session": args.session_name}

    # Execute the requested operation
    if args.list:
        operation_result = list_plugins()
    elif args.add:
        operation_result = add_plugin(args.add, args.scope)
    elif args.remove:
        operation_result = remove_plugin(args.remove, args.scope)
    else:
        operation_result = {"success": False, "error": "No operation specified"}

    # Merge results
    result.update(operation_result)

    # Output JSON
    print(json.dumps(result, indent=2))

    # Return exit code based on success
    return 0 if result.get("success", False) else 1


if __name__ == "__main__":
    sys.exit(main())
