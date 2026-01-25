#!/usr/bin/env python3
"""
Comprehensive second-pass audit for session-memory skill.
Checks all files, anchors, TOC format, links, placeholders, and violations.

Usage:
    python comprehensive_audit.py

    Runs all audit checks and prints results to stdout.
    Exit code 0 on success (no issues), 1 on failure (issues found).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# WHY: Using __file__ parent ensures script works relative to its own location
# The audit_tools directory is inside the skill directory, so we navigate up one level
SKILL_DIR = Path(__file__).resolve().parent.parent
SKILL_FILE = SKILL_DIR / "SKILL.md"
REFERENCES_DIR = SKILL_DIR / "references"

# WHY: Iron Rules violations indicate anti-patterns that must never appear in skills
IRON_RULES_VIOLATIONS = [
    "mock",
    "mocking",
    "mocked",
    "workaround",
    "work around",
    "work-around",
    "fallback",
    "fall back",
    "fall-back",
    "skip test",
    "skip tests",
    "skipping test",
    "ignore error",
    "ignore errors",
    "ignoring error",
    "bypass",
    "bypassing",
    "bypassed",
]

# WHY: Placeholder patterns indicate incomplete content that must be filled in
PLACEHOLDER_PATTERNS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"\bFIXME\b",
    r"to be added",
    r"coming soon",
    r"placeholder",
]


def heading_to_anchor(heading: str) -> str:
    """Convert heading text to GitHub-style anchor."""
    # Remove leading # symbols and whitespace
    text = re.sub(r"^#+\s*", "", heading).strip()
    # Convert to lowercase
    anchor = text.lower()
    # Replace spaces and special chars with hyphens
    anchor = re.sub(r"[^\w\s-]", "", anchor)
    anchor = re.sub(r"[\s_]+", "-", anchor)
    # Remove multiple hyphens
    anchor = re.sub(r"-+", "-", anchor)
    return anchor.strip("-")


def extract_headings(file_path: Path) -> Dict[str, int]:
    """Extract all headings from a markdown file with line numbers."""
    headings: Dict[str, int] = {}
    if not file_path.exists():
        return headings

    with open(file_path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            if line.startswith("#"):
                heading = line.strip()
                anchor = heading_to_anchor(heading)
                headings[anchor] = line_no

    return headings


def extract_toc_entries(skill_file: Path) -> List[Tuple[int, str, str, str]]:
    """Extract TOC entries from SKILL.md.
    Returns: List of (line_no, description, file_path, anchor)
    """
    entries = []
    pattern = r"- (.+?) → \[(.+?)\]\((.+?)\)"

    with open(skill_file, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            match = re.search(pattern, line)
            if match:
                description = match.group(1)
                # WHY: group(2) is anchor text for display, not needed for validation
                _ = match.group(2)  # anchor_text - unused but kept for pattern clarity
                link = match.group(3)

                # Split file path and anchor
                if "#" in link:
                    file_path, anchor = link.split("#", 1)
                else:
                    file_path, anchor = link, ""

                entries.append((line_no, description, file_path, anchor))

    return entries


def check_toc_format(entries: List[Tuple[int, str, str, str]]) -> List[str]:
    """Check that TOC entries start with 'When' or 'If'."""
    errors = []

    for line_no, description, _, _ in entries:
        # Check if description starts with "When" or "If"
        if not (description.startswith("When ") or description.startswith("If ")):
            errors.append(
                f"Line {line_no}: TOC entry must start with 'When' or 'If': '{description}'"
            )

    return errors


def check_anchors(
    entries: List[Tuple[int, str, str, str]], references_dir: Path
) -> List[str]:
    """Check that all anchors exist in their target files."""
    errors = []

    for line_no, description, file_path, anchor in entries:
        if not anchor:
            continue

        # Resolve file path
        if file_path.startswith("references/"):
            full_path = SKILL_DIR / file_path
        else:
            full_path = references_dir / file_path

        # Skip if path is a directory
        if full_path.is_dir():
            continue

        if not full_path.exists():
            errors.append(f"Line {line_no}: File not found: {file_path}")
            continue

        # Extract headings from file
        headings = extract_headings(full_path)

        if anchor not in headings:
            errors.append(
                f"Line {line_no}: Anchor '#{anchor}' not found in {file_path}"
            )
            errors.append(f"  Description: '{description}'")
            errors.append(
                f"  Available anchors: {', '.join(sorted(headings.keys())[:5])}..."
            )

    return errors


def check_file_existence(references_dir: Path) -> List[str]:
    """Check that all referenced files exist."""
    errors = []
    pattern = r"\[.+?\]\((.+?\.md)"

    with open(SKILL_FILE, "r", encoding="utf-8") as f:
        content = f.read()
        for match in re.finditer(pattern, content):
            link = match.group(1)

            # Remove anchor
            if "#" in link:
                link = link.split("#")[0]

            # Resolve path
            if link.startswith("references/"):
                full_path = SKILL_DIR / link
            else:
                full_path = references_dir / link

            if not full_path.exists():
                errors.append(f"Referenced file not found: {link}")

    return errors


def check_orphaned_files(references_dir: Path) -> List[str]:
    """Check for files not linked from SKILL.md."""
    # Get all reference files
    all_files = {f.name for f in references_dir.glob("*.md")}

    # Get all linked files
    linked_files = set()
    pattern = r"\[.+?\]\(references/(.+?\.md)"

    with open(SKILL_FILE, "r", encoding="utf-8") as f:
        content = f.read()
        for match in re.finditer(pattern, content):
            link = match.group(1)
            # Remove anchor
            if "#" in link:
                link = link.split("#")[0]
            linked_files.add(link)

    orphaned = all_files - linked_files
    return [f"Orphaned file (not linked from SKILL.md): {f}" for f in sorted(orphaned)]


def check_placeholders(directory: Path) -> List[str]:
    """Search for placeholder text in all markdown files."""
    errors = []

    for md_file in directory.rglob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                for pattern in PLACEHOLDER_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        errors.append(
                            f"{md_file.name}:{line_no}: Placeholder found: {line.strip()[:80]}"
                        )

    return errors


def check_iron_rules(directory: Path) -> List[str]:
    """Search for Iron Rules violations."""
    errors = []

    for md_file in directory.rglob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                for violation in IRON_RULES_VIOLATIONS:
                    if re.search(
                        r"\b" + re.escape(violation) + r"\b", line, re.IGNORECASE
                    ):
                        errors.append(
                            f"{md_file.name}:{line_no}: Iron Rule violation '{violation}': {line.strip()[:80]}"
                        )

    return errors


def check_markdown_syntax(directory: Path) -> List[str]:
    """Check for common markdown syntax errors."""
    errors = []

    for md_file in directory.rglob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                # Check for broken links [text](path
                if re.search(r"\[.+?\]\([^)]*$", line):
                    errors.append(
                        f"{md_file.name}:{line_no}: Incomplete link syntax: {line.strip()[:80]}"
                    )

                # Check for broken anchor links [text](#anchor with space)
                if re.search(r"\[.+?\]\(#[^)]*\s[^)]*\)", line):
                    errors.append(
                        f"{md_file.name}:{line_no}: Anchor contains space: {line.strip()[:80]}"
                    )

    return errors


def main() -> int:
    """Run comprehensive audit and return exit code."""
    # WHY: Structured output with separators makes logs easy to parse
    print("=" * 80)
    print("COMPREHENSIVE SESSION-MEMORY SKILL AUDIT")
    print("=" * 80)
    print()

    total_issues = 0

    # 1. Check file existence
    print("1. Checking file existence...")
    errors = check_file_existence(REFERENCES_DIR)
    if errors:
        print(f"   FOUND {len(errors)} missing files:")
        for err in errors:
            print(f"   - {err}")
        total_issues += len(errors)
    else:
        print("   ✓ All referenced files exist")
    print()

    # 2. Extract TOC entries
    print("2. Extracting TOC entries...")
    toc_entries = extract_toc_entries(SKILL_FILE)
    print(f"   Found {len(toc_entries)} TOC entries")
    print()

    # 3. Check TOC format
    print("3. Checking TOC format (must start with 'When' or 'If')...")
    errors = check_toc_format(toc_entries)
    if errors:
        print(f"   FOUND {len(errors)} format violations:")
        for err in errors[:20]:  # Show first 20
            print(f"   - {err}")
        if len(errors) > 20:
            print(f"   ... and {len(errors) - 20} more")
        total_issues += len(errors)
    else:
        print("   ✓ All TOC entries properly formatted")
    print()

    # 4. Check anchors
    print("4. Checking anchor validity...")
    errors = check_anchors(toc_entries, REFERENCES_DIR)
    if errors:
        print(f"   FOUND {len(errors)} anchor issues:")
        for err in errors[:30]:  # Show first 30
            print(f"   - {err}")
        if len(errors) > 30:
            print(f"   ... and {len(errors) - 30} more")
        total_issues += len(errors)
    else:
        print("   ✓ All anchors valid")
    print()

    # 5. Check orphaned files
    print("5. Checking for orphaned files...")
    errors = check_orphaned_files(REFERENCES_DIR)
    if errors:
        print(f"   FOUND {len(errors)} orphaned files:")
        for err in errors:
            print(f"   - {err}")
        total_issues += len(errors)
    else:
        print("   ✓ No orphaned files")
    print()

    # 6. Check placeholders
    print("6. Checking for placeholder text...")
    errors = check_placeholders(SKILL_DIR)
    if errors:
        print(f"   FOUND {len(errors)} placeholders:")
        for err in errors[:10]:
            print(f"   - {err}")
        if len(errors) > 10:
            print(f"   ... and {len(errors) - 10} more")
        total_issues += len(errors)
    else:
        print("   ✓ No placeholders found")
    print()

    # 7. Check Iron Rules violations
    print("7. Checking for Iron Rules violations...")
    errors = check_iron_rules(SKILL_DIR)
    if errors:
        print(f"   FOUND {len(errors)} violations:")
        for err in errors[:10]:
            print(f"   - {err}")
        if len(errors) > 10:
            print(f"   ... and {len(errors) - 10} more")
        total_issues += len(errors)
    else:
        print("   ✓ No Iron Rules violations")
    print()

    # 8. Check markdown syntax
    print("8. Checking markdown syntax...")
    errors = check_markdown_syntax(SKILL_DIR)
    if errors:
        print(f"   FOUND {len(errors)} syntax errors:")
        for err in errors[:10]:
            print(f"   - {err}")
        if len(errors) > 10:
            print(f"   ... and {len(errors) - 10} more")
        total_issues += len(errors)
    else:
        print("   ✓ No syntax errors")
    print()

    # Summary
    print("=" * 80)
    print("AUDIT SUMMARY")
    print("=" * 80)
    if total_issues == 0:
        print("✓ ALL CHECKS PASSED - No issues found")
        return 0
    else:
        print(f"✗ FOUND {total_issues} TOTAL ISSUES")
        print("Review output above for details")
        return 1


if __name__ == "__main__":
    # WHY: Explicit sys.exit ensures proper exit code propagation to shell/CI
    sys.exit(main())
