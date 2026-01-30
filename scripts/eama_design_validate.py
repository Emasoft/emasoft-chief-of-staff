#!/usr/bin/env python3
"""
EAMA Design Document Validator - Validate design document structure and frontmatter.

This script validates design documents for the emasoft-assistant-manager-agent:
1. Required frontmatter fields (uuid, title, status, created, updated)
2. UUID format compliance (GUUID-YYYYMMDD-NNNN)
3. Valid status enum values
4. Date format compliance (YYYY-MM-DD)
5. Document type consistency with folder location

Usage:
    python eama_design_validate.py design/pdr/auth-system.md
    python eama_design_validate.py --all
    python eama_design_validate.py --type pdr

Output Format (JSON):
    {
        "valid": true,
        "file_path": "design/pdr/auth-system.md",
        "errors": [],
        "warnings": []
    }
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class DesignDocumentValidator:
    """Validate design document structure and frontmatter."""

    # Required frontmatter fields
    REQUIRED_FIELDS = ["uuid", "title", "status", "created", "updated"]

    # Valid document types
    VALID_TYPES = ["pdr", "spec", "feature", "decision", "architecture", "template"]

    # Valid status values
    VALID_STATUSES = [
        "draft",
        "review",
        "approved",
        "implemented",
        "deprecated",
        "rejected",
    ]

    # UUID format: GUUID-YYYYMMDD-NNNN
    UUID_PATTERN = re.compile(r"^GUUID-(\d{4})(\d{2})(\d{2})-(\d{4})$")

    # Date format: YYYY-MM-DD
    DATE_PATTERN = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")

    def __init__(self, design_root: Path):
        """Initialize validator with design root directory.

        Args:
            design_root: Path to the design/ directory
        """
        self.design_root = design_root

    def parse_frontmatter(
        self, file_path: Path
    ) -> Tuple[Optional[Dict[str, Any]], int, List[str]]:
        """Parse YAML frontmatter from a markdown file with line tracking.

        Args:
            file_path: Path to the markdown file

        Returns:
            Tuple of (frontmatter dict, end line number, parse errors)
        """
        parse_errors: List[str] = []

        try:
            content = file_path.read_text(encoding="utf-8")
        except OSError as e:
            return None, 0, [f"Line 1: Cannot read file: {e}"]
        except UnicodeDecodeError as e:
            return None, 0, [f"Line 1: File encoding error: {e}"]

        lines = content.split("\n")

        # Check for opening delimiter
        if not lines or lines[0].strip() != "---":
            return None, 0, ["Line 1: Missing frontmatter opening delimiter '---'"]

        # Find closing delimiter
        end_idx = None
        for i, line in enumerate(lines[1:], start=2):
            if line.strip() == "---":
                end_idx = i
                break

        if end_idx is None:
            return None, 0, ["Frontmatter: Missing closing delimiter '---'"]

        # Parse frontmatter
        frontmatter: Dict[str, Any] = {}
        frontmatter["_file_path"] = str(file_path)
        frontmatter["_end_line"] = end_idx

        for line_num, line in enumerate(lines[1 : end_idx - 1], start=2):
            original_line = line
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            # Simple key: value parsing
            if ":" not in line:
                parse_errors.append(
                    f"Line {line_num}: Invalid format, expected 'key: value': {original_line}"
                )
                continue

            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()

            # Remove quotes if present
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]

            frontmatter[key] = value
            frontmatter[f"_line_{key}"] = line_num

        return frontmatter, end_idx, parse_errors

    def validate_uuid(self, uuid: str, line_num: int) -> List[str]:
        """Validate UUID format and date validity.

        Args:
            uuid: UUID string to validate
            line_num: Line number for error reporting

        Returns:
            List of validation errors
        """
        errors: List[str] = []

        match = self.UUID_PATTERN.match(uuid)
        if not match:
            errors.append(
                f"Line {line_num}: Invalid UUID format '{uuid}'. Expected: GUUID-YYYYMMDD-NNNN"
            )
            return errors

        year, month, day, sequence = match.groups()
        year, month, day, sequence = int(year), int(month), int(day), int(sequence)

        # Validate date components
        if month < 1 or month > 12:
            errors.append(f"Line {line_num}: Invalid month in UUID: {month}")
        if day < 1 or day > 31:
            errors.append(f"Line {line_num}: Invalid day in UUID: {day}")
        if sequence < 1:
            errors.append(f"Line {line_num}: Sequence number must be >= 1: {sequence}")

        return errors

    def validate_date(self, date_str: str, field_name: str, line_num: int) -> List[str]:
        """Validate date format and validity.

        Args:
            date_str: Date string to validate
            field_name: Name of the field for error messages
            line_num: Line number for error reporting

        Returns:
            List of validation errors
        """
        errors: List[str] = []

        match = self.DATE_PATTERN.match(date_str)
        if not match:
            errors.append(
                f"Line {line_num}: Invalid {field_name} format '{date_str}'. Expected: YYYY-MM-DD"
            )
            return errors

        _, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))

        if month < 1 or month > 12:
            errors.append(f"Line {line_num}: Invalid month in {field_name}: {month}")
        if day < 1 or day > 31:
            errors.append(f"Line {line_num}: Invalid day in {field_name}: {day}")

        return errors

    def validate_file(self, file_path: Path) -> Dict[str, Any]:
        """Validate a single design document.

        Args:
            file_path: Path to the document to validate

        Returns:
            Validation result dictionary
        """
        errors: List[str] = []
        warnings: List[str] = []

        # Check file exists
        if not file_path.exists():
            return {
                "valid": False,
                "file_path": str(file_path),
                "errors": [f"File not found: {file_path}"],
                "warnings": [],
            }

        # Check file extension
        if file_path.suffix != ".md":
            warnings.append(
                f"Line 0: File does not have .md extension: {file_path.suffix}"
            )

        # Parse frontmatter
        frontmatter, end_line, parse_errors = self.parse_frontmatter(file_path)
        errors.extend(parse_errors)

        if frontmatter is None:
            return {
                "valid": False,
                "file_path": str(file_path),
                "errors": errors,
                "warnings": warnings,
            }

        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in frontmatter:
                errors.append(f"Frontmatter: Missing required field '{field}'")

        # Validate UUID
        if "uuid" in frontmatter:
            line_num = frontmatter.get("_line_uuid", end_line)
            errors.extend(self.validate_uuid(frontmatter["uuid"], line_num))

        # Validate status
        if "status" in frontmatter:
            if frontmatter["status"] not in self.VALID_STATUSES:
                line_num = frontmatter.get("_line_status", end_line)
                errors.append(
                    f"Line {line_num}: Invalid status '{frontmatter['status']}'. "
                    f"Valid values: {', '.join(self.VALID_STATUSES)}"
                )

        # Validate dates
        if "created" in frontmatter:
            line_num = frontmatter.get("_line_created", end_line)
            errors.extend(
                self.validate_date(frontmatter["created"], "created", line_num)
            )

        if "updated" in frontmatter:
            line_num = frontmatter.get("_line_updated", end_line)
            errors.extend(
                self.validate_date(frontmatter["updated"], "updated", line_num)
            )

        # Validate type consistency with folder
        if "type" in frontmatter:
            try:
                relative = file_path.relative_to(self.design_root)
                if relative.parts:
                    folder_type = relative.parts[0]
                    if (
                        folder_type in self.VALID_TYPES
                        and folder_type != frontmatter["type"]
                    ):
                        line_num = frontmatter.get("_line_type", end_line)
                        warnings.append(
                            f"Line {line_num}: Type '{frontmatter['type']}' does not match "
                            f"folder '{folder_type}'"
                        )
            except ValueError:
                pass

        # Check for recommended fields
        recommended = ["description", "author"]
        for field in recommended:
            if field not in frontmatter:
                warnings.append(f"Frontmatter: Missing recommended field '{field}'")

        # Compute relative path for output
        try:
            relative_path = file_path.relative_to(self.design_root.parent)
        except ValueError:
            relative_path = file_path

        return {
            "valid": len(errors) == 0,
            "file_path": str(relative_path),
            "errors": errors,
            "warnings": warnings,
        }

    def validate_all(self, doc_type: Optional[str] = None) -> Dict[str, Any]:
        """Validate all design documents.

        Args:
            doc_type: Optional type filter

        Returns:
            Summary of validation results
        """
        results: List[Dict[str, Any]] = []

        # Find files to validate
        if doc_type:
            type_dir = self.design_root / doc_type
            if not type_dir.exists():
                return {
                    "valid": False,
                    "results": [],
                    "summary": {
                        "total": 0,
                        "valid": 0,
                        "invalid": 0,
                        "total_errors": 0,
                        "total_warnings": 0,
                    },
                    "error": f"Type directory not found: {type_dir}",
                }
            files = list(type_dir.glob("**/*.md"))
        else:
            files = list(self.design_root.glob("**/*.md"))

        # Validate each file
        for file_path in files:
            result = self.validate_file(file_path)
            results.append(result)

        # Compute summary
        total_errors = sum(len(r["errors"]) for r in results)
        total_warnings = sum(len(r["warnings"]) for r in results)
        valid_count = sum(1 for r in results if r["valid"])

        return {
            "valid": total_errors == 0,
            "results": results,
            "summary": {
                "total": len(results),
                "valid": valid_count,
                "invalid": len(results) - valid_count,
                "total_errors": total_errors,
                "total_warnings": total_warnings,
            },
        }


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate design document structure and frontmatter for assistant-manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Validate a single file
    %(prog)s design/pdr/auth-system.md

    # Validate all documents
    %(prog)s --all

    # Validate all documents of a specific type
    %(prog)s --all --type pdr

    # Verbose output with all warnings
    %(prog)s design/pdr/auth-system.md --verbose
        """,
    )

    parser.add_argument(
        "file",
        nargs="?",
        type=Path,
        help="Path to design document to validate",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all design documents",
    )
    parser.add_argument(
        "--type",
        dest="doc_type",
        choices=DesignDocumentValidator.VALID_TYPES,
        help="Filter by document type (with --all)",
    )
    parser.add_argument(
        "--design-dir",
        type=Path,
        help="Path to design directory (default: ../design from script location)",
    )
    parser.add_argument(
        "--format",
        choices=["json", "text"],
        default="json",
        help="Output format (default: json)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show warnings in text output",
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.file and not args.all:
        parser.error("Either provide a file path or use --all")

    # Determine design directory
    if args.design_dir:
        design_dir = args.design_dir
    else:
        design_dir = Path(__file__).parent.parent / "design"

    if not design_dir.exists():
        error_result = {
            "valid": False,
            "errors": [f"Design directory not found: {design_dir}"],
            "warnings": [],
        }
        if args.format == "json":
            print(json.dumps(error_result, indent=2))
        else:
            print(f"Error: Design directory not found: {design_dir}")
        sys.exit(1)

    validator = DesignDocumentValidator(design_dir)

    # Perform validation
    if args.all:
        result = validator.validate_all(doc_type=args.doc_type)
    else:
        result = validator.validate_file(args.file)

    # Output results
    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        # Text format
        if args.all:
            print("Design Document Validation Summary")
            print("=" * 50)
            print(f"Total documents: {result['summary']['total']}")
            print(f"Valid: {result['summary']['valid']}")
            print(f"Invalid: {result['summary']['invalid']}")
            print(f"Total errors: {result['summary']['total_errors']}")
            print(f"Total warnings: {result['summary']['total_warnings']}")
            print()

            for doc_result in result["results"]:
                if not doc_result["valid"] or (args.verbose and doc_result["warnings"]):
                    status = "VALID" if doc_result["valid"] else "INVALID"
                    print(f"[{status}] {doc_result['file_path']}")
                    for error in doc_result["errors"]:
                        print(f"  ERROR: {error}")
                    if args.verbose:
                        for warning in doc_result["warnings"]:
                            print(f"  WARNING: {warning}")
        else:
            status = "VALID" if result["valid"] else "INVALID"
            print(f"[{status}] {result['file_path']}")
            for error in result["errors"]:
                print(f"  ERROR: {error}")
            if args.verbose or not result["valid"]:
                for warning in result["warnings"]:
                    print(f"  WARNING: {warning}")

    # Exit with appropriate code
    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
