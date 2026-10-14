"""Regression tests for the ECC-M4 independent verifier."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
FIXTURE = REPO / "evidence/experiments/ecc-m4"
VERIFIER = REPO / "evidence/tools/verify_audit.py"

ORIGINAL_SHA256 = (
    "5d4f21fe14cc96a1c1eda5e674fe897b47d461c4523b1e51eb97d78329fb0636"
)


class AuditVerifierTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="rec-m1-test-")
        self.addCleanup(self.temp.cleanup)

        self.root = Path(self.temp.name)

        for filename in ("input.txt", "output.txt", "audit.json"):
            (self.root / filename).write_bytes(
                (FIXTURE / filename).read_bytes()
            )

    def run_verifier(self):
        result = subprocess.run(
            [
                sys.executable,
                str(VERIFIER),
                "--workspace", str(self.root),
                "--audit", str(self.root / "audit.json"),
                "--original-input-sha256", ORIGINAL_SHA256,
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )

        report = json.loads(result.stdout)
        return result.returncode, report

    def mutate_audit(self, mutation):
        path = self.root / "audit.json"
        audit = json.loads(path.read_text(encoding="utf-8"))
        mutation(audit)
        path.write_text(json.dumps(audit), encoding="utf-8")

    def assert_rejected(self):
        code, report = self.run_verifier()
        self.assertNotEqual(code, 0)
        self.assertEqual(report["status"], "FAIL")

    def test_valid_fixture(self):
        code, report = self.run_verifier()
        self.assertEqual(code, 0)
        self.assertEqual(report["status"], "PASS")
        self.assertTrue(all(report["checks"].values()))

    def test_tampered_output(self):
        (self.root / "output.txt").write_text(
            "alpha=7\nbeta=11\ngamma=13\nsum=999\n"
        )
        self.assert_rejected()

    def test_incorrect_hash(self):
        self.mutate_audit(
            lambda a: a["output"].update({"sha256": "0" * 64})
        )
        self.assert_rejected()

    def test_missing_required_field(self):
        self.mutate_audit(lambda a: a.pop("transformation"))
        self.assert_rejected()

    def test_falsified_observation(self):
        self.mutate_audit(
            lambda a: a["verification"].update({"observed": 999})
        )
        self.assert_rejected()

    def test_invalid_workflows_type(self):
        self.mutate_audit(
            lambda a: a.update({"ecc_workflows": "not-an-array"})
        )
        self.assert_rejected()

    def test_unauthorized_input_path(self):
        self.mutate_audit(
            lambda a: a["input"].update(
                {"path": "/workspace/other/input.txt"}
            )
        )
        self.assert_rejected()

    def test_invalid_rules_type(self):
        self.mutate_audit(
            lambda a: a.update({"ecc_rules": [1, 2, 3]})
        )
        self.assert_rejected()

    def test_invalid_milestone_type(self):
        self.mutate_audit(
            lambda a: a.update({"milestone": ["ECC-M4"]})
        )
        self.assert_rejected()

    def test_invalid_verification_type(self):
        self.mutate_audit(
            lambda a: a.update({"verification": "PASS"})
        )
        self.assert_rejected()

    def test_malformed_json(self):
        (self.root / "audit.json").write_text(
            '{"milestone": "ECC-M4",'
        )
        self.assert_rejected()

    def test_output_symlink(self):
        output = self.root / "output.txt"
        external = self.root / "external-output.txt"

        external.write_bytes(output.read_bytes())
        output.unlink()
        output.symlink_to(external)

        self.assert_rejected()


    def test_unexpected_verification_property(self):
        self.mutate_audit(
            lambda a: a["verification"].update(
                {"untrusted_field": True}
            )
        )
        self.assert_rejected()

    def test_duplicate_ecc_rule(self):
        self.mutate_audit(
            lambda a: a["ecc_rules"].append(
                "/ecc/rules/core.md"
            )
        )
        self.assert_rejected()

    def test_unexpected_input_property(self):
        self.mutate_audit(
            lambda a: a["input"].update(
                {"untrusted_field": True}
            )
        )
        self.assert_rejected()


    def test_report_cannot_overwrite_artifacts(self):
        protected = (
            self.root / "input.txt",
            self.root / "output.txt",
            self.root / "audit.json",
        )

        for destination in protected:
            with self.subTest(destination=destination.name):
                original = destination.read_bytes()

                result = subprocess.run(
                    [
                        sys.executable,
                        str(VERIFIER),
                        "--workspace", str(self.root),
                        "--audit", str(self.root / "audit.json"),
                        "--original-input-sha256", ORIGINAL_SHA256,
                        "--report", str(destination),
                    ],
                    capture_output=True,
                    text=True,
                    timeout=15,
                )

                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(destination.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
