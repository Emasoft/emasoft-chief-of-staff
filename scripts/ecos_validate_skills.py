#!/usr/bin/env python3
"""
Chief of Staff Skill Validation Script

Validates agent skills using the skills-ref validation tool.

Usage:
    python3 ecos_validate_skills.py SESSION_NAME --skill skill-name
    python3 ecos_validate_skills.py SESSION_NAME --skill /path/to/skill
    python3 ecos_validate_skills.py SESSION_NAME --all --skills-dir /path/to/skills

Output:
    JSON with validation results including:
    - success: boolean indicating all validations passed
    - skill: the skill name or path validated
    - errors: list of validation errors (if any)
    - warnings: list of validation warnings (if any)
    - details: detailed validation output
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Optional


def find_skills_ref() -> Optional[str]:
    """
    Find the skills-ref executable.

    Returns:
        Path to skills-ref or None if not found
    """
    # Check if skills-ref is in PATH
    try:
        result = subprocess.run(
            ["which", "skills-ref"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass

    # Check common locations
    common_paths = [
        Path.home() / ".local" / "bin" / "skills-ref",
        Path("/usr/local/bin/skills-ref"),
        Path.cwd() / ".venv" / "bin" / "skills-ref",
    ]

    for path in common_paths:
        if path.exists() and path.is_file():
            return str(path)

    return None


def run_skills_ref_validate(skill_path: str, skills_ref_path: str) -> dict:
    """
    Run skills-ref validate on a skill.

    Args:
        skill_path: Path to the skill directory
        skills_ref_path: Path to skills-ref executable

    Returns:
        Dictionary with validation results
    """
    try:
        result = subprocess.run(
            [skills_ref_path, "validate", skill_path],
            capture_output=True,
            text=True,
            timeout=60,
        )

        # Parse the output
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        # Try to determine if validation passed
        success = result.returncode == 0

        # Parse errors and warnings from output
        errors = []
        warnings = []

        for line in (stdout + "\n" + stderr).split("\n"):
            line = line.strip()
            if not line:
                continue
            lower_line = line.lower()
            if "error" in lower_line or "fail" in lower_line:
                errors.append(line)
            elif "warn" in lower_line:
                warnings.append(line)

        return {
            "success": success,
            "skill": skill_path,
            "errors": errors,
            "warnings": warnings,
            "details": {
                "stdout": stdout,
                "stderr": stderr,
                "exit_code": result.returncode,
            },
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "skill": skill_path,
            "errors": ["Validation timed out after 60 seconds"],
            "warnings": [],
            "details": {},
        }
    except Exception as e:
        return {
            "success": False,
            "skill": skill_path,
            "errors": [f"Validation failed: {str(e)}"],
            "warnings": [],
            "details": {},
        }


def validate_skill_structure(skill_path: Path) -> dict:
    """
    Perform basic structural validation of a skill directory.

    Args:
        skill_path: Path to the skill directory

    Returns:
        Dictionary with structural validation results
    """
    errors = []
    warnings = []

    # Check if directory exists
    if not skill_path.exists():
        return {
            "success": False,
            "errors": [f"Skill path does not exist: {skill_path}"],
            "warnings": [],
        }

    if not skill_path.is_dir():
        return {
            "success": False,
            "errors": [f"Skill path is not a directory: {skill_path}"],
            "warnings": [],
        }

    # Check for SKILL.md
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        errors.append("Missing required SKILL.md file")
    else:
        # Check SKILL.md has frontmatter
        content = skill_md.read_text(encoding="utf-8")
        if not content.startswith("---"):
            warnings.append("SKILL.md missing YAML frontmatter")

    # Check for references directory
    refs_dir = skill_path / "references"
    if not refs_dir.exists():
        warnings.append("Missing recommended 'references' directory")

    # Check for README
    readme = skill_path / "README.md"
    if not readme.exists():
        warnings.append("Missing README.md file")

    return {"success": len(errors) == 0, "errors": errors, "warnings": warnings}


def validate_all_skills(skills_dir: Path, skills_ref_path: Optional[str]) -> dict:
    """
    Validate all skills in a directory.

    Args:
        skills_dir: Path to directory containing skills
        skills_ref_path: Path to skills-ref executable (optional)

    Returns:
        Dictionary with validation results for all skills
    """
    if not skills_dir.exists():
        return {
            "success": False,
            "error": f"Skills directory does not exist: {skills_dir}",
            "skills": [],
        }

    results = []
    all_passed = True

    # Find all skill directories (those containing SKILL.md)
    for item in skills_dir.iterdir():
        if item.is_dir():
            skill_md = item / "SKILL.md"
            if skill_md.exists():
                # Validate this skill
                if skills_ref_path:
                    result = run_skills_ref_validate(str(item), skills_ref_path)
                else:
                    # Fallback to structural validation
                    struct_result = validate_skill_structure(item)
                    result = {
                        "success": struct_result["success"],
                        "skill": str(item),
                        "errors": struct_result["errors"],
                        "warnings": struct_result["warnings"],
                        "details": {"method": "structural_only"},
                    }

                results.append(result)
                if not result["success"]:
                    all_passed = False

    return {"success": all_passed, "skills_validated": len(results), "skills": results}


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate agent skills using skills-ref",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Validate a specific skill
    python3 ecos_validate_skills.py my-session --skill ./skills/my-skill

    # Validate all skills in a directory
    python3 ecos_validate_skills.py my-session --all --skills-dir ./skills

    # Skip skills-ref and use structural validation only
    python3 ecos_validate_skills.py my-session --skill ./skills/my-skill --structural-only
        """,
    )

    parser.add_argument("session_name", help="Name of the agent session")

    skill_group = parser.add_mutually_exclusive_group(required=True)
    skill_group.add_argument(
        "--skill", metavar="SKILL_NAME", help="Skill name or path to validate"
    )
    skill_group.add_argument(
        "--all", action="store_true", help="Validate all skills in the skills directory"
    )

    parser.add_argument(
        "--skills-dir",
        metavar="PATH",
        help="Path to skills directory (required with --all)",
    )

    parser.add_argument(
        "--structural-only",
        action="store_true",
        help="Skip skills-ref validation and only check structure",
    )

    args = parser.parse_args()

    # Validate arguments
    if args.all and not args.skills_dir:
        print(
            json.dumps(
                {
                    "success": False,
                    "error": "--skills-dir is required when using --all",
                },
                indent=2,
            )
        )
        return 1

    # Find skills-ref unless structural-only
    skills_ref_path = None
    if not args.structural_only:
        skills_ref_path = find_skills_ref()
        if not skills_ref_path:
            # skills-ref not found, warn and continue with structural validation
            sys.stderr.write(
                "Warning: skills-ref not found, using structural validation only\n"
            )

    # Build result with session context
    result: dict = {
        "session": args.session_name,
        "validator": skills_ref_path if skills_ref_path else "structural",
    }

    # Execute validation
    if args.all:
        skills_dir = Path(args.skills_dir)
        validation_result = validate_all_skills(skills_dir, skills_ref_path)
    else:
        skill_path = Path(args.skill)
        if skills_ref_path and not args.structural_only:
            validation_result = run_skills_ref_validate(
                str(skill_path), skills_ref_path
            )
        else:
            struct_result = validate_skill_structure(skill_path)
            validation_result = {
                "success": struct_result["success"],
                "skill": str(skill_path),
                "errors": struct_result["errors"],
                "warnings": struct_result["warnings"],
                "details": {"method": "structural_only"},
            }

    # Merge results
    result.update(validation_result)

    # Output JSON
    print(json.dumps(result, indent=2))

    # Return exit code based on success
    return 0 if result.get("success", False) else 1


if __name__ == "__main__":
    sys.exit(main())
