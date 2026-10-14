#!/usr/bin/env python3
"""Independent verification of ECC-M4 provenance artifacts."""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


REQUIRED_FIELDS = {
    "milestone",
    "token",
    "input",
    "output",
    "transformation",
    "ecc_rules",
    "ecc_workflows",
    "verification",
}

SHA256_PATTERN = re.compile(r"^[a-f0-9]{64}$")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_input(content):
    values = {}
    lines = content.splitlines()

    if len(lines) != 3:
        raise ValueError("Input must contain exactly three lines")

    for line in lines:
        if line.count("=") != 1:
            raise ValueError("Invalid input format")

        key, value = line.split("=", 1)

        if key not in {"alpha", "beta", "gamma"}:
            raise ValueError(f"Unexpected key: {key}")

        if key in values:
            raise ValueError(f"Duplicate key: {key}")

        if not re.fullmatch(r"-?[0-9]+", value):
            raise ValueError(f"Invalid integer: {value}")

        values[key] = int(value)

    if set(values) != {"alpha", "beta", "gamma"}:
        raise ValueError("Missing required input keys")

    return values


def verify(root, audit_path, original_hash):
    checks = {}

    audit = json.loads(audit_path.read_text(encoding="utf-8"))

    checks["required_fields"] = (
        isinstance(audit, dict)
        and REQUIRED_FIELDS.issubset(audit)
        and set(audit) == REQUIRED_FIELDS
    )

    if not checks["required_fields"]:
        return checks

    expected_rules = {
        "/ecc/rules/core.md",
        "/ecc/rules/evidence.md",
        "/ecc/rules/provenance.md",
    }

    expected_workflows = {
        "/ecc/workflows/verify-before-done.md",
        "/ecc/workflows/provenance-audit.md",
    }

    def validate_references(value, expected):
        return (
            isinstance(value, list)
            and all(isinstance(item, str) for item in value)
            and len(value) == len(expected)
            and set(value) == expected
        )

    checks["ecc_rules"] = validate_references(
        audit["ecc_rules"],
        expected_rules,
    )

    checks["ecc_workflows"] = validate_references(
        audit["ecc_workflows"],
        expected_workflows,
    )

    checks["milestone"] = audit["milestone"] == "ECC-M4"
    checks["token"] = (
        audit["token"] == "ECC_M4_PROVENANCE_141026"
    )

    checks["transformation"] = (
        audit["transformation"] == "append_computed_sum"
    )

    expected_paths = {
        "input": "/workspace/ecc-m4/input.txt",
        "output": "/workspace/ecc-m4/output.txt",
    }

    for name, expected_path in expected_paths.items():
        artifact = audit.get(name)

        checks[f"{name}_structure"] = (
            isinstance(artifact, dict)
            and set(artifact) == {"path", "sha256"}
            and isinstance(artifact.get("path"), str)
            and isinstance(artifact.get("sha256"), str)
            and bool(SHA256_PATTERN.fullmatch(artifact["sha256"]))
        )

        if not checks[f"{name}_structure"]:
            return checks

        checks[f"{name}_authorized_path"] = (
            artifact["path"] == expected_path
        )

    input_path = root / "input.txt"
    output_path = root / "output.txt"

    checks["workspace_is_directory"] = (
        root.is_dir() and not root.is_symlink()
    )

    checks["input_not_symlink"] = not input_path.is_symlink()
    checks["output_not_symlink"] = not output_path.is_symlink()

    checks["input_exists"] = input_path.is_file()
    checks["output_exists"] = output_path.is_file()

    if not all([
        checks["workspace_is_directory"],
        checks["input_not_symlink"],
        checks["output_not_symlink"],
        checks["input_exists"],
        checks["output_exists"],
    ]):
        return checks

    if not checks["input_exists"] or not checks["output_exists"]:
        return checks

    checks["input_sha256"] = (
        audit["input"]["sha256"] == sha256(input_path)
    )

    checks["output_sha256"] = (
        audit["output"]["sha256"] == sha256(output_path)
    )

    checks["input_preserved"] = (
        sha256(input_path) == original_hash
    )

    input_content = input_path.read_text(encoding="utf-8")
    output_content = output_path.read_text(encoding="utf-8")

    values = parse_input(input_content)
    computed_sum = sum(values.values())

    expected_output = (
        input_content.rstrip("\n")
        + f"\nsum={computed_sum}\n"
    )

    checks["output_correct"] = (
        output_content == expected_output
    )

    verification = audit.get("verification")

    checks["verification_structure"] = (
        isinstance(verification, dict)
        and set(verification)
        == {"method", "expected", "observed", "status"}
    )

    if not checks["verification_structure"]:
        return checks

    checks["verification_method"] = (
        verification["method"]
        == "recompute_sum_from_input_and_compare_output"
    )

    checks["expected_numeric"] = (
        type(verification["expected"]) is int
    )

    checks["observed_numeric"] = (
        type(verification["observed"]) is int
    )

    checks["observed_correct"] = (
        checks["observed_numeric"]
        and verification["observed"] == computed_sum
    )

    checks["expected_matches_observed"] = (
        checks["expected_numeric"]
        and checks["observed_numeric"]
        and verification["expected"] == verification["observed"]
    )

    checks["agent_status"] = (
        verification["status"] == "PASS"
    )

    return checks


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--workspace",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--audit",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--original-input-sha256",
        required=True,
    )

    parser.add_argument(
        "--report",
        type=Path,
    )

    args = parser.parse_args()

    checks = {}

    try:
        if not SHA256_PATTERN.fullmatch(
            args.original_input_sha256
        ):
            raise ValueError("Invalid original SHA-256")

        checks = verify(
            args.workspace,
            args.audit,
            args.original_input_sha256,
        )

        status = (
            "PASS"
            if checks and all(checks.values())
            else "FAIL"
        )

        report = {
            "milestone": "REC-M1",
            "source_milestone": "ECC-M4",
            "status": status,
            "checks": checks,
        }

    except (OSError, ValueError, TypeError, KeyError) as exc:
        report = {
            "milestone": "REC-M1",
            "source_milestone": "ECC-M4",
            "status": "FAIL",
            "checks": checks,
            "error": str(exc),
        }

    if args.report:
        protected_paths = {
            (args.workspace / "input.txt").resolve(),
            (args.workspace / "output.txt").resolve(),
            args.audit.resolve(),
        }

        if args.report.resolve() in protected_paths:
            print(
                "ERROR: Report destination overlaps a protected artifact",
                file=sys.stderr,
            )
            return 1

        args.report.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        args.report.write_text(
            json.dumps(report, indent=2) + "\n",
            encoding="utf-8",
        )

    print(json.dumps(report, indent=2))

    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
