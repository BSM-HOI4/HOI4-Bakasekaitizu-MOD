#!/usr/bin/env python3

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.atrmrw.validate_japan_packing import validate


REPO = Path(__file__).resolve().parents[2]
PACKING = REPO / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE3_JAPAN_SLOT_PACKING.json"
CONTRACT = REPO / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE1_SLOT_CONTRACT.json"
LEDGER = REPO / "documents/00_coding_contexts/atrmrw/ATRMRW_PHASE3_JAPAN_PROTOTYPE_LEDGER.json"


class JapanPackingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.packing = json.loads(PACKING.read_text(encoding="utf-8"))
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

    def test_checked_in_packing_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(REPO / "tools/atrmrw/validate_japan_packing.py")],
            cwd=REPO,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("5 classes, 129 visible slots, hidden=0", result.stdout)

    def test_builder_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "packing.json"
            result = subprocess.run(
                [sys.executable, str(REPO / "tools/atrmrw/build_japan_packing.py"), "--output", str(output)],
                cwd=REPO,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), self.packing)

    def test_duplicate_slot_is_rejected(self) -> None:
        payload = copy.deepcopy(self.packing)
        payload["prototypes"][0]["slots"][1]["logical_slot_id"] = "role_slot"
        errors = validate(payload, self.contract, self.ledger)
        self.assertTrue(any("duplicate logical slot" in error for error in errors), errors)

    def test_non_structure_fixed_slot_is_rejected(self) -> None:
        payload = copy.deepcopy(self.packing)
        payload["prototypes"][0]["slots"][1]["state"] = "fixed_visible"
        errors = validate(payload, self.contract, self.ledger)
        self.assertTrue(any("only hull_structure" in error for error in errors), errors)

    def test_role_must_remain_editable(self) -> None:
        payload = copy.deepcopy(self.packing)
        payload["prototypes"][0]["slots"][0]["state"] = "locked_visible"
        errors = validate(payload, self.contract, self.ledger)
        self.assertTrue(any("role must be editable" in error for error in errors), errors)

    def test_unresolved_default_requires_reason(self) -> None:
        payload = copy.deepcopy(self.packing)
        yamato = payload["prototypes"][0]
        armor = next(slot for slot in yamato["slots"] if slot["logical_slot_id"] == "protection_slot_03")
        armor["default_module_id"] = None
        armor.pop("unresolved_reason", None)
        errors = validate(payload, self.contract, self.ledger)
        self.assertTrue(any("unresolved editable slot needs unresolved_reason" in error for error in errors), errors)

    def test_checked_in_packing_has_no_unresolved_defaults(self) -> None:
        unresolved = [
            f"{row['prototype_key']}/{slot['logical_slot_id']}"
            for row in self.packing["prototypes"]
            for slot in row["slots"]
            if slot["state"] == "editable" and slot.get("default_module_id") is None
        ]
        self.assertEqual(unresolved, [])


if __name__ == "__main__":
    unittest.main()
