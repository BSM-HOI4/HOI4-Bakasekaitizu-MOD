#!/usr/bin/env python3

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
VALIDATOR = REPO / "tools/atrmrw/validate_slot_contract.py"
CONTRACT = REPO / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE1_SLOT_CONTRACT.json"


class ValidateSlotContractTest(unittest.TestCase):
    def run_contract(self, payload: dict) -> subprocess.CompletedProcess[str]:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json") as handle:
            json.dump(payload, handle)
            handle.flush()
            return subprocess.run(
                [sys.executable, str(VALIDATOR), "--contract", handle.name],
                cwd=REPO,
                capture_output=True,
                text=True,
            )

    def test_checked_in_contract_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR)],
            cwd=REPO,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("85 hulls", result.stdout)

    def test_missing_logical_semantic_fails(self) -> None:
        payload = json.loads(CONTRACT.read_text(encoding="utf-8"))
        for slot in payload["profiles"]["maximum_36"]["slots"]:
            slot["semantic"] = [
                value for value in slot["semantic"] if value != "primary_sub_armament"
            ]
        result = self.run_contract(payload)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing logical armament semantics", result.stdout)

    def test_slot_total_mismatch_fails(self) -> None:
        payload = json.loads(CONTRACT.read_text(encoding="utf-8"))
        payload["profiles"]["capital_30"]["total_slot_count"] = 31
        result = self.run_contract(payload)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("total=31 but slots=30", result.stdout)

    def test_hidden_slot_fails(self) -> None:
        payload = json.loads(CONTRACT.read_text(encoding="utf-8"))
        payload["profiles"]["minimal_9"]["slots"][0]["id"] = "hidden_role_slot"
        result = self.run_contract(payload)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("hidden slots are prohibited", result.stdout)

    def test_non_contiguous_gui_index_fails(self) -> None:
        payload = json.loads(CONTRACT.read_text(encoding="utf-8"))
        payload["profiles"]["maximum_36"]["slots"][0]["ui_index"] = 9
        result = self.run_contract(payload)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("UI indices are not contiguous", result.stdout)

    def test_role_cannot_be_fixed(self) -> None:
        payload = json.loads(CONTRACT.read_text(encoding="utf-8"))
        payload["profiles"]["minimal_9"]["slots"][0]["state"] = "fixed_visible"
        result = self.run_contract(payload)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("role must be exactly one editable slot", result.stdout)

    def test_duplicate_gui_coordinate_fails(self) -> None:
        payload = json.loads(CONTRACT.read_text(encoding="utf-8"))
        slots = payload["profiles"]["maximum_36"]["slots"]
        slots[1]["x"], slots[1]["y"] = slots[0]["x"], slots[0]["y"]
        result = self.run_contract(payload)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate GUI coordinates", result.stdout)


if __name__ == "__main__":
    unittest.main()
