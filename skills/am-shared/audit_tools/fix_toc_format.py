#!/usr/bin/env python3
"""Fix TOC format violations by rewriting entries to start with 'When' or 'If'."""

# WHY: Future annotations enable forward references and modern type hint syntax
from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

# WHY: Using __file__ parent ensures script works relative to its own location
# The audit_tools directory is inside the skill directory, so we navigate up one level
SKILL_FILE = Path(__file__).resolve().parent.parent / "SKILL.md"

# WHY: Explicit mapping table enables deterministic, auditable transformations
# Mappings from incorrect to correct format
TOC_FIXES: dict[str, str] = {
    # Common patterns for conversion
    "Understanding the purpose": "When you need to understand the purpose",
    "Understanding what active context is": "When you need to understand what active context is",
    "Understanding directory structure": "When you need to understand directory structure",
    "Understanding directory meanings": "When you need to understand directory meanings",
    "Understanding validation levels": "When you need to understand validation levels",
    "Understanding tracker structure": "When you need to understand tracker structure",
    "Understanding task states": "When you need to understand task states",
    "Understanding dependency types": "When you need to understand dependency types",
    "Understanding recovery scenarios": "When you need to understand recovery scenarios",
    "Understanding compaction risks": "When you need to understand compaction risks",
    "Understanding update patterns overview": "When you need to understand update patterns overview",
    "Understanding pattern categories": "When you need to understand pattern categories",
    "Understanding what patterns are": "When you need to understand what patterns are",
    "Understanding category definitions": "When you need to understand category definitions",
    "Understanding file structure": "When you need to understand file structure",
    "Understanding snapshot structure": "When you need to understand snapshot structure",
    "Understanding archive organization": "When you need to understand archive organization",
    "Understanding context compaction": "When you need to understand context compaction",
    "Understanding context drift": "When you need to understand context drift",
    "Understanding validation rules": "When you need to understand validation rules",
    "Understanding corruption types": "When you need to understand corruption types",
    "Understanding conflict types": "When you need to understand conflict types",
    "Understanding resolution strategies": "When you need to understand resolution strategies",
    "Understanding detection methods": "When you need to understand detection methods",
    "Understanding config snapshots": "When you need to understand config snapshots",
    "Understanding available scripts": "When you need to understand available scripts",
    "Understanding compaction triggers": "When you need to understand compaction triggers",
    # "What" → "When you need to understand what"
    "What files to create initially": "When you need to know what files to create initially",
    "What to archive": "When you need to know what to archive",
    "What Are Patterns": "When you need to understand what patterns are",
    "What is Active Context": "When you need to understand what active context is",
    "What Is Context Drift": "When you need to understand what context drift is",
    "What Is A Config Snapshot": "When you need to understand what a config snapshot is",
    # "How to" → "When you need to know how to"
    "How to perform initialization": "When you need to know how to perform initialization",
    "How to verify initialization": "When you need to know how to verify initialization",
    "How to validate structure": "When you need to know how to validate structure",
    "How to update context": "When you need to know how to update context",
    "How to perform validation": "When you need to know how to perform validation",
    "How to follow validation checklist": "When you need to know how to follow validation checklist",
    "How to record patterns": "When you need to know how to record patterns",
    "How to manage tasks": "When you need to know how to manage tasks",
    "How to perform safe compaction": "When you need to know how to perform safe compaction",
    "How to rollback if needed": "When you need to know how to rollback if needed",
    "How to make go/no-go decision": "When you need to know how to make go/no-go decision",
    "How to recover": "When you need to know how to recover",
    "How to synchronize": "When you need to know how to synchronize",
    "How to archive": "When you need to know how to archive",
    "How to integrate": "When you need to know how to integrate",
    "How to use scripts": "When you need to know how to use scripts",
    "How to create snapshots": "When you need to know how to create snapshots",
    "How to detect changes": "When you need to know how to detect changes",
    "How to resolve conflicts": "When you need to know how to resolve conflicts",
    "How to choose categories": "When you need to know how to choose categories",
    # "Learning" → "When you need to learn"
    "Learning file naming rules": "When you need to learn file naming rules",
    # "For" → "When"
    "For implementation examples": "When you need implementation examples",
    # "To see" → "When you need to see"
    "To see canonical structure": "When you need to see canonical structure",
    # "Using" → "When you need to use"
    "Using validation scripts": "When you need to use validation scripts",
    "Using pattern notation": "When you need to use dependency notation",
    "Using the master checklist": "When you need to use the master checklist",
    "Using decision trees": "When you need to use decision trees",
    "Using update patterns": "When you need to use update patterns",
    # "Creating" → "When you need to create"
    "Creating context snapshots": "When you need to create context snapshots",
    "Creating progress snapshots": "When you need to create progress snapshots",
    # "Managing" → "When you need to manage"
    "Managing dependencies": "When you need to manage dependencies",
    "Managing active context": "When you need to manage active context",
    "Managing pattern index": "When you need to manage pattern index",
    # "Recording" → "When you need to record"
    "Recording dependencies": "When you need to record dependencies",
    # Specific patterns
    "Context update Triggers": "When to update context",
    "Update Procedures": "When you need to know update procedures",
    "Pattern Recording Procedure": "When you need to know pattern recording procedure",
    "Task Management Procedures": "When you need to know task management procedures",
    "Dependency Management": "When you need to manage dependencies",
    "Progress Snapshots": "When you need to create progress snapshots",
    "Recovery Procedures": "When you need to know recovery procedures",
    "Synchronization Procedures": "When you need to know synchronization procedures",
    "Validation Procedures": "When you need to know validation procedures",
    "Archival Procedures": "When you need to know archival procedures",
    "Integration Procedures": "When you need to know integration procedures",
    "Creation Procedures": "When you need to know creation procedures",
    "Detection Procedures": "When you need to know detection procedures",
    "Resolution Procedures": "When you need to know resolution procedures",
    "Script Usage Guide": "When you need to know script usage guide",
    "Common Workflows": "When you need to know common workflows",
    # Pruning and other actions
    "Context Pruning": "When you need to prune context",
    "Analyzing critical path": "When you need to analyze critical path",
    "Validating dependencies": "When you need to validate dependencies",
    "Performing consistency checks": "When you need to perform consistency checks",
    "Pre-compaction safety checks": "When you need to perform pre-compaction safety checks",
    "Post-compaction verification": "When you need to perform post-compaction verification",
    "Preventing corruption": "When you need to prevent corruption",
    "Emergency recovery procedures": "When you need to perform emergency recovery",
    "Automated validation": "When you need to use automated validation",
    "Common validation errors": "When you need to understand common validation errors",
    "Compaction Triggers": "When you need to understand compaction triggers",
    "Change Classification": "When you need to classify changes",
    "Completing preparation phase": "When you need to complete preparation phase",
    "Completing backup phase": "When you need to complete backup phase",
    "Completing validation phase": "When you need to complete validation phase",
    "Performing final verification": "When you need to perform final verification",
    # Specific use patterns
    "Using problem-solution patterns": "When you need to use problem-solution patterns",
    "Using workflow patterns": "When you need to use workflow patterns",
    "Using decision-logic patterns": "When you need to use decision-logic patterns",
    "Using error-recovery patterns": "When you need to use error-recovery patterns",
    "Using configuration patterns": "When you need to use configuration patterns",
    # Why patterns
    "Why snapshots matter": "When you need to understand why snapshots matter",
    "Why Snapshots Matter": "When you need to understand why snapshots matter",
}


def fix_toc_line(line: str) -> str:
    """Fix a single TOC line to start with 'When' or 'If'.

    Args:
        line: A single line from the markdown file

    Returns:
        The fixed line if a match was found, otherwise the original line
    """
    # WHY: Regex captures the three parts of a TOC entry for surgical replacement
    match = re.search(r"^(- )(.+?)( → \[.+?\]\(.+?\))$", line)
    if not match:
        return line

    prefix = match.group(1)
    description = match.group(2)
    suffix = match.group(3)

    # WHY: Early return avoids unnecessary processing for already-correct lines
    if description.startswith("When ") or description.startswith("If "):
        return line

    # WHY: Exact match first for performance, then case-insensitive fallback
    if description in TOC_FIXES:
        new_description = TOC_FIXES[description]
        return f"{prefix}{new_description}{suffix}"

    # WHY: Case-insensitive matching catches minor capitalization differences
    for old, new in TOC_FIXES.items():
        if description.lower() == old.lower():
            return f"{prefix}{new}{suffix}"

    # WHY: Returning original preserves unknown entries for manual review
    return line


def verify_output(file_path: Path, expected_lines: int) -> bool:
    """Verify the output file exists and has expected content.

    Args:
        file_path: Path to the file to verify
        expected_lines: Expected number of lines in the file

    Returns:
        True if verification passes, False otherwise
    """
    # WHY: Verification ensures atomic write completed successfully
    if not file_path.exists():
        print(f"ERROR: Output file does not exist: {file_path}", file=sys.stderr)
        return False

    # WHY: Line count check detects truncation or corruption during write
    with open(file_path, "r", encoding="utf-8") as f:
        actual_lines = len(f.readlines())

    if actual_lines != expected_lines:
        print(
            f"ERROR: Line count mismatch. Expected {expected_lines}, got {actual_lines}",
            file=sys.stderr,
        )
        return False

    # WHY: Size check ensures file is not empty or truncated
    if file_path.stat().st_size == 0:
        print(f"ERROR: Output file is empty: {file_path}", file=sys.stderr)
        return False

    return True


def main() -> int:
    """Fix all TOC entries in SKILL.md.

    Returns:
        0 on success, 1 on failure
    """
    try:
        print(f"Reading {SKILL_FILE}...")

        # WHY: Check file exists before attempting to read
        if not SKILL_FILE.exists():
            print(f"ERROR: File not found: {SKILL_FILE}", file=sys.stderr)
            return 1

        with open(SKILL_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()

        original_line_count = len(lines)
        fixed_count = 0

        for i, line in enumerate(lines):
            # WHY: Pattern matching identifies TOC entries for processing
            if re.match(r"^- .+ → \[.+?\]\(.+?\)$", line):
                fixed_line = fix_toc_line(line)
                if fixed_line != line:
                    print(f"Line {i + 1}: Fixed")
                    print(f"  Before: {line.rstrip()}")
                    print(f"  After:  {fixed_line.rstrip()}")
                    lines[i] = fixed_line
                    fixed_count += 1

        if fixed_count > 0:
            print(f"\nWriting changes to {SKILL_FILE}...")

            # WHY: Atomic write via temp file prevents corruption on crash/interrupt
            temp_dir = SKILL_FILE.parent
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=temp_dir,
                delete=False,
                suffix=".tmp",
            ) as temp_file:
                temp_path = Path(temp_file.name)
                temp_file.writelines(lines)

            # WHY: Rename is atomic on POSIX systems, ensuring file integrity
            temp_path.rename(SKILL_FILE)

            # WHY: Post-write verification catches silent write failures
            if not verify_output(SKILL_FILE, original_line_count):
                print("ERROR: Verification failed after write", file=sys.stderr)
                return 1

            print(f"Fixed {fixed_count} TOC entries")
        else:
            print("No changes needed")

        return 0

    except FileNotFoundError as e:
        print(f"ERROR: File not found: {e}", file=sys.stderr)
        return 1
    except PermissionError as e:
        print(f"ERROR: Permission denied: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"ERROR: OS error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    # WHY: sys.exit ensures proper exit codes for shell integration
    sys.exit(main())
