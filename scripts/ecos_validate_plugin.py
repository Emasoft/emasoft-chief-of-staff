#!/usr/bin/env python3
"""
ecos_validate_plugin.py - Validate emasoft-chief-of-staff plugin structure.

Comprehensive plugin validator that checks:
1. Plugin manifest (plugin.json) structure and required fields
2. Agent definitions (YAML frontmatter, required fields)
3. Command definitions (YAML frontmatter, required fields)
4. Skill structure and frontmatter
5. Hook configuration (hooks.json) structure and script references
6. Script validation via ruff check and mypy

Dependencies: Python 3.8+ stdlib only (ruff/mypy called externally)

Usage:
    python ecos_validate_plugin.py [--verbose] [--json] [--plugin-dir PATH]

Exit codes:
    0 - All checks passed
    1 - Critical errors found
    2 - Major errors found
    3 - Warnings only
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, cast


class ValidationResult:
    """Validation result tracker with categorized issues."""

    def __init__(self) -> None:
        self.critical: list[str] = []
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.passed: list[str] = []

    def add_critical(self, msg: str) -> None:
        """Add critical error (plugin unusable)."""
        self.critical.append(msg)

    def add_error(self, msg: str) -> None:
        """Add error (functionality broken)."""
        self.errors.append(msg)

    def add_warning(self, msg: str) -> None:
        """Add warning (suboptimal but works)."""
        self.warnings.append(msg)

    def add_pass(self, msg: str) -> None:
        """Add passed check."""
        self.passed.append(msg)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON output."""
        return {
            "critical": self.critical,
            "errors": self.errors,
            "warnings": self.warnings,
            "passed": self.passed,
            "summary": {
                "critical_count": len(self.critical),
                "error_count": len(self.errors),
                "warning_count": len(self.warnings),
                "passed_count": len(self.passed),
            },
        }

    def print_results(self, verbose: bool = False) -> int:
        """Print validation results and return exit code."""
        if verbose and self.passed:
            print("\n=== PASSED CHECKS ===")
            for msg in self.passed:
                print(f"  [PASS] {msg}")

        if self.warnings:
            print("\n=== WARNINGS ===")
            for msg in self.warnings:
                print(f"  [WARN] {msg}")

        if self.errors:
            print("\n=== ERRORS ===")
            for msg in self.errors:
                print(f"  [ERR]  {msg}")

        if self.critical:
            print("\n=== CRITICAL ===")
            for msg in self.critical:
                print(f"  [CRIT] {msg}")

        # Summary
        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)
        print(f"  Passed:   {len(self.passed)}")
        print(f"  Warnings: {len(self.warnings)}")
        print(f"  Errors:   {len(self.errors)}")
        print(f"  Critical: {len(self.critical)}")

        # Determine exit code
        if self.critical:
            print("\nResult: FAILED (critical issues)")
            return 1
        elif self.errors:
            print("\nResult: FAILED (errors found)")
            return 2
        elif self.warnings:
            print("\nResult: PASSED with warnings")
            return 3
        else:
            print("\nResult: PASSED")
            return 0


def validate_plugin_json(
    plugin_dir: Path, result: ValidationResult
) -> dict[str, Any] | None:
    """Validate plugin.json manifest.

    Args:
        plugin_dir: Plugin directory path
        result: ValidationResult to add issues to

    Returns:
        Parsed manifest dict or None if invalid
    """
    plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"

    if not plugin_json.exists():
        result.add_critical(f"plugin.json not found: {plugin_json}")
        return None

    result.add_pass("plugin.json exists")

    try:
        with open(plugin_json, encoding="utf-8") as f:
            manifest = json.load(f)
        result.add_pass("plugin.json is valid JSON")
    except json.JSONDecodeError as e:
        result.add_critical(f"plugin.json invalid JSON: {e}")
        return None

    # Required fields
    required = ["name", "version", "description"]
    for field in required:
        if field not in manifest:
            result.add_error(f"plugin.json missing required field: {field}")
        else:
            result.add_pass(f"plugin.json has {field}")

    # Validate name format
    name = manifest.get("name", "")
    if name and not re.match(r"^[a-z][a-z0-9-]*$", name):
        result.add_warning(f"plugin name should be kebab-case: {name}")

    # Validate version format
    version = manifest.get("version", "")
    if version and not re.match(r"^\d+\.\d+\.\d+", version):
        result.add_warning(f"version should be semver: {version}")

    # Check agents field format
    agents = manifest.get("agents", [])
    if agents:
        if not isinstance(agents, list):
            result.add_error("agents field must be an array of .md file paths")
        else:
            for agent_path in agents:
                if not agent_path.endswith(".md"):
                    result.add_warning(f"agent path should end with .md: {agent_path}")
                if not agent_path.startswith("./"):
                    result.add_warning(f"agent path should start with ./: {agent_path}")

    # Validate manifest schema — Claude Code rejects unknown keys
    known_manifest_fields = {
        "name", "version", "description", "author", "homepage",
        "repository", "license", "keywords", "commands", "agents",
        "skills", "hooks", "mcpServers", "outputStyles", "lspServers",
    }
    for key in manifest.keys():
        if key not in known_manifest_fields:
            result.add_error(
                f"Unrecognized manifest field '{key}' — Claude Code rejects "
                f"unknown keys and plugin installation will fail"
            )

    # Validate repository field type — must be string URL, not object
    if "repository" in manifest and not isinstance(manifest["repository"], str):
        result.add_error(
            "Field 'repository' must be a string URL, not an object. "
            "Use \"https://github.com/user/repo\" format."
        )

    return cast(dict[str, Any], manifest)


def validate_agents(plugin_dir: Path, result: ValidationResult) -> None:
    """Validate agent definitions.

    Args:
        plugin_dir: Plugin directory path
        result: ValidationResult to add issues to
    """
    agents_dir = plugin_dir / "agents"

    if not agents_dir.exists():
        result.add_warning("agents/ directory not found")
        return

    agent_files = list(agents_dir.glob("*.md"))
    if not agent_files:
        result.add_warning("No agent files found in agents/")
        return

    result.add_pass(f"Found {len(agent_files)} agent file(s)")

    for agent_file in agent_files:
        try:
            content = agent_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            result.add_error(f"Cannot read {agent_file.name}: {e}")
            continue

        # Check for YAML frontmatter
        if not content.startswith("---"):
            result.add_error(f"{agent_file.name}: Missing YAML frontmatter")
            continue

        # Extract frontmatter
        parts = content.split("---", 2)
        if len(parts) < 3:
            result.add_error(f"{agent_file.name}: Invalid frontmatter format")
            continue

        frontmatter = parts[1].strip()

        # Check required fields
        required_fields = ["name", "description"]
        for field in required_fields:
            if f"{field}:" not in frontmatter:
                result.add_error(f"{agent_file.name}: Missing required field '{field}'")

        result.add_pass(f"Agent validated: {agent_file.name}")


def validate_commands(plugin_dir: Path, result: ValidationResult) -> None:
    """Validate command definitions.

    Args:
        plugin_dir: Plugin directory path
        result: ValidationResult to add issues to
    """
    commands_dir = plugin_dir / "commands"

    if not commands_dir.exists():
        result.add_warning("commands/ directory not found")
        return

    command_files = list(commands_dir.glob("*.md"))
    if not command_files:
        result.add_warning("No command files found in commands/")
        return

    result.add_pass(f"Found {len(command_files)} command file(s)")

    for cmd_file in command_files:
        try:
            content = cmd_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            result.add_error(f"Cannot read {cmd_file.name}: {e}")
            continue

        # Check for YAML frontmatter
        if not content.startswith("---"):
            result.add_error(f"{cmd_file.name}: Missing YAML frontmatter")
            continue

        result.add_pass(f"Command validated: {cmd_file.name}")


def validate_skills(plugin_dir: Path, result: ValidationResult) -> None:
    """Validate skill structure.

    Args:
        plugin_dir: Plugin directory path
        result: ValidationResult to add issues to
    """
    skills_dir = plugin_dir / "skills"

    if not skills_dir.exists():
        result.add_warning("skills/ directory not found")
        return

    skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
    if not skill_dirs:
        result.add_warning("No skill directories found in skills/")
        return

    result.add_pass(f"Found {len(skill_dirs)} skill(s)")

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            result.add_error(f"Skill {skill_dir.name}: Missing SKILL.md")
            continue

        try:
            content = skill_md.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            result.add_error(f"Skill {skill_dir.name}: Cannot read SKILL.md: {e}")
            continue

        # Check for frontmatter
        if content.startswith("---"):
            result.add_pass(f"Skill {skill_dir.name}: Has frontmatter")

            # Check Claude Code-specific fields
            parts = content.split("---", 2)
            if len(parts) >= 2:
                frontmatter = parts[1]
                # context field
                if "context:" in frontmatter:
                    if "fork" not in frontmatter:
                        result.add_warning(
                            f"Skill {skill_dir.name}: context should be 'fork'"
                        )
        else:
            result.add_warning(f"Skill {skill_dir.name}: No frontmatter in SKILL.md")

        result.add_pass(f"Skill validated: {skill_dir.name}")


def validate_hooks(plugin_dir: Path, result: ValidationResult) -> None:
    """Validate hooks configuration.

    Args:
        plugin_dir: Plugin directory path
        result: ValidationResult to add issues to
    """
    hooks_json = plugin_dir / "hooks" / "hooks.json"

    if not hooks_json.exists():
        result.add_warning("hooks/hooks.json not found")
        return

    try:
        with open(hooks_json, encoding="utf-8") as f:
            hooks_config = json.load(f)
        result.add_pass("hooks.json is valid JSON")
    except json.JSONDecodeError as e:
        result.add_error(f"hooks.json invalid JSON: {e}")
        return

    # Check hooks structure
    hooks = hooks_config.get("hooks", {})
    if not hooks:
        result.add_warning("hooks.json has no hooks defined")
        return

    valid_events = [
        "PreToolUse",
        "PostToolUse",
        "PostToolUseFailure",
        "PermissionRequest",
        "UserPromptSubmit",
        "Notification",
        "Stop",
        "SubagentStop",
        "SessionStart",
        "SessionEnd",
        "PreCompact",
    ]

    for event, event_hooks in hooks.items():
        if event not in valid_events:
            result.add_warning(f"Unknown hook event: {event}")

        if not isinstance(event_hooks, list):
            result.add_error(f"Hook {event}: hooks must be an array")
            continue

        for hook_group in event_hooks:
            hook_list = hook_group.get("hooks", [])
            for hook in hook_list:
                command = hook.get("command", "")
                if "${CLAUDE_PLUGIN_ROOT}" not in command:
                    result.add_warning(
                        f"Hook command should use ${{CLAUDE_PLUGIN_ROOT}}: {command[:50]}"
                    )

                # Check script exists
                if "scripts/" in command:
                    script_name = command.split("scripts/")[-1].split()[0]
                    script_path = plugin_dir / "scripts" / script_name
                    if not script_path.exists():
                        result.add_error(f"Hook script not found: {script_name}")
                    else:
                        result.add_pass(f"Hook script exists: {script_name}")

    result.add_pass("Hooks configuration validated")


def validate_scripts(plugin_dir: Path, result: ValidationResult) -> None:
    """Validate Python scripts with ruff and mypy.

    Args:
        plugin_dir: Plugin directory path
        result: ValidationResult to add issues to
    """
    scripts_dir = plugin_dir / "scripts"

    if not scripts_dir.exists():
        result.add_warning("scripts/ directory not found")
        return

    py_files = list(scripts_dir.glob("*.py"))
    if not py_files:
        result.add_warning("No Python scripts found in scripts/")
        return

    result.add_pass(f"Found {len(py_files)} Python script(s)")

    # Check shebangs
    for script in py_files:
        try:
            content = script.read_text(encoding="utf-8")
            if not content.startswith("#!/usr/bin/env python3"):
                result.add_warning(f"{script.name}: Missing or incorrect shebang")
            else:
                result.add_pass(f"{script.name}: Has correct shebang")

            # Check for docstring
            if '"""' not in content[:500]:
                result.add_warning(f"{script.name}: Missing module docstring")
        except (OSError, UnicodeDecodeError):
            pass

    # Run ruff check
    try:
        ruff_result = subprocess.run(
            ["ruff", "check", str(scripts_dir)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if ruff_result.returncode == 0:
            result.add_pass("ruff check: No issues found")
        else:
            # Count issues
            issues = ruff_result.stdout.strip().split("\n")
            issues = [i for i in issues if i.strip()]
            if len(issues) > 0:
                result.add_error(f"ruff check: {len(issues)} issue(s) found")
                for issue in issues[:5]:
                    result.add_error(f"  {issue}")
                if len(issues) > 5:
                    result.add_error(f"  ... and {len(issues) - 5} more")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        result.add_warning("ruff not available or timed out")

    # Run mypy
    try:
        mypy_result = subprocess.run(
            ["mypy", "--ignore-missing-imports", str(scripts_dir)],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if mypy_result.returncode == 0:
            result.add_pass("mypy: No type errors found")
        else:
            # Count errors
            errors = mypy_result.stdout.strip().split("\n")
            errors = [e for e in errors if "error:" in e]
            if len(errors) > 0:
                result.add_warning(f"mypy: {len(errors)} type error(s) found")
                for error in errors[:3]:
                    result.add_warning(f"  {error}")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        result.add_warning("mypy not available or timed out")


def validate_license(plugin_dir: Path, result: ValidationResult) -> None:
    """Check for LICENSE file.

    Args:
        plugin_dir: Plugin directory path
        result: ValidationResult to add issues to
    """
    license_file = plugin_dir / "LICENSE"
    if license_file.exists():
        result.add_pass("LICENSE file exists")
    else:
        result.add_warning("LICENSE file not found")


def validate_readme(plugin_dir: Path, result: ValidationResult) -> None:
    """Check for README.md file.

    Args:
        plugin_dir: Plugin directory path
        result: ValidationResult to add issues to
    """
    readme_file = plugin_dir / "README.md"
    if readme_file.exists():
        result.add_pass("README.md exists")
    else:
        result.add_warning("README.md not found")


def validate_plugin(plugin_dir: Path) -> ValidationResult:
    """Run all plugin validations.

    Args:
        plugin_dir: Plugin directory path

    Returns:
        ValidationResult with all findings
    """
    result = ValidationResult()

    # Check plugin directory exists
    if not plugin_dir.exists():
        result.add_critical(f"Plugin directory not found: {plugin_dir}")
        return result

    result.add_pass(f"Plugin directory exists: {plugin_dir.name}")

    # Run all validations
    validate_plugin_json(plugin_dir, result)
    validate_agents(plugin_dir, result)
    validate_commands(plugin_dir, result)
    validate_skills(plugin_dir, result)
    validate_hooks(plugin_dir, result)
    validate_scripts(plugin_dir, result)
    validate_license(plugin_dir, result)
    validate_readme(plugin_dir, result)

    return result


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate emasoft-chief-of-staff plugin structure"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show all passed checks"
    )
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument(
        "--plugin-dir",
        type=Path,
        help="Path to plugin directory (default: parent of scripts/)",
    )

    args = parser.parse_args()

    # Determine plugin directory
    if args.plugin_dir:
        plugin_dir = args.plugin_dir.resolve()
    else:
        # Assume we're running from scripts/ directory
        plugin_dir = Path(__file__).parent.parent.resolve()

    print(f"Validating plugin: {plugin_dir}")
    print("=" * 60)

    result = validate_plugin(plugin_dir)

    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
        sys.exit(0 if not result.critical and not result.errors else 1)
    else:
        exit_code = result.print_results(args.verbose)
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
