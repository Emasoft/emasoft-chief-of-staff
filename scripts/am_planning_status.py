#!/usr/bin/env python3
"""
Atlas Planning Status Script

Displays the current status of Plan Phase including requirements progress,
module definitions, and exit criteria completion.

Usage:
    python3 atlas_planning_status.py
    python3 atlas_planning_status.py --verbose
"""

import argparse
import sys
from pathlib import Path

import yaml

# Plan phase state file location
PLAN_STATE_FILE = Path(".claude/orchestrator-plan-phase.local.md")


def parse_frontmatter(file_path: Path) -> dict:
    """Parse YAML frontmatter from a markdown file."""
    if not file_path.exists():
        return {}

    content = file_path.read_text(encoding="utf-8")

    # Check for frontmatter delimiters
    if not content.startswith("---"):
        return {}

    # Find the closing delimiter
    end_index = content.find("---", 3)
    if end_index == -1:
        return {}

    # Extract and parse YAML
    yaml_content = content[3:end_index].strip()
    try:
        return yaml.safe_load(yaml_content) or {}
    except yaml.YAMLError:
        return {}


def get_status_icon(status: str) -> str:
    """Return an icon for the given status."""
    icons = {
        "complete": "✓",
        "in_progress": "→",
        "pending": " ",
        "planned": "○",
        "drafting": "○",
        "reviewing": "→",
        "approved": "✓",
    }
    return icons.get(status, "?")


def display_status(verbose: bool = False) -> bool:
    """Display the current plan phase status."""
    if not PLAN_STATE_FILE.exists():
        print("ERROR: Not in Plan Phase")
        print("Run /start-planning to begin planning")
        return False

    data = parse_frontmatter(PLAN_STATE_FILE)
    if not data:
        print("ERROR: Could not parse plan state file")
        return False

    plan_id = data.get("plan_id", "unknown")
    status = data.get("status", "unknown")
    goal = data.get("goal", "No goal set")
    requirements_sections = data.get("requirements_sections", [])
    modules = data.get("modules", [])
    plan_complete = data.get("plan_phase_complete", False)

    # Print header
    print("╔" + "═" * 66 + "╗")
    print("║" + "PLAN PHASE STATUS".center(66) + "║")
    print("╠" + "═" * 66 + "╣")
    print(f"║ Plan ID: {plan_id:<55} ║")
    print(f"║ Status: {status:<56} ║")
    print(f"║ Goal: {goal[:54]:<56} ║")
    if len(goal) > 54:
        print(f"║       {goal[54:108]:<58} ║")

    # Requirements progress
    print("╠" + "═" * 66 + "╣")
    print("║" + "REQUIREMENTS PROGRESS".center(66) + "║")
    print("╠" + "═" * 66 + "╣")

    if requirements_sections:
        for section in requirements_sections:
            name = section.get("name", "Unknown")
            sect_status = section.get("status", "pending")
            icon = get_status_icon(sect_status)
            print(f"║ [{icon}] {name:<30} - {sect_status:<25} ║")
    else:
        print("║ No requirement sections defined                                  ║")

    # Modules
    print("╠" + "═" * 66 + "╣")
    module_count = len(modules)
    print(f"║ MODULES DEFINED ({module_count})".ljust(66) + " ║")
    print("╠" + "═" * 66 + "╣")

    if modules:
        for i, module in enumerate(modules, 1):
            mod_id = module.get("id", "unknown")
            mod_name = module.get("name", mod_id)
            mod_status = module.get("status", "pending")
            priority = module.get("priority", "medium")
            icon = get_status_icon(mod_status)
            line = f"║ {i}. {mod_id:<12} - {mod_name:<20} [{mod_status}]"
            print(f"{line:<66} ║")

            if verbose:
                criteria = module.get("acceptance_criteria", "No criteria defined")
                print(f"║    Criteria: {criteria[:50]:<52} ║")
                print(f"║    Priority: {priority:<52} ║")
    else:
        print("║ No modules defined yet                                           ║")
        print("║ Use /add-requirement module <name> to add modules                ║")

    # Exit criteria
    print("╠" + "═" * 66 + "╣")
    print("║" + "EXIT CRITERIA".center(66) + "║")
    print("╠" + "═" * 66 + "╣")

    # Calculate exit criteria status
    req_file_exists = Path("USER_REQUIREMENTS.md").exists()
    all_req_complete = all(
        s.get("status") == "complete" for s in requirements_sections
    ) if requirements_sections else False
    all_modules_have_criteria = all(
        m.get("acceptance_criteria") for m in modules
    ) if modules else False
    has_modules = len(modules) > 0

    criteria_status = [
        ("USER_REQUIREMENTS.md complete", req_file_exists and all_req_complete),
        ("All modules defined with acceptance criteria", has_modules and all_modules_have_criteria),
        ("GitHub Issues created for all modules", all(m.get("github_issue") for m in modules) if modules else False),
        ("User approved the plan", plan_complete),
    ]

    for criterion, met in criteria_status:
        icon = "✓" if met else " "
        print(f"║ [{icon}] {criterion:<60} ║")

    print("╚" + "═" * 66 + "╝")

    # Summary
    if plan_complete:
        print("\n✓ Plan Phase complete. Run /start-orchestration to begin implementation.")
    else:
        incomplete = sum(1 for _, met in criteria_status if not met)
        print(f"\n{incomplete} exit criteria remaining. Complete them to approve the plan.")

    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Display Plan Phase status"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed module information"
    )

    args = parser.parse_args()
    success = display_status(verbose=args.verbose)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
