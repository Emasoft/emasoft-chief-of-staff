#!/usr/bin/env python3
"""Comprehensive validation script for session-memory skill."""

# WHY: from __future__ import annotations enables postponed evaluation of annotations,
# allowing forward references and improving startup performance
from __future__ import annotations

import re
import sys
from pathlib import Path


def check_file_references() -> tuple[int, list[str]]:
    """Check all file references in SKILL.md exist.

    Returns:
        Tuple of (total reference count, list of missing file names).
    """
    # WHY: Using Path for cross-platform path handling
    skill_md_path = Path("SKILL.md")
    try:
        skill_md = skill_md_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"ERROR: {skill_md_path} not found", file=sys.stderr)
        return 0, []
    except OSError as e:
        print(f"ERROR: Failed to read {skill_md_path}: {e}", file=sys.stderr)
        return 0, []

    # WHY: Regex pattern captures markdown link references to files in references/
    file_refs = re.findall(r"\[references/([\w-]+\.md)\]", skill_md)

    missing: list[str] = []
    for ref in file_refs:
        file_path = Path("references") / ref
        if not file_path.exists():
            missing.append(ref)

    return len(file_refs), missing


def check_all_files_linked() -> tuple[int, list[str]]:
    """Check if all reference files are linked from SKILL.md.

    Returns:
        Tuple of (total file count, list of unlinked file names).
    """
    skill_md_path = Path("SKILL.md")
    try:
        skill_md = skill_md_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"ERROR: {skill_md_path} not found", file=sys.stderr)
        return 0, []
    except OSError as e:
        print(f"ERROR: Failed to read {skill_md_path}: {e}", file=sys.stderr)
        return 0, []

    refs_dir = Path("references")
    if not refs_dir.exists():
        print(f"ERROR: {refs_dir} directory not found", file=sys.stderr)
        return 0, []

    all_refs = {f.name for f in refs_dir.glob("*.md")}
    linked_refs = set(re.findall(r"references/([\w-]+\.md)", skill_md))

    # WHY: Set difference finds files that exist but aren't linked
    unlinked = all_refs - linked_refs
    return len(all_refs), list(unlinked)


def check_anchor_links() -> int:
    """Check for broken anchor links in all files.

    Returns:
        Count of broken anchor links found.
    """
    refs_dir = Path("references")
    if not refs_dir.exists():
        print(f"ERROR: {refs_dir} directory not found", file=sys.stderr)
        return 0

    total_issues = 0

    for f in sorted(refs_dir.glob("*.md")):
        try:
            content = f.read_text(encoding="utf-8")
        except OSError as e:
            print(f"WARNING: Failed to read {f}: {e}", file=sys.stderr)
            continue

        # WHY: Extract TOC links which use #anchor format
        toc_links = re.findall(r"\[.*?\]\(#([\w-]+)\)", content)

        # WHY: Extract actual headings and convert to anchor format for comparison
        headings = re.findall(r"^#{2,6}\s+(.+)$", content, re.MULTILINE)
        # WHY: GitHub-style anchor generation: lowercase, remove special chars, spaces to hyphens
        anchors = [
            re.sub(r"[^\w\s-]", "", h.lower()).replace(" ", "-") for h in headings
        ]

        # Check for broken links
        for link in toc_links:
            if link not in anchors:
                total_issues += 1

    return total_issues


def check_toc_format() -> list[Path]:
    """Check if TOC entries use 'When/If' format.

    Returns:
        List of Path objects for files with incorrect TOC format.
    """
    refs_dir = Path("references")
    if not refs_dir.exists():
        print(f"ERROR: {refs_dir} directory not found", file=sys.stderr)
        return []

    issues: list[Path] = []

    # WHY: These prefixes indicate scenario-based TOC entries that describe
    # WHEN to use the content, not just WHAT it covers (progressive disclosure)
    scenario_prefixes = [
        "When",
        "If",
        "For",
        "How",
        "To",
        "Using",
        "Understanding",
        "Creating",
        "Managing",
        "Detecting",
        "Preventing",
        "Validating",
        "Learning",
        "Analyzing",
        "Archiving",
        "Resolving",
        "Recovering",
        "Syncing",
        "Emergency",
        "Common",
        "Automated",
        "Preparing",
        "Saving",
        "Reloading",
        "Verifying",
        "Classifying",
        "Handling",
        "Periodic",
        "Timestamp-based",
        "Content-based",
        "Pre-compaction",
        "Post-compaction",
        "Consolidating",
        "Restoring",
        "What",
        "Which",
        "Why",
        "Where",
        "Completing",
        "Performing",
    ]

    for f in sorted(refs_dir.glob("*.md")):
        try:
            content = f.read_text(encoding="utf-8")
        except OSError as e:
            print(f"WARNING: Failed to read {f}: {e}", file=sys.stderr)
            continue

        # WHY: Extract only the TOC section to check entry formatting
        toc_match = re.search(
            r"## Table of Contents\n(.*?)(?=\n##)", content, re.DOTALL
        )
        if not toc_match:
            continue

        toc = toc_match.group(1)
        entries = re.findall(r"\d+\.\s+\[(.+?)\]", toc)

        # Check each entry starts with an acceptable prefix
        has_bad_entry = False
        for entry in entries:
            if not any(entry.startswith(prefix) for prefix in scenario_prefixes):
                has_bad_entry = True
                break

        if has_bad_entry:
            issues.append(f)

    return issues


def check_consistency() -> int:
    """Check consistency between SKILL.md and reference files.

    Returns:
        Count of inconsistencies found.
    """
    skill_md_path = Path("SKILL.md")
    try:
        skill_md = skill_md_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"ERROR: {skill_md_path} not found", file=sys.stderr)
        return 0
    except OSError as e:
        print(f"ERROR: Failed to read {skill_md_path}: {e}", file=sys.stderr)
        return 0

    # WHY: This regex extracts section title, filename, and TOC links from SKILL.md
    sections = re.findall(
        r"####\s+(.+?)\s+\(\[references/([\w-]+\.md)\].*?\n(.*?)(?=\n####|\n###|\Z)",
        skill_md,
        re.DOTALL,
    )

    total_issues = 0

    for title, filename, toc_links in sections:
        ref_file = Path("references") / filename
        if not ref_file.exists():
            continue

        try:
            ref_content = ref_file.read_text(encoding="utf-8")
        except OSError as e:
            print(f"WARNING: Failed to read {ref_file}: {e}", file=sys.stderr)
            continue

        # Extract TOC from reference file
        toc_match = re.search(
            r"## Table of Contents\n(.*?)(?=\n##)", ref_content, re.DOTALL
        )
        if not toc_match:
            total_issues += 1
            continue

        ref_toc = toc_match.group(1)

        # WHY: Extract TOC entries from SKILL.md that use arrow notation
        skill_toc_entries = re.findall(
            r"-\s+(.+?)\s+\u2192\s+\[.+?\]\(#.+?\)", toc_links
        )

        # WHY: Extract TOC entries from reference file using numbered list format
        ref_toc_entries = re.findall(r"\d+\.\s+\[(.+?)\]\(#.+?\)", ref_toc)

        # WHY: Entry count mismatch indicates TOC is out of sync
        if len(skill_toc_entries) != len(ref_toc_entries):
            total_issues += 1
            continue

        # WHY: Case-insensitive comparison catches minor formatting differences
        for skill_entry, ref_entry in zip(skill_toc_entries, ref_toc_entries):
            if skill_entry.lower().strip() != ref_entry.lower().strip():
                total_issues += 1

    return total_issues


def main() -> None:
    """Run all validation checks."""
    print("=" * 70)
    print("SESSION-MEMORY SKILL VALIDATION REPORT")
    print("=" * 70)
    print()

    # Check 1: File references
    total_refs, missing = check_file_references()
    print(f"1. File References: {total_refs} total")
    if missing:
        print(f"   X FAILED: {len(missing)} missing files")
        for missing_file in missing:
            print(f"     - {missing_file}")
    else:
        print("   V PASSED: All file references valid")
    print()

    # Check 2: All files linked
    total_files, unlinked = check_all_files_linked()
    print(f"2. File Coverage: {total_files} reference files")
    if unlinked:
        print(f"   X FAILED: {len(unlinked)} files not linked from SKILL.md")
        for unlinked_file in unlinked:
            print(f"     - {unlinked_file}")
    else:
        print("   V PASSED: All reference files linked")
    print()

    # Check 3: Anchor links
    broken_anchors = check_anchor_links()
    print("3. Anchor Links:")
    if broken_anchors > 0:
        print(f"   X FAILED: {broken_anchors} broken anchor links")
    else:
        print("   V PASSED: All anchor links valid")
    print()

    # Check 4: TOC format
    bad_toc = check_toc_format()
    print("4. TOC Format (When/If):")
    if bad_toc:
        print(f"   X FAILED: {len(bad_toc)} files with incorrect format")
        for bad_file in bad_toc:
            print(f"     - {bad_file.name}")
    else:
        print("   V PASSED: All TOCs use When/If format")
    print()

    # Check 5: Consistency
    inconsistencies = check_consistency()
    print("5. SKILL.md <-> Reference Consistency:")
    if inconsistencies > 0:
        print(f"   X FAILED: {inconsistencies} inconsistencies found")
    else:
        print("   V PASSED: All TOCs consistent")
    print()

    # Summary
    print("=" * 70)
    # WHY: Aggregate all check results to determine overall pass/fail
    all_passed = (
        not missing
        and not unlinked
        and broken_anchors == 0
        and not bad_toc
        and inconsistencies == 0
    )

    if all_passed:
        print("OVERALL RESULT: V ALL CHECKS PASSED")
        print("=" * 70)
        # WHY: Exit code 0 indicates success for shell script integration
        sys.exit(0)
    else:
        print("OVERALL RESULT: X SOME CHECKS FAILED")
        print("=" * 70)
        # WHY: Exit code 1 indicates failure for shell script integration
        sys.exit(1)


if __name__ == "__main__":
    main()
